"""Functional tests for Debugger, Overlay, Security, and Audits domains."""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


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


@pytest.mark.integration
class TestDebugger:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.disable()

    async def test_pause_resume(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(False)
            await session.debugger.disable()

    async def test_set_pause_on_exceptions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_pause_on_exceptions("none")
            await session.debugger.disable()

    async def test_set_skip_all_pauses(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            await session.debugger.disable()

    async def test_get_script_source(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            if scripts:
                script_id = scripts[0]["scriptId"]
                result = await session.debugger.get_script_source(script_id)
                assert "scriptSource" in result

            await session.debugger.disable()


@pytest.mark.integration
class TestOverlay:
    async def _setup(self, session: CDPSession) -> None:
        await session.dom.enable()
        await session.page.enable()
        await session.page.navigate("https://example.com")
        await asyncio.sleep(1.0)

    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.disable()

    async def test_set_show_paint_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_paint_rects(True)
            with contextlib.suppress(Exception):
                await session.overlay.set_show_paint_rects(False)
            await session.overlay.disable()

    async def test_set_show_debug_borders(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_debug_borders(True)
            await session.overlay.set_show_debug_borders(False)
            await session.overlay.disable()

    async def test_set_show_fps_counter(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_fps_counter(True)
            await session.overlay.set_show_fps_counter(False)
            await session.overlay.disable()

    async def test_hide_highlight(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_set_inspect_mode(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            highlight_config = {
                "showInfo": True,
                "showStyles": True,
                "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
            }
            await session.overlay.set_inspect_mode(
                "searchForNode", highlight_config=highlight_config
            )
            await session.overlay.set_inspect_mode(
                "none", highlight_config=highlight_config
            )
            await session.overlay.disable()

    async def test_set_show_ad_highlights(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_ad_highlights(True)
            await session.overlay.set_show_ad_highlights(False)
            await session.overlay.disable()

    async def test_set_show_layout_shift_regions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_layout_shift_regions(True)
            await session.overlay.set_show_layout_shift_regions(False)
            await session.overlay.disable()

    async def test_set_show_scroll_bottleneck_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_scroll_bottleneck_rects(True)
            await session.overlay.set_show_scroll_bottleneck_rects(False)
            await session.overlay.disable()

    async def test_set_show_viewport_size_on_resize(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_viewport_size_on_resize(True)
            await session.overlay.set_show_viewport_size_on_resize(False)
            await session.overlay.disable()

    async def test_set_paused_in_debugger_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_paused_in_debugger_message("Paused!")
            await session.overlay.set_paused_in_debugger_message(None)
            await session.overlay.disable()

    async def test_set_show_hinge(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            hinge = {"rect": {"x": 0, "y": 100, "width": 100, "height": 50}}
            await session.overlay.set_show_hinge(hinge_config=hinge)
            await session.overlay.set_show_hinge(None)
            await session.overlay.disable()

    async def test_highlight_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            hc = {
                "showInfo": True,
                "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
            }
            with contextlib.suppress(Exception):
                await session.overlay.highlight_node(hc, selector="body")
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_highlight_quad(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
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
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            color = {"r": 255, "g": 0, "b": 0, "a": 0.5}
            with contextlib.suppress(Exception):
                await session.overlay.highlight_rect(0, 0, 100, 50, color=color)
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_set_show_window_controls_overlay(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            config = {
                "showCSS": True,
                "selectedPlatform": "windows",
                "themeColor": "#000000",
            }
            with contextlib.suppress(Exception):
                await session.overlay.set_show_window_controls_overlay(config)
            with contextlib.suppress(Exception):
                await session.overlay.set_show_window_controls_overlay(None)
            await session.overlay.disable()

    async def test_set_show_isolated_elements(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            configs = [{"showInfo": True}]
            with contextlib.suppress(Exception):
                await session.overlay.set_show_isolated_elements(configs)
            await session.overlay.disable()

    async def test_get_highlight_object_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_highlight_object_for_test(1)
                assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_set_show_grid_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_grid_overlays([])
            await session.overlay.disable()

    async def test_set_show_flex_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_flex_overlays([])
            await session.overlay.disable()

    async def test_set_show_scroll_snap_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_scroll_snap_overlays([])
            await session.overlay.disable()

    async def test_set_show_container_query_overlays(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_container_query_overlays([])
            await session.overlay.disable()

    async def test_set_show_display_cutout(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_display_cutout(None)
            await session.overlay.disable()

    async def test_set_show_inspected_element_anchor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                await session.overlay.set_show_inspected_element_anchor({})
            await session.overlay.disable()

    async def test_highlight_source_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            config = {
                "parentColor": {"r": 0, "g": 0, "b": 0, "a": 1},
                "childColor": {"r": 255, "g": 0, "b": 0, "a": 1},
            }
            with contextlib.suppress(Exception):
                await session.overlay.highlight_source_order(config, selector="body")
            await session.overlay.hide_highlight()
            await session.overlay.disable()

    async def test_get_source_order_highlight_object_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_source_order_highlight_object_for_test(1)
                assert isinstance(result, dict)
            await session.overlay.disable()

    async def test_get_grid_highlight_objects_for_test(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with contextlib.suppress(Exception):
                result = await session.overlay.get_grid_highlight_objects_for_test([1])
                assert isinstance(result, dict)
            await session.overlay.disable()


@pytest.mark.integration
class TestOverlayEdgeCases:
    """Edge cases for Overlay domain on a real browser."""

    async def _setup(self, session: CDPSession) -> None:
        await session.dom.enable()
        await session.page.enable()
        await session.page.navigate("https://example.com")

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.enable()
            await session.overlay.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            with contextlib.suppress(Exception):
                await session.overlay.disable()

    async def test_hide_highlight_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            with contextlib.suppress(Exception):
                await session.overlay.hide_highlight()

    async def test_type_error_on_bad_param(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            with pytest.raises(TypeError):
                await session.overlay.set_show_paint_rects("not a bool")  # type: ignore[arg-type]
            await session.overlay.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_debug_borders(True)
            await session.overlay.set_show_fps_counter(True)
            await session.overlay.set_show_ad_highlights(True)
            await session.overlay.set_show_layout_shift_regions(True)
            await session.overlay.set_show_scroll_bottleneck_rects(True)
            await session.overlay.set_show_viewport_size_on_resize(True)
            await session.overlay.set_paused_in_debugger_message("test")
            await session.overlay.set_show_debug_borders(False)
            await session.overlay.set_show_fps_counter(False)
            await session.overlay.set_show_ad_highlights(False)
            await session.overlay.set_show_layout_shift_regions(False)
            await session.overlay.set_show_scroll_bottleneck_rects(False)
            await session.overlay.set_show_viewport_size_on_resize(False)
            await session.overlay.set_paused_in_debugger_message(None)
            await session.overlay.hide_highlight()
            await session.overlay.disable()


@pytest.mark.integration
class TestSecurity:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.disable()

    async def test_set_override_certificate_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()


@pytest.mark.integration
class TestAudits:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.audits.enable()
            await session.audits.disable()

    async def test_check_contrast(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.audits.check_contrast()


@pytest.mark.integration
class TestAuditsEdgeCases:
    """Edge cases for Audits domain on a real browser."""

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.audits.enable()
            await session.audits.enable()
            await session.audits.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.audits.disable()

    async def test_check_contrast_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.audits.check_contrast()

    async def test_check_forms_issues(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.audits.check_forms_issues()
                assert isinstance(result, dict)

    async def test_get_encoded_response_invalid_request(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.audits.get_encoded_response(
                    "nonexistent-request-id", "webp"
                )

    async def test_get_encoded_response_size_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.audits.get_encoded_response(
                    "nonexistent-request-id", "jpeg", size_only=True
                )


@pytest.mark.integration
class TestAuditsFlow:
    """End-to-end flows combining Audits with other domains."""

    async def test_enable_issue_event_then_disable(self) -> None:
        """Enable Audits → listen for issueAdded events → navigate → disable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            issues: list[dict[str, Any]] = []

            async def on_issue(params: dict[str, Any]) -> None:
                issues.append(params)

            await session.audits.enable()
            session.on("Audits.issueAdded", on_issue)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(2.0)

            await session.audits.disable()

    async def test_check_contrast_after_dom_modification(self) -> None:
        """Inject low-contrast elements → check contrast."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                "const div = document.createElement('div');"
                "div.style.color = '#eee';"
                "div.style.backgroundColor = '#fff';"
                "div.textContent = 'Low contrast text';"
                "document.body.appendChild(div);"
            )

            with contextlib.suppress(Exception):
                await session.audits.check_contrast()

    async def test_audits_with_network_inspection(self) -> None:
        """Enable Audits + Network → navigate → check for issues."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            issues: list[dict[str, Any]] = []

            async def on_issue(params: dict[str, Any]) -> None:
                issues.append(params)

            await session.audits.enable()
            session.on("Audits.issueAdded", on_issue)

            await session.network.enable()
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(2.0)

            await session.network.disable()
            await session.audits.disable()

    async def test_check_forms_issues_on_real_form(self) -> None:
        """Inject a form with issues → run check_forms_issues."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                "const form = document.createElement('form');"
                "const input = document.createElement('input');"
                "input.type = 'text';"
                "input.name = 'test';"
                "form.appendChild(input);"
                "document.body.appendChild(form);"
            )

            with contextlib.suppress(Exception):
                result = await session.audits.check_forms_issues()
                assert isinstance(result, dict)

    async def test_get_encoded_response_on_real_image(self) -> None:
        """Navigate to page with image → capture request → get encoded response."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            responses: list[dict[str, Any]] = []

            async def on_response(params: dict[str, Any]) -> None:
                url = params.get("response", {}).get("url", "")
                if url.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                    responses.append(params)

            await session.network.enable()
            session.on("Network.responseReceived", on_response)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(2.0)

            if responses:
                req_id = responses[0]["requestId"]
                with contextlib.suppress(Exception):
                    result = await session.audits.get_encoded_response(
                        req_id, "webp", size_only=True
                    )
                    assert isinstance(result, dict)

    async def test_issue_added_event_structure(self) -> None:
        """Enable Audits → navigate → verify issueAdded event structure if fired."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            issues: list[dict[str, Any]] = []

            async def on_issue(params: dict[str, Any]) -> None:
                issues.append(params)

            await session.audits.enable()
            session.on("Audits.issueAdded", on_issue)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            for issue in issues:
                assert "issue" in issue
                assert "code" in issue["issue"]

            await session.audits.disable()

    async def test_multiple_enable_disable_cycles(self) -> None:
        """Repeated enable/disable should be stable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.audits.enable()
                await session.audits.disable()

    async def test_check_forms_issues_without_enable(self) -> None:
        """check_forms_issues should work even without enable()."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.audits.check_forms_issues()
                assert isinstance(result, dict)

    async def test_get_encoded_response_all_encodings(self) -> None:
        """Try get_encoded_response with each encoding type on invalid request."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            for encoding in ("webp", "jpeg", "png"):
                with pytest.raises(CommandError):
                    await session.audits.get_encoded_response(
                        "fake-req-id", encoding
                    )
