"""EventBreakpoints domain: instrumentation event breakpoints.

Events:

    None.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class EventBreakpointsDomain(BaseDomain):
    """Wrapper for the CDP EventBreakpoints domain.

    Permits setting JavaScript breakpoints on operations and events
    occurring in native code invoked from JavaScript. Once a breakpoint
    is hit, it is reported through the Debugger domain, similarly to
    regular breakpoints being hit.

    Note: This entire domain is **experimental**.
    """

    async def set_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Set a breakpoint on a particular native event.

        Args:
            event_name: Instrumentation name to stop on (e.g.
                ``"scriptFirstStatement"``,
                ``"cancelAnimationFrame"``,
                ``"requestAnimationFrame"``).
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        return await self._call(
            "EventBreakpoints.setInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def remove_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Remove a breakpoint on a particular native event.

        Args:
            event_name: Instrumentation name to stop on.
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        return await self._call(
            "EventBreakpoints.removeInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def clear_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Remove a breakpoint on a particular native event.

        .. deprecated::
            Use ``remove_instrumentation_breakpoint`` instead.
        """
        return await self.remove_instrumentation_breakpoint(event_name)

    async def disable(self) -> dict[str, Any]:
        """Remove all breakpoints."""
        return await self._call("EventBreakpoints.disable")
