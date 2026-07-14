"""Edge-case tests for the Input domain — validation branches only.

Targets every TypeError/ValueError raise in InputDomain to push
coverage from 89% to >=90%.
"""

import pytest

from cdpwave.domains.input import InputDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestInputEdgeValidation:
    async def test_dispatch_key_event_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.dispatch_key_event(123)  # type: ignore[arg-type]

    async def test_dispatch_key_event_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be 'keyDown'"):
            await d.dispatch_key_event("invalid")

    async def test_dispatch_mouse_event_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.dispatch_mouse_event(123)  # type: ignore[arg-type]

    async def test_dispatch_mouse_event_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be 'mousePressed'"):
            await d.dispatch_mouse_event("invalid")

    async def test_dispatch_mouse_event_button_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="button must be a str"):
            await d.dispatch_mouse_event("mouseMoved", button=123)  # type: ignore[arg-type]

    async def test_dispatch_mouse_event_button_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="button must be 'none'"):
            await d.dispatch_mouse_event("mouseMoved", button="invalid")

    async def test_emulate_touch_from_mouse_event_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="type must be a str"):
            await d.emulate_touch_from_mouse_event(123, 0, 0)  # type: ignore[arg-type]

    async def test_emulate_touch_from_mouse_event_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="type must be 'mouseWheel'"):
            await d.emulate_touch_from_mouse_event("invalid", 0, 0)

    async def test_emulate_touch_from_mouse_event_button_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="button must be a str"):
            await d.emulate_touch_from_mouse_event("mouseMoved", 0, 0, button=123)  # type: ignore[arg-type]

    async def test_emulate_touch_from_mouse_event_button_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="button must be 'none'"):
            await d.emulate_touch_from_mouse_event("mouseMoved", 0, 0, button="invalid")

    async def test_synthesize_pinch_gesture_source_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="gesture_source_type must be a str"):
            await d.synthesize_pinch_gesture(0, 0, 1.0, gesture_source_type=123)  # type: ignore[arg-type]

    async def test_synthesize_pinch_gesture_source_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="gesture_source_type must be 'default'"):
            await d.synthesize_pinch_gesture(0, 0, 1.0, gesture_source_type="invalid")

    async def test_synthesize_scroll_gesture_source_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="gesture_source_type must be a str"):
            await d.synthesize_scroll_gesture(0, 0, gesture_source_type=123)  # type: ignore[arg-type]

    async def test_synthesize_scroll_gesture_source_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="gesture_source_type must be 'default'"):
            await d.synthesize_scroll_gesture(0, 0, gesture_source_type="invalid")

    async def test_synthesize_tap_gesture_source_type_not_str(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(TypeError, match="gesture_source_type must be a str"):
            await d.synthesize_tap_gesture(0, 0, gesture_source_type=123)  # type: ignore[arg-type]

    async def test_synthesize_tap_gesture_source_type_invalid(self) -> None:
        d = InputDomain(FakeSender({}))
        with pytest.raises(ValueError, match="gesture_source_type must be 'default'"):
            await d.synthesize_tap_gesture(0, 0, gesture_source_type="invalid")


@pytest.mark.unit
class TestInputEdgeHappyPaths:
    async def test_dispatch_touch_event_with_modifiers(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.dispatch_touch_event("touchStart", [{"x": 0, "y": 0}], modifiers=1)
        _, params = fake.last_call
        assert params["modifiers"] == 1

    async def test_dispatch_touch_event_with_timestamp(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.dispatch_touch_event("touchStart", [{"x": 0, "y": 0}], timestamp=123.0)
        _, params = fake.last_call
        assert params["timestamp"] == 123.0

    async def test_dispatch_drag_event_with_modifiers(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.dispatch_drag_event("dragEnter", 0, 0, {"items": []}, modifiers=1)
        _, params = fake.last_call
        assert params["modifiers"] == 1

    async def test_ime_set_composition_with_replacement(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.ime_set_composition("text", 0, 4, replacement_start=1, replacement_end=3)
        _, params = fake.last_call
        assert params["replacementStart"] == 1
        assert params["replacementEnd"] == 3

    async def test_synthesize_scroll_gesture_with_marker(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.synthesize_scroll_gesture(0, 0, interaction_marker_name="marker1")
        _, params = fake.last_call
        assert params["interactionMarkerName"] == "marker1"

    async def test_emulate_touch_from_mouse_event_with_opts(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.emulate_touch_from_mouse_event(
            "mouseMoved", 10, 20,
            click_count=2, delta_x=1.0, delta_y=2.0,
            modifiers=1, timestamp=100.0,
        )
        _, params = fake.last_call
        assert params["clickCount"] == 2
        assert params["deltaX"] == 1.0
        assert params["deltaY"] == 2.0
        assert params["modifiers"] == 1
        assert params["timestamp"] == 100.0

    async def test_set_ignore_input_events(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.set_ignore_input_events(True)
        assert fake.last_call == ("Input.setIgnoreInputEvents", {"ignore": True})

    async def test_type_text_empty(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.type_text("")
        assert len(fake.calls) == 0

    async def test_type_text_single_char(self) -> None:
        fake = FakeSender({})
        d = InputDomain(fake)
        await d.type_text("a")
        assert len(fake.calls) == 1
        method, params = fake.last_call
        assert method == "Input.dispatchKeyEvent"
        assert params["type"] == "char"
        assert params["text"] == "a"
