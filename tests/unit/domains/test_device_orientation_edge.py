"""Comprehensive edge-case unit tests for DeviceOrientationDomain."""

import asyncio
import inspect
import math

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.device_orientation import DeviceOrientationDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDeviceOrientationDomainEdge:
    """Edge cases: type validation, return values, lifecycle, PDL order."""

    # ── method order matches PDL ──

    async def test_method_order_matches_pdl(self) -> None:
        expected = [
            "clear_device_orientation_override",
            "set_device_orientation_override",
        ]
        actual = [
            name
            for name, value in DeviceOrientationDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert actual == expected

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in DeviceOrientationDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 2

    async def test_no_spurious_methods(self) -> None:
        assert not hasattr(DeviceOrientationDomain, "set_orientation")
        assert not hasattr(DeviceOrientationDomain, "get_orientation")
        assert not hasattr(DeviceOrientationDomain, "enable")
        assert not hasattr(DeviceOrientationDomain, "disable")

    async def test_inherits_base_domain(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        for name in ("clear_device_orientation_override", "set_device_orientation_override"):
            method = getattr(DeviceOrientationDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    # ── type validation: alpha ──

    @pytest.mark.parametrize(
        "bad_value",
        [0, 42, -1, True, False, "1.0", None, {}, [], (1.0,), {1.0}, b"1.0", complex(1, 2)],
    )
    async def test_alpha_type_error(self, bad_value: object) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="alpha must be a float"):
            await domain.set_device_orientation_override(bad_value, 0.0, 0.0)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    # ── type validation: beta ──

    @pytest.mark.parametrize(
        "bad_value",
        [0, 42, -1, True, False, "1.0", None, {}, [], (1.0,), {1.0}, b"1.0", complex(1, 2)],
    )
    async def test_beta_type_error(self, bad_value: object) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="beta must be a float"):
            await domain.set_device_orientation_override(0.0, bad_value, 0.0)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    # ── type validation: gamma ──

    @pytest.mark.parametrize(
        "bad_value",
        [0, 42, -1, True, False, "1.0", None, {}, [], (1.0,), {1.0}, b"1.0", complex(1, 2)],
    )
    async def test_gamma_type_error(self, bad_value: object) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="gamma must be a float"):
            await domain.set_device_orientation_override(0.0, 0.0, bad_value)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    # ── type validation: alpha checked before beta ──

    async def test_alpha_checked_before_beta(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="alpha must be a float"):
            await domain.set_device_orientation_override("bad", "also_bad", 0.0)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_beta_checked_before_gamma(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="beta must be a float"):
            await domain.set_device_orientation_override(0.0, "bad", "also_bad")  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    # ── float subclass accepted ──

    async def test_float_subclass_accepted(self) -> None:
        class MyFloat(float):
            pass

        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(
            MyFloat(1.0), MyFloat(2.0), MyFloat(3.0)
        )
        method, params = fake.last_call
        assert method == "DeviceOrientation.setDeviceOrientationOverride"
        assert params is not None
        assert params["alpha"] == 1.0
        assert params["beta"] == 2.0
        assert params["gamma"] == 3.0

    # ── edge values ──

    @pytest.mark.parametrize(
        ("alpha", "beta", "gamma"),
        [
            (0.0, 0.0, 0.0),
            (360.0, 180.0, 90.0),
            (-180.0, -90.0, -90.0),
            (90.0, 45.0, -45.0),
            (359.99, 179.99, 89.99),
            (-0.0, -0.0, -0.0),
            (1e10, 1e10, 1e10),
            (-1e10, -1e10, -1e10),
            (float("nan"), 0.0, 0.0),
            (0.0, float("nan"), 0.0),
            (0.0, 0.0, float("nan")),
            (float("inf"), 0.0, 0.0),
            (0.0, float("inf"), 0.0),
            (0.0, 0.0, float("inf")),
            (float("-inf"), 0.0, 0.0),
            (0.0, float("-inf"), 0.0),
            (0.0, 0.0, float("-inf")),
        ],
    )
    async def test_edge_values(self, alpha: float, beta: float, gamma: float) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(alpha, beta, gamma)
        method, params = fake.last_call
        assert method == "DeviceOrientation.setDeviceOrientationOverride"
        assert params is not None
        if math.isnan(alpha):
            assert math.isnan(params["alpha"])
        else:
            assert params["alpha"] == alpha
        if math.isnan(beta):
            assert math.isnan(params["beta"])
        else:
            assert params["beta"] == beta
        if math.isnan(gamma):
            assert math.isnan(params["gamma"])
        else:
            assert params["gamma"] == gamma

    # ── return value passthrough ──

    async def test_set_return_value(self) -> None:
        fake = FakeSender({"status": "ok"})
        domain = DeviceOrientationDomain(fake)
        result = await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        assert result == {"status": "ok"}

    async def test_clear_return_value(self) -> None:
        fake = FakeSender({"cleared": True})
        domain = DeviceOrientationDomain(fake)
        result = await domain.clear_device_orientation_override()
        assert result == {"cleared": True}

    async def test_set_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        result = await domain.set_device_orientation_override(0.0, 0.0, 0.0)
        assert result == {}

    async def test_clear_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        result = await domain.clear_device_orientation_override()
        assert result == {}

    # ── clear sends params=None ──

    async def test_clear_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        _, params = fake.last_call
        assert params is None

    # ── exact param keys ──

    async def test_set_exact_keys(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"alpha", "beta", "gamma"}

    # ── multiple calls ──

    async def test_multiple_set_calls(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        await domain.set_device_orientation_override(4.0, 5.0, 6.0)
        await domain.set_device_orientation_override(7.0, 8.0, 9.0)
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "DeviceOrientation.setDeviceOrientationOverride"

    async def test_multiple_clear_calls(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        await domain.clear_device_orientation_override()
        await domain.clear_device_orientation_override()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "DeviceOrientation.clearDeviceOrientationOverride"

    # ── lifecycle: set → clear ──

    async def test_lifecycle_set_then_clear(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(0.0, 90.0, 0.0)
        await domain.clear_device_orientation_override()
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == "DeviceOrientation.setDeviceOrientationOverride"
        assert fake.calls[1][0] == "DeviceOrientation.clearDeviceOrientationOverride"

    # ── repeated cycle (set+clear × 3) ──

    async def test_repeated_cycle(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        for i in range(3):
            await domain.set_device_orientation_override(
                float(i), float(i * 10), float(i * 100)
            )
            await domain.clear_device_orientation_override()
        assert len(fake.calls) == 6
        for i in range(3):
            set_call = fake.calls[i * 2]
            clear_call = fake.calls[i * 2 + 1]
            assert set_call[0] == "DeviceOrientation.setDeviceOrientationOverride"
            assert clear_call[0] == "DeviceOrientation.clearDeviceOrientationOverride"
            assert set_call[1] is not None
            assert set_call[1]["alpha"] == float(i)
            assert clear_call[1] is None

    # ── clear without set (no prior set) ──

    async def test_clear_without_set(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("DeviceOrientation.clearDeviceOrientationOverride", None)

    # ── concurrency ──

    async def test_concurrent_set_calls(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await asyncio.gather(
            domain.set_device_orientation_override(1.0, 2.0, 3.0),
            domain.set_device_orientation_override(4.0, 5.0, 6.0),
            domain.set_device_orientation_override(7.0, 8.0, 9.0),
        )
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "DeviceOrientation.setDeviceOrientationOverride"

    async def test_concurrent_set_and_clear(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await asyncio.gather(
            domain.set_device_orientation_override(1.0, 2.0, 3.0),
            domain.clear_device_orientation_override(),
            domain.set_device_orientation_override(4.0, 5.0, 6.0),
        )
        assert len(fake.calls) == 3

    # ── docstring tests ──

    async def test_class_docstring_experimental(self) -> None:
        doc = DeviceOrientationDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_no_events(self) -> None:
        doc = DeviceOrientationDomain.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_module_docstring_experimental(self) -> None:
        import cdpwave.domains.device_orientation as mod
        doc = mod.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_module_docstring_no_events(self) -> None:
        import cdpwave.domains.device_orientation as mod
        doc = mod.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_set_docstring_has_raises(self) -> None:
        doc = DeviceOrientationDomain.set_device_orientation_override.__doc__
        assert doc is not None
        assert "Raises:" in doc
        assert "TypeError" in doc

    async def test_set_docstring_describes_alpha(self) -> None:
        doc = DeviceOrientationDomain.set_device_orientation_override.__doc__
        assert doc is not None
        assert "alpha" in doc
        assert "z-axis" in doc

    async def test_set_docstring_describes_beta(self) -> None:
        doc = DeviceOrientationDomain.set_device_orientation_override.__doc__
        assert doc is not None
        assert "beta" in doc
        assert "x-axis" in doc

    async def test_set_docstring_describes_gamma(self) -> None:
        doc = DeviceOrientationDomain.set_device_orientation_override.__doc__
        assert doc is not None
        assert "gamma" in doc
        assert "y-axis" in doc

    async def test_clear_docstring_has_returns(self) -> None:
        doc = DeviceOrientationDomain.clear_device_orientation_override.__doc__
        assert doc is not None
        assert "Returns:" in doc

    async def test_clear_docstring_describes_removal(self) -> None:
        doc = DeviceOrientationDomain.clear_device_orientation_override.__doc__
        assert doc is not None
        assert "override" in doc.lower()

    # ── signature tests ──

    async def test_set_signature(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        sig = inspect.signature(domain.set_device_orientation_override)
        params = list(sig.parameters.keys())
        assert params == ["alpha", "beta", "gamma"]

    async def test_clear_signature(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        sig = inspect.signature(domain.clear_device_orientation_override)
        params = list(sig.parameters.keys())
        assert params == []

    # ── error propagation ──

    async def test_set_propagates_error(self) -> None:
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
        domain = DeviceOrientationDomain(sender)
        with pytest.raises(RuntimeError, match="CDP error"):
            await domain.set_device_orientation_override(1.0, 2.0, 3.0)

    async def test_clear_propagates_error(self) -> None:
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
        domain = DeviceOrientationDomain(sender)
        with pytest.raises(RuntimeError, match="CDP error"):
            await domain.clear_device_orientation_override()

    # ── precision preservation ──

    async def test_precision_preserved(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        alpha = 1.234567890123456789
        beta = 9.876543210987654321
        gamma = 5.555555555555555555
        await domain.set_device_orientation_override(alpha, beta, gamma)
        _, params = fake.last_call
        assert params is not None
        assert params["alpha"] == alpha
        assert params["beta"] == beta
        assert params["gamma"] == gamma

    async def test_very_small_floats(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(
            1e-300, 1e-300, 1e-300
        )
        _, params = fake.last_call
        assert params is not None
        assert params["alpha"] == 1e-300

    async def test_very_large_floats(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(
            1e300, 1e300, 1e300
        )
        _, params = fake.last_call
        assert params is not None
        assert params["alpha"] == 1e300

    # ── set after clear ──

    async def test_set_after_clear(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == "DeviceOrientation.clearDeviceOrientationOverride"
        assert fake.calls[1][0] == "DeviceOrientation.setDeviceOrientationOverride"

    # ── double set (override the override) ──

    async def test_double_set(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        await domain.set_device_orientation_override(4.0, 5.0, 6.0)
        assert len(fake.calls) == 2
        assert fake.calls[0][1] is not None
        assert fake.calls[0][1]["alpha"] == 1.0
        assert fake.calls[1][1] is not None
        assert fake.calls[1][1]["alpha"] == 4.0

    # ── concurrent clear calls ──

    async def test_concurrent_clear_calls(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await asyncio.gather(
            domain.clear_device_orientation_override(),
            domain.clear_device_orientation_override(),
            domain.clear_device_orientation_override(),
        )
        assert len(fake.calls) == 3

    # ── exact CDP method names ──

    async def test_set_exact_method_name(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(1.0, 2.0, 3.0)
        method, _ = fake.last_call
        assert method == "DeviceOrientation.setDeviceOrientationOverride"

    async def test_clear_exact_method_name(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        method, _ = fake.last_call
        assert method == "DeviceOrientation.clearDeviceOrientationOverride"

    # ── params values preserved exactly ──

    async def test_params_values_preserved(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(90.0, 45.0, -30.0)
        _, params = fake.last_call
        assert params is not None
        assert params["alpha"] == 90.0
        assert params["beta"] == 45.0
        assert params["gamma"] == -30.0

    # ── type error message includes actual type ──

    async def test_type_error_includes_actual_type(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="got int"):
            await domain.set_device_orientation_override(0, 0.0, 0.0)

    async def test_type_error_includes_bool_type(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="got bool"):
            await domain.set_device_orientation_override(True, 0.0, 0.0)

    async def test_type_error_includes_str_type(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        with pytest.raises(TypeError, match="got str"):
            await domain.set_device_orientation_override("bad", 0.0, 0.0)  # type: ignore[arg-type]
