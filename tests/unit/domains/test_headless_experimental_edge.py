"""Edge case unit tests for the HeadlessExperimental domain."""

import pytest

from cdpwave.domains.headless_experimental import HeadlessExperimentalDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestHeadlessExperimentalEdgeCases:
    async def test_begin_frame_zero_frame_time_ticks(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(frame_time_ticks=0)
        method, params = fake.last_call
        assert method == "HeadlessExperimental.beginFrame"
        assert params is not None
        assert params["frameTimeTicks"] == 0

    async def test_begin_frame_zero_interval(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(interval=0)
        method, params = fake.last_call
        assert params is not None
        assert params["interval"] == 0

    async def test_begin_frame_no_display_updates_true(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(no_display_updates=True)
        method, params = fake.last_call
        assert params is not None
        assert params["noDisplayUpdates"] is True

    async def test_begin_frame_no_display_updates_false(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(no_display_updates=False)
        method, params = fake.last_call
        assert params is not None
        assert params["noDisplayUpdates"] is False

    async def test_begin_frame_screenshot_jpeg_with_quality_zero(self) -> None:
        fake = FakeSender({"hasDamage": True, "screenshotData": "base64"})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(
            screenshot={"format": "jpeg", "quality": 0, "optimizeForSpeed": False}
        )
        method, params = fake.last_call
        assert params is not None
        assert params["screenshot"]["format"] == "jpeg"
        assert params["screenshot"]["quality"] == 0
        assert params["screenshot"]["optimizeForSpeed"] is False

    async def test_begin_frame_screenshot_webp_with_quality_100(self) -> None:
        fake = FakeSender({"hasDamage": True, "screenshotData": "base64"})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(
            screenshot={"format": "webp", "quality": 100, "optimizeForSpeed": True}
        )
        method, params = fake.last_call
        assert params is not None
        assert params["screenshot"]["format"] == "webp"
        assert params["screenshot"]["quality"] == 100
        assert params["screenshot"]["optimizeForSpeed"] is True

    async def test_begin_frame_screenshot_png_no_quality(self) -> None:
        fake = FakeSender({"hasDamage": True, "screenshotData": "base64"})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(screenshot={"format": "png"})
        method, params = fake.last_call
        assert params is not None
        assert params["screenshot"]["format"] == "png"
        assert "quality" not in params["screenshot"]

    async def test_begin_frame_only_frame_time_ticks(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(frame_time_ticks=500.0)
        method, params = fake.last_call
        assert params is not None
        assert params["frameTimeTicks"] == 500.0
        assert "interval" not in params
        assert "noDisplayUpdates" not in params
        assert "screenshot" not in params

    async def test_begin_frame_only_interval(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(interval=33.333)
        method, params = fake.last_call
        assert params is not None
        assert params["interval"] == 33.333
        assert "frameTimeTicks" not in params

    async def test_begin_frame_return_value(self) -> None:
        fake = FakeSender({"hasDamage": True, "screenshotData": "iVBOR..."})
        domain = HeadlessExperimentalDomain(fake)
        result = await domain.begin_frame(screenshot={"format": "png"})
        assert result["hasDamage"] is True
        assert result["screenshotData"] == "iVBOR..."

    async def test_begin_frame_return_value_no_screenshot(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        result = await domain.begin_frame()
        assert result["hasDamage"] is False
        assert "screenshotData" not in result

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.enable()
        await domain.begin_frame(interval=16.0)
        await domain.disable()
        assert len(fake.calls) == 3
        assert fake.calls[0][0] == "HeadlessExperimental.enable"
        assert fake.calls[1][0] == "HeadlessExperimental.beginFrame"
        assert fake.calls[2][0] == "HeadlessExperimental.disable"

    async def test_begin_frame_empty_params_when_all_none(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(
            frame_time_ticks=None,
            interval=None,
            no_display_updates=None,
            screenshot=None,
        )
        method, params = fake.last_call
        assert method == "HeadlessExperimental.beginFrame"
        assert params == {}

    async def test_begin_frame_negative_frame_time_ticks(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(frame_time_ticks=-1.0)
        method, params = fake.last_call
        assert params is not None
        assert params["frameTimeTicks"] == -1.0

    async def test_begin_frame_very_small_interval(self) -> None:
        fake = FakeSender({"hasDamage": False})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(interval=0.001)
        method, params = fake.last_call
        assert params is not None
        assert params["interval"] == 0.001
