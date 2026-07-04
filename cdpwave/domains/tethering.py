"""Tethering domain: port binding for incoming connections."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TetheringDomain(BaseDomain):
    """Wrapper for the CDP Tethering domain.

    Provides port binding capabilities, allowing the browser to accept
    incoming connections on specified ports. Useful for testing
    network interception and service worker scenarios.
    """

    async def enable(self, port: int | None = None) -> dict[str, Any]:
        """Enable tethering on a port.

        Args:
            port: Port to bind. If omitted, the browser will request
                a port via ``Tethering.requested`` events.
        """
        params: dict[str, Any] = {}
        if port is not None:
            params["port"] = port
        return await self._call("Tethering.bind", params)

    async def disable(self, port: int | None = None) -> dict[str, Any]:
        """Disable tethering on a port.

        Args:
            port: Port to unbind. If omitted, unbinds all.
        """
        params: dict[str, Any] = {}
        if port is not None:
            params["port"] = port
        return await self._call("Tethering.unbind", params)
