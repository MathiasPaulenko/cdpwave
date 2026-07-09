"""Unit tests for HeapProfiler, LayerTree, and PerformanceTimeline domains."""

import pytest

from cdpwave.domains.heap_profiler import HeapProfilerDomain
from cdpwave.domains.layer_tree import LayerTreeDomain
from cdpwave.domains.performance_timeline import PerformanceTimelineDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestHeapProfilerDomain:
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
        assert fake.last_call == ("HeapProfiler.startSampling", {})

    async def test_stop_sampling(self) -> None:
        fake = FakeSender({"profile": {}})
        domain = HeapProfilerDomain(fake)
        await domain.stop_sampling()
        assert fake.last_call == ("HeapProfiler.stopSampling", None)

    async def test_take_heap_snapshot(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.take_heap_snapshot(report_progress=True)
        method, params = fake.last_call
        assert method == "HeapProfiler.takeHeapSnapshot"
        assert params is not None
        assert params["reportProgress"] is True

    async def test_collect_garbage(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.collect_garbage()
        assert fake.last_call == ("HeapProfiler.collectGarbage", None)

    async def test_get_heap_object_id(self) -> None:
        fake = FakeSender({"heapSnapshotObjectId": "obj1"})
        domain = HeapProfilerDomain(fake)
        await domain.get_heap_object_id("remote-obj-1")
        assert fake.last_call == (
            "HeapProfiler.getHeapObjectId",
            {"objectId": "remote-obj-1"},
        )

    async def test_get_object_by_heap_object_id(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-obj-1")
        assert fake.last_call == (
            "HeapProfiler.getObjectByHeapObjectId",
            {"heapObjectId": "heap-obj-1"},
        )

    async def test_get_object_by_heap_object_id_with_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = HeapProfilerDomain(fake)
        await domain.get_object_by_heap_object_id("heap-obj-1", object_group="grp")
        method, params = fake.last_call
        assert params is not None
        assert params["objectGroup"] == "grp"

    async def test_start_tracking_heap_objects(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.start_tracking_heap_objects(track_allocations=True)
        assert fake.last_call == (
            "HeapProfiler.startTrackingHeapObjects",
            {"trackAllocations": True},
        )

    async def test_stop_tracking_heap_objects(self) -> None:
        fake = FakeSender({})
        domain = HeapProfilerDomain(fake)
        await domain.stop_tracking_heap_objects(report_progress=True)
        assert fake.last_call == (
            "HeapProfiler.stopTrackingHeapObjects",
            {"reportProgress": True},
        )


@pytest.mark.unit
class TestLayerTreeDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.enable()
        assert fake.last_call == ("LayerTree.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.disable()
        assert fake.last_call == ("LayerTree.disable", None)

    async def test_get_layers(self) -> None:
        fake = FakeSender({"layers": []})
        domain = LayerTreeDomain(fake)
        await domain.get_layers()
        assert fake.last_call == ("LayerTree.getLayers", {})

    async def test_get_layers_with_root_id(self) -> None:
        fake = FakeSender({"layers": []})
        domain = LayerTreeDomain(fake)
        await domain.get_layers(root_id=42)
        method, params = fake.last_call
        assert method == "LayerTree.getLayers"
        assert params is not None
        assert params["rootId"] == 42

    async def test_compositing_reasons(self) -> None:
        fake = FakeSender({"compositingReasons": [], "compositingReasonIds": []})
        domain = LayerTreeDomain(fake)
        await domain.compositing_reasons("layer1")
        assert fake.last_call == (
            "LayerTree.compositingReasons",
            {"layerId": "layer1"},
        )

    async def test_load_snapshot(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        tiles = [{"dip": {"x": 0, "y": 0, "width": 100, "height": 100}}]
        await domain.load_snapshot(tiles)
        method, params = fake.last_call
        assert method == "LayerTree.loadSnapshot"
        assert params is not None
        assert params["tiles"] == tiles

    async def test_release_snapshot(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.release_snapshot("snap1")
        assert fake.last_call == (
            "LayerTree.releaseSnapshot",
            {"snapshotId": "snap1"},
        )

    async def test_profile_snapshot(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_interval_ms=50)
        method, params = fake.last_call
        assert method == "LayerTree.profileSnapshot"
        assert params is not None
        assert params["snapshotId"] == "snap1"
        assert params["minIntervalMS"] == 50

    async def test_profile_snapshot_with_clip_rect(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        clip = {"x": 0, "y": 0, "width": 100, "height": 100}
        await domain.profile_snapshot("snap1", clip_rect=clip)
        method, params = fake.last_call
        assert params is not None
        assert params["clipRect"] == clip


@pytest.mark.unit
class TestPerformanceTimelineDomain:
    async def test_is_base_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceTimelineDomain(fake)
        assert domain is not None
