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

    async def test_set_window_bounds(self) -> None:
        fake = FakeSender({})
        domain = HeadlessExperimentalDomain(fake)
        await domain.set_window_bounds(
            window_id=1, bounds={"width": 800, "height": 600}
        )
        method, params = fake.last_call
        assert method == "HeadlessExperimental.setWindowBounds"
        assert params is not None
        assert params["windowId"] == 1
        assert params["bounds"]["width"] == 800

    async def test_set_window_bounds_defaults(self) -> None:
        fake = FakeSender({})
        domain = HeadlessExperimentalDomain(fake)
        await domain.set_window_bounds()
        assert fake.last_call == ("HeadlessExperimental.setWindowBounds", {})


@pytest.mark.unit
class TestTetheringDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.enable(port=8080)
        assert fake.last_call == ("Tethering.bind", {"port": 8080})

    async def test_enable_no_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Tethering.bind", {})

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.disable(port=8080)
        assert fake.last_call == ("Tethering.unbind", {"port": 8080})

    async def test_disable_no_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Tethering.unbind", {})


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


@pytest.mark.unit
class TestCastDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Cast.enable", None)

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
