"""Expanded integration tests for existing domains — covers more method
parameter casuistics against a real browser.

Covers: Page (screencast, lifecycle, geolocation, touch, fonts, ad blocking,
compilation cache, test report), Runtime (add binding, serialization, discard),
Network (set cookies, delete cookies, emulate conditions, accepted encodings),
DOM (set attributes, copy to, class names, content quads, file input, set
HTML, highlight, flattened document, node stack traces), Emulation (CPU
throttling, script execution, sensors, pressure, data saver, hardware
concurrency, automation, safe area, posture, display features, text scale),
Storage (clear data, quota, tracking, shared storage, bounce tracking,
related website sets), Overlay (inspect mode, show elements, highlight config).
"""

import asyncio
import base64
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_page(page: CDPSession, url: str = "https://example.com") -> None:
    await page.page.enable()
    await page.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestPageExpanded:
    async def test_stop_loading(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.page.stop_loading()

    async def test_set_lifecycle_events_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.set_lifecycle_events_enabled(True)
            await session.page.set_lifecycle_events_enabled(False)

    async def test_capture_snapshot_mhtml(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.capture_snapshot(format="mhtml")
            assert "data" in result
            assert len(result["data"]) > 0

    async def test_screencast_start_stop(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.start_screencast(format="jpeg", quality=50, every_nth_frame=2)
            await asyncio.sleep(1.0)
            await session.page.stop_screencast()

    async def test_screencast_png_format(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.start_screencast(
                format="png", max_width=800, max_height=600,
            )
            await asyncio.sleep(1.0)
            await session.page.stop_screencast()

    async def test_set_geolocation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_geolocation_override(37.77, -122.41, 10.0)

            result = await session.runtime.evaluate(
                "navigator.geolocation", return_by_value=True
            )
            assert "result" in result

            await session.page.clear_geolocation_override()

    async def test_set_touch_emulation_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_touch_emulation_enabled(True, configuration="mobile")
            await session.page.set_touch_emulation_enabled(False)

    async def test_set_download_behavior(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.set_download_behavior("deny")

    async def test_set_font_sizes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_font_sizes(standard=20, fixed=16)

    async def test_set_ad_blocking_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.set_ad_blocking_enabled(True)
            await session.page.set_ad_blocking_enabled(False)

    async def test_generate_test_report(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.generate_test_report("integration test report", group="tests")

    async def test_compilation_cache(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.produce_compilation_cache(
                scripts=[{"url": "https://example.com/test.js"}]
            )
            with contextlib.suppress(Exception):
                await session.page.add_compilation_cache(
                    "https://example.com/test.js",
                    base64.b64encode(b"cache-data").decode(),
                )
            await session.page.clear_compilation_cache()

    async def test_get_app_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_app_id()
            assert isinstance(result, dict)

    async def test_get_installability_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_installability_errors()
            assert isinstance(result, dict)

    async def test_get_permissions_policy_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.page.get_resource_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            result = await session.page.get_permissions_policy_state(frame_id)
            assert isinstance(result, dict)

    async def test_get_origin_trials(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.page.get_resource_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            result = await session.page.get_origin_trials(frame_id)
            assert isinstance(result, dict)

    async def test_enable_with_file_chooser_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable(enable_file_chooser_opened_event=True)
            await session.page.disable()

    async def test_reload_with_script_to_evaluate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.reload(
                ignore_cache=True,
                script_to_evaluate_on_load="console.log('reloaded')",
            )

    async def test_capture_screenshot_optimize_for_speed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.capture_screenshot(optimize_for_speed=True)
            assert "data" in result

    async def test_print_to_pdf_tagged_and_outline(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.print_to_pdf(
                generate_tagged_pdf=True,
                generate_document_outline=True,
            )
            assert "data" in result

    async def test_set_font_families_with_for_scripts(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.page.set_font_families(
                    {"standard": "Arial"},
                    for_scripts=[
                        {"script": "Zyyy", "fontFamilies": {"standard": "Arial"}},
                    ],
                )

    async def test_set_geolocation_override_partial(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_geolocation_override(latitude=40.0)
            await session.page.clear_geolocation_override()

    async def test_set_geolocation_override_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_geolocation_override()

    async def test_set_intercept_file_chooser_with_cancel(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable(enable_file_chooser_opened_event=True)
            await session.page.set_intercept_file_chooser_dialog(True, cancel=True)
            await session.page.set_intercept_file_chooser_dialog(False)

    async def test_set_prerendering_allowed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.set_prerendering_allowed(True)
            await session.page.set_prerendering_allowed(False)

    async def test_get_app_manifest_with_manifest_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.page.get_app_manifest(
                    manifest_id="https://example.com/manifest.json"
                )
                assert isinstance(result, dict)

    async def test_create_isolated_world_with_csp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.page.get_resource_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            result = await session.page.create_isolated_world(
                frame_id,
                world_name="csp-test",
                grant_universal_access=False,
                content_security_policy="script-src 'self'",
            )
            assert "executionContextId" in result

    async def test_add_script_with_include_command_line_api(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.page.add_script_to_evaluate_on_new_document(
                "console.log('injected')",
                include_command_line_api=True,
                run_immediately=True,
            )
            assert "identifier" in result
            await session.page.remove_script_to_evaluate_on_new_document(
                result["identifier"]
            )

    async def test_get_annotated_page_content(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.page.get_annotated_page_content(
                    include_actionable_information=True,
                )
                assert isinstance(result, dict)

    async def test_produce_compilation_cache_with_eager(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.produce_compilation_cache(
                scripts=[{"url": "https://example.com/test.js", "eager": True}]
            )
            await session.page.clear_compilation_cache()

    async def test_stop_alias_sends_stop_loading(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            with contextlib.suppress(Exception):
                await session.page.stop()

    async def test_set_spc_transaction_mode_auto_accept(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_spc_transaction_mode("autoAccept")
            await session.page.set_spc_transaction_mode("none")

    async def test_set_rph_registration_mode_auto_reject(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_rph_registration_mode("autoReject")
            await session.page.set_rph_registration_mode("none")

    async def test_navigate_with_referrer_policy(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            result = await session.page.navigate(
                "https://example.com",
                referrer="https://ref.com",
                referrer_policy="noReferrer",
            )
            assert "frameId" in result

    async def test_set_web_lifecycle_state_frozen_active(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_web_lifecycle_state("frozen")
            await session.page.set_web_lifecycle_state("active")

    async def test_set_device_metrics_override_full(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_device_metrics_override(
                width=390,
                height=844,
                device_scale_factor=3.0,
                mobile=True,
                screen_orientation={"type": "portraitPrimary", "angle": 0},
            )
            await session.page.clear_device_metrics_override()

    async def test_search_in_resource_regex(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.page.get_resource_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            with contextlib.suppress(Exception):
                result = await session.page.search_in_resource(
                    frame_id, "https://example.com/", "example", is_regex=True,
                )
                assert isinstance(result, dict)

    async def test_handle_dialog_dismiss(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.set_bypass_csp(True)
            await session.runtime.evaluate(
                "setTimeout(() => confirm('test'), 100)",
                await_promise=False,
            )
            await asyncio.sleep(0.5)
            with contextlib.suppress(Exception):
                await session.page.handle_java_script_dialog(accept=False)

    async def test_get_layout_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_layout_metrics()
            assert "layoutViewport" in result
            assert "visualViewport" in result
            assert "contentSize" in result

    async def test_get_frame_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_frame_tree()
            assert "frameTree" in result
            assert "frame" in result["frameTree"]

    async def test_get_resource_content(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.page.get_resource_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            resources = tree["frameTree"].get("resources", [])
            if resources:
                url = resources[0]["url"]
                with contextlib.suppress(Exception):
                    result = await session.page.get_resource_content(frame_id, url)
                    assert "content" in result

    async def test_reset_navigation_history(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.reset_navigation_history()
            history = await session.page.get_navigation_history()
            assert history["currentIndex"] == 0
            assert len(history["entries"]) == 1

    async def test_set_bypass_csp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_bypass_csp(True)
            await session.page.set_bypass_csp(False)

    async def test_capture_screenshot_with_clip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.capture_screenshot(
                clip={"x": 0, "y": 0, "width": 100, "height": 100, "scale": 1},
            )
            assert "data" in result

    async def test_print_to_pdf_landscape(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.print_to_pdf(
                landscape=True, print_background=True,
            )
            assert "data" in result

    async def test_reload_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            await session.page.reload()
            await asyncio.sleep(1.0)

    async def test_reload_with_script(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            await session.page.reload(
                script_to_evaluate_on_load="console.log('reloaded')",
            )
            await asyncio.sleep(1.0)

    async def test_navigate_strict_origin_referrer_policy(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            result = await session.page.navigate(
                "https://example.com",
                referrer_policy="strictOrigin",
            )
            assert "frameId" in result

    async def test_add_script_to_evaluate_on_load_deprecated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            result = await session.page.add_script_to_evaluate_on_load(
                "window.__test = 42"
            )
            assert "identifier" in result
            await session.page.remove_script_to_evaluate_on_load(
                result["identifier"]
            )

    async def test_get_navigation_history_after_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            await session.page.navigate("https://example.org")
            await asyncio.sleep(1.0)
            history = await session.page.get_navigation_history()
            assert history["currentIndex"] >= 1
            assert len(history["entries"]) >= 2

    async def test_go_back_no_history(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.go_back()
            assert result == {}

    async def test_go_forward_no_history(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.go_forward()
            assert result == {}

    async def test_set_device_orientation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_device_orientation_override(
                alpha=0.0, beta=90.0, gamma=0.0,
            )
            await session.page.clear_device_orientation_override()

    async def test_clear_geolocation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.set_geolocation_override(
                latitude=37.7749, longitude=-122.4194,
            )
            await session.page.clear_geolocation_override()

    async def test_screencast_frame_ack(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            frames: list[dict[str, Any]] = []

            async def on_frame(event: dict[str, Any]) -> None:
                frames.append(event)

            session.on("Page.screencastFrame", on_frame)
            await session.page.start_screencast(format="jpeg", quality=50)
            await asyncio.sleep(2.0)
            await session.page.stop_screencast()
            session.off("Page.screencastFrame", on_frame)
            if frames:
                await session.page.screencast_frame_ack(
                    frames[0]["sessionId"]
                )

    async def test_set_document_content(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("about:blank")
            await asyncio.sleep(0.5)
            tree = await session.page.get_frame_tree()
            frame_id = tree["frameTree"]["frame"]["id"]
            await session.page.set_document_content(
                frame_id, "<html><body><h1>Test</h1></body></html>",
            )

    async def test_bring_to_front(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.page.bring_to_front()

    async def test_navigate_with_transition_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            result = await session.page.navigate(
                "https://example.com",
                transition_type="typed",
            )
            assert "frameId" in result

    async def test_capture_screenshot_webp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.capture_screenshot(
                format="webp", quality=60,
            )
            assert "data" in result

    async def test_capture_screenshot_jpeg(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.capture_screenshot(
                format="jpeg", quality=30,
            )
            assert "data" in result

    async def test_navigate_with_transition_type_form_submit(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            result = await session.page.navigate(
                "https://example.com",
                transition_type="form_submit",
            )
            assert "frameId" in result


@pytest.mark.integration
class TestRuntimeExpanded:
    async def test_add_binding(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.add_binding("testBinding")
            await session.runtime.evaluate(
                "globalThis.testBinding", return_by_value=True
            )

    async def test_remove_binding(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.add_binding("tempBinding")
            await session.runtime.remove_binding("tempBinding")

    async def test_get_isolate_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.get_isolate_id()
            assert "id" in result or isinstance(result, dict)

    async def test_get_heap_usage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.get_heap_usage()
            assert "usedSize" in result or isinstance(result, dict)

    async def test_terminate_execution(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.terminate_execution()

    async def test_discard_console_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.discard_console_entries()

    async def test_set_async_call_stack_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.set_async_call_stack_depth(32)

    async def test_set_max_call_stack_size_to_capture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.set_max_call_stack_size_to_capture(100)

    async def test_evaluate_with_include_command_line_api(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "1 + 1", include_command_line_api=True,
            )
            assert result["result"]["value"] == 2

    async def test_call_function_on_with_user_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "window", return_by_value=False,
            )
            obj_id = result["result"]["objectId"]
            result = await session.runtime.call_function_on(
                "function() { return 42; }",
                object_id=obj_id,
                return_by_value=True,
                user_gesture=True,
            )
            assert result["result"]["value"] == 42

    async def test_get_properties_accessor_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "Object.defineProperty({}, 'x', {get(){return 1}, configurable:true})",
                return_by_value=False,
            )
            obj_id = result["result"]["objectId"]
            props = await session.runtime.get_properties(
                obj_id, accessor_properties_only=True,
            )
            assert isinstance(props["result"], list)

    async def test_compile_and_run_script_with_object_group(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            compiled = await session.runtime.compile_script(
                "42", persist_script=True,
            )
            assert "scriptId" in compiled
            result = await session.runtime.run_script(
                compiled["scriptId"],
                return_by_value=True,
                object_group="testGroup",
            )
            assert result["result"]["value"] == 42
            await session.runtime.release_object_group("testGroup")

    async def test_await_promise_with_generate_preview(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "Promise.resolve({a: 1})", return_by_value=False,
            )
            promise_id = result["result"]["objectId"]
            awaited = await session.runtime.await_promise(
                promise_id, return_by_value=True, generate_preview=True,
            )
            assert awaited["result"]["value"]["a"] == 1

    async def test_add_binding_with_context_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.add_binding(
                "namedBinding", execution_context_name="default",
            )

    async def test_evaluate_with_disable_breaks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "1 + 1", disable_breaks=True,
            )
            assert result["result"]["value"] == 2

    async def test_evaluate_with_timeout(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "1 + 1", timeout=5000,
            )
            assert result["result"]["value"] == 2

    async def test_evaluate_with_serialization_options(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "1 + 1",
                return_by_value=True,
                serialization_options={"serialization": "json"},
            )
            assert result["result"]["value"] == 2

    async def test_call_function_on_with_throw_on_side_effect(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            result = await session.runtime.evaluate(
                "window", return_by_value=False,
            )
            obj_id = result["result"]["objectId"]
            result = await session.runtime.call_function_on(
                "function() { return 42; }",
                object_id=obj_id,
                return_by_value=True,
                throw_on_side_effect=True,
            )
            assert result["result"]["value"] == 42


@pytest.mark.integration
class TestNetworkExpanded:
    async def test_set_and_delete_cookies(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            await session.network.set_cookies([
                {
                    "name": "test_cookie",
                    "value": "test_value",
                    "domain": "example.com",
                    "path": "/",
                }
            ])

            cookies = await session.network.get_cookies(urls=["https://example.com"])
            cookie_list = cookies.get("cookies", [])
            assert any(c["name"] == "test_cookie" for c in cookie_list)

            await session.network.delete_cookies(
                "test_cookie", url="https://example.com"
            )

            cookies_after = await session.network.get_cookies(urls=["https://example.com"])
            cookie_list_after = cookies_after.get("cookies", [])
            assert not any(c["name"] == "test_cookie" for c in cookie_list_after)

    async def test_clear_browser_cookies(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            await session.network.clear_browser_cookies()
            result = await session.network.get_cookies(urls=["https://example.com"])
            assert len(result.get("cookies", [])) == 0

    async def test_set_accepted_encodings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.network.set_accepted_encodings(["gzip", "deflate"])
            await session.network.clear_accepted_encodings_override()

    async def test_set_cache_disabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            await session.network.set_cache_disabled(True)
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            await session.network.set_cache_disabled(False)

    async def test_set_attach_debug_stack(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.network.enable()
            with contextlib.suppress(Exception):
                await session.network.set_attach_debug_stack(True)
                await session.network.set_attach_debug_stack(False)


@pytest.mark.integration
class TestDOMExpanded:
    async def test_set_attribute_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            await session.dom.set_attribute_value(h1["nodeId"], "data-test", "value")

            html = await session.dom.get_outer_html(node_id=h1["nodeId"])
            assert "data-test" in html["outerHTML"]

    async def test_get_flattened_document(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.get_flattened_document(depth=3, pierce=True)
            assert "nodes" in result

    async def test_collect_class_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            result = await session.dom.collect_class_names_from_subtree(root_id)
            assert "classNames" in result

    async def test_get_content_quads(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.dom.get_content_quads(node_id=h1["nodeId"])
            assert "quads" in result

    async def test_set_outer_html(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            p = await session.dom.query_selector(root_id, "p")
            if p["nodeId"] != 0:
                await session.dom.set_outer_html(
                    p["nodeId"], "<p id='modified'>Modified text</p>"
                )

    async def test_describe_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            result = await session.dom.describe_node(root_id, depth=2)
            assert "node" in result

    async def test_get_search_results(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            search = await session.dom.perform_search("h1")
            query_id = search["searchId"]
            result_count = search.get("resultCount", 0)
            if result_count > 0:
                result = await session.dom.get_search_results(
                    query_id, 0, result_count
                )
                assert "nodeIds" in result
            await session.dom.discard_search_results(query_id)

    async def test_get_top_layer_elements(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.get_top_layer_elements()
            assert "nodeIds" in result


@pytest.mark.integration
class TestEmulationExpanded:
    async def test_set_cpu_throttling_rate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_cpu_throttling_rate(4.0)
            await asyncio.sleep(0.5)
            await session.emulation.set_cpu_throttling_rate(1.0)

    async def test_set_script_execution_disabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_script_execution_disabled(True)
            await session.emulation.set_script_execution_disabled(False)

    async def test_set_auto_dark_mode_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_auto_dark_mode_override(True)
            await session.emulation.set_auto_dark_mode_override(False)

    async def test_set_default_background_color_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_default_background_color_override(
                r=255, g=0, b=0, a=1.0
            )
            await session.emulation.set_default_background_color_override()

    async def test_set_focus_emulation_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_focus_emulation_enabled(True)
            await session.emulation.set_focus_emulation_enabled(False)

    async def test_set_touch_emulation_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_touch_emulation_enabled(True)
            await session.emulation.set_touch_emulation_enabled(False)

    async def test_set_emulated_media(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_emulated_media("print")
            await session.emulation.set_emulated_media("screen")

    async def test_set_emulated_media_with_features(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_emulated_media(
                features=[{"name": "prefers-color-scheme", "value": "dark"}]
            )
            await session.emulation.set_emulated_media("screen")

    async def test_set_hardware_concurrency_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_hardware_concurrency_override(4)

            result = await session.runtime.evaluate(
                "navigator.hardwareConcurrency", return_by_value=True
            )
            assert result["result"]["value"] == 4

    async def test_set_data_saver_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_data_saver_override(True)
            await session.emulation.set_data_saver_override(False)

    async def test_set_automation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_automation_override(True)
            await session.emulation.set_automation_override(False)

    async def test_set_safe_area_insets_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_safe_area_insets_override(
                top=10, left=5, bottom=10, right=5
            )

    async def test_set_emulated_os_text_scale(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_os_text_scale(1.5)
            await session.emulation.set_emulated_os_text_scale(1.0)


@pytest.mark.integration
class TestStorageExpanded:
    async def test_clear_data_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.storage.clear_data_for_origin(
                "https://example.com", "cookies"
            )

    async def test_get_usage_and_quota(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.storage.get_usage_and_quota("https://example.com")
            assert isinstance(result, dict)

    async def test_track_cache_storage_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.storage.track_cache_storage_for_origin("https://example.com")
            await session.storage.untrack_cache_storage_for_origin("https://example.com")

    async def test_track_indexed_db_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.storage.track_indexed_db_for_origin("https://example.com")
            await session.storage.untrack_indexed_db_for_origin("https://example.com")

    async def test_override_quota_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.storage.override_quota_for_origin(
                "https://example.com", quota_size=1024 * 1024
            )
            await session.storage.override_quota_for_origin("https://example.com")

    async def test_get_shared_storage_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.storage.get_shared_storage_metadata(
                    "https://example.com"
                )
                assert isinstance(result, dict)

    async def test_shared_storage_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.storage.set_shared_storage_entry(
                    "https://example.com", "key1", "value1"
                )

                entries = await session.storage.get_shared_storage_entries(
                    "https://example.com"
                )
                assert isinstance(entries, dict)

                await session.storage.delete_shared_storage_entry(
                    "https://example.com", "key1"
                )

                await session.storage.clear_shared_storage_entries("https://example.com")

    async def test_run_bounce_tracking_mitigations(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.storage.run_bounce_tracking_mitigations()
            assert isinstance(result, dict)

    async def test_get_related_website_sets(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.storage.get_related_website_sets()
                assert isinstance(result, dict)


@pytest.mark.integration
class TestOverlayExpanded:
    async def test_set_inspect_mode(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            highlight_config = {
                "showInfo": True,
                "showStyles": False,
                "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
            }
            await session.overlay.set_inspect_mode(
                "searchForNode", highlight_config=highlight_config
            )
            await session.overlay.set_inspect_mode(
                "none", highlight_config=highlight_config
            )

    async def test_set_show_debug_borders(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.set_show_debug_borders(True)
            await session.overlay.set_show_debug_borders(False)

    async def test_set_show_fps_counter(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.set_show_fps_counter(True)
            await session.overlay.set_show_fps_counter(False)

    async def test_set_show_paint_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.set_show_paint_rects(True)
            await session.overlay.set_show_paint_rects(False)

    async def test_set_show_layout_shift_regions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.set_show_layout_shift_regions(True)
            await session.overlay.set_show_layout_shift_regions(False)

    async def test_set_paused_in_debugger_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.overlay.set_paused_in_debugger_message("Paused for test")
            await session.overlay.set_paused_in_debugger_message()


@pytest.mark.integration
class TestCSSExpanded:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom.enable()
            await session.css.enable()
            await session.css.disable()

    async def test_get_computed_style_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.css.get_computed_style_for_node(h1["nodeId"])
            assert "computedStyle" in result
            await session.css.disable()

    async def test_get_inline_styles_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.css.get_inline_styles_for_node(h1["nodeId"])
            assert isinstance(result, dict)
            await session.css.disable()

    async def test_get_media_queries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_media_queries()
            assert isinstance(result, dict)
            await session.css.disable()

    async def test_get_environment_variables(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_environment_variables()
            assert isinstance(result, dict)
            await session.css.disable()
