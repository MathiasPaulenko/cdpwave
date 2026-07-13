"""E2E tests for the DOMStorage domain.

These tests exercise the full CDP pipeline: launch a real browser,
navigate to a page, set/get/remove/clear localStorage and sessionStorage
via DOMStorage commands, and verify side effects through Runtime.evaluate.
"""

import asyncio
from typing import Any

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


def _get_security_origin(page: CDPSession) -> str:
    """Extract securityOrigin from the page's execution context."""
    # We use a known origin for example.com
    return "https://example.com"


@pytest.mark.integration
class TestDOMStorageE2E:
    async def test_enable_disable_storage_tracking(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            await session.dom_storage.enable()
            await session.dom_storage.disable()

    async def test_local_storage_set_get_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-local", "hello-local"
            )

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "e2e-local"]
            assert len(found) == 1
            assert found[0][1] == "hello-local"

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('e2e-local')", return_by_value=True
            )
            assert js_result["result"]["value"] == "hello-local"

    async def test_session_storage_set_get_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": False}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-session", "hello-session"
            )

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "e2e-session"]
            assert len(found) == 1
            assert found[0][1] == "hello-session"

            js_result = await session.runtime.evaluate(
                "sessionStorage.getItem('e2e-session')", return_by_value=True
            )
            assert js_result["result"]["value"] == "hello-session"

    async def test_local_storage_remove_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "remove-me", "will-be-removed"
            )

            await session.dom_storage.remove_dom_storage_item(storage_id, "remove-me")

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "remove-me"]
            assert found == []

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('remove-me')", return_by_value=True
            )
            assert js_result["result"]["value"] is None

    async def test_session_storage_remove_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": False}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "session-remove", "will-be-removed"
            )

            await session.dom_storage.remove_dom_storage_item(
                storage_id, "session-remove"
            )

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "session-remove"]
            assert found == []

            js_result = await session.runtime.evaluate(
                "sessionStorage.getItem('session-remove')", return_by_value=True
            )
            assert js_result["result"]["value"] is None

    async def test_local_storage_clear_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(storage_id, "k1", "v1")
            await session.dom_storage.set_dom_storage_item(storage_id, "k2", "v2")
            await session.dom_storage.set_dom_storage_item(storage_id, "k3", "v3")

            await session.dom_storage.clear(storage_id)

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

            js_result = await session.runtime.evaluate(
                "localStorage.length", return_by_value=True
            )
            assert js_result["result"]["value"] == 0

    async def test_session_storage_clear_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": False}

            await session.dom_storage.set_dom_storage_item(storage_id, "s1", "v1")
            await session.dom_storage.set_dom_storage_item(storage_id, "s2", "v2")

            await session.dom_storage.clear(storage_id)

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

            js_result = await session.runtime.evaluate(
                "sessionStorage.length", return_by_value=True
            )
            assert js_result["result"]["value"] == 0

    async def test_local_and_session_storage_isolated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            local_id = {"securityOrigin": origin, "isLocalStorage": True}
            session_id = {"securityOrigin": origin, "isLocalStorage": False}

            await session.dom_storage.set_dom_storage_item(
                local_id, "shared", "from-local"
            )
            await session.dom_storage.set_dom_storage_item(
                session_id, "shared", "from-session"
            )

            local_result = await session.dom_storage.get_dom_storage_items(local_id)
            session_result = await session.dom_storage.get_dom_storage_items(session_id)

            local_entry = [e for e in local_result["entries"] if e[0] == "shared"]
            session_entry = [e for e in session_result["entries"] if e[0] == "shared"]
            assert local_entry[0][1] == "from-local"
            assert session_entry[0][1] == "from-session"

    async def test_overwrite_existing_item_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(storage_id, "ow", "old")
            await session.dom_storage.set_dom_storage_item(storage_id, "ow", "new")

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "ow"]
            assert len(found) == 1
            assert found[0][1] == "new"

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('ow')", return_by_value=True
            )
            assert js_result["result"]["value"] == "new"

    async def test_set_empty_value_verify_via_runtime(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(storage_id, "empty-v", "")

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = result["entries"]
            found = [e for e in entries if e[0] == "empty-v"]
            assert len(found) == 1
            assert found[0][1] == ""

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('empty-v')", return_by_value=True
            )
            assert js_result["result"]["value"] == ""

    async def test_clear_dom_storage_items_alias(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(storage_id, "alias-k", "v")
            await session.dom_storage.clear_dom_storage_items(storage_id)

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

    async def test_multiple_items_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            items = {"k1": "v1", "k2": "v2", "k3": "v3"}
            for key, value in items.items():
                await session.dom_storage.set_dom_storage_item(storage_id, key, value)

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = {e[0]: e[1] for e in result["entries"]}
            for key, value in items.items():
                assert entries.get(key) == value

            await session.dom_storage.clear(storage_id)
            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

    async def test_remove_nonexistent_item_no_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.remove_dom_storage_item(
                storage_id, "nonexistent"
            )

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

    async def test_clear_already_empty_storage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.clear(storage_id)

            result = await session.dom_storage.get_dom_storage_items(storage_id)
            assert result["entries"] == []

    async def test_event_item_added_via_dom_storage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            events: list[dict[str, Any]] = []

            async def on_item_added(params: dict[str, Any]) -> None:
                events.append(params)

            await session.dom_storage.enable()
            session.on("DOMStorage.domStorageItemAdded", on_item_added)

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-event-add", "added-value"
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if events:
                    break

            assert len(events) > 0
            assert events[0]["key"] == "e2e-event-add"
            assert events[0]["newValue"] == "added-value"

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('e2e-event-add')", return_by_value=True
            )
            assert js_result["result"]["value"] == "added-value"

            await session.dom_storage.disable()

    async def test_event_item_removed_via_dom_storage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-event-remove", "will-be-removed"
            )

            events: list[dict[str, Any]] = []

            async def on_item_removed(params: dict[str, Any]) -> None:
                events.append(params)

            await session.dom_storage.enable()
            session.on("DOMStorage.domStorageItemRemoved", on_item_removed)

            await session.dom_storage.remove_dom_storage_item(
                storage_id, "e2e-event-remove"
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if events:
                    break

            assert len(events) > 0
            assert events[0]["key"] == "e2e-event-remove"

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('e2e-event-remove')", return_by_value=True
            )
            assert js_result["result"]["value"] is None

            await session.dom_storage.disable()

    async def test_event_item_updated_via_dom_storage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-event-update", "old-val"
            )

            events: list[dict[str, Any]] = []

            async def on_item_updated(params: dict[str, Any]) -> None:
                events.append(params)

            await session.dom_storage.enable()
            session.on("DOMStorage.domStorageItemUpdated", on_item_updated)

            await session.dom_storage.set_dom_storage_item(
                storage_id, "e2e-event-update", "new-val"
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if events:
                    break

            assert len(events) > 0
            assert events[0]["key"] == "e2e-event-update"
            assert events[0]["oldValue"] == "old-val"
            assert events[0]["newValue"] == "new-val"

            js_result = await session.runtime.evaluate(
                "localStorage.getItem('e2e-event-update')", return_by_value=True
            )
            assert js_result["result"]["value"] == "new-val"

            await session.dom_storage.disable()

    async def test_event_items_cleared_via_dom_storage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("https://example.com") as session,
        ):
            await _wait_for_page(session)
            origin = _get_security_origin(session)
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(storage_id, "c1", "v1")
            await session.dom_storage.set_dom_storage_item(storage_id, "c2", "v2")

            events: list[dict[str, Any]] = []

            async def on_items_cleared(params: dict[str, Any]) -> None:
                events.append(params)

            await session.dom_storage.enable()
            session.on("DOMStorage.domStorageItemsCleared", on_items_cleared)

            await session.dom_storage.clear(storage_id)

            for _ in range(10):
                await asyncio.sleep(0.5)
                if events:
                    break

            assert len(events) > 0

            js_result = await session.runtime.evaluate(
                "localStorage.length", return_by_value=True
            )
            assert js_result["result"]["value"] == 0

            await session.dom_storage.disable()
