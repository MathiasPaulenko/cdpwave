"""Unit tests for Debugger, Overlay, Security, and Audits domains (Tier 3)."""

import pytest

from cdpwave.domains.audits import AuditsDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.security import SecurityDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDebuggerDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Debugger.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Debugger.disable", None)

    async def test_pause(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.pause()
        assert fake.last_call == ("Debugger.pause", None)

    async def test_resume(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume()
        assert fake.last_call == ("Debugger.resume", None)

    async def test_step_over(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_over()
        assert fake.last_call == ("Debugger.stepOver", None)

    async def test_step_into(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_into()
        assert fake.last_call == ("Debugger.stepInto", None)

    async def test_step_out(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_out()
        assert fake.last_call == ("Debugger.stepOut", None)

    async def test_set_breakpoint(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint(
            {"scriptId": "1", "lineNumber": 10},
            condition="x > 5",
        )
        method, params = fake.last_call
        assert method == "Debugger.setBreakpoint"
        assert params is not None
        assert params["location"]["scriptId"] == "1"
        assert params["condition"] == "x > 5"

    async def test_set_breakpoint_by_url(self) -> None:
        fake = FakeSender({"breakpointId": "bp2", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(20, url="https://example.com/app.js")
        method, params = fake.last_call
        assert method == "Debugger.setBreakpointByUrl"
        assert params is not None
        assert params["url"] == "https://example.com/app.js"
        assert params["lineNumber"] == 20

    async def test_remove_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.remove_breakpoint("bp1")
        assert fake.last_call == (
            "Debugger.removeBreakpoint",
            {"breakpointId": "bp1"},
        )

    async def test_set_pause_on_exceptions(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_pause_on_exceptions("all")
        assert fake.last_call == (
            "Debugger.setPauseOnExceptions",
            {"state": "all"},
        )

    async def test_evaluate_on_call_frame(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 42}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "frame1",
            "1 + 1",
            return_by_value=True,
        )
        method, params = fake.last_call
        assert method == "Debugger.evaluateOnCallFrame"
        assert params is not None
        assert params["callFrameId"] == "frame1"
        assert params["expression"] == "1 + 1"
        assert params["returnByValue"] is True

    async def test_get_script_source(self) -> None:
        fake = FakeSender({"scriptSource": "console.log('hi')"})
        domain = DebuggerDomain(fake)
        await domain.get_script_source("script1")
        assert fake.last_call == (
            "Debugger.getScriptSource",
            {"scriptId": "script1"},
        )

    async def test_get_stack_trace(self) -> None:
        fake = FakeSender({"stackTrace": {"callFrames": []}})
        domain = DebuggerDomain(fake)
        await domain.get_stack_trace({"id": "st1"})
        assert fake.last_call == (
            "Debugger.getStackTrace",
            {"stackTraceId": {"id": "st1"}},
        )

    async def test_set_skip_all_pauses(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_skip_all_pauses(True)
        assert fake.last_call == (
            "Debugger.setSkipAllPauses",
            {"skip": True},
        )

    async def test_get_possible_breakpoints(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        await domain.get_possible_breakpoints(start)
        method, params = fake.last_call
        assert method == "Debugger.getPossibleBreakpoints"
        assert params is not None
        assert params["start"] == start

    async def test_get_possible_breakpoints_with_end_and_restrict(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        end = {"scriptId": "s1", "lineNumber": 10}
        await domain.get_possible_breakpoints(start, end=end, restrict_to_function=True)
        method, params = fake.last_call
        assert params is not None
        assert params["end"] == end
        assert params["restrictToFunction"] is True

    async def test_set_breakpoint_on_function_call(self) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj1")
        assert fake.last_call == (
            "Debugger.setBreakpointOnFunctionCall",
            {"objectId": "obj1"},
        )

    async def test_set_breakpoint_on_function_call_with_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp2"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj1", condition="x > 5")
        method, params = fake.last_call
        assert method == "Debugger.setBreakpointOnFunctionCall"
        assert params is not None
        assert params["objectId"] == "obj1"
        assert params["condition"] == "x > 5"

    async def test_set_variable_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        new_val = {"value": 42}
        await domain.set_variable_value("frame1", 0, "myVar", new_val)
        assert fake.last_call == (
            "Debugger.setVariableValue",
            {
                "callFrameId": "frame1",
                "scopeNumber": 0,
                "variableName": "myVar",
                "newValue": new_val,
            },
        )


@pytest.mark.unit
class TestOverlayDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Overlay.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Overlay.disable", None)

    async def test_set_show_paint_rects(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_paint_rects(True)
        assert fake.last_call == (
            "Overlay.setShowPaintRects",
            {"result": True},
        )

    async def test_set_show_paint_rects_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="result must be a bool"):
            await domain.set_show_paint_rects("not a bool")  # type: ignore[arg-type]

    async def test_set_show_debug_borders(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_debug_borders(True)
        assert fake.last_call == (
            "Overlay.setShowDebugBorders",
            {"show": True},
        )

    async def test_set_show_fps_counter(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_fps_counter(True)
        assert fake.last_call == (
            "Overlay.setShowFPSCounter",
            {"show": True},
        )

    async def test_set_show_scroll_bottleneck_rects(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_scroll_bottleneck_rects(False)
        assert fake.last_call == (
            "Overlay.setShowScrollBottleneckRects",
            {"show": False},
        )

    async def test_hide_highlight(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.hide_highlight()
        assert fake.last_call == ("Overlay.hideHighlight", None)

    async def test_set_inspect_mode(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_inspect_mode("searchForNode")
        assert fake.last_call == (
            "Overlay.setInspectMode",
            {"mode": "searchForNode"},
        )

    async def test_highlight_node(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node(
            {"showInfo": True},
            node_id=42,
        )
        method, params = fake.last_call
        assert method == "Overlay.highlightNode"
        assert params is not None
        assert params["highlightConfig"]["showInfo"] is True
        assert params["nodeId"] == 42

    async def test_set_show_hinge(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hinge = {"x": 0, "y": 100, "width": 100, "height": 50}
        await domain.set_show_hinge(hinge_config=hinge)
        method, params = fake.last_call
        assert method == "Overlay.setShowHinge"
        assert params is not None
        assert params["hingeConfig"] == hinge

    async def test_set_show_hinge_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_hinge(None)
        method, params = fake.last_call
        assert method == "Overlay.setShowHinge"
        assert params is None

    async def test_set_show_window_controls_overlay(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        config = {"showCSS": True, "selectedPlatform": "windows", "themeColor": "#000"}
        await domain.set_show_window_controls_overlay(config)
        method, params = fake.last_call
        assert method == "Overlay.setShowWindowControlsOverlay"
        assert params is not None
        assert params["windowControlsOverlayConfig"] == config

    async def test_set_show_window_controls_overlay_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_window_controls_overlay(None)
        method, params = fake.last_call
        assert method == "Overlay.setShowWindowControlsOverlay"
        assert params is None

    async def test_set_show_isolated_elements(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"showInfo": True}, {"showStyles": True}]
        await domain.set_show_isolated_elements(configs)
        assert fake.last_call == (
            "Overlay.setShowIsolatedElements",
            {"isolatedElementHighlightConfigs": configs},
        )


@pytest.mark.unit
class TestSecurityDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Security.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Security.disable", None)

    async def test_handle_certificate_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        assert fake.last_call == (
            "Security.handleCertificateError",
            {"eventId": 1, "action": "continue"},
        )

    async def test_set_override_certificate_errors(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        assert fake.last_call == (
            "Security.setOverrideCertificateErrors",
            {"override": True},
        )


@pytest.mark.unit
class TestAuditsDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = AuditsDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Audits.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = AuditsDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Audits.disable", None)

    async def test_check_contrast(self) -> None:
        fake = FakeSender({})
        domain = AuditsDomain(fake)
        await domain.check_contrast()
        assert fake.last_call == ("Audits.checkContrast", None)

    async def test_get_encoded_response(self) -> None:
        fake = FakeSender({"body": "base64data", "originalSize": 100, "encodedSize": 80})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req1", "webp", quality=0.8)
        method, params = fake.last_call
        assert method == "Audits.getEncodedResponse"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["encoding"] == "webp"
        assert params["quality"] == 0.8

    async def test_get_encoded_response_size_only(self) -> None:
        fake = FakeSender({"originalSize": 100, "encodedSize": 80})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req1", "jpeg", size_only=True)
        method, params = fake.last_call
        assert params is not None
        assert params["sizeOnly"] is True

    async def test_check_forms_issues(self) -> None:
        fake = FakeSender({"issues": []})
        domain = AuditsDomain(fake)
        await domain.check_forms_issues()
        assert fake.last_call == ("Audits.checkFormsIssues", None)

    async def test_get_encoded_response_all_params(self) -> None:
        fake = FakeSender({"body": "data", "originalSize": 200, "encodedSize": 100})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response(
            "req2", "png", quality=0.5, size_only=False
        )
        method, params = fake.last_call
        assert params is not None
        assert params["requestId"] == "req2"
        assert params["encoding"] == "png"
        assert params["quality"] == 0.5
        assert params["sizeOnly"] is False

    async def test_get_encoded_response_no_optional_params(self) -> None:
        fake = FakeSender({"body": "data", "originalSize": 50, "encodedSize": 30})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req3", "webp")
        method, params = fake.last_call
        assert params is not None
        assert "quality" not in params
        assert "sizeOnly" not in params

    async def test_get_encoded_response_quality_zero(self) -> None:
        fake = FakeSender({"body": "", "originalSize": 100, "encodedSize": 1})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req4", "jpeg", quality=0.0)
        method, params = fake.last_call
        assert params is not None
        assert params["quality"] == 0.0

    async def test_get_encoded_response_quality_one(self) -> None:
        fake = FakeSender({"body": "data", "originalSize": 100, "encodedSize": 100})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req5", "webp", quality=1.0)
        method, params = fake.last_call
        assert params is not None
        assert params["quality"] == 1.0
