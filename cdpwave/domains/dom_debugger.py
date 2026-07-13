"""DOMDebugger domain: DOM and event breakpoints for debugging."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_INSTRUMENTATION_EVENTS = frozenset({
    "setInterval",
    "setTimeout",
    "requestAnimationFrame",
    "requestIdleCallback",
})


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
        if isinstance(node_id, bool) or not isinstance(node_id, int):
            raise TypeError("node_id must be an int")
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        valid_bp_types = {"subtree-modified", "attribute-modified", "node-removed"}
        if type not in valid_bp_types:
            raise ValueError(
                f"type must be one of {sorted(valid_bp_types)}"
            )
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
        if isinstance(node_id, bool) or not isinstance(node_id, int):
            raise TypeError("node_id must be an int")
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        valid_bp_types = {"subtree-modified", "attribute-modified", "node-removed"}
        if type not in valid_bp_types:
            raise ValueError(
                f"type must be one of {sorted(valid_bp_types)}"
            )
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
            target_name: Optional target name to filter by (experimental).
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        if not event_name:
            raise ValueError("event_name must not be empty")
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            if not isinstance(target_name, str):
                raise TypeError("target_name must be a string or None")
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
            target_name: Optional target name (experimental).
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        if not event_name:
            raise ValueError("event_name must not be empty")
        params: dict[str, Any] = {"eventName": event_name}
        if target_name is not None:
            if not isinstance(target_name, str):
                raise TypeError("target_name must be a string or None")
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
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        return await self._call(
            "DOMDebugger.setXHRBreakpoint",
            {"url": url},
        )

    async def remove_xhr_breakpoint(self, url: str) -> dict[str, Any]:
        """Remove an XHR breakpoint.

        Args:
            url: URL substring of the breakpoint to remove.
        """
        if not isinstance(url, str):
            raise TypeError("url must be a string")
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
            depth: Maximum depth at which Node children should be
                retrieved. Defaults to 1. Use -1 for the entire subtree.
            pierce: Whether to pierce through iframes/shadow DOM.

        Returns:
            Dict with ``listeners`` list.
        """
        if not isinstance(object_id, str):
            raise TypeError("object_id must be a string")
        params: dict[str, Any] = {"objectId": object_id}
        if depth is not None:
            if isinstance(depth, bool) or not isinstance(depth, int):
                raise TypeError("depth must be an int or None")
            params["depth"] = depth
        if pierce is not None:
            if not isinstance(pierce, bool):
                raise TypeError("pierce must be a bool or None")
            params["pierce"] = pierce
        return await self._call("DOMDebugger.getEventListeners", params)

    async def set_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Set an instrumentation breakpoint.

        .. deprecated::
            Experimental and deprecated in the CDP specification.
            Redirected to ``EventBreakpoints.setInstrumentationBreakpoint``.

        Args:
            event_name: Instrumentation event name (e.g. ``"setInterval"``).
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        if event_name not in _VALID_INSTRUMENTATION_EVENTS:
            raise ValueError(
                f"event_name must be one of {sorted(_VALID_INSTRUMENTATION_EVENTS)}"
            )
        return await self._call(
            "DOMDebugger.setInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def remove_instrumentation_breakpoint(
        self,
        event_name: str,
    ) -> dict[str, Any]:
        """Remove an instrumentation breakpoint.

        .. deprecated::
            Experimental and deprecated in the CDP specification.
            Redirected to ``EventBreakpoints.removeInstrumentationBreakpoint``.

        Args:
            event_name: Instrumentation event name to remove.
        """
        if not isinstance(event_name, str):
            raise TypeError("event_name must be a string")
        if event_name not in _VALID_INSTRUMENTATION_EVENTS:
            raise ValueError(
                f"event_name must be one of {sorted(_VALID_INSTRUMENTATION_EVENTS)}"
            )
        return await self._call(
            "DOMDebugger.removeInstrumentationBreakpoint",
            {"eventName": event_name},
        )

    async def set_break_on_csp_violation(
        self,
        violation_types: list[str],
    ) -> dict[str, Any]:
        """Set breakpoints on Content Security Policy violations.

        Note: This command is **experimental**.

        Args:
            violation_types: List of violation types (e.g.
                ``["trustedtype-sink-violation", "trustedtype-policy-violation"]``).
        """
        if not isinstance(violation_types, list):
            raise TypeError("violation_types must be a list")
        valid_csp_types = {
            "trustedtype-sink-violation",
            "trustedtype-policy-violation",
        }
        for vt in violation_types:
            if not isinstance(vt, str):
                raise TypeError("violation_types elements must be strings")
            if vt not in valid_csp_types:
                raise ValueError(
                    f"violation_types contains invalid value {vt!r}; "
                    f"must be one of {sorted(valid_csp_types)}"
                )
        return await self._call(
            "DOMDebugger.setBreakOnCSPViolation",
            {"violationTypes": violation_types},
        )
