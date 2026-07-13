"""Browser domain: browser-level commands (version, windows, permissions).

The Browser domain operates on the browser target (no sessionId),
similar to SystemInfo. It is wired into CDPClient, not CDPSession.

Events:
    Browser.downloadWillBegin — fired when page is about to start
        a download. Params: ``frameId`` (str, id of the frame that
        caused the download), ``guid`` (str, global unique identifier
        of the download), ``url`` (str, URL of the resource being
        downloaded), ``suggestedFilename`` (str, suggested file name
        — the actual name on disk may differ).
    Browser.downloadProgress — fired when download makes progress.
        Last call has ``done`` == true. Params: ``guid`` (str),
        ``totalBytes`` (float, total expected bytes),
        ``receivedBytes`` (float, total bytes received),
        ``state`` (str: ``"inProgress"``, ``"completed"``,
        ``"canceled"``), ``filePath`` (str, optional — file path
        if completed; not guaranteed to be set or exist).
"""

from typing import Any

from cdpwave.types import CommandSender

_VALID_DOWNLOAD_BEHAVIORS = frozenset({
    "allow",
    "allowAndName",
    "deny",
    "default",
})
_VALID_PERMISSION_SETTINGS = frozenset({"granted", "denied", "prompt"})


class BrowserDomain:
    """Wrapper for the CDP Browser domain.

    Provides browser-level commands including version info, window
    management, permission control, download behavior, histograms,
    and privacy sandbox configuration.

    Unlike session-level domains, this domain sends commands directly
    to the browser target without a sessionId.

    Events:
        Browser.downloadWillBegin: fired when page is about to start
            a download. Params: ``frameId`` (id of the frame that
            caused the download), ``guid`` (global unique identifier
            of the download), ``url`` (URL of the resource),
            ``suggestedFilename`` (suggested file name, actual name
            on disk may differ).
        Browser.downloadProgress: fired when download makes progress.
            Last call has ``done`` == true. Params: ``guid``,
            ``totalBytes`` (total expected bytes), ``receivedBytes``
            (total bytes received), ``state`` (``"inProgress"``,
            ``"completed"``, ``"canceled"``), ``filePath`` (optional,
            file path if completed; not guaranteed to be set or exist).
    """

    def __init__(self, send: CommandSender) -> None:
        self._send = send

    async def _call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._send(method, params)

    async def set_permission(
        self,
        permission: dict[str, Any],
        setting: str,
        origin: str | None = None,
        embedded_origin: str | None = None,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Set permission settings for given embedding and embedded origins.

        Args:
            permission: PermissionDescriptor dict with ``name`` (str,
                required) and optional bools ``sysex``, ``userVisibleOnly``,
                ``allowWithoutSanitization``, ``allowWithoutGesture``,
                ``panTiltZoom``.
            setting: Permission setting (``"granted"``, ``"denied"``,
                or ``"prompt"``).
            origin: Embedding origin the permission applies to. All
                origins if not specified.
            embedded_origin: Embedded origin the permission applies to.
                Ignored unless ``origin`` is present and valid. If
                ``origin`` is provided but ``embedded_origin`` isn't,
                ``origin`` is used as the embedded origin.
            browser_context_id: Browser context to override. When
                omitted, default browser context is used.
        """
        params: dict[str, Any] = {"permission": permission, "setting": setting}
        if not isinstance(setting, str):
            raise TypeError("setting must be a str")
        if setting not in _VALID_PERMISSION_SETTINGS:
            raise ValueError(
                "setting must be 'granted', 'denied', or 'prompt'"
            )
        if origin is not None:
            params["origin"] = origin
        if embedded_origin is not None:
            params["embeddedOrigin"] = embedded_origin
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.setPermission", params)

    async def reset_permissions(
        self,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Reset all permission management for all origins.

        Args:
            browser_context_id: Browser context to reset permissions.
                When omitted, default browser context is used.
        """
        params: dict[str, Any] = {}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.resetPermissions", params or None)

    async def set_download_behavior(
        self,
        behavior: str,
        browser_context_id: str | None = None,
        download_path: str | None = None,
        events_enabled: bool = False,
    ) -> dict[str, Any]:
        """Set the behavior when downloading a file.

        Args:
            behavior: ``"allow"``, ``"allowAndName"``, ``"deny"``, or
                ``"default"``.
            browser_context_id: Browser context to set download behavior.
                When omitted, default browser context is used.
            download_path: The default path to save downloaded files
                to. Required if behavior is set to ``"allow"`` or
                ``"allowAndName"``.
            events_enabled: Whether to emit download events (defaults
                to false). Always sent to CDP.
        """
        if not isinstance(behavior, str):
            raise TypeError("behavior must be a str")
        if behavior not in _VALID_DOWNLOAD_BEHAVIORS:
            raise ValueError(
                "behavior must be 'allow', 'allowAndName', 'deny', or 'default'"
            )
        params: dict[str, Any] = {"behavior": behavior, "eventsEnabled": events_enabled}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        if download_path is not None:
            params["downloadPath"] = download_path
        return await self._call("Browser.setDownloadBehavior", params)

    async def cancel_download(
        self,
        guid: str,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Cancel a download if in progress.

        Args:
            guid: Global unique identifier of the download.
            browser_context_id: Browser context to perform the action
                in. When omitted, default browser context is used.
        """
        params: dict[str, Any] = {"guid": guid}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.cancelDownload", params)

    async def close(self) -> dict[str, Any]:
        """Close browser gracefully.

        Terminates the browser process and all associated tabs.
        Equivalent to quitting the browser application.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Browser.close")

    async def crash(self) -> dict[str, Any]:
        """Crashes browser on the main thread.

        Experimental and destructive — use with caution.
        """
        return await self._call("Browser.crash")

    async def crash_gpu_process(self) -> dict[str, Any]:
        """Crashes GPU process.

        Experimental and destructive — use with caution.
        """
        return await self._call("Browser.crashGpuProcess")

    async def get_version(self) -> dict[str, Any]:
        """Returns version information.

        Returns:
            Dict with ``protocolVersion``, ``product``, ``revision``,
            ``userAgent``, and ``jsVersion``.
        """
        return await self._call("Browser.getVersion")

    async def get_browser_command_line(self) -> dict[str, Any]:
        """Returns the command line switches for the browser process.

        Only works if ``--enable-automation`` is on the command line.

        Returns:
            Dict with ``arguments`` (list of command-line parameters).
        """
        return await self._call("Browser.getBrowserCommandLine")

    async def get_command_line(self) -> dict[str, Any]:
        """Returns the command line switches for the browser process.

        Convenience alias for ``get_browser_command_line``.

        Returns:
            Dict with ``arguments`` (list of command-line parameters).
        """
        return await self.get_browser_command_line()

    async def get_histograms(
        self,
        query: str | None = None,
        delta: bool = False,
    ) -> dict[str, Any]:
        """Get Chrome histograms.

        Args:
            query: Requested substring in name. Only histograms which
                have query as a substring in their name are extracted.
                An empty or absent query returns all histograms.
            delta: If true, retrieve delta since last delta call.
                Always sent to CDP (defaults to false).

        Returns:
            Dict with ``histograms`` list.
        """
        params: dict[str, Any] = {"delta": delta}
        if query is not None:
            params["query"] = query
        return await self._call("Browser.getHistograms", params)

    async def get_histogram(
        self,
        name: str,
        delta: bool = False,
    ) -> dict[str, Any]:
        """Get a Chrome histogram by name.

        Args:
            name: Histogram name (e.g. ``"V8.ExecuteJS"``).
            delta: If true, retrieve delta since last delta call.
                Always sent to CDP (defaults to false).

        Returns:
            Dict with ``histogram`` containing ``name``, ``sum``,
            ``count``, and ``buckets``.
        """
        params: dict[str, Any] = {"name": name, "delta": delta}
        return await self._call("Browser.getHistogram", params)

    async def get_window_bounds(self, window_id: int) -> dict[str, Any]:
        """Get position and size of the browser window.

        Args:
            window_id: Browser window id.

        Returns:
            Dict with ``bounds``. When window state is
            ``"minimized"``, the restored window position and size
            are returned.
        """
        return await self._call(
            "Browser.getWindowBounds",
            {"windowId": window_id},
        )

    async def get_window_for_target(
        self,
        target_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the browser window that contains the devtools target.

        Args:
            target_id: Devtools agent host id. If called as part of
                a session, associated targetId is used.

        Returns:
            Dict with ``windowId`` and ``bounds``. When window state
            is ``"minimized"``, the restored window position and size
            are returned.
        """
        params: dict[str, Any] = {}
        if target_id is not None:
            params["targetId"] = target_id
        return await self._call("Browser.getWindowForTarget", params or None)

    async def set_window_bounds(
        self,
        window_id: int,
        bounds: dict[str, Any],
    ) -> dict[str, Any]:
        """Set position and/or size of the browser window.

        Args:
            window_id: Browser window id.
            bounds: New window bounds dict with optional ``left``,
                ``top``, ``width``, ``height``, and ``windowState``.
                The ``minimized``, ``maximized`` and ``fullscreen``
                states cannot be combined with ``left``, ``top``,
                ``width`` or ``height``. Leaves unspecified fields
                unchanged.
        """
        return await self._call(
            "Browser.setWindowBounds",
            {"windowId": window_id, "bounds": bounds},
        )

    async def set_contents_size(
        self,
        window_id: int,
        width: int | None = None,
        height: int | None = None,
    ) -> dict[str, Any]:
        """Set size of the browser contents resizing browser window as necessary.

        Args:
            window_id: Browser window id.
            width: Window contents width in DIP. Assumes current width
                if omitted. Must be specified if ``height`` is omitted.
            height: Window contents height in DIP. Assumes current
                height if omitted. Must be specified if ``width`` is
                omitted.
        """
        params: dict[str, Any] = {"windowId": window_id}
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        return await self._call("Browser.setContentsSize", params)

    async def set_dock_tile(
        self,
        badge_label: str | None = None,
        image: str | None = None,
    ) -> dict[str, Any]:
        """Set dock tile details, platform-specific.

        Args:
            badge_label: Badge label for the dock tile.
            image: PNG encoded image (base64 string).
        """
        params: dict[str, Any] = {}
        if badge_label is not None:
            params["badgeLabel"] = badge_label
        if image is not None:
            params["image"] = image
        return await self._call("Browser.setDockTile", params or None)

    async def execute_browser_command(
        self,
        command_id: str,
    ) -> dict[str, Any]:
        """Invoke custom browser commands used by telemetry.

        Args:
            command_id: Browser command id (``"openTabSearch"``,
                ``"closeTabSearch"``, or ``"openGlic"``).
        """
        return await self._call(
            "Browser.executeBrowserCommand",
            {"commandId": command_id},
        )

    async def add_privacy_sandbox_enrollment_override(
        self,
        url: str,
    ) -> dict[str, Any]:
        """Allows a site to use privacy sandbox features that require enrollment.

        The site does not actually need to be enrolled. Only supported
        on page targets.

        Args:
            url: URL of the site to override enrollment for.
        """
        return await self._call(
            "Browser.addPrivacySandboxEnrollmentOverride",
            {"url": url},
        )

    async def add_privacy_sandbox_coordinator_key_config(
        self,
        api: str,
        coordinator_origin: str,
        key_config: str,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Configures encryption keys used with a given privacy sandbox API.

        The keys are used to talk to a trusted coordinator. Intended
        for test automation only — ``coordinator_origin`` must be a
        ``.test`` domain. No existing coordinator configuration for
        the origin may exist.

        Args:
            api: Privacy sandbox API (``"BiddingAndAuctionServices"``
                or ``"TrustedKeyValue"``).
            coordinator_origin: Coordinator origin (must be ``.test``
                domain).
            key_config: Key configuration string.
            browser_context_id: Browser context to perform the action
                in. When omitted, default browser context is used.
        """
        params: dict[str, Any] = {
            "api": api,
            "coordinatorOrigin": coordinator_origin,
            "keyConfig": key_config,
        }
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call(
            "Browser.addPrivacySandboxCoordinatorKeyConfig", params,
        )

    async def grant_permissions(
        self,
        origin: str,
        permissions: list[str],
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Grant specific permissions to the given origin.

        .. deprecated::
            Deprecated in CDP spec. Use ``set_permission`` instead.

        Args:
            origin: Security origin to grant permissions to, all origins
                if not specified.
            permissions: List of permission names (e.g. ``"geolocation"``,
                ``"notifications"``, ``"camera"``, ``"microphone"``).
            browser_context_id: Browser context to override permissions.
                When omitted, default browser context is used.
        """
        params: dict[str, Any] = {"origin": origin, "permissions": permissions}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Browser.grantPermissions", params)
