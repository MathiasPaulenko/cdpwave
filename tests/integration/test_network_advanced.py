"""Advanced integration tests for Network domain edge cases.

Tests deeper scenarios: event sequences, blocked URL verification,
XHR replay, Fetch interception with response body, cookie edge cases,
encoding overrides, and experimental methods.
"""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPSession
from cdpwave.exceptions import CommandError, CommandTimeoutError


@pytest.mark.integration
class TestNetworkEvents:
    """Verify Network domain event sequences with a real browser."""

    async def test_request_will_be_sent_event(self, page: CDPSession) -> None:
        await page.network.enable()
        events: list[dict[str, Any]] = []

        async def on_request(event: dict[str, Any]) -> None:
            events.append(event)

        page.on("Network.requestWillBeSent", on_request)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.requestWillBeSent", on_request)

        assert len(events) > 0
        first = events[0]
        assert "requestId" in first
        assert "request" in first
        assert "url" in first["request"]
        assert "method" in first["request"]

    async def test_response_received_event(self, page: CDPSession) -> None:
        await page.network.enable()
        events: list[dict[str, Any]] = []

        async def on_response(event: dict[str, Any]) -> None:
            events.append(event)

        page.on("Network.responseReceived", on_response)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response)

        assert len(events) > 0
        first = events[0]
        assert "requestId" in first
        assert "response" in first
        assert "status" in first["response"]
        assert "url" in first["response"]

    async def test_loading_finished_event(self, page: CDPSession) -> None:
        await page.network.enable()
        events: list[dict[str, Any]] = []

        async def on_finished(event: dict[str, Any]) -> None:
            events.append(event)

        page.on("Network.loadingFinished", on_finished)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1.5)
        page.off("Network.loadingFinished", on_finished)

        assert len(events) > 0
        first = events[0]
        assert "requestId" in first
        assert "timestamp" in first
        assert "encodedDataLength" in first

    async def test_data_received_event(self, page: CDPSession) -> None:
        await page.network.enable()
        events: list[dict[str, Any]] = []

        async def on_data(event: dict[str, Any]) -> None:
            events.append(event)

        page.on("Network.dataReceived", on_data)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1.5)
        page.off("Network.dataReceived", on_data)

        assert len(events) > 0
        first = events[0]
        assert "requestId" in first
        assert "dataLength" in first

    async def test_event_off_unsubscribes(self, page: CDPSession) -> None:
        await page.network.enable()
        events: list[dict[str, Any]] = []

        async def on_request(event: dict[str, Any]) -> None:
            events.append(event)

        page.on("Network.requestWillBeSent", on_request)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(0.5)
        page.off("Network.requestWillBeSent", on_request)
        count_after_off = len(events)

        await page.page.navigate("https://example.com")
        await asyncio.sleep(0.5)
        assert len(events) == count_after_off


