import asyncio

import pytest

from cdpwave import CDPClient, CDPSession


@pytest.mark.integration
class TestMultiPage:
    async def test_three_pages_different_urls(self, client: CDPClient) -> None:
        pages: list[CDPSession] = []
        urls = [
            "https://example.com",
            "about:blank",
            "https://example.com",
        ]

        for url in urls:
            p = await client.new_page(url)
            pages.append(p)

        for i, page in enumerate(pages):
            await page.page.enable()
            if urls[i] != "about:blank":
                await page.page.navigate(urls[i])

        for _ in range(20):
            await asyncio.sleep(0.5)
            all_ready = True
            for page in pages:
                result = await page.runtime.evaluate(
                    "document.readyState", return_by_value=True
                )
                if result.get("result", {}).get("value") != "complete":
                    all_ready = False
            if all_ready:
                break

        result = await pages[0].runtime.evaluate(
            "document.title", return_by_value=True
        )
        assert result["result"]["value"] == "Example Domain"

        for page in pages:
            await page.close()

    async def test_close_one_page_other_still_works(self, client: CDPClient) -> None:
        page1 = await client.new_page("https://example.com")
        page2 = await client.new_page("https://example.com")

        await page1.page.enable()
        await page2.page.enable()
        await page1.page.navigate("https://example.com")
        await page2.page.navigate("https://example.com")

        await page1.close()
        assert page1.is_closed

        result = await page2.runtime.evaluate(
            "document.title", return_by_value=True
        )
        assert result["result"]["value"] == "Example Domain"

        await page2.close()

    async def test_get_pages_returns_list(self, client: CDPClient) -> None:
        await client.new_page("about:blank")
        pages = await client.get_pages()
        assert isinstance(pages, list)
        assert len(pages) > 0
