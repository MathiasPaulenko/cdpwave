"""Performance domain: runtime metrics and timeline events."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PerformanceDomain(BaseDomain):
    """Wrapper for the CDP Performance domain.

    Provides access to runtime performance metrics such as JS heap size,
    DOM nodes, event listeners, and timeline timestamps. Enable the domain
    to receive ``Performance.metrics`` events.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable collecting performance metrics.

        Activates periodic reporting of runtime performance metrics
        such as JS heap size, DOM nodes, and event listeners.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Performance.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable collecting performance metrics.

        Stops periodic reporting of runtime performance metrics.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Performance.disable")

    async def get_metrics(self) -> dict[str, Any]:
        """Retrieve current runtime performance metrics.

        Returns:
            Dict with a ``metrics`` list, each containing ``name`` and
            ``value`` keys (e.g. ``"JSHeapUsedSize"``, ``"Nodes"``).
        """
        return await self._call("Performance.getMetrics")

    async def set_time_domain(self, time_domain: str) -> dict[str, Any]:
        """Set the time domain for performance timestamps.

        Args:
            time_domain: ``"timeTicks"`` for thread ticks or
                ``"wallTime"`` for wall clock time.
        """
        return await self._call(
            "Performance.setTimeDomain",
            {"timeDomain": time_domain},
        )
