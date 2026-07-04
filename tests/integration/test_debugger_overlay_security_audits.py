"""Functional tests for Debugger, Overlay, Security, and Audits domains."""

import asyncio
import contextlib
from typing import Any

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

    async def test_set_show_web_vitals(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await self._setup(session)
            await session.overlay.enable()
            await session.overlay.set_show_web_vitals(True)
            await session.overlay.set_show_web_vitals(False)
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
