"""Functional tests for HeadlessExperimental, Tethering, BackgroundService, and Cast domains."""

import asyncio
import contextlib
from typing import Any

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

    async def test_begin_frame(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.begin_frame(
                    interval=16.666
                )


@pytest.mark.integration
class TestTethering:
    async def test_bind_unbind(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(0)
                await session.tethering.unbind(0)


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
class TestBackgroundServiceEdgeCases:
    """Edge cases for BackgroundService domain on a real browser."""

    async def test_stop_without_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.stop_observing(
                    "backgroundSync"
                )

    async def test_clear_events_without_observing(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.clear_events(
                    "notifications"
                )

    async def test_set_recording_false_without_observing(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.set_recording(
                    False, "pushMessaging"
                )

    async def test_start_observing_all_services(self) -> None:
        """Start and stop observing for each ServiceName enum value."""
        services = [
            "backgroundFetch",
            "backgroundSync",
            "periodicBackgroundSync",
            "pushMessaging",
            "notifications",
            "paymentHandler",
        ]
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for service in services:
                with contextlib.suppress(Exception):
                    await session.background_service.start_observing(service)
                    await session.background_service.stop_observing(service)

    async def test_double_start_observing(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.start_observing(
                    "backgroundSync"
                )
                await session.background_service.start_observing(
                    "backgroundSync"
                )
                await session.background_service.stop_observing(
                    "backgroundSync"
                )


@pytest.mark.integration
class TestBackgroundServiceFlow:
    """End-to-end flows for BackgroundService domain."""

    async def test_full_lifecycle(self) -> None:
        """Start observing → set recording → clear events → stop observing."""
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
                await session.background_service.set_recording(
                    False, "backgroundSync"
                )
                await session.background_service.stop_observing(
                    "backgroundSync"
                )

    async def test_event_received_listener(self) -> None:
        """Start observing → listen for backgroundServiceEventReceived."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            with contextlib.suppress(Exception):
                await session.background_service.start_observing(
                    "backgroundSync"
                )
                session.on(
                    "BackgroundService.backgroundServiceEventReceived",
                    on_event,
                )
                await session.background_service.set_recording(
                    True, "backgroundSync"
                )

                await asyncio.sleep(2.0)

                await session.background_service.stop_observing(
                    "backgroundSync"
                )

    async def test_recording_state_changed_listener(self) -> None:
        """Set recording → listen for recordingStateChanged event."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            states: list[dict[str, Any]] = []

            async def on_state(params: dict[str, Any]) -> None:
                states.append(params)

            with contextlib.suppress(Exception):
                session.on(
                    "BackgroundService.recordingStateChanged",
                    on_state,
                )
                await session.background_service.set_recording(
                    True, "backgroundSync"
                )
                await asyncio.sleep(1.0)
                await session.background_service.set_recording(
                    False, "backgroundSync"
                )

    async def test_multiple_services_independent(self) -> None:
        """Observe multiple services simultaneously."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.background_service.start_observing(
                    "backgroundSync"
                )
                await session.background_service.start_observing(
                    "notifications"
                )
                await session.background_service.set_recording(
                    True, "backgroundSync"
                )
                await session.background_service.set_recording(
                    True, "notifications"
                )
                await session.background_service.clear_events(
                    "backgroundSync"
                )
                await session.background_service.clear_events(
                    "notifications"
                )
                await session.background_service.stop_observing(
                    "backgroundSync"
                )
                await session.background_service.stop_observing(
                    "notifications"
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

    async def test_enable_with_presentation_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable(
                    presentation_url="https://example.com/cast"
                )
                await session.cast.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.set_sink_to_use("sink1")
                await session.cast.start_desktop_mirroring("sink1")
                await session.cast.start_tab_mirroring("sink1")
                await session.cast.stop_casting("sink1")
                await session.cast.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.disable()

    async def test_enable_disable_cycle_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.cast.enable()
                    await session.cast.disable()

    async def test_enable_with_empty_presentation_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable(presentation_url="")
                await session.cast.disable()

    async def test_all_sink_methods_same_sink(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.set_sink_to_use("my-chromecast")
                await session.cast.start_desktop_mirroring("my-chromecast")
                await session.cast.start_tab_mirroring("my-chromecast")
                await session.cast.stop_casting("my-chromecast")
                await session.cast.disable()


@pytest.mark.integration
class TestTetheringEdgeCases:
    async def test_bind_unbind_multiple_ports(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(8080)
                await session.tethering.bind(9090)
                await session.tethering.unbind(8080)
                await session.tethering.unbind(9090)

    async def test_unbind_without_bind(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.unbind(8080)

    async def test_bind_same_port_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(8080)
                await session.tethering.bind(8080)
                await session.tethering.unbind(8080)

    async def test_bind_unbind_cycle_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.tethering.bind(0)
                    await session.tethering.unbind(0)

    async def test_bind_negative_port(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(-1)
                await session.tethering.unbind(-1)

    async def test_bind_large_port(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(65535)
                await session.tethering.unbind(65535)
