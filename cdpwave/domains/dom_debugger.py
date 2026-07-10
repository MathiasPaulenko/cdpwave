"""DOMDebugger domain: DOM and event breakpoints for debugging."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMDebuggerDomain(BaseDomain):
    """Wrapper for the CDP DOMDebugger domain.

    Provides DOM breakpoints, event listener breakpoints, and XHR
    breakpoints for pausing JavaScript execution at specific DOM
    events or mutations.
    """

    async def set_dom_breakpoint(
        self,
        node_id: int,
        type: str,
    ) -> dict[str, Any]:
        """Set a DOM breakpoint on a node.

        Args:
            node_id: DOM node ID.
            type: Breakpoint type (``"subtree-modified"``,
                ``"attribute-modified"``, ``"node-removed"``).
        """
        return await self._call(
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": node_id, "type": type},
        )

    async def remove_dom_breakpoint(
        self,
        node_id: int,
        type: str,
    ) -> dict[str, Any]:
        """Remove a DOM breakpoint from a node.

        Args:
            node_id: DOM node ID.
            type: Breakpoint type to remove.
        """
        return await self._call(
            "DOMDebugger.removeDOMBreakpoint",
            {"nodeId": node_id, "type": type},
        )

    async def set_event_listener_breakpoint(
        self,
        event_name: str,
        target_name: str | None = None,
    ) -> dict[str, Any]:
        """Set an event listener breakpoint.

        Args:
            event_name: Event name to break on (e.g. ``"click"``).
            target_name: Optional target name to filter by.
        """
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            params["targetName"] = target_name
        return await self._call(
            "DOMDebugger.setEventListenerBreakpoint",
            params,
        )

    async def remove_event_listener_breakpoint(
        self,
        event_name: str,
        target_name: str | None = None,
    ) -> dict[str, Any]:
        """Remove an event listener breakpoint.

        Args:
            event_name: Event name to remove breakpoint for.
            target_name: Optional target name.
        """
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            params["targetName"] = target_name
        return await self._call(
            "DOMDebugger.removeEventListenerBreakpoint",
            params,
        )

    async def set_xhr_breakpoint(self, url: str) -> dict[str, Any]:
        """Set an XHR breakpoint.

        Args:
            url: URL substring to break on. Use empty string for all XHRs.
        """
        return await self._call(
            "DOMDebugger.setXHRBreakpoint",
            {"url": url},
        )

    async def remove_xhr_breakpoint(self, url: str) -> dict[str, Any]:
        """Remove an XHR breakpoint.

        Args:
            url: URL substring of the breakpoint to remove.
        """
        return await self._call(
            "DOMDebugger.removeXHRBreakpoint",
            {"url": url},
        )

    async def get_event_listeners(
        self,
        object_id: str,
        depth: int | None = None,
        pierce: bool | None = None,
    ) -> dict[str, Any]:
        """Get event listeners for a DOM node.

        Args:
            object_id: Remote object ID of the node.
            depth: Maximum depth to get listeners (0 = no children).
            pierce: Whether to pierce through iframes/shadow DOM.

        Returns:
            Dict with ``listeners`` list.
        """
        params: dict[str, Any] = {"objectId": object_id}
        if depth is not None:
            params["depth"] = depth
        if pierce is not None:
            params["pierce"] = pierce
        return await self._call("DOMDebugger.getEventListeners", params)

    async def set_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Set an instrumentation breakpoint.

        Args:
            event_name: Instrumentation event name (e.g. ``"setInterval"``).
        """
        return await self._call(
            "DOMDebugger.setInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def remove_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Remove an instrumentation breakpoint.

        Args:
            event_name: Instrumentation event name to remove.
        """
        return await self._call(
            "DOMDebugger.removeInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def set_break_on_csp_violation(
        self,
        violation_types: list[str],
    ) -> dict[str, Any]:
        """Set breakpoints on Content Security Policy violations.

        Args:
            violation_types: List of violation types (e.g.
                ``["trustedtype-sink-violation", "trustedtype-sink-violation"]``).
        """
        return await self._call(
            "DOMDebugger.setBreakOnCSPViolation",
            {"violationTypes": violation_types},
        )
