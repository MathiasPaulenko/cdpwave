"""Target domain: session management and target lifecycle."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TargetDomain(BaseDomain):
    """Wrapper for the CDP Target domain."""

    async def create_target(self, url: str) -> dict[str, Any]:
        """Create a new browser target.

        Args:
            url: The initial URL for the new target.

        Returns:
            Response dict containing ``targetId``.
        """
        return await self._call("Target.createTarget", {"url": url})

    async def attach_to_target(
        self,
        target_id: str,
        flatten: bool = True,
    ) -> dict[str, Any]:
        """Attach to a target and return a session ID.

        Args:
            target_id: The target ID to attach to.
            flatten: If True, use flatten mode (single WebSocket).

        Returns:
            Response dict containing ``sessionId``.
        """
        return await self._call(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": flatten},
        )

    async def detach_from_target(self, session_id: str) -> dict[str, Any]:
        """Detach from a target session.

        Args:
            session_id: The session ID to detach.
        """
        return await self._call(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> dict[str, Any]:
        """Close a browser target.

        Args:
            target_id: The target ID to close.
        """
        return await self._call("Target.closeTarget", {"targetId": target_id})

    async def get_targets(self) -> dict[str, Any]:
        """List all available targets.

        Returns all targets (pages, service workers, shared workers,
        browser contexts) known to the browser.

        Returns:
            Response dict with ``targetInfos`` list.
        """
        return await self._call("Target.getTargets")

    async def set_auto_attach(
        self,
        auto_attach: bool,
        flatten: bool = True,
        wait_for_debugger_on_start: bool | None = None,
    ) -> dict[str, Any]:
        """Configure auto-attach to new targets.

        Args:
            auto_attach: If True, auto-attach to new targets.
            flatten: If True, use flatten mode for auto-attached sessions.
            wait_for_debugger_on_start: If set, whether to wait for debugger
                on start.
        """
        params: dict[str, Any] = {
            "autoAttach": auto_attach,
            "flatten": flatten,
        }
        if wait_for_debugger_on_start is not None:
            params["waitForDebuggerOnStart"] = wait_for_debugger_on_start
        return await self._call("Target.setAutoAttach", params)

    async def activate_target(self, target_id: str) -> dict[str, Any]:
        """Activate (focus) a target.

        Args:
            target_id: Target ID to activate.
        """
        return await self._call(
            "Target.activateTarget",
            {"targetId": target_id},
        )

    async def get_target_info(self, target_id: str) -> dict[str, Any]:
        """Get info about a specific target.

        Args:
            target_id: Target ID to query.

        Returns:
            Dict with ``targetInfo``.
        """
        return await self._call(
            "Target.getTargetInfo",
            {"targetId": target_id},
        )

    async def set_discover_targets(self, discover: bool) -> dict[str, Any]:
        """Enable or disable target discovery.

        When enabled, ``Target.targetCreated`` and ``Target.targetDestroyed``
        events will be emitted for all targets.

        Args:
            discover: Whether to discover targets.
        """
        return await self._call(
            "Target.setDiscoverTargets",
            {"discover": discover},
        )

    async def expose_dev_tools_protocol(
        self,
        target_id: str,
        binding_name: str = "cdp",
    ) -> dict[str, Any]:
        """Expose the DevTools protocol to a target's JS context.

        This allows the target page to send CDP commands via a binding.

        Args:
            target_id: Target ID to expose the protocol to.
            binding_name: Name of the binding (default ``"cdp"``).
        """
        return await self._call(
            "Target.exposeDevToolsProtocol",
            {"targetId": target_id, "bindingName": binding_name},
        )

    async def create_browser_context(
        self,
        dispose_on_detach: bool = False,
    ) -> dict[str, Any]:
        """Create a new browser context (like an incognito profile).

        Args:
            dispose_on_detach: Whether to dispose the context when detached.

        Returns:
            Dict with ``browserContextId``.
        """
        return await self._call(
            "Target.createBrowserContext",
            {"disposeOnDetach": dispose_on_detach},
        )

    async def dispose_browser_context(
        self,
        browser_context_id: str,
    ) -> dict[str, Any]:
        """Dispose a browser context.

        Args:
            browser_context_id: Browser context ID to dispose.
        """
        return await self._call(
            "Target.disposeBrowserContext",
            {"browserContextId": browser_context_id},
        )

    async def get_browser_contexts(self) -> dict[str, Any]:
        """List all browser contexts.

        Returns:
            Dict with ``browserContextIds`` list.
        """
        return await self._call("Target.getBrowserContexts")

    async def attach_to_browser_target(self) -> dict[str, Any]:
        """Attach to the browser target.

        Returns:
            Dict with ``sessionId``.
        """
        return await self._call("Target.attachToBrowserTarget")

    async def send_message_to_target(
        self,
        message: str,
        target_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP message to a target.

        Deprecated: Use flatten mode and ``session.send()`` instead.

        Args:
            message: JSON-encoded CDP message string.
            target_id: Optional target ID (legacy mode).
            session_id: Optional session ID (flatten mode).
        """
        params: dict[str, Any] = {"message": message}
        if target_id is not None:
            params["targetId"] = target_id
        if session_id is not None:
            params["sessionId"] = session_id
        return await self._call("Target.sendMessageToTarget", params)

    async def auto_attach_related(
        self,
        target_id: str,
        auto_attach: bool,
        wait_for_debugger_on_start: bool = False,
    ) -> dict[str, Any]:
        """Auto-attach to related targets of a given target.

        Args:
            target_id: Target ID to auto-attach related targets for.
            auto_attach: Whether to auto-attach to related targets.
            wait_for_debugger_on_start: Whether to wait for debugger on start.
        """
        return await self._call(
            "Target.autoAttachRelated",
            {
                "targetId": target_id,
                "autoAttach": auto_attach,
                "waitForDebuggerOnStart": wait_for_debugger_on_start,
            },
        )

    async def set_remote_locations(
        self,
        locations: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Set remote locations for target discovery.

        Args:
            locations: List of location dicts with ``host`` and ``port``.
        """
        return await self._call(
            "Target.setRemoteLocations",
            {"locations": locations},
        )

    async def get_dev_tools_target(self) -> dict[str, Any]:
        """Get the DevTools target info.

        Returns:
            Dict with ``targetInfo``.
        """
        return await self._call("Target.getDevToolsTarget")

    async def open_dev_tools(self) -> dict[str, Any]:
        """Open the DevTools window for the current target."""
        return await self._call("Target.openDevTools")
