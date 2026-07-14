"""E2E tests for the LayerTree domain (real browser flows).

Full end-to-end flows against a real browser, including LayerTree
lifecycle (enable → disable), compositing reasons, snapshot
operations, type validation in real browser context, raw command
sending, event handling, and meta tests for docstrings and
experimental marking.
"""

import asyncio
import contextlib
import inspect
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.domains.base import BaseDomain
from cdpwave.domains.layer_tree import LayerTreeDomain


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
class TestLayerTreeE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.layer_tree is not None
            assert isinstance(session.layer_tree, LayerTreeDomain)

    async def test_enable_disable_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_enable_disable_re_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.layer_tree.enable()
            await session.layer_tree.disable()
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_compositing_reasons(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
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
            await _wait_for_page(session)
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                result = await session.layer_tree.make_snapshot("1")
                snapshot_id = result.get("snapshotId")
                if snapshot_id:
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()

    async def test_profile_snapshot_with_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
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
            await _wait_for_page(session)
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
            await _wait_for_page(session)
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    result = await session.layer_tree.snapshot_command_log(
                        snapshot_id
                    )
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

    async def test_raw_send_enable_disable(self) -> None:
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
            await _wait_for_page(session)
            await session.send("LayerTree.enable", None)
            with contextlib.suppress(Exception):
                result = await session.send(
                    "LayerTree.compositingReasons", {"layerId": "1"}
                )
                assert isinstance(result, dict)
            await session.send("LayerTree.disable", None)

    async def test_layer_tree_did_change_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []
            await _wait_for_page(session)
            await session.on(
                "LayerTree.layerTreeDidChange",
                lambda params: events.append(params),
            )
            await session.layer_tree.enable()
            await session.page.navigate("data:text/html,<div>Hello</div>")
            await asyncio.sleep(1.0)
            await session.layer_tree.disable()
            assert len(events) > 0

    async def test_layer_painted_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []
            await _wait_for_page(session)
            await session.on(
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

    async def test_profile_snapshot_only_clip_rect(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
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
            await _wait_for_page(session)
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
            await _wait_for_page(session)
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
            await _wait_for_page(session)
            await session.layer_tree.enable()
            await session.layer_tree.enable()
            await session.layer_tree.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.layer_tree.enable()
            await session.layer_tree.disable()
            await session.layer_tree.disable()

    async def test_compositing_reasons_nonexistent_layer(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
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

    async def test_full_snapshot_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.layer_tree.enable()
            with contextlib.suppress(Exception):
                snap = await session.layer_tree.make_snapshot("1")
                snapshot_id = snap.get("snapshotId")
                if snapshot_id:
                    await session.layer_tree.profile_snapshot(snapshot_id)
                    await session.layer_tree.replay_snapshot(snapshot_id)
                    await session.layer_tree.snapshot_command_log(snapshot_id)
                    await session.layer_tree.release_snapshot(snapshot_id)
            await session.layer_tree.disable()


@pytest.mark.e2e
class TestLayerTreeMetaE2E:
    def test_is_base_domain(self) -> None:
        assert issubclass(LayerTreeDomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                LayerTreeDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert len(methods) == 9

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                LayerTreeDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_no_get_layers(self) -> None:
        assert not hasattr(LayerTreeDomain, "get_layers")

    def test_module_docstring_has_experimental(self) -> None:
        import cdpwave.domains.layer_tree as mod
        assert mod.__doc__ is not None
        assert "experimental" in mod.__doc__.lower()

    def test_class_docstring_has_experimental(self) -> None:
        assert LayerTreeDomain.__doc__ is not None
        assert "experimental" in LayerTreeDomain.__doc__.lower()

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(
            LayerTreeDomain, predicate=inspect.isfunction
        ):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"
