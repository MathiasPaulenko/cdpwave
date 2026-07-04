"""DeviceOrientation domain: simulate device orientation sensors."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DeviceOrientationDomain(BaseDomain):
    """Wrapper for the CDP DeviceOrientation domain.

    Provides device orientation sensor override for testing
    device-orientation-dependent web APIs (e.g. ``deviceorientation``
    events, ``screen.orientation``).
    """

    async def set_device_orientation_override(
        self,
        alpha: float,
        beta: float,
        gamma: float,
    ) -> dict[str, Any]:
        """Set a device orientation override.

        Args:
            alpha: Rotation around the z-axis (0-360 degrees).
            beta: Rotation around the x-axis (-180 to 180 degrees).
            gamma: Rotation around the y-axis (-90 to 90 degrees).
        """
        return await self._call(
            "DeviceOrientation.setDeviceOrientationOverride",
            {"alpha": alpha, "beta": beta, "gamma": gamma},
        )

    async def clear_device_orientation_override(self) -> dict[str, Any]:
        """Clear the device orientation override.

        Removes the sensor override set by
        ``set_device_orientation_override``, restoring the real
        device orientation sensor data.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "DeviceOrientation.clearDeviceOrientationOverride"
        )
