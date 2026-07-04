"""Profiler domain: CPU profiling and code coverage."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ProfilerDomain(BaseDomain):
    """Wrapper for the CDP Profiler domain.

    Provides CPU profiling and precise code coverage collection.
    Start a profile, execute code, then stop to retrieve the profile
    data. Coverage can be collected at function or block granularity.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Profiler domain."""
        return await self._call("Profiler.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Profiler domain."""
        return await self._call("Profiler.disable")

    async def start(self) -> dict[str, Any]:
        """Start collecting CPU profile.

        Returns:
            Dict containing the profiling ``timestamp``.
        """
        return await self._call("Profiler.start")

    async def stop(self) -> dict[str, Any]:
        """Stop collecting CPU profile and return the profile data.

        Returns:
            Dict with a ``profile`` key containing nodes, samples,
            timeDeltas, and metadata.
        """
        return await self._call("Profiler.stop")

    async def start_precise_coverage(
        self,
        call_count: bool = False,
        detailed: bool = False,
        allow_triggered_updates: bool = False,
    ) -> dict[str, Any]:
        """Enable precise code coverage collection.

        Args:
            call_count: Whether to collect per-function call counts.
            detailed: Whether to collect block-level coverage.
            allow_triggered_updates: Allow triggered updates to be sent
                as ``Profiler.preciseCoverageDeltaUpdate`` events.

        Returns:
            Dict with the ``timestamp`` of coverage start.
        """
        params: dict[str, Any] = {
            "callCount": call_count,
            "detailed": detailed,
            "allowTriggeredUpdates": allow_triggered_updates,
        }
        return await self._call("Profiler.startPreciseCoverage", params)

    async def stop_precise_coverage(self) -> dict[str, Any]:
        """Disable precise code coverage collection.

        Returns:
            Dict with the ``timestamp`` of coverage stop.
        """
        return await self._call("Profiler.stopPreciseCoverage")

    async def take_precise_coverage(self) -> dict[str, Any]:
        """Collect precise code coverage data.

        Returns:
            Dict with a ``result`` list of coverage entries, each
            containing ``scriptId``, ``url``, and ``functions`` with
            ranges and hit counts.
        """
        return await self._call("Profiler.takePreciseCoverage")

    async def get_best_effort_coverage(self) -> dict[str, Any]:
        """Collect best-effort coverage data without precise mode.

        Returns:
            Dict with a ``result`` list of coverage entries.
        """
        return await self._call("Profiler.getBestEffortCoverage")

    async def set_sampling_interval(
        self,
        interval: int,
    ) -> dict[str, Any]:
        """Set the CPU sampling interval in microseconds.

        Args:
            interval: Sampling interval in microseconds.
        """
        return await self._call(
            "Profiler.setSamplingInterval",
            {"interval": interval},
        )
