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
                    is_screen_active=True,
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
