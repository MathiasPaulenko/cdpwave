"""PerformanceTimeline domain: timeline events for performance recordings."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PerformanceTimelineDomain(BaseDomain):
    """Wrapper for the CDP PerformanceTimeline domain.

    Emits ``PerformanceTimeline.timelineEvent`` events containing
    recorded timeline data (LCP, FID, CLS, etc.).

    Subscribe to events via ``session.on("PerformanceTimeline.timelineEvent", handler)``.
    """

    async def enable(
        self,
        event_types: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Enable performance timeline tracking.

        Args:
            event_types: List of event type filters, each with ``name``
                and optional ``eventCategory``.
        """
        return await self._call(
            "PerformanceTimeline.enable",
            {"eventTypes": event_types},
        )
