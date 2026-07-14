"""E2E tests for the Storage domain.

These tests exercise the full CDP pipeline: launch a real browser,
navigate to a page, set and read cookies, check quotas, clear data,
and verify side effects through the DOM/Runtime.
"""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_browser


def _browser_available() -> bool:
    try:
        return find_browser() is not None
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _browser_available(),
    reason="No Chromium-based browser found",
)


async def _wait_for_page(page: CDPSession, url: str = "https://example.com") -> None:
    await page.page.enable()
    await page.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestStorageE2E:
    async def test_set_get_clear_cookies_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_cookies([
                {
                    "name": "e2e-test",
                    "value": "12345",
                    "domain": ".example.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": True,
                },
            ])

            result = await session.storage.get_cookies()
            cookies = result["cookies"]
            test_cookie = [c for c in cookies if c["name"] == "e2e-test"]
            assert len(test_cookie) == 1
            assert test_cookie[0]["value"] == "12345"
            assert test_cookie[0]["httpOnly"] is True

            await session.storage.clear_cookies()

            result = await session.storage.get_cookies()
            remaining = [c for c in result["cookies"] if c["name"] == "e2e-test"]
            assert remaining == []

    async def test_get_usage_and_quota_returns_valid_numbers(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.get_usage_and_quota("https://example.com")
            assert isinstance(result["usage"], (int, float))
            assert isinstance(result["quota"], (int, float))
            assert result["quota"] > 0
            assert isinstance(result["overrideActive"], bool)
            assert "usageBreakdown" in result
            assert isinstance(result["usageBreakdown"], list)

    async def test_clear_data_for_origin_removes_cookies(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_cookies([
                {"name": "clear-me", "value": "1", "domain": ".example.com"},
            ])

            before = await session.storage.get_cookies()
            assert any(c["name"] == "clear-me" for c in before["cookies"])

            await session.storage.clear_data_for_origin("https://example.com", "cookies")

            after = await session.storage.get_cookies()
            assert not any(c["name"] == "clear-me" for c in after["cookies"])

    @pytest.mark.skip(reason="Storage.getStorageKey unsupported in CI Chrome")
    async def test_get_storage_key_for_current_target(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.get_storage_key()
            assert "storageKey" in result
            assert isinstance(result["storageKey"], str)
            assert len(result["storageKey"]) > 0

    @pytest.mark.skip(reason="Storage.getStorageKey unsupported in CI Chrome")
    async def test_get_storage_key_with_frame_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            frame_tree = await session.page.get_frame_tree()
            frame_id = frame_tree["frame"]["id"]

            result = await session.storage.get_storage_key(frame_id)
            assert "storageKey" in result
            assert isinstance(result["storageKey"], str)

    async def test_override_quota_then_reset(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.override_quota_for_origin(
                "https://example.com", quota_size=50_000_000.0,
            )

            result = await session.storage.get_usage_and_quota("https://example.com")
            assert result["overrideActive"] is True

            await session.storage.override_quota_for_origin("https://example.com")

            result = await session.storage.get_usage_and_quota("https://example.com")
            assert result["overrideActive"] is False

    async def test_track_untrack_indexed_db_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.track_indexed_db_for_origin("https://example.com")
            await session.storage.untrack_indexed_db_for_origin("https://example.com")

    async def test_track_untrack_cache_storage_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.track_cache_storage_for_origin("https://example.com")
            await session.storage.untrack_cache_storage_for_origin("https://example.com")

    async def test_interest_group_tracking_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_interest_group_tracking(True)
            await session.storage.set_interest_group_tracking(False)

    async def test_interest_group_auction_tracking_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_interest_group_auction_tracking(True)
            await session.storage.set_interest_group_auction_tracking(False)

    async def test_shared_storage_tracking_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_shared_storage_tracking(True)
            await session.storage.set_shared_storage_tracking(False)

    async def test_storage_bucket_tracking_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            await session.storage.set_storage_bucket_tracking(
                "https://example.com", True,
            )
            await session.storage.set_storage_bucket_tracking(
                "https://example.com", False,
            )

    async def test_get_trust_tokens_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.get_trust_tokens()
            assert "tokens" in result
            assert isinstance(result["tokens"], list)

    async def test_clear_trust_tokens_returns_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.clear_trust_tokens("https://issuer.example.com")
            assert "didDeleteTokens" in result
            assert isinstance(result["didDeleteTokens"], bool)

    async def test_run_bounce_tracking_mitigations_returns_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.run_bounce_tracking_mitigations()
            assert "deletedSites" in result
            assert isinstance(result["deletedSites"], list)

    @pytest.mark.skip(reason="RelatedWebsiteSets fetch fails in CI Chrome")
    async def test_get_related_website_sets_returns_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            result = await session.storage.get_related_website_sets()
            assert "sets" in result
            assert isinstance(result["sets"], list)

    @pytest.mark.skip(reason="Storage.getStorageKey unsupported in CI Chrome")
    async def test_clear_data_for_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]

            await session.storage.clear_data_for_storage_key(storage_key, "all")

    @pytest.mark.skip(reason="Storage.getStorageKey unsupported in CI Chrome")
    async def test_track_untrack_indexed_db_for_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]

            await session.storage.track_indexed_db_for_storage_key(storage_key)
            await session.storage.untrack_indexed_db_for_storage_key(storage_key)

    @pytest.mark.skip(reason="Storage.getStorageKey unsupported in CI Chrome")
    async def test_track_untrack_cache_storage_for_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]

            await session.storage.track_cache_storage_for_storage_key(storage_key)
            await session.storage.untrack_cache_storage_for_storage_key(storage_key)

    @pytest.mark.skip(reason="Storage.getStorageKeyForFrame deprecated and fails in CI Chrome")
    async def test_get_storage_key_for_frame_deprecated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            frame_tree = await session.page.get_frame_tree()
            frame_id = frame_tree["frame"]["id"]

            result = await session.storage.get_storage_key_for_frame(frame_id)
            assert "storageKey" in result
            assert isinstance(result["storageKey"], str)

    async def test_cookie_persistence_across_get(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)

            cookies_to_set = [
                {"name": "c1", "value": "v1", "domain": ".example.com"},
                {"name": "c2", "value": "v2", "domain": ".example.com"},
                {"name": "c3", "value": "v3", "domain": ".example.com"},
            ]
            await session.storage.set_cookies(cookies_to_set)

            result = await session.storage.get_cookies()
            names = {c["name"] for c in result["cookies"]}
            assert {"c1", "c2", "c3"}.issubset(names)

            await session.storage.clear_cookies()
            result = await session.storage.get_cookies()
            names_after = {c["name"] for c in result["cookies"]}
            assert not names_after.intersection({"c1", "c2", "c3"})
