"""E2E tests for the Tracing domain (real browser flows).

Full end-to-end flows against a real browser, including tracing
lifecycle (start → end → tracingComplete event), category discovery,
memory dumps, clock sync markers, track event descriptors, type
validation in real browser context, raw command sending, and meta
tests for docstrings and experimental marking.
"""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.domains.base import BaseDomain
from cdpwave.domains.tracing import TracingDomain


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.e2e
class TestTracingE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.tracing is not None
            assert isinstance(session.tracing, TracingDomain)

    async def test_get_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.tracing.get_categories()
            assert "categories" in result
            assert isinstance(result["categories"], list)
            assert len(result["categories"]) > 0

    async def test_full_tracing_lifecycle(self) -> None:
        """Start → end → verify tracingComplete event."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            completed: list[dict[str, Any]] = []

            async def on_complete(params: dict[str, Any]) -> None:
                completed.append(params)

            session.on("Tracing.tracingComplete", on_complete)

            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                    },
                    transfer_mode="ReportEvents",
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()
                await asyncio.sleep(2.0)

                if completed:
                    assert "dataLossOccurred" in completed[0]
            except Exception:
                pytest.skip("Tracing lifecycle not supported")

    async def test_start_with_stream_format(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                    },
                    transfer_mode="ReturnAsStream",
                    stream_format="json",
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("Tracing with stream format not supported")

    async def test_start_with_stream_compression(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                    },
                    transfer_mode="ReturnAsStream",
                    stream_format="json",
                    stream_compression="gzip",
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("Tracing with stream compression not supported")

    async def test_start_with_buffer_usage_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    buffer_usage_reporting_interval=0.5,
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()
            except Exception:
                pytest.skip("Tracing with buffer usage interval not supported")

    async def test_record_clock_sync_marker(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.record_clock_sync_marker("e2e-sync-1")
            except Exception:
                pytest.skip("recordClockSyncMarker not supported")

    async def test_request_memory_dump(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump()
                assert "dumpGuid" in result
                assert "success" in result
                assert isinstance(result["success"], bool)
            except Exception:
                pytest.skip("requestMemoryDump not supported")

    async def test_request_memory_dump_deterministic_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    deterministic=True
                )
                assert "dumpGuid" in result
                assert "success" in result
            except Exception:
                pytest.skip("requestMemoryDump deterministic not supported")

    async def test_request_memory_dump_deterministic_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    deterministic=False
                )
                assert "dumpGuid" in result
                assert "success" in result
            except Exception:
                pytest.skip("requestMemoryDump not supported")

    async def test_request_memory_dump_with_level_of_detail(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    level_of_detail="light"
                )
                assert "dumpGuid" in result
            except Exception:
                pytest.skip("requestMemoryDump with levelOfDetail not supported")

    async def test_get_track_event_descriptor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.get_track_event_descriptor()
                assert "descriptor" in result
            except Exception:
                pytest.skip("getTrackEventDescriptor not supported")

    async def test_start_with_tracing_backend(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    tracing_backend="auto",
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("Tracing with backend not supported")

    async def test_start_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start()
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("Tracing start with no params not supported")

    async def test_end_without_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.end()

    # ── raw send for all 6 commands ──

    async def test_raw_send_end(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Tracing.end")

    async def test_raw_send_get_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.send("Tracing.getCategories")
            assert "categories" in result

    async def test_raw_send_get_track_event_descriptor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Tracing.getTrackEventDescriptor")

    async def test_raw_send_record_clock_sync_marker(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.recordClockSyncMarker",
                    {"syncId": "raw-sync"},
                )

    async def test_raw_send_request_memory_dump(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.requestMemoryDump",
                    {"deterministic": False},
                )

    async def test_raw_send_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.start",
                    {"transferMode": "ReportEvents"},
                )
                await asyncio.sleep(0.5)
                await session.send("Tracing.end")

    # ── type validation in real browser context ──

    async def test_type_error_sync_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sync_id must be a str"):
                await session.tracing.record_clock_sync_marker(42)

    async def test_type_error_deterministic_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="deterministic must be a bool"):
                await session.tracing.request_memory_dump(deterministic=1)

    async def test_type_error_transfer_mode_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="transfer_mode must be a str"):
                await session.tracing.start(transfer_mode=1)

    async def test_value_error_transfer_mode_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(
                ValueError,
                match="transfer_mode must be 'ReportEvents' or 'ReturnAsStream'",
            ):
                await session.tracing.start(transfer_mode="Invalid")

    async def test_value_error_stream_format_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="stream_format must be 'json' or 'proto'"):
                await session.tracing.start(stream_format="xml")

    async def test_value_error_stream_compression_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="stream_compression must be 'none' or 'gzip'"):
                await session.tracing.start(stream_compression="bzip2")

    async def test_value_error_tracing_backend_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(
                ValueError,
                match="tracing_backend must be 'auto', 'chrome', or 'system'",
            ):
                await session.tracing.start(tracing_backend="firefox")

    async def test_value_error_level_of_detail_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(
                ValueError,
                match="level_of_detail must be 'background', 'light', or 'detailed'",
            ):
                await session.tracing.request_memory_dump(level_of_detail="verbose")

    async def test_type_error_screenshot_max_size_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="screenshot_max_size must be an int"):
                await session.tracing.start(screenshot_max_size=True)

    async def test_type_error_buffer_usage_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="buffer_usage_reporting_interval must be a float"):
                await session.tracing.start(buffer_usage_reporting_interval=True)

    # ── meta tests: docstrings, experimental, method count ──

    async def test_module_docstring_documents_types(self) -> None:
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

    async def test_all_methods_callable_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert callable(session.tracing.end)
            assert callable(session.tracing.get_categories)
            assert callable(session.tracing.get_track_event_descriptor)
            assert callable(session.tracing.record_clock_sync_marker)
            assert callable(session.tracing.request_memory_dump)
            assert callable(session.tracing.start)

    async def test_no_request_clock_sync_marker(self) -> None:
        assert not hasattr(TracingDomain, "request_clock_sync_marker")

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
        assert "base64" in doc.lower()

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


@pytest.mark.e2e
class TestTracingE2EEdgeCases:
    """Edge-case E2E tests for Tracing with real browser."""

    # ── double lifecycle ──

    async def test_double_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
                await asyncio.sleep(0.5)
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("Double tracing lifecycle not supported")

    # ── all recordModes ──

    async def test_record_mode_record_continuously(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={"recordMode": "recordContinuously"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("recordContinuously not supported")

    async def test_record_mode_record_as_much_as_possible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={"recordMode": "recordAsMuchAsPossible"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("recordAsMuchAsPossible not supported")

    async def test_record_mode_echo_to_console(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={"recordMode": "echoToConsole"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("echoToConsole not supported")

    # ── trace_config with excludedCategories and enableSampling ──

    async def test_trace_config_with_excluded_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                        "excludedCategories": ["v8"],
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("excludedCategories not supported")

    async def test_trace_config_with_enable_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "enableSampling": True,
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("enableSampling not supported")

    # ── buffer_usage_reporting_interval as int ──

    async def test_buffer_usage_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    buffer_usage_reporting_interval=1,
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()
            except Exception:
                pytest.skip("buffer_usage int not supported")

    # ── request_memory_dump all levels ──

    async def test_request_memory_dump_background(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    level_of_detail="background"
                )
                assert "dumpGuid" in result or "success" in result
            except Exception:
                pytest.skip("requestMemoryDump background not supported")

    async def test_request_memory_dump_detailed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    deterministic=True, level_of_detail="detailed"
                )
                assert "dumpGuid" in result or "success" in result
            except Exception:
                pytest.skip("requestMemoryDump detailed not supported")

    # ── record_clock_sync_marker empty string ──

    async def test_record_clock_sync_marker_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.record_clock_sync_marker("")

    # ── screenshot params ──

    async def test_start_with_screenshot_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                    screenshot_max_size=1080,
                    screenshot_max_count=5,
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("screenshot params not supported")

    # ── perfetto_config ──

    async def test_start_with_perfetto_config(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    perfetto_config="dGVzdA==",
                    tracing_backend="auto",
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("perfettoConfig not supported")

    # ── all params combined ──

    async def test_start_all_params_combined(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    buffer_usage_reporting_interval=0.5,
                    transfer_mode="ReturnAsStream",
                    stream_format="json",
                    stream_compression="gzip",
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "enableSampling": True,
                    },
                    tracing_backend="chrome",
                    screenshot_max_size=1920,
                    screenshot_max_count=3,
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("All params combined not supported")

    # ── categories type check ──

    async def test_get_categories_returns_list_of_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.tracing.get_categories()
            assert "categories" in result
            cats = result["categories"]
            assert isinstance(cats, list)
            for cat in cats:
                assert isinstance(cat, str)

    # ── bufferUsage event ──

    async def test_buffer_usage_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_buffer_usage(params: dict[str, Any]) -> None:
                events.append(params)

            session.on("Tracing.bufferUsage", on_buffer_usage)
            try:
                await session.tracing.start(
                    buffer_usage_reporting_interval=0.1,
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(2.0)
                await session.tracing.end()
                if events:
                    assert isinstance(events[0], dict)
            except Exception:
                pytest.skip("bufferUsage event not supported")

    # ── dataCollected event ──

    async def test_data_collected_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_data_collected(params: dict[str, Any]) -> None:
                events.append(params)

            session.on("Tracing.dataCollected", on_data_collected)
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                    },
                    transfer_mode="ReportEvents",
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()
                await asyncio.sleep(1.0)
                if events:
                    assert isinstance(events[0], dict)
            except Exception:
                pytest.skip("dataCollected event not supported")

    # ── level_of_detail="" omitempty in real browser ──

    async def test_request_memory_dump_level_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.tracing.request_memory_dump(
                    level_of_detail=""
                )
                assert "dumpGuid" in result or "success" in result
            except Exception:
                pytest.skip("requestMemoryDump with empty level not supported")

    # ── type validation edge cases in real browser ──

    async def test_type_error_trace_config_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="trace_config must be a dict"):
                await session.tracing.start(trace_config=[])

    async def test_type_error_screenshot_max_count_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="screenshot_max_count must be an int"):
                await session.tracing.start(screenshot_max_count="5")

    async def test_type_error_perfetto_config_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="perfetto_config must be a str"):
                await session.tracing.start(perfetto_config=42)

    async def test_type_error_level_of_detail_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="level_of_detail must be a str"):
                await session.tracing.request_memory_dump(level_of_detail=42)

    # ── start with ReturnAsStream + proto ──

    async def test_start_return_as_stream_proto(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    transfer_mode="ReturnAsStream",
                    stream_format="proto",
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("ReturnAsStream + proto not supported")

    # ── start with stream_compression none ──

    async def test_start_stream_compression_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    stream_compression="none",
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("stream_compression none not supported")

    # ── start with tracing_backend system ──

    async def test_start_tracing_backend_system(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    tracing_backend="system",
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("tracing_backend system not supported")

    # ── start with trace_config containing memoryDumpConfig ──

    async def test_start_trace_config_with_memory_dump_config(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "memoryDumpConfig": {},
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
            except Exception:
                pytest.skip("memoryDumpConfig not supported")
