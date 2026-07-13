"""Unit tests for P2 features: completed domain gaps and new 0% domains."""

import pytest

from cdpwave.domains.ads import AdsDomain
from cdpwave.domains.bluetooth_emulation import BluetoothEmulationDomain
from cdpwave.domains.crash_report_context import CrashReportContextDomain
from cdpwave.domains.css import CSSDomain
from cdpwave.domains.digital_credentials import DigitalCredentialsDomain
from cdpwave.domains.dom_debugger import DOMDebuggerDomain
from cdpwave.domains.dom_snapshot import DOMSnapshotDomain
from cdpwave.domains.extensions import ExtensionsDomain
from cdpwave.domains.fed_cm import FedCmDomain
from cdpwave.domains.file_system import FileSystemDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
from cdpwave.domains.inspector import InspectorDomain
from cdpwave.domains.memory import MemoryDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.performance_timeline import PerformanceTimelineDomain
from cdpwave.domains.pwa import PWADomain
from cdpwave.domains.smart_card_emulation import SmartCardEmulationDomain
from cdpwave.domains.web_mcp import WebMCPDomain
from tests.unit.fake_sender import FakeSender


class TestCSSNewCommands:
    async def test_collect_class_names(self) -> None:
        fake = FakeSender({"classNames": [".a", ".b"]})
        domain = CSSDomain(fake)
        await domain.collect_class_names("ss1")
        assert fake.last_call == ("CSS.collectClassNames", {"styleSheetId": "ss1"})

    async def test_get_environment_variables(self) -> None:
        fake = FakeSender({"envVars": []})
        domain = CSSDomain(fake)
        await domain.get_environment_variables()
        assert fake.last_call == ("CSS.getEnvironmentVariables", None)

    async def test_set_local_fonts_enabled(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.set_local_fonts_enabled(True)
        assert fake.last_call == ("CSS.setLocalFontsEnabled", {"enabled": True})

    async def test_track_computed_style_updates(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.track_computed_style_updates([{"properties": ["color"]}])
        method, params = fake.last_call
        assert method == "CSS.trackComputedStyleUpdates"
        assert params is not None
        assert params["propertiesToTrack"] == [{"properties": ["color"]}]


class TestOverlayNewCommands:
    async def test_get_highlight_object_for_test(self) -> None:
        fake = FakeSender({"highlight": {}})
        domain = OverlayDomain(fake)
        await domain.get_highlight_object_for_test(1)
        method, params = fake.last_call
        assert method == "Overlay.getHighlightObjectForTest"
        assert params is not None
        assert params["nodeId"] == 1

    async def test_set_show_ad_highlights(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_ad_highlights(True)
        assert fake.last_call == ("Overlay.setShowAdHighlights", {"show": True})

    async def test_set_show_grid_overlays(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_grid_overlays([{"nodeId": 1}])
        method, params = fake.last_call
        assert method == "Overlay.setShowGridOverlays"
        assert params is not None
        assert params["gridNodeHighlightConfigs"] == [{"nodeId": 1}]


class TestDOMDebuggerNewCommands:
    async def test_get_event_listeners(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1")
        method, params = fake.last_call
        assert method == "DOMDebugger.getEventListeners"
        assert params is not None
        assert params["objectId"] == "obj-1"

    async def test_set_instrumentation_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_instrumentation_breakpoint("setInterval")
        assert fake.last_call == (
            "DOMDebugger.setInstrumentationBreakpoint",
            {"eventName": "setInterval"},
        )

    async def test_set_break_on_csp_violation(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_break_on_csp_violation(["trustedtype-sink-violation"])
        method, params = fake.last_call
        assert method == "DOMDebugger.setBreakOnCSPViolation"
        assert params is not None
        assert params["violationTypes"] == ["trustedtype-sink-violation"]


class TestInspectorNewCommands:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Inspector.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Inspector.disable", None)


class TestPerformanceTimelineNewCommands:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable(["largest-contentful-paint"])
        method, params = fake.last_call
        assert method == "PerformanceTimeline.enable"
        assert params is not None
        assert params["eventTypes"] == ["largest-contentful-paint"]

    async def test_enable_multiple_types(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable(["largest-contentful-paint", "layout-shift"])
        method, params = fake.last_call
        assert method == "PerformanceTimeline.enable"
        assert params["eventTypes"] == ["largest-contentful-paint", "layout-shift"]

    async def test_enable_empty_list(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable([])
        method, params = fake.last_call
        assert method == "PerformanceTimeline.enable"
        assert params["eventTypes"] == []

    async def test_enable_type_error_not_list(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        with pytest.raises(TypeError, match="event_types must be a list"):
            await domain.enable("largest-contentful-paint")  # type: ignore[arg-type]

    async def test_enable_type_error_not_str_element(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        with pytest.raises(TypeError, match="event_types\\[0\\] must be a str"):
            await domain.enable([{"name": "lcp"}])  # type: ignore[list-item]


class TestDOMSnapshotNewCommands:
    async def test_get_snapshot(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color", "display"])
        method, params = fake.last_call
        assert method == "DOMSnapshot.getSnapshot"
        assert params is not None
        assert params["computedStyleWhitelist"] == ["color", "display"]


class TestIndexedDBNewCommands:
    async def test_delete_object_store_entries(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0}, security_origin="https://example.com",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteObjectStoreEntries"
        assert params is not None
        assert params["databaseName"] == "db1"

    async def test_get_metadata(self) -> None:
        fake = FakeSender({"entriesCount": 5, "keyGeneratorValue": 10})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata("db1", "store1")
        method, params = fake.last_call
        assert method == "IndexedDB.getMetadata"
        assert params is not None
        assert params["databaseName"] == "db1"


class TestMemoryNewCommands:
    async def test_forcibly_purge_javascript_memory(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.forcibly_purge_javascript_memory()
        assert fake.last_call == ("Memory.forciblyPurgeJavaScriptMemory", None)

    async def test_get_all_time_sampling_profile(self) -> None:
        fake = FakeSender({"profile": {}})
        domain = MemoryDomain(fake)
        await domain.get_all_time_sampling_profile()
        assert fake.last_call == ("Memory.getAllTimeSamplingProfile", None)

    async def test_get_dom_counters_for_leak_detection(self) -> None:
        fake = FakeSender({"counters": []})
        domain = MemoryDomain(fake)
        await domain.get_dom_counters_for_leak_detection()
        assert fake.last_call == ("Memory.getDOMCountersForLeakDetection", None)


class TestExtensionsNewCommands:
    async def test_get_extensions(self) -> None:
        fake = FakeSender({"extensions": []})
        domain = ExtensionsDomain(fake)
        await domain.get_extensions()
        assert fake.last_call == ("Extensions.getExtensions", None)

    async def test_set_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.set_storage_items("ext1", "local", {"key": "val"})
        method, params = fake.last_call
        assert method == "Extensions.setStorageItems"
        assert params is not None
        assert params["values"] == {"key": "val"}

    async def test_trigger_action(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.trigger_action("ext1", "target1")
        assert fake.last_call == (
            "Extensions.triggerAction",
            {"id": "ext1", "targetId": "target1"},
        )

    async def test_uninstall(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.uninstall("ext1")
        assert fake.last_call == ("Extensions.uninstall", {"id": "ext1"})


class TestPWANewCommands:
    async def test_launch(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("manifest1")
        method, params = fake.last_call
        assert method == "PWA.launch"
        assert params is not None
        assert params["manifestId"] == "manifest1"

    async def test_launch_files_in_app(self) -> None:
        fake = FakeSender({"targetIds": ["T1"]})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("manifest1", ["/file1.txt"])
        method, params = fake.last_call
        assert method == "PWA.launchFilesInApp"
        assert params is not None
        assert params["files"] == ["/file1.txt"]

    async def test_open_current_page_in_app(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.open_current_page_in_app("manifest1")
        assert fake.last_call == (
            "PWA.openCurrentPageInApp",
            {"manifestId": "manifest1"},
        )

    async def test_change_app_user_settings(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", link_capturing=True)
        method, params = fake.last_call
        assert method == "PWA.changeAppUserSettings"
        assert params is not None
        assert params["linkCapturing"] is True


class TestFedCmDomain:
    async def test_enable_default(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "FedCm.enable"
        assert params == {"disableRejectionDelay": False}

    async def test_enable_disable_rejection_delay(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable(disable_rejection_delay=True)
        method, params = fake.last_call
        assert method == "FedCm.enable"
        assert params == {"disableRejectionDelay": True}

    async def test_enable_type_error(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="disable_rejection_delay"):
            await domain.enable(disable_rejection_delay="yes")

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.disable()
        assert fake.last_call == ("FedCm.disable", None)

    async def test_select_account(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.select_account("d1", 0)
        assert fake.last_call == (
            "FedCm.selectAccount",
            {"dialogId": "d1", "accountIndex": 0},
        )

    async def test_select_account_type_error_dialog_id(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.select_account(123, 0)

    async def test_select_account_type_error_account_index(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.select_account("d1", "zero")

    async def test_select_account_bool_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.select_account("d1", True)

    async def test_click_dialog_button(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.click_dialog_button("d1", "ErrorGotIt")
        assert fake.last_call == (
            "FedCm.clickDialogButton",
            {"dialogId": "d1", "dialogButton": "ErrorGotIt"},
        )

    async def test_click_dialog_button_type_error_dialog_id(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.click_dialog_button(123, "ErrorGotIt")

    async def test_click_dialog_button_type_error_button(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_button"):
            await domain.click_dialog_button("d1", 123)

    async def test_open_url(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.open_url("d1", 2, "TermsOfService")
        assert fake.last_call == (
            "FedCm.openUrl",
            {
                "dialogId": "d1",
                "accountIndex": 2,
                "accountUrlType": "TermsOfService",
            },
        )

    async def test_open_url_type_error_dialog_id(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.open_url(123, 0, "TermsOfService")

    async def test_open_url_type_error_account_index(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.open_url("d1", "zero", "TermsOfService")

    async def test_open_url_type_error_account_url_type(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_url_type"):
            await domain.open_url("d1", 0, 123)

    async def test_open_url_bool_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.open_url("d1", True, "TermsOfService")

    async def test_dismiss_dialog_default(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.dismiss_dialog("d1")
        assert fake.last_call == (
            "FedCm.dismissDialog",
            {"dialogId": "d1", "triggerCooldown": False},
        )

    async def test_dismiss_dialog_trigger_cooldown(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.dismiss_dialog("d1", trigger_cooldown=True)
        assert fake.last_call == (
            "FedCm.dismissDialog",
            {"dialogId": "d1", "triggerCooldown": True},
        )

    async def test_dismiss_dialog_type_error_dialog_id(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.dismiss_dialog(123)

    async def test_dismiss_dialog_type_error_trigger_cooldown(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="trigger_cooldown"):
            await domain.dismiss_dialog("d1", trigger_cooldown="yes")

    async def test_reset_cooldown(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.reset_cooldown()
        assert fake.last_call == ("FedCm.resetCooldown", None)

    # ── edge cases ──

    async def test_enable_empty_params_not_none(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is not None
        assert "disableRejectionDelay" in params

    async def test_select_account_negative_index(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.select_account("d1", -1)
        method, params = fake.last_call
        assert method == "FedCm.selectAccount"
        assert params["accountIndex"] == -1

    async def test_select_account_large_index(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.select_account("d1", 999999)
        method, params = fake.last_call
        assert params["accountIndex"] == 999999

    async def test_click_dialog_button_all_values(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        for button in (
            "ConfirmIdpLoginContinue",
            "ErrorGotIt",
            "ErrorMoreDetails",
        ):
            await domain.click_dialog_button("d1", button)
            _, params = fake.last_call
            assert params["dialogButton"] == button

    async def test_open_url_terms_of_service(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.open_url("d1", 0, "TermsOfService")
        _, params = fake.last_call
        assert params["accountUrlType"] == "TermsOfService"

    async def test_open_url_privacy_policy(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.open_url("d1", 1, "PrivacyPolicy")
        _, params = fake.last_call
        assert params["accountUrlType"] == "PrivacyPolicy"

    async def test_dismiss_dialog_empty_string_dialog_id(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.dismiss_dialog("")
        _, params = fake.last_call
        assert params["dialogId"] == ""

    async def test_enable_returns_response_dict(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = FedCmDomain(fake)
        result = await domain.enable()
        assert result == {"result": "ok"}

    async def test_disable_returns_response_dict(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = FedCmDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}

    async def test_reset_cooldown_returns_response_dict(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = FedCmDomain(fake)
        result = await domain.reset_cooldown()
        assert result == {"result": "ok"}

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable()
        await domain.select_account("d1", 0)
        await domain.reset_cooldown()
        assert len(fake.calls) == 3
        assert fake.calls[0][0] == "FedCm.enable"
        assert fake.calls[1][0] == "FedCm.selectAccount"
        assert fake.calls[2][0] == "FedCm.resetCooldown"

    async def test_enable_none_param_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="disable_rejection_delay"):
            await domain.enable(disable_rejection_delay=None)  # type: ignore[arg-type]

    async def test_select_account_none_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.select_account(None, 0)  # type: ignore[arg-type]

    async def test_select_account_none_account_index_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.select_account("d1", None)  # type: ignore[arg-type]

    async def test_click_dialog_button_none_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.click_dialog_button(None, "ErrorGotIt")  # type: ignore[arg-type]

    async def test_click_dialog_button_none_button_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_button"):
            await domain.click_dialog_button("d1", None)  # type: ignore[arg-type]

    async def test_open_url_none_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.open_url(None, 0, "TermsOfService")  # type: ignore[arg-type]

    async def test_open_url_none_account_url_type_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_url_type"):
            await domain.open_url("d1", 0, None)  # type: ignore[arg-type]

    async def test_dismiss_dialog_none_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.dismiss_dialog(None)  # type: ignore[arg-type]

    async def test_dismiss_dialog_none_trigger_cooldown_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="trigger_cooldown"):
            await domain.dismiss_dialog("d1", trigger_cooldown=None)  # type: ignore[arg-type]

    async def test_dismiss_dialog_int_trigger_cooldown_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="trigger_cooldown"):
            await domain.dismiss_dialog("d1", trigger_cooldown=1)  # type: ignore[arg-type]

    async def test_enable_int_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="disable_rejection_delay"):
            await domain.enable(disable_rejection_delay=1)  # type: ignore[arg-type]

    async def test_select_account_float_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.select_account("d1", 1.5)  # type: ignore[arg-type]

    async def test_open_url_float_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_index"):
            await domain.open_url("d1", 1.5, "TermsOfService")  # type: ignore[arg-type]

    async def test_select_account_list_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.select_account(["d1"], 0)  # type: ignore[arg-type]

    async def test_click_dialog_button_dict_button_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_button"):
            await domain.click_dialog_button("d1", {"button": "ErrorGotIt"})  # type: ignore[arg-type]

    async def test_open_url_int_account_url_type_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="account_url_type"):
            await domain.open_url("d1", 0, 123)  # type: ignore[arg-type]

    async def test_dismiss_dialog_list_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.dismiss_dialog(["d1"])  # type: ignore[arg-type]

    async def test_dismiss_dialog_dict_dialog_id_rejected(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        with pytest.raises(TypeError, match="dialog_id"):
            await domain.dismiss_dialog({"id": "d1"})  # type: ignore[arg-type]

    async def test_full_lifecycle_sequence(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable(disable_rejection_delay=True)
        await domain.select_account("d1", 0)
        await domain.click_dialog_button("d1", "ConfirmIdpLoginContinue")
        await domain.open_url("d1", 0, "TermsOfService")
        await domain.dismiss_dialog("d1", trigger_cooldown=True)
        await domain.reset_cooldown()
        await domain.disable()
        assert len(fake.calls) == 7
        assert fake.calls[0] == (
            "FedCm.enable", {"disableRejectionDelay": True}
        )
        assert fake.calls[1] == (
            "FedCm.selectAccount", {"dialogId": "d1", "accountIndex": 0}
        )
        assert fake.calls[2] == (
            "FedCm.clickDialogButton",
            {"dialogId": "d1", "dialogButton": "ConfirmIdpLoginContinue"},
        )
        assert fake.calls[3] == (
            "FedCm.openUrl",
            {"dialogId": "d1", "accountIndex": 0, "accountUrlType": "TermsOfService"},
        )
        assert fake.calls[4] == (
            "FedCm.dismissDialog",
            {"dialogId": "d1", "triggerCooldown": True},
        )
        assert fake.calls[5] == ("FedCm.resetCooldown", None)
        assert fake.calls[6] == ("FedCm.disable", None)


class TestBluetoothEmulationDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable("powered-on", True)
        method, params = fake.last_call
        assert method == "BluetoothEmulation.enable"
        assert params == {"state": "powered-on", "leSupported": True}

    async def test_set_simulated_central_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("powered-on")
        assert fake.last_call == (
            "BluetoothEmulation.setSimulatedCentralState",
            {"state": "powered-on"},
        )


class TestSmartCardEmulationDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.enable()
        assert fake.last_call == ("SmartCardEmulation.enable", None)

    async def test_report_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error("req1", "cancelled")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportError"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["resultCode"] == "cancelled"

    # ── edge cases ──

    async def test_report_establish_bool_result_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="context_id"):
            await domain.report_establish_context_result("req1", True)  # type: ignore[arg-type]

    async def test_report_establish_int_context_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_establish_context_result(123, 0)  # type: ignore[arg-type]

    async def test_report_release_bool_result_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_release_context_result(False)  # type: ignore[arg-type]

    async def test_report_list_readers_str_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="readers"):
            await domain.report_list_readers_result("req1", "not_a_list")  # type: ignore[arg-type]

    async def test_report_list_readers_bool_result_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_list_readers_result(True, [])  # type: ignore[arg-type]

    async def test_report_status_change_str_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="reader_states"):
            await domain.report_get_status_change_result("req1", "nope")  # type: ignore[arg-type]

    async def test_report_connect_int_reader_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_connect_result(123, 0)  # type: ignore[arg-type]

    async def test_report_connect_bool_protocol_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="handle"):
            await domain.report_connect_result("req1", True)  # type: ignore[arg-type]

    async def test_report_status_bool_card_state_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="state"):
            await domain.report_status_result("req1", "r1", True, "atr")  # type: ignore[arg-type]

    async def test_report_data_int_response_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="data"):
            await domain.report_data_result("req1", 123)  # type: ignore[arg-type]

    async def test_report_begin_bool_result_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="handle"):
            await domain.report_begin_transaction_result("req1", True)  # type: ignore[arg-type]

    async def test_report_error_bool_error_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="result_code"):
            await domain.report_error("req1", True)  # type: ignore[arg-type]

    async def test_report_error_int_context_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_error(123, "cancelled")  # type: ignore[arg-type]

    async def test_report_plain_bool_result_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_plain_result(True)  # type: ignore[arg-type]

    async def test_report_plain_int_context_rejected(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_plain_result(123)  # type: ignore[arg-type]


class TestWebMCPDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        assert fake.last_call == ("WebMCP.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.disable()
        assert fake.last_call == ("WebMCP.disable", None)


class TestAdsDomain:
    async def test_get_ad_metrics(self) -> None:
        fake = FakeSender({"metrics": {}})
        domain = AdsDomain(fake)
        await domain.get_ad_metrics()
        assert fake.last_call == ("Ads.getAdMetrics", None)


class TestCrashReportContextDomain:
    async def test_get_entries(self) -> None:
        fake = FakeSender({"entries": []})
        domain = CrashReportContextDomain(fake)
        await domain.get_entries()
        assert fake.last_call == ("CrashReportContext.getEntries", None)


class TestDigitalCredentialsDomain:
    async def test_set_virtual_wallet_behavior(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline")
        assert fake.last_call == (
            "DigitalCredentials.setVirtualWalletBehavior",
            {"action": "decline"},
        )


class TestFileSystemDomain:
    async def test_get_directory(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root", "subdir"],
        )
        method, params = fake.last_call
        assert method == "FileSystem.getDirectory"
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert locator["storageKey"] == "https://example.com"
        assert locator["pathComponents"] == ["root", "subdir"]
        assert "bucketName" not in locator

    async def test_get_directory_with_bucket_name(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
            bucket_name="my-bucket",
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert locator["bucketName"] == "my-bucket"

    async def test_get_directory_empty_bucket_name_omitted(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
            bucket_name="",
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert "bucketName" not in locator

    async def test_get_directory_type_error_storage_key(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match="storage_key must be a str"):
            await domain.get_directory(
                storage_key=123,  # type: ignore[arg-type]
                path_components=["root"],
            )

    async def test_get_directory_type_error_path_components(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match="path_components must be a list"):
            await domain.get_directory(
                storage_key="https://example.com",
                path_components="root",  # type: ignore[arg-type]
            )

    async def test_get_directory_type_error_path_component_element(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match=r"path_components\[1\] must be a str"):
            await domain.get_directory(
                storage_key="https://example.com",
                path_components=["root", 42],  # type: ignore[list-item]
            )

    async def test_get_directory_type_error_bucket_name(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match="bucket_name must be a str"):
            await domain.get_directory(
                storage_key="https://example.com",
                path_components=["root"],
                bucket_name=123,  # type: ignore[arg-type]
            )

    async def test_get_directory_empty_path_components(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=[],
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert locator["pathComponents"] == []

    async def test_get_directory_empty_storage_key(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="",
            path_components=["root"],
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert locator["storageKey"] == ""

    async def test_get_directory_multiple_path_components(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root", "subdir", "deep", "nested"],
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert locator["pathComponents"] == ["root", "subdir", "deep", "nested"]

    async def test_get_directory_return_value(self) -> None:
        fake = FakeSender({"directory": {"name": "root", "nestedDirectories": []}})
        domain = FileSystemDomain(fake)
        result = await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
        )
        assert "directory" in result
        assert result["directory"]["name"] == "root"

    async def test_get_directory_only_bucket_locator_key(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
            bucket_name="bucket1",
        )
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["bucketFileSystemLocator"]

    async def test_get_directory_locator_keys(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
            bucket_name="bucket1",
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert set(locator.keys()) == {"storageKey", "pathComponents", "bucketName"}

    async def test_get_directory_locator_keys_without_bucket(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        await domain.get_directory(
            storage_key="https://example.com",
            path_components=["root"],
        )
        _, params = fake.last_call
        assert params is not None
        locator = params["bucketFileSystemLocator"]
        assert set(locator.keys()) == {"storageKey", "pathComponents"}

    async def test_get_directory_bool_as_storage_key(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match="storage_key must be a str"):
            await domain.get_directory(
                storage_key=True,  # type: ignore[arg-type]
                path_components=["root"],
            )

    async def test_get_directory_none_as_path_components(self) -> None:
        fake = FakeSender({"directory": {}})
        domain = FileSystemDomain(fake)
        with pytest.raises(TypeError, match="path_components must be a list"):
            await domain.get_directory(
                storage_key="https://example.com",
                path_components=None,  # type: ignore[arg-type]
            )


# ── Edge cases & error behavior ────────────────────────────────────────────


class TestCSSEdgeCases:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.enable()
        assert fake.last_call == ("CSS.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.disable()
        assert fake.last_call == ("CSS.disable", None)

    async def test_collect_class_names(self) -> None:
        fake = FakeSender({"classNames": [".a", ".b"]})
        domain = CSSDomain(fake)
        await domain.collect_class_names("ss1")
        assert fake.last_call == (
            "CSS.collectClassNames",
            {"styleSheetId": "ss1"},
        )


class TestDOMDebuggerEdgeCases:
    async def test_set_dom_breakpoint_subtree(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(42, "subtree-modified")
        assert fake.last_call == (
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": 42, "type": "subtree-modified"},
        )

    async def test_remove_dom_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_dom_breakpoint(42, "node-removed")
        assert fake.last_call == (
            "DOMDebugger.removeDOMBreakpoint",
            {"nodeId": 42, "type": "node-removed"},
        )

    async def test_set_event_listener_breakpoint_no_target(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_event_listener_breakpoint("click")
        assert fake.last_call == (
            "DOMDebugger.setEventListenerBreakpoint",
            {"eventName": "click"},
        )

    async def test_set_event_listener_breakpoint_with_target(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_event_listener_breakpoint("click", target_name="document")
        method, params = fake.last_call
        assert params is not None
        assert params["targetName"] == "document"

    async def test_set_xhr_breakpoint_empty_url(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_xhr_breakpoint("")
        assert fake.last_call == (
            "DOMDebugger.setXHRBreakpoint",
            {"url": ""},
        )

    async def test_remove_xhr_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_xhr_breakpoint("api/users")
        assert fake.last_call == (
            "DOMDebugger.removeXHRBreakpoint",
            {"url": "api/users"},
        )


class TestOverlayEdgeCases:
    async def test_set_show_debug_borders_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_debug_borders(True)
        assert fake.last_call == (
            "Overlay.setShowDebugBorders",
            {"show": True},
        )

    async def test_set_show_debug_borders_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_debug_borders(False)
        assert fake.last_call == (
            "Overlay.setShowDebugBorders",
            {"show": False},
        )

    async def test_set_show_fps_counter_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_fps_counter(True)
        assert fake.last_call == (
            "Overlay.setShowFPSCounter",
            {"show": True},
        )


class TestIndexedDBEdgeCases:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        assert fake.last_call == ("IndexedDB.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        assert fake.last_call == ("IndexedDB.disable", None)


class TestInspectorEdgeCases:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Inspector.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Inspector.disable", None)
