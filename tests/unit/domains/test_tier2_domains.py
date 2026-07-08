from typing import Any

from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.fetch import FetchDomain
from cdpwave.domains.input import InputDomain
from tests.unit.fake_sender import FakeSender


class TestInputDomain:
    async def test_dispatch_key_event_required_only(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_key_event("keyDown")
        method, params = fake.last_call
        assert method == "Input.dispatchKeyEvent"
        assert params is not None
        assert params["type"] == "keyDown"

    async def test_dispatch_key_event_all_params(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_key_event(
            "keyDown",
            key="a",
            code="KeyA",
            windows_virtual_key_code=65,
            native_virtual_key_code=65,
            text="a",
            modifiers=0,
            auto_repeat=False,
            location=0,
        )
        method, params = fake.last_call
        assert method == "Input.dispatchKeyEvent"
        assert params is not None
        assert params["key"] == "a"
        assert params["code"] == "KeyA"
        assert params["windowsVirtualKeyCode"] == 65
        assert params["nativeVirtualKeyCode"] == 65
        assert params["text"] == "a"
        assert params["modifiers"] == 0
        assert params["autoRepeat"] is False
        assert params["location"] == 0

    async def test_dispatch_mouse_event_defaults(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_mouse_event("mouseMoved", 100.0, 200.0)
        method, params = fake.last_call
        assert method == "Input.dispatchMouseEvent"
        assert params is not None
        assert params["type"] == "mouseMoved"
        assert params["x"] == 100.0
        assert params["y"] == 200.0
        assert params["button"] == "none"
        assert params["buttons"] == 0

    async def test_dispatch_mouse_event_with_click(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_mouse_event(
            "mousePressed",
            50.0,
            60.0,
            button="left",
            click_count=1,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["button"] == "left"
        assert params["clickCount"] == 1

    async def test_dispatch_touch_event(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        touch_points: list[dict[str, Any]] = [{"x": 10, "y": 20, "id": 1}]
        await domain.dispatch_touch_event("touchStart", touch_points)
        method, params = fake.last_call
        assert method == "Input.dispatchTouchEvent"
        assert params is not None
        assert params["type"] == "touchStart"
        assert params["touchPoints"] == touch_points

    async def test_dispatch_drag_event(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.dispatch_drag_event("dragEnter", 10.0, 20.0)
        method, params = fake.last_call
        assert method == "Input.dispatchDragEvent"
        assert params is not None
        assert params["type"] == "dragEnter"
        assert params["x"] == 10.0
        assert params["y"] == 20.0

    async def test_insert_text(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.insert_text("hello")
        assert fake.last_call == ("Input.insertText", {"text": "hello"})

    async def test_ime_set_composition(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.ime_set_composition("text", 0, 4)
        method, params = fake.last_call
        assert method == "Input.imeSetComposition"
        assert params is not None
        assert params["text"] == "text"
        assert params["selectionStart"] == 0
        assert params["selectionEnd"] == 4

    async def test_cancel_dragging(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.cancel_dragging()
        assert fake.last_call == ("Input.cancelDragging", None)

    async def test_set_intercept_drags(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.set_intercept_drags(True)
        assert fake.last_call == (
            "Input.setInterceptDrags",
            {"enabled": True},
        )

    async def test_synthesize_pinch_gesture(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_pinch_gesture(100.0, 200.0, 1.5)
        method, params = fake.last_call
        assert method == "Input.synthesizePinchGesture"
        assert params is not None
        assert params["x"] == 100.0
        assert params["y"] == 200.0
        assert params["scaleFactor"] == 1.5
        assert params["relativeSpeed"] == 800
        assert params["gestureSourceType"] == "default"

    async def test_synthesize_scroll_gesture_defaults(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_scroll_gesture(50.0, 50.0, y_distance=100.0)
        method, params = fake.last_call
        assert method == "Input.synthesizeScrollGesture"
        assert params is not None
        assert params["x"] == 50.0
        assert params["y"] == 50.0
        assert params["yDistance"] == 100.0
        assert params["preventFling"] is True

    async def test_synthesize_tap_gesture(self) -> None:
        fake = FakeSender({})
        domain = InputDomain(fake)
        await domain.synthesize_tap_gesture(100.0, 200.0)
        method, params = fake.last_call
        assert method == "Input.synthesizeTapGesture"
        assert params is not None
        assert params["x"] == 100.0
        assert params["y"] == 200.0
        assert params["duration"] == 50
        assert params["tapCount"] == 1


class TestEmulationDomain:
    async def test_set_device_metrics_override_required_only(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(1920, 1080)
        method, params = fake.last_call
        assert method == "Emulation.setDeviceMetricsOverride"
        assert params is not None
        assert params["width"] == 1920
        assert params["height"] == 1080
        assert params["deviceScaleFactor"] == 1.0
        assert params["mobile"] is False

    async def test_set_device_metrics_override_mobile(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_device_metrics_override(
            375,
            812,
            device_scale_factor=3.0,
            mobile=True,
            screen_orientation={"type": "portraitPrimary", "angle": 0},
        )
        method, params = fake.last_call
        assert params is not None
        assert params["mobile"] is True
        assert params["deviceScaleFactor"] == 3.0
        assert params["screenOrientation"]["type"] == "portraitPrimary"

    async def test_clear_device_metrics_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_device_metrics_override()
        assert fake.last_call == ("Emulation.clearDeviceMetricsOverride", None)

    async def test_set_user_agent_override_required_only(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_user_agent_override("Test/1.0")
        method, params = fake.last_call
        assert method == "Emulation.setUserAgentOverride"
        assert params is not None
        assert params["userAgent"] == "Test/1.0"
        assert "acceptLanguage" not in params

    async def test_set_cpu_throttling_rate(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_cpu_throttling_rate(4.0)
        assert fake.last_call == (
            "Emulation.setCPUThrottlingRate",
            {"rate": 4.0},
        )

    async def test_set_script_execution_disabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_script_execution_disabled(True)
        assert fake.last_call == (
            "Emulation.setScriptExecutionDisabled",
            {"disabled": True},
        )

    async def test_set_geolocation_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_geolocation_override(37.7749, -122.4194)
        method, params = fake.last_call
        assert method == "Emulation.setGeolocationOverride"
        assert params is not None
        assert params["latitude"] == 37.7749
        assert params["longitude"] == -122.4194
        assert params["accuracy"] == 100.0

    async def test_clear_geolocation_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_geolocation_override()
        assert fake.last_call == ("Emulation.clearGeolocationOverride", None)

    async def test_set_touch_emulation_enabled(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_touch_emulation_enabled(True, max_touch_points=5)
        method, params = fake.last_call
        assert method == "Emulation.setTouchEmulationEnabled"
        assert params is not None
        assert params["enabled"] is True
        assert params["maxTouchPoints"] == 5

    async def test_set_emulated_media(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_emulated_media("print")
        assert fake.last_call == (
            "Emulation.setEmulatedMedia",
            {"media": "print"},
        )

    async def test_set_emulated_media_with_features(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        features: list[dict[str, str]] = [{"name": "prefers-color-scheme", "value": "dark"}]
        await domain.set_emulated_media(features=features)
        method, params = fake.last_call
        assert params is not None
        assert params["media"] == ""
        assert params["features"] == features

    async def test_set_default_background_color_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        color: dict[str, Any] = {"r": 0, "g": 0, "b": 0, "a": 0}
        await domain.set_default_background_color_override(color)
        assert fake.last_call == (
            "Emulation.setDefaultBackgroundColorOverride",
            {"color": color},
        )

    async def test_clear_default_background_color_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_default_background_color_override()
        assert fake.last_call == (
            "Emulation.clearDefaultBackgroundColorOverride",
            None,
        )

    async def test_set_idle_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_idle_override(True, False)
        assert fake.last_call == (
            "Emulation.setIdleOverride",
            {"isUserActive": True, "isScreenActive": False},
        )

    async def test_clear_idle_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_idle_override()
        assert fake.last_call == ("Emulation.clearIdleOverride", None)

    async def test_set_timezone_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_timezone_override("America/New_York")
        assert fake.last_call == (
            "Emulation.setTimezoneOverride",
            {"timezoneId": "America/New_York"},
        )

    async def test_clear_timezone_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_timezone_override()
        assert fake.last_call == (
            "Emulation.setTimezoneOverride",
            {"timezoneId": ""},
        )

    async def test_set_locale_override(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_locale_override("es-ES")
        assert fake.last_call == (
            "Emulation.setLocaleOverride",
            {"locale": "es-ES"},
        )

    async def test_set_disabled_sensors(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_disabled_sensors(True)
        assert fake.last_call == (
            "Emulation.setDisabledSensors",
            {"disabled": True},
        )

    async def test_set_sensor_override_readings(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        reading: dict[str, Any] = {"x": 1.0, "y": 0.0, "z": 0.0}
        await domain.set_sensor_override_readings("accelerometer", reading)
        assert fake.last_call == (
            "Emulation.setSensorOverrideReadings",
            {"type": "accelerometer", "reading": reading},
        )

    async def test_clear_sensor_override_readings(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.clear_sensor_override_readings("gyroscope")
        assert fake.last_call == (
            "Emulation.clearSensorOverrideReadings",
            {"type": "gyroscope"},
        )

    async def test_set_page_scale_factor(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_page_scale_factor(2.0)
        assert fake.last_call == (
            "Emulation.setPageScaleFactor",
            {"pageScaleFactor": 2.0},
        )

    async def test_set_visible_size(self) -> None:
        fake = FakeSender({})
        domain = EmulationDomain(fake)
        await domain.set_visible_size(800, 600)
        assert fake.last_call == (
            "Emulation.setVisibleSize",
            {"width": 800, "height": 600},
        )


class TestFetchDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "Fetch.enable"
        assert params is not None
        assert params["handleAuthRequests"] is False

    async def test_enable_with_patterns(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        patterns: list[dict[str, Any]] = [
            {"urlPattern": "*api*", "requestStage": "Request"},
        ]
        await domain.enable(patterns=patterns, handle_auth_requests=True)
        method, params = fake.last_call
        assert method == "Fetch.enable"
        assert params is not None
        assert params["patterns"] == patterns
        assert params["handleAuthRequests"] is True

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Fetch.disable", None)

    async def test_continue_request_required_only(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_request("REQ-1")
        assert fake.last_call == (
            "Fetch.continueRequest",
            {"requestId": "REQ-1"},
        )

    async def test_continue_request_all_params(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        headers: list[dict[str, str]] = [{"name": "X-Custom", "value": "val"}]
        await domain.continue_request(
            "REQ-1",
            url="https://modified.com",
            method="POST",
            post_data="data",
            headers=headers,
        )
        method, params = fake.last_call
        assert method == "Fetch.continueRequest"
        assert params is not None
        assert params["url"] == "https://modified.com"
        assert params["method"] == "POST"
        assert params["postData"] == "data"
        assert params["headers"] == headers

    async def test_continue_request_with_auth(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        auth_response: dict[str, Any] = {
            "response": "ProvideCredentials",
            "username": "user",
            "password": "pass",
        }
        await domain.continue_request_with_auth("REQ-1", auth_response)
        assert fake.last_call == (
            "Fetch.continueWithAuth",
            {"requestId": "REQ-1", "authChallengeResponse": auth_response},
        )

    async def test_continue_response(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.continue_response("REQ-1", response_code=200)
        method, params = fake.last_call
        assert method == "Fetch.continueResponse"
        assert params is not None
        assert params["responseCode"] == 200

    async def test_fulfill_request(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.fulfill_request("REQ-1", 200, body="hello")
        method, params = fake.last_call
        assert method == "Fetch.fulfillRequest"
        assert params is not None
        assert params["responseCode"] == 200
        assert params["body"] == "hello"

    async def test_fail_request(self) -> None:
        fake = FakeSender({})
        domain = FetchDomain(fake)
        await domain.fail_request("REQ-1", "Failed")
        assert fake.last_call == (
            "Fetch.failRequest",
            {"requestId": "REQ-1", "errorReason": "Failed"},
        )

    async def test_get_response_body(self) -> None:
        fake = FakeSender({"body": "content", "base64Encoded": False})
        domain = FetchDomain(fake)
        await domain.get_response_body("REQ-1")
        assert fake.last_call == (
            "Fetch.getResponseBody",
            {"requestId": "REQ-1"},
        )

    async def test_take_response_body_as_stream(self) -> None:
        fake = FakeSender({"stream": "stream-id"})
        domain = FetchDomain(fake)
        await domain.take_response_body_as_stream("REQ-1")
        assert fake.last_call == (
            "Fetch.takeResponseBodyAsStream",
            {"requestId": "REQ-1"},
        )
