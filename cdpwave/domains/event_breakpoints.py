"""EventBreakpoints domain: instrumentation and native event breakpoints."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class EventBreakpointsDomain(BaseDomain):
    """Wrapper for the CDP EventBreakpoints domain.

    Provides instrumentation breakpoints and native event breakpoints
    for pausing JavaScript execution at specific events.
    """

    async def set_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Set an instrumentation breakpoint.

        Args:
            event_name: Instrumentation event name (e.g.
                ``"scriptFirstStatement"``,
                ``"cancelAnimationFrame"``,
                ``"requestAnimationFrame"``).
        """
        return await self._call(
            "EventBreakpoints.setInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def clear_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Clear an instrumentation breakpoint.

        Args:
            event_name: Instrumentation event name to clear.
        """
        return await self._call(
            "EventBreakpoints.clearInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def set_breakpoint_on_native_event(
        self,
        event_name: str,
        target_name: str | None = None,
    ) -> dict[str, Any]:
        """Set a breakpoint on a native DOM event.

        Args:
            event_name: Native event name (e.g. ``"click"``,
                ``"keydown"``).
            target_name: Optional target name to filter by.
        """
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            params["targetName"] = target_name
        return await self._call(
            "EventBreakpoints.setBreakpointOnNativeEvent",
            params,
        )

    async def clear_breakpoint_on_native_event(
        self,
        event_name: str,
        target_name: str | None = None,
    ) -> dict[str, Any]:
        """Clear a breakpoint on a native DOM event.

        Args:
            event_name: Native event name to clear.
            target_name: Optional target name.
        """
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            params["targetName"] = target_name
        return await self._call(
            "EventBreakpoints.clearBreakpointOnNativeEvent",
            params,
        )
