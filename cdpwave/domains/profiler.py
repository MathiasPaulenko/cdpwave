"""Profiler domain: CPU profiling and code coverage.

Events:

    ``Profiler.consoleProfileFinished`` — sent when a console profile
    finishes.  Parameters: ``id`` (str), ``location`` (Location),
    ``profile`` (Profile), ``title`` (str, optional).

    ``Profiler.consoleProfileStarted`` — sent when new profile recording
    is started via console.profile().  Parameters: ``id`` (str),
    ``location`` (Location), ``title`` (str, optional).

    ``Profiler.preciseCoverageDeltaUpdate`` — **Experimental.** Sent when
    precise coverage delta is available.  Parameters: ``timestamp``
    (float), ``occasion`` (str), ``result`` (list[ScriptCoverage]).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ProfilerDomain(BaseDomain):
    """Wrapper for the CDP Profiler domain.

    Provides CPU profiling and precise code coverage collection.
    Start a profile, execute code, then stop to retrieve the profile
    data. Coverage can be collected at function or block granularity.

    Events:

    - ``Profiler.consoleProfileFinished``: Params ``id`` (str),
      ``location`` (dict), ``profile`` (dict), ``title`` (str, optional).
    - ``Profiler.consoleProfileStarted``: Params ``id`` (str),
      ``location`` (dict), ``title`` (str, optional).
    - ``Profiler.preciseCoverageDeltaUpdate``: **Experimental.** Params
      ``timestamp`` (float), ``occasion`` (str), ``result``
      (list[ScriptCoverage]).

    Subscribe via ``session.on("Profiler.consoleProfileFinished", handler)``.
    """

    async def disable(self) -> dict[str, Any]:
        """Disable the Profiler domain.

        Deactivates Profiler domain events and reporting.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Profiler.disable")

    async def enable(self) -> dict[str, Any]:
        """Enable the Profiler domain.

        Activates Profiler domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Profiler.enable")

    async def get_best_effort_coverage(self) -> dict[str, Any]:
        """Collect best-effort coverage data without precise mode.

        The coverage data may be incomplete due to garbage collection.

        Returns:
            Dict with a ``result`` list of ``ScriptCoverage`` entries,
            each containing ``scriptId``, ``url``, and ``functions`` with
            ranges and hit counts.
        """
        return await self._call("Profiler.getBestEffortCoverage")

    async def set_sampling_interval(
        self,
        interval: int,
    ) -> dict[str, Any]:
        """Set the CPU sampling interval.

        Must be called before CPU profiles recording started.

        Args:
            interval: New sampling interval in microseconds.

        Raises:
            TypeError: If ``interval`` is not an int.
        """
        if not isinstance(interval, int) or isinstance(interval, bool):
            raise TypeError(
                f"interval must be an int, got {type(interval).__name__}"
            )
        return await self._call(
            "Profiler.setSamplingInterval",
            {"interval": interval},
        )

    async def start(self) -> dict[str, Any]:
        """Start collecting CPU profile.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Profiler.start")

    async def start_precise_coverage(
        self,
        call_count: bool = False,
        detailed: bool = False,
        allow_triggered_updates: bool = False,
    ) -> dict[str, Any]:
        """Enable precise code coverage collection.

        Coverage data for JavaScript executed before enabling precise
        code coverage may be incomplete. Enabling prevents running
        optimized code and resets execution counters.

        Args:
            call_count: Collect accurate call counts beyond simple
                'covered' or 'not covered'.
            detailed: Collect block-based coverage.
            allow_triggered_updates: Allow the backend to send updates
                on its own initiative as
                ``Profiler.preciseCoverageDeltaUpdate`` events.

        Returns:
            Dict with the ``timestamp`` (float) of coverage start.

        Raises:
            TypeError: If any argument is not a bool.
        """
        if not isinstance(call_count, bool):
            raise TypeError(
                f"call_count must be a bool, got {type(call_count).__name__}"
            )
        if not isinstance(detailed, bool):
            raise TypeError(
                f"detailed must be a bool, got {type(detailed).__name__}"
            )
        if not isinstance(allow_triggered_updates, bool):
            raise TypeError(
                f"allow_triggered_updates must be a bool, "
                f"got {type(allow_triggered_updates).__name__}"
            )
        params: dict[str, Any] = {
            "callCount": call_count,
            "detailed": detailed,
            "allowTriggeredUpdates": allow_triggered_updates,
        }
        return await self._call("Profiler.startPreciseCoverage", params)

    async def stop(self) -> dict[str, Any]:
        """Stop collecting CPU profile and return the profile data.

        Returns:
            Dict with a ``profile`` key containing a ``Profile`` object
            with ``nodes``, ``startTime``, ``endTime``, ``samples``,
            and ``timeDeltas``.
        """
        return await self._call("Profiler.stop")

    async def stop_precise_coverage(self) -> dict[str, Any]:
        """Disable precise code coverage collection.

        Disabling releases unnecessary execution count records and
        allows executing optimized code.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Profiler.stopPreciseCoverage")

    async def take_precise_coverage(self) -> dict[str, Any]:
        """Collect precise code coverage data and reset execution counters.

        Precise code coverage needs to have started.

        Returns:
            Dict with a ``result`` list of ``ScriptCoverage`` entries
            (each containing ``scriptId``, ``url``, and ``functions``
            with ranges and hit counts) and a ``timestamp`` (float).
        """
        return await self._call("Profiler.takePreciseCoverage")
