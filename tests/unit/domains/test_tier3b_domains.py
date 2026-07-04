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
        await domain.set_breakpoint_by_url("https://example.com/app.js", 20)
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
        await domain.get_stack_trace()
        assert fake.last_call == ("Debugger.getStackTrace", {})

    async def test_set_skip_all_pauses(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_skip_all_pauses(True)
        assert fake.last_call == (
            "Debugger.setSkipAllPauses",
            {"skip": True},
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
            {"show": True},
        )

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

    async def test_set_show_web_vitals(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_web_vitals(True, layered=True)
        method, params = fake.last_call
        assert method == "Overlay.setShowWebVitals"
        assert params is not None
        assert params["show"] is True
        assert params["layered"] is True

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
        fake = FakeSender({"body": "base64data", "byteSize": 100})
        domain = AuditsDomain(fake)
        await domain.get_encoded_response("req1", "base64", quality=80)
        method, params = fake.last_call
        assert method == "Audits.getEncodedResponse"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["encoding"] == "base64"
        assert params["quality"] == 80