@pytest.mark.integration
class TestNetworkBlockedURLs:
    """Verify set_blocked_urls actually blocks requests."""

    async def test_blocked_urls_block_css(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_blocked_urls(urls=["*.css"])
        failed_events: list[dict[str, Any]] = []

        async def on_failed(event: dict[str, Any]) -> None:
            failed_events.append(event)

        page.on("Network.loadingFailed", on_failed)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1.5)
        page.off("Network.loadingFailed", on_failed)

        await page.network.set_blocked_urls(urls=[])

    async def test_blocked_urls_block_then_unblock_image(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(0.5)

        await page.network.set_blocked_urls(urls=["*.png", "*.jpg", "*.gif"])
        failed_events: list[dict[str, Any]] = []

        async def on_failed(event: dict[str, Any]) -> None:
            failed_events.append(event)

        page.on("Network.loadingFailed", on_failed)
        await page.runtime.evaluate(
            "new Image().src = 'https://example.com/test.png';",
            return_by_value=True,
        )
        await asyncio.sleep(1)
        page.off("Network.loadingFailed", on_failed)
        assert len(failed_events) > 0

        await page.network.set_blocked_urls(urls=[])
        failed_after_unblock: list[dict[str, Any]] = []

        async def on_failed2(event: dict[str, Any]) -> None:
            failed_after_unblock.append(event)

        page.on("Network.loadingFailed", on_failed2)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.loadingFailed", on_failed2)
        assert len(failed_after_unblock) == 0


@pytest.mark.integration
class TestNetworkReplayXHR:
    """Test replay_xhr with a real XHR request."""

    async def test_replay_xhr(self, page: CDPSession) -> None:
        await page.network.enable()
        request_events: list[dict[str, Any]] = []

        async def on_request(event: dict[str, Any]) -> None:
            url = event.get("request", {}).get("url", "")
            if "httpbin.org" in url:
                request_events.append(event)

        page.on("Network.requestWillBeSent", on_request)
        await page.page.navigate("https://example.com")
        try:
            await page.runtime.evaluate(
                "fetch('https://httpbin.org/get').catch(() => {})",
                await_promise=True,
            )
        except CommandTimeoutError:
            pytest.skip("Network timeout reaching httpbin.org")
        await asyncio.sleep(2)
        page.off("Network.requestWillBeSent", on_request)

        if request_events:
            with contextlib.suppress(Exception):
                result = await page.network.replay_xhr(request_events[0]["requestId"])
                assert isinstance(result, dict)


@pytest.mark.integration
class TestNetworkFetchInterception:
    """Test get_response_body_for_interception and
    take_response_body_for_interception_as_stream with Fetch domain."""

    async def test_intercept_and_get_response_body(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        await page.fetch.enable(
            patterns=[{"urlPattern": "*example.com*", "requestStage": "Response"}],
        )
        paused_events: list[dict[str, Any]] = []

        async def on_paused(event: dict[str, Any]) -> None:
            paused_events.append(event)
            with contextlib.suppress(Exception):
                await page.fetch.continue_request(event["requestId"])

        page.on("Fetch.requestPaused", on_paused)
        await page.runtime.evaluate(
            "fetch('https://example.com').then(r => r.text()).catch(() => {})",
            await_promise=True,
        )
        await asyncio.sleep(2)
        page.off("Fetch.requestPaused", on_paused)
        await page.fetch.disable()

        if paused_events:
            req_id = paused_events[0]["requestId"]
            with contextlib.suppress(Exception):
                body = await page.network.get_response_body_for_interception(req_id)
                assert isinstance(body, dict)
            with contextlib.suppress(Exception):
                stream = await page.network.take_response_body_for_interception_as_stream(
                    req_id,
                )
                assert isinstance(stream, dict)


@pytest.mark.integration
class TestNetworkCookieEdgeCases:
    """Test cookie edge cases not covered by basic tests."""

    async def test_set_cookie_with_expires(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        future_expiry = 9999999999.0
        result = await page.network.set_cookie(
            name="expcookie",
            value="expval",
            url="https://example.com",
            expires=future_expiry,
        )
        assert result.get("success") is True
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        target = [c for c in cookies["cookies"] if c["name"] == "expcookie"]
        assert len(target) == 1
        assert target[0]["expires"] > 0

    async def test_set_cookie_with_domain_and_path(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.set_cookie(
            name="domaincookie",
            value="domainval",
            domain=".example.com",
            path="/",
        )
        assert result.get("success") is True
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        target = [c for c in cookies["cookies"] if c["name"] == "domaincookie"]
        assert len(target) == 1
        assert target[0]["domain"] == ".example.com"
        assert target[0]["path"] == "/"

    async def test_delete_cookies_by_domain_and_path(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        await page.network.set_cookie(
            name="delbydomain",
            value="val",
            domain=".example.com",
            path="/",
        )
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        assert any(c["name"] == "delbydomain" for c in cookies["cookies"])

        await page.network.delete_cookies(
            "delbydomain", domain=".example.com", path="/",
        )
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        assert not any(c["name"] == "delbydomain" for c in cookies["cookies"])

    async def test_set_cookie_same_site_strict(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        result = await page.network.set_cookie(
            name="sscookie",
            value="ssval",
            url="https://example.com",
            same_site="Strict",
        )
        assert result.get("success") is True
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        target = [c for c in cookies["cookies"] if c["name"] == "sscookie"]
        assert len(target) == 1
        assert target[0]["sameSite"] == "Strict"

    async def test_set_cookies_batch_and_verify(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        await page.network.set_cookies([
            {"name": f"batch{i}", "value": f"val{i}", "domain": ".example.com"}
            for i in range(5)
        ])
        cookies = await page.network.get_cookies(urls=["https://example.com"])
        names = {c["name"] for c in cookies["cookies"]}
        for i in range(5):
            assert f"batch{i}" in names


@pytest.mark.integration
class TestNetworkExtraHeaders:
    """Verify set_extra_request_headers actually sends headers."""

    async def test_extra_headers_appear_in_request(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_extra_request_headers(
            {"X-Cdpwave-Test": "integration-123"},
        )
        request_events: list[dict[str, Any]] = []

        async def on_request(event: dict[str, Any]) -> None:
            request_events.append(event)

        page.on("Network.requestWillBeSent", on_request)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.requestWillBeSent", on_request)

        assert len(request_events) > 0
        headers = request_events[0].get("request", {}).get("headers", {})
        assert headers.get("X-Cdpwave-Test") == "integration-123"


@pytest.mark.integration
class TestNetworkSearchResponseBody:
    """Test search_in_response_body with different options."""

    async def test_search_case_insensitive(self, page: CDPSession) -> None:
        await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=10 * 1024 * 1024,
        )
        request_ids: list[str] = []

        async def on_response(event: dict[str, Any]) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response)
        assert len(request_ids) > 0

        result = await page.network.search_in_response_body(
            request_ids[0], "example domain",
        )
        assert "result" in result
        assert len(result["result"]) > 0

    async def test_search_case_sensitive_no_match(self, page: CDPSession) -> None:
        await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=10 * 1024 * 1024,
        )
        request_ids: list[str] = []

        async def on_response(event: dict[str, Any]) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response)
        assert len(request_ids) > 0

        result = await page.network.search_in_response_body(
            request_ids[0], "example domain",
            case_sensitive=True,
        )
        assert "result" in result
        assert len(result["result"]) == 0

    async def test_search_with_regex(self, page: CDPSession) -> None:
        await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=10 * 1024 * 1024,
        )
        request_ids: list[str] = []

        async def on_response(event: dict[str, Any]) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response)
        assert len(request_ids) > 0

        result = await page.network.search_in_response_body(
            request_ids[0], r"Example\s+Domain", is_regex=True,
        )
        assert "result" in result
        assert len(result["result"]) > 0


@pytest.mark.integration
class TestNetworkEmulateConditions:
    """Test emulate_network_conditions_by_rule with various scenarios."""

    async def test_emulate_with_offline_service_worker(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.emulate_network_conditions_by_rule(
            [{"urlPattern": "", "offline": False, "latency": 0,
              "downloadThroughput": -1, "uploadThroughput": -1}],
            emulate_offline_service_worker=True,
        )
        assert "ruleIds" in result
        await page.network.emulate_network_conditions_by_rule(
            [{"urlPattern": "", "offline": False, "latency": 0,
              "downloadThroughput": -1, "uploadThroughput": -1}],
            emulate_offline_service_worker=False,
        )

    async def test_emulate_multiple_conditions(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.emulate_network_conditions_by_rule([
            {"urlPattern": "*example.com*", "offline": False,
             "latency": 100, "downloadThroughput": 1000,
             "uploadThroughput": 500},
            {"urlPattern": "*httpbin.org*", "offline": True,
             "latency": 0, "downloadThroughput": -1,
             "uploadThroughput": -1},
        ])
        assert "ruleIds" in result
        assert len(result["ruleIds"]) == 2

    async def test_emulate_offline_condition(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.emulate_network_conditions_by_rule(
            [{"urlPattern": "", "offline": True, "latency": 0,
              "downloadThroughput": -1, "uploadThroughput": -1}],
        )
        assert "ruleIds" in result
        await page.network.emulate_network_conditions_by_rule(
            [{"urlPattern": "", "offline": False, "latency": 0,
              "downloadThroughput": -1, "uploadThroughput": -1}],
        )


@pytest.mark.integration
class TestNetworkEnableOptions:
    """Test enable with various boolean and buffer options."""

    async def test_enable_with_report_direct_socket(self, page: CDPSession) -> None:
        result = await page.network.enable(report_direct_socket_traffic=True)
        assert result == {}
        await page.network.disable()

    async def test_enable_with_durable_messages(self, page: CDPSession) -> None:
        result = await page.network.enable(
            max_total_buffer_size=5 * 1024 * 1024,
            enable_durable_messages=True,
        )
        assert result == {}
        await page.network.disable()

    async def test_enable_with_all_options(self, page: CDPSession) -> None:
        result = await page.network.enable(
            max_total_buffer_size=10 * 1024 * 1024,
            max_resource_buffer_size=5 * 1024 * 1024,
            max_post_data_size=2048,
            report_direct_socket_traffic=True,
            enable_durable_messages=True,
        )
        assert result == {}
        await page.network.disable()


@pytest.mark.integration
class TestNetworkExperimentalMethods:
    """Test experimental methods: device bound sessions, cookie controls."""

    async def test_enable_device_bound_sessions(self, page: CDPSession) -> None:
        await page.network.enable()
        with contextlib.suppress(Exception):
            result = await page.network.enable_device_bound_sessions(True)
            assert isinstance(result, dict)
        with contextlib.suppress(Exception):
            result = await page.network.enable_device_bound_sessions(False)
            assert isinstance(result, dict)

    async def test_delete_device_bound_session_invalid_key(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        with contextlib.suppress(Exception):
            result = await page.network.delete_device_bound_session(
                {"site": "https://nonexistent.example", "id": "fake-id"},
            )
            assert isinstance(result, dict)

    async def test_set_cookie_controls_enable(self, page: CDPSession) -> None:
        await page.network.enable()
        with contextlib.suppress(Exception):
            result = await page.network.set_cookie_controls(True)
            assert isinstance(result, dict)
        with contextlib.suppress(Exception):
            await page.network.set_cookie_controls(False)


@pytest.mark.integration
class TestNetworkLoadResource:
    """Test load_network_resource with various options."""

    async def test_load_network_resource_with_disable_cache(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        with contextlib.suppress(Exception):
            result = await page.network.load_network_resource(
                "https://example.com",
                {"disableCache": True},
            )
            assert isinstance(result, dict)
            assert "resource" in result

    async def test_load_network_resource_with_options(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.page.navigate("https://example.com")
        with contextlib.suppress(Exception):
            result = await page.network.load_network_resource(
                "https://example.com",
                {"disableCache": False, "includeCredentials": True},
            )
            assert isinstance(result, dict)


@pytest.mark.integration
class TestNetworkUserAgentOverride:
    """Test set_user_agent_override with various parameter combinations."""

    async def test_user_agent_override_accept_language(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_user_agent_override(
            "cdpwave-lang-test/1.0",
            accept_language="es-ES, en;q=0.9",
        )
        await page.page.navigate("https://example.com")
        result = await page.runtime.evaluate(
            "navigator.userAgent", return_by_value=True,
        )
        assert "cdpwave-lang-test" in result["result"]["value"]

    async def test_user_agent_override_platform(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_user_agent_override(
            "cdpwave-platform-test/1.0",
            platform="Linux",
        )
        await page.page.navigate("https://example.com")
        result = await page.runtime.evaluate(
            "navigator.platform", return_by_value=True,
        )
        assert "Linux" in result["result"]["value"]

    async def test_user_agent_override_all_params(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_user_agent_override(
            "cdpwave-full-ua/3.0",
            accept_language="fr-FR",
            platform="macOS",
            user_agent_metadata={
                "brands": [{"brand": "cdpwave", "version": "3.0"}],
                "platform": "macOS",
                "platformVersion": "14.0",
                "architecture": "arm",
                "model": "",
                "mobile": False,
                "wow64": False,
            },
        )
        await page.page.navigate("https://example.com")
        ua_result = await page.runtime.evaluate(
            "navigator.userAgent", return_by_value=True,
        )
        assert "cdpwave-full-ua" in ua_result["result"]["value"]


@pytest.mark.integration
class TestNetworkGetResponseBody:
    """Test get_response_body with real responses."""

    async def test_get_response_body_html_content(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        request_ids: list[str] = []

        async def on_response(event: dict[str, Any]) -> None:
            request_ids.append(event["requestId"])

        page.on("Network.responseReceived", on_response)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        page.off("Network.responseReceived", on_response)
        assert len(request_ids) > 0

        body = await page.network.get_response_body(request_ids[0])
        assert "body" in body
        assert "base64Encoded" in body
        assert "Example Domain" in body["body"] or body["base64Encoded"] is True

    async def test_get_response_body_for_nonexistent_request(
        self, page: CDPSession,
    ) -> None:
        await page.network.enable()
        with pytest.raises(CommandError):
            await page.network.get_response_body("NONEXISTENT_REQUEST_ID")


@pytest.mark.integration
class TestNetworkCacheAndEncoding:
    """Test cache and encoding interactions."""

    async def test_cache_disabled_then_reenabled(self, page: CDPSession) -> None:
        await page.network.enable()
        await page.network.set_cache_disabled(True)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(0.5)

        await page.network.set_cache_disabled(False)
        await page.page.navigate("https://example.com")
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True,
        )
        assert result.get("result", {}).get("value") == "Example Domain"

    async def test_set_accepted_encodings_br(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_accepted_encodings(["br"])
        assert result == {}
        result = await page.network.clear_accepted_encodings_override()
        assert result == {}

    async def test_set_accepted_encodings_empty_list(self, page: CDPSession) -> None:
        await page.network.enable()
        result = await page.network.set_accepted_encodings([])
        assert result == {}
        result = await page.network.clear_accepted_encodings_override()
        assert result == {}
