"""SystemInfo domain: system and GPU information.

Types:

    ``GPUDevice`` — dict.  Describes a single graphics processor.
    Fields: ``vendorId`` (float), ``deviceId`` (float),
    ``subSysId`` (float, optional), ``revision`` (float, optional),
    ``vendorString`` (str), ``deviceString`` (str),
    ``driverVendor`` (str), ``driverVersion`` (str).

    ``Size`` — dict.  Width and height dimensions.
    Fields: ``width`` (int), ``height`` (int).

    ``GPUInfo`` — dict.  Information about the GPU(s) on the system.
    Fields: ``devices`` (list[GPUDevice]), ``auxAttributes`` (dict,
    optional), ``featureStatus`` (dict, optional),
    ``driverBugWorkarounds`` (list[str]),
    ``videoDecoding`` (list[dict]),
    ``videoEncoding`` (list[dict]).

    ``ProcessInfo`` — dict.  Represents process info.
    Fields: ``type`` (str), ``id`` (int), ``cpuTime`` (float).

Events:

    None.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SystemInfoDomain(BaseDomain):
    """Wrapper for the CDP SystemInfo domain.

    Defines methods and events for querying low-level system
    information.
    """

    async def get_info(self) -> dict[str, Any]:
        """Returns information about the system.

        Returns:
            Dict with ``gpu`` (GPUInfo), ``modelName``,
            ``modelVersion``, and ``commandLine``.
        """
        return await self._call("SystemInfo.getInfo")

    async def get_feature_state(
        self,
        feature_state: str,
    ) -> dict[str, Any]:
        """Returns information about the feature state.

        Args:
            feature_state: Feature state to query.

        Returns:
            Dict with ``featureEnabled`` boolean.

        Raises:
            TypeError: If ``feature_state`` is not a str.
        """
        if not isinstance(feature_state, str):
            raise TypeError(
                f"feature_state must be a str, "
                f"got {type(feature_state).__name__}"
            )
        return await self._call(
            "SystemInfo.getFeatureState",
            {"featureState": feature_state},
        )

    async def get_process_info(self) -> dict[str, Any]:
        """Returns information about all running processes.

        Returns:
            Dict with ``processInfo`` list of process info blocks.
        """
        return await self._call("SystemInfo.getProcessInfo")
