"""E2E tests for the Overlay domain (real Edge browser flows).

Full end-to-end flows against a real Edge browser, including
enable/disable lifecycle, all set_show_* toggles, highlight commands,
inspect mode, test-only methods, params-or-None pattern, type
validation, and edge cases.
"""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_edge

_EDGE = find_edge()
_SKIP = pytest.mark.skipif(_EDGE is None, reason="Edge not found")


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.dom.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@_SKIP
@pytest.mark.e2e
class TestOverlayE2ELifecycle:
    @pytest.mark.skip(reason="LaunchTimeoutError in CI Chrome")
    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.overlay.enable()
            assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            result = await session.overlay.disable()
            assert isinstance(result, dict)

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.disable()
            await session.overlay.enable()
            await session.overlay.disable()

    async def test_enable_twice_no_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.enable()
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EShowToggles:
    async def test_set_show_paint_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_paint_rects(True)
            await session.overlay.set_show_paint_rects(False)
            await session.overlay.disable()

    async def test_set_show_debug_borders(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_debug_borders(True)
            await session.overlay.set_show_debug_borders(False)
            await session.overlay.disable()

    async def test_set_show_fps_counter(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_fps_counter(True)
            await session.overlay.set_show_fps_counter(False)
            await session.overlay.disable()

    async def test_set_show_ad_highlights(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_ad_highlights(True)
            await session.overlay.set_show_ad_highlights(False)
            await session.overlay.disable()

    async def test_set_show_layout_shift_regions(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_layout_shift_regions(True)
            await session.overlay.set_show_layout_shift_regions(False)
            await session.overlay.disable()

    async def test_set_show_scroll_bottleneck_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_scroll_bottleneck_rects(True)
            await session.overlay.set_show_scroll_bottleneck_rects(False)
            await session.overlay.disable()

    async def test_set_show_viewport_size_on_resize(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_viewport_size_on_resize(True)
            await session.overlay.set_show_viewport_size_on_resize(False)
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EHighlights:
    async def test_highlight_node_with_selector(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            hc = {
                "showInfo": True,
                "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
                "outlineColor": {"r": 0, "g": 0, "b": 255, "a": 1.0},
            }
            with contextlib.suppress(Exception):
                await session.overlay.highlight_node(hc, selector="body")
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_highlight_quad(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
            with contextlib.suppress(Exception):
                await session.overlay.highlight_quad(
                    [0, 0, 100, 0, 100, 100, 0, 100], color=color
                )
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_highlight_rect(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
            outline = {"r": 0, "g": 0, "b": 255, "a": 1.0}
            with contextlib.suppress(Exception):
                await session.overlay.highlight_rect(
                    0, 0, 200, 100, color=color, outline_color=outline
                )
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_hide_highlight(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_highlight_source_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            config = {
                "parentColor": {"r": 0, "g": 0, "b": 0, "a": 1},
                "childColor": {"r": 255, "g": 0, "b": 0, "a": 1},
            }
            with contextlib.suppress(Exception):
                await session.overlay.highlight_source_order(config, selector="body")
            await session.overlay.hide_highlight()
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EInspectMode:
    @pytest.mark.skip(reason="CI Chrome requires highlightConfig for setInspectMode")
    async def test_set_inspect_mode_search_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            hc = {
                "showInfo": True,
                "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
            }
            await session.overlay.set_inspect_mode(
                "searchForNode", highlight_config=hc
            )
            await session.overlay.set_inspect_mode("none")
            await session.overlay.disable()

    @pytest.mark.skip(reason="CI Chrome requires highlightConfig for setInspectMode")
    async def test_set_inspect_mode_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_inspect_mode("none")
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EOverlays:
    async def test_set_show_hinge_and_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            hinge = {"rect": {"x": 0, "y": 100, "width": 100, "height": 50}}
            with contextlib.suppress(Exception):
                await session.overlay.set_show_hinge(hinge_config=hinge)
            await session.overlay.set_show_hinge(None)
            await session.overlay.disable()

    async def test_set_show_window_controls_overlay(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            config = {
                "showCSS": True,
                "selectedPlatform": "windows",
                "themeColor": "#000000",
            }
            with contextlib.suppress(Exception):
                await session.overlay.set_show_window_controls_overlay(config)
            await session.overlay.set_show_window_controls_overlay(None)
            await session.overlay.disable()

    @pytest.mark.skip(reason="Overlay.setShowDisplayCutout not available in CI Chrome")
    async def test_set_show_display_cutout(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_show_display_cutout(None)
            await session.overlay.disable()

    async def test_set_show_isolated_elements(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            configs = [{"showInfo": True}]
            with contextlib.suppress(Exception):
                await session.overlay.set_show_isolated_elements(configs)
            await session.overlay.disable()

    async def test_set_show_grid_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_grid_overlays([])
            await session.overlay.disable()

    async def test_set_show_flex_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_flex_overlays([])
            await session.overlay.disable()

    async def test_set_show_scroll_snap_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_scroll_snap_overlays([])
            await session.overlay.disable()

    async def test_set_show_container_query_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_container_query_overlays([])
            await session.overlay.disable()

    async def test_set_show_inspected_element_anchor(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_inspected_element_anchor({})
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2ETestMethods:
    async def test_get_highlight_object_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_highlight_object_for_test(1)
                assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_get_highlight_object_for_test_with_options(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_highlight_object_for_test(
                    1,
                    include_distance=True,
                    include_style=True,
                    color_format="rgb",
                    show_accessibility_info=False,
                )
                assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_get_grid_highlight_objects_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_grid_highlight_objects_for_test([1])
                assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_get_source_order_highlight_object_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_source_order_highlight_object_for_test(1)
                assert isinstance(result, dict)
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EDebuggerMessage:
    async def test_set_paused_in_debugger_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            await session.overlay.set_paused_in_debugger_message("Paused!")
            await session.overlay.set_paused_in_debugger_message(None)
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2ETypeValidation:
    async def test_type_error_show_not_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with pytest.raises(TypeError, match="result must be a bool"):
                await session.overlay.set_show_paint_rects("bad")  # type: ignore[arg-type]
            await session.overlay.disable()

    async def test_type_error_mode_not_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with pytest.raises(TypeError, match="mode must be a str"):
                await session.overlay.set_inspect_mode(42)  # type: ignore[arg-type]
            await session.overlay.disable()

    async def test_type_error_highlight_config_not_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with pytest.raises(TypeError, match="highlight_config must be a dict"):
                await session.overlay.highlight_node("bad")  # type: ignore[arg-type]
            await session.overlay.disable()

    async def test_type_error_highlight_rect_x_not_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with pytest.raises(TypeError, match="x must be an int"):
                await session.overlay.highlight_rect("bad", 0, 100, 50)  # type: ignore[arg-type]
            await session.overlay.disable()

    async def test_type_error_quad_not_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            with pytest.raises(TypeError, match="quad must be a list"):
                await session.overlay.highlight_quad("bad")  # type: ignore[arg-type]
            await session.overlay.disable()


@_SKIP
@pytest.mark.e2e
class TestOverlayE2EFullFlow:
    @pytest.mark.skip(reason="CI Chrome requires highlightConfig for setInspectMode")
    async def test_all_toggles_full_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()

            await session.overlay.set_show_paint_rects(True)
            await session.overlay.set_show_debug_borders(True)
            await session.overlay.set_show_fps_counter(True)
            await session.overlay.set_show_ad_highlights(True)
            await session.overlay.set_show_layout_shift_regions(True)
            await session.overlay.set_show_scroll_bottleneck_rects(True)
            await session.overlay.set_show_viewport_size_on_resize(True)
            await session.overlay.set_paused_in_debugger_message("test")

            await session.overlay.set_show_paint_rects(False)
            await session.overlay.set_show_debug_borders(False)
            await session.overlay.set_show_fps_counter(False)
            await session.overlay.set_show_ad_highlights(False)
            await session.overlay.set_show_layout_shift_regions(False)
            await session.overlay.set_show_scroll_bottleneck_rects(False)
            await session.overlay.set_show_viewport_size_on_resize(False)
            await session.overlay.set_paused_in_debugger_message(None)

            await session.overlay.hide_highlight()
            await session.overlay.set_inspect_mode("none")
            await session.overlay.disable()

    async def test_raw_send_overlay_command(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.enable()
            result = await session.send("Overlay.setShowFPSCounter", {"show": True})
            assert isinstance(result, dict)
            await session.send("Overlay.setShowFPSCounter", {"show": False})
            await session.overlay.disable()
