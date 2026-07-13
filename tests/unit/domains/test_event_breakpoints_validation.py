"""Unit tests for type validation in EventBreakpoints domain."""

import pytest

from cdpwave.domains.event_breakpoints import EventBreakpointsDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestEventBreakpointsTypeValidation:
    async def test_set_instrumentation_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(42)

    async def test_set_instrumentation_breakpoint_event_name_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(True)

    async def test_set_instrumentation_breakpoint_event_name_list_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(["scriptFirstStatement"])

    async def test_set_instrumentation_breakpoint_event_name_none_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(None)  # type: ignore[arg-type]

    async def test_remove_instrumentation_breakpoint_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint(42)

    async def test_remove_instrumentation_breakpoint_event_name_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint(True)

    async def test_remove_instrumentation_breakpoint_event_name_list_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint(["scriptFirstStatement"])

    async def test_remove_instrumentation_breakpoint_event_name_none_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint(None)  # type: ignore[arg-type]

    async def test_clear_instrumentation_breakpoint_alias_event_name_int_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.clear_instrumentation_breakpoint(42)

    async def test_set_instrumentation_breakpoint_valid_str(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        method, params = fake.last_call
        assert method == "EventBreakpoints.setInstrumentationBreakpoint"
        assert params == {"eventName": "scriptFirstStatement"}

    async def test_remove_instrumentation_breakpoint_valid_str(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.remove_instrumentation_breakpoint("scriptFirstStatement")
        method, params = fake.last_call
        assert method == "EventBreakpoints.removeInstrumentationBreakpoint"
        assert params == {"eventName": "scriptFirstStatement"}

    async def test_set_instrumentation_breakpoint_empty_str_accepted(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("")
        method, params = fake.last_call
        assert params == {"eventName": ""}

    async def test_disable_no_call_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_instrumentation_breakpoint(42)
        assert len(fake.calls) == 0
