import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestEvents:
    async def test_page_load_event_fired(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            load_events: list[dict[str, Any]] = []

            async def on_load(params: dict[str, Any]) -> None:
                load_events.append(params)

            await session.page.enable()
            session.on("Page.loadEventFired", on_load)
            await session.page.navigate("https://example.com")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if load_events:
                    break

            assert len(load_events) > 0

    async def test_runtime_console_api_called(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_events: list[dict[str, Any]] = []

            async def on_console(params: dict[str, Any]) -> None:
                console_events.append(params)

            await session.runtime.enable()
            session.on("Runtime.consoleAPICalled", on_console)
            await session.page.navigate("https://example.com")

            await asyncio.sleep(1.0)
            await session.runtime.evaluate(
                "console.log('hello from test')",
                return_by_value=True,
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_events:
                    break

            assert len(console_events) > 0
            assert console_events[0]["type"] == "log"
            assert console_events[0]["args"][0]["value"] == "hello from test"

    async def test_multiple_handlers_same_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            calls: list[str] = []

            async def h1(params: dict[str, Any]) -> None:
                calls.append("h1")

            async def h2(params: dict[str, Any]) -> None:
                calls.append("h2")

            await session.page.enable()
            session.on("Page.loadEventFired", h1)
            session.on("Page.loadEventFired", h2)
            await session.page.navigate("https://example.com")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if len(calls) >= 2:
                    break

            assert "h1" in calls
            assert "h2" in calls

    async def test_handler_error_isolation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            good_calls: list[dict[str, Any]] = []

            async def bad_handler(params: dict[str, Any]) -> None:
                raise ValueError("intentional error")

            async def good_handler(params: dict[str, Any]) -> None:
                good_calls.append(params)

            await session.page.enable()
            session.on("Page.loadEventFired", bad_handler)
            session.on("Page.loadEventFired", good_handler)
            await session.page.navigate("https://example.com")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if good_calls:
                    break

            assert len(good_calls) > 0

    async def test_runtime_exception_thrown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            exception_events: list[dict[str, Any]] = []

            async def on_exception(params: dict[str, Any]) -> None:
                exception_events.append(params)

            await session.runtime.enable()
            session.on("Runtime.exceptionThrown", on_exception)
            await session.runtime.evaluate(
                "setTimeout(() => { throw new Error('test error'); }, 0)"
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if exception_events:
                    break

            assert len(exception_events) > 0
            assert "exceptionDetails" in exception_events[0]

    async def test_unsubscribe_during_dispatch(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            calls: list[str] = []

            async def h1(params: dict[str, Any]) -> None:
                calls.append("h1")

            async def h2(params: dict[str, Any]) -> None:
                calls.append("h2")

            await session.page.enable()
            sub1 = session.on("Page.loadEventFired", h1)
            session.on("Page.loadEventFired", h2)
            sub1.unsubscribe()

            await session.page.navigate("https://example.com")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if calls:
                    break

            assert "h1" not in calls
            assert "h2" in calls
