"""Inspector domain: inspector lifecycle events and commands."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class InspectorDomain(BaseDomain):
    """Wrapper for the CDP Inspector domain.

    The Inspector domain emits:
    - ``Inspector.detached`` — when the inspector is detached.
    - ``Inspector.targetCrashed`` — when the target crashes.

    Use ``session.on("Inspector.detached", handler)``
    to subscribe to these events.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Inspector domain."""
        return await self._call("Inspector.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Inspector domain."""
        return await self._call("Inspector.disable")
