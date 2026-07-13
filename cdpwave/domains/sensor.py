"""Sensor domain: simulate device sensors (accelerometer, gyroscope, etc.)."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_SENSOR_TYPES = frozenset({
    "accelerometer",
    "gyroscope",
    "linear-acceleration",
    "absolute-orientation",
    "relative-orientation",
    "gravity",
    "magnetometer",
    "ambient-light",
    "proximity",
})


class SensorDomain(BaseDomain):
    """Wrapper for the CDP Sensor domain.

    Provides sensor simulation for testing sensor-dependent web APIs
    (e.g. ``Accelerometer``, ``Gyroscope``, ``LinearAccelerationSensor``,
    ``AbsoluteOrientationSensor``).
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Sensor domain.

        Activates Sensor domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Sensor.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Sensor domain.

        Deactivates Sensor domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
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
        if not isinstance(sensor_type, str):
            raise TypeError("sensor_type must be a string")
        if sensor_type not in _VALID_SENSOR_TYPES:
            raise ValueError(
                f"sensor_type must be one of {sorted(_VALID_SENSOR_TYPES)}"
            )
        if reading is not None and not isinstance(reading, dict):
            raise TypeError("reading must be a dict or None")
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
        if not isinstance(sensor_type, str):
            raise TypeError("sensor_type must be a string")
        if sensor_type not in _VALID_SENSOR_TYPES:
            raise ValueError(
                f"sensor_type must be one of {sorted(_VALID_SENSOR_TYPES)}"
            )
        return await self._call(
            "Sensor.clearSensorOverrideReadings",
            {"type": sensor_type},
        )
