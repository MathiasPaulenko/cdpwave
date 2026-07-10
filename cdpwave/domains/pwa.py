"""PWA domain: install, uninstall, and inspect Progressive Web Apps."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PWADomain(BaseDomain):
    """Wrapper for the CDP PWA domain.

    Provides installation and management of Progressive Web Apps
    (PWAs) for testing PWA-related browser behavior.
    """

    async def install(
        self,
        manifest_id: str,
        install_url_or_bundle_url: str | None = None,
    ) -> dict[str, Any]:
        """Install a PWA.

        Args:
            manifest_id: Manifest ID from the web app manifest.
            install_url_or_bundle_url: Optional install URL or bundle URL.

        Returns:
            Dict with ``installState`` or error.
        """
        params: dict[str, Any] = {"manifestId": manifest_id}
        if install_url_or_bundle_url is not None:
            params["installUrlOrBundleUrl"] = install_url_or_bundle_url
        return await self._call("PWA.install", params)

    async def uninstall(self, manifest_id: str) -> dict[str, Any]:
        """Uninstall a PWA.

        Args:
            manifest_id: Manifest ID of the PWA to uninstall.
        """
        return await self._call("PWA.uninstall", {"manifestId": manifest_id})

    async def get_os_app_state(
        self,
        manifest_id: str,
    ) -> dict[str, Any]:
        """Get the OS-level state of an installed PWA.

        Args:
            manifest_id: Manifest ID of the PWA.

        Returns:
            Dict with ``badgeIconIndex``, ``appInstalledState``,
            and ``isAppInstalled``.
        """
        return await self._call(
            "PWA.getOsAppState",
            {"manifestId": manifest_id},
        )

    async def launch(
        self,
        manifest_id: str,
        url: str | None = None,
    ) -> dict[str, Any]:
        """Launch a PWA.

        Args:
            manifest_id: Manifest ID of the PWA to launch.
            url: Optional URL to launch.

        Returns:
            Dict with ``targetId``.
        """
        params: dict[str, Any] = {"manifestId": manifest_id}
        if url is not None:
            params["url"] = url
        return await self._call("PWA.launch", params)

    async def launch_files_in_app(
        self,
        manifest_id: str,
        files: list[str],
    ) -> dict[str, Any]:
        """Launch files in a PWA.

        Args:
            manifest_id: Manifest ID of the PWA.
            files: List of file paths to open.

        Returns:
            Dict with ``targetIds`` list.
        """
        return await self._call(
            "PWA.launchFilesInApp",
            {"manifestId": manifest_id, "files": files},
        )

    async def open_current_page_in_app(
        self,
        manifest_id: str,
    ) -> dict[str, Any]:
        """Open the current page in a PWA.

        Args:
            manifest_id: Manifest ID of the PWA.
        """
        return await self._call(
            "PWA.openCurrentPageInApp",
            {"manifestId": manifest_id},
        )

    async def change_app_user_settings(
        self,
        manifest_id: str,
        link_capturing: bool | None = None,
        display_mode: str | None = None,
    ) -> dict[str, Any]:
        """Change app user settings for a PWA.

        Args:
            manifest_id: Manifest ID of the PWA.
            link_capturing: Whether to enable link capturing.
            display_mode: Display mode (e.g. ``"standalone"``).
        """
        params: dict[str, Any] = {"manifestId": manifest_id}
        if link_capturing is not None:
            params["linkCapturing"] = link_capturing
        if display_mode is not None:
            params["displayMode"] = display_mode
        return await self._call("PWA.changeAppUserSettings", params)
