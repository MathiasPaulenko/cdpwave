"""Unit tests for the Performance domain.

Covers all 4 CDP Performance commands (disable, enable, getMetrics,
setTimeDomain) with FakeSender — parameter verification, omitempty
behavior, return values, CommandError propagation, method parity,
coroutine checks, concurrency, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.performance import PerformanceDomain
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


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Performance.disable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = PerformanceDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Performance.disable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_params_none_without_time_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Performance.enable", None)

    async def test_params_with_time_ticks(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        method, params = fake.last_call
        assert method == "Performance.enable"
        assert params is not None
        assert params["timeDomain"] == "timeTicks"

    async def test_params_with_thread_ticks(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="threadTicks")
        _, params = fake.last_call
        assert params is not None
        assert params["timeDomain"] == "threadTicks"

    async def test_omitempty_empty_time_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="")
        _, params = fake.last_call
        assert params is None

    async def test_omitempty_none_time_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain=None)
        _, params = fake.last_call
        assert params is None

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = PerformanceDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "Performance.enable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict_without_param(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# get_metrics
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetMetrics:
    async def test_params_none(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.get_metrics()
        assert fake.last_call == ("Performance.getMetrics", None)

    async def test_returns_metrics_list(self) -> None:
        fake = FakeSender({
            "metrics": [
                {"name": "JSHeapUsedSize", "value": 1000000},
                {"name": "Nodes", "value": 500},
            ],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert "metrics" in result
        assert isinstance(result["metrics"], list)
        assert len(result["metrics"]) == 2
        assert result["metrics"][0]["name"] == "JSHeapUsedSize"
        assert result["metrics"][0]["value"] == 1000000
        assert result["metrics"][1]["name"] == "Nodes"

    async def test_returns_empty_metrics(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"] == []

    async def test_returns_response(self) -> None:
        fake = FakeSender({"metrics": [{"name": "Test", "value": 1.5}]})
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["value"] == 1.5

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.get_metrics()
        method, _ = fake.last_call
        assert method == "Performance.getMetrics"

    async def test_single_call(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.get_metrics()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.get_metrics()
        _, params = fake.last_call
        assert params is None

    async def test_float_value(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "LayoutCount", "value": 3.14}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert isinstance(result["metrics"][0]["value"], (int, float))

    async def test_large_metrics_list(self) -> None:
        metrics = [{"name": f"M{i}", "value": float(i)} for i in range(100)]
        fake = FakeSender({"metrics": metrics})
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert len(result["metrics"]) == 100


# ---------------------------------------------------------------------------
# set_time_domain
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetTimeDomain:
    async def test_params_with_time_ticks(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        method, params = fake.last_call
        assert method == "Performance.setTimeDomain"
        assert params is not None
        assert params["timeDomain"] == "timeTicks"

    async def test_params_with_thread_ticks(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("threadTicks")
        _, params = fake.last_call
        assert params is not None
        assert params["timeDomain"] == "threadTicks"

    async def test_params_empty_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("")
        assert len(fake.calls) == 0

    async def test_unicode_string(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        _, params = fake.last_call
        assert params is not None
        assert params["timeDomain"] == "timeTicks"

    async def test_special_chars_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("time!@#$%^&*()Ticks")
        assert len(fake.calls) == 0

    async def test_long_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        value = "a" * 10000
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain(value)
        assert len(fake.calls) == 0

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        result = await domain.set_time_domain("timeTicks")
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = PerformanceDomain(fake)
        result = await domain.set_time_domain("timeTicks")
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        method, _ = fake.last_call
        assert method == "Performance.setTimeDomain"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        assert len(fake.calls) == 1


# ---------------------------------------------------------------------------
# Method parity
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    def test_four_methods_exist(self) -> None:
        methods = [
            attr for attr in dir(PerformanceDomain)
            if not attr.startswith("_") and callable(getattr(PerformanceDomain, attr))
        ]
        assert "disable" in methods
        assert "enable" in methods
        assert "get_metrics" in methods
        assert "set_time_domain" in methods

    def test_no_extra_methods(self) -> None:
        expected = {"disable", "enable", "get_metrics", "set_time_domain"}
        actual = {
            attr for attr in dir(PerformanceDomain)
            if not attr.startswith("_")
            and callable(getattr(PerformanceDomain, attr))
        }
        # BaseDomain contributes _call, _send which are filtered by _
        # Only check our domain methods
        domain_methods = actual - set(dir(BaseDomain))
        assert domain_methods == expected

    def test_all_coroutines(self) -> None:
        for name in ("disable", "enable", "get_metrics", "set_time_domain"):
            method = getattr(PerformanceDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_isinstance_base_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        assert isinstance(domain, BaseDomain)

    def test_alphabetical_order(self) -> None:
        methods = [
            name for name in dir(PerformanceDomain)
            if not name.startswith("_")
            and inspect.iscoroutinefunction(getattr(PerformanceDomain, name))
        ]
        assert methods == sorted(methods)

    def test_enable_accepts_optional_time_domain(self) -> None:
        sig = inspect.signature(PerformanceDomain.enable)
        assert "time_domain" in sig.parameters
        param = sig.parameters["time_domain"]
        assert param.default is None

    def test_set_time_domain_requires_time_domain(self) -> None:
        sig = inspect.signature(PerformanceDomain.set_time_domain)
        assert "time_domain" in sig.parameters
        param = sig.parameters["time_domain"]
        assert param.default is inspect.Parameter.empty


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagation:
    async def test_disable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Disable failed")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -32000
        assert "Disable failed" in exc_info.value.message

    async def test_enable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Enable failed")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == -32001
        assert "Enable failed" in exc_info.value.message

    async def test_get_metrics_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32002, message="GetMetrics failed")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.get_metrics()
        assert exc_info.value.code == -32002
        assert "GetMetrics failed" in exc_info.value.message

    async def test_set_time_domain_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32003, message="SetTimeDomain failed")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.set_time_domain("timeTicks")
        assert exc_info.value.code == -32003
        assert "SetTimeDomain failed" in exc_info.value.message

    async def test_error_sender_records_call_before_raising(self) -> None:
        sender = ErrorSender()
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 1
        assert sender.calls[0][0] == "Performance.disable"

    async def test_error_stops_execution(self) -> None:
        sender = ErrorSender()
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 2


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_100_concurrent_calls(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await asyncio.gather(*[domain.get_metrics() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_concurrent_mixed_methods(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.enable(),
            domain.enable(time_domain="timeTicks"),
            domain.set_time_domain("timeTicks"),
        )
        assert len(fake.calls) == 4

    async def test_concurrent_same_method_enable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(*[domain.enable() for _ in range(50)])
        assert len(fake.calls) == 50


# ---------------------------------------------------------------------------
# Repetition
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRepetition:
    async def test_enable_disable_10x(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        for _ in range(10):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 20
        for i in range(10):
            assert fake.calls[i * 2][0] == "Performance.enable"
            assert fake.calls[i * 2 + 1][0] == "Performance.disable"

    async def test_repeated_enable_10x(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        for _ in range(10):
            await domain.enable()
        assert len(fake.calls) == 10

    async def test_repeated_set_time_domain_10x(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        for _ in range(10):
            await domain.set_time_domain("timeTicks")
        assert len(fake.calls) == 10

    async def test_repeated_get_metrics_10x(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        for _ in range(10):
            await domain.get_metrics()
        assert len(fake.calls) == 10


# ---------------------------------------------------------------------------
# Call sequences
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.enable()
        await domain.get_metrics()
        await domain.set_time_domain("timeTicks")
        await domain.disable()
        assert len(fake.calls) == 4
        assert fake.calls[0][0] == "Performance.enable"
        assert fake.calls[1][0] == "Performance.getMetrics"
        assert fake.calls[2][0] == "Performance.setTimeDomain"
        assert fake.calls[3][0] == "Performance.disable"

    async def test_all_methods_use_performance_prefix(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.disable()
        await domain.enable()
        await domain.get_metrics()
        await domain.set_time_domain("timeTicks")
        for method, _ in fake.calls:
            assert method.startswith("Performance.")

    async def test_interleaved_calls(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await domain.enable()
        await domain.get_metrics()
        await domain.disable()
        await domain.enable(time_domain="timeTicks")
        await domain.get_metrics()
        await domain.set_time_domain("threadTicks")
        await domain.disable()
        assert len(fake.calls) == 7


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        r1 = await domain.enable()
        assert r1 == {}
        fake.set_response({"ok": True})
        r2 = await domain.enable()
        assert r2 == {"ok": True}

    async def test_large_response_dict(self) -> None:
        large = {f"key{i}": i for i in range(100)}
        fake = FakeSender(large)
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result == large

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
                return {}

        sender = NoneSender()
        domain = PerformanceDomain(sender)
        result = await domain.disable()
        assert result == {}

    async def test_mixed_error_success(self) -> None:
        class MixedSender:
            def __init__(self) -> None:
                self._count = 0
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                self._count += 1
                if self._count % 2 == 0:
                    raise CommandError(-1, "even call error")
                return {"ok": True}

        sender = MixedSender()
        domain = PerformanceDomain(sender)
        r1 = await domain.enable()
        assert r1 == {"ok": True}
        with pytest.raises(CommandError):
            await domain.enable()
        assert len(sender.calls) == 2

    async def test_enable_with_time_domain_then_without(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        await domain.enable()
        assert fake.calls[0][1] == {"timeDomain": "timeTicks"}
        assert fake.calls[1][1] is None

    async def test_set_time_domain_preserves_exact_value(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        test_value = "timeTicks"
        await domain.set_time_domain(test_value)
        _, params = fake.last_call
        assert params is not None
        assert params["timeDomain"] == test_value

    async def test_exact_response_object(self) -> None:
        response = {"metrics": [{"name": "X", "value": 1}]}
        fake = FakeSender(response)
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result is response

    async def test_params_not_mutated_between_calls(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        await domain.enable(time_domain="threadTicks")
        assert fake.calls[0][1] == {"timeDomain": "timeTicks"}
        assert fake.calls[1][1] == {"timeDomain": "threadTicks"}


# ---------------------------------------------------------------------------
# Edge cases — extended
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCasesExtended:
    async def test_set_time_domain_none_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(None)

    async def test_set_time_domain_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(123)

    async def test_set_time_domain_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(["timeTicks"])

    async def test_set_time_domain_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain({"timeDomain": "timeTicks"})

    async def test_set_time_domain_bool_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(True)

    async def test_set_time_domain_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(3.14)

    async def test_set_time_domain_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(b"timeTicks")

    async def test_set_time_domain_type_error_no_call_to_sender(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_time_domain(None)
        assert len(fake.calls) == 0

    async def test_enable_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=123)

    async def test_enable_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=3.14)

    async def test_enable_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=["timeTicks"])

    async def test_enable_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain={"timeDomain": "timeTicks"})

    async def test_enable_bool_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=True)

    async def test_enable_false_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=False)

    async def test_enable_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=b"timeTicks")

    async def test_enable_zero_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=0)

    async def test_enable_type_error_no_call_to_sender(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError):
            await domain.enable(time_domain=123)
        assert len(fake.calls) == 0

    async def test_enable_none_does_not_raise(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain=None)
        _, params = fake.last_call
        assert params is None

    async def test_enable_empty_string_does_not_raise(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="")
        _, params = fake.last_call
        assert params is None

    async def test_enable_whitespace_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain=" ")
        assert len(fake.calls) == 0

    async def test_enable_newline_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="timeTicks\n")
        assert len(fake.calls) == 0

    async def test_enable_tab_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="\ttimeTicks")
        assert len(fake.calls) == 0

    async def test_enable_unicode_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="timeTicks\u00f1\u4e2d")
        assert len(fake.calls) == 0

    async def test_enable_long_invalid_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="timeTicks" * 1000)
        assert len(fake.calls) == 0

    async def test_enable_string_zero_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="0")
        assert len(fake.calls) == 0

    async def test_enable_string_false_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="False")
        assert len(fake.calls) == 0

    async def test_enable_string_none_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="None")
        assert len(fake.calls) == 0

    async def test_enable_invalid_value_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.enable(time_domain="wallTime")
        assert len(fake.calls) == 0

    async def test_set_time_domain_invalid_value_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("wallTime")
        assert len(fake.calls) == 0

    async def test_set_time_domain_empty_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("")
        assert len(fake.calls) == 0

    async def test_set_time_domain_random_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("abc")
        assert len(fake.calls) == 0

    async def test_set_time_domain_type_error_takes_precedence_over_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string"):
            await domain.set_time_domain(123)
        assert len(fake.calls) == 0

    async def test_enable_type_error_takes_precedence_over_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError, match="time_domain must be a string or None"):
            await domain.enable(time_domain=123)
        assert len(fake.calls) == 0

    async def test_enable_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        first_params = fake.calls[0][1]
        await domain.enable(time_domain="timeTicks")
        second_params = fake.calls[1][1]
        assert first_params is not None
        assert second_params is not None
        assert first_params is not second_params
        assert first_params == second_params

    async def test_set_time_domain_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        first_params = fake.calls[0][1]
        await domain.set_time_domain("timeTicks")
        second_params = fake.calls[1][1]
        assert first_params is not None
        assert second_params is not None
        assert first_params is not second_params
        assert first_params == second_params

    async def test_enable_camel_case_key(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        _, params = fake.last_call
        assert params is not None
        assert "timeDomain" in params
        assert "time_domain" not in params

    async def test_set_time_domain_camel_case_key(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        _, params = fake.last_call
        assert params is not None
        assert "timeDomain" in params
        assert "time_domain" not in params

    async def test_get_metrics_negative_values(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "NegativeMetric", "value": -42.5}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["value"] == -42.5

    async def test_get_metrics_zero_value(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "ZeroMetric", "value": 0}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["value"] == 0

    async def test_get_metrics_large_value(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "LargeMetric", "value": 1e15}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["value"] == 1e15

    async def test_get_metrics_extra_keys_in_response(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "M", "value": 1}],
            "extra": "ignored",
            "count": 42,
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert "metrics" in result
        assert "extra" in result
        assert result["extra"] == "ignored"

    async def test_get_metrics_none_value_in_metric(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "M", "value": None}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["value"] is None

    async def test_get_metrics_empty_name(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "", "value": 1.0}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["name"] == ""

    async def test_get_metrics_extra_keys_in_metric(self) -> None:
        fake = FakeSender({
            "metrics": [{"name": "M", "value": 1, "extra": "yes"}],
        })
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert result["metrics"][0]["extra"] == "yes"

    async def test_disable_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data", "count": 5})
        domain = PerformanceDomain(fake)
        result = await domain.disable()
        assert result["extra"] == "data"
        assert result["count"] == 5

    async def test_enable_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = PerformanceDomain(fake)
        result = await domain.enable()
        assert result["extra"] == "data"

    async def test_set_time_domain_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = PerformanceDomain(fake)
        result = await domain.set_time_domain("timeTicks")
        assert result["extra"] == "data"

    async def test_set_time_domain_whitespace_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain(" ")
        assert len(fake.calls) == 0

    async def test_set_time_domain_newline_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(ValueError, match="time_domain must be 'timeTicks' or 'threadTicks'"):
            await domain.set_time_domain("\n")
        assert len(fake.calls) == 0

    async def test_set_time_domain_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["timeDomain"]

    async def test_enable_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable(time_domain="timeTicks")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["timeDomain"]

    async def test_domain_works_with_custom_sender(self) -> None:
        class CustomSender:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                return {"custom": True}

        sender = CustomSender()
        domain = PerformanceDomain(sender)
        result = await domain.disable()
        assert result == {"custom": True}
        assert len(sender.calls) == 1


# ---------------------------------------------------------------------------
# Extended concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrencyExtended:
    async def test_100_concurrent_set_time_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(
            *[domain.set_time_domain("timeTicks") for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_100_concurrent_disable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(*[domain.disable() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_100_concurrent_enable_with_param(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(
            *[domain.enable(time_domain="timeTicks") for _ in range(100)],
        )
        assert len(fake.calls) == 100
        for _, params in fake.calls:
            assert params == {"timeDomain": "timeTicks"}

    async def test_concurrent_all_four_methods(self) -> None:
        fake = FakeSender({"metrics": []})
        domain = PerformanceDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.enable(),
            domain.enable(time_domain="timeTicks"),
            domain.get_metrics(),
            domain.set_time_domain("timeTicks"),
        )
        assert len(fake.calls) == 5

    async def test_concurrent_50_enable_50_disable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await asyncio.gather(
            *[domain.enable() for _ in range(50)],
            *[domain.disable() for _ in range(50)],
        )
        assert len(fake.calls) == 100


# ---------------------------------------------------------------------------
# Extended error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagationExtended:
    async def test_error_with_positive_code(self) -> None:
        sender = ErrorSender(code=100, message="Positive code")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == 100

    async def test_error_with_zero_code(self) -> None:
        sender = ErrorSender(code=0, message="Zero code")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == 0

    async def test_error_with_empty_message(self) -> None:
        sender = ErrorSender(code=-1, message="")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.get_metrics()
        assert exc_info.value.message == ""

    async def test_error_with_long_message(self) -> None:
        msg = "x" * 10000
        sender = ErrorSender(code=-1, message=msg)
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.set_time_domain("timeTicks")
        assert exc_info.value.message == msg

    async def test_error_with_unicode_message(self) -> None:
        sender = ErrorSender(code=-1, message="Error \u00f1\u4e2d")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert "\u00f1" in exc_info.value.message

    async def test_error_propagation_preserves_code_and_message(self) -> None:
        sender = ErrorSender(code=-42, message="Custom error")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -42
        assert exc_info.value.message == "Custom error"
        assert str(exc_info.value) == "[-42] Custom error"

    async def test_error_enable_with_time_domain(self) -> None:
        sender = ErrorSender(code=-1, message="Enable failed")
        domain = PerformanceDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable(time_domain="timeTicks")

    async def test_error_does_not_swallow_type_error(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_time_domain(None)
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Extended method parity
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParityExtended:
    def test_exactly_four_public_methods(self) -> None:
        public_methods = {
            name for name in dir(PerformanceDomain)
            if not name.startswith("_")
            and inspect.iscoroutinefunction(getattr(PerformanceDomain, name))
        }
        assert len(public_methods) == 4
        assert public_methods == {"disable", "enable", "get_metrics", "set_time_domain"}

    def test_no_sync_methods(self) -> None:
        for name in ("disable", "enable", "get_metrics", "set_time_domain"):
            method = getattr(PerformanceDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be async"

    def test_enable_signature(self) -> None:
        sig = inspect.signature(PerformanceDomain.enable)
        params = list(sig.parameters.keys())
        assert params == ["self", "time_domain"]
        assert sig.parameters["time_domain"].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert sig.return_annotation == dict[str, Any]

    def test_disable_signature(self) -> None:
        sig = inspect.signature(PerformanceDomain.disable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_get_metrics_signature(self) -> None:
        sig = inspect.signature(PerformanceDomain.get_metrics)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_set_time_domain_signature(self) -> None:
        sig = inspect.signature(PerformanceDomain.set_time_domain)
        params = list(sig.parameters.keys())
        assert params == ["self", "time_domain"]
        assert sig.parameters["time_domain"].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert sig.parameters["time_domain"].annotation is str
        assert sig.return_annotation == dict[str, Any]

    def test_all_methods_have_docstrings(self) -> None:
        for name in ("disable", "enable", "get_metrics", "set_time_domain"):
            method = getattr(PerformanceDomain, name)
            assert method.__doc__ is not None, f"{name} missing docstring"
            assert len(method.__doc__) > 10, f"{name} docstring too short"

    def test_class_has_docstring(self) -> None:
        assert PerformanceDomain.__doc__ is not None
        assert "Performance" in PerformanceDomain.__doc__

    def test_module_has_docstring(self) -> None:
        import cdpwave.domains.performance as perf_mod
        assert perf_mod.__doc__ is not None
        assert "Performance.metrics" in perf_mod.__doc__

    def test_module_docstring_mentions_event(self) -> None:
        import cdpwave.domains.performance as perf_mod
        assert "Performance.metrics" in (perf_mod.__doc__ or "")

    def test_class_docstring_mentions_event(self) -> None:
        assert "Performance.metrics" in (PerformanceDomain.__doc__ or "")
