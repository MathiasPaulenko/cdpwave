"""PerformanceTimeline domain: timeline events for performance recordings.

This is an event-only domain — it emits ``PerformanceTimeline.timelineEvent``
events when enabled. There are no commands beyond what the browser
sends automatically during timeline recordings.
"""

from cdpwave.domains.base import BaseDomain


class PerformanceTimelineDomain(BaseDomain):
    """Wrapper for the CDP PerformanceTimeline domain.

    Event-only domain that emits ``PerformanceTimeline.timelineEvent``
    events containing recorded timeline data (LCP, FID, CLS, etc.).

    Subscribe to events via ``session.on("PerformanceTimeline.timelineEvent", handler)``.
    """
