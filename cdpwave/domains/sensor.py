"""Sensor domain: simulate device sensors (accelerometer, gyroscope, etc.)."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SensorDomain(BaseDomain):
    """Wrapper for the CDP Sensor domain.

    Provides sensor simulation for testing sensor-dependent web APIs
    (e.g. ``Accelerometer``, ``Gyroscope``, ``LinearAccelerationSensor``,
    ``AbsoluteOrientationSensor``).
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Sensor domain."""
        return await self._call("Sensor.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Sensor domain."""
        return await self._call("Sensor.disable")

    async def set_sensor_override(
        self,
        sensor_type: str,
        reading: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set a sensor override reading.

        Args:
            sensor_type: Sensor type (e.g. ``"accelerometer"``,
                ``"gyroscope"``, ``"linear-acceleration"``,
                ``"absolute-orientation"``).
            reading: Optional reading dict with sensor-specific fields
                (e.g. ``{"x": 0, "y": 9.8, "z": 0}``).
        """
        params: dict[str, Any] = {"type": sensor_type}
        if reading is not None:
            params["reading"] = reading
        return await self._call("Sensor.setSensorOverrideReadings", params)

    async def clear_sensor_override(
        self,
        sensor_type: str,
    ) -> dict[str, Any]:
        """Clear a sensor override.

        Args:
            sensor_type: Sensor type to clear override for.
        """
        return await self._call(
            "Sensor.clearSensorOverrideReadings",
            {"type": sensor_type},
        )
