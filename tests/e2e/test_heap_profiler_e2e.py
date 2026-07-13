"""E2E tests for the HeapProfiler domain (real browser flows).

Full end-to-end flows against a real Edge browser, including
heap snapshot collection, sampling profile lifecycle, heap object
tracking, object ID roundtrip, type validation, raw command sending,
and meta tests.
"""

import asyncio
import inspect

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.domains.base import BaseDomain
from cdpwave.domains.heap_profiler import HeapProfilerDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


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
class TestHeapProfilerE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.heap_profiler is not None

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()

    async def test_collect_garbage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.collect_garbage()
            await session.heap_profiler.disable()

    async def test_full_sampling_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(
                sampling_interval=4096,
                stack_depth=128,
            )
            await session.runtime.evaluate(
                """
                new Promise((resolve) => {
                    let arr = [];
                    for (let i = 0; i < 10000; i++) { arr.push({x: i, y: i * 2}); }
                    resolve(arr.length);
                })
                """,
                return_by_value=True,
                await_promise=True,
            )
            result = await session.heap_profiler.stop_sampling()
            assert "profile" in result
            profile = result["profile"]
            assert "head" in profile
            assert "samples" in profile
            assert isinstance(profile["head"], dict)
            assert isinstance(profile["samples"], list)
            await session.heap_profiler.disable()

    async def test_get_sampling_profile_mid_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=4096)
            await session.runtime.evaluate("1 + 1")
            result = await session.heap_profiler.get_sampling_profile()
            assert "profile" in result
            assert isinstance(result["profile"], dict)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_sampling_with_include_objects_collected_by_major_gc(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(
                sampling_interval=4096,
                include_objects_collected_by_major_gc=True,
            )
            await session.runtime.evaluate(
                """
                new Promise((resolve) => {
                    let arr = [];
                    for (let i = 0; i < 5000; i++) { arr.push({x: i}); }
                    resolve(arr.length);
                })
                """,
                return_by_value=True,
                await_promise=True,
            )
            result = await session.heap_profiler.stop_sampling()
            assert "profile" in result
            await session.heap_profiler.disable()

    async def test_sampling_with_include_objects_collected_by_minor_gc(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(
                sampling_interval=4096,
                include_objects_collected_by_minor_gc=True,
            )
            await session.runtime.evaluate("1 + 1")
            result = await session.heap_profiler.stop_sampling()
            assert "profile" in result
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot()
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot_with_capture_numeric_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot(
                capture_numeric_value=True
            )
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot(
                report_progress=True,
                capture_numeric_value=True,
                expose_internals=True,
            )
            await session.heap_profiler.disable()

    async def test_heap_object_id_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({name: 'test', value: 42})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if not object_id:
                pytest.skip("No objectId returned from Runtime.evaluate")
            heap_id_result = await session.heap_profiler.get_heap_object_id(object_id)
            assert "heapSnapshotObjectId" in heap_id_result
            heap_obj_id = heap_id_result["heapSnapshotObjectId"]
            assert isinstance(heap_obj_id, str)
            obj_result = await session.heap_profiler.get_object_by_heap_object_id(
                heap_obj_id
            )
            assert "result" in obj_result
            await session.heap_profiler.disable()

    async def test_get_object_by_heap_object_id_with_group(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({name: 'test'})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if not object_id:
                pytest.skip("No objectId returned from Runtime.evaluate")
            heap_id_result = await session.heap_profiler.get_heap_object_id(object_id)
            heap_obj_id = heap_id_result["heapSnapshotObjectId"]
            result = await session.heap_profiler.get_object_by_heap_object_id(
                heap_obj_id, object_group="test-group"
            )
            assert "result" in result
            await session.heap_profiler.disable()

    async def test_start_stop_tracking_heap_objects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_tracking_heap_objects(
                track_allocations=True
            )
            await session.runtime.evaluate(
                """
                new Promise((resolve) => {
                    let arr = [];
                    for (let i = 0; i < 1000; i++) { arr.push({x: i}); }
                    resolve(arr.length);
                })
                """,
                return_by_value=True,
                await_promise=True,
            )
            await session.heap_profiler.stop_tracking_heap_objects()
            await session.heap_profiler.disable()

    async def test_stop_tracking_with_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_tracking_heap_objects(
                track_allocations=True
            )
            await session.heap_profiler.stop_tracking_heap_objects(
                report_progress=True,
                capture_numeric_value=True,
                expose_internals=True,
            )
            await session.heap_profiler.disable()

    async def test_stop_sampling_without_start_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(CommandError):
                await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_type_error_start_sampling_bool_as_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="sampling_interval must be a number"):
                await session.heap_profiler.start_sampling(sampling_interval=True)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_start_sampling_stack_depth_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="stack_depth must be a number"):
                await session.heap_profiler.start_sampling(stack_depth=False)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_start_sampling_include_major_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(
                TypeError,
                match="include_objects_collected_by_major_gc must be a bool",
            ):
                await session.heap_profiler.start_sampling(  # type: ignore[arg-type]
                    include_objects_collected_by_major_gc="yes"
                )
            await session.heap_profiler.disable()

    async def test_type_error_take_heap_snapshot_report_progress_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="report_progress must be a bool"):
                await session.heap_profiler.take_heap_snapshot(report_progress="yes")  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_take_heap_snapshot_capture_numeric_value_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="capture_numeric_value must be a bool"):
                await session.heap_profiler.take_heap_snapshot(capture_numeric_value=1)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_stop_tracking_expose_internals_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="expose_internals must be a bool"):
                await session.heap_profiler.stop_tracking_heap_objects(expose_internals="yes")  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_start_tracking_track_allocations_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="track_allocations must be a bool"):
                await session.heap_profiler.start_tracking_heap_objects(track_allocations=1)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_get_heap_object_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="object_id must be a str"):
                await session.heap_profiler.get_heap_object_id(42)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_get_object_by_heap_object_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="heap_object_id must be a str"):
                await session.heap_profiler.get_object_by_heap_object_id(42)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_type_error_add_inspected_heap_object_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="heap_object_id must be a str"):
                await session.heap_profiler.add_inspected_heap_object(42)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_raw_send_heap_profiler_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send("HeapProfiler.enable")
            await session.send("HeapProfiler.startSampling", {"samplingInterval": 4096})
            await session.runtime.evaluate("1 + 1")
            result = await session.send("HeapProfiler.stopSampling")
            assert "profile" in result
            await session.send("HeapProfiler.disable")

    async def test_inherits_base_domain(self) -> None:
        domain = HeapProfilerDomain(FakeSender({}))
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        domain = HeapProfilerDomain(FakeSender({}))
        for name in (
            "add_inspected_heap_object",
            "collect_garbage",
            "disable",
            "enable",
            "get_heap_object_id",
            "get_object_by_heap_object_id",
            "get_sampling_profile",
            "start_sampling",
            "start_tracking_heap_objects",
            "stop_sampling",
            "stop_tracking_heap_objects",
            "take_heap_snapshot",
        ):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(HeapProfilerDomain)
            if not m.startswith("_") and callable(getattr(HeapProfilerDomain, m))
        ]
        assert len(methods) == 12

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(HeapProfilerDomain)
            if not m.startswith("_") and callable(getattr(HeapProfilerDomain, m))
        ]
        expected = [
            "add_inspected_heap_object",
            "collect_garbage",
            "disable",
            "enable",
            "get_heap_object_id",
            "get_object_by_heap_object_id",
            "get_sampling_profile",
            "start_sampling",
            "start_tracking_heap_objects",
            "stop_sampling",
            "stop_tracking_heap_objects",
            "take_heap_snapshot",
        ]
        assert methods == expected

    # --- second pass edge cases ---

    async def test_get_object_by_heap_object_id_empty_group_omitted(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({a: 1})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if not object_id:
                pytest.skip("No objectId returned from Runtime.evaluate")
            heap_id = await session.heap_profiler.get_heap_object_id(object_id)
            heap_obj_id = heap_id["heapSnapshotObjectId"]
            result = await session.heap_profiler.get_object_by_heap_object_id(
                heap_obj_id, object_group=""
            )
            assert "result" in result
            await session.heap_profiler.disable()

    async def test_start_sampling_negative_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=-1)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_start_sampling_float_stack_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(stack_depth=64.5)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_start_sampling_large_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=2**32)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()
            await session.heap_profiler.disable()

    async def test_start_tracking_with_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.start_tracking_heap_objects(
                track_allocations=False
            )
            await session.heap_profiler.stop_tracking_heap_objects()
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot_with_expose_internals(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot(
                expose_internals=True
            )
            await session.heap_profiler.disable()

    async def test_add_inspected_heap_object_real(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({x: 1})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if not object_id:
                pytest.skip("No objectId returned from Runtime.evaluate")
            heap_id = await session.heap_profiler.get_heap_object_id(object_id)
            heap_obj_id = heap_id["heapSnapshotObjectId"]
            await session.heap_profiler.add_inspected_heap_object(heap_obj_id)
            await session.heap_profiler.disable()

    async def test_type_error_object_group_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="object_group must be a str"):
                await session.heap_profiler.get_object_by_heap_object_id(  # type: ignore[arg-type]
                    "heap-1", object_group=42
                )
            await session.heap_profiler.disable()

    async def test_type_error_include_minor_gc_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(
                TypeError,
                match="include_objects_collected_by_minor_gc must be a bool",
            ):
                await session.heap_profiler.start_sampling(  # type: ignore[arg-type]
                    include_objects_collected_by_minor_gc="yes"
                )
            await session.heap_profiler.disable()

    async def test_type_error_stop_tracking_capture_numeric_value_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(
                TypeError, match="capture_numeric_value must be a bool"
            ):
                await session.heap_profiler.stop_tracking_heap_objects(  # type: ignore[arg-type]
                    capture_numeric_value=1
                )
            await session.heap_profiler.disable()

    async def test_type_error_take_heap_snapshot_expose_internals_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="expose_internals must be a bool"):
                await session.heap_profiler.take_heap_snapshot(expose_internals=0)  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    async def test_module_docstring_documents_all_events(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "addHeapSnapshotChunk" in doc
        assert "heapStatsUpdate" in doc
        assert "lastSeenObjectId" in doc
        assert "reportHeapSnapshotProgress" in doc
        assert "resetProfiles" in doc

    async def test_module_docstring_documents_types(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "HeapSnapshotObjectID" in doc
        assert "SamplingHeapProfileNode" in doc
        assert "SamplingHeapProfileSample" in doc
        assert "SamplingHeapProfile" in doc

    async def test_class_docstring_has_experimental_mark(self) -> None:
        doc = HeapProfilerDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_documents_all_events(self) -> None:
        doc = HeapProfilerDomain.__doc__
        assert doc is not None
        assert "addHeapSnapshotChunk" in doc
        assert "heapStatsUpdate" in doc
        assert "lastSeenObjectId" in doc
        assert "reportHeapSnapshotProgress" in doc
        assert "resetProfiles" in doc

    async def test_module_docstring_last_seen_object_id_extra_detail(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        last_seen_section = doc[doc.index("lastSeenObjectId"):]
        assert "heapStatsUpdate" in last_seen_section

    async def test_add_inspected_heap_object_docstring_mentions_x(self) -> None:
        doc = HeapProfilerDomain.add_inspected_heap_object.__doc__
        assert doc is not None
        assert "$x" in doc
        assert "Command Line API" in doc

    async def test_start_sampling_docstring_major_gc_detailed(self) -> None:
        doc = HeapProfilerDomain.start_sampling.__doc__
        assert doc is not None
        assert "major GC" in doc
        assert "temporary memory" in doc

    async def test_start_sampling_docstring_minor_gc_detailed(self) -> None:
        doc = HeapProfilerDomain.start_sampling.__doc__
        assert doc is not None
        assert "minor GC" in doc
        assert "latency" in doc
