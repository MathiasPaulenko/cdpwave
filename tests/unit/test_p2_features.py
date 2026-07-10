"""Unit tests for P2 features: completed domain gaps and new 0% domains."""


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
from cdpwave.domains.layer_tree import LayerTreeDomain
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
        await domain.enable([{"name": "largest-contentful-paint"}])
        method, params = fake.last_call
        assert method == "PerformanceTimeline.enable"
        assert params is not None
        assert params["eventTypes"] == [{"name": "largest-contentful-paint"}]


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


class TestLayerTreeNewCommands:
    async def test_make_snapshot(self) -> None:
        fake = FakeSender({"snapshotId": "S1"})
        domain = LayerTreeDomain(fake)
        await domain.make_snapshot("L1")
        assert fake.last_call == ("LayerTree.makeSnapshot", {"layerId": "L1"})

    async def test_replay_snapshot(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("S1")
        method, params = fake.last_call
        assert method == "LayerTree.replaySnapshot"
        assert params is not None
        assert params["snapshotId"] == "S1"

    async def test_snapshot_command_log(self) -> None:
        fake = FakeSender({"commandLog": []})
        domain = LayerTreeDomain(fake)
        await domain.snapshot_command_log("S1")
        assert fake.last_call == (
            "LayerTree.snapshotCommandLog",
            {"snapshotId": "S1"},
        )


class TestFedCmDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.enable()
        assert fake.last_call == ("FedCm.enable", None)

    async def test_select_account(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.select_account("d1", 0)
        assert fake.last_call == (
            "FedCm.selectAccount",
            {"dialogId": "d1", "accountIndex": 0},
        )

    async def test_reset_cooldown(self) -> None:
        fake = FakeSender({})
        domain = FedCmDomain(fake)
        await domain.reset_cooldown()
        assert fake.last_call == ("FedCm.resetCooldown", None)


class TestBluetoothEmulationDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.enable()
        assert fake.last_call == ("BluetoothEmulation.enable", None)

    async def test_set_simulated_central_state(self) -> None:
        fake = FakeSender({})
        domain = BluetoothEmulationDomain(fake)
        await domain.set_simulated_central_state("powered")
        assert fake.last_call == (
            "BluetoothEmulation.setSimulatedCentralState",
            {"state": "powered"},
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
        await domain.report_error(context_id="ctx1", error=42)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportError"
        assert params is not None
        assert params["contextId"] == "ctx1"


class TestWebMCPDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        assert fake.last_call == ("WebMCP.enable", None)

    async def test_invoke_tool(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.invoke_tool("search", {"query": "test"})
        method, params = fake.last_call
        assert method == "WebMCP.invokeTool"
        assert params is not None
        assert params["toolName"] == "search"

    async def test_cancel_invocation(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.cancel_invocation("inv1")
        assert fake.last_call == ("WebMCP.cancelInvocation", {"invocationId": "inv1"})


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
        await domain.set_virtual_wallet_behavior("default")
        assert fake.last_call == (
            "DigitalCredentials.setVirtualWalletBehavior",
            {"behavior": "default"},
        )


class TestFileSystemDomain:
    async def test_get_directory(self) -> None:
        fake = FakeSender({"directory": {}, "token": "tok"})
        domain = FileSystemDomain(fake)
        await domain.get_directory()
        assert fake.last_call == ("FileSystem.getDirectory", None)
