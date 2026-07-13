"""Memory domain: DOM counters, sampling profiles, and pressure control.

Types:

    ``PressureLevel`` — str. Memory pressure level.  Values:
    ``"moderate"``, ``"critical"``.

    ``SamplingProfileNode`` — dict. Heap profile sample.
    Fields: ``size`` (float — size of the sampled allocation),
    ``total`` (float — total bytes attributed to this sample),
    ``stack`` (list[str] — execution stack at the point of
    allocation).

    ``SamplingProfile`` — dict. Array of heap profile samples.
    Fields: ``samples`` (list[SamplingProfileNode]),
    ``modules`` (list[Module]).

    ``Module`` — dict. Executable module information.  Fields:
    ``name`` (str — name of the module), ``uuid`` (str — UUID of
    the module), ``baseAddress`` (str — base address where the
    module is loaded into memory, encoded as a decimal or
    hexadecimal (0x prefixed) string), ``size`` (float — size of
    the module in bytes).

    ``DOMCounter`` — dict. DOM object counter data.  Fields:
    ``name`` (str — object name, note: object names should be
    presumed volatile and clients should not expect the returned
    names to be consistent across runs), ``count`` (int — object
    count).

No events.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_PRESSURE_LEVELS = frozenset({"moderate", "critical"})


class MemoryDomain(BaseDomain):
    """Wrapper for the CDP Memory domain.

    Provides access to DOM counters, native memory sampling
    profiles, leak detection preparation, and memory pressure
    notification control.

    **Experimental** — marked as Experimental in the CDP spec.

    No events.
    """

    async def get_dom_counters(self) -> dict[str, Any]:
        """Get current DOM object counters.

        Returns:
            Dict with ``documents`` (int), ``nodes`` (int), and
            ``jsEventListeners`` (int).
        """
        return await self._call("Memory.getDOMCounters")

    async def get_dom_counters_for_leak_detection(self) -> dict[str, Any]:
        """Get DOM object counters after preparing renderer for leak detection.

        Returns:
            Dict with ``counters`` (list[DOMCounter] — DOM object
            counters).
        """
        return await self._call("Memory.getDOMCountersForLeakDetection")

    async def prepare_for_leak_detection(self) -> dict[str, Any]:
        """Prepare for leak detection.

        Terminates workers, stops spellcheckers, drops
        non-essential internal caches, runs garbage collections,
        etc.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Memory.prepareForLeakDetection")

    async def forcibly_purge_javascript_memory(self) -> dict[str, Any]:
        """Forcibly purge JavaScript memory.

        Simulates OomIntervention by purging V8 memory.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Memory.forciblyPurgeJavaScriptMemory")

    async def set_pressure_notifications_suppressed(
        self,
        suppressed: bool,
    ) -> dict[str, Any]:
        """Enable/disable suppressing memory pressure notifications in all processes.

        Args:
            suppressed: If true, memory pressure notifications will
                be suppressed.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``suppressed`` is not a bool.
        """
        if not isinstance(suppressed, bool):
            raise TypeError(
                f"suppressed must be a bool, "
                f"got {type(suppressed).__name__}"
            )
        return await self._call(
            "Memory.setPressureNotificationsSuppressed",
            {"suppressed": suppressed},
        )

    async def simulate_pressure_notification(
        self,
        level: str,
    ) -> dict[str, Any]:
        """Simulate a memory pressure notification in all processes.

        Args:
            level: Memory pressure level of the notification.
                Must be ``"moderate"`` or ``"critical"``.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``level`` is not a str.
            ValueError: If ``level`` is not ``"moderate"`` or
                ``"critical"``.
        """
        if not isinstance(level, str):
            raise TypeError(
                f"level must be a str, "
                f"got {type(level).__name__}"
            )
        if level not in _VALID_PRESSURE_LEVELS:
            raise ValueError(
                f"level must be 'moderate' or 'critical', "
                f"got {level!r}"
            )
        return await self._call(
            "Memory.simulatePressureNotification",
            {"level": level},
        )

    async def start_sampling(
        self,
        sampling_interval: int = 0,
        suppress_randomness: bool = False,
    ) -> dict[str, Any]:
        """Start collecting native memory profile.

        Args:
            sampling_interval: Average number of bytes between
                samples.  Omitted from the request when 0 (the
                default), letting the browser choose.
            suppress_randomness: Do not randomize intervals between
                samples.  Always sent (defaults to False).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``sampling_interval`` is not an int (bool
                is rejected) or ``suppress_randomness`` is not a
                bool.
        """
        if isinstance(sampling_interval, bool) or not isinstance(
            sampling_interval, int
        ):
            raise TypeError(
                f"sampling_interval must be an int, "
                f"got {type(sampling_interval).__name__}"
            )
        if not isinstance(suppress_randomness, bool):
            raise TypeError(
                f"suppress_randomness must be a bool, "
                f"got {type(suppress_randomness).__name__}"
            )
        params: dict[str, Any] = {"suppressRandomness": suppress_randomness}
        if sampling_interval:
            params["samplingInterval"] = sampling_interval
        return await self._call("Memory.startSampling", params)

    async def stop_sampling(self) -> dict[str, Any]:
        """Stop collecting native memory profile.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Memory.stopSampling")

    async def get_all_time_sampling_profile(self) -> dict[str, Any]:
        """Retrieve native memory allocations profile collected since renderer process startup.

        Returns:
            Dict with ``profile`` (SamplingProfile).
        """
        return await self._call("Memory.getAllTimeSamplingProfile")

    async def get_browser_sampling_profile(self) -> dict[str, Any]:
        """Retrieve native memory allocations profile collected since browser process startup.

        Returns:
            Dict with ``profile`` (SamplingProfile).
        """
        return await self._call("Memory.getBrowserSamplingProfile")

    async def get_sampling_profile(self) -> dict[str, Any]:
        """Retrieve native memory allocations profile collected since last startSampling call.

        Returns:
            Dict with ``profile`` (SamplingProfile).
        """
        return await self._call("Memory.getSamplingProfile")
