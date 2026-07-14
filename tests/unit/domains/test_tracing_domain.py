"""Unit tests for the Tracing domain."""

import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.tracing import TracingDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestTracingDomain:
    """Basic tests for all 6 Tracing methods."""

    async def test_end(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.end()
        assert fake.last_call == ("Tracing.end", None)

    async def test_get_categories(self) -> None:
        fake = FakeSender({"categories": ["disabled-by-default-devtools.timeline"]})
        domain = TracingDomain(fake)
        result = await domain.get_categories()
        assert fake.last_call == ("Tracing.getCategories", None)
        assert "categories" in result

    async def test_get_track_event_descriptor(self) -> None:
        fake = FakeSender({"descriptor": "dGVzdA=="})
        domain = TracingDomain(fake)
        result = await domain.get_track_event_descriptor()
        assert fake.last_call == ("Tracing.getTrackEventDescriptor", None)
        assert "descriptor" in result

    async def test_record_clock_sync_marker(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.record_clock_sync_marker("sync-1")
        assert fake.last_call == (
            "Tracing.recordClockSyncMarker",
            {"syncId": "sync-1"},
        )

    async def test_request_memory_dump(self) -> None:
        fake = FakeSender({"dumpGuid": "abc-123", "success": True})
        domain = TracingDomain(fake)
        result = await domain.request_memory_dump()
        method, params = fake.last_call
        assert method == "Tracing.requestMemoryDump"
        assert params is not None
        assert params["deterministic"] is False
        assert "levelOfDetail" not in params
        assert result["dumpGuid"] == "abc-123"
        assert result["success"] is True

    async def test_request_memory_dump_deterministic_true(self) -> None:
        fake = FakeSender({"dumpGuid": "guid", "success": True})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(deterministic=True)
        _, params = fake.last_call
        assert params is not None
        assert params["deterministic"] is True

    async def test_request_memory_dump_level_of_detail(self) -> None:
        fake = FakeSender({"dumpGuid": "guid", "success": True})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(level_of_detail="detailed")
        _, params = fake.last_call
        assert params is not None
        assert params["levelOfDetail"] == "detailed"

    async def test_start_no_params(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start()
        assert fake.last_call == ("Tracing.start", None)

    async def test_start_transfer_mode(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReturnAsStream")
        _, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReturnAsStream"

    async def test_start_stream_format(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_format="proto")
        _, params = fake.last_call
        assert params is not None
        assert params["streamFormat"] == "proto"

    async def test_start_stream_compression(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_compression="gzip")
        _, params = fake.last_call
        assert params is not None
        assert params["streamCompression"] == "gzip"

    async def test_start_buffer_usage_reporting_interval(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=0.5)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 0.5

    async def test_start_trace_config(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        tc = {"recordMode": "recordUntilFull", "enableSampling": True}
        await domain.start(trace_config=tc)
        _, params = fake.last_call
        assert params is not None
        assert params["traceConfig"] == tc

    async def test_start_perfetto_config(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(perfetto_config="base64data==")
        _, params = fake.last_call
        assert params is not None
        assert params["perfettoConfig"] == "base64data=="

    async def test_start_tracing_backend(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(tracing_backend="system")
        _, params = fake.last_call
        assert params is not None
        assert params["tracingBackend"] == "system"

    async def test_start_screenshot_max_size(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_size=1920)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxSize"] == 1920

    async def test_start_screenshot_max_count(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_count=10)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxCount"] == 10

    async def test_start_all_params(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        tc = {"recordMode": "recordContinuously"}
        await domain.start(
            buffer_usage_reporting_interval=1.0,
            transfer_mode="ReturnAsStream",
            stream_format="proto",
            stream_compression="gzip",
            trace_config=tc,
            perfetto_config="cfg==",
            tracing_backend="chrome",
            screenshot_max_size=1080,
            screenshot_max_count=5,
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {
            "bufferUsageReportingInterval",
            "transferMode",
            "streamFormat",
            "streamCompression",
            "traceConfig",
            "perfettoConfig",
            "tracingBackend",
            "screenshotMaxSize",
            "screenshotMaxCount",
        }


@pytest.mark.unit
class TestTracingOmitempty:
    """omitempty,omitzero semantics for start and request_memory_dump."""

    async def test_start_buffer_usage_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=0)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 0

    async def test_start_buffer_usage_zero_float_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=0.0)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 0.0

    async def test_start_screenshot_max_size_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_size=0)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxSize"] == 0

    async def test_start_screenshot_max_count_zero_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_count=0)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxCount"] == 0

    async def test_start_empty_string_omitted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(
            transfer_mode="",
            stream_format="",
            stream_compression="",
            perfetto_config="",
            tracing_backend="",
        )
        assert fake.last_call == ("Tracing.start", None)

    async def test_start_empty_trace_config_omitted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(trace_config={})
        _, params = fake.last_call
        assert params is None

    async def test_request_memory_dump_deterministic_always_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(deterministic=False)
        _, params = fake.last_call
        assert params is not None
        assert "deterministic" in params
        assert params["deterministic"] is False

    async def test_request_memory_dump_level_omitted_when_none(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump()
        _, params = fake.last_call
        assert params is not None
        assert "levelOfDetail" not in params

    async def test_request_memory_dump_exact_keys_default(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump()
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"deterministic"}

    async def test_request_memory_dump_exact_keys_with_level(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(level_of_detail="light")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"deterministic", "levelOfDetail"}


@pytest.mark.unit
class TestTracingTypeValidation:
    """TypeError checks for all params."""

    async def test_record_clock_sync_marker_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="sync_id must be a str"):
            await domain.record_clock_sync_marker(42)  # type: ignore[arg-type]

    async def test_record_clock_sync_marker_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="sync_id must be a str"):
            await domain.record_clock_sync_marker(True)  # type: ignore[arg-type]

    async def test_request_memory_dump_deterministic_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="deterministic must be a bool"):
            await domain.request_memory_dump(deterministic=1)  # type: ignore[arg-type]

    async def test_request_memory_dump_deterministic_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="deterministic must be a bool"):
            await domain.request_memory_dump(deterministic="yes")  # type: ignore[arg-type]

    async def test_request_memory_dump_level_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="level_of_detail must be a str"):
            await domain.request_memory_dump(level_of_detail=42)  # type: ignore[arg-type]

    async def test_start_buffer_usage_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="buffer_usage_reporting_interval must be a float"):
            await domain.start(buffer_usage_reporting_interval="0.5")  # type: ignore[arg-type]

    async def test_start_buffer_usage_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="buffer_usage_reporting_interval must be a float"):
            await domain.start(buffer_usage_reporting_interval=True)

    async def test_start_transfer_mode_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="transfer_mode must be a str"):
            await domain.start(transfer_mode=1)  # type: ignore[arg-type]

    async def test_start_stream_format_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_format must be a str"):
            await domain.start(stream_format=1)  # type: ignore[arg-type]

    async def test_start_stream_compression_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_compression must be a str"):
            await domain.start(stream_compression=1)  # type: ignore[arg-type]

    async def test_start_trace_config_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="trace_config must be a dict"):
            await domain.start(trace_config="config")  # type: ignore[arg-type]

    async def test_start_trace_config_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="trace_config must be a dict"):
            await domain.start(trace_config=[])  # type: ignore[arg-type]

    async def test_start_perfetto_config_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="perfetto_config must be a str"):
            await domain.start(perfetto_config=42)  # type: ignore[arg-type]

    async def test_start_tracing_backend_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="tracing_backend must be a str"):
            await domain.start(tracing_backend=1)  # type: ignore[arg-type]

    async def test_start_screenshot_max_size_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_size must be an int"):
            await domain.start(screenshot_max_size="1080")  # type: ignore[arg-type]

    async def test_start_screenshot_max_size_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_size must be an int"):
            await domain.start(screenshot_max_size=1080.5)  # type: ignore[arg-type]

    async def test_start_screenshot_max_size_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_size must be an int"):
            await domain.start(screenshot_max_size=True)

    async def test_start_screenshot_max_count_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_count must be an int"):
            await domain.start(screenshot_max_count="10")  # type: ignore[arg-type]

    async def test_start_screenshot_max_count_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_count must be an int"):
            await domain.start(screenshot_max_count=True)

    async def test_start_screenshot_max_count_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="screenshot_max_count must be an int"):
            await domain.start(screenshot_max_count=10.5)  # type: ignore[arg-type]

    async def test_start_perfetto_config_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="perfetto_config must be a str"):
            await domain.start(perfetto_config=[])  # type: ignore[arg-type]

    async def test_start_perfetto_config_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="perfetto_config must be a str"):
            await domain.start(perfetto_config={})  # type: ignore[arg-type]

    async def test_start_trace_config_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="trace_config must be a dict"):
            await domain.start(trace_config=42)  # type: ignore[arg-type]

    async def test_start_trace_config_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="trace_config must be a dict"):
            await domain.start(trace_config=3.14)  # type: ignore[arg-type]

    async def test_start_buffer_usage_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(
            TypeError, match="buffer_usage_reporting_interval must be a float"
        ):
            await domain.start(buffer_usage_reporting_interval=[])  # type: ignore[arg-type]

    async def test_start_buffer_usage_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(
            TypeError, match="buffer_usage_reporting_interval must be a float"
        ):
            await domain.start(buffer_usage_reporting_interval={})  # type: ignore[arg-type]

    async def test_request_memory_dump_deterministic_type_error_zero(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="deterministic must be a bool"):
            await domain.request_memory_dump(deterministic=0)  # type: ignore[arg-type]


