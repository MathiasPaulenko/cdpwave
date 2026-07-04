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
