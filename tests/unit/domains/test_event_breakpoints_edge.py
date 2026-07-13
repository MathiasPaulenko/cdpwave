"""Edge case unit tests for the EventBreakpoints domain."""

import pytest

from cdpwave.domains.event_breakpoints import EventBreakpointsDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestEventBreakpointsEdgeCases:
    async def test_set_instrumentation_breakpoint_empty_string(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("")
        method, params = fake.last_call
        assert method == "EventBreakpoints.setInstrumentationBreakpoint"
        assert params == {"eventName": ""}

    async def test_remove_instrumentation_breakpoint_empty_string(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.remove_instrumentation_breakpoint("")
        method, params = fake.last_call
        assert method == "EventBreakpoints.removeInstrumentationBreakpoint"
        assert params == {"eventName": ""}

    async def test_set_instrumentation_breakpoint_unicode(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement🔑")
        method, params = fake.last_call
        assert params == {"eventName": "scriptFirstStatement🔑"}

    async def test_set_instrumentation_breakpoint_long_name(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        long_name = "A" * 10000
        await domain.set_instrumentation_breakpoint(long_name)
        method, params = fake.last_call
        assert params == {"eventName": long_name}

    async def test_set_instrumentation_breakpoint_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(b"scriptFirstStatement")

    async def test_remove_instrumentation_breakpoint_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint(b"scriptFirstStatement")

    async def test_set_instrumentation_breakpoint_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint({"name": "test"})

    async def test_remove_instrumentation_breakpoint_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.remove_instrumentation_breakpoint({"name": "test"})

    async def test_set_instrumentation_breakpoint_float_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.set_instrumentation_breakpoint(3.14)

    async def test_clear_alias_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.clear_instrumentation_breakpoint(b"scriptFirstStatement")

    async def test_clear_alias_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.clear_instrumentation_breakpoint({"name": "test"})

    async def test_clear_alias_float_raises(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        with pytest.raises(TypeError, match="event_name must be a string"):
            await domain.clear_instrumentation_breakpoint(3.14)

    async def test_clear_alias_delegates_to_remove(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.clear_instrumentation_breakpoint("scriptFirstStatement")
        method, params = fake.last_call
        assert method == "EventBreakpoints.removeInstrumentationBreakpoint"
        assert params == {"eventName": "scriptFirstStatement"}

    async def test_clear_alias_no_direct_call(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.clear_instrumentation_breakpoint("scriptFirstStatement")
        assert len(fake.calls) == 1
        assert fake.calls[0][0] == "EventBreakpoints.removeInstrumentationBreakpoint"

    async def test_return_value_passthrough_set(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = EventBreakpointsDomain(fake)
        result = await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_remove(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = EventBreakpointsDomain(fake)
        result = await domain.remove_instrumentation_breakpoint("scriptFirstStatement")
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_disable(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = EventBreakpointsDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        await domain.remove_instrumentation_breakpoint("scriptFirstStatement")
        await domain.disable()
        assert len(fake.calls) == 3
        assert fake.calls[0] == (
            "EventBreakpoints.setInstrumentationBreakpoint",
            {"eventName": "scriptFirstStatement"},
        )
        assert fake.calls[1] == (
            "EventBreakpoints.removeInstrumentationBreakpoint",
            {"eventName": "scriptFirstStatement"},
        )
        assert fake.calls[2] == (
            "EventBreakpoints.disable",
            None,
        )

    async def test_set_same_breakpoint_twice(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        assert len(fake.calls) == 2
        assert fake.calls[0] == fake.calls[1]

    async def test_remove_without_set(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.remove_instrumentation_breakpoint("scriptFirstStatement")
        assert len(fake.calls) == 1
        assert fake.calls[0][0] == "EventBreakpoints.removeInstrumentationBreakpoint"

    async def test_disable_without_any_breakpoints(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("EventBreakpoints.disable", None)

    async def test_set_multiple_different_breakpoints(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        events = ["scriptFirstStatement", "cancelAnimationFrame", "requestAnimationFrame"]
        for event in events:
            await domain.set_instrumentation_breakpoint(event)
        assert len(fake.calls) == 3
        for i, event in enumerate(events):
            assert fake.calls[i][1] == {"eventName": event}

    async def test_full_lifecycle_set_remove_disable(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        await domain.set_instrumentation_breakpoint("cancelAnimationFrame")
        await domain.remove_instrumentation_breakpoint("scriptFirstStatement")
        await domain.disable()
        await domain.remove_instrumentation_breakpoint("cancelAnimationFrame")
        assert len(fake.calls) == 5
        assert fake.calls[3] == ("EventBreakpoints.disable", None)

    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "EventBreakpoints.disable"
        assert params is None

    async def test_no_enable_method_exists(self) -> None:
        assert not hasattr(EventBreakpointsDomain, "enable")

    async def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(EventBreakpointsDomain)
            if not name.startswith("_") and callable(getattr(EventBreakpointsDomain, name))
        }
        assert public_methods == {
            "set_instrumentation_breakpoint",
            "remove_instrumentation_breakpoint",
            "clear_instrumentation_breakpoint",
            "disable",
        }

    async def test_order_matches_pdl(self) -> None:
        methods = [
            name for name in EventBreakpointsDomain.__dict__
            if not name.startswith("_") and callable(EventBreakpointsDomain.__dict__[name])
        ]
        assert methods.index("set_instrumentation_breakpoint") < (
            methods.index("remove_instrumentation_breakpoint")
        )
        assert methods.index("remove_instrumentation_breakpoint") < methods.index("disable")

    async def test_set_instrumentation_breakpoint_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint(MyStr("scriptFirstStatement"))
        method, params = fake.last_call
        assert params == {"eventName": "scriptFirstStatement"}
