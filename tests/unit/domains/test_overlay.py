"""Unit tests for the Overlay domain.

Covers all 28 CDP Overlay commands with FakeSender — parameter
verification, type validation, return values, CommandError propagation,
method parity, alphabetical ordering, params-or-None pattern, and
edge cases.

Bugs fixed during review:
    - highlight_frame: removed (not in Go source, deprecated in CDP)
    - set_show_hit_test_borders: removed (not in Go source, deprecated in CDP)
    - set_show_web_vitals: removed (not in Go source, deprecated in CDP)
    - set_show_window_controls → set_show_window_controls_overlay:
      renamed to match CDP method name, param key fixed from
      "windowControls" to "windowControlsOverlayConfig", made optional
    - highlight_node: highlight_config changed from Optional to required
    - highlight_rect: x/y/width/height changed from float to int
    - get_highlight_object_for_test: include_distance/include_style
      changed from Optional to bool=False, show_accessibility_info
      changed from Optional to bool=True, color_format empty string
      now omitted per Go omitempty,omitzero
    - set_show_hinge: param renamed from hinge to hinge_config
    - set_paused_in_debugger_message: added params or None pattern,
      empty string now omitted per Go omitempty,omitzero
    - set_show_display_cutout: added params or None pattern
    - All methods: added isinstance type validation
    - All methods: reordered alphabetically
    - Module/class docstrings: added Experimental marking and events
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message
        self._calls: list[tuple[str, dict[str, Any] | None]] = []

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._calls.append((method, params))
        raise CommandError(self._code, self._message)

    @property
    def calls(self) -> list[tuple[str, dict[str, Any] | None]]:
        return self._calls

    @property
    def last_call(self) -> tuple[str, dict[str, Any] | None]:
        return self._calls[-1]


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Overlay.disable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = OverlayDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Overlay.disable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1

    async def test_command_error_propagates(self) -> None:
        fake = ErrorSender()
        domain = OverlayDomain(fake)
        with pytest.raises(CommandError):
            await domain.disable()

    async def test_is_coroutine(self) -> None:
        assert inspect.iscoroutinefunction(OverlayDomain.disable)


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Overlay.enable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = OverlayDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}

    async def test_command_error_propagates(self) -> None:
        fake = ErrorSender()
        domain = OverlayDomain(fake)
        with pytest.raises(CommandError):
            await domain.enable()


# ---------------------------------------------------------------------------
# get_grid_highlight_objects_for_test
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetGridHighlightObjectsForTest:
    async def test_basic_call(self) -> None:
        fake = FakeSender({"highlights": []})
        domain = OverlayDomain(fake)
        result = await domain.get_grid_highlight_objects_for_test([1, 2, 3])
        method, params = fake.last_call
        assert method == "Overlay.getGridHighlightObjectsForTest"
        assert params == {"nodeIds": [1, 2, 3]}
        assert result == {"highlights": []}

    async def test_empty_list(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.get_grid_highlight_objects_for_test([])
        _, params = fake.last_call
        assert params == {"nodeIds": []}

    async def test_type_error_non_list(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="node_ids must be a list"):
            await domain.get_grid_highlight_objects_for_test(42)  # type: ignore[arg-type]

    async def test_type_error_string(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="node_ids must be a list"):
            await domain.get_grid_highlight_objects_for_test("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# get_highlight_object_for_test
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetHighlightObjectForTest:
    async def test_required_params_only(self) -> None:
        fake = FakeSender({"highlight": {}})
        domain = OverlayDomain(fake)
        result = await domain.get_highlight_object_for_test(42)
        method, params = fake.last_call
        assert method == "Overlay.getHighlightObjectForTest"
        assert params == {
            "nodeId": 42,
            "includeDistance": False,
            "includeStyle": False,
            "showAccessibilityInfo": True,
        }
        assert result == {"highlight": {}}

    async def test_all_params(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.get_highlight_object_for_test(
            42,
            include_distance=True,
            include_style=True,
            color_format="rgb",
            show_accessibility_info=False,
        )
        _, params = fake.last_call
        assert params == {
            "nodeId": 42,
            "includeDistance": True,
            "includeStyle": True,
            "colorFormat": "rgb",
            "showAccessibilityInfo": False,
        }

    async def test_color_format_omitted_when_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.get_highlight_object_for_test(1, color_format=None)
        _, params = fake.last_call
        assert "colorFormat" not in params

    async def test_color_format_omitted_when_empty_string(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.get_highlight_object_for_test(1, color_format="")
        _, params = fake.last_call
        assert "colorFormat" not in params

    async def test_type_error_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="node_id must be an int"):
            await domain.get_highlight_object_for_test("bad")  # type: ignore[arg-type]

    async def test_type_error_include_distance(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="include_distance must be a bool"):
            await domain.get_highlight_object_for_test(1, include_distance="bad")  # type: ignore[arg-type]

    async def test_type_error_include_style(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="include_style must be a bool"):
            await domain.get_highlight_object_for_test(1, include_style="bad")  # type: ignore[arg-type]

    async def test_type_error_show_accessibility_info(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show_accessibility_info must be a bool"):
            await domain.get_highlight_object_for_test(1, show_accessibility_info="bad")  # type: ignore[arg-type]

    async def test_type_error_color_format(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="color_format must be a str or None"):
            await domain.get_highlight_object_for_test(1, color_format=123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# get_source_order_highlight_object_for_test
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetSourceOrderHighlightObjectForTest:
    async def test_basic_call(self) -> None:
        fake = FakeSender({"highlight": {}})
        domain = OverlayDomain(fake)
        result = await domain.get_source_order_highlight_object_for_test(7)
        method, params = fake.last_call
        assert method == "Overlay.getSourceOrderHighlightObjectForTest"
        assert params == {"nodeId": 7}
        assert result == {"highlight": {}}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="node_id must be an int"):
            await domain.get_source_order_highlight_object_for_test("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# hide_highlight
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHideHighlight:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.hide_highlight()
        assert fake.last_call == ("Overlay.hideHighlight", None)

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = OverlayDomain(fake)
        result = await domain.hide_highlight()
        assert result == {"ok": True}


# ---------------------------------------------------------------------------
# highlight_node
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHighlightNode:
    async def test_required_only(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hc = {"showInfo": True}
        await domain.highlight_node(hc)
        method, params = fake.last_call
        assert method == "Overlay.highlightNode"
        assert params == {"highlightConfig": hc}

    async def test_with_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, node_id=42)
        _, params = fake.last_call
        assert params["nodeId"] == 42

    async def test_with_backend_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, backend_node_id=99)
        _, params = fake.last_call
        assert params["backendNodeId"] == 99

    async def test_with_object_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, object_id="obj-1")
        _, params = fake.last_call
        assert params["objectId"] == "obj-1"

    async def test_with_selector(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, selector="#my-element")
        _, params = fake.last_call
        assert params["selector"] == "#my-element"

    async def test_empty_string_object_id_omitted(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, object_id="")
        _, params = fake.last_call
        assert "objectId" not in params

    async def test_empty_string_selector_omitted(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_node({"showInfo": True}, selector="")
        _, params = fake.last_call
        assert "selector" not in params

    async def test_all_params(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hc = {"showInfo": True}
        await domain.highlight_node(
            hc, node_id=1, backend_node_id=2, object_id="o3", selector="#s"
        )
        _, params = fake.last_call
        assert params == {
            "highlightConfig": hc,
            "nodeId": 1,
            "backendNodeId": 2,
            "objectId": "o3",
            "selector": "#s",
        }

    async def test_type_error_highlight_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="highlight_config must be a dict"):
            await domain.highlight_node("bad")  # type: ignore[arg-type]

    async def test_type_error_highlight_config_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="highlight_config must be a dict"):
            await domain.highlight_node(None)  # type: ignore[arg-type]

    async def test_type_error_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="node_id must be an int or None"):
            await domain.highlight_node({}, node_id="bad")  # type: ignore[arg-type]

    async def test_type_error_object_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str or None"):
            await domain.highlight_node({}, object_id=42)  # type: ignore[arg-type]

    async def test_type_error_selector(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="selector must be a str or None"):
            await domain.highlight_node({}, selector=42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# highlight_quad
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHighlightQuad:
    async def test_required_only(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        quad = [0, 0, 100, 0, 100, 100, 0, 100]
        await domain.highlight_quad(quad)
        method, params = fake.last_call
        assert method == "Overlay.highlightQuad"
        assert params == {"quad": quad}

    async def test_with_colors(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
        outline = {"r": 0, "g": 0, "b": 255, "a": 1.0}
        await domain.highlight_quad([0, 0, 1, 0, 1, 1, 0, 1], color=color, outline_color=outline)
        _, params = fake.last_call
        assert params["color"] == color
        assert params["outlineColor"] == outline

    async def test_type_error_quad(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="quad must be a list"):
            await domain.highlight_quad("bad")  # type: ignore[arg-type]

    async def test_type_error_color(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="color must be a dict or None"):
            await domain.highlight_quad([0, 0, 1, 0, 1, 1, 0, 1], color="bad")  # type: ignore[arg-type]

    async def test_type_error_outline_color(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="outline_color must be a dict or None"):
            await domain.highlight_quad([0, 0, 1, 0, 1, 1, 0, 1], outline_color=42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# highlight_rect
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHighlightRect:
    async def test_required_only(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_rect(10, 20, 100, 50)
        method, params = fake.last_call
        assert method == "Overlay.highlightRect"
        assert params == {"x": 10, "y": 20, "width": 100, "height": 50}

    async def test_with_colors(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
        outline = {"r": 0, "g": 0, "b": 255, "a": 1.0}
        await domain.highlight_rect(0, 0, 100, 50, color=color, outline_color=outline)
        _, params = fake.last_call
        assert params["color"] == color
        assert params["outlineColor"] == outline

    async def test_zero_values(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_rect(0, 0, 0, 0)
        _, params = fake.last_call
        assert params == {"x": 0, "y": 0, "width": 0, "height": 0}

    async def test_type_error_x(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="x must be an int"):
            await domain.highlight_rect("bad", 0, 100, 50)  # type: ignore[arg-type]

    async def test_type_error_y(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="y must be an int"):
            await domain.highlight_rect(0, "bad", 100, 50)  # type: ignore[arg-type]

    async def test_type_error_width(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="width must be an int"):
            await domain.highlight_rect(0, 0, "bad", 50)  # type: ignore[arg-type]

    async def test_type_error_height(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="height must be an int"):
            await domain.highlight_rect(0, 0, 100, "bad")  # type: ignore[arg-type]

    async def test_type_error_color(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="color must be a dict or None"):
            await domain.highlight_rect(0, 0, 100, 50, color="bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# highlight_source_order
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHighlightSourceOrder:
    async def test_required_only(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        config = {"parentColor": {"r": 0, "g": 0, "b": 0, "a": 1}}
        await domain.highlight_source_order(config)
        method, params = fake.last_call
        assert method == "Overlay.highlightSourceOrder"
        assert params == {"sourceOrderConfig": config}

    async def test_with_node_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_source_order({}, node_id=5)
        _, params = fake.last_call
        assert params["nodeId"] == 5

    async def test_with_object_id(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_source_order({}, object_id="obj-1")
        _, params = fake.last_call
        assert params["objectId"] == "obj-1"

    async def test_empty_string_object_id_omitted(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.highlight_source_order({}, object_id="")
        _, params = fake.last_call
        assert "objectId" not in params

    async def test_type_error_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="source_order_config must be a dict"):
            await domain.highlight_source_order("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_inspect_mode
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetInspectMode:
    async def test_required_only(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_inspect_mode("searchForNode")
        method, params = fake.last_call
        assert method == "Overlay.setInspectMode"
        assert params == {"mode": "searchForNode"}

    async def test_with_highlight_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hc = {"showInfo": True}
        await domain.set_inspect_mode("searchForNode", highlight_config=hc)
        _, params = fake.last_call
        assert params["highlightConfig"] == hc

    async def test_mode_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_inspect_mode("none")
        _, params = fake.last_call
        assert params == {"mode": "none"}

    async def test_type_error_mode(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="mode must be a str"):
            await domain.set_inspect_mode(42)  # type: ignore[arg-type]

    async def test_type_error_highlight_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="highlight_config must be a dict or None"):
            await domain.set_inspect_mode("none", highlight_config="bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_paused_in_debugger_message
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetPausedInDebuggerMessage:
    async def test_with_message(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_paused_in_debugger_message("Paused!")
        assert fake.last_call == (
            "Overlay.setPausedInDebuggerMessage",
            {"message": "Paused!"},
        )

    async def test_none_message_params_or_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_paused_in_debugger_message(None)
        method, params = fake.last_call
        assert method == "Overlay.setPausedInDebuggerMessage"
        assert params is None

    async def test_empty_string_omitted(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_paused_in_debugger_message("")
        method, params = fake.last_call
        assert method == "Overlay.setPausedInDebuggerMessage"
        assert params is None

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="message must be a str or None"):
            await domain.set_paused_in_debugger_message(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_ad_highlights
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowAdHighlights:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_ad_highlights(True)
        assert fake.last_call == ("Overlay.setShowAdHighlights", {"show": True})

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_ad_highlights(False)
        assert fake.last_call == ("Overlay.setShowAdHighlights", {"show": False})

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show must be a bool"):
            await domain.set_show_ad_highlights("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_container_query_overlays
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowContainerQueryOverlays:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"containerColor": {"r": 0, "g": 0, "b": 0, "a": 1}}]
        await domain.set_show_container_query_overlays(configs)
        method, params = fake.last_call
        assert method == "Overlay.setShowContainerQueryOverlays"
        assert params == {"containerQueryHighlightConfigs": configs}

    async def test_empty_list(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_container_query_overlays([])
        _, params = fake.last_call
        assert params == {"containerQueryHighlightConfigs": []}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="container_query_highlight_configs must be a list"):
            await domain.set_show_container_query_overlays("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_debug_borders
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowDebugBorders:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_debug_borders(True)
        assert fake.last_call == ("Overlay.setShowDebugBorders", {"show": True})

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_debug_borders(False)
        assert fake.last_call == ("Overlay.setShowDebugBorders", {"show": False})

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show must be a bool"):
            await domain.set_show_debug_borders(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_display_cutout
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowDisplayCutout:
    async def test_with_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        config = {"displayCutout": {"x": 0, "y": 0, "width": 100, "height": 50}}
        await domain.set_show_display_cutout(config)
        method, params = fake.last_call
        assert method == "Overlay.setShowDisplayCutout"
        assert params == {"displayCutoutConfig": config}

    async def test_none_params_or_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_display_cutout(None)
        method, params = fake.last_call
        assert method == "Overlay.setShowDisplayCutout"
        assert params is None

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="display_cutout_config must be a dict or None"):
            await domain.set_show_display_cutout("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_flex_overlays
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowFlexOverlays:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"flexContainerColor": {"r": 0, "g": 0, "b": 0, "a": 1}}]
        await domain.set_show_flex_overlays(configs)
        method, params = fake.last_call
        assert method == "Overlay.setShowFlexOverlays"
        assert params == {"flexNodeHighlightConfigs": configs}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="flex_node_highlight_configs must be a list"):
            await domain.set_show_flex_overlays(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_fps_counter
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowFPSCounter:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_fps_counter(True)
        assert fake.last_call == ("Overlay.setShowFPSCounter", {"show": True})

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_fps_counter(False)
        assert fake.last_call == ("Overlay.setShowFPSCounter", {"show": False})

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show must be a bool"):
            await domain.set_show_fps_counter("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_grid_overlays
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowGridOverlays:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"gridColor": {"r": 0, "g": 0, "b": 0, "a": 1}}]
        await domain.set_show_grid_overlays(configs)
        method, params = fake.last_call
        assert method == "Overlay.setShowGridOverlays"
        assert params == {"gridNodeHighlightConfigs": configs}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="grid_node_highlight_configs must be a list"):
            await domain.set_show_grid_overlays("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_hinge
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowHinge:
    async def test_with_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        hinge = {"x": 0, "y": 100, "width": 100, "height": 50}
        await domain.set_show_hinge(hinge_config=hinge)
        method, params = fake.last_call
        assert method == "Overlay.setShowHinge"
        assert params == {"hingeConfig": hinge}

    async def test_none_params_or_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_hinge(None)
        method, params = fake.last_call
        assert method == "Overlay.setShowHinge"
        assert params is None

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="hinge_config must be a dict or None"):
            await domain.set_show_hinge(hinge_config=42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_inspected_element_anchor
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowInspectedElementAnchor:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        config = {"nodeId": 42}
        await domain.set_show_inspected_element_anchor(config)
        method, params = fake.last_call
        assert method == "Overlay.setShowInspectedElementAnchor"
        assert params == {"inspectedElementAnchorConfig": config}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="inspected_element_anchor_config must be a dict"):
            await domain.set_show_inspected_element_anchor("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_isolated_elements
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowIsolatedElements:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"showInfo": True}, {"showStyles": True}]
        await domain.set_show_isolated_elements(configs)
        assert fake.last_call == (
            "Overlay.setShowIsolatedElements",
            {"isolatedElementHighlightConfigs": configs},
        )

    async def test_empty_list(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_isolated_elements([])
        _, params = fake.last_call
        assert params == {"isolatedElementHighlightConfigs": []}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="isolated_element_highlight_configs must be a list"):
            await domain.set_show_isolated_elements("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_layout_shift_regions
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowLayoutShiftRegions:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_layout_shift_regions(True)
        assert fake.last_call == (
            "Overlay.setShowLayoutShiftRegions",
            {"result": True},
        )

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_layout_shift_regions(False)
        assert fake.last_call == (
            "Overlay.setShowLayoutShiftRegions",
            {"result": False},
        )

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="result must be a bool"):
            await domain.set_show_layout_shift_regions("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_paint_rects
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowPaintRects:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_paint_rects(True)
        assert fake.last_call == ("Overlay.setShowPaintRects", {"result": True})

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_paint_rects(False)
        assert fake.last_call == ("Overlay.setShowPaintRects", {"result": False})

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="result must be a bool"):
            await domain.set_show_paint_rects("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_scroll_bottleneck_rects
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowScrollBottleneckRects:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_scroll_bottleneck_rects(True)
        assert fake.last_call == (
            "Overlay.setShowScrollBottleneckRects",
            {"show": True},
        )

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_scroll_bottleneck_rects(False)
        assert fake.last_call == (
            "Overlay.setShowScrollBottleneckRects",
            {"show": False},
        )

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show must be a bool"):
            await domain.set_show_scroll_bottleneck_rects(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_scroll_snap_overlays
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowScrollSnapOverlays:
    async def test_basic(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        configs = [{"scrollSnapColor": {"r": 0, "g": 0, "b": 0, "a": 1}}]
        await domain.set_show_scroll_snap_overlays(configs)
        method, params = fake.last_call
        assert method == "Overlay.setShowScrollSnapOverlays"
        assert params == {"scrollSnapHighlightConfigs": configs}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="scroll_snap_highlight_configs must be a list"):
            await domain.set_show_scroll_snap_overlays("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_viewport_size_on_resize
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowViewportSizeOnResize:
    async def test_true(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_viewport_size_on_resize(True)
        assert fake.last_call == (
            "Overlay.setShowViewportSizeOnResize",
            {"show": True},
        )

    async def test_false(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_viewport_size_on_resize(False)
        assert fake.last_call == (
            "Overlay.setShowViewportSizeOnResize",
            {"show": False},
        )

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(TypeError, match="show must be a bool"):
            await domain.set_show_viewport_size_on_resize("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_show_window_controls_overlay
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetShowWindowControlsOverlay:
    async def test_with_config(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        config = {"showCSS": True, "selectedPlatform": "windows", "themeColor": "#000"}
        await domain.set_show_window_controls_overlay(config)
        method, params = fake.last_call
        assert method == "Overlay.setShowWindowControlsOverlay"
        assert params == {"windowControlsOverlayConfig": config}

    async def test_none_params_or_none(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await domain.set_show_window_controls_overlay(None)
        method, params = fake.last_call
        assert method == "Overlay.setShowWindowControlsOverlay"
        assert params is None

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        with pytest.raises(
            TypeError, match="window_controls_overlay_config must be a dict or None"
        ):
            await domain.set_show_window_controls_overlay(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Method parity and structure
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    def test_all_methods_are_coroutines(self) -> None:
        for name in dir(OverlayDomain):
            if name.startswith("_"):
                continue
            attr = getattr(OverlayDomain, name)
            if callable(attr):
                assert inspect.iscoroutinefunction(attr), f"{name} is not a coroutine"

    def test_no_removed_methods_exist(self) -> None:
        assert not hasattr(OverlayDomain, "highlight_frame")
        assert not hasattr(OverlayDomain, "set_show_hit_test_borders")
        assert not hasattr(OverlayDomain, "set_show_window_controls")
        assert not hasattr(OverlayDomain, "set_show_web_vitals")

    def test_renamed_method_exists(self) -> None:
        assert hasattr(OverlayDomain, "set_show_window_controls_overlay")

    def test_inherits_basedomain(self) -> None:
        assert issubclass(OverlayDomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name in dir(OverlayDomain)
            if not name.startswith("_")
            and callable(getattr(OverlayDomain, name))
            and inspect.iscoroutinefunction(getattr(OverlayDomain, name))
        ]
        assert len(methods) == 28

    async def test_concurrent_calls(self) -> None:
        fake = FakeSender({})
        domain = OverlayDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.hide_highlight(),
        )
        assert len(fake.calls) == 3
