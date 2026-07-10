"""Comprehensive coverage tests for page, network, emulation, dom, storage,
overlay, css, bluetooth_emulation, smart_card_emulation, target, and sync.

Targets methods that were previously uncovered, bringing total unit test
coverage to >=95%.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from cdpwave.domains.bluetooth_emulation import BluetoothEmulationDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.smart_card_emulation import SmartCardEmulationDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.domains.target import TargetDomain
from cdpwave.sync import SyncCDPClient, SyncCDPSession
from tests.unit.fake_sender import FakeSender

# ── Page ──────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestPageCoverage:
    async def test_stop_loading(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.stop_loading()
        assert fake.last_call == ("Page.stopLoading", None)

    async def test_set_lifecycle_events_enabled(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_lifecycle_events_enabled(True)
        assert fake.last_call == ("Page.setLifecycleEventsEnabled", {"enabled": True})

    async def test_add_script_to_evaluate_on_load(self) -> None:
        fake = FakeSender({"identifier": "s1"})
        domain = PageDomain(fake)
        await domain.add_script_to_evaluate_on_load("alert(1)")
        method, params = fake.last_call
        assert method == "Page.addScriptToEvaluateOnLoad"
        assert params is not None
        assert params["source"] == "alert(1)"

    async def test_remove_script_to_evaluate_on_load(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.remove_script_to_evaluate_on_load("s1")
        assert fake.last_call == (
            "Page.removeScriptToEvaluateOnLoad",
            {"identifier": "s1"},
        )

    async def test_start_screencast_defaults(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.start_screencast()
        method, params = fake.last_call
        assert method == "Page.startScreencast"
        assert params is not None
        assert params["format"] == "jpeg"
        assert params["quality"] == 80
        assert params["everyNthFrame"] == 1

    async def test_start_screencast_with_opts(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.start_screencast(
            format="png", quality=50, max_width=800, max_height=600, every_nth_frame=2,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["format"] == "png"
        assert params["quality"] == 50
        assert params["maxWidth"] == 800
        assert params["maxHeight"] == 600
        assert params["everyNthFrame"] == 2

    async def test_start_screencast_invalid_format(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="format must be"):
            await domain.start_screencast(format="bmp")

    async def test_start_screencast_invalid_quality(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="quality must be"):
            await domain.start_screencast(quality=200)

    async def test_stop_screencast(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.stop_screencast()
        assert fake.last_call == ("Page.stopScreencast", None)

    async def test_screencast_frame_ack(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.screencast_frame_ack(42)
        assert fake.last_call == ("Page.screencastFrameAck", {"sessionId": 42})

    async def test_search_in_resource(self) -> None:
        fake = FakeSender({"result": []})
        domain = PageDomain(fake)
        await domain.search_in_resource("F1", "https://example.com/x.js", "hello")
        method, params = fake.last_call
        assert method == "Page.searchInResource"
        assert params is not None
        assert params["frameId"] == "F1"
        assert params["query"] == "hello"

    async def test_set_device_metrics_override_full(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2.0, mobile=True,
            scale=1.0, screen_width=375, screen_height=667,
            position_x=0, position_y=0, dont_set_visible_size=True,
            screen_orientation={"type": "portraitPrimary"},
            viewport={"width": 375, "height": 667},
        )
        method, params = fake.last_call
        assert method == "Page.setDeviceMetricsOverride"
        assert params is not None
        assert params["width"] == 375
        assert params["screenWidth"] == 375
        assert params["dontSetVisibleSize"] is True

    async def test_clear_device_metrics_override(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.clear_device_metrics_override()
        assert fake.last_call == ("Page.clearDeviceMetricsOverride", None)

    async def test_set_device_orientation_override(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        assert fake.last_call == (
            "Page.setDeviceOrientationOverride",
            {"alpha": 1.0, "beta": 2.0, "gamma": 3.0},
        )

    async def test_clear_device_orientation_override(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.clear_device_orientation_override()
        assert fake.last_call == ("Page.clearDeviceOrientationOverride", None)

    async def test_set_geolocation_override(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_geolocation_override(37.77, -122.41, 10.0)
        assert fake.last_call == (
            "Page.setGeolocationOverride",
            {"latitude": 37.77, "longitude": -122.41, "accuracy": 10.0},
        )

    async def test_clear_geolocation_override(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.clear_geolocation_override()
        assert fake.last_call == ("Page.clearGeolocationOverride", None)

    async def test_set_touch_emulation_enabled(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_touch_emulation_enabled(True, configuration="mobile")
        assert fake.last_call == (
            "Page.setTouchEmulationEnabled",
            {"enabled": True, "configuration": "mobile"},
        )

    async def test_set_download_behavior(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_download_behavior("allow", download_path="/tmp", events_enabled=True)
        method, params = fake.last_call
        assert method == "Page.setDownloadBehavior"
        assert params is not None
        assert params["behavior"] == "allow"
        assert params["downloadPath"] == "/tmp"
        assert params["eventsEnabled"] is True

    async def test_set_font_families(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_font_families({"standard": "Arial"})
        method, params = fake.last_call
        assert method == "Page.setFontFamilies"
        assert params is not None
        assert params["fontFamilies"] == {"standard": "Arial"}

    async def test_set_font_families_empty(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_font_families()
        assert fake.last_call == ("Page.setFontFamilies", None)

    async def test_set_font_sizes(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_font_sizes(standard=18, fixed=14)
        assert fake.last_call == (
            "Page.setFontSizes",
            {"fontSizes": {"standard": 18, "fixed": 14}},
        )

    async def test_set_ad_blocking_enabled(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_ad_blocking_enabled(True)
        assert fake.last_call == ("Page.setAdBlockingEnabled", {"enabled": True})

    async def test_set_prerendering_allowed(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_prerendering_allowed(False)
        assert fake.last_call == ("Page.setPrerenderingAllowed", {"allowed": False})

    async def test_wait_for_debugger(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.wait_for_debugger()
        assert fake.last_call == ("Page.waitForDebugger", None)

    async def test_generate_test_report(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.generate_test_report("test", group="g1")
        assert fake.last_call == (
            "Page.generateTestReport",
            {"message": "test", "group": "g1"},
        )

    async def test_produce_compilation_cache(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.produce_compilation_cache(scripts=[{"url": "https://example.com/a.js"}])
        method, params = fake.last_call
        assert method == "Page.produceCompilationCache"
        assert params is not None
        assert "scripts" in params

    async def test_produce_compilation_cache_empty(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.produce_compilation_cache()
        assert fake.last_call == ("Page.produceCompilationCache", None)

    async def test_add_compilation_cache(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.add_compilation_cache("https://example.com/a.js", "base64data")
        assert fake.last_call == (
            "Page.addCompilationCache",
            {"url": "https://example.com/a.js", "data": "base64data"},
        )

    async def test_clear_compilation_cache(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.clear_compilation_cache()
        assert fake.last_call == ("Page.clearCompilationCache", None)

    async def test_set_spc_transaction_mode(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_spc_transaction_mode("auto")
        assert fake.last_call == ("Page.setSPCTransactionMode", {"mode": "auto"})

    async def test_set_rph_registration_mode(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_rph_registration_mode("block")
        assert fake.last_call == ("Page.setRPHRegistrationMode", {"mode": "block"})

    async def test_delete_cookie(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.delete_cookie("session", "https://example.com")
        assert fake.last_call == (
            "Page.deleteCookie",
            {"cookieName": "session", "url": "https://example.com"},
        )

    async def test_get_manifest_icons(self) -> None:
        fake = FakeSender({"primaryIcon": "base64"})
        domain = PageDomain(fake)
        await domain.get_manifest_icons()
        assert fake.last_call == ("Page.getManifestIcons", None)

    async def test_get_app_id(self) -> None:
        fake = FakeSender({"appId": "abc"})
        domain = PageDomain(fake)
        await domain.get_app_id()
        assert fake.last_call == ("Page.getAppId", None)

    async def test_get_installability_errors(self) -> None:
        fake = FakeSender({"installabilityErrors": []})
        domain = PageDomain(fake)
        await domain.get_installability_errors()
        assert fake.last_call == ("Page.getInstallabilityErrors", None)

    async def test_get_ad_script_ancestry(self) -> None:
        fake = FakeSender({"ancestry": []})
        domain = PageDomain(fake)
        await domain.get_ad_script_ancestry("F1")
        assert fake.last_call == (
            "Page.getAdScriptAncestry",
            {"frameId": "F1"},
        )

    async def test_get_permissions_policy_state(self) -> None:
        fake = FakeSender({"states": []})
        domain = PageDomain(fake)
        await domain.get_permissions_policy_state("F1")
        assert fake.last_call == (
            "Page.getPermissionsPolicyState",
            {"frameId": "F1"},
        )

    async def test_get_origin_trials(self) -> None:
        fake = FakeSender({"trials": []})
        domain = PageDomain(fake)
        await domain.get_origin_trials("F1")
        method, params = fake.last_call
        assert method == "Page.getOriginTrials"
        assert params is not None
        assert params["frameId"] == "F1"

    async def test_get_origin_trials_no_frame(self) -> None:
        fake = FakeSender({"trials": []})
        domain = PageDomain(fake)
        await domain.get_origin_trials()
        assert fake.last_call == ("Page.getOriginTrials", None)

    async def test_get_annotated_page_content(self) -> None:
        fake = FakeSender({"content": {}})
        domain = PageDomain(fake)
        await domain.get_annotated_page_content()
        assert fake.last_call == ("Page.getAnnotatedPageContent", None)


# ── Network ───────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestNetworkCoverage:
    async def test_delete_cookies_with_all_params(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.delete_cookies(
            "session", url="https://example.com", domain="example.com", path="/",
        )
        method, params = fake.last_call
        assert method == "Network.deleteCookies"
        assert params is not None
        assert params["name"] == "session"
        assert params["url"] == "https://example.com"
        assert params["domain"] == "example.com"
        assert params["path"] == "/"

    async def test_get_response_body(self) -> None:
        fake = FakeSender({"body": "data", "base64Encoded": False})
        domain = NetworkDomain(fake)
        await domain.get_response_body("r1")
        assert fake.last_call == ("Network.getResponseBody", {"requestId": "r1"})

    async def test_set_cache_disabled_with_types(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cache_disabled(True, resource_types=["Image", "Script"])
        method, params = fake.last_call
        assert params is not None
        assert params["cacheDisabled"] is True
        assert params["resourceTypes"] == ["Image", "Script"]

    async def test_can_emulate_network_conditions(self) -> None:
        fake = FakeSender({"result": True})
        domain = NetworkDomain(fake)
        await domain.can_emulate_network_conditions()
        assert fake.last_call == ("Network.canEmulateNetworkConditions", None)

    async def test_can_clear_browser_cache(self) -> None:
        fake = FakeSender({"result": True})
        domain = NetworkDomain(fake)
        await domain.can_clear_browser_cache()
        assert fake.last_call == ("Network.canClearBrowserCache", None)

    async def test_can_clear_browser_cookies(self) -> None:
        fake = FakeSender({"result": True})
        domain = NetworkDomain(fake)
        await domain.can_clear_browser_cookies()
        assert fake.last_call == ("Network.canClearBrowserCookies", None)

    async def test_set_cookies(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        cookies: list[dict[str, Any]] = [{"name": "a", "value": "1"}]
        await domain.set_cookies(cookies)
        assert fake.last_call == ("Network.setCookies", {"cookies": cookies})

    async def test_emulate_network_conditions_by_rule(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.emulate_network_conditions_by_rule("Slow 3G")
        assert fake.last_call == (
            "Network.emulateNetworkConditionsByRule",
            {"networkId": "Slow 3G"},
        )

    async def test_override_network_state(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.override_network_state("Fast 4G")
        assert fake.last_call == ("Network.overrideNetworkState", {"networkId": "Fast 4G"})

    async def test_set_accepted_encodings(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_accepted_encodings(["gzip", "br"])
        assert fake.last_call == (
            "Network.setAcceptedEncodings",
            {"encodings": ["gzip", "br"]},
        )

    async def test_clear_accepted_encodings_override(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.clear_accepted_encodings_override()
        assert fake.last_call == ("Network.clearAcceptedEncodingsOverride", None)

    async def test_get_certificate(self) -> None:
        fake = FakeSender({"tableNames": []})
        domain = NetworkDomain(fake)
        await domain.get_certificate("https://example.com")
        assert fake.last_call == ("Network.getCertificate", {"origin": "https://example.com"})

    async def test_get_security_isolation_status(self) -> None:
        fake = FakeSender({"status": {}})
        domain = NetworkDomain(fake)
        await domain.get_security_isolation_status("F1")
        method, params = fake.last_call
        assert method == "Network.getSecurityIsolationStatus"
        assert params is not None
        assert params["frameId"] == "F1"

    async def test_get_security_isolation_status_no_frame(self) -> None:
        fake = FakeSender({"status": {}})
        domain = NetworkDomain(fake)
        await domain.get_security_isolation_status()
        assert fake.last_call == ("Network.getSecurityIsolationStatus", None)

    async def test_enable_reporting_api(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.enable_reporting_api(True)
        assert fake.last_call == ("Network.enableReportingApi", {"enable": True})

    async def test_replay_xhr(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.replay_xhr("r1")
        assert fake.last_call == ("Network.replayXHR", {"requestId": "r1"})

    async def test_search_in_response_body(self) -> None:
        fake = FakeSender({"result": []})
        domain = NetworkDomain(fake)
        await domain.search_in_response_body("r1", "hello", case_sensitive=True, is_regex=True)
        method, params = fake.last_call
        assert method == "Network.searchInResponseBody"
        assert params is not None
        assert params["requestId"] == "r1"
        assert params["caseSensitive"] is True
        assert params["isRegex"] is True

    async def test_set_attach_debug_stack(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_attach_debug_stack(True)
        assert fake.last_call == ("Network.setAttachDebugStack", {"attach": True})

    async def test_set_request_interception(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        patterns: list[dict[str, Any]] = [{"urlPattern": "*"}]
        await domain.set_request_interception(patterns)
        assert fake.last_call == ("Network.setRequestInterception", {"patterns": patterns})

    async def test_continue_intercepted_request_full(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.continue_intercepted_request(
            "i1", error_reason="Failed", raw_response="resp",
            url="https://new.com", method="POST",
            headers={"X": "Y"}, post_data="data",
        )
        method, params = fake.last_call
        assert method == "Network.continueInterceptedRequest"
        assert params is not None
        assert params["interceptionId"] == "i1"
        assert params["errorReason"] == "Failed"
        assert params["rawResponse"] == "resp"
        assert params["url"] == "https://new.com"
        assert params["method"] == "POST"
        assert params["headers"] == {"X": "Y"}
        assert params["postData"] == "data"

    async def test_get_response_body_for_interception(self) -> None:
        fake = FakeSender({"body": "data"})
        domain = NetworkDomain(fake)
        await domain.get_response_body_for_interception("i1")
        assert fake.last_call == (
            "Network.getResponseBodyForInterception",
            {"interceptionId": "i1"},
        )

    async def test_take_response_body_for_interception_as_stream(self) -> None:
        fake = FakeSender({"stream": "s1"})
        domain = NetworkDomain(fake)
        await domain.take_response_body_for_interception_as_stream("i1")
        assert fake.last_call == (
            "Network.takeResponseBodyForInterceptionAsStream",
            {"interceptionId": "i1"},
        )

    async def test_stream_resource_content(self) -> None:
        fake = FakeSender({"bufferedData": "data"})
        domain = NetworkDomain(fake)
        await domain.stream_resource_content("r1")
        assert fake.last_call == ("Network.streamResourceContent", {"requestId": "r1"})

    async def test_fetch_schemeful_site(self) -> None:
        fake = FakeSender({"schemefulSite": "https://example.com"})
        domain = NetworkDomain(fake)
        await domain.fetch_schemeful_site("r1")
        assert fake.last_call == ("Network.fetchSchemefulSite", {"requestId": "r1"})

    async def test_set_cookie_controls(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cookie_controls(
            enable_third_party_cookie_restriction=True,
            enable_same_site_by_default=True,
            without_same_site_lax_by_default=True,
        )
        method, params = fake.last_call
        assert method == "Network.setCookieControls"
        assert params is not None
        assert params["enableThirdPartyCookieRestriction"] is True

    async def test_enable_device_bound_sessions(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.enable_device_bound_sessions(True)
        assert fake.last_call == ("Network.enableDeviceBoundSessions", {"enable": True})

    async def test_delete_device_bound_session(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.delete_device_bound_session("s1")
        assert fake.last_call == ("Network.deleteDeviceBoundSession", {"sessionId": "s1"})

    async def test_configure_durable_messages(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.configure_durable_messages(max_messages=100)
        method, params = fake.last_call
        assert method == "Network.configureDurableMessages"
        assert params is not None
        assert params["maxMessages"] == 100

    async def test_configure_durable_messages_empty(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.configure_durable_messages()
        assert fake.last_call == ("Network.configureDurableMessages", None)


# ── Emulation ─────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestEmulationCoverage:
    async def test_set_device_metrics_override_with_ua_and_viewport(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2.0, mobile=True,
            user_agent="Mozilla/5.0", screen_orientation={"type": "portraitPrimary"},
            viewport={"width": 375, "height": 667},
        )
        method, params = fake.last_call
        assert method == "Emulation.setDeviceMetricsOverride"
        assert params is not None
        assert params["userAgent"] == "Mozilla/5.0"
        assert params["viewport"] == {"width": 375, "height": 667}

    async def test_set_user_agent_override_with_opts(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_user_agent_override(
            "UA", accept_language="en-US", platform="Win32",
            user_agent_metadata={"brands": []},
        )
        method, params = fake.last_call
        assert method == "Emulation.setUserAgentOverride"
        assert params is not None
        assert params["acceptLanguage"] == "en-US"
        assert params["platform"] == "Win32"

    async def test_can_emulate(self) -> None:
        fake = FakeSender({"result": True})
        domain = EmulationDomain(fake)
        await domain.can_emulate()
        assert fake.last_call == ("Emulation.canEmulate", None)

    async def test_reset_page_scale_factor(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.reset_page_scale_factor()
        assert fake.last_call == ("Emulation.resetPageScaleFactor", None)

    async def test_set_safe_area_insets_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(top=10, left=5, bottom=10, right=5)
        method, params = fake.last_call
        assert method == "Emulation.setSafeAreaInsetsOverride"
        assert params is not None
        assert params["insets"]["top"] == 10

    async def test_set_device_posture_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_posture_override("folded")
        assert fake.last_call == ("Emulation.setDevicePostureOverride", {"posture": "folded"})

    async def test_clear_device_posture_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_device_posture_override()
        assert fake.last_call == ("Emulation.clearDevicePostureOverride", None)

    async def test_set_display_features_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        features: list[dict[str, Any]] = [
            {"orientation": "vertical", "offset": 100, "maskLength": 10, "maskThickness": 5},
        ]
        await domain.set_display_features_override(features)
        method, params = fake.last_call
        assert method == "Emulation.setDisplayFeaturesOverride"
        assert params is not None
        assert params["displayFeatures"] == features

    async def test_clear_display_features_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_display_features_override()
        assert fake.last_call == ("Emulation.clearDisplayFeaturesOverride", None)

    async def test_set_emulated_os_text_scale(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_os_text_scale(1.5)
        assert fake.last_call == ("Emulation.setEmulatedOSTextScale", {"fontScale": 1.5})

    async def test_set_sensor_override_enabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_enabled(True, "accelerometer")
        assert fake.last_call == (
            "Emulation.setSensorOverrideEnabled",
            {"enabled": True, "type": "accelerometer"},
        )

    async def test_get_overridden_sensor_information(self) -> None:
        fake = FakeSender({"requestedFrequencyHz": 60})
        domain = EmulationDomain(fake)
        await domain.get_overridden_sensor_information("gyroscope")
        assert fake.last_call == (
            "Emulation.getOverriddenSensorInformation",
            {"type": "gyroscope"},
        )

    async def test_set_pressure_source_override_enabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_pressure_source_override_enabled("cpu", True, metadata={"k": "v"})
        method, params = fake.last_call
        assert method == "Emulation.setPressureSourceOverrideEnabled"
        assert params is not None
        assert params["metadata"] == {"k": "v"}

    async def test_set_pressure_state_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_pressure_state_override("cpu", "critical", own_contribution=0.8)
        method, params = fake.last_call
        assert method == "Emulation.setPressureStateOverride"
        assert params is not None
        assert params["ownContribution"] == 0.8

    async def test_set_disabled_image_types(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_disabled_image_types(["avif", "webp"])
        assert fake.last_call == (
            "Emulation.setDisabledImageTypes",
            {"imageTypes": ["avif", "webp"]},
        )

    async def test_set_data_saver_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_data_saver_override(True)
        assert fake.last_call == ("Emulation.setDataSaverOverride", {"enabled": True})

    async def test_set_hardware_concurrency_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_hardware_concurrency_override(8)
        assert fake.last_call == (
            "Emulation.setHardwareConcurrencyOverride",
            {"hardwareConcurrency": 8},
        )

    async def test_set_automation_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_automation_override(True)
        assert fake.last_call == ("Emulation.setAutomationOverride", {"enabled": True})

    async def test_set_small_viewport_height_difference_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_small_viewport_height_difference_override(True)
        method, params = fake.last_call
        assert method == "Emulation.setSmallViewportHeightDifferenceOverride"
        assert params is not None

    async def test_get_screen_infos(self) -> None:
        fake = FakeSender({"screenInfos": []})
        domain = EmulationDomain(fake)
        await domain.get_screen_infos()
        assert fake.last_call == ("Emulation.getScreenInfos", None)

    async def test_add_screen(self) -> None:
        fake = FakeSender({"screenId": "s1"})
        domain = EmulationDomain(fake)
        await domain.add_screen(
            1920, 1080, device_scale_factor=1.5, touch=True, external=True, label="main",
        )
        method, params = fake.last_call
        assert method == "Emulation.addScreen"
        assert params is not None
        assert params["label"] == "main"

    async def test_update_screen_full(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.update_screen(
            "s1", width=800, height=600, device_scale_factor=2.0,
            touch=False, external=False, label="updated",
        )
        method, params = fake.last_call
        assert method == "Emulation.updateScreen"
        assert params is not None
        assert params["width"] == 800
        assert params["label"] == "updated"

    async def test_remove_screen(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.remove_screen("s1")
        assert fake.last_call == ("Emulation.removeScreen", {"screenId": "s1"})

    async def test_set_primary_screen(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_primary_screen("s1")
        assert fake.last_call == ("Emulation.setPrimaryScreen", {"screenId": "s1"})


# ── DOM ───────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestDOMCoverage:
    async def test_resolve_node_with_object_id(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(object_id="OBJ-1", object_group="group1")
        method, params = fake.last_call
        assert method == "DOM.resolveNode"
        assert params is not None
        assert params["objectId"] == "OBJ-1"
        assert params["objectGroup"] == "group1"

    async def test_request_node_with_object_id(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.request_node(object_id="OBJ-1")
        method, params = fake.last_call
        assert method == "DOM.requestNode"
        assert params is not None
        assert params["objectId"] == "OBJ-1"

    async def test_set_attributes_as_text_with_name(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attributes_as_text(1, "class='foo'", name="class")
        method, params = fake.last_call
        assert method == "DOM.setAttributesAsText"
        assert params is not None
        assert params["name"] == "class"

    async def test_get_flattened_document(self) -> None:
        fake = FakeSender({"root": {}})
        domain = DOMDomain(fake)
        await domain.get_flattened_document(depth=2, pierce=True)
        assert fake.last_call == (
            "DOM.getFlattenedDocument",
            {"depth": 2, "pierce": True},
        )

    async def test_collect_class_names_from_subtree(self) -> None:
        fake = FakeSender({"classNames": ["a", "b"]})
        domain = DOMDomain(fake)
        await domain.collect_class_names_from_subtree(1)
        assert fake.last_call == (
            "DOM.collectClassNamesFromSubtree",
            {"nodeId": 1},
        )

    async def test_get_content_quads(self) -> None:
        fake = FakeSender({"quads": [[0, 0, 100, 0, 100, 100, 0, 100]]})
        domain = DOMDomain(fake)
        await domain.get_content_quads(1)
        assert fake.last_call == ("DOM.getContentQuads", {"nodeId": 1})

    async def test_set_file_input_files(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_file_input_files(1, ["/tmp/a.txt"])
        assert fake.last_call == (
            "DOM.setFileInputFiles",
            {"nodeId": 1, "files": ["/tmp/a.txt"]},
        )

    async def test_set_outer_html(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_outer_html(1, "<div>hi</div>")
        assert fake.last_call == (
            "DOM.setOuterHTML",
            {"nodeId": 1, "outerHTML": "<div>hi</div>"},
        )

    async def test_set_text_content(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_text_content(1, "hello")
        assert fake.last_call == ("DOM.setNodeValue", {"nodeId": 1, "value": "hello"})

    async def test_get_highlight_object_for_test(self) -> None:
        fake = FakeSender({"highlight": {}})
        domain = DOMDomain(fake)
        await domain.get_highlight_object_for_test(1)
        assert fake.last_call == ("DOM.getHighlightObjectForTest", {"nodeId": 1})

    async def test_get_inner_html(self) -> None:
        fake = FakeSender({"innerHTML": "<p>hi</p>"})
        domain = DOMDomain(fake)
        await domain.get_inner_html(1)
        assert fake.last_call == ("DOM.getInnerHTML", {"nodeId": 1})

    async def test_undo(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.undo()
        assert fake.last_call == ("DOM.undo", None)

    async def test_redo(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.redo()
        assert fake.last_call == ("DOM.redo", None)

    async def test_mark_undoable_state(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.mark_undoable_state()
        assert fake.last_call == ("DOM.markUndoableState", None)

    async def test_hide_highlight(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.hide_highlight()
        assert fake.last_call == ("DOM.hideHighlight", None)

    async def test_highlight_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.highlight_node(1)
        assert fake.last_call == ("DOM.highlightNode", {"nodeId": 1})

    async def test_highlight_rect(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.highlight_rect(0, 0, 100, 100)
        assert fake.last_call == (
            "DOM.highlightRect",
            {"x": 0, "y": 0, "width": 100, "height": 100},
        )

    async def test_push_node_by_path_to_frontend(self) -> None:
        fake = FakeSender({"nodeId": 3})
        domain = DOMDomain(fake)
        await domain.push_node_by_path_to_frontend("0,1,2")
        assert fake.last_call == ("DOM.pushNodeByPathToFrontend", {"path": "0,1,2"})

    async def test_push_nodes_by_backend_ids_to_frontend(self) -> None:
        fake = FakeSender({"nodeIds": [1, 2]})
        domain = DOMDomain(fake)
        await domain.push_nodes_by_backend_ids_to_frontend([10, 20])
        method, params = fake.last_call
        assert method == "DOM.pushNodesByBackendIdsToFrontend"
        assert params is not None
        assert params["backendNodeIds"] == [10, 20]

    async def test_get_nodes_for_subtree_by_style(self) -> None:
        fake = FakeSender({"nodeIds": [1, 2]})
        domain = DOMDomain(fake)
        await domain.get_nodes_for_subtree_by_style(1, ["color"], pierce=True)
        method, params = fake.last_call
        assert method == "DOM.getNodesForSubtreeByStyle"
        assert params is not None
        assert params["pierce"] is True

    async def test_get_relayout_boundary(self) -> None:
        fake = FakeSender({"relayoutBoundary": 5})
        domain = DOMDomain(fake)
        await domain.get_relayout_boundary(1)
        assert fake.last_call == ("DOM.getRelayoutBoundary", {"nodeId": 1})

    async def test_get_top_layer_elements(self) -> None:
        fake = FakeSender({"nodeIds": [1, 2]})
        domain = DOMDomain(fake)
        await domain.get_top_layer_elements()
        assert fake.last_call == ("DOM.getTopLayerElements", None)

    async def test_get_element_by_relation(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_element_by_relation(1, "controlledby")
        assert fake.last_call == (
            "DOM.getElementByRelation",
            {"documentId": 1, "relation": "controlledby"},
        )

    async def test_set_node_stack_traces_enabled(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_node_stack_traces_enabled(True)
        assert fake.last_call == ("DOM.setNodeStackTracesEnabled", {"enabled": True})

    async def test_get_node_stack_traces(self) -> None:
        fake = FakeSender({"creation": {}})
        domain = DOMDomain(fake)
        await domain.get_node_stack_traces(1)
        assert fake.last_call == ("DOM.getNodeStackTraces", {"nodeId": 1})

    async def test_get_file_info(self) -> None:
        fake = FakeSender({"name": "a.txt"})
        domain = DOMDomain(fake)
        await domain.get_file_info("f1")
        assert fake.last_call == ("DOM.getFileInfo", {"fileId": "f1"})

    async def test_get_detached_dom_nodes(self) -> None:
        fake = FakeSender({"detachedNodes": []})
        domain = DOMDomain(fake)
        await domain.get_detached_dom_nodes()
        assert fake.last_call == ("DOM.getDetachedDomNodes", None)

    async def test_set_inspected_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_inspected_node(1)
        assert fake.last_call == ("DOM.setInspectedNode", {"nodeId": 1})

    async def test_set_node_name(self) -> None:
        fake = FakeSender({"nodeId": 2})
        domain = DOMDomain(fake)
        await domain.set_node_name(1, "div")
        assert fake.last_call == ("DOM.setNodeName", {"nodeId": 1, "name": "div"})

    async def test_get_frame_owner(self) -> None:
        fake = FakeSender({"nodeId": 1, "backendNodeId": 2})
        domain = DOMDomain(fake)
        await domain.get_frame_owner("F1")
        assert fake.last_call == ("DOM.getFrameOwner", {"frameId": "F1"})

    async def test_get_container_for_node_with_name(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_container_for_node(1, container_name="c1")
        method, params = fake.last_call
        assert method == "DOM.getContainerForNode"
        assert params is not None
        assert params["containerName"] == "c1"

    async def test_get_querying_descendants_for_container(self) -> None:
        fake = FakeSender({"nodeIds": [2, 3]})
        domain = DOMDomain(fake)
        await domain.get_querying_descendants_for_container(1)
        assert fake.last_call == (
            "DOM.getQueryingDescendantsForContainer",
            {"nodeId": 1},
        )

    async def test_get_anchor_element_with_name(self) -> None:
        fake = FakeSender({"anchorElement": 5})
        domain = DOMDomain(fake)
        await domain.get_anchor_element(1, anchor_name="a1")
        method, params = fake.last_call
        assert method == "DOM.getAnchorElement"
        assert params is not None
        assert params["anchorName"] == "a1"

    async def test_force_show_popover(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.force_show_popover(1)
        assert fake.last_call == ("DOM.forceShowPopover", {"nodeId": 1})


# ── Storage ───────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestStorageCoverage:
    async def test_get_storage_key(self) -> None:
        fake = FakeSender({"storageKey": "key1"})
        domain = StorageDomain(fake)
        await domain.get_storage_key("F1")
        assert fake.last_call == ("Storage.getStorageKey", {"frameId": "F1"})

    async def test_clear_data_for_storage_key(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_data_for_storage_key("key1", "cookies,local_storage")
        method, params = fake.last_call
        assert method == "Storage.clearDataForStorageKey"
        assert params is not None
        assert params["storageTypes"] == "cookies,local_storage"

    async def test_override_quota_for_origin_with_size(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.override_quota_for_origin("https://example.com", quota_size=1024)
        method, params = fake.last_call
        assert method == "Storage.overrideQuotaForOrigin"
        assert params is not None
        assert params["quotaSize"] == 1024

    async def test_track_indexed_db_for_storage_key(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.track_indexed_db_for_storage_key("key1")
        assert fake.last_call == (
            "Storage.trackIndexedDBForStorageKey",
            {"storageKey": "key1"},
        )

    async def test_untrack_indexed_db_for_storage_key(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.untrack_indexed_db_for_storage_key("key1")
        assert fake.last_call == (
            "Storage.untrackIndexedDBForStorageKey",
            {"storageKey": "key1"},
        )

    async def test_track_cache_storage_for_storage_key(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.track_cache_storage_for_storage_key("key1")
        assert fake.last_call == (
            "Storage.trackCacheStorageForStorageKey",
            {"storageKey": "key1"},
        )

    async def test_untrack_cache_storage_for_storage_key(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.untrack_cache_storage_for_storage_key("key1")
        assert fake.last_call == (
            "Storage.untrackCacheStorageForStorageKey",
            {"storageKey": "key1"},
        )

    async def test_get_interest_group_details(self) -> None:
        fake = FakeSender({"details": {}})
        domain = StorageDomain(fake)
        await domain.get_interest_group_details("https://owner.com", "group1")
        method, params = fake.last_call
        assert method == "Storage.getInterestGroupDetails"
        assert params is not None

    async def test_set_interest_group_tracking(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_interest_group_tracking(True)
        assert fake.last_call == (
            "Storage.setInterestGroupTracking",
            {"enable": True},
        )

    async def test_set_interest_group_auction_tracking(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_interest_group_auction_tracking(True)
        assert fake.last_call == (
            "Storage.setInterestGroupAuctionTracking",
            {"enable": True},
        )

    async def test_get_shared_storage_metadata(self) -> None:
        fake = FakeSender({"metadata": {}})
        domain = StorageDomain(fake)
        await domain.get_shared_storage_metadata("https://owner.com")
        assert fake.last_call == (
            "Storage.getSharedStorageMetadata",
            {"ownerOrigin": "https://owner.com"},
        )

    async def test_get_shared_storage_entries(self) -> None:
        fake = FakeSender({"entries": []})
        domain = StorageDomain(fake)
        await domain.get_shared_storage_entries("https://owner.com")
        assert fake.last_call == (
            "Storage.getSharedStorageEntries",
            {"ownerOrigin": "https://owner.com"},
        )

    async def test_set_shared_storage_entry(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_shared_storage_entry("https://owner.com", "k", "v", ignore_if_present=True)
        method, params = fake.last_call
        assert method == "Storage.setSharedStorageEntry"
        assert params is not None
        assert params["ignoreIfPresent"] is True

    async def test_delete_shared_storage_entry(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.delete_shared_storage_entry("https://owner.com", "k")
        method, params = fake.last_call
        assert method == "Storage.deleteSharedStorageEntry"
        assert params is not None

    async def test_clear_shared_storage_entries(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_shared_storage_entries("https://owner.com")
        method, params = fake.last_call
        assert method == "Storage.clearSharedStorageEntries"
        assert params is not None

    async def test_reset_shared_storage_budget_with_budget(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.reset_shared_storage_budget("https://owner.com", budget=100.0)
        method, params = fake.last_call
        assert method == "Storage.resetSharedStorageBudget"
        assert params is not None
        assert params["budget"] == 100.0

    async def test_set_shared_storage_tracking(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_shared_storage_tracking(True)
        assert fake.last_call == (
            "Storage.setSharedStorageTracking",
            {"enable": True},
        )

    async def test_set_storage_bucket_tracking(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_storage_bucket_tracking("key1", True)
        method, params = fake.last_call
        assert method == "Storage.setStorageBucketTracking"
        assert params is not None

    async def test_delete_storage_bucket(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.delete_storage_bucket("key1", "bucket1")
        method, params = fake.last_call
        assert method == "Storage.deleteStorageBucket"
        assert params is not None

    async def test_run_bounce_tracking_mitigations(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.run_bounce_tracking_mitigations()
        assert fake.last_call == ("Storage.runBounceTrackingMitigations", None)

    async def test_get_related_website_sets(self) -> None:
        fake = FakeSender({"sets": []})
        domain = StorageDomain(fake)
        await domain.get_related_website_sets()
        assert fake.last_call == ("Storage.getRelatedWebsiteSets", None)

    async def test_set_protected_audience_k_anonymity(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_protected_audience_k_anonymity(
            "https://owner.com", "group1", True,
        )
        method, params = fake.last_call
        assert method == "Storage.setProtectedAudienceKAnonymity"
        assert params is not None
        assert params["kAnonymity"] is True


# ── Target ────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestTargetCoverage:
    async def test_get_target_info(self) -> None:
        fake = FakeSender({"targetInfo": {}})
        domain = TargetDomain(fake)
        await domain.get_target_info("T1")
        assert fake.last_call == ("Target.getTargetInfo", {"targetId": "T1"})

    async def test_set_auto_attach_with_flatten(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_auto_attach(True, flatten=True, wait_for_debugger_on_start=True)
        method, params = fake.last_call
        assert method == "Target.setAutoAttach"
        assert params is not None
        assert params["flatten"] is True

    async def test_get_browser_contexts(self) -> None:
        fake = FakeSender({"browserContextIds": []})
        domain = TargetDomain(fake)
        await domain.get_browser_contexts()
        assert fake.last_call == ("Target.getBrowserContexts", None)

    async def test_attach_to_browser_target(self) -> None:
        fake = FakeSender({"sessionId": "S1"})
        domain = TargetDomain(fake)
        await domain.attach_to_browser_target()
        assert fake.last_call == ("Target.attachToBrowserTarget", None)

    async def test_send_message_to_target(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.send_message_to_target("msg", target_id="T1", session_id="S1")
        method, params = fake.last_call
        assert method == "Target.sendMessageToTarget"
        assert params is not None
        assert params["targetId"] == "T1"
        assert params["sessionId"] == "S1"

    async def test_auto_attach_related(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.auto_attach_related("T1", True, wait_for_debugger_on_start=True)
        method, params = fake.last_call
        assert method == "Target.autoAttachRelated"
        assert params is not None

    async def test_set_remote_locations(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_remote_locations([{"host": "localhost", "port": "9222"}])
        method, params = fake.last_call
        assert method == "Target.setRemoteLocations"
        assert params is not None

    async def test_get_dev_tools_target(self) -> None:
        fake = FakeSender({"targetInfo": {}})
        domain = TargetDomain(fake)
        await domain.get_dev_tools_target()
        assert fake.last_call == ("Target.getDevToolsTarget", None)

    async def test_open_dev_tools(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.open_dev_tools()
        assert fake.last_call == ("Target.openDevTools", None)


# ── BluetoothEmulation ────────────────────────────────────────────────────


@pytest.mark.unit
class TestBluetoothEmulationCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable()
        assert fake.last_call == ("BluetoothEmulation.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.disable()
        assert fake.last_call == ("BluetoothEmulation.disable", None)

    async def test_simulate_preconnected_peripheral(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_preconnected_peripheral(
            "addr1", "name1", known_service_uuids=["uuid1"],
        )
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulatePreconnectedPeripheral"
        assert params is not None
        assert params["knownServiceUuids"] == ["uuid1"]

    async def test_simulate_advertisement(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_advertisement({"gpAdvertisement": {}})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateAdvertisement"
        assert params is not None

    async def test_set_simulated_central_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("poweredOn")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.setSimulatedCentralState"
        assert params is not None

    async def test_add_service(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_service("addr1", {"uuid": "s1", "isPrimary": True})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addService"
        assert params is not None

    async def test_remove_service(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_service("addr1", "uuid1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeService"
        assert params is not None

    async def test_add_characteristic(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_characteristic("addr1", "uuid1", {"uuid": "c1"})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addCharacteristic"
        assert params is not None

    async def test_remove_characteristic(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_characteristic("addr1", "uuid1", "uuid2")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeCharacteristic"
        assert params is not None

    async def test_add_descriptor(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_descriptor("addr1", "uuid1", "uuid2", {"uuid": "d1"})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addDescriptor"
        assert params is not None

    async def test_remove_descriptor(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_descriptor("addr1", "uuid1", "uuid2", "uuid3")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeDescriptor"
        assert params is not None

    async def test_simulate_gatt_disconnection(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_disconnection("addr1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTDisconnection"
        assert params is not None

    async def test_simulate_gatt_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_operation_response("addr1", "uuid1", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTOperationResponse"
        assert params is not None

    async def test_simulate_characteristic_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response("addr1", "uuid1", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateCharacteristicOperationResponse"
        assert params is not None

    async def test_simulate_descriptor_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_descriptor_operation_response("addr1", "uuid1", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateDescriptorOperationResponse"
        assert params is not None


# ── SmartCardEmulation ────────────────────────────────────────────────────


@pytest.mark.unit
class TestSmartCardEmulationCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.enable()
        assert fake.last_call == ("SmartCardEmulation.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.disable()
        assert fake.last_call == ("SmartCardEmulation.disable", None)

    async def test_report_establish_context_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_establish_context_result("ctx1", 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportEstablishContextResult"
        assert params is not None

    async def test_report_release_context_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_release_context_result("ctx1", 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportReleaseContextResult"
        assert params is not None

    async def test_report_list_readers_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("ctx1", [], 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportListReadersResult"
        assert params is not None

    async def test_report_get_status_change_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_get_status_change_result("ctx1", [], 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportGetStatusChangeResult"
        assert params is not None

    async def test_report_connect_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("ctx1", "reader1", "card1", 0, 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportConnectResult"
        assert params is not None

    async def test_report_status_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("ctx1", "reader1", 0, 0, 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportStatusResult"
        assert params is not None

    async def test_report_data_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_data_result("card1", "resp1", 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportDataResult"
        assert params is not None

    async def test_report_begin_transaction_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_begin_transaction_result("card1", 0)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportBeginTransactionResult"
        assert params is not None

    async def test_report_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error(context_id="ctx1", error=1)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportError"
        assert params is not None

    async def test_report_plain_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_plain_result(0, context_id="ctx1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportPlainResult"
        assert params is not None


# ── Sync API ──────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestSyncCoverage:
    def test_run_method(self) -> None:
        mock_session = MagicMock()
        mock_session.page = "page_domain"
        mock_session.network = "net_domain"
        mock_session.dom = "dom_domain"
        mock_session.input = "input_domain"
        mock_session.emulation = "emul_domain"
        mock_session.fetch = "fetch_domain"
        mock_session.target = "target_domain"
        mock_session.runtime = "runtime_domain"
        sync_session = SyncCDPSession(mock_session)
        assert sync_session.page == "page_domain"
        assert sync_session.network == "net_domain"
        assert sync_session.dom == "dom_domain"
        assert sync_session.input == "input_domain"
        assert sync_session.emulation == "emul_domain"
        assert sync_session.fetch == "fetch_domain"
        assert sync_session.target == "target_domain"
        assert sync_session.runtime == "runtime_domain"

    def test_sync_session_run(self) -> None:
        mock_session = MagicMock()
        mock_session.page = MagicMock()
        mock_session.page.enable = AsyncMock(return_value={"ok": True})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.run(mock_session.page.enable())
        assert result == {"ok": True}

    def test_sync_session_send(self) -> None:
        mock_session = MagicMock()
        mock_session.send = AsyncMock(return_value={"result": 1})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.send("Page.enable")
        assert result == {"result": 1}

    def test_sync_session_close(self) -> None:
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        sync_session = SyncCDPSession(mock_session)
        sync_session.close()
        mock_session.close.assert_called_once()

    def test_wait_for_navigation(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_navigation = AsyncMock(return_value={"frameId": "F1"})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.wait_for_navigation(url="https://example.com", timeout=5.0)
        assert result == {"frameId": "F1"}

    def test_wait_for_load_state(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_load_state = AsyncMock(return_value={})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.wait_for_load_state(state="load", timeout=5.0)
        assert result == {}

    def test_wait_for_selector(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_selector = AsyncMock(return_value=42)
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.wait_for_selector(".btn", timeout=1.0)
        assert result == 42

    def test_wait_for_network_idle(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_network_idle = AsyncMock()
        sync_session = SyncCDPSession(mock_session)
        sync_session.wait_for_network_idle(idle_time=0.3, timeout=5.0)
        mock_session.wait_for_network_idle.assert_called_once()

    def test_session_id_and_target_id(self) -> None:
        mock_session = MagicMock()
        mock_session.session_id = "S1"
        mock_session.target_id = "T1"
        sync_session = SyncCDPSession(mock_session)
        assert sync_session.session_id == "S1"
        assert sync_session.target_id == "T1"

    def test_client_launch(self) -> None:
        mock_client = MagicMock()
        mock_client.close = AsyncMock()
        sync_client = SyncCDPClient(mock_client)
        assert sync_client._client is mock_client

    def test_client_new_page(self) -> None:
        mock_client = MagicMock()
        mock_session = MagicMock()
        mock_client.new_page = AsyncMock(return_value=mock_session)
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.new_page("https://example.com")
        assert isinstance(result, SyncCDPSession)

    def test_client_connect_to_page(self) -> None:
        mock_client = MagicMock()
        mock_session = MagicMock()
        mock_client.connect_to_page = AsyncMock(return_value=mock_session)
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.connect_to_page("T1")
        assert isinstance(result, SyncCDPSession)

    def test_client_send(self) -> None:
        mock_client = MagicMock()
        mock_client.send = AsyncMock(return_value={"ok": True})
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.send("Page.enable")
        assert result == {"ok": True}

    def test_client_close(self) -> None:
        mock_client = MagicMock()
        mock_client.close = AsyncMock()
        sync_client = SyncCDPClient(mock_client)
        sync_client.close()
        mock_client.close.assert_called_once()

    def test_client_context_manager(self) -> None:
        mock_client = MagicMock()
        mock_client.close = AsyncMock()
        sync_client = SyncCDPClient(mock_client)
        with sync_client as ctx:
            assert ctx is sync_client
        mock_client.close.assert_called_once()
