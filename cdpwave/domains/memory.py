"""Memory domain: DOM counters, sampling profiles, and GC control."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class MemoryDomain(BaseDomain):
    """Wrapper for the CDP Memory domain.

    Provides access to memory metrics (DOM nodes, JS heap), sampling
    profiles, leak detection preparation, and forced garbage collection.
    """

    async def get_dom_counters(self) -> dict[str, Any]:
        """Get current DOM node and document counts.

        Returns:
            Dict with ``documents``, ``nodes``, and ``jsEventListeners``.
        """
        return await self._call("Memory.getDOMCounters")

    async def prepare_for_leak_detection(self) -> dict[str, Any]:
        """Prepare the browser for leak detection by clearing caches."""
        return await self._call("Memory.prepareForLeakDetection")

    async def force_garbage_collection(self) -> dict[str, Any]:
        """Force a garbage collection cycle.

        Triggers a full GC cycle in the browser process,
        reclaiming unreachable objects across all V8 isolates.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Memory.forceGarbageCollection")

    async def set_pressure_notifications_suppressed(
        self,
        suppressed: bool,
    ) -> dict[str, Any]:
        """Suppress or enable memory pressure notifications.

        Args:
            suppressed: Whether to suppress notifications.
        """
        return await self._call(
            "Memory.setPressureNotificationsSuppressed",
            {"suppressed": suppressed},
        )

    async def simulate_pressure_notification(
        self,
        level: str,
    ) -> dict[str, Any]:
        """Simulate a memory pressure notification.

        Args:
            level: Pressure level (``"moderate"`` or ``"critical"``).
        """
        return await self._call(
            "Memory.simulatePressureNotification",
            {"level": level},
        )

    async def start_sampling(
        self,
        sampling_interval: int | None = None,
        suppress_randomness: bool | None = None,
    ) -> dict[str, Any]:
        """Start memory sampling.

        Args:
            sampling_interval: Interval in bytes between samples.
            suppress_randomness: Whether to suppress randomness.
        """
        params: dict[str, Any] = {}
        if sampling_interval is not None:
            params["samplingInterval"] = sampling_interval
        if suppress_randomness is not None:
            params["suppressRandomness"] = suppress_randomness
        return await self._call("Memory.startSampling", params)

    async def stop_sampling(self) -> dict[str, Any]:
        """Stop memory sampling.

        Stops the memory sampling that was started by
        ``start_sampling``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Memory.stopSampling")

    async def get_sampling_profile(self) -> dict[str, Any]:
        """Get the current memory sampling profile.

        Returns:
            Dict with ``samples`` and ``modules``.
        """
        return await self._call("Memory.getSamplingProfile")

    async def forcibly_purge_javascript_memory(self) -> dict[str, Any]:
        """Forcibly purge JavaScript memory across all V8 isolates."""
        return await self._call("Memory.forciblyPurgeJavaScriptMemory")

    async def get_all_time_sampling_profile(self) -> dict[str, Any]:
        """Get the all-time memory sampling profile.

        Returns:
            Dict with ``samples`` and ``modules``.
        """
        return await self._call("Memory.getAllTimeSamplingProfile")

    async def get_browser_sampling_profile(self) -> dict[str, Any]:
        """Get the browser process memory sampling profile.

        Returns:
            Dict with ``samples`` and ``modules``.
        """
        return await self._call("Memory.getBrowserSamplingProfile")

    async def get_dom_counters_for_leak_detection(self) -> dict[str, Any]:
        """Get DOM counters for leak detection.

        Returns:
            Dict with ``counters`` list.
        """
        return await self._call("Memory.getDOMCountersForLeakDetection")
