"""Tracing domain: performance tracing and timeline recording."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TracingDomain(BaseDomain):
    """Wrapper for the CDP Tracing domain.

    Provides performance tracing capabilities. Start recording with
    categories, then end to receive the trace data as a stream.
    """

    async def start(
        self,
        categories: str | None = None,
        options: str | None = None,
        buffer_usage_reporting_interval: float | None = None,
        transfer_mode: str = "ReportEvents",
        stream_format: str = "json",
        stream_compression: str = "none",
        trace_type: str | None = None,
    ) -> dict[str, Any]:
        """Start trace event recording.

        Args:
            categories: Comma-separated category filter (e.g.
                ``"-*,devtools.timeline"``).
            options: Tracing options string.
            buffer_usage_reporting_interval: Interval in seconds for
                buffer usage reports.
            transfer_mode: ``"ReportEvents"`` or ``"ReturnAsStream"``.
            stream_format: ``"json"``, ``"proto"``.
            stream_compression: ``"none"``, ``"gzip"``.
            trace_type: Trace type (e.g. ``"devtools-test"``).
        """
        params: dict[str, Any] = {
            "transferMode": transfer_mode,
            "streamFormat": stream_format,
            "streamCompression": stream_compression,
        }
        if categories is not None:
            params["categories"] = categories
        if options is not None:
            params["options"] = options
        if buffer_usage_reporting_interval is not None:
            params["bufferUsageReportingInterval"] = (
                buffer_usage_reporting_interval
            )
        if trace_type is not None:
            params["traceType"] = trace_type
        return await self._call("Tracing.start", params)

    async def end(self) -> dict[str, Any]:
        """Stop trace event recording.

        Returns:
            Dict with trace data or stream handle depending on transfer mode.
        """
        return await self._call("Tracing.end")

    async def get_categories(self) -> dict[str, Any]:
        """Get supported tracing categories.

        Returns:
            Dict with ``categories`` list of category names.
        """
        return await self._call("Tracing.getCategories")

    async def record_clock_sync_marker(
        self,
        sync_id: str,
    ) -> dict[str, Any]:
        """Record a clock sync marker for trace timing.

        Args:
            sync_id: Unique ID for the sync marker.
        """
        return await self._call(
            "Tracing.recordClockSyncMarker",
            {"syncId": sync_id},
        )

    async def request_clock_sync_marker(self) -> dict[str, Any]:
        """Request a clock sync marker from the browser.

        Returns:
            Dict with ``syncId`` for the marker.
        """
        return await self._call("Tracing.requestClockSyncMarker")
