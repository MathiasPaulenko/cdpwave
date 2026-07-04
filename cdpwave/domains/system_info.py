"""SystemInfo domain: system and GPU information."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SystemInfoDomain(BaseDomain):
    """Wrapper for the CDP SystemInfo domain.

    Provides access to system-level information including GPU info,
    process info, and feature state.
    """

    async def get_info(self) -> dict[str, Any]:
        """Get system information.

        Returns:
            Dict with ``gpu``, ``modelName``, ``modelVersion``,
            ``commandLine``, and other system info.
        """
        return await self._call("SystemInfo.getInfo")

    async def get_process_info(self) -> dict[str, Any]:
        """Get process information.

        Returns:
            Dict with ``processInfo`` list of process dicts.
        """
        return await self._call("SystemInfo.getProcessInfo")

    async def get_feature_state(
        self,
        feature_name: str,
    ) -> dict[str, Any]:
        """Get the state of a feature flag.

        Args:
            feature_name: Name of the feature to query.

        Returns:
            Dict with ``featureEnabled`` boolean.
        """
        return await self._call(
            "SystemInfo.getFeatureState",
            {"featureName": feature_name},
        )

    async def get_gpu_info(self) -> dict[str, Any]:
        """Get GPU information.

        Returns:
            Dict with ``gpu`` containing GPU device info, driver info,
            and feature status.
        """
        return await self._call("SystemInfo.getGPUInfo")
