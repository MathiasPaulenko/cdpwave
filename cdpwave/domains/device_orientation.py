"""DeviceOrientation domain: simulate device orientation sensors.

Experimental domain. No events.

Types: None (uses plain ``number`` for alpha/beta/gamma).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DeviceOrientationDomain(BaseDomain):
    """Wrapper for the CDP DeviceOrientation domain.

    Experimental domain that provides device orientation sensor override
    for testing device-orientation-dependent web APIs (e.g.
    ``deviceorientation`` events, ``screen.orientation``).

    No events are defined for this domain.
    """

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

    async def set_device_orientation_override(
        self,
        alpha: float,
        beta: float,
        gamma: float,
    ) -> dict[str, Any]:
        """Set a device orientation override.

        Args:
            alpha: Mock alpha (rotation around the z-axis, 0-360 degrees).
            beta: Mock beta (rotation around the x-axis, -180 to 180 degrees).
            gamma: Mock gamma (rotation around the y-axis, -90 to 90 degrees).

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``alpha``, ``beta`` or ``gamma`` is not a ``float``.
        """
        if isinstance(alpha, bool) or not isinstance(alpha, float):
            raise TypeError(
                f"alpha must be a float, got {type(alpha).__name__}"
            )
        if isinstance(beta, bool) or not isinstance(beta, float):
            raise TypeError(
                f"beta must be a float, got {type(beta).__name__}"
            )
        if isinstance(gamma, bool) or not isinstance(gamma, float):
            raise TypeError(
                f"gamma must be a float, got {type(gamma).__name__}"
            )
        return await self._call(
            "DeviceOrientation.setDeviceOrientationOverride",
            {"alpha": alpha, "beta": beta, "gamma": gamma},
        )
