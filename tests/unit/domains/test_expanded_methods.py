"""Unit tests for expanded domain methods.

Covers Page, Runtime, DOM, Network, Debugger, Target, Emulation,
CSS, Storage, Overlay, Fetch.
"""

import pytest

from cdpwave.domains.css import CSSDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.fetch import FetchDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.runtime import RuntimeDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.domains.target import TargetDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestPageExpanded:
    async def test_add_script_to_evaluate_on_new_document(self) -> None:
        fake = FakeSender({"identifier": "scr1"})
        domain = PageDomain(fake)
        await domain.add_script_to_evaluate_on_new_document("console.log('hi')")
        method, params = fake.last_call
        assert method == "Page.addScriptToEvaluateOnNewDocument"
        assert params is not None
        assert params["source"] == "console.log('hi')"

    async def test_remove_script_to_evaluate_on_new_document(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.remove_script_to_evaluate_on_new_document("scr1")
        assert fake.last_call == (
            "Page.removeScriptToEvaluateOnNewDocument",
            {"identifier": "scr1"},
        )

    async def test_get_frame_tree(self) -> None:
        fake = FakeSender({"frameTree": {}})
        domain = PageDomain(fake)
        await domain.get_frame_tree()
        assert fake.last_call == ("Page.getFrameTree", None)

    async def test_set_bypass_csp(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_bypass_csp(True)
        assert fake.last_call == ("Page.setBypassCSP", {"enabled": True})

    async def test_crash(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.crash()
        assert fake.last_call == ("Page.crash", None)

    async def test_close(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.close()
        assert fake.last_call == ("Page.close", None)

    async def test_bring_to_front(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.bring_to_front()
        assert fake.last_call == ("Page.bringToFront", None)

    async def test_handle_java_script_dialog(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.handle_java_script_dialog(accept=True, prompt_text="ok")
        method, params = fake.last_call
        assert method == "Page.handleJavaScriptDialog"
        assert params is not None
        assert params["accept"] is True
        assert params["promptText"] == "ok"

    async def test_create_isolated_world(self) -> None:
        fake = FakeSender({"executionContextId": 1})
        domain = PageDomain(fake)
        await domain.create_isolated_world("frame1", world_name="iso")
        method, params = fake.last_call
        assert params is not None
        assert params["frameId"] == "frame1"
        assert params["worldName"] == "iso"

    async def test_create_isolated_world_grant_universal_access(self) -> None:
        fake = FakeSender({"executionContextId": 1})
        domain = PageDomain(fake)
        await domain.create_isolated_world("frame1", grant_universal_access=True)
        method, params = fake.last_call
        assert params is not None
        assert params["frameId"] == "frame1"
        assert params["grantUniversalAccess"] is True

    async def test_set_document_content(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_document_content("frame1", "<h1>hi</h1>")
        assert fake.last_call == (
            "Page.setDocumentContent",
            {"frameId": "frame1", "html": "<h1>hi</h1>"},
        )

    async def test_capture_snapshot(self) -> None:
        fake = FakeSender({"data": "mhtml..."})
        domain = PageDomain(fake)
        await domain.capture_snapshot()
        assert fake.last_call == ("Page.captureSnapshot", {"format": "mhtml"})

    async def test_get_resource_tree(self) -> None:
        fake = FakeSender({"frameTree": {}})
        domain = PageDomain(fake)
        await domain.get_resource_tree()
        assert fake.last_call == ("Page.getResourceTree", None)

    async def test_get_resource_content(self) -> None:
        fake = FakeSender({"content": "abc", "base64Encoded": False})
        domain = PageDomain(fake)
        await domain.get_resource_content("frame1", "https://example.com/x.js")
        assert fake.last_call == (
            "Page.getResourceContent",
            {"frameId": "frame1", "url": "https://example.com/x.js"},
        )

    async def test_reset_navigation_history(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reset_navigation_history()
        assert fake.last_call == ("Page.resetNavigationHistory", None)

    async def test_navigate_to_history_entry(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.navigate_to_history_entry(3)
        assert fake.last_call == (
            "Page.navigateToHistoryEntry",
            {"entryId": 3},
        )

    async def test_set_web_lifecycle_state(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_web_lifecycle_state("frozen")
        assert fake.last_call == (
            "Page.setWebLifecycleState",
            {"state": "frozen"},
        )

    async def test_set_web_lifecycle_state_invalid(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="state must be"):
            await domain.set_web_lifecycle_state("invalid")

    async def test_set_intercept_file_chooser_dialog(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.set_intercept_file_chooser_dialog(True)
        assert fake.last_call == (
            "Page.setInterceptFileChooserDialog",
            {"enabled": True},
        )

    async def test_get_app_manifest(self) -> None:
        fake = FakeSender({"url": "", "data": "", "errors": [], "parsed": {}})
        domain = PageDomain(fake)
        await domain.get_app_manifest()
        assert fake.last_call == ("Page.getAppManifest", None)


@pytest.mark.unit
class TestRuntimeExpanded:
    async def test_add_binding(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.add_binding("myCallback")
        assert fake.last_call == ("Runtime.addBinding", {"name": "myCallback"})

    async def test_remove_binding(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.remove_binding("myCallback")
        assert fake.last_call == ("Runtime.removeBinding", {"name": "myCallback"})

    async def test_compile_script(self) -> None:
        fake = FakeSender({"scriptId": "s1"})
        domain = RuntimeDomain(fake)
        await domain.compile_script("1+1", persist_script=True)
        method, params = fake.last_call
        assert method == "Runtime.compileScript"
        assert params is not None
        assert params["persistScript"] is True

    async def test_run_script(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("s1")
        method, params = fake.last_call
        assert method == "Runtime.runScript"
        assert params is not None
        assert params["scriptId"] == "s1"

    async def test_query_objects(self) -> None:
        fake = FakeSender({"objects": {}})
        domain = RuntimeDomain(fake)
        await domain.query_objects("proto1")
        assert fake.last_call == (
            "Runtime.queryObjects",
            {"prototypeObjectId": "proto1"},
        )

    async def test_get_heap_usage(self) -> None:
        fake = FakeSender({"usedSize": 100, "totalSize": 200})
        domain = RuntimeDomain(fake)
        await domain.get_heap_usage()
        assert fake.last_call == ("Runtime.getHeapUsage", None)

    async def test_set_async_call_stack_depth(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.set_async_call_stack_depth(32)
        assert fake.last_call == (
            "Runtime.setAsyncCallStackDepth",
            {"maxDepth": 32},
        )

    async def test_set_async_call_stack_depth_negative(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="depth must be"):
            await domain.set_async_call_stack_depth(-1)

    async def test_terminate_execution(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.terminate_execution()
        assert fake.last_call == ("Runtime.terminateExecution", None)

    async def test_await_promise(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.await_promise("p1", return_by_value=True)
        assert fake.last_call == (
            "Runtime.awaitPromise",
            {"promiseObjectId": "p1", "returnByValue": True},
        )

    async def test_global_lexical_scope_names(self) -> None:
        fake = FakeSender({"names": ["x", "y"]})
        domain = RuntimeDomain(fake)
        await domain.global_lexical_scope_names()
        assert fake.last_call == ("Runtime.globalLexicalScopeNames", None)

    async def test_get_exception_details(self) -> None:
        fake = FakeSender({"exceptionDetails": {}})
        domain = RuntimeDomain(fake)
        await domain.get_exception_details("err1")
        assert fake.last_call == (
            "Runtime.getExceptionDetails",
            {"errorObjectId": "err1"},
        )

    async def test_discard_console_entries(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.discard_console_entries()
        assert fake.last_call == ("Runtime.discardConsoleEntries", None)


@pytest.mark.unit
class TestDOMExpanded:
    async def test_remove_attribute(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.remove_attribute(1, "class")
        assert fake.last_call == (
            "DOM.removeAttribute",
            {"nodeId": 1, "name": "class"},
        )

    async def test_describe_node(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(node_id=1)
        method, params = fake.last_call
        assert method == "DOM.describeNode"
        assert params is not None
        assert params["nodeId"] == 1

    async def test_get_box_model(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(node_id=1)
        method, params = fake.last_call
        assert method == "DOM.getBoxModel"
        assert params is not None
        assert params["nodeId"] == 1

    async def test_get_node_for_location(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_node_for_location(10, 20)
        assert fake.last_call == (
            "DOM.getNodeForLocation",
            {"x": 10, "y": 20},
        )

    async def test_resolve_node(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(node_id=1, object_group="grp")
        method, params = fake.last_call
        assert method == "DOM.resolveNode"
        assert params is not None
        assert params["objectGroup"] == "grp"

    async def test_request_node(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.request_node(1)
        assert fake.last_call == ("DOM.requestNode", {"nodeId": 1})

    async def test_perform_search(self) -> None:
        fake = FakeSender({"searchId": "s1", "resultCount": 3})
        domain = DOMDomain(fake)
        await domain.perform_search("//div")
        assert fake.last_call == (
            "DOM.performSearch",
            {"query": "//div"},
        )

    async def test_get_search_results(self) -> None:
        fake = FakeSender({"nodeIds": [1, 2, 3]})
        domain = DOMDomain(fake)
        await domain.get_search_results("s1", 0, 3)
        assert fake.last_call == (
            "DOM.getSearchResults",
            {"searchId": "s1", "fromIndex": 0, "toIndex": 3},
        )

    async def test_discard_search_results(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.discard_search_results("s1")
        assert fake.last_call == (
            "DOM.discardSearchResults",
            {"searchId": "s1"},
        )

    async def test_set_node_value(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_node_value(1, "new value")
        assert fake.last_call == (
            "DOM.setNodeValue",
            {"nodeId": 1, "value": "new value"},
        )

    async def test_copy_to(self) -> None:
        fake = FakeSender({"nodeId": 2})
        domain = DOMDomain(fake)
        await domain.copy_to(1, 2)
        assert fake.last_call == (
            "DOM.copyTo",
            {"nodeId": 1, "targetNodeId": 2},
        )

    async def test_move_to(self) -> None:
        fake = FakeSender({"nodeId": 2})
        domain = DOMDomain(fake)
        await domain.move_to(1, 2)
        assert fake.last_call == (
            "DOM.moveTo",
            {"nodeId": 1, "targetNodeId": 2},
        )


@pytest.mark.unit
class TestNetworkExpanded:
    async def test_get_all_cookies(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = NetworkDomain(fake)
        await domain.get_all_cookies()
        assert fake.last_call == ("Network.getAllCookies", None)

    async def test_set_blocked_urls(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_blocked_urls(["*://evil.com/*"])
        assert fake.last_call == (
            "Network.setBlockedURLs",
            {"urls": ["*://evil.com/*"]},
        )

    async def test_set_bypass_service_worker(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_bypass_service_worker(True)
        assert fake.last_call == (
            "Network.setBypassServiceWorker",
            {"bypass": True},
        )

    async def test_get_request_post_data(self) -> None:
        fake = FakeSender({"postData": "abc=1"})
        domain = NetworkDomain(fake)
        await domain.get_request_post_data("req1")
        assert fake.last_call == (
            "Network.getRequestPostData",
            {"requestId": "req1"},
        )


@pytest.mark.unit
class TestDebuggerExpanded:
    async def test_set_breakpoints_active(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoints_active(False)
        assert fake.last_call == (
            "Debugger.setBreakpointsActive",
            {"active": False},
        )

    async def test_search_in_content(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "TODO")
        method, params = fake.last_call
        assert method == "Debugger.searchInContent"
        assert params is not None
        assert params["scriptId"] == "s1"
        assert params["query"] == "TODO"

    async def test_set_blackbox_patterns(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns(["node_modules/.*"])
        assert fake.last_call == (
            "Debugger.setBlackboxPatterns",
            {"patterns": ["node_modules/.*"]},
        )

    async def test_set_return_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_return_value({"value": 42})
        assert fake.last_call == (
            "Debugger.setReturnValue",
            {"newValue": {"value": 42}},
        )


@pytest.mark.unit
class TestTargetExpanded:
    async def test_activate_target(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.activate_target("t1")
        assert fake.last_call == (
            "Target.activateTarget",
            {"targetId": "t1"},
        )

    async def test_get_target_info(self) -> None:
        fake = FakeSender({"targetInfo": {}})
        domain = TargetDomain(fake)
        await domain.get_target_info("t1")
        assert fake.last_call == (
            "Target.getTargetInfo",
            {"targetId": "t1"},
        )

    async def test_set_discover_targets(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_discover_targets(True)
        assert fake.last_call == (
            "Target.setDiscoverTargets",
            {"discover": True},
        )

    async def test_create_browser_context(self) -> None:
        fake = FakeSender({"browserContextId": "ctx1"})
        domain = TargetDomain(fake)
        await domain.create_browser_context()
        assert fake.last_call == (
            "Target.createBrowserContext",
            {"disposeOnDetach": False},
        )

    async def test_dispose_browser_context(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.dispose_browser_context("ctx1")
        assert fake.last_call == (
            "Target.disposeBrowserContext",
            {"browserContextId": "ctx1"},
        )


@pytest.mark.unit
class TestEmulationExpanded:
    async def test_set_scrollbars_hidden(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_scrollbars_hidden(True)
        assert fake.last_call == (
            "Emulation.setScrollbarsHidden",
            {"hidden": True},
        )

    async def test_set_javascript_disabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_javascript_disabled(True)
        assert fake.last_call == (
            "Emulation.setJavaScriptDisabled",
            {"disabled": True},
        )

    async def test_set_auto_dark_mode_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_auto_dark_mode_override(True)
        assert fake.last_call == (
            "Emulation.setAutoDarkModeOverride",
            {"enabled": True},
        )


@pytest.mark.unit
class TestCSSExpanded:
    async def test_add_rule(self) -> None:
        fake = FakeSender({"rule": {}})
        domain = CSSDomain(fake)
        await domain.add_rule("ss1", ".cls { color: red; }")
        assert fake.last_call == (
            "CSS.addRule",
            {"styleSheetId": "ss1", "ruleText": ".cls { color: red; }"},
        )

    async def test_create_style_sheet(self) -> None:
        fake = FakeSender({"styleSheetId": "ss2"})
        domain = CSSDomain(fake)
        await domain.create_style_sheet("frame1")
        assert fake.last_call == (
            "CSS.createStyleSheet",
            {"frameId": "frame1"},
        )

    async def test_force_pseudo_state(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.force_pseudo_state(1, ["hover"])
        assert fake.last_call == (
            "CSS.forcePseudoState",
            {"nodeId": 1, "forcedPseudoClasses": ["hover"]},
        )


@pytest.mark.unit
class TestStorageExpanded:
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


@pytest.mark.unit
class TestOverlayExpanded:
    async def test_set_paused_in_debugger_message(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_paused_in_debugger_message("Paused!")
        assert fake.last_call == (
            "Overlay.setPausedInDebuggerMessage",
            {"message": "Paused!"},
        )

    async def test_set_show_viewport_size_on_resize(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_viewport_size_on_resize(True)
        assert fake.last_call == (
            "Overlay.setShowViewportSizeOnResize",
            {"show": True},
        )


@pytest.mark.unit
class TestFetchExpanded:
    async def test_get_request_post_data(self) -> None:
        fake = FakeSender({"postData": "abc=1"})
        domain = FetchDomain(fake)
        await domain.get_request_post_data("req1")
        assert fake.last_call == (
            "Fetch.getRequestPostData",
            {"requestId": "req1"},
        )
