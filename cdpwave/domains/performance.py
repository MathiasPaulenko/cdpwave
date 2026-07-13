"""Performance domain: collecting and reporting run-time metrics.

Events:

    ``Performance.metrics`` — current values of run-time metrics.
    Parameters: ``metrics`` (list[Metric]), ``title`` (str).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PerformanceDomain(BaseDomain):
    """Wrapper for the CDP Performance domain.

    Provides access to run-time execution metrics such as JS heap size,
    DOM nodes, event listeners, and timeline timestamps. Enable the domain
    to receive ``Performance.metrics`` events.

    Event ``Performance.metrics``:
        - ``metrics``: list of Metric dicts (``name``: str, ``value``: float)
        - ``title``: str — timestamp title
    """

    async def disable(self) -> dict[str, Any]:
        """Disable collecting and reporting metrics.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Performance.disable")

    async def enable(self, time_domain: str | None = None) -> dict[str, Any]:
        """Enable collecting and reporting metrics.

        Args:
            time_domain: Optional time domain to use for collecting and
                reporting duration metrics. Allowed values: ``"timeTicks"``
                and ``"threadTicks"``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``time_domain`` is not a string or ``None``.
            ValueError: If ``time_domain`` is a non-empty string that is
                not ``"timeTicks"`` or ``"threadTicks"``.
        """
        params: dict[str, Any] | None = None
        if time_domain is not None:
            if not isinstance(time_domain, str):
                raise TypeError("time_domain must be a string or None")
            if time_domain:
                if time_domain not in ("timeTicks", "threadTicks"):
                    raise ValueError(
                        "time_domain must be 'timeTicks' or 'threadTicks'"
                    )
                params = {"timeDomain": time_domain}
        return await self._call("Performance.enable", params)

    async def get_metrics(self) -> dict[str, Any]:
        """Retrieve current values of run-time metrics.

        Returns:
            Dict with a ``metrics`` list, each containing ``name`` (str)
            and ``value`` (float) keys (e.g. ``"JSHeapUsedSize"``,
            ``"Nodes"``).
        """
        return await self._call("Performance.getMetrics")

    async def set_time_domain(self, time_domain: str) -> dict[str, Any]:
        """Sets time domain to use for collecting and reporting duration metrics.

        Deprecated and experimental. Must be called before enabling metrics
        collection. Calling this method while metrics collection is enabled
        returns an error.

        Args:
            time_domain: Time domain. Allowed values: ``"timeTicks"`` and
                ``"threadTicks"``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``time_domain`` is not a string.
            ValueError: If ``time_domain`` is not ``"timeTicks"`` or
                ``"threadTicks"``.
        """
        if not isinstance(time_domain, str):
            raise TypeError("time_domain must be a string")
        if time_domain not in ("timeTicks", "threadTicks"):
            raise ValueError(
                "time_domain must be 'timeTicks' or 'threadTicks'"
            )
        return await self._call(
            "Performance.setTimeDomain",
            {"timeDomain": time_domain},
        )
