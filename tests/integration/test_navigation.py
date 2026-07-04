import asyncio

import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestNavigation:
    async def test_navigate_and_evaluate_title(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")

        for _ in range(20):
            await asyncio.sleep(0.5)
            result = await page.runtime.evaluate(
                "document.title", return_by_value=True
            )
            title = result.get("result", {}).get("value", "")
            if title:
                break

        assert title == "Example Domain"

    async def test_navigate_to_about_blank(self, page: CDPSession) -> None:
        result = await page.page.navigate("about:blank")
        assert "frameId" in result

    async def test_reload_after_navigate(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")

        for _ in range(20):
            await asyncio.sleep(0.5)
            result = await page.runtime.evaluate(
                "document.title", return_by_value=True
            )
            if result.get("result", {}).get("value"):
                break

        reload_result = await page.page.reload()
        assert reload_result == {}

    async def test_page_enable_disable(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.disable()
