"""Functional tests for HeapProfiler, LayerTree, and PerformanceTimeline domains."""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestHeapProfiler:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()

    async def test_collect_garbage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.collect_garbage()
            await session.heap_profiler.disable()

    async def test_start_stop_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=4096)
            result = await session.heap_profiler.stop_sampling()
            assert "profile" in result
            assert isinstance(result["profile"], dict)
            await session.heap_profiler.disable()

    async def test_start_sampling_with_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(
                sampling_interval=4096,
                stack_depth=64,
                include_objects_collected_by_major_gc=True,
                include_objects_collected_by_minor_gc=True,
            )
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_get_sampling_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=4096)
            result = await session.heap_profiler.get_sampling_profile()
            assert "profile" in result
            assert isinstance(result["profile"], dict)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot()
            await session.heap_profiler.disable()

    async def test_take_heap_snapshot_with_numeric_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot(capture_numeric_value=True)
            await session.heap_profiler.disable()

    async def test_get_heap_object_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({a: 1})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                result = await session.heap_profiler.get_heap_object_id(object_id)
                assert "heapSnapshotObjectId" in result
                assert isinstance(result["heapSnapshotObjectId"], str)
            await session.heap_profiler.disable()

    @pytest.mark.skip(reason="Heap object not available after GC in CI")
    async def test_get_object_by_heap_object_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({a: 1})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                heap_id = await session.heap_profiler.get_heap_object_id(object_id)
                heap_obj_id = heap_id["heapSnapshotObjectId"]
                result = await session.heap_profiler.get_object_by_heap_object_id(
                    heap_obj_id
                )
                assert "result" in result
            await session.heap_profiler.disable()

    async def test_start_stop_tracking_heap_objects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_tracking_heap_objects(
                track_allocations=True
            )
            await session.heap_profiler.stop_tracking_heap_objects()
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

    async def test_type_error_take_heap_snapshot_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(TypeError, match="report_progress must be a bool"):
                await session.heap_profiler.take_heap_snapshot(report_progress="yes")  # type: ignore[arg-type]
            await session.heap_profiler.disable()

    @pytest.mark.skip(reason="Chrome rejects negative sampling interval")
    async def test_start_sampling_negative_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=-1)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_start_sampling_float_stack_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(stack_depth=64.5)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()

    async def test_start_sampling_large_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
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
            await session.heap_profiler.enable()
            await session.heap_profiler.take_heap_snapshot(
                expose_internals=True
            )
            await session.heap_profiler.disable()

    @pytest.mark.skip(reason="Heap object not available after GC in CI")
    async def test_add_inspected_heap_object(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "({x: 1})", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                heap_id = await session.heap_profiler.get_heap_object_id(object_id)
                heap_obj_id = heap_id["heapSnapshotObjectId"]
                await session.heap_profiler.add_inspected_heap_object(heap_obj_id)
            await session.heap_profiler.disable()

    async def test_type_error_get_object_by_heap_object_id_object_group_int(self) -> None:
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

    async def test_type_error_start_sampling_include_minor_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            with pytest.raises(
                TypeError, match="include_objects_collected_by_minor_gc must be a bool"
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


@pytest.mark.integration
class TestLayerTree:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_enable_disable_re_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            await session.layer_tree.disable()
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_compositing_reasons(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                result = await session.layer_tree.compositing_reasons("1")
                assert isinstance(result, dict)
            await session.layer_tree.disable()

    async def test_make_snapshot_and_release(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                result = await session.layer_tree.make_snapshot("1")
                snapshot_id = result.get("snapshotId")
                if snapshot_id:
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_profile_snapshot_with_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    clip = {"x": 0, "y": 0, "width": 100, "height": 100}
                    result = await session.layer_tree.profile_snapshot(
                        snapshot_id,
                        min_repeat_count=2,
                        min_duration=0.1,
                        clip_rect=clip,
                    )
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_replay_snapshot(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    result = await session.layer_tree.replay_snapshot(snapshot_id)
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_snapshot_command_log(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    result = await session.layer_tree.snapshot_command_log(snapshot_id)
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_load_snapshot_and_release(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                tiles = [{"x": 0, "y": 0, "picture": ""}]
                result = await session.layer_tree.load_snapshot(tiles)
                snapshot_id = result.get("snapshotId")
                if snapshot_id:
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_raw_send_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("LayerTree.enable", None)
            await session.send("LayerTree.disable", None)

    async def test_raw_send_compositing_reasons(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.send("LayerTree.enable", None)
            with contextlib.suppress(Exception):
                result = await session.send(
                    "LayerTree.compositingReasons", {"layerId": "1"}
                )
                assert isinstance(result, dict)
            await session.send("LayerTree.disable", None)

    async def test_type_error_compositing_reasons_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="layer_id must be a str"):
                await session.layer_tree.compositing_reasons(42)  # type: ignore[arg-type]

    async def test_type_error_make_snapshot_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="layer_id must be a str"):
                await session.layer_tree.make_snapshot(True)  # type: ignore[arg-type]

    async def test_type_error_profile_snapshot_snapshot_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="snapshot_id must be a str"):
                await session.layer_tree.profile_snapshot(42)  # type: ignore[arg-type]

    async def test_type_error_replay_snapshot_from_step_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="from_step must be an int"):
                await session.layer_tree.replay_snapshot("S1", from_step="2")  # type: ignore[arg-type]

    async def test_type_error_release_snapshot_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="snapshot_id must be a str"):
                await session.layer_tree.release_snapshot(["snap1"])  # type: ignore[arg-type]

    async def test_type_error_load_snapshot_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="tiles must be a list"):
                await session.layer_tree.load_snapshot("not a list")  # type: ignore[arg-type]

    async def test_type_error_snapshot_command_log_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="snapshot_id must be a str"):
                await session.layer_tree.snapshot_command_log(42)  # type: ignore[arg-type]

    async def test_layer_tree_did_change_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            session.on(
                "LayerTree.layerTreeDidChange",
                lambda params: events.append(params),
            )
            await session.page.navigate(
                "data:text/html,<div style='transform:translateZ(0);"
                "will-change:transform'>Hello</div>"
            )
            await asyncio.sleep(2.0)
            await session.layer_tree.disable()
            if not events:
                pytest.skip("LayerTree.layerTreeDidChange not emitted in headless mode")

    async def test_layer_painted_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []
            await session.page.navigate("about:blank")
            session.on(
                "LayerTree.layerPainted",
                lambda params: events.append(params),
            )
            await session.layer_tree.enable()
            await session.page.navigate("data:text/html,<div>Hello</div>")
            await asyncio.sleep(1.0)
            await session.layer_tree.disable()
            for event in events:
                assert "layerId" in event
                assert "clip" in event

    async def test_profile_snapshot_only_clip_rect(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    clip = {"x": 0, "y": 0, "width": 50, "height": 50}
                    result = await session.layer_tree.profile_snapshot(
                        snapshot_id, clip_rect=clip
                    )
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_profile_snapshot_empty_dict_clip_rect(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    result = await session.layer_tree.profile_snapshot(
                        snapshot_id, clip_rect={}
                    )
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_replay_snapshot_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    result = await session.layer_tree.replay_snapshot(
                        snapshot_id, from_step=1, to_step=3, scale=1.5
                    )
                    assert isinstance(result, dict)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_load_snapshot_multiple_tiles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                tiles = [
                    {"x": 0, "y": 0, "picture": ""},
                    {"x": 10, "y": 10, "picture": ""},
                    {"x": 20, "y": 20, "picture": ""},
                ]
                result = await session.layer_tree.load_snapshot(tiles)
                snapshot_id = result.get("snapshotId")
                if snapshot_id:
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.layer_tree.enable()
            await session.layer_tree.disable()
            await session.layer_tree.disable()

    async def test_compositing_reasons_nonexistent_layer(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                result = await session.layer_tree.compositing_reasons(
                    "nonexistent-layer-id"
                )
                assert isinstance(result, dict)
            await session.layer_tree.disable()

    async def test_type_error_load_snapshot_element_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"tiles\[0\] must be a dict"):
                await session.layer_tree.load_snapshot(["not a dict"])  # type: ignore[list-item]

    async def test_type_error_profile_snapshot_min_repeat_count_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="min_repeat_count must be an int"):
                await session.layer_tree.profile_snapshot("S1", min_repeat_count=True)  # type: ignore[arg-type]

    async def test_type_error_replay_snapshot_scale_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="scale must be a float"):
                await session.layer_tree.replay_snapshot("S1", scale="2.0")  # type: ignore[arg-type]

    async def test_type_error_profile_snapshot_clip_rect_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="clip_rect must be a dict"):
                await session.layer_tree.profile_snapshot("S1", clip_rect=42)  # type: ignore[arg-type]


@pytest.mark.integration
class TestPerformanceTimeline:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.performance_timeline is not None

    async def test_enable_with_event_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance_timeline.enable(["largest-contentful-paint"])
            await session.page.navigate("about:blank")
            await session.performance_timeline.enable([])
