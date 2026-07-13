"""Unit tests for the LayerTree domain.

Tests cover:
- Each method (basic call, correct params, return value)
- omitempty behaviour (None, 0, "", empty omitted)
- Type validation (TypeError for each param)
- Meta-tests (method count, alphabetical order, docstrings)
- Edge cases: non-string falsy values (0, False, []) raise TypeError
"""

import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.layer_tree import LayerTreeDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestLayerTreeDomain:
    # --- compositing_reasons ---

    async def test_compositing_reasons(self) -> None:
        fake = FakeSender({"compositingReasons": ["r1"], "compositingReasonIds": ["id1"]})
        domain = LayerTreeDomain(fake)
        result = await domain.compositing_reasons("layer1")
        assert fake.last_call == (
            "LayerTree.compositingReasons",
            {"layerId": "layer1"},
        )
        assert result["compositingReasons"] == ["r1"]
        assert result["compositingReasonIds"] == ["id1"]

    async def test_compositing_reasons_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons(42)  # type: ignore[arg-type]

    async def test_compositing_reasons_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons(True)  # type: ignore[arg-type]

    async def test_compositing_reasons_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons(["layer1"])  # type: ignore[arg-type]

    async def test_compositing_reasons_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons({"id": "layer1"})  # type: ignore[arg-type]

    async def test_compositing_reasons_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons(3.14)  # type: ignore[arg-type]

    async def test_compositing_reasons_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.compositing_reasons(None)  # type: ignore[arg-type]

    async def test_compositing_reasons_empty_string(self) -> None:
        fake = FakeSender({"compositingReasons": [], "compositingReasonIds": []})
        domain = LayerTreeDomain(fake)
        await domain.compositing_reasons("")
        assert fake.last_call == ("LayerTree.compositingReasons", {"layerId": ""})

    # --- disable ---

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.disable()
        assert fake.last_call == ("LayerTree.disable", None)

    # --- enable ---

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.enable()
        assert fake.last_call == ("LayerTree.enable", None)

    # --- load_snapshot ---

    async def test_load_snapshot(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        tiles = [{"x": 0, "y": 0, "picture": "abc"}]
        result = await domain.load_snapshot(tiles)
        method, params = fake.last_call
        assert method == "LayerTree.loadSnapshot"
        assert params is not None
        assert params["tiles"] == tiles
        assert result["snapshotId"] == "snap1"

    async def test_load_snapshot_type_error_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="tiles must be a list"):
            await domain.load_snapshot("not a list")  # type: ignore[arg-type]

    async def test_load_snapshot_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="tiles must be a list"):
            await domain.load_snapshot(42)  # type: ignore[arg-type]

    async def test_load_snapshot_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="tiles must be a list"):
            await domain.load_snapshot({"x": 0})  # type: ignore[arg-type]

    async def test_load_snapshot_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="tiles must be a list"):
            await domain.load_snapshot(True)  # type: ignore[arg-type]

    async def test_load_snapshot_type_error_element_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match=r"tiles\[0\] must be a dict"):
            await domain.load_snapshot(["not a dict"])  # type: ignore[list-item]

    async def test_load_snapshot_type_error_element_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match=r"tiles\[0\] must be a dict"):
            await domain.load_snapshot([42])  # type: ignore[list-item]

    async def test_load_snapshot_type_error_element_int_at_index_1(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match=r"tiles\[1\] must be a dict"):
            await domain.load_snapshot([{"x": 0}, 42])  # type: ignore[list-item]

    async def test_load_snapshot_type_error_element_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match=r"tiles\[0\] must be a dict"):
            await domain.load_snapshot([True])  # type: ignore[list-item]

    async def test_load_snapshot_type_error_element_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match=r"tiles\[0\] must be a dict"):
            await domain.load_snapshot([[1, 2]])  # type: ignore[list-item]

    async def test_load_snapshot_empty_list(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        await domain.load_snapshot([])
        assert fake.last_call == ("LayerTree.loadSnapshot", {"tiles": []})

    async def test_load_snapshot_multiple_tiles(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        tiles = [
            {"x": 0, "y": 0, "picture": "abc"},
            {"x": 10, "y": 10, "picture": "def"},
            {"x": 20, "y": 20, "picture": "ghi"},
        ]
        await domain.load_snapshot(tiles)
        _, params = fake.last_call
        assert params is not None
        assert params["tiles"] == tiles

    # --- make_snapshot ---

    async def test_make_snapshot(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        result = await domain.make_snapshot("layer1")
        assert fake.last_call == (
            "LayerTree.makeSnapshot",
            {"layerId": "layer1"},
        )
        assert result["snapshotId"] == "snap1"

    async def test_make_snapshot_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.make_snapshot(42)  # type: ignore[arg-type]

    async def test_make_snapshot_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.make_snapshot(False)  # type: ignore[arg-type]

    async def test_make_snapshot_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.make_snapshot(3.14)  # type: ignore[arg-type]

    async def test_make_snapshot_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.make_snapshot(["layer1"])  # type: ignore[arg-type]

    async def test_make_snapshot_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="layer_id must be a str"):
            await domain.make_snapshot({"id": "layer1"})  # type: ignore[arg-type]

    async def test_make_snapshot_empty_string(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        await domain.make_snapshot("")
        assert fake.last_call == ("LayerTree.makeSnapshot", {"layerId": ""})

    # --- profile_snapshot ---

    async def test_profile_snapshot_basic(self) -> None:
        fake = FakeSender({"timings": [[1.0, 2.0]]})
        domain = LayerTreeDomain(fake)
        result = await domain.profile_snapshot("snap1")
        method, params = fake.last_call
        assert method == "LayerTree.profileSnapshot"
        assert params is not None
        assert params["snapshotId"] == "snap1"
        assert "minRepeatCount" not in params
        assert "minDuration" not in params
        assert "clipRect" not in params
        assert result["timings"] == [[1.0, 2.0]]

    async def test_profile_snapshot_with_min_repeat_count(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_repeat_count=5)
        _, params = fake.last_call
        assert params is not None
        assert params["minRepeatCount"] == 5

    async def test_profile_snapshot_with_min_duration(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_duration=0.5)
        _, params = fake.last_call
        assert params is not None
        assert params["minDuration"] == 0.5

    async def test_profile_snapshot_with_clip_rect(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        clip = {"x": 0, "y": 0, "width": 100, "height": 100}
        await domain.profile_snapshot("snap1", clip_rect=clip)
        _, params = fake.last_call
        assert params is not None
        assert params["clipRect"] == clip

    async def test_profile_snapshot_omit_min_repeat_count_zero(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_repeat_count=0)
        _, params = fake.last_call
        assert params is not None
        assert "minRepeatCount" not in params

    async def test_profile_snapshot_omit_min_duration_zero(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_duration=0.0)
        _, params = fake.last_call
        assert params is not None
        assert "minDuration" not in params

    async def test_profile_snapshot_omit_min_duration_zero_int(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_duration=0)
        _, params = fake.last_call
        assert params is not None
        assert "minDuration" not in params

    async def test_profile_snapshot_omit_clip_rect_none(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", clip_rect=None)
        _, params = fake.last_call
        assert params is not None
        assert "clipRect" not in params

    async def test_profile_snapshot_all_params(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        clip = {"x": 10, "y": 10, "width": 50, "height": 50}
        await domain.profile_snapshot(
            "snap1",
            min_repeat_count=3,
            min_duration=1.5,
            clip_rect=clip,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["snapshotId"] == "snap1"
        assert params["minRepeatCount"] == 3
        assert params["minDuration"] == 1.5
        assert params["clipRect"] == clip

    async def test_profile_snapshot_type_error_snapshot_id_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.profile_snapshot(42)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_snapshot_id_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.profile_snapshot(True)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_repeat_count_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_repeat_count must be an int"):
            await domain.profile_snapshot("snap1", min_repeat_count="5")  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_repeat_count_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_repeat_count must be an int"):
            await domain.profile_snapshot("snap1", min_repeat_count=True)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_repeat_count_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_repeat_count must be an int"):
            await domain.profile_snapshot("snap1", min_repeat_count=5.0)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_duration_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_duration must be a float"):
            await domain.profile_snapshot("snap1", min_duration="0.5")  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_duration_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_duration must be a float"):
            await domain.profile_snapshot("snap1", min_duration=False)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_clip_rect_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="clip_rect must be a dict"):
            await domain.profile_snapshot("snap1", clip_rect="not a dict")  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_clip_rect_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="clip_rect must be a dict"):
            await domain.profile_snapshot("snap1", clip_rect=42)  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_clip_rect_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="clip_rect must be a dict"):
            await domain.profile_snapshot("snap1", clip_rect=[1, 2])  # type: ignore[arg-type]

    async def test_profile_snapshot_accepts_int_for_min_duration(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_duration=1)
        _, params = fake.last_call
        assert params is not None
        assert params["minDuration"] == 1

    async def test_profile_snapshot_empty_dict_clip_rect_sent(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", clip_rect={})
        _, params = fake.last_call
        assert params is not None
        assert params["clipRect"] == {}

    async def test_profile_snapshot_negative_min_repeat_count_sent(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_repeat_count=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["minRepeatCount"] == -1

    async def test_profile_snapshot_negative_min_duration_sent(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_duration=-0.5)
        _, params = fake.last_call
        assert params is not None
        assert params["minDuration"] == -0.5

    async def test_profile_snapshot_type_error_snapshot_id_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.profile_snapshot(["snap1"])  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_snapshot_id_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.profile_snapshot({"id": "snap1"})  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_repeat_count_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_repeat_count must be an int"):
            await domain.profile_snapshot("snap1", min_repeat_count=[1])  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_min_duration_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="min_duration must be a float"):
            await domain.profile_snapshot("snap1", min_duration=[0.5])  # type: ignore[arg-type]

    async def test_profile_snapshot_type_error_clip_rect_tuple(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="clip_rect must be a dict"):
            await domain.profile_snapshot("snap1", clip_rect=(1, 2))  # type: ignore[arg-type]

    # --- release_snapshot ---

    async def test_release_snapshot(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.release_snapshot("snap1")
        assert fake.last_call == (
            "LayerTree.releaseSnapshot",
            {"snapshotId": "snap1"},
        )

    async def test_release_snapshot_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.release_snapshot(42)  # type: ignore[arg-type]

    async def test_release_snapshot_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.release_snapshot(False)  # type: ignore[arg-type]

    async def test_release_snapshot_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.release_snapshot(["snap1"])  # type: ignore[arg-type]

    async def test_release_snapshot_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.release_snapshot(3.14)  # type: ignore[arg-type]

    async def test_release_snapshot_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.release_snapshot({"id": "snap1"})  # type: ignore[arg-type]

    async def test_release_snapshot_empty_string(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        await domain.release_snapshot("")
        assert fake.last_call == (
            "LayerTree.releaseSnapshot",
            {"snapshotId": ""},
        )

    # --- replay_snapshot ---

    async def test_replay_snapshot_basic(self) -> None:
        fake = FakeSender({"dataURL": "data:image/png;base64,..."})
        domain = LayerTreeDomain(fake)
        result = await domain.replay_snapshot("snap1")
        method, params = fake.last_call
        assert method == "LayerTree.replaySnapshot"
        assert params is not None
        assert params["snapshotId"] == "snap1"
        assert "fromStep" not in params
        assert "toStep" not in params
        assert "scale" not in params
        assert result["dataURL"] == "data:image/png;base64,..."

    async def test_replay_snapshot_with_from_step(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", from_step=2)
        _, params = fake.last_call
        assert params is not None
        assert params["fromStep"] == 2

    async def test_replay_snapshot_with_to_step(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", to_step=5)
        _, params = fake.last_call
        assert params is not None
        assert params["toStep"] == 5

    async def test_replay_snapshot_with_scale(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", scale=2.0)
        _, params = fake.last_call
        assert params is not None
        assert params["scale"] == 2.0

    async def test_replay_snapshot_all_params(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", from_step=1, to_step=3, scale=1.5)
        _, params = fake.last_call
        assert params is not None
        assert params["snapshotId"] == "snap1"
        assert params["fromStep"] == 1
        assert params["toStep"] == 3
        assert params["scale"] == 1.5

    async def test_replay_snapshot_omit_from_step_zero(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", from_step=0)
        _, params = fake.last_call
        assert params is not None
        assert "fromStep" not in params

    async def test_replay_snapshot_omit_to_step_zero(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", to_step=0)
        _, params = fake.last_call
        assert params is not None
        assert "toStep" not in params

    async def test_replay_snapshot_omit_scale_zero(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", scale=0.0)
        _, params = fake.last_call
        assert params is not None
        assert "scale" not in params

    async def test_replay_snapshot_omit_scale_zero_int(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", scale=0)
        _, params = fake.last_call
        assert params is not None
        assert "scale" not in params

    async def test_replay_snapshot_type_error_snapshot_id_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.replay_snapshot(42)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_snapshot_id_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.replay_snapshot(True)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_from_step_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="from_step must be an int"):
            await domain.replay_snapshot("snap1", from_step="2")  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_from_step_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="from_step must be an int"):
            await domain.replay_snapshot("snap1", from_step=True)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_from_step_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="from_step must be an int"):
            await domain.replay_snapshot("snap1", from_step=2.0)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_to_step_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="to_step must be an int"):
            await domain.replay_snapshot("snap1", to_step="5")  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_to_step_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="to_step must be an int"):
            await domain.replay_snapshot("snap1", to_step=False)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_scale_str(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="scale must be a float"):
            await domain.replay_snapshot("snap1", scale="2.0")  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_scale_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="scale must be a float"):
            await domain.replay_snapshot("snap1", scale=True)  # type: ignore[arg-type]

    async def test_replay_snapshot_accepts_int_for_scale(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", scale=2)
        _, params = fake.last_call
        assert params is not None
        assert params["scale"] == 2

    async def test_replay_snapshot_negative_from_step_sent(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", from_step=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["fromStep"] == -1

    async def test_replay_snapshot_negative_to_step_sent(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", to_step=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["toStep"] == -1

    async def test_replay_snapshot_negative_scale_sent(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", scale=-1.5)
        _, params = fake.last_call
        assert params is not None
        assert params["scale"] == -1.5

    async def test_replay_snapshot_type_error_snapshot_id_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.replay_snapshot(["snap1"])  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_snapshot_id_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.replay_snapshot({"id": "snap1"})  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_to_step_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="to_step must be an int"):
            await domain.replay_snapshot("snap1", to_step=5.5)  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_to_step_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="to_step must be an int"):
            await domain.replay_snapshot("snap1", to_step=[5])  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_scale_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="scale must be a float"):
            await domain.replay_snapshot("snap1", scale=[2.0])  # type: ignore[arg-type]

    async def test_replay_snapshot_type_error_scale_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="scale must be a float"):
            await domain.replay_snapshot("snap1", scale={"x": 2})  # type: ignore[arg-type]

    # --- snapshot_command_log ---

    async def test_snapshot_command_log(self) -> None:
        fake = FakeSender({"commandLog": [{"name": "drawRect"}]})
        domain = LayerTreeDomain(fake)
        result = await domain.snapshot_command_log("snap1")
        assert fake.last_call == (
            "LayerTree.snapshotCommandLog",
            {"snapshotId": "snap1"},
        )
        assert result["commandLog"] == [{"name": "drawRect"}]

    async def test_snapshot_command_log_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.snapshot_command_log(42)  # type: ignore[arg-type]

    async def test_snapshot_command_log_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.snapshot_command_log(False)  # type: ignore[arg-type]

    async def test_snapshot_command_log_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.snapshot_command_log(["snap1"])  # type: ignore[arg-type]

    async def test_snapshot_command_log_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.snapshot_command_log(3.14)  # type: ignore[arg-type]

    async def test_snapshot_command_log_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = LayerTreeDomain(fake)
        with pytest.raises(TypeError, match="snapshot_id must be a str"):
            await domain.snapshot_command_log({"id": "snap1"})  # type: ignore[arg-type]

    async def test_snapshot_command_log_empty_string(self) -> None:
        fake = FakeSender({"commandLog": []})
        domain = LayerTreeDomain(fake)
        await domain.snapshot_command_log("")
        assert fake.last_call == (
            "LayerTree.snapshotCommandLog",
            {"snapshotId": ""},
        )

    # --- multi-call isolation ---

    async def test_multi_call_params_isolation(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain.profile_snapshot("snap1", min_repeat_count=5, min_duration=2.0)
        await domain.profile_snapshot("snap2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["snapshotId"] == "snap1"
        assert params1["minRepeatCount"] == 5
        assert params1["minDuration"] == 2.0
        assert params2["snapshotId"] == "snap2"
        assert "minRepeatCount" not in params2
        assert "minDuration" not in params2

    async def test_multi_call_replay_isolation(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain.replay_snapshot("snap1", from_step=1, to_step=3, scale=1.5)
        await domain.replay_snapshot("snap2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["fromStep"] == 1
        assert params1["toStep"] == 3
        assert params1["scale"] == 1.5
        assert "fromStep" not in params2
        assert "toStep" not in params2
        assert "scale" not in params2

    # --- raw send ---

    async def test_raw_send_compositing_reasons(self) -> None:
        fake = FakeSender({"compositingReasons": [], "compositingReasonIds": []})
        domain = LayerTreeDomain(fake)
        await domain._call("LayerTree.compositingReasons", {"layerId": "L1"})
        assert fake.last_call == (
            "LayerTree.compositingReasons",
            {"layerId": "L1"},
        )

    async def test_raw_send_profile_snapshot(self) -> None:
        fake = FakeSender({"timings": []})
        domain = LayerTreeDomain(fake)
        await domain._call(
            "LayerTree.profileSnapshot",
            {"snapshotId": "S1", "minRepeatCount": 3},
        )
        assert fake.last_call == (
            "LayerTree.profileSnapshot",
            {"snapshotId": "S1", "minRepeatCount": 3},
        )

    async def test_raw_send_load_snapshot(self) -> None:
        fake = FakeSender({"snapshotId": "snap1"})
        domain = LayerTreeDomain(fake)
        await domain._call(
            "LayerTree.loadSnapshot",
            {"tiles": [{"x": 0, "y": 0, "picture": "abc"}]},
        )
        assert fake.last_call == (
            "LayerTree.loadSnapshot",
            {"tiles": [{"x": 0, "y": 0, "picture": "abc"}]},
        )

    async def test_raw_send_replay_snapshot(self) -> None:
        fake = FakeSender({"dataURL": "data:..."})
        domain = LayerTreeDomain(fake)
        await domain._call(
            "LayerTree.replaySnapshot",
            {"snapshotId": "S1", "fromStep": 1, "toStep": 3, "scale": 1.5},
        )
        assert fake.last_call == (
            "LayerTree.replaySnapshot",
            {"snapshotId": "S1", "fromStep": 1, "toStep": 3, "scale": 1.5},
        )


@pytest.mark.unit
class TestLayerTreeMeta:
    def test_is_base_domain(self) -> None:
        assert issubclass(LayerTreeDomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(LayerTreeDomain, predicate=inspect.isfunction)
            if not name.startswith("_") and isinstance(obj, object)
        ]
        assert len(methods) == 9

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(LayerTreeDomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_expected_methods(self) -> None:
        expected = {
            "compositing_reasons",
            "disable",
            "enable",
            "load_snapshot",
            "make_snapshot",
            "profile_snapshot",
            "release_snapshot",
            "replay_snapshot",
            "snapshot_command_log",
        }
        actual = {
            name
            for name, obj in inspect.getmembers(LayerTreeDomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        }
        assert actual == expected

    def test_no_get_layers(self) -> None:
        assert not hasattr(LayerTreeDomain, "get_layers")

    def test_module_docstring_exists(self) -> None:
        import cdpwave.domains.layer_tree as mod
        assert mod.__doc__ is not None
        assert "experimental" in mod.__doc__.lower()

    def test_module_docstring_has_types(self) -> None:
        import cdpwave.domains.layer_tree as mod
        assert mod.__doc__ is not None
        assert "LayerId" in mod.__doc__
        assert "SnapshotId" in mod.__doc__
        assert "PaintProfile" in mod.__doc__
        assert "PictureTile" in mod.__doc__
        assert "ScrollRect" in mod.__doc__
        assert "StickyPositionConstraint" in mod.__doc__
        assert "Layer" in mod.__doc__

    def test_module_docstring_has_events(self) -> None:
        import cdpwave.domains.layer_tree as mod
        assert mod.__doc__ is not None
        assert "layerPainted" in mod.__doc__
        assert "layerTreeDidChange" in mod.__doc__

    def test_class_docstring_has_experimental(self) -> None:
        assert LayerTreeDomain.__doc__ is not None
        assert "experimental" in LayerTreeDomain.__doc__.lower()

    def test_class_docstring_has_events(self) -> None:
        assert LayerTreeDomain.__doc__ is not None
        assert "layerPainted" in LayerTreeDomain.__doc__
        assert "layerTreeDidChange" in LayerTreeDomain.__doc__

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(LayerTreeDomain, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"

    def test_all_methods_with_params_have_raises(self) -> None:
        methods_with_params = [
            "compositing_reasons",
            "load_snapshot",
            "make_snapshot",
            "profile_snapshot",
            "release_snapshot",
            "replay_snapshot",
            "snapshot_command_log",
        ]
        for name in methods_with_params:
            method = getattr(LayerTreeDomain, name)
            assert method.__doc__ is not None
            assert "Raises:" in method.__doc__, f"{name} missing Raises section"

    def test_omitempty_documented_in_profile_snapshot(self) -> None:
        method = LayerTreeDomain.profile_snapshot
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__

    def test_omitempty_documented_in_replay_snapshot(self) -> None:
        method = LayerTreeDomain.replay_snapshot
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__
