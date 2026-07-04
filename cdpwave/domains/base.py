"""Base class for all CDP domain wrappers."""

from typing import Any

from cdpwave.types import CommandSender


class BaseDomain:
    """Base class for CDP domain wrappers.

    Each domain (Page, Runtime, Network, etc.) inherits from BaseDomain
    and uses ``_call()`` to send CDP commands via the session's CommandSender.
    """

    def __init__(self, send: CommandSender) -> None:
        self._send = send

    async def _call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a CDP command and return the response result dict.

        Args:
            method: CDP method name (e.g. ``"Page.navigate"``).
            params: Optional command parameters.

        Returns:
            The CDP response result dict.
        """
        return await self._send(method, params)
