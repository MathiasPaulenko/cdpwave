import asyncio
import base64

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestHelloWorld:
    async def test_navigate_evaluate_screenshot(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            title = ""
            for _ in range(20):
                await asyncio.sleep(0.5)
                result = await session.runtime.evaluate(
                    "document.title", return_by_value=True
                )
                title = result.get("result", {}).get("value", "")
                if title:
                    break

            assert title == "Example Domain"

            shot = await session.page.capture_screenshot(format="png")
            data = shot.get("data", "")
            assert len(data) > 0
            decoded = base64.b64decode(data)
            assert decoded[:8] == b"\x89PNG\r\n\x1a\n"
