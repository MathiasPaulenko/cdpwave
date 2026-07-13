"""Unit tests for type and enum validation in DOMDebugger domain."""

import pytest

from cdpwave.domains.dom_debugger import DOMDebuggerDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDOMDebuggerTypeValidation:
    async def test_set_dom_breakpoint_node_id_str_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="node_id"):
            await domain.set_dom_breakpoint("42", "subtree-modified")

    async def test_set_dom_breakpoint_node_id_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="node_id"):
            await domain.set_dom_breakpoint(True, "subtree-modified")

    async def test_set_dom_breakpoint_type_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="type"):
            await domain.set_dom_breakpoint(1, 42)

    async def test_set_dom_breakpoint_invalid_enum_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="type must be one of"):
            await domain.set_dom_breakpoint(1, "invalid-type")

    async def test_set_dom_breakpoint_empty_type_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="type must be one of"):
            await domain.set_dom_breakpoint(1, "")

    async def test_remove_dom_breakpoint_node_id_str_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="node_id"):
            await domain.remove_dom_breakpoint("42", "subtree-modified")

    async def test_remove_dom_breakpoint_type_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="type"):
            await domain.remove_dom_breakpoint(1, 42)

    async def test_remove_dom_breakpoint_invalid_enum_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="type must be one of"):
            await domain.remove_dom_breakpoint(1, "invalid-type")

    async def test_set_event_listener_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="event_name"):
            await domain.set_event_listener_breakpoint(42)

    async def test_set_event_listener_breakpoint_target_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="target_name"):
            await domain.set_event_listener_breakpoint("click", target_name=42)

    async def test_remove_event_listener_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="event_name"):
            await domain.remove_event_listener_breakpoint(42)

    async def test_remove_event_listener_breakpoint_target_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="target_name"):
            await domain.remove_event_listener_breakpoint("click", target_name=42)

    async def test_set_xhr_breakpoint_url_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="url"):
            await domain.set_xhr_breakpoint(42)

    async def test_set_xhr_breakpoint_url_list_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="url"):
            await domain.set_xhr_breakpoint(["/api/"])

    async def test_remove_xhr_breakpoint_url_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="url"):
            await domain.remove_xhr_breakpoint(42)

    async def test_get_event_listeners_object_id_int_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="object_id"):
            await domain.get_event_listeners(42)

    async def test_get_event_listeners_depth_str_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="depth"):
            await domain.get_event_listeners("obj-1", depth="0")

    async def test_get_event_listeners_depth_bool_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="depth"):
            await domain.get_event_listeners("obj-1", depth=True)

    async def test_get_event_listeners_depth_float_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="depth"):
            await domain.get_event_listeners("obj-1", depth=1.5)

    async def test_get_event_listeners_pierce_str_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="pierce"):
            await domain.get_event_listeners("obj-1", pierce="true")

    async def test_get_event_listeners_pierce_int_raises(self) -> None:
        fake = FakeSender({"listeners": []})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="pierce"):
            await domain.get_event_listeners("obj-1", pierce=1)

    async def test_set_instrumentation_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="event_name"):
            await domain.set_instrumentation_breakpoint(42)

    async def test_remove_instrumentation_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="event_name"):
            await domain.remove_instrumentation_breakpoint(42)

    async def test_set_break_on_csp_violation_str_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="violation_types"):
            await domain.set_break_on_csp_violation("trustedtype-sink-violation")

    async def test_set_break_on_csp_violation_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="violation_types"):
            await domain.set_break_on_csp_violation(42)

    async def test_set_break_on_csp_violation_element_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(TypeError, match="violation_types elements"):
            await domain.set_break_on_csp_violation([42])

    async def test_set_break_on_csp_violation_invalid_enum_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="invalid value"):
            await domain.set_break_on_csp_violation(["trustedtype-sink-violation", "invalid"])

    async def test_set_break_on_csp_violation_all_invalid_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="invalid value"):
            await domain.set_break_on_csp_violation(["not-a-real-type"])

    async def test_set_break_on_csp_violation_empty_string_element_raises(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        with pytest.raises(ValueError, match="invalid value"):
            await domain.set_break_on_csp_violation([""])
