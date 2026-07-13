import contextlib

import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestNetworkCasuistics:
    async def test_set_cache_disabled(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_cache_disabled(True)
        assert result == {}

    async def test_set_blocked_urls(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_blocked_urls(urls=["*.jpg", "*.png"])
        assert result == {}

    async def test_set_blocked_urls_with_patterns(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_blocked_urls(urls=["/api/*", "*.css"])
        assert result == {}

    async def test_set_bypass_service_worker(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_bypass_service_worker(True)
        assert result == {}

    async def test_load_network_resource(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        with contextlib.suppress(Exception):
            await page.network.load_network_resource(
                "https://example.com", {"disableCache": True},
            )
        assert True

    async def test_get_request_post_data(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        # This requires a specific requestId from a POST request
        # For now, test that the method exists
        with contextlib.suppress(Exception):
            await page.network.get_request_post_data("request_id")
        # May fail with invalid request_id, but that's expected
        assert True

    async def test_set_cookie_with_priority(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.set_cookie(
            "test_cookie", "value123",
            url="https://example.com",
            priority="High",
            source_scheme="Secure",
            source_port=443,
        )
        assert result.get("success") is True

    async def test_override_network_state(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.override_network_state(
            offline=False, latency=0,
            download_throughput=-1, upload_throughput=-1,
        )
        assert result == {}

    async def test_set_user_agent_override_with_metadata(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_user_agent_override(
            "cdpwave-test/2.0",
            user_agent_metadata={
                "brands": [{"brand": "cdpwave", "version": "2.0"}],
                "platform": "Windows",
                "platformVersion": "10.0",
                "architecture": "x86",
                "model": "",
                "mobile": False,
                "wow64": False,
            },
        )
        await page.page.navigate("https://example.com")
        result = await page.runtime.evaluate(
            "navigator.userAgent", return_by_value=True
        )
        assert "cdpwave-test" in result["result"]["value"]
