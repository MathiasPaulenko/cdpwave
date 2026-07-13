"""Unit tests for Memory, Schema, DeviceOrientation, and Sensor domains."""

import pytest

from cdpwave.domains.device_orientation import DeviceOrientationDomain
from cdpwave.domains.memory import MemoryDomain
from cdpwave.domains.schema import SchemaDomain
from cdpwave.domains.sensor import SensorDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestMemoryDomain:
    async def test_get_dom_counters(self) -> None:
        fake = FakeSender({"documents": 1, "nodes": 10, "jsEventListeners": 5})
        domain = MemoryDomain(fake)
        await domain.get_dom_counters()
        assert fake.last_call == ("Memory.getDOMCounters", None)

    async def test_prepare_for_leak_detection(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.prepare_for_leak_detection()
        assert fake.last_call == ("Memory.prepareForLeakDetection", None)

    async def test_set_pressure_notifications_suppressed(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.set_pressure_notifications_suppressed(True)
        assert fake.last_call == (
            "Memory.setPressureNotificationsSuppressed",
            {"suppressed": True},
        )

    async def test_simulate_pressure_notification(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.simulate_pressure_notification("critical")
        assert fake.last_call == (
            "Memory.simulatePressureNotification",
            {"level": "critical"},
        )

    async def test_start_sampling(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=1024, suppress_randomness=True)
        method, params = fake.last_call
        assert method == "Memory.startSampling"
        assert params is not None
        assert params["samplingInterval"] == 1024
        assert params["suppressRandomness"] is True

    async def test_start_sampling_defaults(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling()
        method, params = fake.last_call
        assert method == "Memory.startSampling"
        assert params is not None
        assert "samplingInterval" not in params
        assert params["suppressRandomness"] is False

    async def test_stop_sampling(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.stop_sampling()
        assert fake.last_call == ("Memory.stopSampling", None)

    async def test_get_sampling_profile(self) -> None:
        fake = FakeSender({"profile": {"samples": [], "modules": []}})
        domain = MemoryDomain(fake)
        await domain.get_sampling_profile()
        assert fake.last_call == ("Memory.getSamplingProfile", None)

    async def test_get_browser_sampling_profile(self) -> None:
        fake = FakeSender({"profile": {"samples": [], "modules": []}})
        domain = MemoryDomain(fake)
        await domain.get_browser_sampling_profile()
        assert fake.last_call == ("Memory.getBrowserSamplingProfile", None)


@pytest.mark.unit
class TestSchemaDomain:
    async def test_get_domains(self) -> None:
        fake = FakeSender({"domains": [{"name": "Page", "version": "1.3"}]})
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert fake.last_call == ("Schema.getDomains", None)
        assert "domains" in result

    async def test_get_domains_returns_list(self) -> None:
        fake = FakeSender({
            "domains": [
                {"name": "Page", "version": "1.3"},
                {"name": "Runtime", "version": "1.2"},
            ]
        })
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert isinstance(result["domains"], list)
        assert len(result["domains"]) == 2
        assert result["domains"][0]["name"] == "Page"
        assert result["domains"][0]["version"] == "1.3"

    async def test_get_domains_empty(self) -> None:
        fake = FakeSender({"domains": []})
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert result["domains"] == []

    # ── edge cases ──

    async def test_get_domains_returns_dict(self) -> None:
        fake = FakeSender({"domains": []})
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert isinstance(result, dict)

    async def test_get_domains_no_params_sent(self) -> None:
        fake = FakeSender({"domains": []})
        domain = SchemaDomain(fake)
        await domain.get_domains()
        method, params = fake.last_call
        assert method == "Schema.getDomains"
        assert params is None

    async def test_get_domains_multiple_calls(self) -> None:
        fake = FakeSender({"domains": []})
        domain = SchemaDomain(fake)
        await domain.get_domains()
        await domain.get_domains()
        await domain.get_domains()
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "Schema.getDomains"

    async def test_get_domains_with_extra_fields(self) -> None:
        fake = FakeSender({
            "domains": [
                {
                    "name": "Page",
                    "version": "1.3",
                    "types": ["Frame", "Resource"],
                    "commands": ["navigate", "reload"],
                    "events": ["frameNavigated", "loadEventFired"],
                }
            ]
        })
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert result["domains"][0]["name"] == "Page"
        assert result["domains"][0]["version"] == "1.3"
        assert "types" in result["domains"][0]
        assert "commands" in result["domains"][0]
        assert "events" in result["domains"][0]

    async def test_get_domains_name_is_str(self) -> None:
        fake = FakeSender({
            "domains": [{"name": "Runtime", "version": "1.2"}]
        })
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert isinstance(result["domains"][0]["name"], str)

    async def test_get_domains_version_is_str(self) -> None:
        fake = FakeSender({
            "domains": [{"name": "Runtime", "version": "1.2"}]
        })
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert isinstance(result["domains"][0]["version"], str)

    async def test_get_domains_returns_response(self) -> None:
        fake = FakeSender({"domains": [{"name": "Page", "version": "1.3"}]})
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert result == {"domains": [{"name": "Page", "version": "1.3"}]}


@pytest.mark.unit
class TestDeviceOrientationDomain:
    async def test_set_device_orientation_override(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.set_device_orientation_override(0.0, 90.0, 0.0)
        method, params = fake.last_call
        assert method == "DeviceOrientation.setDeviceOrientationOverride"
        assert params is not None
        assert params["alpha"] == 0.0
        assert params["beta"] == 90.0
        assert params["gamma"] == 0.0

    async def test_clear_device_orientation_override(self) -> None:
        fake = FakeSender({})
        domain = DeviceOrientationDomain(fake)
        await domain.clear_device_orientation_override()
        assert fake.last_call == (
            "DeviceOrientation.clearDeviceOrientationOverride",
            None,
        )


@pytest.mark.unit
class TestSensorDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = SensorDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Sensor.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = SensorDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Sensor.disable", None)

    async def test_set_sensor_override(self) -> None:
        fake = FakeSender({})
        domain = SensorDomain(fake)
        await domain.set_sensor_override(
            "accelerometer", {"x": 0, "y": 9.8, "z": 0}
        )
        method, params = fake.last_call
        assert method == "Sensor.setSensorOverrideReadings"
        assert params is not None
        assert params["type"] == "accelerometer"
        assert params["reading"]["y"] == 9.8

    async def test_clear_sensor_override(self) -> None:
        fake = FakeSender({})
        domain = SensorDomain(fake)
        await domain.clear_sensor_override("gyroscope")
        assert fake.last_call == (
            "Sensor.clearSensorOverrideReadings",
            {"type": "gyroscope"},
        )


@pytest.mark.unit
class TestMemoryDomainEdgeCases:
    """Edge cases for Memory domain: type validation, omitempty, defaults."""

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in MemoryDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 11

    async def test_method_order_matches_go(self) -> None:
        expected = [
            "get_dom_counters",
            "get_dom_counters_for_leak_detection",
            "prepare_for_leak_detection",
            "forcibly_purge_javascript_memory",
            "set_pressure_notifications_suppressed",
            "simulate_pressure_notification",
            "start_sampling",
            "stop_sampling",
            "get_all_time_sampling_profile",
            "get_browser_sampling_profile",
            "get_sampling_profile",
        ]
        actual = [
            name
            for name, value in MemoryDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert actual == expected

    # ── set_pressure_notifications_suppressed ──

    async def test_suppressed_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppressed must be a bool"):
            await domain.set_pressure_notifications_suppressed(1)  # type: ignore[arg-type]

    async def test_suppressed_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppressed must be a bool"):
            await domain.set_pressure_notifications_suppressed("true")  # type: ignore[arg-type]

    async def test_suppressed_false_sent(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.set_pressure_notifications_suppressed(False)
        assert fake.last_call == (
            "Memory.setPressureNotificationsSuppressed",
            {"suppressed": False},
        )

    async def test_suppressed_return_value(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = MemoryDomain(fake)
        result = await domain.set_pressure_notifications_suppressed(True)
        assert result == {"result": "ok"}

    # ── simulate_pressure_notification ──

    async def test_level_moderate(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.simulate_pressure_notification("moderate")
        assert fake.last_call == (
            "Memory.simulatePressureNotification",
            {"level": "moderate"},
        )

    async def test_level_critical(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.simulate_pressure_notification("critical")
        assert fake.last_call == (
            "Memory.simulatePressureNotification",
            {"level": "critical"},
        )

    async def test_level_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="level must be a str"):
            await domain.simulate_pressure_notification(42)  # type: ignore[arg-type]

    async def test_level_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="level must be a str"):
            await domain.simulate_pressure_notification(True)  # type: ignore[arg-type]

    async def test_level_value_error_invalid(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
            await domain.simulate_pressure_notification("low")

    async def test_level_value_error_empty(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
            await domain.simulate_pressure_notification("")

    async def test_level_return_value(self) -> None:
        fake = FakeSender({"done": True})
        domain = MemoryDomain(fake)
        result = await domain.simulate_pressure_notification("critical")
        assert result == {"done": True}

    # ── start_sampling ──

    async def test_start_sampling_interval_zero_omitted(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=0)
        _, params = fake.last_call
        assert params is not None
        assert "samplingInterval" not in params
        assert params["suppressRandomness"] is False

    async def test_start_sampling_suppress_randomness_false(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(suppress_randomness=False)
        _, params = fake.last_call
        assert params is not None
        assert params["suppressRandomness"] is False

    async def test_start_sampling_suppress_randomness_true(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(suppress_randomness=True)
        _, params = fake.last_call
        assert params is not None
        assert params["suppressRandomness"] is True

    async def test_start_sampling_both_params(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=2048, suppress_randomness=True)
        _, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 2048
        assert params["suppressRandomness"] is True

    async def test_start_sampling_interval_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="sampling_interval must be an int"):
            await domain.start_sampling(sampling_interval="1024")  # type: ignore[arg-type]

    async def test_start_sampling_interval_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="sampling_interval must be an int"):
            await domain.start_sampling(sampling_interval=1024.5)  # type: ignore[arg-type]

    async def test_start_sampling_interval_bool_as_int_guard(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="sampling_interval must be an int"):
            await domain.start_sampling(sampling_interval=True)

    async def test_start_sampling_suppress_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppress_randomness must be a bool"):
            await domain.start_sampling(suppress_randomness=1)  # type: ignore[arg-type]

    async def test_start_sampling_suppress_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppress_randomness must be a bool"):
            await domain.start_sampling(suppress_randomness="yes")  # type: ignore[arg-type]

    async def test_start_sampling_return_value(self) -> None:
        fake = FakeSender({"started": True})
        domain = MemoryDomain(fake)
        result = await domain.start_sampling(sampling_interval=512)
        assert result == {"started": True}

    async def test_start_sampling_params_always_has_suppress(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling()
        _, params = fake.last_call
        assert params is not None
        assert "suppressRandomness" in params

    # ── return value tests for no-param methods ──

    async def test_get_dom_counters_return_value(self) -> None:
        fake = FakeSender({"documents": 3, "nodes": 42, "jsEventListeners": 7})
        domain = MemoryDomain(fake)
        result = await domain.get_dom_counters()
        assert result["documents"] == 3
        assert result["nodes"] == 42
        assert result["jsEventListeners"] == 7

    async def test_get_dom_counters_for_leak_detection_return_value(self) -> None:
        fake = FakeSender({"counters": [{"name": "Node", "count": 10}]})
        domain = MemoryDomain(fake)
        result = await domain.get_dom_counters_for_leak_detection()
        assert result["counters"][0]["name"] == "Node"

    async def test_prepare_for_leak_detection_return_value(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        result = await domain.prepare_for_leak_detection()
        assert result == {}

    async def test_forcibly_purge_javascript_memory_return_value(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        result = await domain.forcibly_purge_javascript_memory()
        assert result == {}

    async def test_stop_sampling_return_value(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        result = await domain.stop_sampling()
        assert result == {}

    async def test_get_all_time_sampling_profile_return_value(self) -> None:
        fake = FakeSender({"profile": {"samples": [{"size": 1.0}], "modules": []}})
        domain = MemoryDomain(fake)
        result = await domain.get_all_time_sampling_profile()
        assert result["profile"]["samples"][0]["size"] == 1.0

    async def test_get_browser_sampling_profile_return_value(self) -> None:
        fake = FakeSender({"profile": {"samples": [], "modules": [{"name": "lib"}]}})
        domain = MemoryDomain(fake)
        result = await domain.get_browser_sampling_profile()
        assert result["profile"]["modules"][0]["name"] == "lib"

    async def test_get_sampling_profile_return_value(self) -> None:
        fake = FakeSender({"profile": {"samples": [], "modules": []}})
        domain = MemoryDomain(fake)
        result = await domain.get_sampling_profile()
        assert "profile" in result

    # ── no-param methods send None ──

    async def test_get_dom_counters_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_dom_counters()
        _, params = fake.last_call
        assert params is None

    async def test_get_dom_counters_for_leak_detection_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_dom_counters_for_leak_detection()
        _, params = fake.last_call
        assert params is None

    async def test_prepare_for_leak_detection_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.prepare_for_leak_detection()
        _, params = fake.last_call
        assert params is None

    async def test_forcibly_purge_javascript_memory_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.forcibly_purge_javascript_memory()
        _, params = fake.last_call
        assert params is None

    async def test_stop_sampling_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.stop_sampling()
        _, params = fake.last_call
        assert params is None

    async def test_get_all_time_sampling_profile_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_all_time_sampling_profile()
        _, params = fake.last_call
        assert params is None

    async def test_get_browser_sampling_profile_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_browser_sampling_profile()
        _, params = fake.last_call
        assert params is None

    async def test_get_sampling_profile_sends_none(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_sampling_profile()
        _, params = fake.last_call
        assert params is None

    # ── exact key sets ──

    async def test_start_sampling_exact_keys_with_interval(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=1024)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"samplingInterval", "suppressRandomness"}

    async def test_start_sampling_exact_keys_without_interval(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling()
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"suppressRandomness"}

    async def test_set_pressure_suppressed_exact_keys(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.set_pressure_notifications_suppressed(True)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"suppressed"}

    async def test_simulate_pressure_exact_keys(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.simulate_pressure_notification("moderate")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"level"}

    # ── negative interval, large interval ──

    async def test_start_sampling_negative_interval_sent(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == -1

    async def test_start_sampling_large_interval(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=2**63 - 1)
        _, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 2**63 - 1

    # ── multiple calls independence ──

    async def test_multiple_calls_independent(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.start_sampling(sampling_interval=1024)
        await domain.start_sampling()
        first_method, first_params = fake.calls[0]
        second_method, second_params = fake.calls[1]
        assert first_params is not None
        assert "samplingInterval" in first_params
        assert second_params is not None
        assert "samplingInterval" not in second_params

    async def test_multiple_calls_all_methods(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.get_dom_counters()
        await domain.get_dom_counters_for_leak_detection()
        await domain.prepare_for_leak_detection()
        await domain.forcibly_purge_javascript_memory()
        await domain.set_pressure_notifications_suppressed(True)
        await domain.simulate_pressure_notification("moderate")
        await domain.start_sampling()
        await domain.stop_sampling()
        await domain.get_all_time_sampling_profile()
        await domain.get_browser_sampling_profile()
        await domain.get_sampling_profile()
        assert len(fake.calls) == 11

    # ── suppress_randomness bool-as-int guard ──

    async def test_start_sampling_suppress_bool_as_int_guard(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppress_randomness must be a bool"):
            await domain.start_sampling(suppress_randomness=0)  # type: ignore[arg-type]

    # ── suppressed bool-as-int guard ──

    async def test_suppressed_bool_as_int_guard(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="suppressed must be a bool"):
            await domain.set_pressure_notifications_suppressed(0)  # type: ignore[arg-type]

    # ── level with bytes ──

    async def test_level_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(TypeError, match="level must be a str"):
            await domain.simulate_pressure_notification(b"moderate")  # type: ignore[arg-type]

    # ── level case sensitivity ──

    async def test_level_case_sensitive_moderate(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
            await domain.simulate_pressure_notification("Moderate")

    async def test_level_case_sensitive_critical(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
            await domain.simulate_pressure_notification("Critical")

    async def test_level_uppercase(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
            await domain.simulate_pressure_notification("MODERATE")

    # ── docstring accuracy vs Go source ──

    async def test_set_pressure_suppressed_docstring_all_processes(self) -> None:
        doc = MemoryDomain.set_pressure_notifications_suppressed.__doc__
        assert doc is not None
        assert "all processes" in doc.lower()

    async def test_simulate_pressure_docstring_all_processes(self) -> None:
        doc = MemoryDomain.simulate_pressure_notification.__doc__
        assert doc is not None
        assert "all processes" in doc.lower()

    async def test_get_dom_counters_for_leak_detection_docstring_renderer(self) -> None:
        doc = MemoryDomain.get_dom_counters_for_leak_detection.__doc__
        assert doc is not None
        assert "renderer" in doc.lower()

    async def test_get_all_time_sampling_profile_docstring_renderer_process(self) -> None:
        doc = MemoryDomain.get_all_time_sampling_profile.__doc__
        assert doc is not None
        assert "renderer process" in doc.lower()

    async def test_get_browser_sampling_profile_docstring_browser_process(self) -> None:
        doc = MemoryDomain.get_browser_sampling_profile.__doc__
        assert doc is not None
        assert "browser process" in doc.lower()

    async def test_get_sampling_profile_docstring_last_call(self) -> None:
        doc = MemoryDomain.get_sampling_profile.__doc__
        assert doc is not None
        assert "last startSampling call" in doc

    async def test_get_dom_counters_docstring_js_event_listeners(self) -> None:
        doc = MemoryDomain.get_dom_counters.__doc__
        assert doc is not None
        assert "jsEventListeners" in doc

    async def test_forcibly_purge_docstring_v8(self) -> None:
        doc = MemoryDomain.forcibly_purge_javascript_memory.__doc__
        assert doc is not None
        assert "V8" in doc

    async def test_forcibly_purge_docstring_oom_intervention(self) -> None:
        doc = MemoryDomain.forcibly_purge_javascript_memory.__doc__
        assert doc is not None
        assert "OomIntervention" in doc

    async def test_prepare_for_leak_detection_docstring_terminates_workers(self) -> None:
        doc = MemoryDomain.prepare_for_leak_detection.__doc__
        assert doc is not None
        assert "workers" in doc.lower()

    async def test_prepare_for_leak_detection_docstring_spellcheckers(self) -> None:
        doc = MemoryDomain.prepare_for_leak_detection.__doc__
        assert doc is not None
        assert "spellcheck" in doc.lower()

    async def test_start_sampling_docstring_omitted(self) -> None:
        doc = MemoryDomain.start_sampling.__doc__
        assert doc is not None
        assert "Omitted" in doc or "omitted" in doc

    async def test_start_sampling_docstring_always_sent(self) -> None:
        doc = MemoryDomain.start_sampling.__doc__
        assert doc is not None
        assert "Always sent" in doc

    async def test_class_docstring_experimental(self) -> None:
        doc = MemoryDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_no_events(self) -> None:
        doc = MemoryDomain.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_module_docstring_types(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "PressureLevel" in doc
        assert "SamplingProfileNode" in doc
        assert "SamplingProfile" in doc
        assert "Module" in doc
        assert "DOMCounter" in doc

    async def test_module_docstring_no_events(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_module_docstring_pressure_level_values(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "moderate" in doc
        assert "critical" in doc

    async def test_module_docstring_module_base_address(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "baseAddress" in doc

    async def test_module_docstring_dom_counter_count_int(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "count" in doc
        assert "int" in doc
