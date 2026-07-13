"""Unit tests for the DOMSnapshot domain.

Covers all 4 DOMSnapshot commands with FakeSender — parameter
verification, type validation, bool sending semantics (always-sent
for capture_snapshot, conditional for get_snapshot), return values,
CommandError propagation, method parity, coroutine checks,
concurrency, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.dom_snapshot import DOMSnapshotDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise CommandError(self._code, self._message)


# ---------------------------------------------------------------------------
# capture_snapshot
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCaptureSnapshot:
    async def test_method(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"])
        method, _ = fake.last_call
        assert method == "DOMSnapshot.captureSnapshot"

    async def test_required_computed_styles_always_sent(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color", "display"])
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyles"] == ["color", "display"]

    async def test_defaults_all_bools_false(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"])
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {
            "computedStyles",
            "includePaintOrder",
            "includeDOMRects",
            "includeBlendedBackgroundColors",
            "includeTextColorOpacities",
        }
        assert params["includePaintOrder"] is False
        assert params["includeDOMRects"] is False
        assert params["includeBlendedBackgroundColors"] is False
        assert params["includeTextColorOpacities"] is False

    async def test_computed_styles(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(computed_styles=["color", "display"])
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyles"] == ["color", "display"]

    async def test_include_paint_order(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_paint_order=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includePaintOrder"] is True

    async def test_include_dom_rects(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_dom_rects=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeDOMRects"] is True

    async def test_include_blended_background_colors(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_blended_background_colors=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeBlendedBackgroundColors"] is True

    async def test_include_text_color_opacities(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_text_color_opacities=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeTextColorOpacities"] is True

    async def test_all_params(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            computed_styles=["color"],
            include_paint_order=True,
            include_dom_rects=True,
            include_blended_background_colors=True,
            include_text_color_opacities=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {
            "computedStyles",
            "includePaintOrder",
            "includeDOMRects",
            "includeBlendedBackgroundColors",
            "includeTextColorOpacities",
        }

    async def test_bools_false_are_sent(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            ["color"],
            include_paint_order=False,
            include_dom_rects=False,
            include_blended_background_colors=False,
            include_text_color_opacities=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["includePaintOrder"] is False
        assert params["includeDOMRects"] is False
        assert params["includeBlendedBackgroundColors"] is False
        assert params["includeTextColorOpacities"] is False

    async def test_type_error_computed_styles(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_styles"):
            await domain.capture_snapshot("color")  # type: ignore[arg-type]

    async def test_type_error_include_paint_order(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_paint_order"):
            await domain.capture_snapshot(["color"], include_paint_order="yes")  # type: ignore[arg-type]

    async def test_type_error_include_dom_rects(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_dom_rects"):
            await domain.capture_snapshot(["color"], include_dom_rects="yes")  # type: ignore[arg-type]

    async def test_type_error_include_blended_background_colors(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_blended_background_colors"):
            await domain.capture_snapshot(["color"], include_blended_background_colors="yes")  # type: ignore[arg-type]

    async def test_type_error_include_text_color_opacities(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_text_color_opacities"):
            await domain.capture_snapshot(["color"], include_text_color_opacities="yes")  # type: ignore[arg-type]

    async def test_returns_response(self) -> None:
        resp = {"documents": [{"nodeId": 1}], "strings": ["div"]}
        fake = FakeSender(resp)
        domain = DOMSnapshotDomain(fake)
        result = await domain.capture_snapshot(["color"])
        assert result == resp


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "DOMSnapshot.disable"

    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = DOMSnapshotDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "DOMSnapshot.enable"

    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = DOMSnapshotDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}


# ---------------------------------------------------------------------------
# get_snapshot
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetSnapshot:
    async def test_method(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"])
        method, _ = fake.last_call
        assert method == "DOMSnapshot.getSnapshot"

    async def test_required_computed_style_whitelist(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color", "display"])
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyleWhitelist"] == ["color", "display"]

    async def test_include_event_listeners(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_event_listeners=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeEventListeners"] is True

    async def test_include_paint_order(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_paint_order=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includePaintOrder"] is True

    async def test_include_user_agent_shadow_tree(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_user_agent_shadow_tree=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeUserAgentShadowTree"] is True

    async def test_all_params(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(
            ["color"],
            include_event_listeners=True,
            include_paint_order=True,
            include_user_agent_shadow_tree=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {
            "computedStyleWhitelist",
            "includeEventListeners",
            "includePaintOrder",
            "includeUserAgentShadowTree",
        }

    async def test_optionals_omitted_when_none(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"])
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"computedStyleWhitelist"}

    async def test_bools_false_are_sent(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(
            ["color"],
            include_event_listeners=False,
            include_paint_order=False,
            include_user_agent_shadow_tree=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["includeEventListeners"] is False
        assert params["includePaintOrder"] is False
        assert params["includeUserAgentShadowTree"] is False

    async def test_type_error_computed_style_whitelist(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_style_whitelist"):
            await domain.get_snapshot("color")  # type: ignore[arg-type]

    async def test_type_error_include_event_listeners(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_event_listeners"):
            await domain.get_snapshot(["color"], include_event_listeners="yes")  # type: ignore[arg-type]

    async def test_type_error_include_paint_order(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_paint_order"):
            await domain.get_snapshot(["color"], include_paint_order="yes")  # type: ignore[arg-type]

    async def test_type_error_include_user_agent_shadow_tree(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_user_agent_shadow_tree"):
            await domain.get_snapshot(["color"], include_user_agent_shadow_tree="yes")  # type: ignore[arg-type]

    async def test_returns_response(self) -> None:
        resp = {"domNodes": [{"nodeId": 1}], "layoutTreeNodes": [], "computedStyles": []}
        fake = FakeSender(resp)
        domain = DOMSnapshotDomain(fake)
        result = await domain.get_snapshot(["color"])
        assert result == resp


# ---------------------------------------------------------------------------
# Method parity, signatures, and structural tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    def test_inherits_basedomain(self) -> None:
        assert issubclass(DOMSnapshotDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        methods = [
            "capture_snapshot",
            "disable",
            "enable",
            "get_snapshot",
        ]
        for name in methods:
            attr = getattr(DOMSnapshotDomain, name)
            assert inspect.iscoroutinefunction(attr), f"{name} is not a coroutine"

    def test_no_extra_methods_beyond_expected(self) -> None:
        expected = {
            "capture_snapshot",
            "disable",
            "enable",
            "get_snapshot",
        }
        actual = {
            name for name, val in inspect.getmembers(
                DOMSnapshotDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_") and not name.startswith("test")
        }
        extra = actual - expected
        missing = expected - actual
        assert actual == expected, f"Unexpected: {extra}, missing: {missing}"


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagation:
    async def test_command_error_disable(self) -> None:
        domain = DOMSnapshotDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.disable()

    async def test_command_error_enable(self) -> None:
        domain = DOMSnapshotDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.enable()

    async def test_command_error_capture_snapshot(self) -> None:
        domain = DOMSnapshotDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.capture_snapshot(["color"])

    async def test_command_error_get_snapshot(self) -> None:
        domain = DOMSnapshotDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.get_snapshot(["color"])


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_concurrent_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await asyncio.gather(domain.enable(), domain.disable())
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == "DOMSnapshot.enable"
        assert fake.calls[1][0] == "DOMSnapshot.disable"

    async def test_concurrent_capture_snapshot(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await asyncio.gather(
            domain.capture_snapshot(["color"]),
            domain.capture_snapshot(["color"]),
            domain.capture_snapshot(["color"]),
        )
        assert len(fake.calls) == 3
        for _, params in fake.calls:
            assert params is not None
            assert params["computedStyles"] == ["color"]


# ---------------------------------------------------------------------------
# Optional bool edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOptionalBoolEdgeCases:
    async def test_capture_snapshot_false_paint_order_is_sent(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_paint_order=False)
        _, params = fake.last_call
        assert params is not None
        assert params["includePaintOrder"] is False

    async def test_capture_snapshot_false_dom_rects_is_sent(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_dom_rects=False)
        _, params = fake.last_call
        assert params is not None
        assert params["includeDOMRects"] is False

    async def test_get_snapshot_false_event_listeners_is_sent(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_event_listeners=False)
        _, params = fake.last_call
        assert params is not None
        assert params["includeEventListeners"] is False

    async def test_get_snapshot_false_paint_order_is_sent(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_paint_order=False)
        _, params = fake.last_call
        assert params is not None
        assert params["includePaintOrder"] is False

    async def test_get_snapshot_false_ua_shadow_tree_is_sent(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_user_agent_shadow_tree=False)
        _, params = fake.last_call
        assert params is not None
        assert params["includeUserAgentShadowTree"] is False


# ---------------------------------------------------------------------------
# Repetition / stability
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRepetition:
    async def test_enable_disable_repeated(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10

    async def test_new_dict_each_call(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(computed_styles=["color"])
        first = fake.calls[0][1]
        await domain.capture_snapshot(computed_styles=["color"])
        second = fake.calls[1][1]
        assert first is not None
        assert second is not None
        assert first is not second


# ---------------------------------------------------------------------------
# Docstring and signature checks
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDocstrings:
    def test_module_has_docstring(self) -> None:
        import cdpwave.domains.dom_snapshot as mod
        assert mod.__doc__ is not None
        assert "DOMSnapshot" in mod.__doc__

    def test_module_docstring_mentions_experimental(self) -> None:
        import cdpwave.domains.dom_snapshot as mod
        assert mod.__doc__ is not None
        assert "Experimental" in mod.__doc__ or "experimental" in mod.__doc__

    def test_class_has_docstring(self) -> None:
        assert DOMSnapshotDomain.__doc__ is not None
        assert "DOMSnapshot" in DOMSnapshotDomain.__doc__

    def test_class_docstring_mentions_experimental(self) -> None:
        doc = DOMSnapshotDomain.__doc__ or ""
        assert "Experimental" in doc or "experimental" in doc

    @pytest.mark.parametrize("method_name", [
        "capture_snapshot",
        "disable",
        "enable",
        "get_snapshot",
    ])
    def test_method_has_docstring(self, method_name: str) -> None:
        method = getattr(DOMSnapshotDomain, method_name)
        assert method.__doc__ is not None
        assert len(method.__doc__.strip()) > 10

    def test_get_snapshot_docstring_mentions_deprecated(self) -> None:
        doc = DOMSnapshotDomain.get_snapshot.__doc__ or ""
        assert "Deprecated" in doc or "deprecated" in doc

    def test_capture_snapshot_blended_background_colors_mentions_experimental(self) -> None:
        doc = DOMSnapshotDomain.capture_snapshot.__doc__ or ""
        assert "Experimental" in doc or "experimental" in doc

    def test_capture_snapshot_text_color_opacities_mentions_experimental(self) -> None:
        doc = DOMSnapshotDomain.capture_snapshot.__doc__ or ""
        assert "Experimental" in doc or "experimental" in doc


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    async def test_capture_snapshot_empty_list_computed_styles(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(computed_styles=[])
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyles"] == []

    async def test_get_snapshot_empty_list_whitelist(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot([])
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyleWhitelist"] == []

    async def test_capture_snapshot_int_one_rejected_as_bool(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_paint_order"):
            await domain.capture_snapshot(["color"], include_paint_order=1)  # type: ignore[arg-type]

    async def test_capture_snapshot_int_zero_rejected_as_bool(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_paint_order"):
            await domain.capture_snapshot(["color"], include_paint_order=0)  # type: ignore[arg-type]

    async def test_get_snapshot_int_one_rejected_as_bool(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="include_event_listeners"):
            await domain.get_snapshot(["color"], include_event_listeners=1)  # type: ignore[arg-type]

    async def test_get_snapshot_int_rejected_as_list(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_style_whitelist"):
            await domain.get_snapshot(42)  # type: ignore[arg-type]

    async def test_get_snapshot_none_rejected_as_required(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_style_whitelist"):
            await domain.get_snapshot(None)  # type: ignore[arg-type]

    async def test_capture_snapshot_dict_rejected_as_list(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_styles"):
            await domain.capture_snapshot({"color": "red"})  # type: ignore[arg-type]

    async def test_capture_snapshot_tuple_rejected_as_list(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_styles"):
            await domain.capture_snapshot(("color", "display"))  # type: ignore[arg-type]

    async def test_capture_snapshot_none_rejected_as_required(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_styles"):
            await domain.capture_snapshot(None)  # type: ignore[arg-type]

    async def test_capture_snapshot_int_rejected_as_list(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        with pytest.raises(TypeError, match="computed_styles"):
            await domain.capture_snapshot(42)  # type: ignore[arg-type]

    async def test_capture_snapshot_large_styles_list(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        styles = [f"style-{i}" for i in range(100)]
        await domain.capture_snapshot(computed_styles=styles)
        _, params = fake.last_call
        assert params is not None
        assert params["computedStyles"] == styles
        assert len(params["computedStyles"]) == 100

    async def test_capture_snapshot_bool_overrides_default(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(["color"], include_dom_rects=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeDOMRects"] is True
        assert params["includePaintOrder"] is False
        assert params["includeBlendedBackgroundColors"] is False
        assert params["includeTextColorOpacities"] is False

    async def test_get_snapshot_single_optional_sent(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(["color"], include_user_agent_shadow_tree=True)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"computedStyleWhitelist", "includeUserAgentShadowTree"}


# ---------------------------------------------------------------------------
# CamelCase verification
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCamelCase:
    async def test_capture_snapshot_camelcase_keys(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            computed_styles=["color"],
            include_paint_order=True,
            include_dom_rects=True,
            include_blended_background_colors=True,
            include_text_color_opacities=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert "computedStyles" in params
        assert "includePaintOrder" in params
        assert "includeDOMRects" in params
        assert "includeBlendedBackgroundColors" in params
        assert "includeTextColorOpacities" in params

    async def test_get_snapshot_camelcase_keys(self) -> None:
        fake = FakeSender({"domNodes": [], "layoutTreeNodes": [], "computedStyles": []})
        domain = DOMSnapshotDomain(fake)
        await domain.get_snapshot(
            ["color"],
            include_event_listeners=True,
            include_paint_order=True,
            include_user_agent_shadow_tree=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert "computedStyleWhitelist" in params
        assert "includeEventListeners" in params
        assert "includePaintOrder" in params
        assert "includeUserAgentShadowTree" in params

    async def test_no_snake_case_keys_leaked(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            computed_styles=["color"],
            include_paint_order=True,
            include_dom_rects=True,
            include_blended_background_colors=True,
            include_text_color_opacities=True,
        )
        _, params = fake.last_call
        assert params is not None
        for key in params:
            assert "_" not in key, f"snake_case key leaked: {key}"


# ---------------------------------------------------------------------------
# Alphabetical method ordering
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAlphabeticalOrder:
    def test_methods_alphabetically_ordered(self) -> None:
        methods = [
            name for name, _ in inspect.getmembers(
                DOMSnapshotDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert methods == sorted(methods), f"Methods not alphabetically ordered: {methods}"
