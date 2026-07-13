"""E2E tests for the CacheStorage domain (real browser flows).

Full end-to-end flows against a real Chrome browser, including
Cache API interaction via JS, CDP CacheStorage domain verification,
raw command sending, and edge cases.
"""

import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


async def _wait_for_page(page: CDPSession) -> str:
    await page.page.enable()
    nav_result = await page.page.navigate("https://example.com")
    frame_id = nav_result.get("frameId", "")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True,
        )
        if result.get("result", {}).get("value"):
            break
    return frame_id


async def _setup_cache(
    session: CDPSession,
    cache_name: str = "e2e-cache",
    url: str = "https://example.com/e2e-resource",
    body: str = "e2e cached body",
) -> dict[str, Any]:
    """Create a cache + entry via JS Cache API. Returns cache info."""
    await session.runtime.enable()
    await session.runtime.evaluate(
        f"""
        (async () => {{
            const cache = await caches.open('{cache_name}');
            const response = new Response('{body}', {{
                headers: {{'Content-Type': 'text/plain'}}
            }});
            await cache.put('{url}', response);
            return 'done';
        }})()
        """,
        return_by_value=True,
    )
    result = await session.cache_storage.request_cache_names(
        security_origin="https://example.com",
    )
    cache_id = None
    for c in result.get("caches", []):
        if c.get("cacheName") == cache_name:
            cache_id = c["cacheId"]
            break
    return {"cache_id": cache_id, "cache_name": cache_name, "url": url}


