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
from cdpwave.domains.dom_storage import DOMStorageDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.runtime import RuntimeDomain
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
        assert params["scriptSource"] == "alert(1)"

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

    async def test_set_geolocation_override_partial(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_geolocation_override(latitude=40.0)
        method, params = fake.last_call
        assert method == "Page.setGeolocationOverride"
        assert params == {"latitude": 40.0}

    async def test_set_geolocation_override_clear(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_geolocation_override()
        assert fake.last_call == ("Page.setGeolocationOverride", None)

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
        await domain.set_download_behavior("allow", download_path="/tmp")
        method, params = fake.last_call
        assert method == "Page.setDownloadBehavior"
        assert params is not None
        assert params["behavior"] == "allow"
        assert params["downloadPath"] == "/tmp"
        assert "eventsEnabled" not in params

    async def test_set_download_behavior_deny(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_download_behavior("deny")
        method, params = fake.last_call
        assert params == {"behavior": "deny"}

    async def test_set_font_families(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_font_families({"standard": "Arial"})
        method, params = fake.last_call
        assert method == "Page.setFontFamilies"
        assert params is not None
        assert params["fontFamilies"] == {"standard": "Arial"}

    async def test_set_font_families_with_for_scripts(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        scripts = [{"script": "Hangul", "fontFamilies": {"standard": "Noto Sans KR"}}]
        await domain.set_font_families({"standard": "Arial"}, for_scripts=scripts)
        method, params = fake.last_call
        assert params is not None
        assert params["forScripts"] == scripts

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
        assert fake.last_call == ("Page.setPrerenderingAllowed", {"isAllowed": False})

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

    async def test_produce_compilation_cache_with_eager(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        scripts = [{"url": "https://example.com/a.js", "eager": True}]
        await domain.produce_compilation_cache(scripts=scripts)
        method, params = fake.last_call
        assert method == "Page.produceCompilationCache"
        assert params == {"scripts": scripts}

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
        await domain.set_spc_transaction_mode("autoAccept")
        assert fake.last_call == ("Page.setSPCTransactionMode", {"mode": "autoAccept"})

    async def test_set_rph_registration_mode(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_rph_registration_mode("autoReject")
        assert fake.last_call == ("Page.setRPHRegistrationMode", {"mode": "autoReject"})

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

    async def test_get_annotated_page_content_with_actionable_info(self) -> None:
        fake = FakeSender({"content": {}})
        domain = PageDomain(fake)
        await domain.get_annotated_page_content(include_actionable_information=True)
        method, params = fake.last_call
        assert method == "Page.getAnnotatedPageContent"
        assert params == {"includeActionableInformation": True}

    async def test_enable_with_file_chooser_event(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.enable(enable_file_chooser_opened_event=True)
        method, params = fake.last_call
        assert method == "Page.enable"
        assert params == {"enableFileChooserOpenedEvent": True}

    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Page.enable", None)

    async def test_reload_with_script_and_loader(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload(
            ignore_cache=True,
            script_to_evaluate_on_load="console.log('hi')",
            loader_id="L1",
        )
        method, params = fake.last_call
        assert method == "Page.reload"
        assert params["ignoreCache"] is True
        assert params["scriptToEvaluateOnLoad"] == "console.log('hi')"
        assert params["loaderId"] == "L1"

    async def test_capture_screenshot_optimize_for_speed(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(optimize_for_speed=True)
        method, params = fake.last_call
        assert params["optimizeForSpeed"] is True

    async def test_print_to_pdf_generate_tagged_pdf(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(generate_tagged_pdf=True)
        method, params = fake.last_call
        assert params["generateTaggedPDF"] is True

    async def test_print_to_pdf_generate_document_outline(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(generate_document_outline=True)
        method, params = fake.last_call
        assert params["generateDocumentOutline"] is True

    async def test_add_script_with_include_command_line_api(self) -> None:
        fake = FakeSender({"identifier": "scr1"})
        domain = PageDomain(fake)
        await domain.add_script_to_evaluate_on_new_document(
            "console.log('hi')", include_command_line_api=True,
        )
        method, params = fake.last_call
        assert params["includeCommandLineAPI"] is True

    async def test_get_app_manifest_with_manifest_id(self) -> None:
        fake = FakeSender({"url": "", "data": "", "errors": [], "parsed": {}})
        domain = PageDomain(fake)
        await domain.get_app_manifest(manifest_id="manifest-1")
        method, params = fake.last_call
        assert params == {"manifestId": "manifest-1"}

    async def test_create_isolated_world_with_csp(self) -> None:
        fake = FakeSender({"executionContextId": 1})
        domain = PageDomain(fake)
        await domain.create_isolated_world(
            "frame1", content_security_policy="script-src 'self'",
        )
        method, params = fake.last_call
        assert params["contentSecurityPolicy"] == "script-src 'self'"

    async def test_set_intercept_file_chooser_with_cancel(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_intercept_file_chooser_dialog(True, cancel=True)
        method, params = fake.last_call
        assert params["enabled"] is True
        assert params["cancel"] is True

    async def test_stop_sends_stop_loading(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.stop()
        assert fake.last_call == ("Page.stopLoading", None)

    async def test_set_spc_transaction_mode_valid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_spc_transaction_mode("autoAccept")
        assert fake.last_call == (
            "Page.setSPCTransactionMode",
            {"mode": "autoAccept"},
        )

    async def test_set_spc_transaction_mode_all_enums(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        for mode in (
            "none", "autoAccept", "autoChooseToAuthAnotherWay",
            "autoReject", "autoOptOut",
        ):
            await domain.set_spc_transaction_mode(mode)
            method, params = fake.last_call
            assert method == "Page.setSPCTransactionMode"
            assert params["mode"] == mode

    async def test_set_spc_transaction_mode_invalid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="mode must be one of"):
            await domain.set_spc_transaction_mode("auto")

    async def test_set_rph_registration_mode_valid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_rph_registration_mode("autoReject")
        assert fake.last_call == (
            "Page.setRPHRegistrationMode",
            {"mode": "autoReject"},
        )

    async def test_set_rph_registration_mode_all_enums(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        for mode in ("none", "autoAccept", "autoReject"):
            await domain.set_rph_registration_mode(mode)
            method, params = fake.last_call
            assert method == "Page.setRPHRegistrationMode"
            assert params["mode"] == mode

    async def test_set_rph_registration_mode_invalid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="mode must be one of"):
            await domain.set_rph_registration_mode("block")

    async def test_set_touch_emulation_invalid_config(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="configuration must be"):
            await domain.set_touch_emulation_enabled(True, configuration="tablet")

    async def test_set_download_behavior_invalid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="behavior must be"):
            await domain.set_download_behavior("block")

    async def test_capture_snapshot_invalid_format(self) -> None:
        fake = FakeSender({"data": "x"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="format must be 'mhtml'"):
            await domain.capture_snapshot(format="html")

    async def test_navigate_with_referrer_policy(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        await domain.navigate("https://example.com", referrer_policy="noReferrer")
        method, params = fake.last_call
        assert params["referrerPolicy"] == "noReferrer"

    async def test_navigate_invalid_referrer_policy(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="referrer_policy must be one of"):
            await domain.navigate("https://example.com", referrer_policy="invalid")

    async def test_navigate_with_all_params(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        await domain.navigate(
            "https://example.com",
            referrer="https://ref.com",
            transition_type="link",
            frame_id="F1",
            referrer_policy="strictOrigin",
        )
        method, params = fake.last_call
        assert params["url"] == "https://example.com"
        assert params["referrer"] == "https://ref.com"
        assert params["transitionType"] == "link"
        assert params["frameId"] == "F1"
        assert params["referrerPolicy"] == "strictOrigin"

    async def test_reload_default_ignore_cache_false(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload()
        assert fake.last_call == ("Page.reload", None)

    async def test_print_to_pdf_return_as_stream(self) -> None:
        fake = FakeSender({"stream": "handle1"})
        domain = PageDomain(fake)
        result = await domain.print_to_pdf(return_as_stream=True)
        method, params = fake.last_call
        assert params["transferMode"] == "ReturnAsStream"
        assert result == {"stream": "handle1"}

    async def test_capture_screenshot_webp_format(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(format="webp")
        method, params = fake.last_call
        assert params["format"] == "webp"

    async def test_set_font_sizes_only_standard(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_font_sizes(standard=20)
        method, params = fake.last_call
        assert params["fontSizes"]["standard"] == 20

    async def test_set_device_metrics_override_all_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_device_metrics_override(
            width=390,
            height=844,
            device_scale_factor=3.0,
            mobile=True,
            scale=1.0,
            screen_width=390,
            screen_height=844,
            position_x=0,
            position_y=0,
            dont_set_visible_size=True,
            screen_orientation={"type": "portraitPrimary", "angle": 0},
            viewport={"x": 0, "y": 0, "width": 390, "height": 844, "scale": 1},
        )
        method, params = fake.last_call
        assert params["width"] == 390
        assert params["height"] == 844
        assert params["deviceScaleFactor"] == 3.0
        assert params["mobile"] is True
        assert params["dontSetVisibleSize"] is True
        assert params["screenOrientation"] == {"type": "portraitPrimary", "angle": 0}
        assert params["viewport"]["width"] == 390

    async def test_search_in_resource_with_regex(self) -> None:
        fake = FakeSender({"result": []})
        domain = PageDomain(fake)
        await domain.search_in_resource(
            "F1", "https://example.com/x.js", "test.*", is_regex=True,
        )
        method, params = fake.last_call
        assert params["isRegex"] is True
        assert params["query"] == "test.*"

    async def test_start_screencast_all_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.start_screencast(
            format="png", quality=90, max_width=1024, max_height=768, every_nth_frame=5,
        )
        method, params = fake.last_call
        assert params["format"] == "png"
        assert params["quality"] == 90
        assert params["maxWidth"] == 1024
        assert params["maxHeight"] == 768
        assert params["everyNthFrame"] == 5

    async def test_start_screencast_invalid_format_webp(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="format must be"):
            await domain.start_screencast(format="webp")

    async def test_handle_java_script_dialog_dismiss(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.handle_java_script_dialog(accept=False)
        method, params = fake.last_call
        assert params["accept"] is False
        assert "promptText" not in params

    async def test_set_web_lifecycle_state_frozen(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_web_lifecycle_state("frozen")
        assert fake.last_call == ("Page.setWebLifecycleState", {"state": "frozen"})

    async def test_set_web_lifecycle_state_active(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_web_lifecycle_state("active")
        assert fake.last_call == ("Page.setWebLifecycleState", {"state": "active"})

    async def test_reload_with_script_only(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload(script_to_evaluate_on_load="console.log('hi')")
        method, params = fake.last_call
        assert params == {"scriptToEvaluateOnLoad": "console.log('hi')"}

    async def test_reload_with_loader_id_only(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload(loader_id="L1")
        method, params = fake.last_call
        assert params == {"loaderId": "L1"}

    async def test_navigate_referrer_policy_all_enums(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        policies = [
            "noReferrer", "noReferrerWhenDowngrade", "origin",
            "originWhenCrossOrigin", "sameOrigin", "strictOrigin",
            "strictOriginWhenCrossOrigin", "unsafeUrl",
        ]
        for policy in policies:
            await domain.navigate("https://example.com", referrer_policy=policy)
            method, params = fake.last_call
            assert params["referrerPolicy"] == policy

    async def test_navigate_invalid_transition_type(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="transition_type must be one of"):
            await domain.navigate("https://example.com", transition_type="invalid")

    async def test_navigate_transition_type_all_enums(self) -> None:
        fake = FakeSender({"frameId": "F1"})
        domain = PageDomain(fake)
        transitions = [
            "link", "typed", "address_bar", "auto_bookmark",
            "auto_subframe", "manual_subframe", "generated",
            "auto_toplevel", "form_submit", "reload", "keyword",
            "keyword_generated", "other",
        ]
        for t in transitions:
            await domain.navigate("https://example.com", transition_type=t)
            method, params = fake.last_call
            assert params["transitionType"] == t

    async def test_capture_screenshot_webp_with_quality(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(format="webp", quality=50)
        method, params = fake.last_call
        assert params["format"] == "webp"
        assert params["quality"] == 50


# ── Runtime ──────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestRuntimeCoverage:
    async def test_evaluate_with_include_command_line_api(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 42}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", include_command_line_api=True)
        method, params = fake.last_call
        assert params["includeCommandLineAPI"] is True

    async def test_evaluate_without_include_command_line_api(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 42}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1")
        method, params = fake.last_call
        assert "includeCommandLineAPI" not in params

    async def test_call_function_on_with_user_gesture(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => 42", execution_context_id=1, user_gesture=True,
        )
        method, params = fake.last_call
        assert params["userGesture"] is True

    async def test_call_function_on_without_user_gesture(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on("() => 42", execution_context_id=1)
        method, params = fake.last_call
        assert "userGesture" not in params

    async def test_call_function_on_await_promise_not_sent_when_false(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on("() => 42", execution_context_id=1)
        method, params = fake.last_call
        assert "awaitPromise" not in params

    async def test_call_function_on_await_promise_sent_when_true(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => Promise.resolve(42)", execution_context_id=1, await_promise=True,
        )
        method, params = fake.last_call
        assert params["awaitPromise"] is True

    async def test_get_properties_with_accessor_only(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1", accessor_properties_only=True)
        method, params = fake.last_call
        assert params["accessorPropertiesOnly"] is True

    async def test_get_properties_with_generate_preview(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1", generate_preview=True)
        method, params = fake.last_call
        assert params["generatePreview"] is True

    async def test_get_properties_with_non_indexed_only(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1", non_indexed_properties_only=True)
        method, params = fake.last_call
        assert params["nonIndexedPropertiesOnly"] is True

    async def test_get_properties_default_no_extras(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1")
        method, params = fake.last_call
        assert "accessorPropertiesOnly" not in params
        assert "generatePreview" not in params
        assert "nonIndexedPropertiesOnly" not in params
        assert "ownProperties" not in params

    async def test_get_properties_own_properties_true(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1", own_properties=True)
        method, params = fake.last_call
        assert params["ownProperties"] is True

    async def test_add_binding_with_execution_context_id(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.add_binding("myBinding", execution_context_id=3)
        method, params = fake.last_call
        assert params["executionContextId"] == 3

    async def test_add_binding_with_execution_context_name(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.add_binding("myBinding", execution_context_name="ctx1")
        method, params = fake.last_call
        assert params["executionContextName"] == "ctx1"

    async def test_add_binding_default_only_name(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.add_binding("myBinding")
        method, params = fake.last_call
        assert params == {"name": "myBinding"}

    async def test_run_script_with_object_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("S1", object_group="group1")
        method, params = fake.last_call
        assert params["objectGroup"] == "group1"

    async def test_run_script_with_silent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("S1", silent=True)
        method, params = fake.last_call
        assert params["silent"] is True

    async def test_run_script_with_include_command_line_api(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("S1", include_command_line_api=True)
        method, params = fake.last_call
        assert params["includeCommandLineAPI"] is True

    async def test_run_script_with_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("S1", generate_preview=True)
        method, params = fake.last_call
        assert params["generatePreview"] is True

    async def test_run_script_default_no_extras(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("S1")
        method, params = fake.last_call
        assert "objectGroup" not in params
        assert "silent" not in params
        assert "includeCommandLineAPI" not in params
        assert "generatePreview" not in params
        assert "awaitPromise" not in params
        assert "returnByValue" not in params

    async def test_await_promise_with_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.await_promise("P1", generate_preview=True)
        method, params = fake.last_call
        assert params["generatePreview"] is True

    async def test_await_promise_default_no_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.await_promise("P1")
        method, params = fake.last_call
        assert "generatePreview" not in params
        assert "returnByValue" not in params

    async def test_set_max_call_stack_size_to_capture(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.set_max_call_stack_size_to_capture(100)
        method, params = fake.last_call
        assert method == "Runtime.setMaxCallStackSizeToCapture"
        assert params["size"] == 100

    async def test_set_max_call_stack_size_negative_raises(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="size must be >= 0"):
            await domain.set_max_call_stack_size_to_capture(-1)

    async def test_evaluate_with_throw_on_side_effect(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", throw_on_side_effect=True)
        _, params = fake.last_call
        assert params["throwOnSideEffect"] is True

    async def test_evaluate_with_timeout(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", timeout=5000)
        _, params = fake.last_call
        assert params["timeout"] == 5000
        assert isinstance(params["timeout"], int)

    async def test_evaluate_with_disable_breaks(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", disable_breaks=True)
        _, params = fake.last_call
        assert params["disableBreaks"] is True

    async def test_evaluate_with_repl_mode(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", repl_mode=True)
        _, params = fake.last_call
        assert params["replMode"] is True

    async def test_evaluate_with_allow_unsafe_eval_blocked_by_csp(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", allow_unsafe_eval_blocked_by_csp=False)
        _, params = fake.last_call
        assert params["allowUnsafeEvalBlockedByCSP"] is False

    async def test_evaluate_with_unique_context_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", unique_context_id="ctx-abc")
        _, params = fake.last_call
        assert params["uniqueContextId"] == "ctx-abc"

    async def test_evaluate_with_serialization_options(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate(
            "1+1", serialization_options={"serialization": "deep"},
        )
        _, params = fake.last_call
        assert params["serializationOptions"] == {"serialization": "deep"}

    async def test_evaluate_default_no_advanced_params(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1")
        _, params = fake.last_call
        for key in (
            "throwOnSideEffect", "timeout", "disableBreaks",
            "replMode", "allowUnsafeEvalBlockedByCSP",
            "uniqueContextId", "serializationOptions",
        ):
            assert key not in params

    async def test_call_function_on_with_throw_on_side_effect(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => 42", execution_context_id=1, throw_on_side_effect=True,
        )
        _, params = fake.last_call
        assert params["throwOnSideEffect"] is True

    async def test_call_function_on_with_unique_context_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => 42", unique_context_id="ctx-xyz",
        )
        _, params = fake.last_call
        assert params["uniqueContextId"] == "ctx-xyz"

    async def test_call_function_on_with_serialization_options(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => 42", execution_context_id=1,
            serialization_options={"serialization": "json"},
        )
        _, params = fake.last_call
        assert params["serializationOptions"] == {"serialization": "json"}

    async def test_call_function_on_default_no_advanced_params(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on("() => 42", execution_context_id=1)
        _, params = fake.last_call
        for key in ("throwOnSideEffect", "uniqueContextId", "serializationOptions"):
            assert key not in params

    async def test_evaluate_allow_unsafe_eval_default_not_sent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1")
        _, params = fake.last_call
        assert "allowUnsafeEvalBlockedByCSP" not in params

    async def test_evaluate_allow_unsafe_eval_false_sent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", allow_unsafe_eval_blocked_by_csp=False)
        _, params = fake.last_call
        assert params["allowUnsafeEvalBlockedByCSP"] is False

    async def test_call_function_on_with_unique_context_id_only(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "() => 42", unique_context_id="ctx-unique",
        )
        _, params = fake.last_call
        assert params["uniqueContextId"] == "ctx-unique"
        assert "objectId" not in params
        assert "executionContextId" not in params

    async def test_call_function_on_no_context_raises(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="unique_context_id"):
            await domain.call_function_on("() => 42")

    async def test_evaluate_mutual_exclusivity_context_ids(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="mutually exclusive"):
            await domain.evaluate(
                "1+1", execution_context_id=1, unique_context_id="ctx",
            )

    async def test_call_function_on_mutual_exclusivity_context_ids(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="mutually exclusive"):
            await domain.call_function_on(
                "() => 42",
                execution_context_id=1,
                unique_context_id="ctx",
            )

    async def test_call_function_on_mutual_exclusivity_object_and_context(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="mutually exclusive"):
            await domain.call_function_on(
                "() => 42",
                object_id="OBJ-1",
                execution_context_id=1,
            )

    async def test_call_function_on_mutual_exclusivity_object_and_unique(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="mutually exclusive"):
            await domain.call_function_on(
                "() => 42",
                object_id="OBJ-1",
                unique_context_id="ctx",
            )

    async def test_add_binding_mutual_exclusivity(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="mutually exclusive"):
            await domain.add_binding(
                "fn", execution_context_id=1, execution_context_name="ctx",
            )


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

    async def test_set_cache_disabled(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cache_disabled(True)
        method, params = fake.last_call
        assert params is not None
        assert params["cacheDisabled"] is True

    async def test_set_cookies(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        cookies: list[dict[str, Any]] = [{"name": "a", "value": "1"}]
        await domain.set_cookies(cookies)
        assert fake.last_call == ("Network.setCookies", {"cookies": cookies})

    async def test_emulate_network_conditions_by_rule(self) -> None:
        fake = FakeSender({"ruleIds": ["r1"]})
        domain = NetworkDomain(fake)
        conditions: list[dict[str, Any]] = [
            {"urlPattern": "*", "offline": True, "latency": 100,
             "downloadThroughput": 1000, "uploadThroughput": 500},
        ]
        await domain.emulate_network_conditions_by_rule(conditions)
        method, params = fake.last_call
        assert method == "Network.emulateNetworkConditionsByRule"
        assert params is not None
        assert params["matchedNetworkConditions"] == conditions
        assert params["emulateOfflineServiceWorker"] is False

    async def test_override_network_state(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.override_network_state(
            offline=True, latency=200, download_throughput=500,
            upload_throughput=250, connection_type="cellular3g",
        )
        method, params = fake.last_call
        assert method == "Network.overrideNetworkState"
        assert params is not None
        assert params["offline"] is True
        assert params["latency"] == 200
        assert params["downloadThroughput"] == 500
        assert params["uploadThroughput"] == 250
        assert params["connectionType"] == "cellular3g"

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
        assert fake.last_call == ("Network.getSecurityIsolationStatus", {})

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
        assert fake.last_call == ("Network.setAttachDebugStack", {"enabled": True})

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
        await domain.fetch_schemeful_site("https://example.com")
        assert fake.last_call == ("Network.fetchSchemefulSite", {"origin": "https://example.com"})

    async def test_set_cookie_controls(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cookie_controls(
            enable_third_party_cookie_restriction=True,
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
        key: dict[str, Any] = {"site": "https://example.com", "id": "s1"}
        await domain.delete_device_bound_session(key)
        assert fake.last_call == ("Network.deleteDeviceBoundSession", {"key": key})

    async def test_configure_durable_messages(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.configure_durable_messages(
            max_total_buffer_size=1024, max_resource_buffer_size=512,
        )
        method, params = fake.last_call
        assert method == "Network.configureDurableMessages"
        assert params is not None
        assert params["maxTotalBufferSize"] == 1024
        assert params["maxResourceBufferSize"] == 512

    async def test_configure_durable_messages_empty(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.configure_durable_messages()
        assert fake.last_call == ("Network.configureDurableMessages", {})

    async def test_enable_with_direct_socket_and_durable(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.enable(
            report_direct_socket_traffic=True,
            enable_durable_messages=True,
        )
        method, params = fake.last_call
        assert method == "Network.enable"
        assert params is not None
        assert params["reportDirectSocketTraffic"] is True
        assert params["enableDurableMessages"] is True

    async def test_set_user_agent_override_with_metadata(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        metadata = {"brands": [{"brand": "Chromium", "version": "120"}]}
        await domain.set_user_agent_override(
            "UA/1.0", user_agent_metadata=metadata,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["userAgentMetadata"] == metadata

    async def test_set_cookie_with_priority_and_source(self) -> None:
        fake = FakeSender({"success": True})
        domain = NetworkDomain(fake)
        partition = {"topLevelSite": "https://example.com"}
        await domain.set_cookie(
            "name", "val",
            priority="High",
            source_scheme="Secure",
            source_port=443,
            partition_key=partition,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["priority"] == "High"
        assert params["sourceScheme"] == "Secure"
        assert params["sourcePort"] == 443
        assert params["partitionKey"] == partition

    async def test_delete_cookies_with_partition_key(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        partition = {"topLevelSite": "https://example.com"}
        await domain.delete_cookies("name", partition_key=partition)
        method, params = fake.last_call
        assert params is not None
        assert params["partitionKey"] == partition

    async def test_set_blocked_urls_with_url_patterns(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        patterns: list[dict[str, Any]] = [
            {"urlPattern": "*://evil.com/*"},
        ]
        await domain.set_blocked_urls(url_patterns=patterns)
        method, params = fake.last_call
        assert params is not None
        assert params["urlPatterns"] == patterns

    async def test_set_blocked_urls_empty(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_blocked_urls()
        assert fake.last_call == ("Network.setBlockedURLs", {})

    async def test_emulate_network_conditions_by_rule_with_offline_sw(self) -> None:
        fake = FakeSender({"ruleIds": ["r1"]})
        domain = NetworkDomain(fake)
        conditions: list[dict[str, Any]] = [
            {"urlPattern": "", "offline": True},
        ]
        await domain.emulate_network_conditions_by_rule(
            conditions, emulate_offline_service_worker=True,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["emulateOfflineServiceWorker"] is True

    async def test_override_network_state_without_connection_type(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.override_network_state(
            offline=False, latency=0, download_throughput=-1,
            upload_throughput=-1,
        )
        method, params = fake.last_call
        assert params is not None
        assert "connectionType" not in params

    async def test_configure_durable_messages_only_total(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.configure_durable_messages(max_total_buffer_size=2048)
        method, params = fake.last_call
        assert params is not None
        assert params["maxTotalBufferSize"] == 2048
        assert "maxResourceBufferSize" not in params


# ── Emulation ─────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestEmulationCoverage:
    async def test_set_device_metrics_override_with_ua_and_viewport(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2.0, mobile=True,
            screen_orientation={"type": "portraitPrimary"},
            viewport={"width": 375, "height": 667},
        )
        method, params = fake.last_call
        assert method == "Emulation.setDeviceMetricsOverride"
        assert params is not None
        assert "userAgent" not in params
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
        method, params = fake.last_call
        assert method == "Emulation.setDevicePostureOverride"
        assert params == {"posture": {"type": "folded"}}

    async def test_clear_device_posture_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_device_posture_override()
        assert fake.last_call == ("Emulation.clearDevicePostureOverride", None)

    async def test_set_display_features_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        features: list[dict[str, Any]] = [
            {"orientation": "vertical", "offset": 100, "maskLength": 10},
        ]
        await domain.set_display_features_override(features)
        method, params = fake.last_call
        assert method == "Emulation.setDisplayFeaturesOverride"
        assert params is not None
        assert params["features"] == features

    async def test_clear_display_features_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_display_features_override()
        assert fake.last_call == ("Emulation.clearDisplayFeaturesOverride", None)

    async def test_set_emulated_os_text_scale(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_os_text_scale(1.5)
        assert fake.last_call == ("Emulation.setEmulatedOSTextScale", {"scale": 1.5})

    async def test_set_emulated_os_text_scale_default_zero(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_os_text_scale()
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedOSTextScale"
        assert params == {"scale": 0.0}

    async def test_set_sensor_override_enabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_enabled(True, "accelerometer")
        assert fake.last_call == (
            "Emulation.setSensorOverrideEnabled",
            {"enabled": True, "type": "accelerometer"},
        )

    async def test_set_sensor_override_enabled_with_metadata(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_enabled(
            True, "gyroscope", metadata={"samplingFrequency": 60}
        )
        method, params = fake.last_call
        assert method == "Emulation.setSensorOverrideEnabled"
        assert params["metadata"] == {"samplingFrequency": 60}

    async def test_get_overridden_sensor_information(self) -> None:
        fake = FakeSender({"requestedSamplingFrequency": 60})
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
        await domain.set_pressure_state_override("cpu", "critical")
        method, params = fake.last_call
        assert method == "Emulation.setPressureStateOverride"
        assert params is not None
        assert params["source"] == "cpu"
        assert params["state"] == "critical"

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
        assert fake.last_call == ("Emulation.setDataSaverOverride", {"dataSaverEnabled": True})

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
        await domain.set_small_viewport_height_difference_override(50)
        method, params = fake.last_call
        assert method == "Emulation.setSmallViewportHeightDifferenceOverride"
        assert params is not None
        assert params["difference"] == 50

    async def test_get_screen_infos(self) -> None:
        fake = FakeSender({"screenInfos": []})
        domain = EmulationDomain(fake)
        await domain.get_screen_infos()
        assert fake.last_call == ("Emulation.getScreenInfos", None)

    async def test_add_screen(self) -> None:
        fake = FakeSender({"screenInfo": {"screenId": "s1"}})
        domain = EmulationDomain(fake)
        await domain.add_screen(
            0, 0, 1920, 1080, device_pixel_ratio=1.5, label="main",
        )
        method, params = fake.last_call
        assert method == "Emulation.addScreen"
        assert params is not None
        assert params["label"] == "main"

    async def test_update_screen_full(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.update_screen(
            "s1", width=800, height=600, device_pixel_ratio=2.0,
            label="updated",
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

    # --- Edge cases for zero values (previously omitted due to falsy-zero bug) ---

    async def test_set_device_metrics_scale_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 667, device_scale_factor=2.0, mobile=True, scale=0.0,
        )
        method, params = fake.last_call
        assert params["scale"] == 0.0

    async def test_set_device_metrics_screen_dims_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 667, device_scale_factor=2.0, mobile=True,
            screen_width=0, screen_height=0, position_x=0, position_y=0,
        )
        method, params = fake.last_call
        assert params["screenWidth"] == 0
        assert params["screenHeight"] == 0
        assert params["positionX"] == 0
        assert params["positionY"] == 0

    async def test_set_user_agent_override_empty_strings_omitted(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_user_agent_override(
            "UA", accept_language="", platform="",
        )
        method, params = fake.last_call
        assert "acceptLanguage" not in params
        assert "platform" not in params

    async def test_set_geolocation_zero_values_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_geolocation_override(
            latitude=0.0, longitude=0.0, accuracy=0.0,
            altitude=0.0, altitude_accuracy=0.0, heading=0.0, speed=0.0,
        )
        method, params = fake.last_call
        assert params["latitude"] == 0.0
        assert params["longitude"] == 0.0
        assert params["accuracy"] == 0.0
        assert params["altitude"] == 0.0
        assert params["altitudeAccuracy"] == 0.0
        assert params["heading"] == 0.0
        assert params["speed"] == 0.0

    async def test_set_touch_emulation_max_touch_points_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_touch_emulation_enabled(True, max_touch_points=0)
        method, params = fake.last_call
        assert params["maxTouchPoints"] == 0

    async def test_set_virtual_time_budget_zero_sent(self) -> None:
        fake = FakeSender({"virtualTimeTicksBase": 0.0})
        domain = EmulationDomain(fake)
        await domain.set_virtual_time_policy(
            "advance", budget=0.0, max_virtual_time_task_starvation_count=0,
        )
        method, params = fake.last_call
        assert params["budget"] == 0.0
        assert params["maxVirtualTimeTaskStarvationCount"] == 0

    async def test_set_emit_touch_events_empty_config_omitted(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emit_touch_events_for_mouse(True, configuration="")
        method, params = fake.last_call
        assert "configuration" not in params

    async def test_add_screen_zero_optionals_sent(self) -> None:
        fake = FakeSender({"screenInfo": {"screenId": "s1"}})
        domain = EmulationDomain(fake)
        await domain.add_screen(
            0, 0, 1920, 1080,
            device_pixel_ratio=0.0, rotation=0, color_depth=0, label="",
        )
        method, params = fake.last_call
        assert params["devicePixelRatio"] == 0.0
        assert params["rotation"] == 0
        assert params["colorDepth"] == 0
        assert params["label"] == ""

    async def test_update_screen_zero_optionals_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.update_screen(
            "s1", left=0, top=0, width=0, height=0,
            device_pixel_ratio=0.0, rotation=0, color_depth=0, label="",
        )
        method, params = fake.last_call
        assert params["left"] == 0
        assert params["top"] == 0
        assert params["width"] == 0
        assert params["height"] == 0
        assert params["devicePixelRatio"] == 0.0
        assert params["rotation"] == 0
        assert params["colorDepth"] == 0
        assert params["label"] == ""

    async def test_set_device_metrics_no_display_feature_param(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 667, device_scale_factor=2.0, mobile=True,
        )
        method, params = fake.last_call
        assert "displayFeature" not in params

    async def test_set_device_metrics_no_device_posture_param(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 667, device_scale_factor=2.0, mobile=True,
        )
        method, params = fake.last_call
        assert "devicePosture" not in params

    async def test_set_default_background_color_alpha_is_float_0_to_1(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_default_background_color_override(r=255, g=0, b=0)
        method, params = fake.last_call
        assert params is not None
        assert params["color"]["a"] == 1.0
        assert isinstance(params["color"]["a"], float)

    async def test_set_default_background_color_alpha_custom_float(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_default_background_color_override(r=0, g=0, b=0, a=0.3)
        method, params = fake.last_call
        assert params is not None
        assert params["color"]["a"] == 0.3

    async def test_set_device_posture_override_uses_type_key(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_posture_override("folded")
        method, params = fake.last_call
        assert params == {"posture": {"type": "folded"}}
        assert "posture" not in params["posture"]

    async def test_set_safe_area_insets_override_only_sends_set_values(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(top=10, bottom=20)
        method, params = fake.last_call
        assert method == "Emulation.setSafeAreaInsetsOverride"
        assert params is not None
        assert params["insets"] == {"top": 10, "bottom": 20}
        assert "left" not in params["insets"]
        assert "right" not in params["insets"]

    async def test_set_safe_area_insets_override_with_max_values(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(
            top=10, left=5, bottom=10, right=5,
            top_max=20, left_max=10, bottom_max=20, right_max=10,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["insets"]["topMax"] == 20
        assert params["insets"]["leftMax"] == 10
        assert params["insets"]["bottomMax"] == 20
        assert params["insets"]["rightMax"] == 10

    async def test_set_safe_area_insets_override_explicit_zero(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(top=10, left=0)
        method, params = fake.last_call
        assert params is not None
        assert params["insets"]["top"] == 10
        assert params["insets"]["left"] == 0

    async def test_set_virtual_time_policy_zero_initial_virtual_time_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_virtual_time_policy(
            "pause",
            budget=500,
            initial_virtual_time=0.0,
        )
        method, params = fake.last_call
        assert method == "Emulation.setVirtualTimePolicy"
        assert params is not None
        assert params["initialVirtualTime"] == 0.0
        assert params["budget"] == 500

    async def test_set_emulated_media_empty_features_omitted(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_media("print", features=[])
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedMedia"
        assert params is not None
        assert params["media"] == "print"
        assert "features" not in params

    async def test_set_emulated_media_none_features_omitted(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_media("print")
        method, params = fake.last_call
        assert params is not None
        assert "features" not in params

    async def test_set_device_metrics_override_empty_scrollbar_type_omitted(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 812, mobile=True, scrollbar_type="",
        )
        method, params = fake.last_call
        assert params is not None
        assert "scrollbarType" not in params

    async def test_set_device_metrics_override_scrollbar_type_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 812, mobile=True, scrollbar_type="overlay",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["scrollbarType"] == "overlay"

    async def test_set_default_background_color_alpha_zero(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_default_background_color_override(r=255, g=0, b=0, a=0.0)
        method, params = fake.last_call
        assert params is not None
        assert params["color"]["a"] == 0.0

    async def test_set_geolocation_override_all_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_geolocation_override(
            latitude=0.0, longitude=0.0, accuracy=0.0,
        )
        method, params = fake.last_call
        assert method == "Emulation.setGeolocationOverride"
        assert params["latitude"] == 0.0
        assert params["longitude"] == 0.0
        assert params["accuracy"] == 0.0

    async def test_set_device_metrics_override_all_optional_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 812, mobile=True,
            scale=0.0, screen_width=0, screen_height=0,
            position_x=0, position_y=0,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["scale"] == 0.0
        assert params["screenWidth"] == 0
        assert params["screenHeight"] == 0
        assert params["positionX"] == 0
        assert params["positionY"] == 0

    async def test_set_virtual_time_policy_all_optional_omitted(self) -> None:
        fake = FakeSender({"virtualTimeTicksBase": 0.0})
        domain = EmulationDomain(fake)
        await domain.set_virtual_time_policy("pause")
        method, params = fake.last_call
        assert method == "Emulation.setVirtualTimePolicy"
        assert params == {"policy": "pause"}

    async def test_set_touch_emulation_max_touch_points_zero_sent_verbose(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_touch_emulation_enabled(True, max_touch_points=0)
        method, params = fake.last_call
        assert params is not None
        assert params["maxTouchPoints"] == 0

    async def test_set_safe_area_insets_zero_values_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(
            top=0, left=0, bottom=0, right=0,
            top_max=0, left_max=0, bottom_max=0, right_max=0,
        )
        method, params = fake.last_call
        assert method == "Emulation.setSafeAreaInsetsOverride"
        assert params["insets"] == {
            "top": 0, "left": 0, "bottom": 0, "right": 0,
            "topMax": 0, "leftMax": 0, "bottomMax": 0, "rightMax": 0,
        }

    async def test_set_safe_area_insets_nonzero_sent(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_safe_area_insets_override(
            top=44, bottom=34, top_max=88,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["insets"]["top"] == 44
        assert params["insets"]["bottom"] == 34
        assert params["insets"]["topMax"] == 88
        assert "left" not in params["insets"]
        assert "right" not in params["insets"]
        assert "leftMax" not in params["insets"]
        assert "bottomMax" not in params["insets"]
        assert "rightMax" not in params["insets"]

    async def test_set_sensor_override_readings_xyz_format(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_readings(
            "accelerometer", {"xyz": {"x": 1.0, "y": 0.0, "z": 9.8}},
        )
        method, params = fake.last_call
        assert method == "Emulation.setSensorOverrideReadings"
        assert params == {
            "type": "accelerometer",
            "reading": {"xyz": {"x": 1.0, "y": 0.0, "z": 9.8}},
        }

    async def test_set_sensor_override_readings_single_format(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_readings(
            "ambient-light", {"single": {"value": 100.0}},
        )
        method, params = fake.last_call
        assert params == {
            "type": "ambient-light",
            "reading": {"single": {"value": 100.0}},
        }

    async def test_set_sensor_override_readings_quaternion_format(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_sensor_override_readings(
            "absolute-orientation",
            {"quaternion": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}},
        )
        method, params = fake.last_call
        assert params == {
            "type": "absolute-orientation",
            "reading": {"quaternion": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}},
        }


# ── DOM ───────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestDOMCoverage:
    async def test_resolve_node_with_execution_context_id(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(
            node_id=1, execution_context_id=3, object_group="group1"
        )
        method, params = fake.last_call
        assert method == "DOM.resolveNode"
        assert params is not None
        assert params["nodeId"] == 1
        assert params["executionContextId"] == 3
        assert params["objectGroup"] == "group1"

    async def test_resolve_node_no_id_raises(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        with pytest.raises(ValueError, match="Either node_id or backend_node_id"):
            await domain.resolve_node()

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
        await domain.get_content_quads(node_id=1)
        assert fake.last_call == ("DOM.getContentQuads", {"nodeId": 1})

    async def test_set_file_input_files(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_file_input_files(["/tmp/a.txt"], node_id=1)
        assert fake.last_call == (
            "DOM.setFileInputFiles",
            {"files": ["/tmp/a.txt"], "nodeId": 1},
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
        assert fake.last_call == ("Overlay.hideHighlight", None)

    async def test_highlight_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        cfg = {"showInfo": True, "contentColor": {"r": 255, "g": 0, "b": 0, "a": 1}}
        await domain.highlight_node(cfg, node_id=1)
        _, params = fake.last_call
        assert params["highlightConfig"] == cfg
        assert params["nodeId"] == 1

    async def test_highlight_rect(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.highlight_rect(0, 0, 100, 100)
        method, params = fake.last_call
        assert method == "Overlay.highlightRect"
        assert params == {"x": 0, "y": 0, "width": 100, "height": 100}

    async def test_highlight_rect_with_colors(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        red = {"r": 255, "g": 0, "b": 0, "a": 0.5}
        blue = {"r": 0, "g": 0, "b": 255, "a": 1}
        await domain.highlight_rect(0, 0, 100, 100, color=red, outline_color=blue)
        method, params = fake.last_call
        assert method == "Overlay.highlightRect"
        assert params["color"] == red
        assert params["outlineColor"] == blue

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
        await domain.get_nodes_for_subtree_by_style(
            1, [{"name": "color", "value": "red"}], pierce=True
        )
        method, params = fake.last_call
        assert method == "DOM.getNodesForSubtreeByStyle"
        assert params is not None
        assert params["computedStyles"] == [{"name": "color", "value": "red"}]
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
            {"nodeId": 1, "relation": "controlledby"},
        )

    async def test_set_node_stack_traces_enabled(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_node_stack_traces_enabled(True)
        assert fake.last_call == ("DOM.setNodeStackTracesEnabled", {"enable": True})

    async def test_get_node_stack_traces(self) -> None:
        fake = FakeSender({"creation": {}})
        domain = DOMDomain(fake)
        await domain.get_node_stack_traces(1)
        assert fake.last_call == ("DOM.getNodeStackTraces", {"nodeId": 1})

    async def test_get_file_info(self) -> None:
        fake = FakeSender({"path": "/tmp/a.txt"})
        domain = DOMDomain(fake)
        await domain.get_file_info("OBJ-1")
        assert fake.last_call == ("DOM.getFileInfo", {"objectId": "OBJ-1"})

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

    async def test_get_anchor_element_with_specifier(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_anchor_element(1, anchor_specifier="a1")
        method, params = fake.last_call
        assert method == "DOM.getAnchorElement"
        assert params is not None
        assert params["anchorSpecifier"] == "a1"

    async def test_force_show_popover(self) -> None:
        fake = FakeSender({"nodeIds": []})
        domain = DOMDomain(fake)
        await domain.force_show_popover(1, enable=True)
        assert fake.last_call == (
            "DOM.forceShowPopover",
            {"nodeId": 1, "enable": True},
        )

    async def test_force_show_popover_with_invoker(self) -> None:
        fake = FakeSender({"nodeIds": []})
        domain = DOMDomain(fake)
        await domain.force_show_popover(1, enable=False, invoker_node_id=2)
        method, params = fake.last_call
        assert params is not None
        assert params["enable"] is False
        assert params["invokerNodeId"] == 2


# ── Storage ───────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestStorageCoverage:
    async def test_get_storage_key_with_frame(self) -> None:
        fake = FakeSender({"storageKey": "key1"})
        domain = StorageDomain(fake)
        await domain.get_storage_key("F1")
        assert fake.last_call == ("Storage.getStorageKey", {"frameId": "F1"})

    async def test_get_storage_key_without_frame(self) -> None:
        fake = FakeSender({"storageKey": "key1"})
        domain = StorageDomain(fake)
        await domain.get_storage_key()
        assert fake.last_call == ("Storage.getStorageKey", {})

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
        await domain.override_quota_for_origin("https://example.com", quota_size=1024.0)
        method, params = fake.last_call
        assert method == "Storage.overrideQuotaForOrigin"
        assert params is not None
        assert params["quotaSize"] == 1024.0

    async def test_override_quota_for_origin_without_size(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.override_quota_for_origin("https://example.com")
        method, params = fake.last_call
        assert method == "Storage.overrideQuotaForOrigin"
        assert params == {"origin": "https://example.com"}

    async def test_override_quota_for_origin_zero_size_sent(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.override_quota_for_origin("https://example.com", quota_size=0.0)
        method, params = fake.last_call
        assert params == {"origin": "https://example.com", "quotaSize": 0.0}

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

    async def test_reset_shared_storage_budget(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.reset_shared_storage_budget("https://owner.com")
        assert fake.last_call == (
            "Storage.resetSharedStorageBudget",
            {"ownerOrigin": "https://owner.com"},
        )

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

    async def test_delete_storage_bucket_with_name(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.delete_storage_bucket("key1", "bucket1")
        method, params = fake.last_call
        assert method == "Storage.deleteStorageBucket"
        assert params == {"bucket": {"storageKey": "key1", "name": "bucket1"}}

    async def test_delete_storage_bucket_without_name(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.delete_storage_bucket("key1")
        method, params = fake.last_call
        assert method == "Storage.deleteStorageBucket"
        assert params == {"bucket": {"storageKey": "key1"}}

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
            "https://owner.com", "group1", ["hash1", "hash2"],
        )
        method, params = fake.last_call
        assert method == "Storage.setProtectedAudienceKAnonymity"
        assert params == {
            "owner": "https://owner.com",
            "name": "group1",
            "hashes": ["hash1", "hash2"],
        }

    async def test_get_cookies_with_context(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = StorageDomain(fake)
        await domain.get_cookies(browser_context_id="ctx1")
        assert fake.last_call == (
            "Storage.getCookies",
            {"browserContextId": "ctx1"},
        )

    async def test_get_cookies_without_context(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = StorageDomain(fake)
        await domain.get_cookies()
        assert fake.last_call == ("Storage.getCookies", {})

    async def test_get_cookies_empty_context_omitted(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = StorageDomain(fake)
        await domain.get_cookies(browser_context_id="")
        assert fake.last_call == ("Storage.getCookies", {})

    async def test_set_cookies_with_context(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_cookies([{"name": "a"}], browser_context_id="ctx1")
        method, params = fake.last_call
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_set_cookies_empty_context_omitted(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_cookies([{"name": "a"}], browser_context_id="")
        method, params = fake.last_call
        assert params is not None
        assert "browserContextId" not in params

    async def test_clear_cookies_with_context(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_cookies(browser_context_id="ctx1")
        assert fake.last_call == (
            "Storage.clearCookies",
            {"browserContextId": "ctx1"},
        )

    async def test_clear_cookies_empty_context_omitted(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_cookies(browser_context_id="")
        assert fake.last_call == ("Storage.clearCookies", {})

    async def test_clear_trust_tokens(self) -> None:
        fake = FakeSender({"didDeleteTokens": True})
        domain = StorageDomain(fake)
        await domain.clear_trust_tokens("https://issuer.com")
        assert fake.last_call == (
            "Storage.clearTrustTokens",
            {"issuerOrigin": "https://issuer.com"},
        )

    async def test_get_storage_key_for_frame(self) -> None:
        fake = FakeSender({"storageKey": "key1"})
        domain = StorageDomain(fake)
        await domain.get_storage_key_for_frame("F1")
        assert fake.last_call == (
            "Storage.getStorageKeyForFrame",
            {"frameId": "F1"},
        )

    async def test_get_usage_and_quota(self) -> None:
        fake = FakeSender({"usage": 100.0, "quota": 1000.0, "overrideActive": False})
        domain = StorageDomain(fake)
        await domain.get_usage_and_quota("https://example.com")
        assert fake.last_call == (
            "Storage.getUsageAndQuota",
            {"origin": "https://example.com"},
        )

    async def test_run_bounce_tracking_mitigations_return(self) -> None:
        fake = FakeSender({"deletedSites": ["https://tracker1.com"]})
        domain = StorageDomain(fake)
        result = await domain.run_bounce_tracking_mitigations()
        assert fake.last_call == ("Storage.runBounceTrackingMitigations", None)
        assert result["deletedSites"] == ["https://tracker1.com"]

    async def test_track_indexed_db_for_origin(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.track_indexed_db_for_origin("https://example.com")
        assert fake.last_call == (
            "Storage.trackIndexedDBForOrigin",
            {"origin": "https://example.com"},
        )

    async def test_untrack_indexed_db_for_origin(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.untrack_indexed_db_for_origin("https://example.com")
        assert fake.last_call == (
            "Storage.untrackIndexedDBForOrigin",
            {"origin": "https://example.com"},
        )

    async def test_track_cache_storage_for_origin(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.track_cache_storage_for_origin("https://example.com")
        assert fake.last_call == (
            "Storage.trackCacheStorageForOrigin",
            {"origin": "https://example.com"},
        )

    async def test_untrack_cache_storage_for_origin(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.untrack_cache_storage_for_origin("https://example.com")
        assert fake.last_call == (
            "Storage.untrackCacheStorageForOrigin",
            {"origin": "https://example.com"},
        )

    async def test_set_interest_group_tracking_false(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_interest_group_tracking(False)
        assert fake.last_call == (
            "Storage.setInterestGroupTracking",
            {"enable": False},
        )

    async def test_set_interest_group_auction_tracking_false(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_interest_group_auction_tracking(False)
        assert fake.last_call == (
            "Storage.setInterestGroupAuctionTracking",
            {"enable": False},
        )

    async def test_set_shared_storage_tracking_false(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_shared_storage_tracking(False)
        assert fake.last_call == (
            "Storage.setSharedStorageTracking",
            {"enable": False},
        )

    async def test_set_storage_bucket_tracking_false(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_storage_bucket_tracking("key1", False)
        method, params = fake.last_call
        assert method == "Storage.setStorageBucketTracking"
        assert params == {"storageKey": "key1", "enable": False}

    async def test_set_shared_storage_entry_default_ignore(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_shared_storage_entry("https://owner.com", "k", "v")
        method, params = fake.last_call
        assert method == "Storage.setSharedStorageEntry"
        assert params == {
            "ownerOrigin": "https://owner.com",
            "key": "k",
            "value": "v",
            "ignoreIfPresent": False,
        }

    async def test_get_storage_key_empty_frame_omitted(self) -> None:
        fake = FakeSender({"storageKey": "key1"})
        domain = StorageDomain(fake)
        await domain.get_storage_key("")
        assert fake.last_call == ("Storage.getStorageKey", {})

    async def test_delete_storage_bucket_empty_name_omitted(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.delete_storage_bucket("key1", "")
        method, params = fake.last_call
        assert method == "Storage.deleteStorageBucket"
        assert params == {"bucket": {"storageKey": "key1"}}

    async def test_clear_trust_tokens_return_value(self) -> None:
        fake = FakeSender({"didDeleteTokens": True})
        domain = StorageDomain(fake)
        result = await domain.clear_trust_tokens("https://issuer.com")
        assert result["didDeleteTokens"] is True

    async def test_get_usage_and_quota_return_values(self) -> None:
        fake = FakeSender({
            "usage": 500.0,
            "quota": 10000.0,
            "overrideActive": True,
            "usageBreakdown": [{"storageType": "cookies", "usage": 50.0}],
        })
        domain = StorageDomain(fake)
        result = await domain.get_usage_and_quota("https://example.com")
        assert result["usage"] == 500.0
        assert result["quota"] == 10000.0
        assert result["overrideActive"] is True
        assert len(result["usageBreakdown"]) == 1


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
        assert params["waitForDebuggerOnStart"] is True

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
        await domain.auto_attach_related("T1", wait_for_debugger_on_start=True)
        method, params = fake.last_call
        assert method == "Target.autoAttachRelated"
        assert params is not None
        assert params["targetId"] == "T1"
        assert params["waitForDebuggerOnStart"] is True
        assert "autoAttach" not in params

    async def test_set_remote_locations(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_remote_locations([{"host": "localhost", "port": "9222"}])
        method, params = fake.last_call
        assert method == "Target.setRemoteLocations"
        assert params is not None

    async def test_get_dev_tools_target(self) -> None:
        fake = FakeSender({"targetId": "dt1"})
        domain = TargetDomain(fake)
        await domain.get_dev_tools_target("T1")
        assert fake.last_call == ("Target.getDevToolsTarget", {"targetId": "T1"})

    async def test_open_dev_tools(self) -> None:
        fake = FakeSender({"targetId": "dt1"})
        domain = TargetDomain(fake)
        await domain.open_dev_tools("T1")
        assert fake.last_call == ("Target.openDevTools", {"targetId": "T1"})


# ── BluetoothEmulation ────────────────────────────────────────────────────


@pytest.mark.unit
class TestBluetoothEmulationCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable("powered-on", True)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.enable"
        assert params == {"state": "powered-on", "leSupported": True}

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.disable()
        assert fake.last_call == ("BluetoothEmulation.disable", None)

    async def test_simulate_preconnected_peripheral(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_preconnected_peripheral(
            "addr1", "name1",
            manufacturer_data=[{"company": 1, "data": "abc"}],
            known_service_uuids=["uuid1"],
        )
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulatePreconnectedPeripheral"
        assert params is not None
        assert params["address"] == "addr1"
        assert params["name"] == "name1"
        assert params["manufacturerData"] == [{"company": 1, "data": "abc"}]
        assert params["knownServiceUuids"] == ["uuid1"]

    async def test_simulate_advertisement(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_advertisement({"deviceAddress": "addr1"})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateAdvertisement"
        assert params is not None
        assert params["entry"] == {"deviceAddress": "addr1"}

    async def test_set_simulated_central_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("powered-on")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.setSimulatedCentralState"
        assert params is not None

    async def test_add_service(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_service("addr1", "service-uuid-1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addService"
        assert params is not None
        assert params["address"] == "addr1"
        assert params["serviceUuid"] == "service-uuid-1"

    async def test_remove_service(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_service("service-id-1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeService"
        assert params is not None
        assert params["serviceId"] == "service-id-1"

    async def test_add_characteristic(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_characteristic("service-id-1", "char-uuid-1", {"broadcast": True})
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addCharacteristic"
        assert params is not None
        assert params["serviceId"] == "service-id-1"
        assert params["characteristicUuid"] == "char-uuid-1"
        assert params["properties"] == {"broadcast": True}

    async def test_remove_characteristic(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_characteristic("char-id-1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeCharacteristic"
        assert params is not None
        assert params["characteristicId"] == "char-id-1"

    async def test_add_descriptor(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.add_descriptor("char-id-1", "desc-uuid-1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.addDescriptor"
        assert params is not None
        assert params["characteristicId"] == "char-id-1"
        assert params["descriptorUuid"] == "desc-uuid-1"

    async def test_remove_descriptor(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.remove_descriptor("desc-id-1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.removeDescriptor"
        assert params is not None
        assert params["descriptorId"] == "desc-id-1"

    async def test_simulate_gatt_disconnection(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_disconnection("addr1")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTDisconnection"
        assert params is not None
        assert params["address"] == "addr1"

    async def test_simulate_gatt_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_operation_response("addr1", "connection", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTOperationResponse"
        assert params is not None
        assert params["address"] == "addr1"
        assert params["type"] == "connection"
        assert params["code"] == 0

    async def test_simulate_characteristic_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response("char-id-1", "read", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateCharacteristicOperationResponse"
        assert params is not None
        assert params["characteristicId"] == "char-id-1"
        assert params["type"] == "read"
        assert params["code"] == 0
        assert "data" not in params

    async def test_simulate_characteristic_operation_response_with_data(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response(
            "char-id-1", "read", 0, data="dGVzdA==",
        )
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateCharacteristicOperationResponse"
        assert params is not None
        assert params["data"] == "dGVzdA=="

    async def test_simulate_descriptor_operation_response(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_descriptor_operation_response("desc-id-1", "read", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateDescriptorOperationResponse"
        assert params is not None
        assert params["descriptorId"] == "desc-id-1"
        assert params["type"] == "read"
        assert params["code"] == 0
        assert "data" not in params

    async def test_simulate_descriptor_operation_response_with_data(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_descriptor_operation_response(
            "desc-id-1", "read", 0, data="dGVzdA==",
        )
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateDescriptorOperationResponse"
        assert params is not None
        assert params["data"] == "dGVzdA=="

    async def test_enable_absent_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable("absent", False)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.enable"
        assert params == {"state": "absent", "leSupported": False}

    async def test_enable_powered_off_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable("powered-off", True)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.enable"
        assert params == {"state": "powered-off", "leSupported": True}

    async def test_set_simulated_central_state_absent(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("absent")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.setSimulatedCentralState"
        assert params == {"state": "absent"}

    async def test_set_simulated_central_state_powered_off(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("powered-off")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.setSimulatedCentralState"
        assert params == {"state": "powered-off"}

    async def test_set_simulated_central_state_powered_on(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("powered-on")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.setSimulatedCentralState"
        assert params == {"state": "powered-on"}

    async def test_simulate_gatt_operation_response_discovery(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_operation_response("addr1", "discovery", 0x0A)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTOperationResponse"
        assert params == {"address": "addr1", "type": "discovery", "code": 0x0A}

    async def test_simulate_characteristic_operation_response_write(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response("char-1", "write", 0)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateCharacteristicOperationResponse"
        assert params == {"characteristicId": "char-1", "type": "write", "code": 0}
        assert "data" not in params

    async def test_simulate_characteristic_operation_response_subscribe(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response(
            "char-1", "subscribe-to-notifications", 0,
        )
        method, params = fake.last_call
        assert params["type"] == "subscribe-to-notifications"

    async def test_simulate_characteristic_operation_response_unsubscribe(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response(
            "char-1", "unsubscribe-from-notifications", 0,
        )
        method, params = fake.last_call
        assert params["type"] == "unsubscribe-from-notifications"

    async def test_simulate_descriptor_operation_response_write(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_descriptor_operation_response("desc-1", "write", 0)
        method, params = fake.last_call
        assert params == {"descriptorId": "desc-1", "type": "write", "code": 0}

    async def test_add_service_returns_service_id(self) -> None:
        fake = FakeSender({"serviceId": "svc-id-123"})
        domain = BluetoothEmulationDomain(fake)
        result = await domain.add_service("addr1", "svc-uuid-1")
        assert result == {"serviceId": "svc-id-123"}

    async def test_add_characteristic_returns_characteristic_id(self) -> None:
        fake = FakeSender({"characteristicId": "char-id-456"})
        domain = BluetoothEmulationDomain(fake)
        result = await domain.add_characteristic("svc-1", "char-uuid-1", {"read": True})
        assert result == {"characteristicId": "char-id-456"}

    async def test_add_descriptor_returns_descriptor_id(self) -> None:
        fake = FakeSender({"descriptorId": "desc-id-789"})
        domain = BluetoothEmulationDomain(fake)
        result = await domain.add_descriptor("char-1", "desc-uuid-1")
        assert result == {"descriptorId": "desc-id-789"}

    async def test_add_characteristic_full_properties(self) -> None:
        fake = FakeSender({"characteristicId": "char-1"})
        domain = BluetoothEmulationDomain(fake)
        props = {
            "broadcast": True,
            "read": True,
            "writeWithoutResponse": False,
            "write": True,
            "notify": True,
            "indicate": False,
            "authenticatedSignedWrites": True,
            "extendedProperties": False,
        }
        await domain.add_characteristic("svc-1", "char-uuid-1", props)
        method, params = fake.last_call
        assert params["properties"] == props

    async def test_simulate_advertisement_full_scan_entry(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        entry = {
            "deviceAddress": "AA:BB:CC:DD:EE:FF",
            "rssi": -40,
            "scanRecord": {
                "name": "Test Device",
                "uuids": ["0000180f-0000-1000-8000-00805f9b34fb"],
                "appearance": 384,
                "txPower": 4,
                "manufacturerData": [
                    {"key": 6, "data": "dGVzdA=="},
                ],
            },
        }
        await domain.simulate_advertisement(entry)
        method, params = fake.last_call
        assert params["entry"] == entry

    async def test_simulate_preconnected_peripheral_with_manufacturer_data(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        mfr_data = [{"key": 6, "data": "dGVzdA=="}]
        await domain.simulate_preconnected_peripheral(
            "AA:BB:CC:DD:EE:FF",
            "Test Device",
            manufacturer_data=mfr_data,
            known_service_uuids=["00001800-0000-1000-8000-00805f9b34fb"],
        )
        method, params = fake.last_call
        assert params["manufacturerData"] == mfr_data
        assert params["knownServiceUuids"] == ["00001800-0000-1000-8000-00805f9b34fb"]

    async def test_simulate_preconnected_peripheral_empty_manufacturer_data(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_preconnected_peripheral(
            "addr1", "name1",
            manufacturer_data=[],
            known_service_uuids=[],
        )
        method, params = fake.last_call
        assert params["manufacturerData"] == []
        assert params["knownServiceUuids"] == []

    async def test_simulate_gatt_disconnection_address_param(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_gatt_disconnection("AA:BB:CC:DD:EE:FF")
        method, params = fake.last_call
        assert method == "BluetoothEmulation.simulateGATTDisconnection"
        assert params == {"address": "AA:BB:CC:DD:EE:FF"}

    async def test_enable_le_supported_false(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable("powered-on", False)
        method, params = fake.last_call
        assert params == {"state": "powered-on", "leSupported": False}

    async def test_simulate_characteristic_operation_response_error_code(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_characteristic_operation_response("char-1", "read", 0x05)
        method, params = fake.last_call
        assert params["code"] == 0x05

    async def test_simulate_descriptor_operation_response_error_code(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.simulate_descriptor_operation_response("desc-1", "write", 0x0A)
        method, params = fake.last_call
        assert params["code"] == 0x0A


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
        await domain.report_establish_context_result("req1", 42)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportEstablishContextResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["contextId"] == 42

    async def test_report_release_context_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_release_context_result("req1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportReleaseContextResult"
        assert params is not None
        assert params["requestId"] == "req1"

    async def test_report_list_readers_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("req1", ["reader1", "reader2"])
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportListReadersResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["readers"] == ["reader1", "reader2"]

    async def test_report_get_status_change_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_get_status_change_result("req1", [{"reader": "r1"}])
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportGetStatusChangeResult"
        assert params is not None
        assert params["requestId"] == "req1"

    async def test_report_connect_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req1", 99, active_protocol="t0")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportConnectResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["handle"] == 99
        assert params["activeProtocol"] == "t0"

    async def test_report_status_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("req1", "reader1", "present", "atr123", protocol="t1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportStatusResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["readerName"] == "reader1"
        assert params["state"] == "present"
        assert params["atr"] == "atr123"
        assert params["protocol"] == "t1"

    async def test_report_data_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_data_result("req1", "data123")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportDataResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["data"] == "data123"

    async def test_report_begin_transaction_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_begin_transaction_result("req1", 77)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportBeginTransactionResult"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["handle"] == 77

    async def test_report_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error("req1", "cancelled")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportError"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["resultCode"] == "cancelled"

    async def test_report_plain_result(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_plain_result("req1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportPlainResult"
        assert params is not None
        assert params["requestId"] == "req1"


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

    def test_getattr_delegates_to_session(self) -> None:
        mock_session = MagicMock()
        mock_session.fed_cm = "fed_cm_domain"
        mock_session.schema = "schema_domain"
        mock_session.memory = "memory_domain"
        mock_session.storage = "storage_domain"
        mock_session.tracing = "tracing_domain"
        sync_session = SyncCDPSession(mock_session)
        assert sync_session.fed_cm == "fed_cm_domain"
        assert sync_session.schema == "schema_domain"
        assert sync_session.memory == "memory_domain"
        assert sync_session.storage == "storage_domain"
        assert sync_session.tracing == "tracing_domain"

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


# ── Edge cases & error behavior ────────────────────────────────────────────


@pytest.mark.unit
class TestNetworkEdgeCases:
    async def test_set_cookie_minimal(self) -> None:
        fake = FakeSender({"success": True})
        domain = NetworkDomain(fake)
        await domain.set_cookie("session", "abc123")
        method, params = fake.last_call
        assert method == "Network.setCookie"
        assert params is not None
        assert params["name"] == "session"
        assert params["value"] == "abc123"
        assert params["secure"] is False
        assert params["httpOnly"] is False
        assert "url" not in params
        assert "domain" not in params

    async def test_set_cookie_full(self) -> None:
        fake = FakeSender({"success": True})
        domain = NetworkDomain(fake)
        await domain.set_cookie(
            "token", "xyz",
            url="https://example.com",
            domain="example.com",
            path="/",
            secure=True,
            http_only=True,
            same_site="Strict",
            expires=1234567890.0,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["secure"] is True
        assert params["httpOnly"] is True
        assert params["sameSite"] == "Strict"
        assert params["expires"] == 1234567890.0

    async def test_get_cookies_with_urls(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = NetworkDomain(fake)
        await domain.get_cookies(["https://a.com", "https://b.com"])
        method, params = fake.last_call
        assert method == "Network.getCookies"
        assert params is not None
        assert params["urls"] == ["https://a.com", "https://b.com"]

    async def test_get_cookies_no_urls(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = NetworkDomain(fake)
        await domain.get_cookies()
        assert fake.last_call == ("Network.getCookies", {})

    async def test_delete_cookies_minimal(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.delete_cookies("session")
        method, params = fake.last_call
        assert method == "Network.deleteCookies"
        assert params is not None
        assert params["name"] == "session"
        assert "url" not in params
        assert "domain" not in params


@pytest.mark.unit
class TestEmulationEdgeCases:
    async def test_set_device_metrics_minimal(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(375, 667)
        method, params = fake.last_call
        assert method == "Emulation.setDeviceMetricsOverride"
        assert params is not None
        assert params["width"] == 375
        assert params["height"] == 667
        assert params["deviceScaleFactor"] == 1.0
        assert params["mobile"] is False
        assert "screenWidth" not in params
        assert "userAgent" not in params

    async def test_set_device_metrics_with_orientation(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375, 667, mobile=True,
            screen_orientation={"type": "portraitPrimary", "angle": 0},
        )
        method, params = fake.last_call
        assert params is not None
        assert params["mobile"] is True
        assert params["screenOrientation"] == {"type": "portraitPrimary", "angle": 0}

    async def test_set_user_agent_override_minimal(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_user_agent_override("Mozilla/5.0")
        method, params = fake.last_call
        assert method == "Emulation.setUserAgentOverride"
        assert params is not None
        assert params["userAgent"] == "Mozilla/5.0"
        assert "acceptLanguage" not in params
        assert "platform" not in params

    async def test_set_user_agent_override_full(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_user_agent_override(
            "Mozilla/5.0", accept_language="en-US", platform="Windows",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["acceptLanguage"] == "en-US"
        assert params["platform"] == "Windows"


@pytest.mark.unit
class TestDOMEdgeCasesCoverage:
    async def test_set_attribute_value(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attribute_value(42, "class", "highlight")
        assert fake.last_call == (
            "DOM.setAttributeValue",
            {"nodeId": 42, "name": "class", "value": "highlight"},
        )

    async def test_get_outer_html(self) -> None:
        fake = FakeSender({"outerHTML": "<div>hi</div>"})
        domain = DOMDomain(fake)
        await domain.get_outer_html(node_id=42)
        assert fake.last_call == ("DOM.getOuterHTML", {"nodeId": 42})

    async def test_remove_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.remove_node(42)
        assert fake.last_call == ("DOM.removeNode", {"nodeId": 42})

    async def test_request_node(self) -> None:
        fake = FakeSender({"nodeId": 42})
        domain = DOMDomain(fake)
        await domain.request_node("OBJ-42")
        assert fake.last_call == ("DOM.requestNode", {"objectId": "OBJ-42"})

    async def test_describe_node(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(42)
        method, params = fake.last_call
        assert method == "DOM.describeNode"
        assert params is not None
        assert params["nodeId"] == 42
        assert params["depth"] == -1
        assert "pierce" not in params


@pytest.mark.unit
class TestPageEdgeCasesCoverage:
    async def test_navigate_with_frame_id(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate("https://example.com", frame_id="F-0")
        method, params = fake.last_call
        assert params is not None
        assert params["frameId"] == "F-0"

    async def test_navigate_with_referrer_policy(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate("https://example.com", referrer_policy="noReferrer")
        method, params = fake.last_call
        assert params is not None
        assert params["referrerPolicy"] == "noReferrer"

    async def test_capture_screenshot_from_surface_false(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(from_surface=False)
        method, params = fake.last_call
        assert params is not None
        assert params["fromSurface"] is False

    async def test_capture_screenshot_capture_beyond_viewport(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(capture_beyond_viewport=True)
        method, params = fake.last_call
        assert params is not None
        assert params["captureBeyondViewport"] is True

    async def test_start_screencast_quality_zero(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.start_screencast(quality=0)
        method, params = fake.last_call
        assert params is not None
        assert params["quality"] == 0

    async def test_set_download_behavior_deny(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_download_behavior("deny")
        method, params = fake.last_call
        assert params is not None
        assert params["behavior"] == "deny"
        assert "downloadPath" not in params
        assert "eventsEnabled" not in params


# ── DOM Edge Cases ────────────────────────────────────────────────────────


@pytest.mark.unit
class TestDOMEdgeCases:
    async def test_describe_node_no_identifier(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node()
        method, params = fake.last_call
        assert method == "DOM.describeNode"
        assert params is not None
        assert "nodeId" not in params
        assert "backendNodeId" not in params
        assert "objectId" not in params
        assert params["depth"] == -1
        assert "pierce" not in params

    async def test_describe_node_with_pierce_false_no_pierce_key(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(node_id=1, pierce=False)
        _, params = fake.last_call
        assert "pierce" not in params

    async def test_describe_node_with_pierce_true_sends_pierce(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(node_id=1, pierce=True)
        _, params = fake.last_call
        assert params["pierce"] is True

    async def test_get_outer_html_with_backend_node_id(self) -> None:
        fake = FakeSender({"outerHTML": "<div>"})
        domain = DOMDomain(fake)
        await domain.get_outer_html(backend_node_id=10)
        assert fake.last_call == (
            "DOM.getOuterHTML",
            {"backendNodeId": 10},
        )

    async def test_get_outer_html_with_object_id(self) -> None:
        fake = FakeSender({"outerHTML": "<div>"})
        domain = DOMDomain(fake)
        await domain.get_outer_html(object_id="OBJ-1")
        assert fake.last_call == (
            "DOM.getOuterHTML",
            {"objectId": "OBJ-1"},
        )

    async def test_get_outer_html_with_include_shadow_dom(self) -> None:
        fake = FakeSender({"outerHTML": "<div>"})
        domain = DOMDomain(fake)
        await domain.get_outer_html(node_id=1, include_shadow_dom=True)
        _, params = fake.last_call
        assert params["includeShadowDOM"] is True

    async def test_get_outer_html_no_identifier(self) -> None:
        fake = FakeSender({"outerHTML": ""})
        domain = DOMDomain(fake)
        await domain.get_outer_html()
        method, params = fake.last_call
        assert method == "DOM.getOuterHTML"
        assert params == {}

    async def test_focus_with_backend_node_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.focus(backend_node_id=10)
        assert fake.last_call == ("DOM.focus", {"backendNodeId": 10})

    async def test_focus_with_object_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.focus(object_id="OBJ-1")
        assert fake.last_call == ("DOM.focus", {"objectId": "OBJ-1"})

    async def test_focus_no_identifier(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.focus()
        method, params = fake.last_call
        assert method == "DOM.focus"
        assert params == {}

    async def test_get_box_model_with_backend_node_id(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(backend_node_id=10)
        assert fake.last_call == ("DOM.getBoxModel", {"backendNodeId": 10})

    async def test_get_box_model_with_object_id(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(object_id="OBJ-1")
        assert fake.last_call == ("DOM.getBoxModel", {"objectId": "OBJ-1"})

    async def test_get_content_quads_with_backend_node_id(self) -> None:
        fake = FakeSender({"quads": []})
        domain = DOMDomain(fake)
        await domain.get_content_quads(backend_node_id=10)
        assert fake.last_call == ("DOM.getContentQuads", {"backendNodeId": 10})

    async def test_get_content_quads_with_object_id(self) -> None:
        fake = FakeSender({"quads": []})
        domain = DOMDomain(fake)
        await domain.get_content_quads(object_id="OBJ-1")
        assert fake.last_call == ("DOM.getContentQuads", {"objectId": "OBJ-1"})

    async def test_scroll_into_view_with_rect(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        rect = {"x": 0, "y": 0, "width": 100, "height": 100}
        await domain.scroll_into_view_if_needed(node_id=1, rect=rect)
        _, params = fake.last_call
        assert params["rect"] == rect

    async def test_scroll_into_view_with_backend_node_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.scroll_into_view_if_needed(backend_node_id=10)
        assert fake.last_call == (
            "DOM.scrollIntoViewIfNeeded",
            {"backendNodeId": 10},
        )

    async def test_set_file_input_files_with_backend_node_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_file_input_files(["/a.txt"], backend_node_id=10)
        assert fake.last_call == (
            "DOM.setFileInputFiles",
            {"files": ["/a.txt"], "backendNodeId": 10},
        )

    async def test_set_file_input_files_with_object_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_file_input_files(["/a.txt"], object_id="OBJ-1")
        assert fake.last_call == (
            "DOM.setFileInputFiles",
            {"files": ["/a.txt"], "objectId": "OBJ-1"},
        )

    async def test_get_attribute_with_name_found(self) -> None:
        fake = FakeSender(
            {"attributes": ["class", "hero", "id", "main"]}
        )
        domain = DOMDomain(fake)
        result = await domain.get_attribute(1, "class")
        assert result == {"value": "hero"}

    async def test_get_attribute_with_name_not_found(self) -> None:
        fake = FakeSender(
            {"attributes": ["class", "hero", "id", "main"]}
        )
        domain = DOMDomain(fake)
        result = await domain.get_attribute(1, "data-missing")
        assert result == {"value": None}

    async def test_get_attribute_without_name_returns_all(self) -> None:
        fake = FakeSender(
            {"attributes": ["class", "hero", "id", "main"]}
        )
        domain = DOMDomain(fake)
        result = await domain.get_attribute(1)
        assert "attributes" in result
        assert result["attributes"] == ["class", "hero", "id", "main"]

    async def test_set_attributes_as_text_with_name(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attributes_as_text(1, "class='foo'", name="old")
        _, params = fake.last_call
        assert params["name"] == "old"

    async def test_resolve_node_with_backend_node_id_only(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(backend_node_id=10)
        assert fake.last_call == (
            "DOM.resolveNode",
            {"backendNodeId": 10},
        )

    async def test_resolve_node_with_execution_context_id(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(node_id=1, execution_context_id=7)
        _, params = fake.last_call
        assert params["executionContextId"] == 7

    async def test_enable_with_include_whitespace_none(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.enable(include_whitespace="none")
        _, params = fake.last_call
        assert params["includeWhitespace"] == "none"

    async def test_enable_with_include_whitespace_all(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.enable(include_whitespace="all")
        _, params = fake.last_call
        assert params["includeWhitespace"] == "all"

    async def test_enable_without_include_whitespace(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert "includeWhitespace" not in params

    async def test_get_node_for_location_with_ignore_pointer_events(self) -> None:
        fake = FakeSender({"backendNodeId": 1, "frameId": "F1"})
        domain = DOMDomain(fake)
        await domain.get_node_for_location(10, 20, ignore_pointer_events_none=True)
        _, params = fake.last_call
        assert params["ignorePointerEventsNone"] is True

    async def test_get_node_for_location_without_optional_flags(self) -> None:
        fake = FakeSender({"backendNodeId": 1, "frameId": "F1"})
        domain = DOMDomain(fake)
        await domain.get_node_for_location(10, 20)
        _, params = fake.last_call
        assert "includeUserAgentShadowDOM" not in params
        assert "ignorePointerEventsNone" not in params

    async def test_get_nodes_for_subtree_by_style_no_pierce(self) -> None:
        fake = FakeSender({"nodeIds": [1]})
        domain = DOMDomain(fake)
        await domain.get_nodes_for_subtree_by_style(
            1, [{"name": "color", "value": "red"}]
        )
        _, params = fake.last_call
        assert "pierce" not in params

    async def test_get_container_for_node_all_optionals(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_container_for_node(
            1,
            container_name="my-container",
            physical_axes="Both",
            logical_axes="Inline",
            queries_scroll_state=True,
            queries_anchored=True,
        )
        _, params = fake.last_call
        assert params["containerName"] == "my-container"
        assert params["physicalAxes"] == "Both"
        assert params["logicalAxes"] == "Inline"
        assert params["queriesScrollState"] is True
        assert params["queriesAnchored"] is True

    async def test_get_container_for_node_no_optionals(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_container_for_node(1)
        assert fake.last_call == ("DOM.getContainerForNode", {"nodeId": 1})

    async def test_force_show_popover_enable_false(self) -> None:
        fake = FakeSender({"nodeIds": []})
        domain = DOMDomain(fake)
        await domain.force_show_popover(1, enable=False)
        assert fake.last_call == (
            "DOM.forceShowPopover",
            {"nodeId": 1, "enable": False},
        )

    async def test_get_anchor_element_without_specifier(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_anchor_element(1)
        assert fake.last_call == (
            "DOM.getAnchorElement",
            {"nodeId": 1},
        )

    async def test_get_document_invalid_depth_raises(self) -> None:
        fake = FakeSender({"root": {}})
        domain = DOMDomain(fake)
        with pytest.raises(ValueError, match="depth must be >= -1"):
            await domain.get_document(depth=-2)

    async def test_request_child_nodes_no_pierce(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.request_child_nodes(1, depth=2)
        _, params = fake.last_call
        assert params["depth"] == 2
        assert "pierce" not in params

    async def test_perform_search_with_shadow_dom(self) -> None:
        fake = FakeSender({"searchId": "s1", "resultCount": 1})
        domain = DOMDomain(fake)
        await domain.perform_search("//div", include_user_agent_shadow_dom=True)
        _, params = fake.last_call
        assert params["includeUserAgentShadowDOM"] is True

    async def test_perform_search_without_shadow_dom(self) -> None:
        fake = FakeSender({"searchId": "s1", "resultCount": 1})
        domain = DOMDomain(fake)
        await domain.perform_search("//div")
        _, params = fake.last_call
        assert "includeUserAgentShadowDOM" not in params

    async def test_copy_to_with_insert_before(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.copy_to(1, 2, insert_before_node_id=3)
        assert fake.last_call == (
            "DOM.copyTo",
            {"nodeId": 1, "targetNodeId": 2, "insertBeforeNodeId": 3},
        )

    async def test_move_to_with_insert_before(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.move_to(1, 2, insert_before_node_id=3)
        assert fake.last_call == (
            "DOM.moveTo",
            {"nodeId": 1, "targetNodeId": 2, "insertBeforeNodeId": 3},
        )

    async def test_set_node_name(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.set_node_name(1, "span")
        assert fake.last_call == (
            "DOM.setNodeName",
            {"nodeId": 1, "name": "span"},
        )

    async def test_get_frame_owner(self) -> None:
        fake = FakeSender({"backendNodeId": 10, "nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_frame_owner("F1")
        assert fake.last_call == ("DOM.getFrameOwner", {"frameId": "F1"})

    async def test_set_inspected_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_inspected_node(1)
        assert fake.last_call == ("DOM.setInspectedNode", {"nodeId": 1})

    async def test_set_node_stack_traces_enabled_false(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_node_stack_traces_enabled(False)
        assert fake.last_call == (
            "DOM.setNodeStackTracesEnabled",
            {"enable": False},
        )

    async def test_get_element_by_relation_all_enums(self) -> None:
        for relation in ("PopoverTarget", "InterestTarget", "CommandFor"):
            fake = FakeSender({"nodeId": 5})
            domain = DOMDomain(fake)
            await domain.get_element_by_relation(1, relation)
            method, params = fake.last_call
            assert method == "DOM.getElementByRelation"
            assert params["relation"] == relation


# ── DOMStorage ─────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestDOMStorageCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        await domain.enable()
        assert fake.last_call == ("DOMStorage.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        await domain.disable()
        assert fake.last_call == ("DOMStorage.disable", None)

    async def test_get_dom_storage_items(self) -> None:
        fake = FakeSender({"entries": [["k1", "v1"], ["k2", "v2"]]})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        result = await domain.get_dom_storage_items(storage_id)
        method, params = fake.last_call
        assert method == "DOMStorage.getDOMStorageItems"
        assert params is not None
        assert params["storageId"] == storage_id
        assert result["entries"] == [["k1", "v1"], ["k2", "v2"]]

    async def test_get_dom_storage_items_with_storage_key(self) -> None:
        fake = FakeSender({"entries": []})
        domain = DOMStorageDomain(fake)
        storage_id = {
            "securityOrigin": "https://example.com",
            "storageKey": "key123",
            "isLocalStorage": False,
        }
        await domain.get_dom_storage_items(storage_id)
        method, params = fake.last_call
        assert method == "DOMStorage.getDOMStorageItems"
        assert params is not None
        assert params["storageId"]["storageKey"] == "key123"
        assert params["storageId"]["isLocalStorage"] is False

    async def test_set_dom_storage_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.set_dom_storage_item(storage_id, "key1", "val1")
        method, params = fake.last_call
        assert method == "DOMStorage.setDOMStorageItem"
        assert params is not None
        assert params["storageId"] == storage_id
        assert params["key"] == "key1"
        assert params["value"] == "val1"

    async def test_remove_dom_storage_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.remove_dom_storage_item(storage_id, "key1")
        method, params = fake.last_call
        assert method == "DOMStorage.removeDOMStorageItem"
        assert params is not None
        assert params["storageId"] == storage_id
        assert params["key"] == "key1"

    async def test_clear(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.clear(storage_id)
        method, params = fake.last_call
        assert method == "DOMStorage.clear"
        assert params is not None
        assert params["storageId"] == storage_id

    async def test_clear_dom_storage_items_alias(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": False}
        await domain.clear_dom_storage_items(storage_id)
        method, params = fake.last_call
        assert method == "DOMStorage.clear"
        assert params is not None
        assert params["storageId"] == storage_id

    async def test_get_dom_storage_items_return_entries(self) -> None:
        fake = FakeSender({"entries": [["a", "1"], ["b", "2"]]})
        domain = DOMStorageDomain(fake)
        result = await domain.get_dom_storage_items(
            {"securityOrigin": "https://example.com", "isLocalStorage": True}
        )
        assert isinstance(result["entries"], list)
        assert all(isinstance(item, list) for item in result["entries"])
        assert len(result["entries"][0]) == 2

    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "DOMStorage.enable"
        assert params is None

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "DOMStorage.disable"
        assert params is None

    async def test_set_dom_storage_item_empty_value(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.set_dom_storage_item(storage_id, "key1", "")
        method, params = fake.last_call
        assert params is not None
        assert params["value"] == ""

    async def test_storage_id_is_local_storage_false(self) -> None:
        fake = FakeSender({"entries": []})
        domain = DOMStorageDomain(fake)
        storage_id = {"securityOrigin": "https://example.com", "isLocalStorage": False}
        await domain.get_dom_storage_items(storage_id)
        method, params = fake.last_call
        assert params is not None
        assert params["storageId"]["isLocalStorage"] is False
