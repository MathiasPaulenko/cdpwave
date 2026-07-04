"""Browser domain: browser-level commands (version, windows, permissions).

The Browser domain operates on the browser target (no sessionId),
similar to SystemInfo. It is wired into CDPClient, not CDPSession.
"""

from typing import Any

from cdpwave.types import CommandSender


class BrowserDomain:
    """Wrapper for the CDP Browser domain.

    Provides browser-level commands including version info, window
    management, permission control, and download behavior.

    Unlike session-level domains, this domain sends commands directly
    to the browser target without a sessionId.
    """

    def __init__(self, send: CommandSender) -> None:
        self._send = send

    async def _call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._send(method, params)

    async def get_version(self) -> dict[str, Any]:
        """Get browser version information.

        Returns:
            Dict with ``protocolVersion``, ``product``, ``revision``,
            ``userAgent``, and ``jsVersion``.
        """
        return await self._call("Browser.getVersion")

    async def close(self) -> dict[str, Any]:
        """Close the browser gracefully.

        Terminates the browser process and all associated tabs.
        Equivalent to quitting the browser application.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Browser.close")

    async def get_window_for_target(
        self,
        target_id: str | None = None,
        window_id: int | None = None,
    ) -> dict[str, Any]:
        """Get the window ID for a target.

        Args:
            target_id: Target ID to look up.
            window_id: Window ID to look up (alternative to target_id).

        Returns:
            Dict with ``windowId`` and ``bounds``.
        """
        params: dict[str, Any] = {}
        if target_id is not None:
            params["targetId"] = target_id
        if window_id is not None:
            params["windowId"] = window_id
        return await self._call("Browser.getWindowForTarget", params)

    async def set_window_bounds(
        self,
        window_id: int,
        bounds: dict[str, Any],
    ) -> dict[str, Any]:
        """Set window bounds for a browser window.

        Args:
            window_id: Window ID to resize.
            bounds: Bounds dict with optional ``left``, ``top``,
                ``width``, ``height``, and ``windowState``.
        """
        return await self._call(
            "Browser.setWindowBounds",
            {"windowId": window_id, "bounds": bounds},
        )

    async def get_window_bounds(self, window_id: int) -> dict[str, Any]:
        """Get bounds of a browser window.

        Args:
            window_id: Window ID to query.

        Returns:
            Dict with ``bounds``.
        """
        return await self._call(
            "Browser.getWindowBounds",
            {"windowId": window_id},
        )

    async def grant_permissions(
        self,
        origin: str,
        permissions: list[str],
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Grant permissions to an origin.

        Args:
            origin: Security origin to grant permissions to.
            permissions: List of permission names (e.g. ``"geolocation"``,
                ``"notifications"``, ``"camera"``, ``"microphone"``).
            browser_context_id: Optional browser context ID.
        """
        params: dict[str, Any] = {"origin": origin, "permissions": permissions}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.grantPermissions", params)

    async def reset_permissions(
        self,
        origin: str,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Reset all permissions granted to an origin.

        Args:
            origin: Security origin to reset.
            browser_context_id: Optional browser context ID.
        """
        params: dict[str, Any] = {"origin": origin}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.resetPermissions", params)

    async def set_download_behavior(
        self,
        behavior: str,
        browser_context_id: str | None = None,
        download_path: str | None = None,
        events_enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Set download behavior for the browser.

        Args:
            behavior: ``"allow"``, ``"deny"``, or ``"default"``.
            browser_context_id: Optional browser context ID.
            download_path: Path for downloads (when ``behavior`` is
                ``"allow"``).
            events_enabled: Whether to emit download events.
        """
        params: dict[str, Any] = {"behavior": behavior}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        if download_path is not None:
            params["downloadPath"] = download_path
        if events_enabled is not None:
            params["eventsEnabled"] = events_enabled
        return await self._call("Browser.setDownloadBehavior", params)
