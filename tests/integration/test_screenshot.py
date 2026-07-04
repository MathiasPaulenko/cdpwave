import asyncio
import base64

import pytest

from cdpwave import CDPSession


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
class TestScreenshot:
    async def test_png_screenshot(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        result = await page.page.capture_screenshot(format="png")
        data = base64.b64decode(result["data"])
        assert data[:8] == b"\x89PNG\r\n\x1a\n"

    async def test_jpeg_screenshot(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        result = await page.page.capture_screenshot(format="jpeg", quality=90)
        data = base64.b64decode(result["data"])
        assert data[:3] == b"\xff\xd8\xff"

    async def test_screenshot_with_clip(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        clip = {
            "x": 0,
            "y": 0,
            "width": 100,
            "height": 100,
            "scale": 1,
        }
        result = await page.page.capture_screenshot(format="png", clip=clip)
        data = base64.b64decode(result["data"])
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert len(data) > 100

    async def test_full_page_screenshot(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        result = await page.page.capture_screenshot(
            format="png",
            capture_beyond_viewport=True,
        )
        data = base64.b64decode(result["data"])
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert len(data) > 1000
