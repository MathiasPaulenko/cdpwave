"""PWA domain: install, uninstall, and inspect Progressive Web Apps.

Types:

    ``DisplayMode`` — str. If user prefers opening the app in browser
    or an app window.  Values: ``"standalone"``, ``"browser"``.

    ``FileHandlerAccept`` — dict. Replica of the web app OS integration
    state proto.  Fields: ``mediaType`` (str — new name of the
    mimetype), ``fileExtensions`` (list[str]).

    ``FileHandler`` — dict.  Fields: ``action`` (str), ``accepts``
    (list[FileHandlerAccept]), ``displayName`` (str).

Events:

    None.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_DISPLAY_MODES = frozenset({"standalone", "browser"})


class PWADomain(BaseDomain):
    """Wrapper for the CDP PWA domain.

    Provides installation and management of Progressive Web Apps
    (PWAs) for testing PWA-related browser behavior.
    """

    async def change_app_user_settings(
        self,
        manifest_id: str,
        link_capturing: bool = False,
        display_mode: str | None = None,
    ) -> dict[str, Any]:
        """Change user settings of the web app identified by its manifestId.

        If the app was not installed, this command returns an error.
        Unset parameters will be ignored; unrecognized values will
        cause an error.

        Args:
            manifest_id: The id from the webapp's manifest file.
            link_capturing: Whether to enable link capturing.  Always
                sent (no omitempty in Go source — defaults to
                ``False``).
            display_mode: Display mode (e.g. ``"standalone"`` or
                ``"browser"``).  Omitted when None or ``""``
                (omitempty,omitzero in Go source).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``manifest_id`` is not a str,
                ``link_capturing`` is not a bool, or ``display_mode``
                is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        if not isinstance(link_capturing, bool):
            raise TypeError(
                f"link_capturing must be a bool, "
                f"got {type(link_capturing).__name__}"
            )
        if display_mode is not None and not isinstance(display_mode, str):
            raise TypeError(
                f"display_mode must be a str, "
                f"got {type(display_mode).__name__}"
            )
        if display_mode and display_mode not in _VALID_DISPLAY_MODES:
            raise ValueError(
                f"display_mode must be one of "
                f"{sorted(_VALID_DISPLAY_MODES)}, got {display_mode!r}"
            )
        params: dict[str, Any] = {
            "manifestId": manifest_id,
            "linkCapturing": link_capturing,
        }
        if display_mode:
            params["displayMode"] = display_mode
        return await self._call("PWA.changeAppUserSettings", params)

    async def get_os_app_state(
        self,
        manifest_id: str,
    ) -> dict[str, Any]:
        """Get the OS-level state of an installed PWA.

        Args:
            manifest_id: The id from the webapp's manifest file.

        Returns:
            Dict with ``badgeCount`` (int — badge count) and
            ``fileHandlers`` (list[FileHandler] — file handlers
            registered by the app).

        Raises:
            TypeError: If ``manifest_id`` is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        return await self._call(
            "PWA.getOsAppState",
            {"manifestId": manifest_id},
        )

    async def install(
        self,
        manifest_id: str,
        install_url_or_bundle_url: str | None = None,
    ) -> dict[str, Any]:
        """Install a PWA given its manifest identity.

        Args:
            manifest_id: The id from the webapp's manifest file.
            install_url_or_bundle_url: The location of the app or
                bundle overriding the one derived from the
                manifestId.  Omitted when None or ``""``
                (omitempty,omitzero in Go source).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``manifest_id`` is not a str, or
                ``install_url_or_bundle_url`` is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        if install_url_or_bundle_url is not None and not isinstance(
            install_url_or_bundle_url, str
        ):
            raise TypeError(
                f"install_url_or_bundle_url must be a str, "
                f"got {type(install_url_or_bundle_url).__name__}"
            )
        params: dict[str, Any] = {"manifestId": manifest_id}
        if install_url_or_bundle_url:
            params["installUrlOrBundleUrl"] = install_url_or_bundle_url
        return await self._call("PWA.install", params)

    async def launch(
        self,
        manifest_id: str,
        url: str | None = None,
    ) -> dict[str, Any]:
        """Launch the installed web app, or a URL in the same web app.

        Returns a page Target.TargetID which can be used to attach to
        via Target.attachToTarget or similar APIs.

        Args:
            manifest_id: The id from the webapp's manifest file.
            url: URL to launch instead of the default start URL.
                Omitted when None or ``""`` (omitempty,omitzero in Go
                source).

        Returns:
            Dict with ``targetId`` (str — ID of the tab target
            created as a result).

        Raises:
            TypeError: If ``manifest_id`` is not a str, or ``url``
                is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        if url is not None and not isinstance(url, str):
            raise TypeError(
                f"url must be a str, "
                f"got {type(url).__name__}"
            )
        params: dict[str, Any] = {"manifestId": manifest_id}
        if url:
            params["url"] = url
        return await self._call("PWA.launch", params)

    async def launch_files_in_app(
        self,
        manifest_id: str,
        files: list[str],
    ) -> dict[str, Any]:
        """Open one or more local files from an installed web app.

        The web app needs to have file handlers registered to process
        the files.  The API returns one or more page Target.TargetIDs
        which can be used to attach to via Target.attachToTarget or
        similar APIs.

        Args:
            manifest_id: The id from the webapp's manifest file.
            files: List of file paths to open.

        Returns:
            Dict with ``targetIds`` (list[str] — IDs of the tab
            targets created as the result).

        Raises:
            TypeError: If ``manifest_id`` is not a str, ``files`` is
                not a list, or any element is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        if not isinstance(files, list):
            raise TypeError(
                f"files must be a list, "
                f"got {type(files).__name__}"
            )
        for i, f in enumerate(files):
            if not isinstance(f, str):
                raise TypeError(
                    f"files[{i}] must be a str, "
                    f"got {type(f).__name__}"
                )
        return await self._call(
            "PWA.launchFilesInApp",
            {"manifestId": manifest_id, "files": files},
        )

    async def open_current_page_in_app(
        self,
        manifest_id: str,
    ) -> dict[str, Any]:
        """Open the current page in its web app identified by the manifest id.

        Needs to be called on a page target.  Returns immediately
        without waiting for the app to finish loading.

        Args:
            manifest_id: The id from the webapp's manifest file.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``manifest_id`` is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        return await self._call(
            "PWA.openCurrentPageInApp",
            {"manifestId": manifest_id},
        )

    async def uninstall(self, manifest_id: str) -> dict[str, Any]:
        """Uninstall the given manifest_id and close any opened app windows.

        Args:
            manifest_id: The id from the webapp's manifest file.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``manifest_id`` is not a str.
        """
        if not isinstance(manifest_id, str):
            raise TypeError(
                f"manifest_id must be a str, "
                f"got {type(manifest_id).__name__}"
            )
        return await self._call(
            "PWA.uninstall",
            {"manifestId": manifest_id},
        )
