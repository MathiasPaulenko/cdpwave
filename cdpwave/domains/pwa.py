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
