"""PerformanceTimeline domain: timeline events for performance recordings.

Experimental domain. Reporting of performance timeline events, as specified in
https://w3c.github.io/performance-timeline/#dom-performanceobserver.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PerformanceTimelineDomain(BaseDomain):
    """Wrapper for the CDP PerformanceTimeline domain.

    **Experimental.**

    Emits ``PerformanceTimeline.timelineEventAdded`` events containing
    recorded timeline data (LCP, CLS, etc.).

    Events:

    - ``PerformanceTimeline.timelineEventAdded``: Sent when a performance
      timeline event is added.  Params: ``event`` (dict — a ``TimelineEvent``
      with fields ``frameId`` (str), ``type`` (str), ``name`` (str),
      ``time`` (float), ``duration`` (float, optional),
      ``lcpDetails`` (dict, optional), ``layoutShiftDetails`` (dict, optional)).

    Subscribe via ``session.on("PerformanceTimeline.timelineEventAdded", handler)``.
    """

    async def enable(
        self,
        event_types: list[str],
    ) -> dict[str, Any]:
        """Enable performance timeline tracking.

        Previously buffered events are reported before the method returns.

        Args:
            event_types: List of event type strings to report, as specified
                in
                https://w3c.github.io/performance-timeline/#dom-performanceentry-entrytype
                (e.g. ``"largest-contentful-paint"``, ``"layout-shift"``).
                The specified filter overrides any previous filters; passing
                an empty list disables recording. Note that not all types
                exposed to the web platform are currently supported.

        Returns:
            Empty dict (no return value from CDP).
        """
        if not isinstance(event_types, list):
            raise TypeError(
                f"event_types must be a list[str], got {type(event_types).__name__}"
            )
        for i, et in enumerate(event_types):
            if not isinstance(et, str):
                raise TypeError(
                    f"event_types[{i}] must be a str, got {type(et).__name__}"
                )
        return await self._call(
            "PerformanceTimeline.enable",
            {"eventTypes": event_types},
        )
