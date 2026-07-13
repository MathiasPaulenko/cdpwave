"""Unit tests for type validation in Inspector domain.

Inspector has only no-param commands (enable, disable), so there are
no type validation tests. This file exists for completeness and to
verify the commands send correctly.
"""

import pytest

from cdpwave.domains.inspector import InspectorDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestInspectorValidation:
    async def test_disable_sends_no_params(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "Inspector.disable"
        assert params is None

    async def test_enable_sends_no_params(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "Inspector.enable"
        assert params is None

    async def test_disable_then_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        await domain.enable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("Inspector.disable", None)
        assert fake.calls[1] == ("Inspector.enable", None)
