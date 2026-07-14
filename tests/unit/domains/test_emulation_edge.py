"""Edge-case tests for the Emulation domain — validation branches only.

Targets every TypeError/ValueError raise in EmulationDomain to push
coverage from 88% to >=90%.
"""

import pytest

from cdpwave.domains.emulation import EmulationDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestEmulationEdgeValidation:
    async def test_set_device_metrics_scrollbar_type_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="scrollbar_type must be a str or None"):
            await d.set_device_metrics_override(100, 100, scrollbar_type=123)  # type: ignore[arg-type]

    async def test_set_device_metrics_scrollbar_type_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="scrollbar_type must be 'default' or 'overlay'"):
            await d.set_device_metrics_override(100, 100, scrollbar_type="invalid")

    async def test_set_emulated_media_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="media must be 'print', 'screen', or ''"):
            await d.set_emulated_media("invalid")

    async def test_set_sensor_override_readings_type_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.set_sensor_override_readings(123, {})  # type: ignore[arg-type]

    async def test_set_sensor_override_readings_type_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be one of"):
            await d.set_sensor_override_readings("invalid", {})

    async def test_set_emulated_vision_deficiency_type_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.set_emulated_vision_deficiency(123)  # type: ignore[arg-type]

    async def test_set_emulated_vision_deficiency_type_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be 'none'"):
            await d.set_emulated_vision_deficiency("invalid")

    async def test_set_virtual_time_policy_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="policy must be a str"):
            await d.set_virtual_time_policy(123)  # type: ignore[arg-type]

    async def test_set_virtual_time_policy_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="policy must be 'advance'"):
            await d.set_virtual_time_policy("invalid")

    async def test_set_device_posture_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="posture must be a str"):
            await d.set_device_posture_override(123)  # type: ignore[arg-type]

    async def test_set_device_posture_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="posture must be 'continuous' or 'folded'"):
            await d.set_device_posture_override("invalid")

    async def test_set_emit_touch_events_configuration_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="configuration must be a str or None"):
            await d.set_emit_touch_events_for_mouse(True, configuration=123)  # type: ignore[arg-type]

    async def test_set_emit_touch_events_configuration_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="configuration must be 'mobile' or 'desktop'"):
            await d.set_emit_touch_events_for_mouse(True, configuration="invalid")

    async def test_set_sensor_override_enabled_type_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.set_sensor_override_enabled(True, 123)  # type: ignore[arg-type]

    async def test_set_sensor_override_enabled_type_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be one of"):
            await d.set_sensor_override_enabled(True, "invalid")

    async def test_get_overridden_sensor_information_type_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.get_overridden_sensor_information(123)  # type: ignore[arg-type]

    async def test_get_overridden_sensor_information_type_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be one of"):
            await d.get_overridden_sensor_information("invalid")

    async def test_set_pressure_source_override_source_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="source must be a str"):
            await d.set_pressure_source_override_enabled(123, True)  # type: ignore[arg-type]

    async def test_set_pressure_source_override_source_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="source must be 'cpu'"):
            await d.set_pressure_source_override_enabled("invalid", True)

    async def test_set_pressure_state_override_source_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="source must be a str"):
            await d.set_pressure_state_override(123, "nominal")  # type: ignore[arg-type]

    async def test_set_pressure_state_override_state_not_str(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(TypeError, match="state must be a str"):
            await d.set_pressure_state_override("cpu", 123)  # type: ignore[arg-type]

    async def test_set_pressure_state_override_state_invalid(self) -> None:
        d = EmulationDomain(FakeSender({}))
        with pytest.raises(ValueError, match="state must be 'nominal'"):
            await d.set_pressure_state_override("cpu", "invalid")


@pytest.mark.unit
class TestEmulationEdgeHappyPaths:
    async def test_set_device_metrics_with_scrollbar_type(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_device_metrics_override(100, 100, scrollbar_type="overlay")
        _, params = fake.last_call
        assert params["scrollbarType"] == "overlay"

    async def test_set_device_metrics_with_scale(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_device_metrics_override(100, 100, scale=2.0)
        _, params = fake.last_call
        assert params["scale"] == 2.0

    async def test_set_device_metrics_with_screen_dims(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_device_metrics_override(
            100, 100, screen_width=1920, screen_height=1080,
            position_x=10, position_y=20,
        )
        _, params = fake.last_call
        assert params["screenWidth"] == 1920
        assert params["screenHeight"] == 1080
        assert params["positionX"] == 10
        assert params["positionY"] == 20

    async def test_set_default_background_color_override_from_rgba(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_default_background_color_override(r=255, g=0, b=0, a=0.5)
        _, params = fake.last_call
        assert params["color"] == {"r": 255, "g": 0, "b": 0, "a": 0.5}

    async def test_set_default_background_color_override_clear(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_default_background_color_override()
        _, params = fake.last_call
        assert "color" not in params

    async def test_set_emulated_media_feature(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_emulated_media_feature("prefers-color-scheme", "dark")
        _, params = fake.last_call
        assert params["features"] == [{"name": "prefers-color-scheme", "value": "dark"}]

    async def test_set_idle_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_idle_override(True, False)
        assert fake.last_call == (
            "Emulation.setIdleOverride",
            {"isUserActive": True, "isScreenUnlocked": False},
        )

    async def test_clear_idle_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.clear_idle_override()
        assert fake.last_call == ("Emulation.clearIdleOverride", None)

    async def test_set_timezone_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_timezone_override("America/New_York")
        assert fake.last_call == (
            "Emulation.setTimezoneOverride",
            {"timezoneId": "America/New_York"},
        )

    async def test_clear_timezone_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.clear_timezone_override()
        assert fake.last_call == (
            "Emulation.setTimezoneOverride",
            {"timezoneId": ""},
        )

    async def test_set_locale_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_locale_override("en-US")
        assert fake.last_call == ("Emulation.setLocaleOverride", {"locale": "en-US"})

    async def test_set_locale_override_empty(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_locale_override("")
        _, params = fake.last_call
        assert "locale" not in params

    async def test_clear_emulated_vision_deficiency(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.clear_emulated_vision_deficiency()
        assert fake.last_call == (
            "Emulation.setEmulatedVisionDeficiency",
            {"type": "none"},
        )

    async def test_set_virtual_time_policy_with_opts(self) -> None:
        fake = FakeSender({"virtualTimeTicksBase": 0})
        d = EmulationDomain(fake)
        await d.set_virtual_time_policy(
            "advance", budget=1000.0,
            max_virtual_time_task_starvation_count=10,
            initial_virtual_time=500.0,
        )
        _, params = fake.last_call
        assert params["budget"] == 1000.0
        assert params["maxVirtualTimeTaskStarvationCount"] == 10
        assert params["initialVirtualTime"] == 500.0

    async def test_set_focus_emulation_enabled(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_focus_emulation_enabled(True)
        assert fake.last_call == (
            "Emulation.setFocusEmulationEnabled",
            {"enabled": True},
        )

    async def test_set_auto_dark_mode_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_auto_dark_mode_override(True)
        assert fake.last_call == (
            "Emulation.setAutoDarkModeOverride",
            {"enabled": True},
        )

    async def test_clear_auto_dark_mode_override(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.clear_auto_dark_mode_override()
        assert fake.last_call == (
            "Emulation.setAutoDarkModeOverride",
            {"enabled": False},
        )

    async def test_set_navigator_overrides(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_navigator_overrides("Win32")
        assert fake.last_call == (
            "Emulation.setNavigatorOverrides",
            {"platform": "Win32"},
        )

    async def test_set_page_scale_factor(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_page_scale_factor(1.5)
        assert fake.last_call == (
            "Emulation.setPageScaleFactor",
            {"pageScaleFactor": 1.5},
        )

    async def test_set_visible_size(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_visible_size(800, 600)
        assert fake.last_call == (
            "Emulation.setVisibleSize",
            {"width": 800, "height": 600},
        )

    async def test_set_scrollbars_hidden(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_scrollbars_hidden(True)
        assert fake.last_call == (
            "Emulation.setScrollbarsHidden",
            {"hidden": True},
        )

    async def test_set_document_cookie_disabled(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_document_cookie_disabled(True)
        assert fake.last_call == (
            "Emulation.setDocumentCookieDisabled",
            {"disabled": True},
        )

    async def test_set_emit_touch_events_for_mouse_with_config(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_emit_touch_events_for_mouse(True, configuration="mobile")
        _, params = fake.last_call
        assert params["configuration"] == "mobile"

    async def test_clear_emulated_media(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.clear_emulated_media()
        assert fake.last_call == ("Emulation.setEmulatedMedia", None)

    async def test_set_touch_emulation_enabled_no_max(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_touch_emulation_enabled(True)
        _, params = fake.last_call
        assert "maxTouchPoints" not in params

    async def test_set_emulated_media_empty(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_emulated_media("")
        _, params = fake.last_call
        assert "media" not in params

    async def test_set_emulated_media_with_both(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_emulated_media("print", [{"name": "x", "value": "y"}])
        _, params = fake.last_call
        assert params["media"] == "print"
        assert params["features"] == [{"name": "x", "value": "y"}]

    async def test_remove_screen(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.remove_screen("s1")
        assert fake.last_call == ("Emulation.removeScreen", {"screenId": "s1"})

    async def test_set_primary_screen(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_primary_screen("s1")
        assert fake.last_call == ("Emulation.setPrimaryScreen", {"screenId": "s1"})

    async def test_update_screen(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.update_screen("s1", left=10, top=20, width=800, height=600)
        _, params = fake.last_call
        assert params["screenId"] == "s1"
        assert params["left"] == 10
        assert params["top"] == 20
        assert params["width"] == 800
        assert params["height"] == 600

    async def test_update_screen_with_all_opts(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.update_screen(
            "s1", work_area_insets={"top": 10}, device_pixel_ratio=2.0,
            rotation=90, color_depth=32, label="main",
        )
        _, params = fake.last_call
        assert params["workAreaInsets"] == {"top": 10}
        assert params["devicePixelRatio"] == 2.0
        assert params["rotation"] == 90
        assert params["colorDepth"] == 32
        assert params["label"] == "main"

    async def test_add_screen_with_all_opts(self) -> None:
        fake = FakeSender({"screenInfo": {}})
        d = EmulationDomain(fake)
        await d.add_screen(
            0, 0, 1920, 1080,
            work_area_insets={"top": 10}, rotation=90, color_depth=32,
        )
        _, params = fake.last_call
        assert params["workAreaInsets"] == {"top": 10}
        assert params["rotation"] == 90
        assert params["colorDepth"] == 32

    async def test_set_safe_area_insets_override_with_max(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_safe_area_insets_override(
            top=10, left=5, bottom=10, right=5,
            top_max=20, left_max=15, bottom_max=20, right_max=15,
        )
        _, params = fake.last_call
        assert params["insets"]["topMax"] == 20
        assert params["insets"]["leftMax"] == 15
        assert params["insets"]["bottomMax"] == 20
        assert params["insets"]["rightMax"] == 15

    async def test_set_geolocation_override_all_params(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_geolocation_override(
            latitude=37.0, longitude=-122.0, accuracy=100.0,
            altitude=10.0, altitude_accuracy=5.0, heading=180.0, speed=50.0,
        )
        _, params = fake.last_call
        assert params["latitude"] == 37.0
        assert params["longitude"] == -122.0
        assert params["accuracy"] == 100.0
        assert params["altitude"] == 10.0
        assert params["altitudeAccuracy"] == 5.0
        assert params["heading"] == 180.0
        assert params["speed"] == 50.0

    async def test_set_geolocation_override_empty(self) -> None:
        fake = FakeSender({})
        d = EmulationDomain(fake)
        await d.set_geolocation_override()
        _, params = fake.last_call
        assert params == {}
