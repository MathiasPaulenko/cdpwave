"""Comprehensive integration tests for Network domain methods.

Tests every Network domain method against a real Chrome browser to
verify parameters are accepted and responses are well-formed.
"""

import asyncio

import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestNetworkComprehensive:
    async def test_disable(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.disable()
        assert result == {}

    async def test_set_extra_request_headers(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_extra_request_headers(
            {"X-Test-Header": "test-value"},
        )
        assert result == {}

    async def test_set_cookies_plural(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.set_cookies([
            {"name": "multi1", "value": "val1", "domain": ".example.com"},
            {"name": "multi2", "value": "val2", "domain": ".example.com"},
        ])
        assert result == {}
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        names = [c["name"] for c in cookies["cookies"]]
        assert "multi1" in names
        assert "multi2" in names

    async def test_get_response_body(self, page: CDPSession) -> None:
        await page.network.enable()
        request_ids: list[str] = []

        async def on_response_received(event: dict) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response_received)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response_received)
        assert len(request_ids) > 0
        body = await page.network.get_response_body(request_ids[0])
        assert "body" in body
        assert "base64Encoded" in body

    async def test_emulate_network_conditions_by_rule(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.emulate_network_conditions_by_rule(
            [{"urlPattern": "", "offline": False, "latency": 0,
              "downloadThroughput": -1, "uploadThroughput": -1}],
        )
        assert "ruleIds" in result
        assert len(result["ruleIds"]) == 1

    async def test_clear_accepted_encodings_override(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_accepted_encodings(["gzip", "deflate"])
        result = await page.network.clear_accepted_encodings_override()
        assert result == {}

    async def test_get_certificate(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.get_certificate("https://example.com")
        assert "tableNames" in result

    async def test_get_security_isolation_status(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.get_security_isolation_status()
        assert "status" in result

    async def test_enable_reporting_api(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.enable_reporting_api(True)
        assert result == {}
        result = await page.network.enable_reporting_api(False)
        assert result == {}

    async def test_search_in_response_body(self, page: CDPSession) -> None:
        await page.network.enable(max_total_buffer_size=10 * 1024 * 1024,
                                  max_resource_buffer_size=10 * 1024 * 1024)
        request_ids: list[str] = []

        async def on_response_received(event: dict) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response_received)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response_received)
        assert len(request_ids) > 0
        result = await page.network.search_in_response_body(
            request_ids[0], "Example Domain",
        )
        assert "result" in result
        assert len(result["result"]) > 0

    async def test_fetch_schemeful_site(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.fetch_schemeful_site("https://example.com")
        assert "schemefulSite" in result

    async def test_set_cookie_controls(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_cookie_controls(False)
        assert result == {}

    async def test_configure_durable_messages(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.configure_durable_messages(
            max_total_buffer_size=5 * 1024 * 1024,
            max_resource_buffer_size=1 * 1024 * 1024,
        )
        assert result == {}

    async def test_configure_durable_messages_disable(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.configure_durable_messages()
        assert result == {}

    async def test_enable_with_buffer_sizes(self, page: CDPSession) -> None:
        result = await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=5 * 1024 * 1024,
            max_post_data_size=1024,
        )
        assert result == {}

    async def test_enable_disable_cycle(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.disable()
        result = await page.network.enable()
        assert result == {}
        await page.network.disable()

    async def test_set_cookie_with_all_params(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.set_cookie(
            name="fullcookie",
            value="fullvalue",
            url="https://example.com",
            path="/",
            secure=True,
            http_only=True,
            same_site="Lax",
            priority="High",
            source_scheme="Secure",
            source_port=443,
        )
        assert result == {"success": True}
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        target = [c for c in cookies["cookies"] if c["name"] == "fullcookie"]
        assert len(target) == 1
        assert target[0]["httpOnly"] is True
        assert target[0]["secure"] is True
        assert target[0]["sameSite"] == "Lax"
        assert target[0]["priority"] == "High"

    async def test_delete_cookies_by_domain(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        await page.network.set_cookie(
            name="delcookie", value="val", url="https://example.com",
        )
        result = await page.network.delete_cookies("delcookie", url="https://example.com")
        assert result == {}
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        names = [c["name"] for c in cookies["cookies"]]
        assert "delcookie" not in names

    async def test_override_network_state_online(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.override_network_state(
            offline=False, latency=0,
            download_throughput=-1, upload_throughput=-1,
        )
        assert result == {}

    async def test_override_network_state_with_connection_type(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        result = await page.network.override_network_state(
            offline=False, latency=100,
            download_throughput=500000, upload_throughput=500000,
            connection_type="wifi",
        )
        assert result == {}

    async def test_stream_resource_content(self, page: CDPSession) -> None:
        await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=10 * 1024 * 1024,
        )
        request_ids: list[str] = []

        async def on_response_received(event: dict) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response_received)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response_received)
        assert len(request_ids) > 0
        try:
            result = await page.network.stream_resource_content(request_ids[0])
            assert "bufferedData" in result
        except Exception as e:
            assert "already finished loading" in str(e)
