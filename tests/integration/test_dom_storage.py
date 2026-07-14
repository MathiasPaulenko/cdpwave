"""Integration tests for the DOMStorage domain."""

import asyncio
import contextlib
from collections.abc import AsyncIterator
from typing import Any

import pytest
import pytest_asyncio

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_browser
from cdpwave.exceptions import CommandError


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
    p = await client.new_page("https://example.com")
    await p.page.enable()
    await p.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await p.runtime.evaluate("document.title", return_by_value=True)
        if result.get("result", {}).get("value"):
            break
    yield p
    with contextlib.suppress(Exception):
        await p.close()


@pytest.mark.integration
class TestDOMStorageIntegration:
    async def test_enable_disable(self, page: CDPSession) -> None:
        await page.dom_storage.enable()
        await page.dom_storage.disable()

    async def test_get_dom_storage_items_empty(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        assert "entries" in result
        assert isinstance(result["entries"], list)

    async def test_set_and_get_local_storage_item(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "test-key", "test-value")
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        entries = result["entries"]
        found = [e for e in entries if e[0] == "test-key"]
        assert len(found) == 1
        assert found[0][1] == "test-value"

    async def test_set_and_get_session_storage_item(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": False}
        await page.dom_storage.set_dom_storage_item(storage_id, "session-key", "session-val")
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        entries = result["entries"]
        found = [e for e in entries if e[0] == "session-key"]
        assert len(found) == 1
        assert found[0][1] == "session-val"

    async def test_remove_dom_storage_item(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "remove-me", "val")
        await page.dom_storage.remove_dom_storage_item(storage_id, "remove-me")
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        entries = result["entries"]
        found = [e for e in entries if e[0] == "remove-me"]
        assert found == []

    async def test_clear_dom_storage_items(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "k1", "v1")
        await page.dom_storage.set_dom_storage_item(storage_id, "k2", "v2")
        await page.dom_storage.clear(storage_id)
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        assert result["entries"] == []

    async def test_clear_dom_storage_items_alias(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "alias-k", "alias-v")
        await page.dom_storage.clear_dom_storage_items(storage_id)
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        assert result["entries"] == []

    async def test_local_and_session_storage_isolated(self, page: CDPSession) -> None:
        local_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        session_id = {"securityOrigin": "https://example.com", "isLocalStorage": False}
        await page.dom_storage.set_dom_storage_item(local_id, "shared-key", "local-val")
        await page.dom_storage.set_dom_storage_item(session_id, "shared-key", "session-val")
        local_result = await page.dom_storage.get_dom_storage_items(local_id)
        session_result = await page.dom_storage.get_dom_storage_items(session_id)
        local_entry = [e for e in local_result["entries"] if e[0] == "shared-key"]
        session_entry = [e for e in session_result["entries"] if e[0] == "shared-key"]
        assert local_entry[0][1] == "local-val"
        assert session_entry[0][1] == "session-val"

    async def test_set_empty_value(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "empty-val", "")
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        entries = result["entries"]
        found = [e for e in entries if e[0] == "empty-val"]
        assert len(found) == 1
        assert found[0][1] == ""

    async def test_overwrite_existing_item(self, page: CDPSession) -> None:
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "overwrite", "old")
        await page.dom_storage.set_dom_storage_item(storage_id, "overwrite", "new")
        result = await page.dom_storage.get_dom_storage_items(storage_id)
        entries = result["entries"]
        found = [e for e in entries if e[0] == "overwrite"]
        assert len(found) == 1
        assert found[0][1] == "new"

    async def test_event_dom_storage_item_added(self, page: CDPSession) -> None:
        events: list[dict[str, Any]] = []

        async def on_item_added(params: dict[str, Any]) -> None:
            events.append(params)

        await page.dom_storage.enable()
        page.on("DOMStorage.domStorageItemAdded", on_item_added)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "event-add", "val")
        for _ in range(10):
            await asyncio.sleep(0.5)
            if events:
                break
        assert len(events) > 0
        assert events[0]["key"] == "event-add"
        assert events[0]["newValue"] == "val"
        await page.dom_storage.disable()

    async def test_event_dom_storage_item_removed(self, page: CDPSession) -> None:
        events: list[dict[str, Any]] = []

        async def on_item_removed(params: dict[str, Any]) -> None:
            events.append(params)

        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "event-remove", "val")
        await page.dom_storage.enable()
        page.on("DOMStorage.domStorageItemRemoved", on_item_removed)
        await page.dom_storage.remove_dom_storage_item(storage_id, "event-remove")
        for _ in range(10):
            await asyncio.sleep(0.5)
            if events:
                break
        assert len(events) > 0
        assert events[0]["key"] == "event-remove"
        await page.dom_storage.disable()

    async def test_event_dom_storage_item_updated(self, page: CDPSession) -> None:
        events: list[dict[str, Any]] = []

        async def on_item_updated(params: dict[str, Any]) -> None:
            events.append(params)

        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        try:
            await page.dom_storage.set_dom_storage_item(storage_id, "event-update", "old")
        except CommandError:
            pytest.skip("Frame not ready for DOMStorage in CI")
        await page.dom_storage.enable()
        page.on("DOMStorage.domStorageItemUpdated", on_item_updated)
        await page.dom_storage.set_dom_storage_item(storage_id, "event-update", "new")
        for _ in range(10):
            await asyncio.sleep(0.5)
            if events:
                break
        assert len(events) > 0
        assert events[0]["key"] == "event-update"
        assert events[0]["oldValue"] == "old"
        assert events[0]["newValue"] == "new"
        await page.dom_storage.disable()

    async def test_event_dom_storage_items_cleared(self, page: CDPSession) -> None:
        events: list[dict[str, Any]] = []

        async def on_items_cleared(params: dict[str, Any]) -> None:
            events.append(params)

        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await page.dom_storage.set_dom_storage_item(storage_id, "k1", "v1")
        await page.dom_storage.enable()
        page.on("DOMStorage.domStorageItemsCleared", on_items_cleared)
        await page.dom_storage.clear(storage_id)
        for _ in range(10):
            await asyncio.sleep(0.5)
            if events:
                break
        assert len(events) > 0
        await page.dom_storage.disable()
