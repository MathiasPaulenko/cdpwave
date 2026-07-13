"""Unit tests for HeadlessExperimental, Tethering, BackgroundService, and Cast domains."""

import pytest

from cdpwave.domains.background_service import BackgroundServiceDomain
from cdpwave.domains.cast import CastDomain
from cdpwave.domains.headless_experimental import HeadlessExperimentalDomain
from cdpwave.domains.tethering import TetheringDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestHeadlessExperimentalDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = HeadlessExperimentalDomain(fake)
        await domain.enable()
        assert fake.last_call == ("HeadlessExperimental.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = HeadlessExperimentalDomain(fake)
        await domain.disable()
        assert fake.last_call == ("HeadlessExperimental.disable", None)

    async def test_begin_frame(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(
            frame_time_ticks=100.5,
            interval=16.666,
            no_display_updates=False,
            screenshot={"format": "png"},
        )
        method, params = fake.last_call
        assert method == "HeadlessExperimental.beginFrame"
        assert params is not None
        assert params["frameTimeTicks"] == 100.5
        assert params["interval"] == 16.666
        assert params["noDisplayUpdates"] is False
        assert params["screenshot"]["format"] == "png"

    async def test_begin_frame_defaults(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame()
        assert fake.last_call == ("HeadlessExperimental.beginFrame", {})


@pytest.mark.unit
class TestTetheringDomain:
    async def test_bind(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(8080)
        assert fake.last_call == ("Tethering.bind", {"port": 8080})

    async def test_unbind(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(8080)
        assert fake.last_call == ("Tethering.unbind", {"port": 8080})


@pytest.mark.unit
class TestBackgroundServiceDomain:
    async def test_start_observing(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.start_observing("backgroundSync")
        assert fake.last_call == (
            "BackgroundService.startObserving",
            {"service": "backgroundSync"},
        )

    async def test_stop_observing(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.stop_observing("backgroundSync")
        assert fake.last_call == (
            "BackgroundService.stopObserving",
            {"service": "backgroundSync"},
        )

    async def test_set_recording(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.set_recording(True, "pushMessaging")
        method, params = fake.last_call
        assert method == "BackgroundService.setRecording"
        assert params is not None
        assert params["shouldRecord"] is True
        assert params["service"] == "pushMessaging"

    async def test_clear_events(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.clear_events("notifications")
        assert fake.last_call == (
            "BackgroundService.clearEvents",
            {"service": "notifications"},
        )

    async def test_set_recording_false(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.set_recording(False, "backgroundFetch")
        method, params = fake.last_call
        assert method == "BackgroundService.setRecording"
        assert params is not None
        assert params["shouldRecord"] is False
        assert params["service"] == "backgroundFetch"

    async def test_start_observing_periodic_sync(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.start_observing("periodicBackgroundSync")
        assert fake.last_call == (
            "BackgroundService.startObserving",
            {"service": "periodicBackgroundSync"},
        )

    async def test_stop_observing_payment_handler(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.stop_observing("paymentHandler")
        assert fake.last_call == (
            "BackgroundService.stopObserving",
            {"service": "paymentHandler"},
        )

    async def test_clear_events_push_messaging(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.clear_events("pushMessaging")
        assert fake.last_call == (
            "BackgroundService.clearEvents",
            {"service": "pushMessaging"},
        )

    async def test_start_observing_background_fetch(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.start_observing("backgroundFetch")
        assert fake.last_call == (
            "BackgroundService.startObserving",
            {"service": "backgroundFetch"},
        )


@pytest.mark.unit
class TestCastDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Cast.enable", {})

    async def test_enable_with_presentation_url(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url="https://example.com/cast")
        assert fake.last_call == (
            "Cast.enable",
            {"presentationUrl": "https://example.com/cast"},
        )

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Cast.disable", None)

    async def test_set_sink_to_use(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("chromecast-1234")
        assert fake.last_call == (
            "Cast.setSinkToUse",
            {"sinkName": "chromecast-1234"},
        )

    async def test_start_desktop_mirroring(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_desktop_mirroring("chromecast-1234")
        assert fake.last_call == (
            "Cast.startDesktopMirroring",
            {"sinkName": "chromecast-1234"},
        )

    async def test_start_tab_mirroring(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_tab_mirroring("chromecast-1234")
        assert fake.last_call == (
            "Cast.startTabMirroring",
            {"sinkName": "chromecast-1234"},
        )

    async def test_stop_casting(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.stop_casting("chromecast-1234")
        assert fake.last_call == (
            "Cast.stopCasting",
            {"sinkName": "chromecast-1234"},
        )
