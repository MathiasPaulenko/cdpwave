"""Tracing domain: performance tracing and timeline recording.

Types:

    ``RecordMode`` — str. Trace record mode.  Values:
    ``"recordUntilFull"``, ``"recordContinuously"``,
    ``"recordAsMuchAsPossible"``, ``"echoToConsole"``.

    ``StreamFormat`` — str. Trace stream format.  Values:
    ``"json"``, ``"proto"``.

    ``StreamCompression`` — str. Trace stream compression.  Values:
    ``"none"``, ``"gzip"``.

    ``MemoryDumpLevelOfDetail`` — str. Memory dump level of detail.
    Values: ``"background"``, ``"light"``, ``"detailed"``.

    ``Backend`` — str. Tracing backend.  Values: ``"auto"``,
    ``"chrome"``, ``"system"``.

    ``TransferMode`` — str. Trace transfer mode.  Values:
    ``"ReportEvents"``, ``"ReturnAsStream"``.

    ``TraceConfig`` — dict. Trace configuration.  Fields:
    ``recordMode`` (str, optional — RecordMode enum),
    ``traceBufferSizeInKb`` (float, optional),
    ``enableSampling`` (bool — always sent),
    ``enableSystrace`` (bool — always sent),
    ``enableArgumentFilter`` (bool — always sent),
    ``includedCategories`` (list[str], optional),
    ``excludedCategories`` (list[str], optional),
    ``syntheticDelays`` (list[str], optional),
    ``memoryDumpConfig`` (dict, optional — MemoryDumpConfig).

    ``MemoryDumpConfig`` — dict. Memory dump configuration (empty
    struct, no fields).

Events:
    Tracing.bufferUsage: Issued when the tracing buffer usage crosses
        a threshold.  Parameters:
        percentFull (float, optional),
        eventCount (float, optional),
        value (float, optional).

    Tracing.dataCollected: Issued when trace data is collected.
        Parameters:
        value (list — sequence of trace events as JSON objects).

    Tracing.tracingComplete: Issued when tracing is complete.
        Parameters:
        dataLossOccurred (bool — always sent),
        stream (str, optional — io.StreamHandle),
        traceFormat (str, optional — StreamFormat),
        streamCompression (str, optional — StreamCompression).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_TRANSFER_MODES = frozenset({"ReportEvents", "ReturnAsStream"})
_VALID_STREAM_FORMATS = frozenset({"json", "proto"})
_VALID_STREAM_COMPRESSIONS = frozenset({"none", "gzip"})
_VALID_LEVELS_OF_DETAIL = frozenset({"background", "light", "detailed"})
_VALID_BACKENDS = frozenset({"auto", "chrome", "system"})
_VALID_RECORD_MODES = frozenset({
    "recordUntilFull",
    "recordContinuously",
    "recordAsMuchAsPossible",
    "echoToConsole",
})


class TracingDomain(BaseDomain):
    """Wrapper for the CDP Tracing domain.

    Provides performance tracing capabilities.  Start recording with
    a trace configuration, then end to receive the trace data as a
    stream or events.

    **Experimental** — marked as Experimental in the CDP spec.

    Events:
        Tracing.bufferUsage: Buffer usage update.
        Tracing.dataCollected: Trace data collected.
        Tracing.tracingComplete: Tracing complete.
    """

    async def end(self) -> dict[str, Any]:
        """Stop trace events collection.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Tracing.end")

    async def get_categories(self) -> dict[str, Any]:
        """Get supported tracing categories.

        Returns:
            Dict with ``categories`` (list[str] — category names).
        """
        return await self._call("Tracing.getCategories")

    async def get_track_event_descriptor(self) -> dict[str, Any]:
        """Retrieve the track event descriptor.

        The descriptor is base64-encoded.  Go source decodes it to
        ``[]byte``.

        Returns:
            Dict with ``descriptor`` (str — base64-encoded track
            event descriptor).
        """
        return await self._call("Tracing.getTrackEventDescriptor")

    async def record_clock_sync_marker(
        self,
        sync_id: str,
    ) -> dict[str, Any]:
        """Record a clock sync marker.

        Args:
            sync_id: Unique ID for the sync marker.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``sync_id`` is not a str.
        """
        if not isinstance(sync_id, str):
            raise TypeError(
                f"sync_id must be a str, "
                f"got {type(sync_id).__name__}"
            )
        return await self._call(
            "Tracing.recordClockSyncMarker",
            {"syncId": sync_id},
        )

    async def request_memory_dump(
        self,
        deterministic: bool = False,
        level_of_detail: str | None = None,
    ) -> dict[str, Any]:
        """Request a global memory dump.

        Args:
            deterministic: Enables deterministic memory dump.  Always sent
                (defaults to False).
            level_of_detail: Memory dump level of detail.  Must be
                ``"background"``, ``"light"``, or ``"detailed"``.
                Omitted from the request when None (the default).

        Returns:
            Dict with ``dumpGuid`` (str — memory dump GUID) and
            ``success`` (bool — whether the dump was successful).

        Raises:
            TypeError: If ``deterministic`` is not a bool or
                ``level_of_detail`` is not a str.
            ValueError: If ``level_of_detail`` is not ``"background"``,
                ``"light"``, or ``"detailed"``.
        """
        if not isinstance(deterministic, bool):
            raise TypeError(
                f"deterministic must be a bool, "
                f"got {type(deterministic).__name__}"
            )
        if level_of_detail is not None:
            if not isinstance(level_of_detail, str):
                raise TypeError(
                    f"level_of_detail must be a str, "
                    f"got {type(level_of_detail).__name__}"
                )
            if level_of_detail and level_of_detail not in _VALID_LEVELS_OF_DETAIL:
                raise ValueError(
                    f"level_of_detail must be 'background', 'light', "
                    f"or 'detailed', got {level_of_detail!r}"
                )
        params: dict[str, Any] = {"deterministic": deterministic}
        if level_of_detail:
            params["levelOfDetail"] = level_of_detail
        return await self._call("Tracing.requestMemoryDump", params)

    async def start(
        self,
        buffer_usage_reporting_interval: float | None = None,
        transfer_mode: str | None = None,
        stream_format: str | None = None,
        stream_compression: str | None = None,
        trace_config: dict[str, Any] | None = None,
        perfetto_config: str | None = None,
        tracing_backend: str | None = None,
        screenshot_max_size: int | None = None,
        screenshot_max_count: int | None = None,
    ) -> dict[str, Any]:
        """Start trace events collection.

        All parameters are optional (omitempty,omitzero in Go source —
        only sent if truthy).

        Args:
            buffer_usage_reporting_interval: Interval in seconds for
                buffer usage reports.  Omitted when 0 or None.
            transfer_mode: ``"ReportEvents"`` or ``"ReturnAsStream"``.
                Omitted when None.
            stream_format: ``"json"`` or ``"proto"``.  Omitted when
                None.
            stream_compression: ``"none"`` or ``"gzip"``.  Omitted
                when None.
            trace_config: TraceConfig dict.  Omitted when None.
            perfetto_config: Base64-encoded Perfetto config string.
                Omitted when None or empty.
            tracing_backend: ``"auto"``, ``"chrome"``, or
                ``"system"``.  Omitted when None.
            screenshot_max_size: Maximum screenshot size.  Omitted
                when 0 or None.
            screenshot_max_count: Maximum screenshot count.  Omitted
                when 0 or None.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``buffer_usage_reporting_interval`` is not
                a float, ``transfer_mode``/``stream_format``/
                ``stream_compression``/``tracing_backend`` are not
                str, ``trace_config`` is not a dict,
                ``perfetto_config`` is not a str, or
                ``screenshot_max_size``/``screenshot_max_count`` are
                not int (bool is rejected).
            ValueError: If ``transfer_mode`` is not ``"ReportEvents"``
                or ``"ReturnAsStream"``, ``stream_format`` is not
                ``"json"`` or ``"proto"``, ``stream_compression`` is
                not ``"none"`` or ``"gzip"``, or ``tracing_backend``
                is not ``"auto"``, ``"chrome"``, or ``"system"``.
        """
        if buffer_usage_reporting_interval is not None and (
            isinstance(buffer_usage_reporting_interval, bool)
            or not isinstance(buffer_usage_reporting_interval, (int, float))
        ):
            raise TypeError(
                f"buffer_usage_reporting_interval must be a float, "
                f"got {type(buffer_usage_reporting_interval).__name__}"
            )
        if transfer_mode is not None:
            if not isinstance(transfer_mode, str):
                raise TypeError(
                    f"transfer_mode must be a str, "
                    f"got {type(transfer_mode).__name__}"
                )
            if transfer_mode and transfer_mode not in _VALID_TRANSFER_MODES:
                raise ValueError(
                    f"transfer_mode must be 'ReportEvents' or "
                    f"'ReturnAsStream', got {transfer_mode!r}"
                )
        if stream_format is not None:
            if not isinstance(stream_format, str):
                raise TypeError(
                    f"stream_format must be a str, "
                    f"got {type(stream_format).__name__}"
                )
            if stream_format and stream_format not in _VALID_STREAM_FORMATS:
                raise ValueError(
                    f"stream_format must be 'json' or 'proto', "
                    f"got {stream_format!r}"
                )
        if stream_compression is not None:
            if not isinstance(stream_compression, str):
                raise TypeError(
                    f"stream_compression must be a str, "
                    f"got {type(stream_compression).__name__}"
                )
            if stream_compression and stream_compression not in _VALID_STREAM_COMPRESSIONS:
                raise ValueError(
                    f"stream_compression must be 'none' or 'gzip', "
                    f"got {stream_compression!r}"
                )
        if trace_config is not None and not isinstance(trace_config, dict):
            raise TypeError(
                f"trace_config must be a dict, "
                f"got {type(trace_config).__name__}"
            )
        if trace_config is not None and "recordMode" in trace_config:
            rm = trace_config["recordMode"]
            if not isinstance(rm, str):
                raise TypeError("trace_config['recordMode'] must be a str")
            if rm not in _VALID_RECORD_MODES:
                raise ValueError(
                    f"trace_config['recordMode'] must be one of "
                    f"{sorted(_VALID_RECORD_MODES)}, got {rm!r}"
                )
        if perfetto_config is not None and not isinstance(perfetto_config, str):
            raise TypeError(
                f"perfetto_config must be a str, "
                f"got {type(perfetto_config).__name__}"
            )
        if tracing_backend is not None:
            if not isinstance(tracing_backend, str):
                raise TypeError(
                    f"tracing_backend must be a str, "
                    f"got {type(tracing_backend).__name__}"
                )
            if tracing_backend and tracing_backend not in _VALID_BACKENDS:
                raise ValueError(
                    f"tracing_backend must be 'auto', 'chrome', or "
                    f"'system', got {tracing_backend!r}"
                )
        if screenshot_max_size is not None and (
            isinstance(screenshot_max_size, bool)
            or not isinstance(screenshot_max_size, int)
        ):
            raise TypeError(
                f"screenshot_max_size must be an int, "
                f"got {type(screenshot_max_size).__name__}"
            )
        if screenshot_max_count is not None and (
            isinstance(screenshot_max_count, bool)
            or not isinstance(screenshot_max_count, int)
        ):
            raise TypeError(
                f"screenshot_max_count must be an int, "
                f"got {type(screenshot_max_count).__name__}"
            )
        params: dict[str, Any] = {}
        if buffer_usage_reporting_interval:
            params["bufferUsageReportingInterval"] = (
                buffer_usage_reporting_interval
            )
        if transfer_mode:
            params["transferMode"] = transfer_mode
        if stream_format:
            params["streamFormat"] = stream_format
        if stream_compression:
            params["streamCompression"] = stream_compression
        if trace_config:
            params["traceConfig"] = trace_config
        if perfetto_config:
            params["perfettoConfig"] = perfetto_config
        if tracing_backend:
            params["tracingBackend"] = tracing_backend
        if screenshot_max_size:
            params["screenshotMaxSize"] = screenshot_max_size
        if screenshot_max_count:
            params["screenshotMaxCount"] = screenshot_max_count
        return await self._call("Tracing.start", params or None)
