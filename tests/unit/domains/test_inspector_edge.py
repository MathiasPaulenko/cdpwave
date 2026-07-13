"""Edge case unit tests for the Inspector domain."""

import pytest

from cdpwave.domains.inspector import InspectorDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestInspectorEdgeCases:
    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "Inspector.disable"
        assert params is None

    async def test_enable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "Inspector.enable"
        assert params is None

    async def test_return_value_passthrough_disable(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = InspectorDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_enable(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = InspectorDomain(fake)
        result = await domain.enable()
        assert result == {"result": "ok"}

    async def test_multiple_enable_disable_cycles(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("Inspector.enable", None)
            assert fake.calls[i * 2 + 1] == ("Inspector.disable", None)

    async def test_enable_when_already_enabled(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        await domain.enable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("Inspector.enable", None)
        assert fake.calls[1] == ("Inspector.enable", None)

    async def test_disable_when_already_disabled(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        await domain.disable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("Inspector.disable", None)
        assert fake.calls[1] == ("Inspector.disable", None)

    async def test_enable_only_no_disable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("Inspector.enable", None)

    async def test_disable_only_no_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("Inspector.disable", None)

    async def test_order_matches_pdl_disable_before_enable(self) -> None:
        methods = [
            name for name in InspectorDomain.__dict__
            if not name.startswith("_") and callable(InspectorDomain.__dict__[name])
        ]
        assert methods.index("disable") < methods.index("enable")

    async def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(InspectorDomain)
            if not name.startswith("_") and callable(getattr(InspectorDomain, name))
        }
        assert public_methods == {"disable", "enable"}

    async def test_enable_then_disable_then_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.enable()
        assert len(fake.calls) == 3
        assert fake.calls[0] == ("Inspector.enable", None)
        assert fake.calls[1] == ("Inspector.disable", None)
        assert fake.calls[2] == ("Inspector.enable", None)
