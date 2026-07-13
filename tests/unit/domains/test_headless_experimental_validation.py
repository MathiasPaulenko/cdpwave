"""Unit tests for type and enum validation in HeadlessExperimental domain."""

import pytest

from cdpwave.domains.headless_experimental import HeadlessExperimentalDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestHeadlessExperimentalTypeValidation:
    async def test_begin_frame_frame_time_ticks_str_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="frame_time_ticks"):
            await domain.begin_frame(frame_time_ticks="100")

    async def test_begin_frame_frame_time_ticks_bool_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="frame_time_ticks"):
            await domain.begin_frame(frame_time_ticks=True)

    async def test_begin_frame_interval_str_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="interval"):
            await domain.begin_frame(interval="16")

    async def test_begin_frame_interval_bool_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="interval"):
            await domain.begin_frame(interval=True)

    async def test_begin_frame_no_display_updates_str_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="no_display_updates"):
            await domain.begin_frame(no_display_updates="true")

    async def test_begin_frame_no_display_updates_int_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="no_display_updates"):
            await domain.begin_frame(no_display_updates=1)

    async def test_begin_frame_screenshot_str_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="screenshot"):
            await domain.begin_frame(screenshot="png")

    async def test_begin_frame_screenshot_list_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="screenshot"):
            await domain.begin_frame(screenshot=["png"])

    async def test_begin_frame_screenshot_int_raises(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        with pytest.raises(TypeError, match="screenshot"):
            await domain.begin_frame(screenshot=42)

    async def test_begin_frame_int_frame_time_ticks_accepted(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(frame_time_ticks=100)
        method, params = fake.last_call
        assert params is not None
        assert params["frameTimeTicks"] == 100

    async def test_begin_frame_int_interval_accepted(self) -> None:
        fake = FakeSender({"hasDamage": True})
        domain = HeadlessExperimentalDomain(fake)
        await domain.begin_frame(interval=16)
        method, params = fake.last_call
        assert params is not None
        assert params["interval"] == 16
