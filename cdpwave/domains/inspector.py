"""Inspector domain: inspector domain notifications and lifecycle events.

Events:
    Inspector.detached: Fired when remote debugging connection is about
        to be terminated. Contains detach reason.
        Params: ``reason`` (string — the reason why connection has been
        terminated).
    Inspector.targetCrashed: Fired when debugging target has crashed.
        No params.
    Inspector.targetReloadedAfterCrash: Fired when debugging target has
        reloaded after crash. No params.
    Inspector.workerScriptLoaded: Experimental. Fired on worker targets
        when main worker script and any imported scripts have been
        evaluated. No params.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class InspectorDomain(BaseDomain):
    """Wrapper for the CDP Inspector domain.

    Note: This entire domain is **experimental**.

    Events:
        ``Inspector.detached`` — fired when remote debugging connection
            is about to be terminated. Contains detach reason.
            Params: ``reason`` (string — the reason why connection has
            been terminated).
        ``Inspector.targetCrashed`` — fired when debugging target has
            crashed. No params.
        ``Inspector.targetReloadedAfterCrash`` — fired when debugging
            target has reloaded after crash. No params.
        ``Inspector.workerScriptLoaded`` — experimental. Fired on worker
            targets when main worker script and any imported scripts
            have been evaluated. No params.

    Use ``session.on("Inspector.detached", handler)``
    to subscribe to these events.
    """

    async def disable(self) -> dict[str, Any]:
        """Disable inspector domain notifications."""
        return await self._call("Inspector.disable")

    async def enable(self) -> dict[str, Any]:
        """Enable inspector domain notifications."""
        return await self._call("Inspector.enable")
