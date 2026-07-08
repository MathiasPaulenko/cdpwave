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

    async def test_force_garbage_collection(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.force_garbage_collection()
        assert fake.last_call == ("Memory.forceGarbageCollection", None)

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

    async def test_stop_sampling(self) -> None:
        fake = FakeSender({})
        domain = MemoryDomain(fake)
        await domain.stop_sampling()
        assert fake.last_call == ("Memory.stopSampling", None)

    async def test_get_sampling_profile(self) -> None:
        fake = FakeSender({"samples": [], "modules": []})
        domain = MemoryDomain(fake)
        await domain.get_sampling_profile()
        assert fake.last_call == ("Memory.getSamplingProfile", None)


@pytest.mark.unit
class TestSchemaDomain:
    async def test_get_domains(self) -> None:
        fake = FakeSender({"domains": [{"name": "Page", "version": "1.3"}]})
        domain = SchemaDomain(fake)
        result = await domain.get_domains()
        assert fake.last_call == ("Schema.getDomains", None)
        assert "domains" in result


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
