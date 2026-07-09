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
class TestPDF:
    async def test_print_to_pdf(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        result = await page.page.print_to_pdf(print_background=True)
        data = base64.b64decode(result)
        assert data[:5] == b"%PDF-"

    async def test_landscape_pdf(self, page: CDPSession) -> None:
        await _wait_for_page(page)
        result = await page.page.print_to_pdf(landscape=True, print_background=True)
        data = base64.b64decode(result)
        assert data[:5] == b"%PDF-"
