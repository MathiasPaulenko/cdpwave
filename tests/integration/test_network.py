import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestNetwork:
    async def test_network_enable_get_cookies(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                result = await session.network.get_cookies(
                    urls=["https://example.com"]
                )
                if result.get("cookies"):
                    break

            assert "cookies" in result

    async def test_network_request_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            request_events: list[dict[str, Any]] = []

            async def on_request(params: dict[str, Any]) -> None:
                request_events.append(params)

            await session.network.enable()
            session.on("Network.requestWillBeSent", on_request)
            await session.page.navigate("https://example.com")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if request_events:
                    break

            assert len(request_events) > 0
            assert "requestId" in request_events[0]
            assert "request" in request_events[0]

    async def test_set_user_agent_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.network.set_user_agent_override(
                "cdpwave-test-agent/1.0",
                accept_language="en-US",
                platform="TestOS",
            )
            await session.page.navigate("https://example.com")

            result = await session.runtime.evaluate(
                "navigator.userAgent", return_by_value=True
            )
            assert "cdpwave-test-agent" in result["result"]["value"]

    async def test_clear_browser_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.page.navigate("https://example.com")

            await session.network.clear_browser_cache()

            await session.page.navigate("https://example.com")
            result = await session.runtime.evaluate(
                "document.title", return_by_value=True
            )
            assert result.get("result", {}).get("value") == "Example Domain"
