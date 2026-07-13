"""Edge case unit tests for the DOMDebugger domain."""

import pytest

from cdpwave.domains.dom_debugger import DOMDebuggerDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDOMDebuggerEdgeCases:
    async def test_set_dom_breakpoint_attribute_modified(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(10, "attribute-modified")
        assert fake.last_call == (
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": 10, "type": "attribute-modified"},
        )

    async def test_set_dom_breakpoint_node_removed(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(5, "node-removed")
        assert fake.last_call == (
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": 5, "type": "node-removed"},
        )

    async def test_remove_dom_breakpoint_attribute_modified(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_dom_breakpoint(10, "attribute-modified")
        assert fake.last_call == (
            "DOMDebugger.removeDOMBreakpoint",
            {"nodeId": 10, "type": "attribute-modified"},
        )

    async def test_remove_dom_breakpoint_node_removed(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_dom_breakpoint(5, "node-removed")
        assert fake.last_call == (
            "DOMDebugger.removeDOMBreakpoint",
            {"nodeId": 5, "type": "node-removed"},
        )

    async def test_set_dom_breakpoint_node_id_zero(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(0, "subtree-modified")
        assert fake.last_call == (
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": 0, "type": "subtree-modified"},
        )

    async def test_get_event_listeners_depth_zero(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1", depth=0)
        method, params = fake.last_call
        assert method == "DOMDebugger.getEventListeners"
        assert params is not None
        assert params["objectId"] == "obj-1"
        assert params["depth"] == 0

    async def test_get_event_listeners_depth_negative_one(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1", depth=-1)
        method, params = fake.last_call
        assert params is not None
        assert params["depth"] == -1

    async def test_get_event_listeners_pierce_false(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1", pierce=False)
        method, params = fake.last_call
        assert params is not None
        assert params["pierce"] is False

    async def test_get_event_listeners_pierce_true(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1", pierce=True)
        method, params = fake.last_call
        assert params is not None
        assert params["pierce"] is True

    async def test_get_event_listeners_depth_and_pierce(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1", depth=3, pierce=True)
        method, params = fake.last_call
        assert params is not None
        assert params["depth"] == 3
        assert params["pierce"] is True

    async def test_get_event_listeners_only_object_id(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("obj-1")
        method, params = fake.last_call
        assert params is not None
        assert params["objectId"] == "obj-1"
        assert "depth" not in params
        assert "pierce" not in params

    async def test_get_event_listeners_return_value(self) -> None:
        listeners_data = [
            {
                "type": "click",
                "useCapture": False,
                "passive": True,
                "once": False,
                "scriptId": "42",
                "lineNumber": 10,
                "columnNumber": 5,
            }
        ]
        fake = FakeSender({"listeners": listeners_data})
        domain = DOMDebuggerDomain(fake)
        result = await domain.get_event_listeners("obj-1")
        assert "listeners" in result
        assert len(result["listeners"]) == 1
        assert result["listeners"][0]["type"] == "click"
        assert result["listeners"][0]["passive"] is True

    async def test_remove_event_listener_breakpoint_with_target(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_event_listener_breakpoint("click", target_name="window")
        method, params = fake.last_call
        assert method == "DOMDebugger.removeEventListenerBreakpoint"
        assert params is not None
        assert params["eventName"] == "click"
        assert params["targetName"] == "window"

    async def test_set_instrumentation_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_instrumentation_breakpoint("setInterval")
        assert fake.last_call == (
            "DOMDebugger.setInstrumentationBreakpoint",
            {"eventName": "setInterval"},
        )

    async def test_remove_instrumentation_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_instrumentation_breakpoint("setInterval")
        assert fake.last_call == (
            "DOMDebugger.removeInstrumentationBreakpoint",
            {"eventName": "setInterval"},
        )

    async def test_set_break_on_csp_violation_both_types(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_break_on_csp_violation(
            ["trustedtype-sink-violation", "trustedtype-policy-violation"]
        )
        method, params = fake.last_call
        assert method == "DOMDebugger.setBreakOnCSPViolation"
        assert params is not None
        assert params["violationTypes"] == [
            "trustedtype-sink-violation",
            "trustedtype-policy-violation",
        ]

    async def test_set_break_on_csp_violation_empty_list(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_break_on_csp_violation([])
        method, params = fake.last_call
        assert method == "DOMDebugger.setBreakOnCSPViolation"
        assert params is not None
        assert params["violationTypes"] == []

    async def test_set_break_on_csp_violation_single_sink(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_break_on_csp_violation(["trustedtype-sink-violation"])
        method, params = fake.last_call
        assert params is not None
        assert params["violationTypes"] == ["trustedtype-sink-violation"]

    async def test_set_xhr_breakpoint_empty_url(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_xhr_breakpoint("")
        assert fake.last_call == (
            "DOMDebugger.setXHRBreakpoint",
            {"url": ""},
        )

    async def test_remove_xhr_breakpoint_empty_url(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_xhr_breakpoint("")
        assert fake.last_call == (
            "DOMDebugger.removeXHRBreakpoint",
            {"url": ""},
        )

    async def test_set_event_listener_breakpoint_target_empty_string(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_event_listener_breakpoint("click", target_name="")
        method, params = fake.last_call
        assert params is not None
        assert params["targetName"] == ""

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(1, "subtree-modified")
        await domain.remove_dom_breakpoint(1, "subtree-modified")
        await domain.set_xhr_breakpoint("/api/")
        await domain.remove_xhr_breakpoint("/api/")
        assert len(fake.calls) == 4
        assert fake.calls[0][0] == "DOMDebugger.setDOMBreakpoint"
        assert fake.calls[1][0] == "DOMDebugger.removeDOMBreakpoint"
        assert fake.calls[2][0] == "DOMDebugger.setXHRBreakpoint"
        assert fake.calls[3][0] == "DOMDebugger.removeXHRBreakpoint"

    async def test_all_dom_breakpoint_types_roundtrip(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        bp_types = ["subtree-modified", "attribute-modified", "node-removed"]
        for bp_type in bp_types:
            await domain.set_dom_breakpoint(1, bp_type)
            await domain.remove_dom_breakpoint(1, bp_type)
        assert len(fake.calls) == 6
        for i, bp_type in enumerate(bp_types):
            set_call = fake.calls[i * 2]
            remove_call = fake.calls[i * 2 + 1]
            assert set_call[1] is not None
            assert set_call[1]["type"] == bp_type
            assert remove_call[1] is not None
            assert remove_call[1]["type"] == bp_type

    async def test_set_dom_breakpoint_large_node_id(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(2147483647, "subtree-modified")
        method, params = fake.last_call
        assert params is not None
        assert params["nodeId"] == 2147483647

    async def test_get_event_listeners_empty_object_id(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        await domain.get_event_listeners("")
        method, params = fake.last_call
        assert params is not None
        assert params["objectId"] == ""
