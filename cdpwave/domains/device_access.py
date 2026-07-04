"""DeviceAccess domain: Bluetooth and USB device access prompts."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DeviceAccessDomain(BaseDomain):
    """Wrapper for the CDP DeviceAccess domain.

    Provides control over device access prompts (e.g. Bluetooth
    device selection) for testing Web Bluetooth and similar APIs.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the DeviceAccess domain."""
        return await self._call("DeviceAccess.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the DeviceAccess domain."""
        return await self._call("DeviceAccess.disable")

    async def select_bluetooth_device(
        self,
        request_id: str,
        device: dict[str, Any],
    ) -> dict[str, Any]:
        """Select a Bluetooth device in response to a prompt.

        Args:
            request_id: Request ID from ``DeviceAccess.deviceRequestPrompted``.
            device: Device dict with ``id`` and ``name``.
        """
        return await self._call(
            "DeviceAccess.selectBluetoothDevice",
            {"requestId": request_id, "device": device},
        )

    async def cancel_prompt(self, request_id: str) -> dict[str, Any]:
        """Cancel a device access prompt.

        Args:
            request_id: Request ID to cancel.
        """
        return await self._call(
            "DeviceAccess.cancelPrompt",
            {"requestId": request_id},
        )
