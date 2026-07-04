import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestCookies:
    async def test_set_and_get_cookie(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")

        await page.network.set_cookie(
            name="test_cookie",
            value="abc123",
            url="https://example.com",
            secure=True,
            http_only=True,
        )

        result = await page.network.get_cookies(urls=["https://example.com"])
        cookie_names = [c["name"] for c in result.get("cookies", [])]
        assert "test_cookie" in cookie_names

    async def test_delete_cookie(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")

        await page.network.set_cookie(
            name="delete_me",
            value="value",
            url="https://example.com",
        )

        result = await page.network.get_cookies(urls=["https://example.com"])
        names = [c["name"] for c in result.get("cookies", [])]
        assert "delete_me" in names

        await page.network.delete_cookies("delete_me", url="https://example.com")

        result = await page.network.get_cookies(urls=["https://example.com"])
        names = [c["name"] for c in result.get("cookies", [])]
        assert "delete_me" not in names

    async def test_clear_all_cookies(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")

        await page.network.set_cookie(
            name="cookie1",
            value="val1",
            url="https://example.com",
        )
        await page.network.set_cookie(
            name="cookie2",
            value="val2",
            url="https://example.com",
        )

        await page.network.clear_browser_cookies()

        result = await page.network.get_cookies(urls=["https://example.com"])
        names = [c["name"] for c in result.get("cookies", [])]
        assert "cookie1" not in names
        assert "cookie2" not in names
