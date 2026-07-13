"""Unit tests for the Console domain.

Covers all 3 Console commands (clearMessages, disable, enable) with
FakeSender — parameterless methods, return values, call sequences,
exact CDP method names, params None vs empty dict, CommandError
propagation, and edge cases.
"""

import inspect
from typing import Any

import pytest

from cdpwave.domains.console import ConsoleDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message
        self._calls: list[tuple[str, dict[str, Any] | None]] = []

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._calls.append((method, params))
        raise CommandError(self._code, self._message)

    @property
    def calls(self) -> list[tuple[str, dict[str, Any] | None]]:
        return self._calls

    @property
    def last_call(self) -> tuple[str, dict[str, Any] | None]:
        return self._calls[-1]


@pytest.mark.unit
class TestConsoleClearMessages:
    async def test_clear_messages_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        assert fake.last_call == ("Console.clearMessages", None)

    async def test_clear_messages_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        result = await domain.clear_messages()
        assert result == {}

    async def test_clear_messages_returns_response(self) -> None:
        fake = FakeSender({"status": "ok"})
        domain = ConsoleDomain(fake)
        result = await domain.clear_messages()
        assert result == {"status": "ok"}

    async def test_clear_messages_single_call(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        assert len(fake.calls) == 1

    async def test_clear_messages_params_is_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        _, params = fake.last_call
        assert params is None

    async def test_clear_messages_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        method, _ = fake.last_call
        assert method == "Console.clearMessages"

    async def test_clear_messages_called_three_times(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(3):
            await domain.clear_messages()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call == ("Console.clearMessages", None)


@pytest.mark.unit
class TestConsoleDisable:
    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Console.disable", None)

    async def test_disable_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_disable_returns_response(self) -> None:
        fake = FakeSender({"done": True})
        domain = ConsoleDomain(fake)
        result = await domain.disable()
        assert result == {"done": True}

    async def test_disable_single_call(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1

    async def test_disable_params_is_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    async def test_disable_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Console.disable"

    async def test_disable_called_three_times(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(3):
            await domain.disable()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call == ("Console.disable", None)


@pytest.mark.unit
class TestConsoleEnable:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Console.enable", None)

    async def test_enable_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_enable_returns_response(self) -> None:
        fake = FakeSender({"enabled": True})
        domain = ConsoleDomain(fake)
        result = await domain.enable()
        assert result == {"enabled": True}

    async def test_enable_single_call(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1

    async def test_enable_params_is_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_enable_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "Console.enable"

    async def test_enable_called_three_times(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(3):
            await domain.enable()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call == ("Console.enable", None)


@pytest.mark.unit
class TestConsoleMethodOrder:
    async def test_method_order_alphabetical(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        methods = [m for m in dir(domain) if not m.startswith("_")]
        idx_clear = methods.index("clear_messages")
        idx_disable = methods.index("disable")
        idx_enable = methods.index("enable")
        assert idx_clear < idx_disable < idx_enable

    async def test_all_three_methods_exist(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        assert hasattr(domain, "clear_messages")
        assert hasattr(domain, "disable")
        assert hasattr(domain, "enable")

    async def test_no_extra_methods(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        public_methods = {
            m for m in dir(domain) if not m.startswith("_")
        }
        expected = {"clear_messages", "disable", "enable"}
        assert public_methods == expected

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for method_name in ("clear_messages", "disable", "enable"):
            method = getattr(domain, method_name)
            assert inspect.iscoroutinefunction(method)


@pytest.mark.unit
class TestConsoleCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        await domain.clear_messages()
        await domain.disable()
        assert len(fake.calls) == 3
        assert fake.calls[0] == ("Console.enable", None)
        assert fake.calls[1] == ("Console.clearMessages", None)
        assert fake.calls[2] == ("Console.disable", None)

    async def test_repeated_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(3):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 6

    async def test_clear_without_enable(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        assert fake.last_call == ("Console.clearMessages", None)

    async def test_disable_without_enable(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Console.disable", None)

    async def test_interleaved_calls(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        await domain.clear_messages()
        await domain.enable()
        await domain.clear_messages()
        await domain.disable()
        assert len(fake.calls) == 5
        assert fake.calls[0] == ("Console.enable", None)
        assert fake.calls[1] == ("Console.clearMessages", None)
        assert fake.calls[2] == ("Console.enable", None)
        assert fake.calls[3] == ("Console.clearMessages", None)
        assert fake.calls[4] == ("Console.disable", None)

    async def test_only_clear_messages_repeated(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(5):
            await domain.clear_messages()
        assert len(fake.calls) == 5
        for call in fake.calls:
            assert call == ("Console.clearMessages", None)

    async def test_only_enable_repeated(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(5):
            await domain.enable()
        assert len(fake.calls) == 5
        for call in fake.calls:
            assert call == ("Console.enable", None)

    async def test_only_disable_repeated(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for _ in range(5):
            await domain.disable()
        assert len(fake.calls) == 5
        for call in fake.calls:
            assert call == ("Console.disable", None)


@pytest.mark.unit
class TestConsoleErrorPropagation:
    async def test_clear_messages_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Server error")
        domain = ConsoleDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.clear_messages()
        assert exc_info.value.code == -32000
        assert "Server error" in exc_info.value.message
        assert len(sender.calls) == 1

    async def test_disable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32602, message="Invalid params")
        domain = ConsoleDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -32602
        assert "Invalid params" in exc_info.value.message
        assert len(sender.calls) == 1

    async def test_enable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32601, message="Method not found")
        domain = ConsoleDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == -32601
        assert "Method not found" in exc_info.value.message
        assert len(sender.calls) == 1

    async def test_command_error_stops_execution(self) -> None:
        sender = ErrorSender(code=-32000, message="Failed")
        domain = ConsoleDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 2


@pytest.mark.unit
class TestConsoleEdgeCases:
    async def test_console_domain_is_basedomain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_methods_return_exact_response_object(self) -> None:
        fake = FakeSender({"key": "value"})
        domain = ConsoleDomain(fake)
        result = await domain.enable()
        assert result is fake._response

    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        r1 = await domain.enable()
        assert r1 == {}
        fake.set_response({"changed": True})
        r2 = await domain.disable()
        assert r2 == {"changed": True}

    async def test_mixed_error_and_success(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1
        error_sender = ErrorSender(code=-32000, message="Fail")
        domain_err = ConsoleDomain(error_sender)
        with pytest.raises(CommandError):
            await domain_err.enable()
        assert len(error_sender.calls) == 1

    async def test_method_signatures_no_required_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        for method_name in ("clear_messages", "disable", "enable"):
            sig = inspect.signature(getattr(domain, method_name))
            params = list(sig.parameters.values())
            for p in params:
                assert p.default is not inspect.Parameter.empty or p.kind in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                )

    async def test_large_response_dict(self) -> None:
        large = {f"key_{i}": f"value_{i}" for i in range(100)}
        fake = FakeSender(large)
        domain = ConsoleDomain(fake)
        result = await domain.enable()
        assert result == large
        assert len(result) == 100

    async def test_none_response_from_sender(self) -> None:
        class NoneSender:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                return None  # type: ignore[return-value]

        sender = NoneSender()
        domain = ConsoleDomain(sender)
        result = await domain.enable()
        assert result is None

    async def test_error_sender_records_call_before_raising(self) -> None:
        sender = ErrorSender(code=-32000, message="err")
        domain = ConsoleDomain(sender)
        with pytest.raises(CommandError):
            await domain.clear_messages()
        assert sender.calls[0] == ("Console.clearMessages", None)

    async def test_all_methods_same_domain_instance(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        await domain.clear_messages()
        await domain.disable()
        assert all(call[0].startswith("Console.") for call in fake.calls)

    async def test_concurrent_calls_isolated(self) -> None:
        import asyncio
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.clear_messages(),
        )
        assert len(fake.calls) == 3
        methods = {call[0] for call in fake.calls}
        assert methods == {"Console.enable", "Console.disable", "Console.clearMessages"}