@pytest.mark.e2e
class TestCacheStorageE2E:
    async def test_request_cache_names_security_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            assert "caches" in result
            assert isinstance(result["caches"], list)

    async def test_request_cache_names_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names()
            assert "caches" in result

    async def test_request_cache_names_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            sk_result = await session.storage.get_storage_key()
            result = await session.cache_storage.request_cache_names(
                storage_key=sk_result["storageKey"],
            )
            assert "caches" in result

    async def test_create_cache_and_list_via_cdp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session, cache_name="e2e-list-cache")
            assert info["cache_id"] is not None

            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            cache_names = {c["cacheName"] for c in result.get("caches", [])}
            assert "e2e-list-cache" in cache_names

            await session.cache_storage.delete_cache(info["cache_id"])

    async def test_request_entries_after_create(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            assert "cacheDataEntries" in entries
            assert "returnCount" in entries
            assert entries["returnCount"] >= 1

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_verify_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(
                session, url="https://example.com/e2e-verify-url",
            )
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            urls = {e.get("requestURL") for e in entry_list}
            assert "https://example.com/e2e-verify-url" in urls

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_cached_response_body(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(
                session, body="e2e response body content",
            )
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                request_headers = entry_list[0].get("requestHeaders", [])
                result = await session.cache_storage.request_cached_response(
                    cache_id, request_url, request_headers,
                )
                assert "response" in result

            await session.cache_storage.delete_cache(cache_id)

    async def test_delete_entry_and_verify_removed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                await session.cache_storage.delete_entry(cache_id, request_url)

                entries_after = await session.cache_storage.request_entries(cache_id)
                after_urls = {
                    e.get("requestURL")
                    for e in entries_after.get("cacheDataEntries", [])
                }
                assert request_url not in after_urls

            await session.cache_storage.delete_cache(cache_id)

    async def test_delete_cache_and_verify_removed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session, cache_name="e2e-delete-verify")
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            await session.cache_storage.delete_cache(cache_id)

            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            cache_names = {c["cacheName"] for c in result.get("caches", [])}
            assert "e2e-delete-verify" not in cache_names

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session, cache_name="e2e-lifecycle")
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            assert entries["returnCount"] >= 1

            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                request_headers = entry_list[0].get("requestHeaders", [])
                cached = await session.cache_storage.request_cached_response(
                    cache_id, request_url, request_headers,
                )
                assert "response" in cached

                await session.cache_storage.delete_entry(cache_id, request_url)

                entries_after = await session.cache_storage.request_entries(cache_id)
                assert entries_after["returnCount"] == 0

            await session.cache_storage.delete_cache(cache_id)

            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            names = {c["cacheName"] for c in result.get("caches", [])}
            assert "e2e-lifecycle" not in names

    async def test_request_entries_with_path_filter(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(
                session, url="https://example.com/api/data",
            )
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(
                cache_id, path_filter="/api/",
            )
            assert "cacheDataEntries" in entries

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_with_skip_and_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(
                cache_id, skip_count=0, page_size=10,
            )
            assert "cacheDataEntries" in entries

            await session.cache_storage.delete_cache(cache_id)

    async def test_raw_send_request_cache_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.send(
                "CacheStorage.requestCacheNames",
                {"securityOrigin": "https://example.com"},
            )
            assert "caches" in result

    async def test_raw_send_request_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            result = await session.send(
                "CacheStorage.requestEntries",
                {"cacheId": cache_id},
            )
            assert "cacheDataEntries" in result

            await session.send("CacheStorage.deleteCache", {"cacheId": cache_id})

    async def test_raw_send_delete_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session, cache_name="e2e-raw-delete")
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            result = await session.send(
                "CacheStorage.deleteCache", {"cacheId": cache_id},
            )
            assert isinstance(result, dict)

    async def test_raw_send_delete_entry(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                result = await session.send(
                    "CacheStorage.deleteEntry",
                    {"cacheId": cache_id, "request": request_url},
                )
                assert isinstance(result, dict)

            await session.cache_storage.delete_cache(cache_id)

    async def test_raw_send_request_cached_response(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                request_headers = entry_list[0].get("requestHeaders", [])
                result = await session.send(
                    "CacheStorage.requestCachedResponse",
                    {
                        "cacheId": cache_id,
                        "requestURL": request_url,
                        "requestHeaders": request_headers,
                    },
                )
                assert "response" in result

            await session.cache_storage.delete_cache(cache_id)

    async def test_all_methods_return_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            r1 = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            assert isinstance(r1, dict)

            caches = r1.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                r2 = await session.cache_storage.request_entries(cache_id)
                assert isinstance(r2, dict)

    async def test_multiple_caches_create_and_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.runtime.enable()
            await session.runtime.evaluate(
                """
                (async () => {
                    await caches.open('e2e-multi-1');
                    await caches.open('e2e-multi-2');
                    return 'done';
                })()
                """,
                return_by_value=True,
            )
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            names = {c["cacheName"] for c in result.get("caches", [])}
            assert "e2e-multi-1" in names
            assert "e2e-multi-2" in names

            for c in result.get("caches", []):
                if c["cacheName"].startswith("e2e-multi-"):
                    await session.cache_storage.delete_cache(c["cacheId"])

    async def test_request_entries_empty_cache_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.request_entries("")

    async def test_delete_nonexistent_cache_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.delete_cache("nonexistent-id-12345")

    async def test_request_cached_response_nonexistent(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.request_cached_response(
                    "nonexistent-id", "https://example.com", [],
                )

    async def test_cache_entry_with_special_chars_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.runtime.enable()
            await session.runtime.evaluate(
                """
                (async () => {
                    const cache = await caches.open('e2e-special-chars');
                    const response = new Response('special', {
                        headers: {'Content-Type': 'text/plain'}
                    });
                    await cache.put('https://example.com/path?q=hello&lang=es', response);
                    return 'done';
                })()
                """,
                return_by_value=True,
            )
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            cache_id = None
            for c in result.get("caches", []):
                if c["cacheName"] == "e2e-special-chars":
                    cache_id = c["cacheId"]
                    break

            if cache_id:
                entries = await session.cache_storage.request_entries(cache_id)
                entry_list = entries.get("cacheDataEntries", [])
                urls = {e.get("requestURL") for e in entry_list}
                assert any("q=hello" in u for u in urls)
                await session.cache_storage.delete_cache(cache_id)

    async def test_cache_entry_with_unicode_body(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(
                session, body="unicode content ñ üñîçödé 🎉",
            )
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                request_headers = entry_list[0].get("requestHeaders", [])
                result = await session.cache_storage.request_cached_response(
                    cache_id, request_url, request_headers,
                )
                assert "response" in result

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_omitempty_no_optional_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            assert "cacheDataEntries" in entries
            assert "returnCount" in entries

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_large_skip_count(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(
                cache_id, skip_count=999,
            )
            assert entries["returnCount"] == 0

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_page_size_one(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.runtime.enable()
            await session.runtime.evaluate(
                """
                (async () => {
                    const cache = await caches.open('e2e-page-size-1');
                    for (let i = 0; i < 5; i++) {
                        const resp = new Response('body' + i);
                        await cache.put('https://example.com/item' + i, resp);
                    }
                    return 'done';
                })()
                """,
                return_by_value=True,
            )
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            cache_id = None
            for c in result.get("caches", []):
                if c["cacheName"] == "e2e-page-size-1":
                    cache_id = c["cacheId"]
                    break

            if cache_id:
                entries = await session.cache_storage.request_entries(
                    cache_id, page_size=1,
                )
                assert len(entries.get("cacheDataEntries", [])) <= 1
                await session.cache_storage.delete_cache(cache_id)

    async def test_delete_entry_then_delete_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _setup_cache(session, cache_name="e2e-delete-then-cache")
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache created")

            entries = await session.cache_storage.request_entries(cache_id)
            for entry in entries.get("cacheDataEntries", []):
                await session.cache_storage.delete_entry(
                    cache_id, entry.get("requestURL", ""),
                )

            await session.cache_storage.delete_cache(cache_id)

    async def test_repeated_request_cache_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            for _ in range(3):
                result = await session.cache_storage.request_cache_names(
                    security_origin="https://example.com",
                )
                assert "caches" in result

    async def test_request_cache_names_invalid_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.request_cache_names(
                    security_origin="not-a-valid-origin",
                )
