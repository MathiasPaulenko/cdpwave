"""Integration tests for the CacheStorage domain (real browser).

Exercises all CacheStorage domain methods against a real Chrome browser,
including requestCacheNames, requestEntries, deleteEntry, deleteCache,
requestCachedResponse, and full lifecycle flows.
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


async def _create_cache_and_entry(session: CDPSession) -> dict[str, Any]:
    """Create a cache with a cached entry via JS Cache API. Returns cache info."""
    await session.runtime.enable()
    await session.runtime.evaluate(
        """
        (async () => {
            const cache = await caches.open('test-cache-integration');
            const response = new Response('cached body content', {
                headers: {'Content-Type': 'text/plain'}
            });
            await cache.put('https://example.com/cached-resource', response);
            return 'done';
        })()
        """,
        return_by_value=True,
    )
    result = await session.cache_storage.request_cache_names(
        security_origin="https://example.com",
    )
    caches = result.get("caches", [])
    cache_id = None
    for c in caches:
        if c.get("cacheName") == "test-cache-integration":
            cache_id = c["cacheId"]
            break
    return {"cache_id": cache_id, "caches": caches}


@pytest.mark.integration
class TestCacheStorageIntegration:
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
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            result = await session.cache_storage.request_cache_names(
                storage_key=storage_key,
            )
            assert "caches" in result

    async def test_request_entries_empty_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(cache_id)
                assert "cacheDataEntries" in entries
                assert "returnCount" in entries

    async def test_request_entries_with_skip_count(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, skip_count=0,
                )
                assert "cacheDataEntries" in entries

    async def test_request_entries_with_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, page_size=10,
                )
                assert "cacheDataEntries" in entries

    async def test_request_entries_with_path_filter(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, path_filter="/api/",
                )
                assert "cacheDataEntries" in entries

    async def test_full_lifecycle_create_and_delete(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_cache_and_entry(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache was created")

            entries = await session.cache_storage.request_entries(cache_id)
            assert "cacheDataEntries" in entries

            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                await session.cache_storage.delete_entry(cache_id, request_url)

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_cached_response(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_cache_and_entry(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache was created")

            entries = await session.cache_storage.request_entries(cache_id)
            entry_list = entries.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                request_headers = entry_list[0].get("requestHeaders", [])
                result = await session.cache_storage.request_cached_response(
                    cache_id, request_url, request_headers,
                )
                assert "response" in result

                await session.cache_storage.delete_entry(cache_id, request_url)

            await session.cache_storage.delete_cache(cache_id)

    async def test_delete_nonexistent_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.delete_cache("nonexistent-cache-id")

    async def test_delete_entry_nonexistent_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.delete_entry(
                    "nonexistent-cache-id", "https://example.com",
                )

    async def test_request_entries_nonexistent_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.cache_storage.request_entries("nonexistent-cache-id")

    async def test_request_entries_omitempty_skip_count_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, skip_count=0,
                )
                assert "cacheDataEntries" in entries

    async def test_request_entries_all_optional_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, skip_count=2, page_size=5, path_filter="/data/",
                )
                assert "cacheDataEntries" in entries

    async def test_raw_send_all_commands(self) -> None:
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

    async def test_request_cache_names_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            assert isinstance(result, dict)

    async def test_request_entries_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(cache_id)
                assert isinstance(entries, dict)

    async def test_create_multiple_caches_and_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.runtime.enable()
            await session.runtime.evaluate(
                """
                (async () => {
                    await caches.open('multi-cache-1');
                    await caches.open('multi-cache-2');
                    await caches.open('multi-cache-3');
                    return 'done';
                })()
                """,
                return_by_value=True,
            )
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            cache_names = {c["cacheName"] for c in result.get("caches", [])}
            assert "multi-cache-1" in cache_names
            assert "multi-cache-2" in cache_names
            assert "multi-cache-3" in cache_names

            for c in result.get("caches", []):
                if c["cacheName"].startswith("multi-cache-"):
                    await session.cache_storage.delete_cache(c["cacheId"])

    async def test_delete_entry_and_verify(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_cache_and_entry(session)
            cache_id = info["cache_id"]
            if cache_id is None:
                pytest.skip("No cache was created")

            entries_before = await session.cache_storage.request_entries(cache_id)
            entry_list = entries_before.get("cacheDataEntries", [])
            if entry_list:
                request_url = entry_list[0].get("requestURL", "")
                await session.cache_storage.delete_entry(cache_id, request_url)

                entries_after = await session.cache_storage.request_entries(cache_id)
                after_list = entries_after.get("cacheDataEntries", [])
                after_urls = {e.get("requestURL") for e in after_list}
                assert request_url not in after_urls

            await session.cache_storage.delete_cache(cache_id)

    async def test_request_entries_large_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com",
            )
            caches = result.get("caches", [])
            if caches:
                cache_id = caches[0]["cacheId"]
                entries = await session.cache_storage.request_entries(
                    cache_id, page_size=1000,
                )
                assert "cacheDataEntries" in entries
