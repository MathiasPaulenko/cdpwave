"""Unit tests for HeapProfiler and PerformanceTimeline domains."""

import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.heap_profiler import HeapProfilerDomain
from cdpwave.domains.performance_timeline import PerformanceTimelineDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestHeapProfilerDomain:
    # --- enable / disable ---

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.enable()
        assert fake.last_call == ("HeapProfiler.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.disable()
        assert fake.last_call == ("HeapProfiler.disable", None)

    # --- add_inspected_heap_object ---

    async def test_add_inspected_heap_object(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.add_inspected_heap_object("heap-obj-1")
        assert fake.last_call == (
            "HeapProfiler.addInspectedHeapObject",
            {"heapObjectId": "heap-obj-1"},
        )

    async def test_add_inspected_heap_object_type_error(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="heap_object_id must be a str"):
            await domain.add_inspected_heap_object(123)  # type: ignore[arg-type]

    # --- collect_garbage ---

    async def test_collect_garbage(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.collect_garbage()
        assert fake.last_call == ("HeapProfiler.collectGarbage", None)

    # --- get_heap_object_id ---

    async def test_get_heap_object_id(self) -> None:
        fake = FakeSender({"heapSnapshotObjectId": "obj1"})
        domain = HeapProfilerDomain(fake)
        result = await domain.get_heap_object_id("remote-obj-1")
        assert fake.last_call == (
            "HeapProfiler.getHeapObjectId",
            {"objectId": "remote-obj-1"},
        )
        assert result == {"heapSnapshotObjectId": "obj1"}

    async def test_get_heap_object_id_type_error(self) -> None:
        fake = FakeSender({"heapSnapshotObjectId": "obj1"})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.get_heap_object_id(42)  # type: ignore[arg-type]

    # --- get_object_by_heap_object_id ---

    async def test_get_object_by_heap_object_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-obj-1")
        assert fake.last_call == (
            "HeapProfiler.getObjectByHeapObjectId",
            {"objectId": "heap-obj-1"},
        )

    async def test_get_object_by_heap_object_id_with_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-obj-1", object_group="grp")
        method, params = fake.last_call
        assert method == "HeapProfiler.getObjectByHeapObjectId"
        assert params is not None
        assert params["objectId"] == "heap-obj-1"
        assert params["objectGroup"] == "grp"

    async def test_get_object_by_heap_object_id_type_error(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="heap_object_id must be a str"):
            await domain.get_object_by_heap_object_id(42)  # type: ignore[arg-type]

    async def test_get_object_by_heap_object_id_type_error_object_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="object_group must be a str"):
            await domain.get_object_by_heap_object_id("heap-obj-1", object_group=42)  # type: ignore[arg-type]

    async def test_get_object_by_heap_object_id_return(self) -> None:
        fake = FakeSender({"result": {"type": "object"}})
        domain = HeapProfilerDomain(fake)
        result = await domain.get_object_by_heap_object_id("heap-obj-1")
        assert result == {"result": {"type": "object"}}

    # --- get_sampling_profile ---

    async def test_get_sampling_profile(self) -> None:
        fake = FakeSender({"profile": {"head": {}, "samples": []}})
        domain = HeapProfilerDomain(fake)
        await domain.get_sampling_profile()
        assert fake.last_call == ("HeapProfiler.getSamplingProfile", None)

    async def test_get_sampling_profile_return(self) -> None:
        profile = {
            "head": {
                "callFrame": {}, "selfSize": 1024.0,
                "id": 1, "children": [],
            },
            "samples": [],
        }
        fake = FakeSender({"profile": profile})
        domain = HeapProfilerDomain(fake)
        result = await domain.get_sampling_profile()
        assert result == {"profile": profile}

    # --- start_sampling ---

    async def test_start_sampling(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=4096)
        method, params = fake.last_call
        assert method == "HeapProfiler.startSampling"
        assert params is not None
        assert params["samplingInterval"] == 4096

    async def test_start_sampling_default(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling()
        method, params = fake.last_call
        assert method == "HeapProfiler.startSampling"
        assert params is not None
        assert params["includeObjectsCollectedByMajorGC"] is False
        assert params["includeObjectsCollectedByMinorGC"] is False
        assert "samplingInterval" not in params
        assert "stackDepth" not in params

    async def test_start_sampling_with_stack_depth(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=64)
        method, params = fake.last_call
        assert params is not None
        assert params["stackDepth"] == 64

    async def test_start_sampling_with_include_objects_collected_by_major_gc(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(include_objects_collected_by_major_gc=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeObjectsCollectedByMajorGC"] is True

    async def test_start_sampling_with_include_objects_collected_by_minor_gc(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(include_objects_collected_by_minor_gc=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeObjectsCollectedByMinorGC"] is True

    async def test_start_sampling_all_params(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(
            sampling_interval=8192,
            stack_depth=256,
            include_objects_collected_by_major_gc=True,
            include_objects_collected_by_minor_gc=True,
        )
        method, params = fake.last_call
        assert method == "HeapProfiler.startSampling"
        assert params is not None
        assert params["samplingInterval"] == 8192
        assert params["stackDepth"] == 256
        assert params["includeObjectsCollectedByMajorGC"] is True
        assert params["includeObjectsCollectedByMinorGC"] is True

    async def test_start_sampling_float_interval(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=4096.5)
        method, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 4096.5

    async def test_start_sampling_zero_interval_omitted(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=0)
        method, params = fake.last_call
        assert params is not None
        assert "samplingInterval" not in params

    async def test_start_sampling_zero_stack_depth_omitted(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=0)
        method, params = fake.last_call
        assert params is not None
        assert "stackDepth" not in params

    async def test_start_sampling_bool_as_int_sampling_interval(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="sampling_interval must be a number"):
            await domain.start_sampling(sampling_interval=True)  # type: ignore[arg-type]

    async def test_start_sampling_bool_as_int_stack_depth(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="stack_depth must be a number"):
            await domain.start_sampling(stack_depth=False)  # type: ignore[arg-type]

    async def test_start_sampling_type_error_sampling_interval_str(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="sampling_interval must be a number"):
            await domain.start_sampling(sampling_interval="4096")  # type: ignore[arg-type]

    async def test_start_sampling_type_error_stack_depth_str(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="stack_depth must be a number"):
            await domain.start_sampling(stack_depth="128")  # type: ignore[arg-type]

    async def test_start_sampling_type_error_include_major(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="include_objects_collected_by_major_gc must be a bool"):
            await domain.start_sampling(include_objects_collected_by_major_gc="yes")  # type: ignore[arg-type]

    async def test_start_sampling_type_error_include_minor(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="include_objects_collected_by_minor_gc must be a bool"):
            await domain.start_sampling(include_objects_collected_by_minor_gc=1)  # type: ignore[arg-type]

    # --- stop_sampling ---

    async def test_stop_sampling(self) -> None:
        fake = FakeSender({"profile": {}})
        domain = HeapProfilerDomain(fake)
        await domain.stop_sampling()
        assert fake.last_call == ("HeapProfiler.stopSampling", None)

    async def test_stop_sampling_return(self) -> None:
        profile = {
            "head": {
                "callFrame": {}, "selfSize": 512.0,
                "id": 1, "children": [],
            },
            "samples": [],
        }
        fake = FakeSender({"profile": profile})
        domain = HeapProfilerDomain(fake)
        result = await domain.stop_sampling()
        assert result == {"profile": profile}

    # --- start_tracking_heap_objects ---

    async def test_start_tracking_heap_objects(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_tracking_heap_objects(track_allocations=True)
        assert fake.last_call == (
            "HeapProfiler.startTrackingHeapObjects",
            {"trackAllocations": True},
        )

    async def test_start_tracking_heap_objects_default(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_tracking_heap_objects()
        assert fake.last_call == (
            "HeapProfiler.startTrackingHeapObjects",
            {"trackAllocations": False},
        )

    async def test_start_tracking_heap_objects_type_error(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="track_allocations must be a bool"):
            await domain.start_tracking_heap_objects(track_allocations="yes")  # type: ignore[arg-type]

    # --- stop_tracking_heap_objects ---

    async def test_stop_tracking_heap_objects(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects(report_progress=True)
        method, params = fake.last_call
        assert method == "HeapProfiler.stopTrackingHeapObjects"
        assert params is not None
        assert params["reportProgress"] is True

    async def test_stop_tracking_heap_objects_default(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects()
        method, params = fake.last_call
        assert method == "HeapProfiler.stopTrackingHeapObjects"
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is False
        assert params["exposeInternals"] is False

    async def test_stop_tracking_heap_objects_all_params(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects(
            report_progress=True,
            capture_numeric_value=True,
            expose_internals=True,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is True
        assert params["captureNumericValue"] is True
        assert params["exposeInternals"] is True

    async def test_stop_tracking_heap_objects_type_error_report_progress(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="report_progress must be a bool"):
            await domain.stop_tracking_heap_objects(report_progress="yes")  # type: ignore[arg-type]

    async def test_stop_tracking_heap_objects_type_error_capture_numeric_value(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="capture_numeric_value must be a bool"):
            await domain.stop_tracking_heap_objects(capture_numeric_value=1)  # type: ignore[arg-type]

    async def test_stop_tracking_heap_objects_type_error_expose_internals(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="expose_internals must be a bool"):
            await domain.stop_tracking_heap_objects(expose_internals="yes")  # type: ignore[arg-type]

    # --- take_heap_snapshot ---

    async def test_take_heap_snapshot(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot(report_progress=True)
        method, params = fake.last_call
        assert method == "HeapProfiler.takeHeapSnapshot"
        assert params is not None
        assert params["reportProgress"] is True

    async def test_take_heap_snapshot_default(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot()
        method, params = fake.last_call
        assert method == "HeapProfiler.takeHeapSnapshot"
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is False
        assert params["exposeInternals"] is False

    async def test_take_heap_snapshot_all_params(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot(
            report_progress=True,
            capture_numeric_value=True,
            expose_internals=True,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is True
        assert params["captureNumericValue"] is True
        assert params["exposeInternals"] is True

    async def test_take_heap_snapshot_type_error_report_progress(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="report_progress must be a bool"):
            await domain.take_heap_snapshot(report_progress="yes")  # type: ignore[arg-type]

    async def test_take_heap_snapshot_type_error_capture_numeric_value(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="capture_numeric_value must be a bool"):
            await domain.take_heap_snapshot(capture_numeric_value=1)  # type: ignore[arg-type]

    async def test_take_heap_snapshot_type_error_expose_internals(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        with pytest.raises(TypeError, match="expose_internals must be a bool"):
            await domain.take_heap_snapshot(expose_internals="yes")  # type: ignore[arg-type]

    # --- meta tests ---

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

    async def test_inherits_base_domain(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
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

    # --- edge cases (second pass) ---

    async def test_get_object_by_heap_object_id_empty_string_group_omitted(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-obj-1", object_group="")
        method, params = fake.last_call
        assert params is not None
        assert "objectGroup" not in params
        assert params["objectId"] == "heap-obj-1"

    async def test_add_inspected_heap_object_empty_string(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.add_inspected_heap_object("")
        assert fake.last_call == (
            "HeapProfiler.addInspectedHeapObject",
            {"heapObjectId": ""},
        )

    async def test_get_heap_object_id_empty_string(self) -> None:
        fake = FakeSender({"heapSnapshotObjectId": "obj1"})
        domain = HeapProfilerDomain(fake)
        await domain.get_heap_object_id("")
        assert fake.last_call == (
            "HeapProfiler.getHeapObjectId",
            {"objectId": ""},
        )

    async def test_start_sampling_negative_interval_sent(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=-1)
        method, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == -1

    async def test_start_sampling_negative_stack_depth_sent(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=-1)
        method, params = fake.last_call
        assert params is not None
        assert params["stackDepth"] == -1

    async def test_start_sampling_large_interval(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=2**53)
        method, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 2**53

    async def test_start_sampling_float_stack_depth(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=64.5)
        method, params = fake.last_call
        assert params is not None
        assert params["stackDepth"] == 64.5

    async def test_start_sampling_float_zero_interval_omitted(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=0.0)
        method, params = fake.last_call
        assert params is not None
        assert "samplingInterval" not in params

    async def test_start_sampling_float_zero_stack_depth_omitted(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=0.0)
        method, params = fake.last_call
        assert params is not None
        assert "stackDepth" not in params

    async def test_start_sampling_only_major_gc_true(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(include_objects_collected_by_major_gc=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeObjectsCollectedByMajorGC"] is True
        assert params["includeObjectsCollectedByMinorGC"] is False

    async def test_start_sampling_only_minor_gc_true(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(include_objects_collected_by_minor_gc=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeObjectsCollectedByMajorGC"] is False
        assert params["includeObjectsCollectedByMinorGC"] is True

    async def test_module_docstring_documents_all_events(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "addHeapSnapshotChunk" in doc
        assert "heapStatsUpdate" in doc
        assert "lastSeenObjectId" in doc
        assert "reportHeapSnapshotProgress" in doc
        assert "resetProfiles" in doc

    async def test_module_docstring_event_params(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "chunk" in doc
        assert "statsUpdate" in doc
        assert "lastSeenObjectId" in doc
        assert "timestamp" in doc
        assert "done" in doc
        assert "total" in doc
        assert "finished" in doc

    async def test_module_docstring_documents_types(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "HeapSnapshotObjectID" in doc
        assert "SamplingHeapProfileNode" in doc
        assert "SamplingHeapProfileSample" in doc
        assert "SamplingHeapProfile" in doc

    async def test_module_docstring_type_fields(self) -> None:
        import cdpwave.domains.heap_profiler as mod
        doc = mod.__doc__
        assert "callFrame" in doc
        assert "selfSize" in doc
        assert "ordinal" in doc
        assert "head" in doc
        assert "samples" in doc

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
        assert "heapStatsUpdate" in doc
        # The lastSeenObjectId event description should mention that
        # heapStatsUpdate events are sent before it if there were changes
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

    # --- edge cases (third pass) ---

    async def test_enable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_disable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_collect_garbage_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.collect_garbage()
        assert result == {}

    async def test_add_inspected_heap_object_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.add_inspected_heap_object("heap-1")
        assert result == {}

    async def test_start_sampling_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.start_sampling()
        assert result == {}

    async def test_start_tracking_heap_objects_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.start_tracking_heap_objects()
        assert result == {}

    async def test_stop_tracking_heap_objects_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.stop_tracking_heap_objects()
        assert result == {}

    async def test_take_heap_snapshot_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        result = await domain.take_heap_snapshot()
        assert result == {}

    async def test_start_sampling_both_zero_omitted(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=0, stack_depth=0)
        method, params = fake.last_call
        assert params is not None
        assert "samplingInterval" not in params
        assert "stackDepth" not in params
        assert params["includeObjectsCollectedByMajorGC"] is False
        assert params["includeObjectsCollectedByMinorGC"] is False

    async def test_start_sampling_int_accepted_for_float(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=4096, stack_depth=128)
        method, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 4096
        assert params["stackDepth"] == 128

    async def test_start_sampling_small_float(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(sampling_interval=0.001)
        method, params = fake.last_call
        assert params is not None
        assert params["samplingInterval"] == 0.001

    async def test_start_sampling_large_float(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(stack_depth=1e15)
        method, params = fake.last_call
        assert params is not None
        assert params["stackDepth"] == 1e15

    async def test_get_object_by_heap_object_id_explicit_none_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-1", object_group=None)
        method, params = fake.last_call
        assert params is not None
        assert "objectGroup" not in params
        assert params["objectId"] == "heap-1"

    async def test_take_heap_snapshot_only_capture_numeric_value(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot(capture_numeric_value=True)
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is True
        assert params["exposeInternals"] is False

    async def test_take_heap_snapshot_only_expose_internals(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot(expose_internals=True)
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is False
        assert params["exposeInternals"] is True

    async def test_stop_tracking_only_capture_numeric_value(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects(capture_numeric_value=True)
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is True
        assert params["exposeInternals"] is False

    async def test_stop_tracking_only_expose_internals(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects(expose_internals=True)
        method, params = fake.last_call
        assert params is not None
        assert params["reportProgress"] is False
        assert params["captureNumericValue"] is False
        assert params["exposeInternals"] is True

    async def test_start_sampling_params_key_count_default(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling()
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 2

    async def test_start_sampling_params_key_count_all(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_sampling(
            sampling_interval=4096,
            stack_depth=128,
            include_objects_collected_by_major_gc=True,
            include_objects_collected_by_minor_gc=True,
        )
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 4

    async def test_take_heap_snapshot_params_key_count(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot()
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 3

    async def test_stop_tracking_heap_objects_params_key_count(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects()
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 3

    async def test_start_tracking_heap_objects_params_key_count(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_tracking_heap_objects()
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 1

    async def test_add_inspected_heap_object_params_key_count(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.add_inspected_heap_object("heap-1")
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 1

    async def test_get_heap_object_id_params_key_count(self) -> None:
        fake = FakeSender({"heapSnapshotObjectId": "obj1"})
        domain = HeapProfilerDomain(fake)
        await domain.get_heap_object_id("remote-1")
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 1

    async def test_get_object_by_heap_object_id_params_key_count_no_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-1")
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 1

    async def test_get_object_by_heap_object_id_params_key_count_with_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-1", object_group="grp")
        method, params = fake.last_call
        assert params is not None
        assert len(params) == 2


@pytest.mark.unit
class TestPerformanceTimelineDomain:
    async def test_is_base_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        assert domain is not None

    async def test_enable_command_name(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable(["largest-contentful-paint"])
        method, _ = fake.last_call
        assert method == "PerformanceTimeline.enable"

    async def test_enable_json_key_camel_case(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable(["layout-shift"])
        _, params = fake.last_call
        assert "eventTypes" in params
        assert params["eventTypes"] == ["layout-shift"]

    async def test_enable_multiple_event_types(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable(["largest-contentful-paint", "layout-shift", "first-input"])
        _, params = fake.last_call
        assert params["eventTypes"] == ["largest-contentful-paint", "layout-shift", "first-input"]

    async def test_enable_empty_list_disables_recording(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        await domain.enable([])
        _, params = fake.last_call
        assert params["eventTypes"] == []

    async def test_enable_type_error_not_list(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        with pytest.raises(TypeError, match="event_types must be a list"):
            await domain.enable("largest-contentful-paint")  # type: ignore[arg-type]

    async def test_enable_type_error_element_not_str(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        with pytest.raises(TypeError, match="event_types\\[1\\] must be a str"):
            await domain.enable(["lcp", 42])  # type: ignore[list-item]

    async def test_enable_type_error_dict_element(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        with pytest.raises(TypeError, match="event_types\\[0\\] must be a str"):
            await domain.enable([{"name": "lcp"}])  # type: ignore[list-item]
