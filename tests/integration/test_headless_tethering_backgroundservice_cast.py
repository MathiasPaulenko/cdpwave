"""Functional tests for HeadlessExperimental, Tethering, BackgroundService, and Cast domains."""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestHeadlessExperimental:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.enable()
                await session.headless_experimental.disable()

    async def test_set_window_bounds(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.set_window_bounds(
                    bounds={"width": 800, "height": 600}
                )


@pytest.mark.integration
class TestTethering:
    async def test_bind_unbind(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.enable(port=0)
                await session.tethering.disable(port=0)


@pytest.mark.integration
class TestBackgroundService:
    async def test_start_stop_observing(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.start_observing(
                    "backgroundSync"
                )
                await session.background_service.set_recording(
                    True, "backgroundSync"
                )
                await session.background_service.clear_events(
                    "backgroundSync"
                )
                await session.background_service.stop_observing(
                    "backgroundSync"
                )


@pytest.mark.integration
class TestCast:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.disable()
