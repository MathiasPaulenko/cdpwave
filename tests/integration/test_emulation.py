import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


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
class TestEmulation:
    async def test_set_device_metrics_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.emulation.set_device_metrics_override(
                width=375,
                height=812,
                device_scale_factor=3.0,
                mobile=True,
            )
            await asyncio.sleep(0.5)

            w = await session.runtime.evaluate(
                "window.innerWidth", return_by_value=True,
            )
            h = await session.runtime.evaluate(
                "window.innerHeight", return_by_value=True,
            )
            assert w["result"]["value"] == 375
            assert h["result"]["value"] == 812

            await session.emulation.clear_device_metrics_override()

    async def test_set_device_metrics_override_desktop(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            await session.emulation.set_device_metrics_override(
                width=1920,
                height=1080,
                device_scale_factor=1.0,
                mobile=False,
            )
            await asyncio.sleep(0.5)

            result = await session.runtime.evaluate(
                "window.innerWidth", return_by_value=True,
            )
            assert result["result"]["value"] == 1920

            await session.emulation.clear_device_metrics_override()

    async def test_set_user_agent_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_user_agent_override(
                "cdpwave-emulation-test/2.0",
                accept_language="es-ES",
                platform="TestPlatform",
            )

            result = await session.runtime.evaluate(
                "navigator.userAgent", return_by_value=True,
            )
            assert "cdpwave-emulation-test" in result["result"]["value"]

    async def test_set_cpu_throttling_rate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_cpu_throttling_rate(2.0)
            await session.emulation.set_cpu_throttling_rate(1.0)

    async def test_set_script_execution_disabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            await session.runtime.evaluate(
                "window._scriptRan = false; "
                "setTimeout(() => { window._scriptRan = true; }, 100);",
            )

            await session.emulation.set_script_execution_disabled(True)
            await asyncio.sleep(0.5)

            await session.runtime.evaluate(
                "window._scriptRan2 = false; "
                "setTimeout(() => { window._scriptRan2 = true; }, 100);",
            )

            await asyncio.sleep(0.5)
            result = await session.runtime.evaluate(
                "window._scriptRan2", return_by_value=True,
            )
            assert result["result"]["value"] is False

            await session.emulation.set_script_execution_disabled(False)

    async def test_set_geolocation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_geolocation_override(
                latitude=37.7749,
                longitude=-122.4194,
                accuracy=10.0,
            )

            await session.runtime.evaluate(
                """
                navigator.permissions.query({name: 'geolocation'})
                    .then(r => r.state)
                """,
                await_promise=True,
                return_by_value=True,
            )

            await session.emulation.clear_geolocation_override()

    async def test_set_touch_emulation_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_touch_emulation_enabled(
                True,
                max_touch_points=5,
            )

            result = await session.runtime.evaluate(
                "navigator.maxTouchPoints", return_by_value=True,
            )
            assert result["result"]["value"] == 5

            await session.emulation.set_touch_emulation_enabled(False)

    async def test_set_emulated_media_print(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media("print")

            result = await session.runtime.evaluate(
                "window.matchMedia('print').matches", return_by_value=True,
            )
            assert result["result"]["value"] is True

            await session.emulation.set_emulated_media("")

    async def test_set_emulated_media_dark_mode(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media(
                features=[{"name": "prefers-color-scheme", "value": "dark"}],
            )

            result = await session.runtime.evaluate(
                "window.matchMedia('(prefers-color-scheme: dark)').matches",
                return_by_value=True,
            )
            assert result["result"]["value"] is True

            await session.emulation.set_emulated_media(
                features=[{"name": "prefers-color-scheme", "value": "light"}],
            )

    async def test_set_default_background_color_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.set_default_background_color_override(
                {"r": 255, "g": 0, "b": 0, "a": 1.0},
            )
            assert result == {}

            await session.emulation.clear_default_background_color_override()

    async def test_set_idle_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.emulation.set_idle_override(
                    is_user_active=True,
                    is_screen_unlocked=True,
                )
                await session.emulation.clear_idle_override()

    async def test_set_timezone_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_timezone_override("America/New_York")

            result = await session.runtime.evaluate(
                "Intl.DateTimeFormat().resolvedOptions().timeZone",
                return_by_value=True,
            )
            assert result["result"]["value"] == "America/New_York"

            await session.emulation.clear_timezone_override()

    async def test_set_locale_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_locale_override("es-ES")

            result = await session.runtime.evaluate(
                "Intl.DateTimeFormat().resolvedOptions().locale",
                return_by_value=True,
            )
            assert result["result"]["value"] == "es-ES"

    async def test_set_page_scale_factor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_page_scale_factor(2.0)

            await session.emulation.set_page_scale_factor(1.0)

    async def test_set_visible_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_visible_size(800, 600)

            await session.emulation.set_visible_size(1280, 720)

    # --- Edge cases for omitempty / omitzero behavior ---

    async def test_set_device_metrics_override_with_orientation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_device_metrics_override(
                width=768,
                height=1024,
                device_scale_factor=2.0,
                mobile=True,
                screen_orientation={"type": "portraitPrimary", "angle": 0},
            )
            await asyncio.sleep(0.3)
            result = await session.runtime.evaluate(
                "screen.orientation.type", return_by_value=True,
            )
            assert result["result"]["value"] == "portrait-primary"
            await session.emulation.clear_device_metrics_override()

    async def test_set_device_metrics_override_with_viewport(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_device_metrics_override(
                width=400,
                height=800,
                device_scale_factor=2.0,
                mobile=True,
                viewport={"x": 0, "y": 0, "width": 400, "height": 800, "scale": 1},
            )
            await asyncio.sleep(0.3)
            w = await session.runtime.evaluate(
                "window.innerWidth", return_by_value=True,
            )
            assert w["result"]["value"] == 400
            await session.emulation.clear_device_metrics_override()

    async def test_set_device_metrics_override_scale(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_device_metrics_override(
                width=375,
                height=667,
                device_scale_factor=2.0,
                mobile=True,
                scale=0.5,
            )
            await asyncio.sleep(0.3)
            await session.emulation.clear_device_metrics_override()

    async def test_set_device_metrics_override_dont_set_visible_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.emulation.set_device_metrics_override(
                width=375,
                height=667,
                device_scale_factor=2.0,
                mobile=True,
                dont_set_visible_size=True,
            )
            await asyncio.sleep(0.3)
            await session.emulation.clear_device_metrics_override()

    async def test_clear_emulated_media(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media("print")
            await asyncio.sleep(0.2)
            await session.emulation.clear_emulated_media()
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "window.matchMedia('print').matches", return_by_value=True,
            )
            assert result["result"]["value"] is False

    async def test_set_emulated_media_feature_convenience(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media_feature(
                "prefers-reduced-motion", "reduce",
            )
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "window.matchMedia('(prefers-reduced-motion: reduce)').matches",
                return_by_value=True,
            )
            assert result["result"]["value"] is True

            await session.emulation.set_emulated_media_feature(
                "prefers-reduced-motion", "no-preference",
            )

    async def test_set_emulated_media_multiple_features(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media(
                features=[
                    {"name": "prefers-color-scheme", "value": "dark"},
                    {"name": "prefers-reduced-motion", "value": "reduce"},
                ],
            )
            await asyncio.sleep(0.2)
            r1 = await session.runtime.evaluate(
                "window.matchMedia('(prefers-color-scheme: dark)').matches",
                return_by_value=True,
            )
            r2 = await session.runtime.evaluate(
                "window.matchMedia('(prefers-reduced-motion: reduce)').matches",
                return_by_value=True,
            )
            assert r1["result"]["value"] is True
            assert r2["result"]["value"] is True
            await session.emulation.clear_emulated_media()

    async def test_set_default_background_color_rgba(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_default_background_color_override(
                r=255, g=128, b=0, a=1.0,
            )
            await asyncio.sleep(0.2)
            await session.emulation.clear_default_background_color_override()

    async def test_clear_default_background_color_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_default_background_color_override(
                {"r": 0, "g": 255, "b": 0, "a": 1.0},
            )
            await asyncio.sleep(0.2)
            await session.emulation.clear_default_background_color_override()

    async def test_clear_timezone_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_timezone_override("Asia/Tokyo")
            await asyncio.sleep(0.2)
            await session.emulation.clear_timezone_override()
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "Intl.DateTimeFormat().resolvedOptions().timeZone",
                return_by_value=True,
            )
            assert result["result"]["value"] != "Asia/Tokyo"

    async def test_set_locale_override_empty_clears(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_locale_override("fr-FR")
            await asyncio.sleep(0.2)
            r1 = await session.runtime.evaluate(
                "Intl.DateTimeFormat().resolvedOptions().locale",
                return_by_value=True,
            )
            assert r1["result"]["value"] == "fr-FR"

            await session.emulation.set_locale_override("")
            await asyncio.sleep(0.2)
            r2 = await session.runtime.evaluate(
                "Intl.DateTimeFormat().resolvedOptions().locale",
                return_by_value=True,
            )
            assert r2["result"]["value"] != "fr-FR"

    async def test_set_emulated_vision_deficiency(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_vision_deficiency("deuteranopia")
            await asyncio.sleep(0.2)
            await session.emulation.clear_emulated_vision_deficiency()

    async def test_clear_emulated_vision_deficiency(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_vision_deficiency("protanopia")
            await asyncio.sleep(0.2)
            await session.emulation.clear_emulated_vision_deficiency()

    async def test_set_focus_emulation_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_focus_emulation_enabled(True)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "document.hasFocus()", return_by_value=True,
            )
            assert result["result"]["value"] is True
            await session.emulation.set_focus_emulation_enabled(False)

    async def test_set_auto_dark_mode_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_auto_dark_mode_override(True)
            await asyncio.sleep(0.2)
            await session.emulation.clear_auto_dark_mode_override()

    async def test_clear_auto_dark_mode_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_auto_dark_mode_override(True)
            await asyncio.sleep(0.2)
            await session.emulation.clear_auto_dark_mode_override()

    async def test_set_hardware_concurrency_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_hardware_concurrency_override(4)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.hardwareConcurrency", return_by_value=True,
            )
            assert result["result"]["value"] == 4

    async def test_set_automation_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_automation_override(True)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.webdriver", return_by_value=True,
            )
            assert result["result"]["value"] is True
            await session.emulation.set_automation_override(False)

    async def test_set_navigator_overrides(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_navigator_overrides("Linux x86_64")
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.platform", return_by_value=True,
            )
            assert result["result"]["value"] == "Linux x86_64"

    async def test_set_virtual_time_policy_pause(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.set_virtual_time_policy("pause")
            assert "virtualTimeTicksBase" in result

    async def test_set_virtual_time_policy_advance_with_budget(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.set_virtual_time_policy(
                "advance", budget=1000,
            )
            assert "virtualTimeTicksBase" in result

    async def test_set_scrollbars_hidden(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_scrollbars_hidden(True)
            await asyncio.sleep(0.2)
            await session.emulation.set_scrollbars_hidden(False)

    async def test_set_document_cookie_disabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_document_cookie_disabled(True)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "document.cookie = 'test=1'; document.cookie",
                return_by_value=True,
            )
            assert result["result"]["value"] == ""
            await session.emulation.set_document_cookie_disabled(False)

    async def test_set_emulated_os_text_scale(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_os_text_scale(1.5)
            await asyncio.sleep(0.2)
            await session.emulation.set_emulated_os_text_scale(0)

    async def test_set_emulated_os_text_scale_zero_clears(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_os_text_scale(2.0)
            await asyncio.sleep(0.2)
            await session.emulation.set_emulated_os_text_scale()
            await asyncio.sleep(0.2)

    async def test_set_safe_area_insets_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_safe_area_insets_override(
                top=44, left=0, bottom=34, right=0,
                top_max=88, bottom_max=68,
            )
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "getComputedStyle(document.documentElement)"
                ".getPropertyValue('env(safe-area-inset-top)')",
                return_by_value=True,
            )
            assert result["result"]["value"] is not None

    async def test_set_small_viewport_height_difference_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_small_viewport_height_difference_override(50)
            await asyncio.sleep(0.2)

    async def test_set_data_saver_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_data_saver_override(True)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.connection ? navigator.connection.saveData : 'unsupported'",
                return_by_value=True,
            )
            assert result["result"]["value"] in (True, "unsupported")
            await session.emulation.set_data_saver_override(False)

    async def test_set_disabled_image_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_disabled_image_types(["avif", "webp"])
            await asyncio.sleep(0.2)

    async def test_set_sensor_override_enabled_with_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "accelerometer",
                metadata={"samplingFrequency": 60},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_sensor_override_enabled(
                False, "accelerometer",
            )

    async def test_set_sensor_override_readings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "accelerometer",
            )
            await session.emulation.set_sensor_override_readings(
                "accelerometer", {"xyz": {"x": 1.0, "y": 0.0, "z": 0.0}},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_sensor_override_enabled(
                False, "accelerometer",
            )

    async def test_get_overridden_sensor_information(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "gyroscope",
                metadata={"samplingFrequency": 30},
            )
            await asyncio.sleep(0.2)
            result = await session.emulation.get_overridden_sensor_information(
                "gyroscope",
            )
            assert "requestedSamplingFrequency" in result
            await session.emulation.set_sensor_override_enabled(
                False, "gyroscope",
            )

    async def test_set_pressure_source_override_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_pressure_source_override_enabled(
                "cpu", True, metadata={"available": True},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_pressure_source_override_enabled(
                "cpu", False,
            )

    async def test_set_pressure_state_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_pressure_source_override_enabled("cpu", True)
            await session.emulation.set_pressure_state_override("cpu", "critical")
            await asyncio.sleep(0.2)
            await session.emulation.set_pressure_source_override_enabled("cpu", False)

    async def test_set_device_posture_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_device_posture_override("folded")
            await asyncio.sleep(0.2)
            await session.emulation.clear_device_posture_override()

    async def test_clear_device_posture_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_device_posture_override("continuous")
            await asyncio.sleep(0.2)
            await session.emulation.clear_device_posture_override()

    async def test_set_display_features_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_display_features_override([
                {
                    "orientation": "vertical",
                    "offset": 200,
                    "maskLength": 10,
                },
            ])
            await asyncio.sleep(0.2)
            await session.emulation.clear_display_features_override()

    async def test_clear_display_features_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.clear_display_features_override()

    async def test_get_screen_infos(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.get_screen_infos()
            assert "screenInfos" in result
            assert isinstance(result["screenInfos"], list)

    async def test_can_emulate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.can_emulate()
            assert "result" in result

    async def test_reset_page_scale_factor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_page_scale_factor(2.0)
            await asyncio.sleep(0.2)
            await session.emulation.reset_page_scale_factor()

    # --- Headless-only screen management ---

    async def test_add_and_remove_screen(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.add_screen(
                0, 0, 1920, 1080, device_pixel_ratio=1.0, label="test-screen",
            )
            assert "screenInfo" in result
            screen_id = result["screenInfo"]["id"]
            await session.emulation.remove_screen(screen_id)

    async def test_update_screen(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.add_screen(
                0, 0, 1920, 1080, label="orig",
            )
            screen_id = result["screenInfo"]["id"]
            await session.emulation.update_screen(
                screen_id, width=800, height=600, label="updated",
            )
            await session.emulation.remove_screen(screen_id)

    async def test_set_primary_screen(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            r1 = await session.emulation.add_screen(
                0, 0, 1920, 1080, label="primary",
            )
            r2 = await session.emulation.add_screen(
                1920, 0, 800, 600, label="secondary",
            )
            sid2 = r2["screenInfo"]["id"]
            await session.emulation.set_primary_screen(sid2)
            await session.emulation.set_primary_screen(r1["screenInfo"]["id"])
            await session.emulation.remove_screen(sid2)

    # --- Edge cases for geolocation ---

    async def test_set_geolocation_override_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_geolocation_override(
                latitude=40.7128,
                longitude=-74.0060,
                accuracy=5.0,
                altitude=10.0,
                altitude_accuracy=2.0,
                heading=180.0,
                speed=1.5,
            )
            await asyncio.sleep(0.2)
            await session.emulation.clear_geolocation_override()

    async def test_set_geolocation_override_empty_emulates_unavailable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_geolocation_override()
            await asyncio.sleep(0.2)
            await session.emulation.clear_geolocation_override()

    # --- Edge cases for user agent ---

    async def test_set_user_agent_override_with_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_user_agent_override(
                "TestUA/1.0",
                accept_language="en-US",
                platform="MacIntel",
                user_agent_metadata={
                    "brands": [
                        {"brand": "Chromium", "version": "120"},
                    ],
                    "fullVersionList": [
                        {"brand": "Chromium", "version": "120.0.0.0"},
                    ],
                    "platform": "macOS",
                    "platformVersion": "14.0",
                    "architecture": "arm",
                    "model": "",
                    "mobile": False,
                    "bitness": "64",
                    "wow64": False,
                },
            )
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.userAgent", return_by_value=True,
            )
            assert "TestUA" in result["result"]["value"]

    # --- Edge cases for touch ---

    async def test_set_touch_emulation_default_touch_points(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_touch_emulation_enabled(True)
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.maxTouchPoints", return_by_value=True,
            )
            assert result["result"]["value"] >= 1
            await session.emulation.set_touch_emulation_enabled(False)

    # --- Edge cases for emit touch events for mouse ---

    async def test_set_emit_touch_events_for_mouse(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emit_touch_events_for_mouse(
                True, configuration="mobile",
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_emit_touch_events_for_mouse(False)

    # --- Integration tests for missing methods ---

    async def test_set_virtual_time_policy_pause_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.set_virtual_time_policy(
                "pause",
            )
            assert "virtualTimeTicksBase" in result
            await session.emulation.set_virtual_time_policy("advance")

    async def test_set_virtual_time_policy_advance(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.emulation.set_virtual_time_policy(
                "advance", budget=500.0, initial_virtual_time=100.0,
            )
            assert "virtualTimeTicksBase" in result

    async def test_set_sensor_override_readings_accelerometer(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "accelerometer",
            )
            await session.emulation.set_sensor_override_readings(
                "accelerometer", {"xyz": {"x": 1.0, "y": 0.0, "z": 9.8}},
            )
            await session.emulation.set_sensor_override_readings(
                "accelerometer", {"xyz": {"x": 0.0, "y": 0.0, "z": 0.0}},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_sensor_override_enabled(
                False, "accelerometer",
            )

    async def test_set_sensor_override_enabled_with_metadata_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "accelerometer",
                metadata={"available": True, "minimumFrequency": 10, "maximumFrequency": 60},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_sensor_override_enabled(
                False, "accelerometer",
            )

    async def test_get_overridden_sensor_information_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_sensor_override_enabled(
                True, "gyroscope",
            )
            result = await session.emulation.get_overridden_sensor_information(
                "gyroscope",
            )
            assert "requestedSamplingFrequency" in result
            await session.emulation.set_sensor_override_enabled(
                False, "gyroscope",
            )

    async def test_set_pressure_source_override_enabled_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_pressure_source_override_enabled(
                "cpu", True,
                metadata={"available": True, "minimumFrequency": 1, "maximumFrequency": 10},
            )
            await asyncio.sleep(0.2)
            await session.emulation.set_pressure_source_override_enabled(
                "cpu", False,
            )

    async def test_set_pressure_state_override_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_pressure_source_override_enabled("cpu", True)
            await session.emulation.set_pressure_state_override("cpu", "serious")
            await asyncio.sleep(0.2)
            await session.emulation.set_pressure_source_override_enabled("cpu", False)

    async def test_set_disabled_image_types_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_disabled_image_types(["webp", "avif"])
            await asyncio.sleep(0.2)
            await session.emulation.set_disabled_image_types([])

    async def test_set_small_viewport_height_difference_override_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_small_viewport_height_difference_override(50)
            await asyncio.sleep(0.2)
            await session.emulation.set_small_viewport_height_difference_override(0)

    async def test_set_navigator_overrides_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_navigator_overrides("Win32")
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "navigator.platform", return_by_value=True,
            )
            assert result["result"]["value"] == "Win32"

    async def test_set_scrollbars_hidden_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_scrollbars_hidden(True)
            await asyncio.sleep(0.2)
            await session.emulation.set_scrollbars_hidden(False)

    async def test_set_document_cookie_disabled_extra(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_document_cookie_disabled(True)
            await asyncio.sleep(0.2)
            await session.emulation.set_document_cookie_disabled(False)

    async def test_set_emulated_media_both_media_and_features(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_emulated_media(
                "print",
                features=[{"name": "prefers-color-scheme", "value": "dark"}],
            )
            await asyncio.sleep(0.2)
            result = await session.runtime.evaluate(
                "window.matchMedia('print').matches", return_by_value=True,
            )
            assert result["result"]["value"] is True
            await session.emulation.clear_emulated_media()

    async def test_set_device_metrics_override_with_scrollbar_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_device_metrics_override(
                375, 812, device_scale_factor=2.0, mobile=True,
                scrollbar_type="overlay",
            )
            await asyncio.sleep(0.3)
            await session.emulation.clear_device_metrics_override()

    async def test_set_device_metrics_override_with_screen_orientation_lock(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.emulation.set_device_metrics_override(
                375, 812, device_scale_factor=2.0, mobile=True,
                screen_orientation={"type": "landscapePrimary", "angle": 90},
                screen_orientation_lock_emulation=True,
            )
            await asyncio.sleep(0.3)
            await session.emulation.clear_device_metrics_override()
