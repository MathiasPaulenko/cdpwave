"""Comprehensive edge-case unit tests for MediaDomain."""

import asyncio
import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.media import MediaDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestMediaDomainEdge:
    """Edge cases: return values, lifecycle, PDL order, error propagation."""

    # ── method order matches PDL ──

    async def test_method_order_matches_pdl(self) -> None:
        expected = ["enable", "disable"]
        actual = [
            name
            for name, value in MediaDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert actual == expected

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in MediaDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 2

    async def test_no_spurious_methods(self) -> None:
        assert not hasattr(MediaDomain, "get_player_properties")
        assert not hasattr(MediaDomain, "get_players")
        assert not hasattr(MediaDomain, "set_player_properties")
        assert not hasattr(MediaDomain, "create_player")
        assert not hasattr(MediaDomain, "remove_player")

    async def test_inherits_base_domain(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        for name in ("enable", "disable"):
            method = getattr(MediaDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    # ── return value passthrough ──

    async def test_enable_return_value(self) -> None:
        fake = FakeSender({"enabled": True})
        domain = MediaDomain(fake)
        result = await domain.enable()
        assert result == {"enabled": True}

    async def test_disable_return_value(self) -> None:
        fake = FakeSender({"disabled": True})
        domain = MediaDomain(fake)
        result = await domain.disable()
        assert result == {"disabled": True}

    async def test_enable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_disable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        result = await domain.disable()
        assert result == {}

    # ── params=None for no-param methods ──

    async def test_enable_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_disable_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    # ── exact CDP method names ──

    async def test_enable_exact_method(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "Media.enable"

    async def test_disable_exact_method(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Media.disable"

    # ── multiple calls ──

    async def test_multiple_enable_calls(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        await domain.enable()
        await domain.enable()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "Media.enable"

    async def test_multiple_disable_calls(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        await domain.disable()
        await domain.disable()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "Media.disable"

    # ── lifecycle: enable → disable ──

    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == "Media.enable"
        assert fake.calls[1][0] == "Media.disable"

    # ── repeated cycle (enable+disable × 3) ──

    async def test_repeated_enable_disable_cycle(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        for _ in range(3):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 6
        for i in range(3):
            assert fake.calls[i * 2][0] == "Media.enable"
            assert fake.calls[i * 2 + 1][0] == "Media.disable"

    # ── disable without enable ──

    async def test_disable_without_enable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("Media.disable", None)

    # ── double enable ──

    async def test_double_enable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        await domain.enable()
        assert len(fake.calls) == 2
        for call in fake.calls:
            assert call[0] == "Media.enable"

    # ── double disable ──

    async def test_double_disable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        await domain.disable()
        assert len(fake.calls) == 2
        for call in fake.calls:
            assert call[0] == "Media.disable"

    # ── enable then disable then enable again ──

    async def test_enable_disable_enable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.enable()
        assert len(fake.calls) == 3
        assert fake.calls[0] == ("Media.enable", None)
        assert fake.calls[1] == ("Media.disable", None)
        assert fake.calls[2] == ("Media.enable", None)

    # ── concurrency ──

    async def test_concurrent_enable_calls(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.enable(),
            domain.enable(),
        )
        assert len(fake.calls) == 3

    async def test_concurrent_disable_calls(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.disable(),
            domain.disable(),
        )
        assert len(fake.calls) == 3

    async def test_concurrent_mixed_methods(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.enable(),
            domain.disable(),
        )
        assert len(fake.calls) == 4

    # ── error propagation ──

    async def test_enable_propagates_error(self) -> None:
        class ErrorSender:
            def __init__(self) -> None:
                self._calls: list[tuple[str, dict[str, object] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, object] | None = None,
            ) -> dict[str, object]:
                self._calls.append((method, params))
                raise RuntimeError("CDP error")

            @property
            def calls(self) -> list[tuple[str, dict[str, object] | None]]:
                return self._calls

        sender = ErrorSender()
        domain = MediaDomain(sender)
        with pytest.raises(RuntimeError, match="CDP error"):
            await domain.enable()

    async def test_disable_propagates_error(self) -> None:
        class ErrorSender:
            def __init__(self) -> None:
                self._calls: list[tuple[str, dict[str, object] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, object] | None = None,
            ) -> dict[str, object]:
                self._calls.append((method, params))
                raise RuntimeError("CDP error")

            @property
            def calls(self) -> list[tuple[str, dict[str, object] | None]]:
                return self._calls

        sender = ErrorSender()
        domain = MediaDomain(sender)
        with pytest.raises(RuntimeError, match="CDP error"):
            await domain.disable()

    # ── docstring tests ──

    async def test_class_docstring_experimental(self) -> None:
        doc = MediaDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_has_events(self) -> None:
        doc = MediaDomain.__doc__
        assert doc is not None
        assert "playerPropertiesChanged" in doc
        assert "playerEventsAdded" in doc
        assert "playerMessagesLogged" in doc
        assert "playerErrorsRaised" in doc
        assert "playerCreated" in doc

    async def test_class_docstring_has_commands(self) -> None:
        doc = MediaDomain.__doc__
        assert doc is not None
        assert "enable" in doc
        assert "disable" in doc

    async def test_module_docstring_experimental(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_module_docstring_has_types(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "PlayerId" in doc
        assert "Timestamp" in doc
        assert "PlayerMessage" in doc
        assert "PlayerProperty" in doc
        assert "PlayerEvent" in doc
        assert "PlayerErrorSourceLocation" in doc
        assert "PlayerError" in doc
        assert "Player" in doc

    async def test_module_docstring_has_events(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "playerPropertiesChanged" in doc
        assert "playerEventsAdded" in doc
        assert "playerMessagesLogged" in doc
        assert "playerErrorsRaised" in doc
        assert "playerCreated" in doc

    async def test_module_docstring_has_commands(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "enable" in doc
        assert "disable" in doc

    async def test_module_docstring_player_id_description(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "unique within the agent context" in doc

    async def test_module_docstring_player_error_fields(self) -> None:
        import cdpwave.domains.media as mod
        doc = mod.__doc__
        assert doc is not None
        assert "errorType" in doc
        assert "code" in doc
        assert "stack" in doc
        assert "cause" in doc

    async def test_enable_docstring_no_activates(self) -> None:
        doc = MediaDomain.enable.__doc__
        assert doc is not None
        assert "Activates" not in doc
        assert "Must be called" not in doc

    async def test_disable_docstring_no_deactivates(self) -> None:
        doc = MediaDomain.disable.__doc__
        assert doc is not None
        assert "Deactivates" not in doc

    async def test_enable_docstring_has_returns(self) -> None:
        doc = MediaDomain.enable.__doc__
        assert doc is not None
        assert "Returns:" in doc

    async def test_disable_docstring_has_returns(self) -> None:
        doc = MediaDomain.disable.__doc__
        assert doc is not None
        assert "Returns:" in doc

    # ── signature tests ──

    async def test_enable_signature(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        sig = inspect.signature(domain.enable)
        assert len(sig.parameters) == 0

    async def test_disable_signature(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        sig = inspect.signature(domain.disable)
        assert len(sig.parameters) == 0

