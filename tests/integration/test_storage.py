"""Integration tests for the Storage domain."""

import contextlib
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio

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


@pytest_asyncio.fixture
async def client() -> AsyncIterator[CDPClient]:
    c = await CDPClient.launch(headless=True)
    yield c
    with contextlib.suppress(Exception):
        await c.close()


@pytest_asyncio.fixture
async def page(client: CDPClient) -> AsyncIterator[CDPSession]:
    p = await client.new_page("about:blank")
    yield p
    with contextlib.suppress(Exception):
        await p.close()


@pytest.mark.integration
class TestStorageIntegration:
    async def test_get_cookies(self, page: CDPSession) -> None:
        result = await page.storage.get_cookies()
        assert "cookies" in result
        assert isinstance(result["cookies"], list)

    async def test_set_and_clear_cookies(self, page: CDPSession) -> None:
        await page.storage.set_cookies([
            {"name": "test", "value": "1", "domain": "example.com"},
        ])
        await page.storage.clear_cookies()
        result = await page.storage.get_cookies()
        assert result["cookies"] == []

    async def test_get_usage_and_quota(self, page: CDPSession) -> None:
        result = await page.storage.get_usage_and_quota("https://example.com")
        assert "usage" in result
        assert "quota" in result
        assert "overrideActive" in result
        assert isinstance(result["usage"], (int, float))
        assert isinstance(result["quota"], (int, float))

    async def test_clear_data_for_origin(self, page: CDPSession) -> None:
        await page.storage.clear_data_for_origin("https://example.com", "all")

    async def test_get_trust_tokens(self, page: CDPSession) -> None:
        result = await page.storage.get_trust_tokens()
        assert "tokens" in result
        assert isinstance(result["tokens"], list)

    async def test_clear_trust_tokens(self, page: CDPSession) -> None:
        result = await page.storage.clear_trust_tokens("https://issuer.example.com")
        assert "didDeleteTokens" in result
        assert isinstance(result["didDeleteTokens"], bool)

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_get_storage_key(self, page: CDPSession) -> None:
        result = await page.storage.get_storage_key()
        assert "storageKey" in result
        assert isinstance(result["storageKey"], str)

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_get_storage_key_with_frame(self, page: CDPSession) -> None:
        frame_tree = await page.page.get_frame_tree()
        frame_id = frame_tree["frameTree"]["frame"]["id"]
        result = await page.storage.get_storage_key(frame_id)
        assert "storageKey" in result
        assert isinstance(result["storageKey"], str)

    async def test_override_quota_for_origin(self, page: CDPSession) -> None:
        await page.storage.override_quota_for_origin(
            "https://example.com", quota_size=1048576.0,
        )
        await page.storage.override_quota_for_origin("https://example.com")

    async def test_track_indexed_db_for_origin(self, page: CDPSession) -> None:
        await page.storage.track_indexed_db_for_origin("https://example.com")
        await page.storage.untrack_indexed_db_for_origin("https://example.com")

    async def test_track_cache_storage_for_origin(self, page: CDPSession) -> None:
        await page.storage.track_cache_storage_for_origin("https://example.com")
        await page.storage.untrack_cache_storage_for_origin("https://example.com")

    async def test_get_interest_group_details(self, page: CDPSession) -> None:
        result = await page.storage.get_interest_group_details(
            "https://owner.example.com", "test-group",
        )
        assert "details" in result

    async def test_set_interest_group_tracking(self, page: CDPSession) -> None:
        await page.storage.set_interest_group_tracking(True)
        await page.storage.set_interest_group_tracking(False)

    async def test_set_interest_group_auction_tracking(self, page: CDPSession) -> None:
        await page.storage.set_interest_group_auction_tracking(True)
        await page.storage.set_interest_group_auction_tracking(False)

    async def test_set_shared_storage_tracking(self, page: CDPSession) -> None:
        await page.storage.set_shared_storage_tracking(True)
        await page.storage.set_shared_storage_tracking(False)

    @pytest.mark.skip(reason="Shared storage not available for this origin in CI")
    async def test_get_shared_storage_metadata(self, page: CDPSession) -> None:
        result = await page.storage.get_shared_storage_metadata(
            "https://example.com",
        )
        assert "metadata" in result

    async def test_get_shared_storage_entries(self, page: CDPSession) -> None:
        result = await page.storage.get_shared_storage_entries(
            "https://example.com",
        )
        assert "entries" in result

    async def test_set_shared_storage_entry(self, page: CDPSession) -> None:
        await page.storage.set_shared_storage_entry(
            "https://example.com", "key1", "value1",
            ignore_if_present=True,
        )
        await page.storage.delete_shared_storage_entry(
            "https://example.com", "key1",
        )

    async def test_set_shared_storage_entry_default(self, page: CDPSession) -> None:
        await page.storage.set_shared_storage_entry(
            "https://example.com", "key2", "value2",
        )
        await page.storage.delete_shared_storage_entry(
            "https://example.com", "key2",
        )

    async def test_clear_shared_storage_entries(self, page: CDPSession) -> None:
        await page.storage.clear_shared_storage_entries("https://example.com")

    async def test_reset_shared_storage_budget(self, page: CDPSession) -> None:
        await page.storage.reset_shared_storage_budget("https://example.com")

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_set_storage_bucket_tracking(self, page: CDPSession) -> None:
        sk = (await page.storage.get_storage_key())["storageKey"]
        await page.storage.set_storage_bucket_tracking(sk, True)
        await page.storage.set_storage_bucket_tracking(sk, False)

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_delete_storage_bucket(self, page: CDPSession) -> None:
        sk = (await page.storage.get_storage_key())["storageKey"]
        with contextlib.suppress(Exception):
            await page.storage.delete_storage_bucket(sk, "test-bucket")

    async def test_run_bounce_tracking_mitigations(self, page: CDPSession) -> None:
        result = await page.storage.run_bounce_tracking_mitigations()
        assert "deletedSites" in result
        assert isinstance(result["deletedSites"], list)

    @pytest.mark.skip(reason="RelatedWebsiteSets fetch fails in CI environment")
    async def test_get_related_website_sets(self, page: CDPSession) -> None:
        result = await page.storage.get_related_website_sets()
        assert "sets" in result
        assert isinstance(result["sets"], list)

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_clear_data_for_storage_key(self, page: CDPSession) -> None:
        sk = (await page.storage.get_storage_key())["storageKey"]
        await page.storage.clear_data_for_storage_key(sk, "all")

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_track_indexed_db_for_storage_key(self, page: CDPSession) -> None:
        sk = (await page.storage.get_storage_key())["storageKey"]
        await page.storage.track_indexed_db_for_storage_key(sk)
        await page.storage.untrack_indexed_db_for_storage_key(sk)

    @pytest.mark.skip(reason="Storage.getStorageKey not supported in CI Chrome")
    async def test_track_cache_storage_for_storage_key(self, page: CDPSession) -> None:
        sk = (await page.storage.get_storage_key())["storageKey"]
        await page.storage.track_cache_storage_for_storage_key(sk)
        await page.storage.untrack_cache_storage_for_storage_key(sk)

    @pytest.mark.skip(reason="Protected audience K-anonymity not supported in CI Chrome")
    async def test_set_protected_audience_k_anonymity(self, page: CDPSession) -> None:
        await page.storage.set_protected_audience_k_anonymity(
            "https://owner.com", "group1", ["hash1", "hash2"],
        )