@pytest.mark.unit
class TestTracingEnumValidation:
    """ValueError checks for enum params."""

    async def test_start_transfer_mode_invalid(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(
            ValueError,
            match="transfer_mode must be 'ReportEvents' or 'ReturnAsStream'",
        ):
            await domain.start(transfer_mode="Invalid")

    async def test_start_stream_format_invalid(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(ValueError, match="stream_format must be 'json' or 'proto'"):
            await domain.start(stream_format="xml")

    async def test_start_stream_compression_invalid(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(ValueError, match="stream_compression must be 'none' or 'gzip'"):
            await domain.start(stream_compression="bzip2")

    async def test_start_tracing_backend_invalid(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(
            ValueError,
            match="tracing_backend must be 'auto', 'chrome', or 'system'",
        ):
            await domain.start(tracing_backend="firefox")

    async def test_request_memory_dump_level_invalid(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(
            ValueError,
            match="level_of_detail must be 'background', 'light', or 'detailed'",
        ):
            await domain.request_memory_dump(level_of_detail="verbose")

    async def test_start_transfer_mode_empty_not_validated(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="")
        _, params = fake.last_call
        assert params is None

    async def test_start_stream_format_empty_not_validated(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_format="")
        _, params = fake.last_call
        assert params is None


@pytest.mark.unit
class TestTracingReturnValues:
    """Return value pass-through for all methods."""

    async def test_end_return_value(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        result = await domain.end()
        assert result == {}

    async def test_get_categories_return_value(self) -> None:
        fake = FakeSender({"categories": ["cat1", "cat2"]})
        domain = TracingDomain(fake)
        result = await domain.get_categories()
        assert result["categories"] == ["cat1", "cat2"]

    async def test_get_track_event_descriptor_return_value(self) -> None:
        fake = FakeSender({"descriptor": "dGVzdA=="})
        domain = TracingDomain(fake)
        result = await domain.get_track_event_descriptor()
        assert result["descriptor"] == "dGVzdA=="

    async def test_record_clock_sync_marker_return_value(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        result = await domain.record_clock_sync_marker("sync-1")
        assert result == {}

    async def test_request_memory_dump_return_value(self) -> None:
        fake = FakeSender({"dumpGuid": "guid-abc", "success": True})
        domain = TracingDomain(fake)
        result = await domain.request_memory_dump()
        assert result["dumpGuid"] == "guid-abc"
        assert result["success"] is True

    async def test_start_return_value(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        result = await domain.start(transfer_mode="ReportEvents")
        assert result == {}


@pytest.mark.unit
class TestTracingMeta:
    """Meta tests: method count, order, BaseDomain, coroutines, docstrings."""

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in TracingDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 6

    async def test_method_order_matches_go(self) -> None:
        expected = [
            "end",
            "get_categories",
            "get_track_event_descriptor",
            "record_clock_sync_marker",
            "request_memory_dump",
            "start",
        ]
        actual = [
            name
            for name, value in TracingDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert actual == expected

    async def test_inherits_basedomain(self) -> None:
        assert issubclass(TracingDomain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        methods = [
            value
            for name, value in TracingDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        for method in methods:
            assert inspect.iscoroutinefunction(method)

    async def test_no_request_clock_sync_marker(self) -> None:
        assert not hasattr(TracingDomain, "request_clock_sync_marker")

    async def test_class_docstring_experimental(self) -> None:
        doc = TracingDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_events(self) -> None:
        doc = TracingDomain.__doc__
        assert doc is not None
        assert "bufferUsage" in doc
        assert "dataCollected" in doc
        assert "tracingComplete" in doc

    async def test_module_docstring_types(self) -> None:
        import cdpwave.domains.tracing as mod
        doc = mod.__doc__
        assert doc is not None
        assert "RecordMode" in doc
        assert "StreamFormat" in doc
        assert "StreamCompression" in doc
        assert "MemoryDumpLevelOfDetail" in doc
        assert "Backend" in doc
        assert "TransferMode" in doc
        assert "TraceConfig" in doc
        assert "MemoryDumpConfig" in doc

    async def test_module_docstring_events(self) -> None:
        import cdpwave.domains.tracing as mod
        doc = mod.__doc__
        assert doc is not None
        assert "bufferUsage" in doc
        assert "dataCollected" in doc
        assert "tracingComplete" in doc
        assert "dataLossOccurred" in doc

    async def test_module_docstring_record_mode_values(self) -> None:
        import cdpwave.domains.tracing as mod
        doc = mod.__doc__
        assert doc is not None
        assert "recordUntilFull" in doc
        assert "recordContinuously" in doc
        assert "recordAsMuchAsPossible" in doc
        assert "echoToConsole" in doc

    async def test_end_docstring(self) -> None:
        doc = TracingDomain.end.__doc__
        assert doc is not None
        assert "Stop trace events collection" in doc

    async def test_get_categories_docstring(self) -> None:
        doc = TracingDomain.get_categories.__doc__
        assert doc is not None
        assert "categories" in doc

    async def test_get_track_event_descriptor_docstring(self) -> None:
        doc = TracingDomain.get_track_event_descriptor.__doc__
        assert doc is not None
        assert "base64" in doc.lower() or "base64" in doc

    async def test_record_clock_sync_marker_docstring(self) -> None:
        doc = TracingDomain.record_clock_sync_marker.__doc__
        assert doc is not None
        assert "sync_id" in doc
        assert "TypeError" in doc

    async def test_request_memory_dump_docstring(self) -> None:
        doc = TracingDomain.request_memory_dump.__doc__
        assert doc is not None
        assert "deterministic" in doc
        assert "level_of_detail" in doc
        assert "dumpGuid" in doc
        assert "success" in doc
        assert "Always sent" in doc

    async def test_start_docstring_omitempty(self) -> None:
        doc = TracingDomain.start.__doc__
        assert doc is not None
        assert "omitempty" in doc or "Omitted" in doc or "omitted" in doc

    async def test_start_docstring_all_params(self) -> None:
        doc = TracingDomain.start.__doc__
        assert doc is not None
        assert "buffer_usage_reporting_interval" in doc
        assert "transfer_mode" in doc
        assert "stream_format" in doc
        assert "stream_compression" in doc
        assert "trace_config" in doc
        assert "perfetto_config" in doc
        assert "tracing_backend" in doc
        assert "screenshot_max_size" in doc
        assert "screenshot_max_count" in doc

    async def test_start_no_categories_param(self) -> None:
        doc = TracingDomain.start.__doc__
        assert doc is not None
        assert "categories" not in doc.lower().replace("includedCategories", "")

    async def test_start_no_options_param(self) -> None:
        doc = TracingDomain.start.__doc__
        assert doc is not None
        assert (
            "options" not in doc.lower()
            .replace("excludedCategories", "")
            .replace("syntheticDelays", "")
        )

    async def test_start_no_trace_type_param(self) -> None:
        doc = TracingDomain.start.__doc__
        assert doc is not None
        assert "trace_type" not in doc


@pytest.mark.unit
class TestTracingMultipleCalls:
    """Independence and sequence tests."""

    async def test_multiple_calls_independent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReportEvents")
        await domain.start()
        first_method, first_params = fake.calls[0]
        second_method, second_params = fake.calls[1]
        assert first_params is not None
        assert "transferMode" in first_params
        assert second_params is None

    async def test_all_methods_called(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.end()
        await domain.get_categories()
        await domain.get_track_event_descriptor()
        await domain.record_clock_sync_marker("sync")
        await domain.request_memory_dump()
        await domain.start()
        assert len(fake.calls) == 6

    async def test_start_negative_interval_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=-1.0)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == -1.0

    async def test_start_negative_screenshot_size_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_size=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxSize"] == -1


@pytest.mark.unit
class TestTracingEdgeCases:
    """Edge-case tests for boundary conditions and subtle bugs."""

    # ── level_of_detail="" omitempty (bug fix) ──

    async def test_request_memory_dump_level_empty_string_omitted(self) -> None:
        fake = FakeSender({"dumpGuid": "g", "success": True})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(level_of_detail="")
        _, params = fake.last_call
        assert params is not None
        assert "levelOfDetail" not in params
        assert params["deterministic"] is False

    async def test_request_memory_dump_level_empty_no_error(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        result = await domain.request_memory_dump(level_of_detail="")
        assert result == {}

    # ── empty string omitempty for start() enum params individually ──

    async def test_start_stream_compression_empty_omitted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_compression="")
        _, params = fake.last_call
        assert params is None

    async def test_start_tracing_backend_empty_omitted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(tracing_backend="")
        _, params = fake.last_call
        assert params is None

    async def test_start_perfetto_config_empty_omitted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(perfetto_config="")
        _, params = fake.last_call
        assert params is None

    # ── record_clock_sync_marker with empty string (required, not omitempty) ──

    async def test_record_clock_sync_marker_empty_string_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.record_clock_sync_marker("")
        method, params = fake.last_call
        assert method == "Tracing.recordClockSyncMarker"
        assert params == {"syncId": ""}

    # ── int accepted for buffer_usage_reporting_interval ──

    async def test_start_buffer_usage_int_accepted(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=2)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 2

    # ── all valid enum values ──

    async def test_start_transfer_mode_report_events(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReportEvents")
        _, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReportEvents"

    async def test_start_transfer_mode_return_as_stream(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReturnAsStream")
        _, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReturnAsStream"

    async def test_start_stream_format_json(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_format="json")
        _, params = fake.last_call
        assert params is not None
        assert params["streamFormat"] == "json"

    async def test_start_stream_compression_none(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(stream_compression="none")
        _, params = fake.last_call
        assert params is not None
        assert params["streamCompression"] == "none"

    async def test_start_tracing_backend_auto(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(tracing_backend="auto")
        _, params = fake.last_call
        assert params is not None
        assert params["tracingBackend"] == "auto"

    async def test_start_tracing_backend_chrome(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(tracing_backend="chrome")
        _, params = fake.last_call
        assert params is not None
        assert params["tracingBackend"] == "chrome"

    async def test_request_memory_dump_level_background(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(level_of_detail="background")
        _, params = fake.last_call
        assert params is not None
        assert params["levelOfDetail"] == "background"

    async def test_request_memory_dump_level_detailed(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(level_of_detail="detailed")
        _, params = fake.last_call
        assert params is not None
        assert params["levelOfDetail"] == "detailed"

    # ── negative values sent (omitempty,omitzero only omits zero) ──

    async def test_start_negative_screenshot_count_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_count=-5)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxCount"] == -5

    async def test_start_negative_buffer_usage_int_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=-3)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == -3

    # ── request_memory_dump multiple calls independence ──

    async def test_request_memory_dump_multiple_calls_independent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(deterministic=True, level_of_detail="light")
        await domain.request_memory_dump(deterministic=False)
        first_method, first_params = fake.calls[0]
        second_method, second_params = fake.calls[1]
        assert first_params is not None
        assert first_params["deterministic"] is True
        assert first_params["levelOfDetail"] == "light"
        assert second_params is not None
        assert second_params["deterministic"] is False
        assert "levelOfDetail" not in second_params

    # ── start with trace_config containing nested memoryDumpConfig ──

    async def test_start_trace_config_with_memory_dump_config(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        tc = {
            "recordMode": "recordAsMuchAsPossible",
            "enableSampling": True,
            "memoryDumpConfig": {},
        }
        await domain.start(trace_config=tc)
        _, params = fake.last_call
        assert params is not None
        assert params["traceConfig"] == tc
        assert params["traceConfig"]["memoryDumpConfig"] == {}

    # ── exact param keys for various combos ──

    async def test_start_only_transfer_mode_keys(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(transfer_mode="ReportEvents")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"transferMode"}

    async def test_start_trace_config_and_backend_keys(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(
            trace_config={"recordMode": "recordUntilFull"},
            tracing_backend="system",
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"traceConfig", "tracingBackend"}

    async def test_request_memory_dump_deterministic_true_with_level_keys(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(
            deterministic=True, level_of_detail="detailed"
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"deterministic", "levelOfDetail"}
        assert params["deterministic"] is True
        assert params["levelOfDetail"] == "detailed"

    # ── start() with all params sends all keys ──

    async def test_start_all_params_exact_values(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        tc = {"recordMode": "echoToConsole", "enableSystrace": True}
        await domain.start(
            buffer_usage_reporting_interval=2.5,
            transfer_mode="ReturnAsStream",
            stream_format="proto",
            stream_compression="gzip",
            trace_config=tc,
            perfetto_config="perf==",
            tracing_backend="chrome",
            screenshot_max_size=1920,
            screenshot_max_count=3,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 2.5
        assert params["transferMode"] == "ReturnAsStream"
        assert params["streamFormat"] == "proto"
        assert params["streamCompression"] == "gzip"
        assert params["traceConfig"] == tc
        assert params["perfettoConfig"] == "perf=="
        assert params["tracingBackend"] == "chrome"
        assert params["screenshotMaxSize"] == 1920
        assert params["screenshotMaxCount"] == 3

    # ── start() with None params sends None ──

    async def test_start_all_none_sends_none(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(
            buffer_usage_reporting_interval=None,
            transfer_mode=None,
            stream_format=None,
            stream_compression=None,
            trace_config=None,
            perfetto_config=None,
            tracing_backend=None,
            screenshot_max_size=None,
            screenshot_max_count=None,
        )
        assert fake.last_call == ("Tracing.start", None)

    # ── request_memory_dump with deterministic=True only ──

    async def test_request_memory_dump_deterministic_true_only(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.request_memory_dump(deterministic=True)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"deterministic"}
        assert params["deterministic"] is True

    # ── start() with screenshot_max_size=1 (minimum truthy) ──

    async def test_start_screenshot_max_size_one_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_size=1)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxSize"] == 1

    # ── start() with screenshot_max_count=1 (minimum truthy) ──

    async def test_start_screenshot_max_count_one_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(screenshot_max_count=1)
        _, params = fake.last_call
        assert params is not None
        assert params["screenshotMaxCount"] == 1

    # ── start() with buffer_usage_reporting_interval=0.1 (small float) ──

    async def test_start_buffer_usage_small_float_sent(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(buffer_usage_reporting_interval=0.1)
        _, params = fake.last_call
        assert params is not None
        assert params["bufferUsageReportingInterval"] == 0.1

    # ── non-string falsy values must raise TypeError (bug fix) ──

    async def test_start_transfer_mode_int_zero_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="transfer_mode must be a str"):
            await domain.start(transfer_mode=0)  # type: ignore[arg-type]

    async def test_start_transfer_mode_false_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="transfer_mode must be a str"):
            await domain.start(transfer_mode=False)  # type: ignore[arg-type]

    async def test_start_transfer_mode_list_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="transfer_mode must be a str"):
            await domain.start(transfer_mode=[])  # type: ignore[arg-type]

    async def test_start_stream_format_int_zero_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_format must be a str"):
            await domain.start(stream_format=0)  # type: ignore[arg-type]

    async def test_start_stream_format_false_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_format must be a str"):
            await domain.start(stream_format=False)  # type: ignore[arg-type]

    async def test_start_stream_compression_int_zero_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_compression must be a str"):
            await domain.start(stream_compression=0)  # type: ignore[arg-type]

    async def test_start_stream_compression_false_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="stream_compression must be a str"):
            await domain.start(stream_compression=False)  # type: ignore[arg-type]

    async def test_start_tracing_backend_int_zero_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="tracing_backend must be a str"):
            await domain.start(tracing_backend=0)  # type: ignore[arg-type]

    async def test_start_tracing_backend_false_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="tracing_backend must be a str"):
            await domain.start(tracing_backend=False)  # type: ignore[arg-type]

    async def test_request_memory_dump_level_int_zero_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="level_of_detail must be a str"):
            await domain.request_memory_dump(level_of_detail=0)  # type: ignore[arg-type]

    async def test_request_memory_dump_level_false_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="level_of_detail must be a str"):
            await domain.request_memory_dump(level_of_detail=False)  # type: ignore[arg-type]

    async def test_request_memory_dump_level_list_raises(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        with pytest.raises(TypeError, match="level_of_detail must be a str"):
            await domain.request_memory_dump(level_of_detail=[])  # type: ignore[arg-type]
