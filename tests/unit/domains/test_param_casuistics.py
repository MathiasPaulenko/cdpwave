"""Unit tests for parameter casuistics of methods with many optional params.

Covers optional parameter combinations for Input, Debugger, Emulation,
Fetch, Runtime, Page, Tracing, Network, Overlay, Accessibility, Audits,
CacheStorage, IndexedDB, ServiceWorker.
"""

import pytest

from cdpwave.domains.accessibility import AccessibilityDomain
from cdpwave.domains.audits import AuditsDomain
from cdpwave.domains.cache_storage import CacheStorageDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.fetch import FetchDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
from cdpwave.domains.input import InputDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.runtime import RuntimeDomain
from cdpwave.domains.service_worker import ServiceWorkerDomain
from cdpwave.domains.tracing import TracingDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestInputParamCasuistics:
    async def test_dispatch_key_event_with_unmodified_text(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_key_event("keyDown", unmodified_text="a")
        method, params = fake.last_call
        assert params is not None
        assert params["unmodifiedText"] == "a"

    async def test_dispatch_key_event_with_commands(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_key_event("keyDown", commands=["selectAll"])
        method, params = fake.last_call
        assert params is not None
        assert params["commands"] == ["selectAll"]

    async def test_dispatch_mouse_event_with_delta_x(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_mouse_event("mouseWheel", 10.0, 20.0, delta_x=5.0)
        method, params = fake.last_call
        assert params is not None
        assert params["deltaX"] == 5.0

    async def test_dispatch_mouse_event_with_delta_y(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_mouse_event("mouseWheel", 10.0, 20.0, delta_y=-10.0)
        method, params = fake.last_call
        assert params is not None
        assert params["deltaY"] == -10.0

    async def test_ime_set_composition_with_composition_range(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.ime_set_composition(
            "text", 0, 4, composition_start=0, composition_end=4
        )
        method, params = fake.last_call
        assert params is not None
        assert params["compositionStart"] == 0
        assert params["compositionEnd"] == 4

    async def test_ime_set_composition_with_replace(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.ime_set_composition("text", 0, 4, replace=True)
        method, params = fake.last_call
        assert params is not None
        assert params["replace"] is True

    async def test_synthesize_pinch_gesture_with_relative_speed(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_pinch_gesture(100, 100, 2.0, relative_speed=500)
        method, params = fake.last_call
        assert params is not None
        assert params["relativeSpeed"] == 500

    async def test_synthesize_pinch_gesture_with_gesture_source_type(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_pinch_gesture(100, 100, 2.0, gesture_source_type="touch")
        method, params = fake.last_call
        assert params is not None
        assert params["gestureSourceType"] == "touch"

    async def test_synthesize_scroll_gesture_with_x_distance(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, x_distance=50.0)
        method, params = fake.last_call
        assert params is not None
        assert params["xDistance"] == 50.0

    async def test_synthesize_scroll_gesture_with_overscroll(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(
            100, 100, x_overscroll=10.0, y_overscroll=20.0
        )
        method, params = fake.last_call
        assert params is not None
        assert params["xOverscroll"] == 10.0
        assert params["yOverscroll"] == 20.0

    async def test_synthesize_scroll_gesture_with_prevent_fling(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, prevent_fling=False)
        method, params = fake.last_call
        assert params is not None
        assert params["preventFling"] is False

    async def test_synthesize_scroll_gesture_with_speed(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, speed=1200)
        method, params = fake.last_call
        assert params is not None
        assert params["speed"] == 1200

    async def test_synthesize_scroll_gesture_with_gesture_source_type(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, gesture_source_type="mouse")
        method, params = fake.last_call
        assert params is not None
        assert params["gestureSourceType"] == "mouse"

    async def test_synthesize_scroll_gesture_with_repeat_count(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, repeat_count=5)
        method, params = fake.last_call
        assert params is not None
        assert params["repeatCount"] == 5

    async def test_synthesize_scroll_gesture_with_repeat_delay_ms(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(100, 100, repeat_delay_ms=100)
        method, params = fake.last_call
        assert params is not None
        assert params["repeatDelayMs"] == 100

    async def test_synthesize_tap_gesture_with_tap_count(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_tap_gesture(100, 100, tap_count=2)
        method, params = fake.last_call
        assert params is not None
        assert params["tapCount"] == 2

    async def test_synthesize_tap_gesture_with_gesture_source_type(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_tap_gesture(100, 100, gesture_source_type="touch")
        method, params = fake.last_call
        assert params is not None
        assert params["gestureSourceType"] == "touch"


@pytest.mark.unit
class TestDebuggerParamCasuistics:
    async def test_evaluate_on_call_frame_with_include_command_line_api(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "frame1", "1+1", include_command_line_api=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["includeCommandLineAPI"] is True

    async def test_evaluate_on_call_frame_with_silent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("frame1", "1+1", silent=True)
        method, params = fake.last_call
        assert params is not None
        assert params["silent"] is True

    async def test_evaluate_on_call_frame_with_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "frame1", "1+1", generate_preview=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["generatePreview"] is True

    async def test_evaluate_on_call_frame_with_throw_on_side_effect(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "frame1", "1+1", throw_on_side_effect=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["throwOnSideEffect"] is True

    async def test_search_in_content_with_case_sensitive(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "query", case_sensitive=True)
        method, params = fake.last_call
        assert params is not None
        assert params["caseSensitive"] is True

    async def test_search_in_content_with_is_regex(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "qu.*ry", is_regex=True)
        method, params = fake.last_call
        assert params is not None
        assert params["isRegex"] is True

    async def test_set_breakpoint_by_url_with_column_number(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url("https://example.com", 10, column_number=5)
        method, params = fake.last_call
        assert params is not None
        assert params["columnNumber"] == 5


@pytest.mark.unit
class TestEmulationParamCasuistics:
    async def test_set_device_metrics_override_with_screen_dimensions(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2, mobile=True,
            screen_width=375, screen_height=667,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["screenWidth"] == 375
        assert params["screenHeight"] == 667

    async def test_set_device_metrics_override_with_position(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2, mobile=True,
            position_x=10, position_y=20,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["positionX"] == 10
        assert params["positionY"] == 20

    async def test_set_device_metrics_override_with_display_feature(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        display_feature = {
            "orientation": "portrait",
            "offset": 0,
            "maskLength": 100,
            "maskThickness": 50,
        }
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2, mobile=True,
            display_feature=display_feature,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["displayFeature"] == {
            "orientation": "portrait",
            "offset": 0,
            "maskLength": 100,
            "maskThickness": 50,
        }

    async def test_set_device_metrics_override_with_device_posture(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        posture = {"type": "folded", "fold": 0.5}
        await domain.set_device_metrics_override(
            width=375, height=667, device_scale_factor=2, mobile=True,
            device_posture=posture,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["devicePosture"] == posture

    async def test_set_user_agent_override_with_metadata(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        metadata = {"platform": "iPhone", "mobile": True}
        await domain.set_user_agent_override(
            "Mozilla/5.0", user_agent_metadata=metadata
        )
        method, params = fake.last_call
        assert params is not None
        assert params["userAgentMetadata"] == metadata


@pytest.mark.unit
class TestFetchParamCasuistics:
    async def test_continue_request_with_intercept_response(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_request("req1", intercept_response=True)
        method, params = fake.last_call
        assert params is not None
        assert params["interceptResponse"] is True

    async def test_continue_response_with_response_headers(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        headers = [{"name": "Content-Type", "value": "text/html"}]
        await domain.continue_response("req1", response_headers=headers)
        method, params = fake.last_call
        assert params is not None
        assert params["responseHeaders"] == headers

    async def test_continue_response_with_binary_response_headers(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_response("req1", binary_response_headers="base64data")
        method, params = fake.last_call
        assert params is not None
        assert params["binaryResponseHeaders"] == "base64data"

    async def test_continue_response_with_status_text(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_response("req1", status_text="OK")
        method, params = fake.last_call
        assert params is not None
        assert params["statusText"] == "OK"

    async def test_fulfill_request_with_response_headers(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        headers = [{"name": "X-Custom", "value": "test"}]
        await domain.fulfill_request("req1", 200, response_headers=headers)
        method, params = fake.last_call
        assert params is not None
        assert params["responseHeaders"] == headers

    async def test_fulfill_request_with_binary_response_headers(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.fulfill_request("req1", 200, binary_response_headers="base64hdr")
        method, params = fake.last_call
        assert params is not None
        assert params["binaryResponseHeaders"] == "base64hdr"


@pytest.mark.unit
class TestRuntimeParamCasuistics:
    async def test_evaluate_with_user_gesture(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", user_gesture=True)
        method, params = fake.last_call
        assert params is not None
        assert params["userGesture"] is True

    async def test_evaluate_with_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("({})", generate_preview=True)
        method, params = fake.last_call
        assert params is not None
        assert params["generatePreview"] is True

    async def test_evaluate_with_silent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("throw new Error()", silent=True)
        method, params = fake.last_call
        assert params is not None
        assert params["silent"] is True

    async def test_call_function_on_with_execution_context_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return 1; }", execution_context_id=3
        )
        method, params = fake.last_call
        assert params is not None
        assert params["executionContextId"] == 3

    async def test_call_function_on_with_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return {}; }", object_id="obj1", generate_preview=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["generatePreview"] is True

    async def test_call_function_on_with_silent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return 1; }", object_id="obj1", silent=True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["silent"] is True

    async def test_compile_script_with_source_url(self) -> None:
        fake = FakeSender({"scriptId": "s1"})
        domain = RuntimeDomain(fake)
        await domain.compile_script("1+2", source_url="test.js")
        method, params = fake.last_call
        assert params is not None
        assert params["sourceURL"] == "test.js"

    async def test_compile_script_with_execution_context_id(self) -> None:
        fake = FakeSender({"scriptId": "s1"})
        domain = RuntimeDomain(fake)
        await domain.compile_script("1+2", execution_context_id=5)
        method, params = fake.last_call
        assert params is not None
        assert params["executionContextId"] == 5

    async def test_run_script_with_execution_context_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        await domain.run_script("s1", execution_context_id=7)
        method, params = fake.last_call
        assert params is not None
        assert params["executionContextId"] == 7


@pytest.mark.unit
class TestPageParamCasuistics:
    async def test_capture_screenshot_with_from_surface(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(from_surface=False)
        method, params = fake.last_call
        assert params is not None
        assert params["fromSurface"] is False

    async def test_capture_screenshot_with_capture_beyond_viewport(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(capture_beyond_viewport=True)
        method, params = fake.last_call
        assert params is not None
        assert params["captureBeyondViewport"] is True

    async def test_print_to_pdf_with_display_header_footer(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(display_header_footer=True)
        method, params = fake.last_call
        assert params is not None
        assert params["displayHeaderFooter"] is True

    async def test_print_to_pdf_with_print_background(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(print_background=True)
        method, params = fake.last_call
        assert params is not None
        assert params["printBackground"] is True

    async def test_print_to_pdf_with_paper_width_and_height(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(paper_width=8.5, paper_height=11.0)
        method, params = fake.last_call
        assert params is not None
        assert params["paperWidth"] == 8.5
        assert params["paperHeight"] == 11.0

    async def test_print_to_pdf_with_margins(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(
            margin_top=0.5, margin_bottom=0.5, margin_left=0.5, margin_right=0.5
        )
        method, params = fake.last_call
        assert params is not None
        assert params["marginTop"] == 0.5
        assert params["marginBottom"] == 0.5
        assert params["marginLeft"] == 0.5
        assert params["marginRight"] == 0.5

    async def test_print_to_pdf_with_page_ranges(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(page_ranges="1,3,5-7")
        method, params = fake.last_call
        assert params is not None
        assert params["pageRanges"] == "1,3,5-7"

    async def test_print_to_pdf_with_header_template(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(header_template="<div>Header</div>")
        method, params = fake.last_call
        assert params is not None
        assert params["headerTemplate"] == "<div>Header</div>"

    async def test_print_to_pdf_with_footer_template(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(footer_template="<div>Footer</div>")
        method, params = fake.last_call
        assert params is not None
        assert params["footerTemplate"] == "<div>Footer</div>"

    async def test_print_to_pdf_with_prefer_css_page_size(self) -> None:
        fake = FakeSender({"data": "base64"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(prefer_css_page_size=True)
        method, params = fake.last_call
        assert params is not None
        assert params["preferCSSPageSize"] is True


@pytest.mark.unit
class TestTracingParamCasuistics:
    async def test_start_with_buffer_usage_reporting_interval(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=1.0)
        method, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 1.0

    async def test_start_with_transfer_mode_stream(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReturnAsStream")
        method, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReturnAsStream"

    async def test_start_with_stream_format_proto(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_format="proto")
        method, params = fake.last_call
        assert params is not None
        assert params["streamFormat"] == "proto"

    async def test_start_with_stream_compression_gzip(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_compression="gzip")
        method, params = fake.last_call
        assert params is not None
        assert params["streamCompression"] == "gzip"

    async def test_start_with_trace_type(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(trace_type="devtools-test")
        method, params = fake.last_call
        assert params is not None
        assert params["traceType"] == "devtools-test"


@pytest.mark.unit
class TestNetworkParamCasuistics:
    async def test_emulate_network_conditions_with_upload_throughput(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.emulate_network_conditions(
            offline=False, latency=100, download_throughput=1000,
            upload_throughput=500,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["uploadThroughput"] == 500

    async def test_emulate_network_conditions_with_resource_types(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.emulate_network_conditions(
            offline=False, latency=100, download_throughput=1000,
            upload_throughput=500, resource_types=["XHR", "Fetch"],
        )
        method, params = fake.last_call
        assert params is not None
        assert params["resourceTypes"] == ["XHR", "Fetch"]


@pytest.mark.unit
class TestOverlayParamCasuistics:
    async def test_highlight_node_with_backend_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node(
            {"showInfo": True}, backend_node_id=99
        )
        method, params = fake.last_call
        assert params is not None
        assert params["backendNodeId"] == 99

    async def test_highlight_node_with_object_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node(
            {"showInfo": True}, object_id="obj1"
        )
        method, params = fake.last_call
        assert params is not None
        assert params["objectId"] == "obj1"

    async def test_highlight_node_with_selector(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node(
            {"showInfo": True}, selector="#my-element"
        )
        method, params = fake.last_call
        assert params is not None
        assert params["selector"] == "#my-element"


@pytest.mark.unit
class TestAccessibilityParamCasuistics:
    async def test_get_partial_ax_tree_with_fetch_relatives(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_partial_ax_tree(fetch_relatives=True)
        method, params = fake.last_call
        assert params is not None
        assert params["fetchRelatives"] is True

    async def test_query_ax_tree_with_accessible_name(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.query_ax_tree(accessible_name="Submit")
        method, params = fake.last_call
        assert params is not None
        assert params["accessibleName"] == "Submit"


@pytest.mark.unit
class TestAuditsParamCasuistics:
    async def test_get_encoded_response_with_size_only(self) -> None:
        fake = FakeSender({"totalSize": 1024})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req1", "base64", size_only=True)
        method, params = fake.last_call
        assert params is not None
        assert params["sizeOnly"] is True


@pytest.mark.unit
class TestCacheStorageParamCasuistics:
    async def test_request_entries_with_cache_id(self) -> None:
        fake = FakeSender({"cacheId": "c1", "entries": []})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1")
        method, params = fake.last_call
        assert params is not None
        assert params["cacheId"] == "c1"


@pytest.mark.unit
class TestIndexedDBParamCasuistics:
    async def test_request_data_with_index_name(self) -> None:
        fake = FakeSender({"entries": []})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            database_name="db1", object_store_name="objStore1", index_name="idx1"
        )
        method, params = fake.last_call
        assert params is not None
        assert params["indexName"] == "idx1"

    async def test_request_data_with_key_range(self) -> None:
        fake = FakeSender({"entries": []})
        domain = IndexedDBDomain(fake)
        key_range = {"lower": 0, "upper": 100}
        await domain.request_data(
            database_name="db1", object_store_name="objStore1", key_range=key_range
        )
        method, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == key_range


@pytest.mark.unit
class TestServiceWorkerParamCasuistics:
    async def test_dispatch_sync_event_with_registration_id(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.dispatch_sync_event(
            "https://example.com", "reg1", "tag1", False
        )
        method, params = fake.last_call
        assert params is not None
        assert params["registrationId"] == "reg1"
