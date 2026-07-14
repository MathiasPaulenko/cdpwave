"""Target domain: session management and target lifecycle."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TargetDomain(BaseDomain):
    """Wrapper for the CDP Target domain."""

    async def create_target(
        self,
        url: str,
        left: int | None = None,
        top: int | None = None,
        width: int | None = None,
        height: int | None = None,
        window_state: str | None = None,
        browser_context_id: str | None = None,
        enable_begin_frame_control: bool = False,
        new_window: bool = False,
        background: bool = False,
        for_tab: bool = False,
        hidden: bool = False,
        focus: bool = False,
    ) -> dict[str, Any]:
        """Create a new browser target.

        Args:
            url: The initial URL for the new target.
            left: Optional frame left origin in DIP.
            top: Optional frame top origin in DIP.
            width: Optional frame width in DIP.
            height: Optional frame height in DIP.
            window_state: Optional frame window state ("normal",
                "minimized", "maximized", "fullscreen").
            browser_context_id: Optional browser context ID for isolation.
            enable_begin_frame_control: Whether BeginFrames for this target
                will be controlled via DevTools (headless shell only).
            new_window: If True, open in a new window.
            background: If True, open in background (not focused).
            for_tab: If True, create the target of type "tab".
            hidden: If True, create a hidden target (not in tab UI strip).
            focus: If True, focus the new target.

        Returns:
            Response dict containing ``targetId``.
        """
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if not url:
            raise ValueError("url must not be empty")
        params: dict[str, Any] = {
            "url": url,
            "enableBeginFrameControl": enable_begin_frame_control,
            "newWindow": new_window,
            "background": background,
            "forTab": for_tab,
            "hidden": hidden,
            "focus": focus,
        }
        if left is not None:
            params["left"] = left
        if top is not None:
            params["top"] = top
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if window_state is not None:
            if not isinstance(window_state, str):
                raise TypeError("window_state must be a string or None")
            valid_window_states = {"normal", "minimized", "maximized", "fullscreen"}
            if window_state not in valid_window_states:
                raise ValueError(
                    f"window_state must be one of {sorted(valid_window_states)}"
                )
            params["windowState"] = window_state
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Target.createTarget", params)

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
        if not isinstance(target_id, str):
            raise TypeError("target_id must be a string")
        return await self._call(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": flatten},
        )

    async def detach_from_target(self, session_id: str) -> dict[str, Any]:
        """Detach from a target session.

        Args:
            session_id: The session ID to detach.
        """
        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string")
        return await self._call(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> dict[str, Any]:
        """Close a browser target.

        Args:
            target_id: The target ID to close.
        """
        if not isinstance(target_id, str):
            raise TypeError("target_id must be a string")
        return await self._call("Target.closeTarget", {"targetId": target_id})

    async def get_targets(
        self,
        filter: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """List all available targets.

        Returns all targets (pages, service workers, shared workers,
        browser contexts) known to the browser.

        Args:
            filter: Optional filter dict to match targets.

        Returns:
            Response dict with ``targetInfos`` list.
        """
        if filter is not None and not isinstance(filter, dict):
            raise TypeError("filter must be a dict or None")
        params: dict[str, Any] = {}
        if filter is not None:
            params["filter"] = filter
        return await self._call("Target.getTargets", params)

    async def set_auto_attach(
        self,
        auto_attach: bool,
        wait_for_debugger_on_start: bool = False,
        flatten: bool = True,
        filter: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Configure auto-attach to new targets.

        Args:
            auto_attach: If True, auto-attach to new targets.
            wait_for_debugger_on_start: Whether to pause new targets when
                attaching to them.
            flatten: If True, use flatten mode for auto-attached sessions.
            filter: Optional filter dict to match targets.
        """
        if filter is not None and not isinstance(filter, dict):
            raise TypeError("filter must be a dict or None")
        params: dict[str, Any] = {
            "autoAttach": auto_attach,
            "waitForDebuggerOnStart": wait_for_debugger_on_start,
            "flatten": flatten,
        }
        if filter is not None:
            params["filter"] = filter
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

    async def set_discover_targets(
        self,
        discover: bool,
        filter: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Enable or disable target discovery.

        When enabled, ``Target.targetCreated`` and ``Target.targetDestroyed``
        events will be emitted for all targets.

        Args:
            discover: Whether to discover targets.
            filter: Optional filter dict to match targets.
        """
        if filter is not None and not isinstance(filter, dict):
            raise TypeError("filter must be a dict or None")
        params: dict[str, Any] = {"discover": discover}
        if filter is not None:
            params["filter"] = filter
        return await self._call("Target.setDiscoverTargets", params)

    async def expose_dev_tools_protocol(
        self,
        target_id: str,
        binding_name: str | None = None,
        inherit_permissions: bool = False,
    ) -> dict[str, Any]:
        """Expose the DevTools protocol to a target's JS context.

        This allows the target page to send CDP commands via a binding.

        Args:
            target_id: Target ID to expose the protocol to.
            binding_name: Optional binding name (``"cdp"`` if not specified).
            inherit_permissions: If True, inherits the current root session's
                permissions.
        """
        params: dict[str, Any] = {
            "targetId": target_id,
            "inheritPermissions": inherit_permissions,
        }
        if binding_name is not None:
            params["bindingName"] = binding_name
        return await self._call("Target.exposeDevToolsProtocol", params)

    async def create_browser_context(
        self,
        dispose_on_detach: bool = False,
        proxy_server: str | None = None,
        proxy_bypass_list: str | None = None,
        origins_with_universal_network_access: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new browser context (like an incognito profile).

        Args:
            dispose_on_detach: Whether to dispose the context when detached.
            proxy_server: Optional proxy server, similar to --proxy-server.
            proxy_bypass_list: Optional proxy bypass list.
            origins_with_universal_network_access: Optional list of origins
                to grant unlimited cross-origin access to.

        Returns:
            Dict with ``browserContextId``.
        """
        params: dict[str, Any] = {"disposeOnDetach": dispose_on_detach}
        if proxy_server is not None:
            params["proxyServer"] = proxy_server
        if proxy_bypass_list is not None:
            params["proxyBypassList"] = proxy_bypass_list
        if origins_with_universal_network_access is not None:
            params["originsWithUniversalNetworkAccess"] = origins_with_universal_network_access
        return await self._call("Target.createBrowserContext", params)

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
        wait_for_debugger_on_start: bool = False,
        filter: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Auto-attach to related targets of a given target.

        Args:
            target_id: Target ID to auto-attach related targets for.
            wait_for_debugger_on_start: Whether to wait for debugger on start.
            filter: Optional filter dict to match targets.
        """
        if filter is not None and not isinstance(filter, dict):
            raise TypeError("filter must be a dict or None")
        params: dict[str, Any] = {
            "targetId": target_id,
            "waitForDebuggerOnStart": wait_for_debugger_on_start,
        }
        if filter is not None:
            params["filter"] = filter
        return await self._call("Target.autoAttachRelated", params)

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

    async def get_dev_tools_target(
        self,
        target_id: str,
    ) -> dict[str, Any]:
        """Get the DevTools target info for a given target.

        Args:
            target_id: Page or tab target ID.

        Returns:
            Dict with ``targetId`` of the DevTools page target.
        """
        return await self._call(
            "Target.getDevToolsTarget",
            {"targetId": target_id},
        )

    async def open_dev_tools(
        self,
        target_id: str,
        panel_id: str | None = None,
    ) -> dict[str, Any]:
        """Open the DevTools window for a target.

        Args:
            target_id: Page or tab target ID.
            panel_id: Optional panel to open (``"elements"``, ``"console"``,
                ``"network"``, ``"sources"``, etc.).
        """
        params: dict[str, Any] = {"targetId": target_id}
        if panel_id is not None:
            params["panelId"] = panel_id
        return await self._call("Target.openDevTools", params)
