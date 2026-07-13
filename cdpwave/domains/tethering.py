"""Tethering domain: browser port binding.

Events:
    Tethering.accepted: Informs that port was successfully bound and
        got a specified connection id.
        Params: ``port`` (integer — port number that was bound),
        ``connectionId`` (string — connection id to be used).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TetheringDomain(BaseDomain):
    """Wrapper for the CDP Tethering domain.

    The Tethering domain defines methods and events for browser
    port binding.

    Note: This entire domain is **experimental**.

    Events:
        ``Tethering.accepted`` — informs that port was successfully
            bound and got a specified connection id.
            Params: ``port`` (integer — port number that was bound),
            ``connectionId`` (string — connection id to be used).

    Use ``session.on("Tethering.accepted", handler)``
    to subscribe to these events.
    """

    async def bind(self, port: int) -> dict[str, Any]:
        """Request browser port binding.

        Args:
            port: Port number to bind.
        """
        if not isinstance(port, int) or isinstance(port, bool):
            raise TypeError("port must be an integer")
        return await self._call(
            "Tethering.bind",
            {"port": port},
        )

    async def unbind(self, port: int) -> dict[str, Any]:
        """Request browser port unbinding.

        Args:
            port: Port number to unbind.
        """
        if not isinstance(port, int) or isinstance(port, bool):
            raise TypeError("port must be an integer")
        return await self._call(
            "Tethering.unbind",
            {"port": port},
        )
