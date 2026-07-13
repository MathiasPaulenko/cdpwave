"""Unit tests to close coverage gaps for domains below 90%."""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cdpwave.browser.discovery import _http_get, _http_put
from cdpwave.browser.finder import (
    _check_paths,
    _find_on_linux,
    find_brave,
    find_browser,
    find_chrome,
    find_chromium,
    find_edge,
)
from cdpwave.domains.accessibility import AccessibilityDomain
from cdpwave.domains.autofill import AutofillDomain
from cdpwave.domains.browser import BrowserDomain
from cdpwave.domains.cache_storage import CacheStorageDomain
from cdpwave.domains.css import CSSDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.domains.dom_storage import DOMStorageDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.fetch import FetchDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
from cdpwave.domains.input import InputDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.domains.web_audio import WebAudioDomain
from cdpwave.exceptions import BrowserNotFoundError
from tests.unit.fake_sender import FakeSender

_CONNECT = "cdpwave.client.Connection"


@pytest.mark.unit
class TestAutofillCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Autofill.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Autofill.disable", None)

    async def test_trigger_fill_with_frame_and_card(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        card = {"number": "4111111111111111", "name": "Test"}
        await domain.trigger_fill(42, frame_id="F1", card=card)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params is not None
        assert params["fieldId"] == 42
        assert params["frameId"] == "F1"
        assert params["card"] == card

    async def test_trigger_fill_minimal(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.trigger_fill(10)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params == {"fieldId": 10}

    async def test_trigger_with_address(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        address = {"fields": [{"name": "GIVEN_NAME", "value": "Jon"}]}
        await domain.trigger(20, address=address)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params is not None
        assert params["fieldId"] == 20
        assert params["address"] == address

    async def test_trigger_fill_after_save_with_frame(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.trigger_fill_after_save(5, frame_id="F2")
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params is not None
        assert params["fieldId"] == 5
        assert params["frameId"] == "F2"

    async def test_trigger_fill_after_save_minimal(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.trigger_fill_after_save(7)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params == {"fieldId": 7}

    async def test_set_addresses(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        addresses = [
            {"fields": [{"name": "NAME_FULL", "value": "Jon Doe"}]},
            {"fields": [{"name": "NAME_FULL", "value": "Jane Doe"}]},
        ]
        await domain.set_addresses(addresses)
        method, params = fake.last_call
        assert method == "Autofill.setAddresses"
        assert params is not None
        assert params["addresses"] == addresses

    async def test_trigger_direct_with_all_params(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        card = {"number": "4111111111111111", "name": "Test"}
        await domain.trigger(30, frame_id="F3", card=card)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params is not None
        assert params["fieldId"] == 30
        assert params["frameId"] == "F3"
        assert params["card"] == card

    async def test_trigger_no_optional_params(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.trigger(15)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params == {"fieldId": 15}

    async def test_trigger_fill_after_save_no_frame(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.trigger_fill_after_save(3)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params == {"fieldId": 3}

    async def test_trigger_fill_alias_with_address(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        address = {"fields": [{"name": "NAME_FULL", "value": "Jon"}]}
        await domain.trigger_fill(25, address=address)
        method, params = fake.last_call
        assert method == "Autofill.trigger"
        assert params is not None
        assert params["fieldId"] == 25
        assert params["address"] == address

    async def test_set_addresses_empty(self) -> None:
        fake = FakeSender({})
        domain = AutofillDomain(fake)
        await domain.set_addresses([])
        method, params = fake.last_call
        assert method == "Autofill.setAddresses"
        assert params == {"addresses": []}


@pytest.mark.unit
class TestWebAudioCoverage:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.enable()
        assert fake.last_call == ("WebAudio.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.disable()
        assert fake.last_call == ("WebAudio.disable", None)

    async def test_get_realtime_data(self) -> None:
        fake = FakeSender({"currentValue": 0.5, "currentTime": 1.0})
        domain = WebAudioDomain(fake)
        result = await domain.get_realtime_data("ctx1")
        method, params = fake.last_call
        assert method == "WebAudio.getRealtimeData"
        assert params == {"contextId": "ctx1"}
        assert "currentValue" in result


@pytest.mark.unit
class TestAccessibilityCoverage:
    async def test_get_partial_ax_tree_all_params(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_partial_ax_tree(
            node_id=1,
            backend_node_id=2,
            object_id="obj3",
            fetch_relatives=False,
        )
        method, params = fake.last_call
        assert method == "Accessibility.getPartialAXTree"
        assert params is not None
        assert params["nodeId"] == 1
        assert params["backendNodeId"] == 2
        assert params["objectId"] == "obj3"
        assert params["fetchRelatives"] is False

    async def test_get_root_ax_node_with_frame(self) -> None:
        fake = FakeSender({"node": {}})
        domain = AccessibilityDomain(fake)
        await domain.get_root_ax_node(frame_id="F1")
        method, params = fake.last_call
        assert method == "Accessibility.getRootAXNode"
        assert params is not None
        assert params["frameId"] == "F1"

    async def test_get_child_ax_nodes_with_frame(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_child_ax_nodes("node1", frame_id="F2")
        method, params = fake.last_call
        assert method == "Accessibility.getChildAXNodes"
        assert params is not None
        assert params["id"] == "node1"
        assert params["frameId"] == "F2"

    async def test_query_ax_tree_all_params(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.query_ax_tree(
            node_id=1,
            backend_node_id=2,
            object_id="obj3",
            accessible_name="Submit",
            role="button",
        )
        method, params = fake.last_call
        assert method == "Accessibility.queryAXTree"
        assert params is not None
        assert params["nodeId"] == 1
        assert params["backendNodeId"] == 2
        assert params["objectId"] == "obj3"
        assert params["accessibleName"] == "Submit"
        assert params["role"] == "button"


@pytest.mark.unit
class TestIndexedDBCoverage:
    async def test_request_database_names_with_storage_key_and_bucket(self) -> None:
        fake = FakeSender({"databaseNames": ["db1"]})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_database_names(
            storage_key="sk1", storage_bucket=bucket
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabaseNames"
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_request_database_with_storage_key_and_bucket(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": []})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_database(
            storage_key="sk1",
            database_name="mydb",
            storage_bucket=bucket,
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabase"
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert params["databaseName"] == "mydb"
        assert params["storageBucket"] == bucket

    async def test_request_data_with_all_optional(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        key_range = {"lower": 0, "upper": 100}
        await domain.request_data(
            security_origin="https://example.com",
            storage_key="sk1",
            database_name="mydb",
            object_store_name="store1",
            index_name="idx1",
            key_range=key_range,
            storage_bucket=bucket,
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestData"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["indexName"] == "idx1"
        assert params["keyRange"] == key_range
        assert params["storageBucket"] == bucket

    async def test_delete_database_with_storage_key_and_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.delete_database(
            storage_key="sk1",
            database_name="mydb",
            storage_bucket=bucket,
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteDatabase"
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_clear_object_store_with_all_optional(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.clear_object_store(
            security_origin="https://example.com",
            storage_key="sk1",
            database_name="mydb",
            object_store_name="store1",
            storage_bucket=bucket,
        )
        method, params = fake.last_call
        assert method == "IndexedDB.clearObjectStore"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket


@pytest.mark.unit
class TestCacheStorageCoverage:
    async def test_request_cache_names_with_storage_key_and_bucket(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_cache_names(
            storage_key="sk1", storage_bucket=bucket
        )
        method, params = fake.last_call
        assert method == "CacheStorage.requestCacheNames"
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_request_entries_with_path_filter(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("cache1", path_filter="/api")
        method, params = fake.last_call
        assert method == "CacheStorage.requestEntries"
        assert params is not None
        assert params["pathFilter"] == "/api"


@pytest.mark.unit
class TestCSSCoverage:
    async def test_get_inline_styles_alias(self) -> None:
        fake = FakeSender({"inlineStyle": {}})
        domain = CSSDomain(fake)
        await domain.get_inline_styles(42)
        method, params = fake.last_call
        assert method == "CSS.getInlineStylesForNode"
        assert params == {"nodeId": 42}

    async def test_get_platform_fonts_for_node(self) -> None:
        fake = FakeSender({"fonts": []})
        domain = CSSDomain(fake)
        await domain.get_platform_fonts_for_node(10)
        method, params = fake.last_call
        assert method == "CSS.getPlatformFontsForNode"
        assert params == {"nodeId": 10}

    async def test_add_rule_with_location(self) -> None:
        fake = FakeSender({"rule": {}})
        domain = CSSDomain(fake)
        loc = {"startLine": 0, "startColumn": 0, "endLine": 0, "endColumn": 10}
        await domain.add_rule("ss1", ".cls { color: red; }", location=loc)
        method, params = fake.last_call
        assert method == "CSS.addRule"
        assert params is not None
        assert params["location"] == loc

    async def test_set_rule_style(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.set_rule_style("ss1", "color: green")
        method, params = fake.last_call
        assert method == "CSS.setStyleTexts"
        assert params is not None
        assert params["edits"][0]["styleSheetId"] == "ss1"
        assert params["edits"][0]["text"] == "color: green"

    async def test_start_rule_usage_tracking(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.start_rule_usage_tracking()
        assert fake.last_call == ("CSS.startRuleUsageTracking", None)

    async def test_stop_rule_usage_tracking(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.stop_rule_usage_tracking()
        assert fake.last_call == ("CSS.stopRuleUsageTracking", None)

    async def test_take_coverage_delta(self) -> None:
        fake = FakeSender({"coverage": []})
        domain = CSSDomain(fake)
        await domain.take_coverage_delta()
        assert fake.last_call == ("CSS.takeCoverageDelta", None)


@pytest.mark.unit
class TestStorageCoverage:
    async def test_get_dom_storage_items(self) -> None:
        fake = FakeSender({"entries": [["key", "val"]]})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.get_dom_storage_items(sid)
        method, params = fake.last_call
        assert method == "DOMStorage.getDOMStorageItems"
        assert params is not None
        assert params["storageId"] == sid

    async def test_set_dom_storage_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.set_dom_storage_item(sid, "key", "val")
        method, params = fake.last_call
        assert method == "DOMStorage.setDOMStorageItem"
        assert params is not None
        assert params["key"] == "key"
        assert params["value"] == "val"

    async def test_remove_dom_storage_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.remove_dom_storage_item(sid, "key")
        method, params = fake.last_call
        assert method == "DOMStorage.removeDOMStorageItem"
        assert params is not None
        assert params["key"] == "key"

    async def test_clear_dom_storage_items(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.clear_dom_storage_items(sid)
        method, params = fake.last_call
        assert method == "DOMStorage.clear"
        assert params is not None
        assert params["storageId"] == sid

    async def test_get_cookies_with_context(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = StorageDomain(fake)
        await domain.get_cookies(browser_context_id="ctx1")
        method, params = fake.last_call
        assert method == "Storage.getCookies"
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_set_cookies_with_context(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        cookies = [{"name": "k", "value": "v"}]
        await domain.set_cookies(cookies, browser_context_id="ctx1")
        method, params = fake.last_call
        assert method == "Storage.setCookies"
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_clear_cookies_with_context(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_cookies(browser_context_id="ctx1")
        method, params = fake.last_call
        assert method == "Storage.clearCookies"
        assert params is not None
        assert params["browserContextId"] == "ctx1"


@pytest.mark.unit
class TestPageCoverage:
    async def test_go_back_with_history(self) -> None:
        fake = FakeSender({
            "currentIndex": 1,
            "entries": [
                {"id": 100, "url": "https://a.com"},
                {"id": 200, "url": "https://b.com"},
            ],
        })
        domain = PageDomain(fake)
        result = await domain.go_back()
        assert result != {}

    async def test_go_back_at_first_entry(self) -> None:
        fake = FakeSender({"currentIndex": 0, "entries": [{"id": 100}]})
        domain = PageDomain(fake)
        result = await domain.go_back()
        assert result == {}

    async def test_go_forward_with_history(self) -> None:
        fake = FakeSender({
            "currentIndex": 0,
            "entries": [
                {"id": 100, "url": "https://a.com"},
                {"id": 200, "url": "https://b.com"},
            ],
        })
        domain = PageDomain(fake)
        result = await domain.go_forward()
        assert result != {}

    async def test_go_forward_at_last_entry(self) -> None:
        fake = FakeSender({
            "currentIndex": 1,
            "entries": [{"id": 100}, {"id": 200}],
        })
        domain = PageDomain(fake)
        result = await domain.go_forward()
        assert result == {}

    async def test_add_script_with_world_name_and_run_immediately(self) -> None:
        fake = FakeSender({"identifier": "scr1"})
        domain = PageDomain(fake)
        await domain.add_script_to_evaluate_on_new_document(
            "console.log('hi')", world_name="w1", run_immediately=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["worldName"] == "w1"
        assert params["runImmediately"] is True


@pytest.mark.unit
class TestDebuggerCoverage:
    async def test_set_breakpoint_by_url_with_column_and_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(
            10,
            url="https://example.com/js.js",
            column_number=5,
            condition="x > 0",
        )
        method, params = fake.last_call
        assert method == "Debugger.setBreakpointByUrl"
        assert params is not None
        assert params["columnNumber"] == 5
        assert params["condition"] == "x > 0"

    async def test_set_breakpoint_by_url_all_params(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(
            5,
            url_regex="https://.*\\.js",
            column_number=3,
            condition="debugger",
        )
        method, params = fake.last_call
        assert method == "Debugger.setBreakpointByUrl"
        assert params is not None
        assert params["urlRegex"] == "https://.*\\.js"
        assert params["columnNumber"] == 3
        assert params["condition"] == "debugger"

    async def test_evaluate_on_call_frame_all_optional(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "cf1",
            "x + 1",
            object_group="grp",
            include_command_line_api=True,
            silent=False,
            return_by_value=True,
            generate_preview=True,
            throw_on_side_effect=False,
        )
        method, params = fake.last_call
        assert method == "Debugger.evaluateOnCallFrame"
        assert params is not None
        assert params["objectGroup"] == "grp"
        assert params["includeCommandLineAPI"] is True
        assert params["silent"] is False
        assert params["returnByValue"] is True
        assert params["generatePreview"] is True
        assert params["throwOnSideEffect"] is False

    async def test_set_script_source_with_dry_run(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;", dry_run=True)
        method, params = fake.last_call
        assert method == "Debugger.setScriptSource"
        assert params is not None
        assert params["dryRun"] is True

    async def test_get_possible_breakpoints_with_end_and_restrict(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        end = {"scriptId": "s1", "lineNumber": 10}
        await domain.get_possible_breakpoints(
            start, end=end, restrict_to_function=True
        )
        method, params = fake.last_call
        assert method == "Debugger.getPossibleBreakpoints"
        assert params is not None
        assert params["end"] == end
        assert params["restrictToFunction"] is True

    async def test_set_breakpoint_on_function_call_with_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp2"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj1", condition="x > 0")
        method, params = fake.last_call
        assert method == "Debugger.setBreakpointOnFunctionCall"
        assert params is not None
        assert params["condition"] == "x > 0"

    async def test_search_in_content(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "TODO", case_sensitive=True, is_regex=True)
        method, params = fake.last_call
        assert method == "Debugger.searchInContent"
        assert params is not None
        assert params["caseSensitive"] is True
        assert params["isRegex"] is True

    async def test_set_blackbox_patterns(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns(["node_modules/.*"])
        method, params = fake.last_call
        assert method == "Debugger.setBlackboxPatterns"
        assert params is not None
        assert params["patterns"] == ["node_modules/.*"]

    async def test_set_variable_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_variable_value("cf1", 0, "x", {"value": 42})
        method, params = fake.last_call
        assert method == "Debugger.setVariableValue"
        assert params is not None
        assert params["callFrameId"] == "cf1"
        assert params["scopeNumber"] == 0
        assert params["variableName"] == "x"
        assert params["newValue"] == {"value": 42}

    async def test_set_return_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_return_value({"value": 99})
        method, params = fake.last_call
        assert method == "Debugger.setReturnValue"
        assert params is not None
        assert params["newValue"] == {"value": 99}


@pytest.mark.unit
class TestOverlayCoverage:
    async def test_set_inspect_mode_with_highlight_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hc = {"showInfo": True}
        await domain.set_inspect_mode("searchForNode", highlight_config=hc)
        method, params = fake.last_call
        assert method == "Overlay.setInspectMode"
        assert params is not None
        assert params["highlightConfig"] == hc

    async def test_highlight_quad_with_colors(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
        outline = {"r": 0, "g": 0, "b": 255, "a": 1.0}
        await domain.highlight_quad(
            [0, 0, 100, 0, 100, 100, 0, 100], color=color, outline_color=outline,
        )
        method, params = fake.last_call
        assert method == "Overlay.highlightQuad"
        assert params is not None
        assert params["color"] == color
        assert params["outlineColor"] == outline

    async def test_highlight_rect_with_colors(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
        outline = {"r": 0, "g": 0, "b": 255, "a": 1.0}
        await domain.highlight_rect(10, 20, 100, 50, color=color, outline_color=outline)
        method, params = fake.last_call
        assert method == "Overlay.highlightRect"
        assert params is not None
        assert params["color"] == color
        assert params["outlineColor"] == outline

    async def test_highlight_rect_default_no_colors(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_rect(0, 0, 100, 50)
        method, params = fake.last_call
        assert method == "Overlay.highlightRect"
        assert params == {"x": 0, "y": 0, "width": 100, "height": 50}

    async def test_highlight_rect_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="x must be an int"):
            await domain.highlight_rect("bad", 0, 100, 50)  # type: ignore[arg-type]


@pytest.mark.unit
class TestInputCoverage:
    async def test_dispatch_key_event_all_optional(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_key_event(
            "keyDown",
            key="a",
            code="KeyA",
            windows_virtual_key_code=65,
            native_virtual_key_code=65,
            text="a",
            unmodified_text="a",
            modifiers=0,
            timestamp=1000.0,
            auto_repeat=False,
            is_keypad=False,
            is_system_key=False,
            location=0,
            commands=["copy"],
        )
        method, params = fake.last_call
        assert method == "Input.dispatchKeyEvent"
        assert params is not None
        assert params["key"] == "a"
        assert params["code"] == "KeyA"
        assert params["windowsVirtualKeyCode"] == 65
        assert params["nativeVirtualKeyCode"] == 65
        assert params["unmodifiedText"] == "a"
        assert params["modifiers"] == 0
        assert params["timestamp"] == 1000.0
        assert params["autoRepeat"] is False
        assert params["isKeypad"] is False
        assert params["isSystemKey"] is False
        assert params["location"] == 0
        assert params["commands"] == ["copy"]

    async def test_dispatch_mouse_event_all_optional(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_mouse_event(
            "mousePressed",
            x=10.0,
            y=20.0,
            button="left",
            buttons=1,
            click_count=1,
            delta_x=5.0,
            delta_y=10.0,
            modifiers=0,
            timestamp=1000.0,
        )
        method, params = fake.last_call
        assert method == "Input.dispatchMouseEvent"
        assert params is not None
        assert params["clickCount"] == 1
        assert params["deltaX"] == 5.0
        assert params["deltaY"] == 10.0
        assert params["modifiers"] == 0
        assert params["timestamp"] == 1000.0

    async def test_dispatch_touch_event_all_optional(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        points = [{"x": 10, "y": 20}]
        await domain.dispatch_touch_event(
            "touchStart", points, modifiers=0, timestamp=1000.0
        )
        method, params = fake.last_call
        assert method == "Input.dispatchTouchEvent"
        assert params is not None
        assert params["modifiers"] == 0
        assert params["timestamp"] == 1000.0

    async def test_dispatch_drag_event_all_optional(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        data = {"items": [], "dragOperationsMask": 1}
        await domain.dispatch_drag_event(
            "dragEnter", 10.0, 20.0, data=data, modifiers=0
        )
        method, params = fake.last_call
        assert method == "Input.dispatchDragEvent"
        assert params is not None
        assert params["data"] == data
        assert params["modifiers"] == 0

    async def test_type_text(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.type_text("abc")
        assert len(fake.calls) == 3
        for i, (method, params) in enumerate(fake.calls):
            assert method == "Input.dispatchKeyEvent"
            assert params is not None
            assert params["type"] == "char"
            assert params["text"] == "abc"[i]

    async def test_emulate_touch_from_mouse_event_all_optional(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.emulate_touch_from_mouse_event(
            "mousePressed",
            10,
            20,
            button="left",
            click_count=1,
            delta_x=5.0,
            delta_y=10.0,
            modifiers=0,
            timestamp=1000.0,
        )
        method, params = fake.last_call
        assert method == "Input.emulateTouchFromMouseEvent"
        assert params is not None
        assert params["clickCount"] == 1
        assert params["deltaX"] == 5.0
        assert params["deltaY"] == 10.0
        assert params["modifiers"] == 0
        assert params["timestamp"] == 1000.0

    async def test_set_ignore_input_events(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.set_ignore_input_events(True)
        method, params = fake.last_call
        assert method == "Input.setIgnoreInputEvents"
        assert params == {"ignore": True}


@pytest.mark.unit
class TestBrowserCoverage:
    async def test_set_download_behavior_all_params(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_download_behavior(
            "allow",
            browser_context_id="ctx1",
            download_path="/tmp",
            events_enabled=True,
        )
        method, params = fake.last_call
        assert method == "Browser.setDownloadBehavior"
        assert params is not None
        assert params["browserContextId"] == "ctx1"
        assert params["downloadPath"] == "/tmp"
        assert params["eventsEnabled"] is True

    async def test_get_browser_command_line(self) -> None:
        fake = FakeSender({"arguments": ["--foo"]})
        domain = BrowserDomain(fake)
        result = await domain.get_browser_command_line()
        assert fake.last_call[0] == "Browser.getBrowserCommandLine"
        assert "arguments" in result

    async def test_get_command_line_alias(self) -> None:
        fake = FakeSender({"arguments": ["--foo"]})
        domain = BrowserDomain(fake)
        result = await domain.get_command_line()
        assert "arguments" in result

    async def test_get_histogram_with_delta(self) -> None:
        fake = FakeSender({"histogram": {"name": "test", "sum": 100}})
        domain = BrowserDomain(fake)
        await domain.get_histogram("V8.ExecuteJS", delta=True)
        method, params = fake.last_call
        assert method == "Browser.getHistogram"
        assert params is not None
        assert params["delta"] is True

    async def test_get_histograms(self) -> None:
        fake = FakeSender({"histograms": []})
        domain = BrowserDomain(fake)
        await domain.get_histograms()
        method, params = fake.last_call
        assert method == "Browser.getHistograms"
        assert params is not None
        assert params["delta"] is False

    async def test_get_histograms_with_query(self) -> None:
        fake = FakeSender({"histograms": []})
        domain = BrowserDomain(fake)
        await domain.get_histograms(query="V8", delta=True)
        method, params = fake.last_call
        assert params is not None
        assert params["query"] == "V8"
        assert params["delta"] is True


@pytest.mark.unit
class TestEmulationCoverage:
    async def test_clear_auto_dark_mode_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_auto_dark_mode_override()
        assert fake.last_call == (
            "Emulation.setAutoDarkModeOverride",
            {"enabled": False},
        )

    async def test_set_navigator_overrides(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_navigator_overrides("Win32")
        method, params = fake.last_call
        assert method == "Emulation.setNavigatorOverrides"
        assert params == {"platform": "Win32"}

    async def test_set_virtual_time_policy_all_optional(self) -> None:
        fake = FakeSender({"virtualTimeTicksBase": 0.0})
        domain = EmulationDomain(fake)
        await domain.set_virtual_time_policy(
            "pause",
            budget=500,
            max_virtual_time_task_starvation_count=1000,
            initial_virtual_time=100.0,
        )
        method, params = fake.last_call
        assert method == "Emulation.setVirtualTimePolicy"
        assert params is not None
        assert params["budget"] == 500
        assert params["maxVirtualTimeTaskStarvationCount"] == 1000
        assert params["initialVirtualTime"] == 100.0

    async def test_set_focus_emulation_enabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_focus_emulation_enabled(True)
        method, params = fake.last_call
        assert method == "Emulation.setFocusEmulationEnabled"
        assert params == {"enabled": True}

    async def test_set_emulated_vision_deficiency(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_vision_deficiency("deuteranopia")
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedVisionDeficiency"
        assert params == {"type": "deuteranopia"}

    async def test_clear_emulated_vision_deficiency(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_emulated_vision_deficiency()
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedVisionDeficiency"
        assert params == {"type": "none"}

    async def test_clear_emulated_media(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_emulated_media()
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedMedia"
        assert params is None

    async def test_set_emulated_media_feature(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_media_feature("prefers-color-scheme", "dark")
        method, params = fake.last_call
        assert method == "Emulation.setEmulatedMedia"
        assert params is not None
        assert params["features"] == [{"name": "prefers-color-scheme", "value": "dark"}]

    async def test_set_default_background_color_override_from_rgba(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_default_background_color_override(r=255, g=0, b=0, a=0.5)
        method, params = fake.last_call
        assert method == "Emulation.setDefaultBackgroundColorOverride"
        assert params is not None
        assert params["color"] == {"r": 255, "g": 0, "b": 0, "a": 0.5}

    async def test_set_default_background_color_override_clear(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_default_background_color_override()
        method, params = fake.last_call
        assert method == "Emulation.setDefaultBackgroundColorOverride"
        assert params == {}

    async def test_clear_default_background_color_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_default_background_color_override()
        assert fake.last_call[0] == "Emulation.setDefaultBackgroundColorOverride"


@pytest.mark.unit
class TestFinderCoverage:
    def test_check_paths_empty_list(self) -> None:
        assert _check_paths([]) is None

    def test_check_paths_nonexistent(self) -> None:
        assert _check_paths(["/nonexistent/path/xyz"]) is None

    def test_find_on_linux_not_found(self) -> None:
        result = _find_on_linux(["nonexistent_binary_xyz_123"])
        assert result is None

    def test_find_chrome_env_not_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CDPWAVE_CHROME_PATH", "/nonexistent/chrome")
        monkeypatch.setattr("sys.platform", "linux")
        monkeypatch.setattr(
            "cdpwave.browser.finder._find_on_linux", lambda names: None
        )
        assert find_chrome() is None

    def test_find_edge_env_not_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CDPWAVE_EDGE_PATH", "/nonexistent/edge")
        monkeypatch.setattr("sys.platform", "linux")
        monkeypatch.setattr(
            "cdpwave.browser.finder._find_on_linux", lambda names: None
        )
        assert find_edge() is None

    def test_find_brave_env_not_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CDPWAVE_BRAVE_PATH", "/nonexistent/brave")
        monkeypatch.setattr("sys.platform", "linux")
        monkeypatch.setattr(
            "cdpwave.browser.finder._find_on_linux", lambda names: None
        )
        assert find_brave() is None

    def test_find_chromium_env_not_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CDPWAVE_CHROMIUM_PATH", "/nonexistent/chromium")
        monkeypatch.setattr("sys.platform", "linux")
        monkeypatch.setattr(
            "cdpwave.browser.finder._find_on_linux", lambda names: None
        )
        assert find_chromium() is None

    def test_find_chrome_macos(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_CHROME_PATH", raising=False)
        monkeypatch.setattr("sys.platform", "darwin")
        monkeypatch.setattr(
            "cdpwave.browser.finder._check_paths", lambda paths: "/fake/chrome"
        )
        assert find_chrome() == "/fake/chrome"

    def test_find_edge_macos(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_EDGE_PATH", raising=False)
        monkeypatch.setattr("sys.platform", "darwin")
        monkeypatch.setattr(
            "cdpwave.browser.finder._check_paths", lambda paths: "/fake/edge"
        )
        assert find_edge() == "/fake/edge"

    def test_find_brave_macos(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_BRAVE_PATH", raising=False)
        monkeypatch.setattr("sys.platform", "darwin")
        monkeypatch.setattr(
            "cdpwave.browser.finder._check_paths", lambda paths: "/fake/brave"
        )
        assert find_brave() == "/fake/brave"

    def test_find_chromium_macos(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_CHROMIUM_PATH", raising=False)
        monkeypatch.setattr("sys.platform", "darwin")
        monkeypatch.setattr(
            "cdpwave.browser.finder._check_paths", lambda paths: "/fake/chromium"
        )
        assert find_chromium() == "/fake/chromium"

    def test_find_browser_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        with pytest.raises(BrowserNotFoundError):
            find_browser()

    def test_find_browser_with_preferred(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: "/fake/edge")
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        result = find_browser(preferred="edge")
        assert result == "/fake/edge"

    def test_find_browser_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as f:
            tmp_path = f.name
        try:
            monkeypatch.setenv("CDPWAVE_BROWSER_PATH", tmp_path)
            result = find_browser()
            assert result == tmp_path
        finally:
            os.unlink(tmp_path)


@pytest.mark.unit
class TestDiscoveryCoverage:
    def test_http_get_returns_parsed_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import json

        class FakeResp:
            def __init__(self, data: bytes) -> None:
                self._data = data

            def read(self) -> bytes:
                return self._data

            def __enter__(self) -> "FakeResp":
                return self

            def __exit__(self, *args: object) -> None:
                pass

        payload = json.dumps({"Browser": "Chrome/100"}).encode()
        monkeypatch.setattr(
            "cdpwave.browser.discovery.urllib.request.urlopen",
            lambda url, timeout: FakeResp(payload),
        )
        result = _http_get("http://localhost:9222/json/version")
        assert result["Browser"] == "Chrome/100"

    def test_http_put_returns_parsed_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import json

        class FakeResp:
            def __init__(self, data: bytes) -> None:
                self._data = data

            def read(self) -> bytes:
                return self._data

            def __enter__(self) -> "FakeResp":
                return self

            def __exit__(self, *args: object) -> None:
                pass

        payload = json.dumps({"id": "tab1"}).encode()
        monkeypatch.setattr(
            "cdpwave.browser.discovery.urllib.request.urlopen",
            lambda req, timeout: FakeResp(payload),
        )
        result = _http_put("http://localhost:9222/json/new")
        assert result["id"] == "tab1"


@pytest.mark.unit
class TestFetchCoverage:
    async def test_continue_with_auth_username_and_password(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_with_auth(
            "req1", "ProvideCredentials", username="user", password="pass",
        )
        method, params = fake.last_call
        assert method == "Fetch.continueWithAuth"
        assert params is not None
        assert params["authChallengeResponse"]["username"] == "user"
        assert params["authChallengeResponse"]["password"] == "pass"

    async def test_fulfill_request_with_all_optional(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        headers = [{"name": "Content-Type", "value": "application/json"}]
        await domain.fulfill_request(
            "req1",
            response_code=200,
            response_headers=headers,
            body="SGVsbG8=",
            binary_response_headers="aGVhZGVycw==",
        )
        method, params = fake.last_call
        assert method == "Fetch.fulfillRequest"
        assert params is not None
        assert params["responseCode"] == 200
        assert params["responseHeaders"] == headers
        assert params["body"] == "SGVsbG8="
        assert params["binaryResponseHeaders"] == "aGVhZGVycw=="

    async def test_fulfill_request_with_status_code_alias(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.fulfill_request("req1", status_code=404)
        method, params = fake.last_call
        assert method == "Fetch.fulfillRequest"
        assert params is not None
        assert params["responseCode"] == 404

    async def test_fulfill_request_no_code_raises(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        with pytest.raises(ValueError, match="response_code or status_code"):
            await domain.fulfill_request("req1")

    async def test_continue_response_all_optional(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        headers = [{"name": "X-Custom", "value": "yes"}]
        await domain.continue_response(
            "req1",
            response_code=302,
            response_headers=headers,
            binary_response_headers="aGc=",
            response_phrase="Found",
        )
        method, params = fake.last_call
        assert method == "Fetch.continueResponse"
        assert params is not None
        assert params["responseCode"] == 302
        assert params["responseHeaders"] == headers
        assert params["binaryResponseHeaders"] == "aGc="
        assert params["responsePhrase"] == "Found"


@pytest.mark.unit
@pytest.mark.filterwarnings("ignore::RuntimeWarning:cdpwave.browser.launcher")
class TestLauncherCoverage:
    def test_is_ci_with_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from cdpwave.browser.launcher import _is_ci

        monkeypatch.setenv("CI", "true")
        assert _is_ci() is True

    def test_is_ci_without_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from cdpwave.browser.launcher import _is_ci

        for var in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"):
            monkeypatch.delenv(var, raising=False)
        assert _is_ci() is False

    def test_find_free_port(self) -> None:
        from cdpwave.browser.launcher import _find_free_port

        port = _find_free_port()
        assert isinstance(port, int)
        assert port > 0

    def test_build_args_with_headless_and_ci(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        monkeypatch.setenv("CI", "true")
        monkeypatch.setattr("cdpwave.browser.launcher.find_browser", lambda: "/fake/chrome")
        launcher = BrowserLauncher(browser_path=None, port=1234, headless=True)
        args = launcher._build_args()
        assert "--headless=new" in args
        assert "--no-sandbox" in args
        assert "--remote-debugging-port=1234" in args

    def test_build_args_with_extra_args(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        monkeypatch.delenv("CI", raising=False)
        monkeypatch.setattr("cdpwave.browser.launcher.find_browser", lambda: "/fake/chrome")
        launcher = BrowserLauncher(
            browser_path="/fake/chrome", port=0, headless=False, extra_args=["--disable-gpu"]
        )
        args = launcher._build_args()
        assert "--disable-gpu" in args
        assert "--headless=new" not in args

    def test_build_args_with_user_data_dir(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        monkeypatch.delenv("CI", raising=False)
        launcher = BrowserLauncher(
            browser_path="/fake/chrome", port=0, headless=False, user_data_dir="/tmp/profile"
        )
        args = launcher._build_args()
        assert "--user-data-dir=/tmp/profile" in args

    async def test_launch_already_running_raises(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        launcher = BrowserLauncher(browser_path="/fake/chrome")
        launcher._process = MagicMock()  # type: ignore[assignment]
        with pytest.raises(RuntimeError, match="already running"):
            await launcher.launch()

    async def test_close_without_process(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        launcher = BrowserLauncher(browser_path="/fake/chrome")
        await launcher.close()
        assert launcher.is_running is False
        assert launcher.info is None

    def test_info_property_none_before_launch(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        launcher = BrowserLauncher(browser_path="/fake/chrome")
        assert launcher.info is None

    async def test_wait_for_endpoint_process_exited(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher, LaunchError

        launcher = BrowserLauncher(browser_path="/fake/chrome", port=1234)
        mock_proc = AsyncMock()
        mock_proc.returncode = 1
        mock_proc.stderr = AsyncMock()
        mock_proc.stderr.read.return_value = b"some error"
        launcher._process = mock_proc
        with pytest.raises(LaunchError, match="exited with code 1"):
            await launcher._wait_for_endpoint(timeout=1.0)

    async def test_wait_for_endpoint_process_exited_no_stderr(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher, LaunchError

        launcher = BrowserLauncher(browser_path="/fake/chrome", port=1234)
        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.stderr = None
        launcher._process = mock_proc
        with pytest.raises(LaunchError, match="exited with code 0"):
            await launcher._wait_for_endpoint(timeout=1.0)

    async def test_wait_for_endpoint_timeout(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher, LaunchTimeoutError

        launcher = BrowserLauncher(browser_path="/fake/chrome", port=1234)
        mock_proc = AsyncMock()
        mock_proc.returncode = None
        launcher._process = mock_proc
        with pytest.raises(LaunchTimeoutError, match="did not become ready"):
            await launcher._wait_for_endpoint(timeout=0.2)

    async def test_close_terminates_process(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        launcher = BrowserLauncher(browser_path="/fake/chrome")
        mock_proc = MagicMock()
        mock_proc.returncode = None
        mock_proc.terminate = lambda: None
        mock_proc.wait = AsyncMock(return_value=0)
        launcher._process = mock_proc
        await launcher.close()
        assert launcher._process is None

    async def test_close_kills_on_timeout(self) -> None:
        from cdpwave.browser.launcher import BrowserLauncher

        launcher = BrowserLauncher(browser_path="/fake/chrome")
        mock_proc = MagicMock()
        mock_proc.returncode = None
        mock_proc.terminate = lambda: None
        mock_proc.kill = lambda: None
        mock_proc.wait = AsyncMock(side_effect=TimeoutError)
        launcher._process = mock_proc

        async def fake_wait_for(coro: Any, timeout: float) -> Any:
            if timeout == 2.0:
                coro.close()
                raise TimeoutError()
            return await coro

        with patch("cdpwave.browser.launcher.asyncio.wait_for", fake_wait_for):
            await launcher.close()
        assert launcher._process is None


@pytest.mark.unit
class TestClientDomainProperties:
    async def test_all_domain_properties(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPSession

        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        assert session.input is not None
        assert session.emulation is not None
        assert session.fetch is not None
        assert session.performance is not None
        assert session.profiler is not None
        assert session.debugger is not None
        assert session.overlay is not None
        assert session.security is not None
        assert session.audits is not None
        assert session.accessibility is not None
        assert session.storage is not None
        assert session.tracing is not None
        assert session.animation is not None
        assert session.service_worker is not None
        assert session.system_info is not None
        assert session.web_authn is not None
        assert session.io is not None
        assert session.memory is not None
        assert session.schema is not None
        assert session.device_orientation is not None
        assert session.sensor is not None
        assert session.headless_experimental is not None
        assert session.tethering is not None
        assert session.background_service is not None
        assert session.cast is not None
        assert session.preload is not None
        assert session.indexed_db is not None
        assert session.media is not None
        assert session.device_access is not None
        assert session.extensions is not None
        assert session.pwa is not None
        assert session.worker is not None
        assert session.inspector is not None
        assert session.cache_storage is not None
        assert session.css is not None
        assert session.dom_debugger is not None
        assert session.dom_snapshot is not None
        assert session.event_breakpoints is not None
        assert session.heap_profiler is not None
        assert session.layer_tree is not None
        assert session.performance_timeline is not None
        assert session.autofill is not None
        assert session.web_audio is not None

    async def test_close_with_managed_target(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        conn.send_command.return_value = {}
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._managed_targets.add("T-1")
        await session.close()
        assert session.is_closed is True
        assert "T-1" not in client._managed_targets

    async def test_wait_for_event_returns_params(self) -> None:

        from unittest.mock import AsyncMock

        from cdpwave.client import CDPSession

        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")

        async def fire_event() -> None:
            await asyncio.sleep(0.05)
            await session._dispatcher.dispatch("Page.loadEventFired", {"frameId": "F1"})

        task = asyncio.create_task(fire_event())
        result = await session.wait_for_event("Page.loadEventFired", timeout=2.0)
        await task
        assert result == {"frameId": "F1"}

    async def test_wait_for_event_timeout(self) -> None:

        from unittest.mock import AsyncMock

        from cdpwave.client import CDPSession

        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        with pytest.raises(TimeoutError):
            await session.wait_for_event("Page.loadEventFired", timeout=0.1)

    async def test_send_on_closed_session_raises(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPSession
        from cdpwave.exceptions import SessionClosedError

        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        await session.close()
        with pytest.raises(SessionClosedError):
            await session.send("Page.enable")

    async def test_client_off_removes_handler(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)

        async def handler(params: dict) -> None:
            pass

        sub = client.on("Page.loadEventFired", handler)
        client.off("Page.loadEventFired", handler)
        assert sub not in client._dispatcher._handlers.get("Page.loadEventFired", [])

    async def test_client_send_method(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.send_command.return_value = {"result": 42}
        client = CDPClient(conn)
        result = await client.send("SystemInfo.getInfo")
        assert result == {"result": 42}

    async def test_client_browser_property(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        client = CDPClient(conn)
        assert client.browser is not None

    async def test_client_is_closed_and_is_connected(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        assert client.is_closed is False
        assert client.is_connected is True
        conn.is_closed = True
        assert client.is_closed is True
        assert client.is_connected is False

    async def test_client_sessions_property(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        client = CDPClient(conn)
        assert client.sessions == []
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session
        assert len(client.sessions) == 1
        assert client.sessions[0] is session

    async def test_event_callback_detached_from_target(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session
        await client._event_callback(
            "Target.detachedFromTarget", {"sessionId": "S-1"}, None
        )
        assert session.is_closed is True
        assert "S-1" not in client._sessions

    async def test_event_callback_detached_unknown_session(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        client = CDPClient(conn)
        await client._event_callback(
            "Target.detachedFromTarget", {"sessionId": "S-unknown"}, None
        )

    async def test_event_callback_with_session_id(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session

        received: list[dict] = []

        async def handler(params: dict) -> None:
            received.append(params)

        session.on("Page.loadEventFired", handler)
        await client._event_callback(
            "Page.loadEventFired", {"frameId": "F1"}, "S-1"
        )
        assert received == [{"frameId": "F1"}]

    async def test_event_callback_with_unknown_session_id(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        client = CDPClient(conn)
        await client._event_callback(
            "Page.loadEventFired", {"frameId": "F1"}, "S-unknown"
        )

    async def test_event_callback_browser_level(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        client = CDPClient(conn)

        received: list[dict] = []

        async def handler(params: dict) -> None:
            received.append(params)

        client.on("Target.targetCreated", handler)
        await client._event_callback(
            "Target.targetCreated", {"targetId": "T-1"}, None
        )
        assert received == [{"targetId": "T-1"}]

    async def test_connect_with_ws_url(self) -> None:
        from unittest.mock import AsyncMock, patch

        from cdpwave.client import CDPClient

        mock_conn = AsyncMock()
        mock_conn.is_closed = False

        with patch(_CONNECT, return_value=mock_conn):
            client = await CDPClient.connect(ws_url="ws://localhost:9222/devtools/browser/abc")

        assert client.is_closed is False
        assert client.is_connected is True

    async def test_close_idempotent(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        client = CDPClient(conn)
        await client.close()
        await client.close()
        assert conn.close.call_count == 1
