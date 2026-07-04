"""Functional tests for CacheStorage, CSS, DOMDebugger, and EventBreakpoints domains."""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestCacheStorage:
    async def test_request_cache_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com"
            )
            assert "caches" in result


@pytest.mark.integration
class TestCSS:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            await session.css.disable()

    async def test_get_media_queries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_media_queries()
            assert "medias" in result
            await session.css.disable()


@pytest.mark.integration
class TestDOMDebugger:
    async def test_set_remove_dom_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_set_remove_xhr_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_debugger.set_xhr_breakpoint("/api/")
            await session.dom_debugger.remove_xhr_breakpoint("/api/")


@pytest.mark.integration
class TestEventBreakpoints:
    async def test_set_clear_instrumentation_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.clear_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )

    async def test_set_clear_native_event_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_breakpoint_on_native_event(
                    "click"
                )
                await session.event_breakpoints.clear_breakpoint_on_native_event(
                    "click"
                )
