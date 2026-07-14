"""Edge-case tests for the Sensor domain — validation branches only.

Targets every TypeError/ValueError raise in SensorDomain to push
coverage from 80% to >=90%.
"""

import pytest

from cdpwave.domains.sensor import SensorDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestSensorEdgeValidation:
    async def test_set_sensor_override_sensor_type_not_str(self) -> None:
        d = SensorDomain(FakeSender({}))
        with pytest.raises(TypeError, match="sensor_type must be a string"):
            await d.set_sensor_override(123)  # type: ignore[arg-type]

    async def test_set_sensor_override_sensor_type_invalid(self) -> None:
        d = SensorDomain(FakeSender({}))
        with pytest.raises(ValueError, match="sensor_type must be one of"):
            await d.set_sensor_override("invalid-sensor")

    async def test_set_sensor_override_reading_not_dict(self) -> None:
        d = SensorDomain(FakeSender({}))
        with pytest.raises(TypeError, match="reading must be a dict or None"):
            await d.set_sensor_override("accelerometer", reading="not-a-dict")  # type: ignore[arg-type]

    async def test_clear_sensor_override_sensor_type_not_str(self) -> None:
        d = SensorDomain(FakeSender({}))
        with pytest.raises(TypeError, match="sensor_type must be a string"):
            await d.clear_sensor_override(123)  # type: ignore[arg-type]

    async def test_clear_sensor_override_sensor_type_invalid(self) -> None:
        d = SensorDomain(FakeSender({}))
        with pytest.raises(ValueError, match="sensor_type must be one of"):
            await d.clear_sensor_override("invalid-sensor")
