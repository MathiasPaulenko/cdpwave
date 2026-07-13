"""DeviceAccess domain: Bluetooth and USB device access prompts.

Types:

    ``RequestID`` — str. Device request id.

    ``DeviceID`` — str. A device id.

    ``PromptDevice`` — dict. Device information displayed in a user
    prompt to select a device. Fields: ``id`` (DeviceID), ``name``
    (str — display name as it appears in a device request user
    prompt).

Events:

    ``DeviceAccess.deviceRequestPrompted`` — A device request opened
    a user prompt to select a device. Respond with the selectPrompt
    or cancelPrompt command. Params: ``id`` (RequestID), ``devices``
    (list[PromptDevice]).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DeviceAccessDomain(BaseDomain):
    """Wrapper for the CDP DeviceAccess domain.

    Provides control over device access prompts (e.g. Bluetooth
    device selection) for testing Web Bluetooth and similar APIs.

    **Experimental domain.**

    Events:

    - ``deviceRequestPrompted`` — A device request opened a user
      prompt to select a device. Respond with the selectPrompt or
      cancelPrompt command. Params: ``id`` (RequestID), ``devices``
      (list[PromptDevice]).
    """

    async def cancel_prompt(self, id: str) -> dict[str, Any]:
        """Cancel a prompt in response to a
        DeviceAccess.deviceRequestPrompted event.

        Args:
            id: Device request id.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` is not a str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        return await self._call(
            "DeviceAccess.cancelPrompt",
            {"id": id},
        )

    async def disable(self) -> dict[str, Any]:
        """Disable events in this domain.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("DeviceAccess.disable")

    async def enable(self) -> dict[str, Any]:
        """Enable events in this domain.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("DeviceAccess.enable")

    async def select_prompt(
        self,
        id: str,
        device_id: str,
    ) -> dict[str, Any]:
        """Select a device in response to a
        DeviceAccess.deviceRequestPrompted event.

        Args:
            id: Device request id.
            device_id: A device id.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` or ``device_id`` is not a str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(device_id, str):
            raise TypeError(
                f"device_id must be a str, "
                f"got {type(device_id).__name__}"
            )
        return await self._call(
            "DeviceAccess.selectPrompt",
            {"id": id, "deviceId": device_id},
        )
