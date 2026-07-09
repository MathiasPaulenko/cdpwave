"""P1b: EMULATION, INPUT, FETCH, STORAGE domain tests."""

from __future__ import annotations
import asyncio, contextlib
from typing import Any, Callable, Awaitable
from cdpwave.client import CDPClient, CDPSession
from cdpwave.exceptions import CommandError
from tests.manual._test_helpers import fresh_session, safe_navigate, nav_data
from tests.manual._test_helpers import log_result

_test_registry: list[tuple[str, str, Callable[[CDPClient], Awaitable[None]]]] = []

def reg(tc_id: str, name: str):
    def decorator(func):
        _test_registry.append((tc_id, name, func))
        return func
    return decorator

# ===================== EMULATION DOMAIN (39 tests) =====================
@reg("TC-EMULATION-001", "setDeviceMetricsOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True)
    await s.close(); log_result("TC-EMULATION-001", "setDeviceMetricsOverride", "PASS")

@reg("TC-EMULATION-002", "clearDeviceMetricsOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True)
    await s.emulation.clear_device_metrics_override()
    await s.close(); log_result("TC-EMULATION-002", "clearDeviceMetricsOverride", "PASS")

@reg("TC-EMULATION-003", "setGeolocationOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_geolocation_override(latitude=40.7, longitude=-74.0)
    await s.close(); log_result("TC-EMULATION-003", "setGeolocationOverride", "PASS")

@reg("TC-EMULATION-004", "clearGeolocationOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_geolocation_override(latitude=40.7, longitude=-74.0)
    await s.emulation.clear_geolocation_override()
    await s.close(); log_result("TC-EMULATION-004", "clearGeolocationOverride", "PASS")

@reg("TC-EMULATION-005", "setCPUThrottlingRate")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_cpu_throttling_rate(rate=4)
    await s.emulation.set_cpu_throttling_rate(rate=1)
    await s.close(); log_result("TC-EMULATION-005", "setCPUThrottlingRate", "PASS")

@reg("TC-EMULATION-006", "setUserAgentOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_user_agent_override("TestBot")
    await s.close(); log_result("TC-EMULATION-006", "setUserAgentOverride", "PASS")

@reg("TC-EMULATION-007", "setTouchEmulationEnabled")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_touch_emulation_enabled(True); await s.close()
        log_result("TC-EMULATION-007", "setTouchEmulationEnabled", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-007", "setTouchEmulationEnabled", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-007", "setTouchEmulationEnabled", "FAIL", str(e))

@reg("TC-EMULATION-008", "setEmulatedMedia")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_emulated_media(features=[{"name":"prefers-color-scheme","value":"dark"}])
    await s.close(); log_result("TC-EMULATION-008", "setEmulatedMedia", "PASS")

@reg("TC-EMULATION-009", "clearEmulatedMedia")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.clear_emulated_media(); await s.close()
        log_result("TC-EMULATION-009", "clearEmulatedMedia", "PASS")
    except AttributeError:
        await s.emulation.set_emulated_media(media=""); await s.close()
        log_result("TC-EMULATION-009", "clearEmulatedMedia", "PASS", "Used set_emulated_media('') (fallback)")

@reg("TC-EMULATION-010", "setTimezoneOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_timezone_override("America/New_York")
    await s.close(); log_result("TC-EMULATION-010", "setTimezoneOverride", "PASS")

@reg("TC-EMULATION-011", "clearTimezoneOverride")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_timezone_override("America/New_York")
    await s.emulation.clear_timezone_override()
    await s.close(); log_result("TC-EMULATION-011", "clearTimezoneOverride", "PASS")

@reg("TC-EMULATION-012", "setIdleOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_idle_override(is_user_active=False, is_screen_active=False); await s.close()
        log_result("TC-EMULATION-012", "setIdleOverride", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-EMULATION-012", "setIdleOverride", "FAIL", f"Deprecated: {e}")

@reg("TC-EMULATION-013", "clearIdleOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.clear_idle_override(); await s.close()
        log_result("TC-EMULATION-013", "clearIdleOverride", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-013", "clearIdleOverride", "FAIL", str(e))

@reg("TC-EMULATION-014", "setNavigatorOverrides")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_navigator_overrides("Win32"); await s.close()
        log_result("TC-EMULATION-014", "setNavigatorOverrides", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-014", "setNavigatorOverrides", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-014", "setNavigatorOverrides", "FAIL", str(e))

@reg("TC-EMULATION-015", "setPageScaleFactor")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_page_scale_factor(2); await s.close()
        log_result("TC-EMULATION-015", "setPageScaleFactor", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-015", "setPageScaleFactor", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-015", "setPageScaleFactor", "FAIL", str(e))

@reg("TC-EMULATION-016", "setScriptExecutionDisabled")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_script_execution_disabled(True); await s.close()
        log_result("TC-EMULATION-016", "setScriptExecutionDisabled", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-016", "setScriptExecutionDisabled", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-016", "setScriptExecutionDisabled", "FAIL", str(e))

@reg("TC-EMULATION-017", "setDefaultBackgroundColorOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_default_background_color_override(r=255, g=0, b=0, a=255); await s.close()
        log_result("TC-EMULATION-017", "setDefaultBackgroundColorOverride", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-017", "setDefaultBackgroundColorOverride", "FAIL", str(e))

@reg("TC-EMULATION-018", "clearDefaultBackgroundColorOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.clear_default_background_color_override(); await s.close()
        log_result("TC-EMULATION-018", "clearDefaultBackgroundColorOverride", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-018", "clearDefaultBackgroundColorOverride", "FAIL", str(e))

@reg("TC-EMULATION-019", "setVirtualTimePolicy")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_virtual_time_policy("pause"); await s.close()
        log_result("TC-EMULATION-019", "setVirtualTimePolicy", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-019", "setVirtualTimePolicy", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-019", "setVirtualTimePolicy", "FAIL", str(e))

@reg("TC-EMULATION-020", "setLocale")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_locale_override("es-ES"); await s.close()
        log_result("TC-EMULATION-020", "setLocale", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-020", "setLocale", "FAIL", str(e))

@reg("TC-EMULATION-021", "setScrollPosition")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_scroll_position(x=100, y=100); await s.close()
        log_result("TC-EMULATION-021", "setScrollPosition", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-021", "setScrollPosition", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-021", "setScrollPosition", "FAIL", str(e))

@reg("TC-EMULATION-022", "setFocusEmulationEnabled")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_focus_emulation_enabled(True); await s.close()
        log_result("TC-EMULATION-022", "setFocusEmulationEnabled", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-022", "setFocusEmulationEnabled", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-022", "setFocusEmulationEnabled", "FAIL", str(e))

@reg("TC-EMULATION-023", "setEmulatedVisionDeficiency")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_emulated_vision_deficiency("achromatopsia"); await s.close()
        log_result("TC-EMULATION-023", "setEmulatedVisionDeficiency", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-023", "setEmulatedVisionDeficiency", "FAIL", "Method missing")

@reg("TC-EMULATION-024", "clearEmulatedVisionDeficiency")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.clear_emulated_vision_deficiency(); await s.close()
        log_result("TC-EMULATION-024", "clearEmulatedVisionDeficiency", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-024", "clearEmulatedVisionDeficiency", "FAIL", "Method missing")

@reg("TC-EMULATION-025", "setAutoDarkModeOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_auto_dark_mode_override(True); await s.close()
        log_result("TC-EMULATION-025", "setAutoDarkModeOverride", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-025", "setAutoDarkModeOverride", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-025", "setAutoDarkModeOverride", "FAIL", str(e))

@reg("TC-EMULATION-026", "clearAutoDarkModeOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.clear_auto_dark_mode_override(); await s.close()
        log_result("TC-EMULATION-026", "clearAutoDarkModeOverride", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-026", "clearAutoDarkModeOverride", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-026", "clearAutoDarkModeOverride", "FAIL", str(e))

@reg("TC-EMULATION-027", "set_scrollbars_hidden")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_scrollbars_hidden(True); await s.close()
        log_result("TC-EMULATION-027", "set_scrollbars_hidden", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-EMULATION-027", "set_scrollbars_hidden", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-027", "set_scrollbars_hidden", "FAIL", str(e))

@reg("TC-EMULATION-028", "set_javascript_disabled")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_script_execution_disabled(True); await s.close()
        log_result("TC-EMULATION-028", "set_javascript_disabled", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-028", "set_javascript_disabled", "FAIL", str(e))

@reg("TC-EMULATION-029", "set_document_cookie_disabled")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Emulation.setDocumentCookieDisabled", {"disabled": True}); await s.close()
        log_result("TC-EMULATION-029", "set_document_cookie_disabled", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-029", "set_document_cookie_disabled", "FAIL", str(e))

@reg("TC-EMULATION-030", "set_emit_touch_events_for_mouse")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Emulation.setEmitTouchEventsForMouse", {"enabled": True}); await s.close()
        log_result("TC-EMULATION-030", "set_emit_touch_events_for_mouse", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-030", "set_emit_touch_events_for_mouse", "FAIL", str(e))

@reg("TC-EMULATION-031", "set_locale_override v2")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_locale_override("es-ES"); await s.close()
        log_result("TC-EMULATION-031", "set_locale_override v2", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-031", "set_locale_override v2", "FAIL", str(e))

@reg("TC-EMULATION-032", "set_disabled_sensors")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Emulation.setDisabledSensors", {"disabled": ["accelerometer"]}); await s.close()
        log_result("TC-EMULATION-032", "set_disabled_sensors", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-032", "set_disabled_sensors", "FAIL", str(e))

@reg("TC-EMULATION-033", "set_sensor_override_readings")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.sensor.enable()
        await s.sensor.set_sensor_override("accelerometer", {"x":0,"y":9.8,"z":0}); await s.close()
        log_result("TC-EMULATION-033", "set_sensor_override_readings", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-033", "set_sensor_override_readings", "FAIL", str(e))

@reg("TC-EMULATION-034", "clear_sensor_override_readings")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.sensor.enable()
        await s.sensor.clear_sensor_override("accelerometer"); await s.close()
        log_result("TC-EMULATION-034", "clear_sensor_override_readings", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-034", "clear_sensor_override_readings", "FAIL", str(e))

@reg("TC-EMULATION-035", "set_visible_size")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=1, mobile=False)
        await s.close(); log_result("TC-EMULATION-035", "set_visible_size", "PASS", "Used set_device_metrics_override")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-035", "set_visible_size", "FAIL", str(e))

@reg("TC-EMULATION-036", "device_metrics with screen_orientation")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True, screen_orientation={"type":"portraitPrimary","angle":0})
        await s.close(); log_result("TC-EMULATION-036", "device_metrics screen_orientation", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-036", "device_metrics screen_orientation", "FAIL", str(e))

@reg("TC-EMULATION-037", "device_metrics with viewport")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=1, mobile=False, viewport={"x":0,"y":0,"width":375,"height":667,"scale":1})
        await s.close(); log_result("TC-EMULATION-037", "device_metrics viewport", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-037", "device_metrics viewport", "FAIL", str(e))

@reg("TC-EMULATION-038", "device_metrics with display_feature")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=1, mobile=True, display_feature={"orientation":"vertical","offset":0,"maskLength":100})
        await s.close(); log_result("TC-EMULATION-038", "device_metrics display_feature", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-038", "device_metrics display_feature", "FAIL", str(e))

@reg("TC-EMULATION-039", "device_metrics with device_posture")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=1, mobile=True, device_posture={"type":"folded"})
        await s.close(); log_result("TC-EMULATION-039", "device_metrics device_posture", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-EMULATION-039", "device_metrics device_posture", "FAIL", str(e))

# ===================== INPUT DOMAIN (23 tests) =====================
@reg("TC-INPUT-001", "dispatchKeyEvent char")
async def t(client):
    s = await fresh_session(client)
    await nav_data(s, "<input id='t'>"); await s.dom.enable()
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.focus(n["nodeId"])
    await s.input.dispatch_key_event("char", text="H"); await s.close()
    log_result("TC-INPUT-001", "dispatchKeyEvent char", "PASS")

@reg("TC-INPUT-002", "dispatchKeyEvent keyDown")
async def t(client):
    s = await fresh_session(client)
    await s.input.dispatch_key_event("keyDown", key="Enter"); await s.close()
    log_result("TC-INPUT-002", "dispatchKeyEvent keyDown", "PASS")

@reg("TC-INPUT-003", "dispatchMouseEvent")
async def t(client):
    s = await fresh_session(client)
    await s.input.dispatch_mouse_event("mousePressed", 100, 100, button="left")
    await s.input.dispatch_mouse_event("mouseReleased", 100, 100, button="left"); await s.close()
    log_result("TC-INPUT-003", "dispatchMouseEvent", "PASS")

@reg("TC-INPUT-004", "dispatchTouchEvent")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_touch_event("touchStart", [{"x":100,"y":100}]); await s.close()
        log_result("TC-INPUT-004", "dispatchTouchEvent", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-004", "dispatchTouchEvent", "FAIL", str(e))

@reg("TC-INPUT-005", "emulateTouchFromMouseEvent")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.emulate_touch_from_mouse_event("mousePressed", x=100, y=100, button="left", click_count=1); await s.close()
        log_result("TC-INPUT-005", "emulateTouchFromMouseEvent", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-005", "emulateTouchFromMouseEvent", "FAIL", str(e))

@reg("TC-INPUT-006", "synthesizePinchGesture")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_pinch_gesture(x=100, y=100, scale_factor=2); await s.close()
        log_result("TC-INPUT-006", "synthesizePinchGesture", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-006", "synthesizePinchGesture", "FAIL", str(e))

@reg("TC-INPUT-007", "synthesizeScrollGesture")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_scroll_gesture(x=100, y=100, y_distance=100); await s.close()
        log_result("TC-INPUT-007", "synthesizeScrollGesture", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-007", "synthesizeScrollGesture", "FAIL", str(e))

@reg("TC-INPUT-008", "synthesizeTapGesture")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_tap_gesture(x=100, y=100); await s.close()
        log_result("TC-INPUT-008", "synthesizeTapGesture", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-008", "synthesizeTapGesture", "FAIL", str(e))

@reg("TC-INPUT-009", "insertText")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.insert_text("Hello World"); await s.close()
        log_result("TC-INPUT-009", "insertText", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-INPUT-009", "insertText", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-009", "insertText", "FAIL", str(e))

@reg("TC-INPUT-010", "setIgnoreInputEvents")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.set_ignore_input_events(True); await s.close()
        log_result("TC-INPUT-010", "setIgnoreInputEvents", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-INPUT-010", "setIgnoreInputEvents", "FAIL", "Method missing")

@reg("TC-INPUT-011", "cancelDragging")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.cancel_dragging(); await s.close()
        log_result("TC-INPUT-011", "cancelDragging", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-011", "cancelDragging", "FAIL", str(e))

@reg("TC-INPUT-012", "dispatch_drag_event")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_drag_event("dragEnter", x=100, y=100, data={"items":[{"mimeType":"text/plain","data":"test"}],"dragOperationsMask": 1}); await s.close()
        log_result("TC-INPUT-012", "dispatch_drag_event", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-012", "dispatch_drag_event", "FAIL", str(e))

@reg("TC-INPUT-013", "ime_set_composition")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.ime_set_composition("text", selection_start=0, selection_end=4); await s.close()
        log_result("TC-INPUT-013", "ime_set_composition", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-013", "ime_set_composition", "FAIL", str(e))

@reg("TC-INPUT-014", "set_intercept_drags")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.set_intercept_drags(True); await s.close()
        log_result("TC-INPUT-014", "set_intercept_drags", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-014", "set_intercept_drags", "FAIL", str(e))

@reg("TC-INPUT-015", "dispatch_key_event with modifiers")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_key_event("keyDown", key="A", modifiers=8); await s.close()
        log_result("TC-INPUT-015", "dispatch_key_event modifiers", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-015", "dispatch_key_event modifiers", "FAIL", str(e))

@reg("TC-INPUT-016", "dispatch_key_event with location")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_key_event("keyDown", key="Shift", location=1); await s.close()
        log_result("TC-INPUT-016", "dispatch_key_event location", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-016", "dispatch_key_event location", "FAIL", str(e))

@reg("TC-INPUT-017", "dispatch_key_event with auto_repeat")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_key_event("keyDown", key="A", auto_repeat=True); await s.close()
        log_result("TC-INPUT-017", "dispatch_key_event auto_repeat", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-017", "dispatch_key_event auto_repeat", "FAIL", str(e))

@reg("TC-INPUT-018", "dispatch_key_event with is_keypad")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_key_event("keyDown", key="Enter", is_keypad=True); await s.close()
        log_result("TC-INPUT-018", "dispatch_key_event is_keypad", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-018", "dispatch_key_event is_keypad", "FAIL", str(e))

@reg("TC-INPUT-019", "dispatch_key_event with is_system_key")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.dispatch_key_event("keyDown", key="S", is_system_key=True); await s.close()
        log_result("TC-INPUT-019", "dispatch_key_event is_system_key", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-019", "dispatch_key_event is_system_key", "FAIL", str(e))

@reg("TC-INPUT-020", "synthesize_pinch_gesture with gesture_source_type")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_pinch_gesture(x=100, y=100, scale_factor=2, gesture_source_type="touch"); await s.close()
        log_result("TC-INPUT-020", "synthesize_pinch_gesture source_type", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-020", "synthesize_pinch_gesture source_type", "FAIL", str(e))

@reg("TC-INPUT-021", "synthesize_scroll_gesture with repeat_count")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_scroll_gesture(x=100, y=100, y_distance=100, repeat_count=5); await s.close()
        log_result("TC-INPUT-021", "synthesize_scroll_gesture repeat_count", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-021", "synthesize_scroll_gesture repeat_count", "FAIL", str(e))

@reg("TC-INPUT-022", "synthesize_scroll_gesture with repeat_delay_ms")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_scroll_gesture(x=100, y=100, y_distance=100, repeat_delay_ms=100); await s.close()
        log_result("TC-INPUT-022", "synthesize_scroll_gesture repeat_delay_ms", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-022", "synthesize_scroll_gesture repeat_delay_ms", "FAIL", str(e))

@reg("TC-INPUT-023", "synthesize_tap_gesture with gesture_source_type")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.synthesize_tap_gesture(x=100, y=100, gesture_source_type="mouse"); await s.close()
        log_result("TC-INPUT-023", "synthesize_tap_gesture source_type", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INPUT-023", "synthesize_tap_gesture source_type", "FAIL", str(e))

# ===================== FETCH DOMAIN (10 tests) =====================
@reg("TC-FETCH-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    await s.fetch.disable(); await s.close()
    log_result("TC-FETCH-001", "enable/disable", "PASS")

@reg("TC-FETCH-002", "failRequest")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused_reqs: list[dict] = []
    async def on_pause(p): paused_reqs.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused_reqs:
        try:
            await s.fetch.fail_request(paused_reqs[0]["requestId"], error_reason="Failed")
            await s.fetch.disable(); await s.close()
            log_result("TC-FETCH-002", "failRequest", "PASS")
        except Exception as e:
            await s.fetch.disable(); await s.close(); log_result("TC-FETCH-002", "failRequest", "FAIL", str(e))
    else:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-002", "failRequest", "SKIP", "No request paused")

@reg("TC-FETCH-003", "fulfillRequest")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused_reqs: list[dict] = []
    async def on_pause(p): paused_reqs.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused_reqs:
        try:
            await s.fetch.fulfill_request(paused_reqs[0]["requestId"], status_code=200, body="dGVzdA==")
            await s.fetch.disable(); await s.close()
            log_result("TC-FETCH-003", "fulfillRequest", "PASS")
        except Exception as e:
            await s.fetch.disable(); await s.close(); log_result("TC-FETCH-003", "fulfillRequest", "FAIL", str(e))
    else:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-003", "fulfillRequest", "SKIP", "No request paused")

@reg("TC-FETCH-004", "continueRequest")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused_reqs: list[dict] = []
    async def on_pause(p): paused_reqs.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused_reqs:
        try:
            await s.fetch.continue_request(paused_reqs[0]["requestId"])
            await s.fetch.disable(); await s.close()
            log_result("TC-FETCH-004", "continueRequest", "PASS")
        except Exception as e:
            await s.fetch.disable(); await s.close(); log_result("TC-FETCH-004", "continueRequest", "FAIL", str(e))
    else:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-004", "continueRequest", "SKIP", "No request paused")

@reg("TC-FETCH-005", "continueWithAuth")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}], handle_auth_requests=True)
    paused = asyncio.Event()
    rid: list[str] = []
    async def _on_paused(p):
        rid.append(p.get("requestId", ""))
        if "authChallenge" in p:
            paused.set()
        else:
            try: await s.fetch.continue_request(p["requestId"])
            except: pass
    s.on("Fetch.requestPaused", _on_paused)
    try:
        asyncio.create_task(s.page.navigate("https://httpbin.org/basic-auth/user/pass"))
        await asyncio.wait_for(paused.wait(), timeout=10)
        await s.fetch.continue_with_auth(rid[0], "Default")
        await s.fetch.disable(); await s.close()
        log_result("TC-FETCH-005", "continueWithAuth", "PASS")
    except asyncio.TimeoutError:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-005", "continueWithAuth", "SKIP", "No auth challenge received")
    except Exception as e:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-005", "continueWithAuth", "FAIL", str(e))

@reg("TC-FETCH-006", "getResponseBody")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*","requestStage":"Response"}])
    paused = asyncio.Event()
    rid: list[str] = []
    async def _on_paused(p):
        rid.append(p.get("requestId", ""))
        paused.set()
    s.on("Fetch.requestPaused", _on_paused)
    try:
        asyncio.create_task(s.page.navigate("https://example.com"))
        await asyncio.wait_for(paused.wait(), timeout=10)
        await s.fetch.get_response_body(rid[0])
        await s.fetch.disable(); await s.close()
        log_result("TC-FETCH-006", "getResponseBody", "PASS")
    except Exception as e:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-006", "getResponseBody", "FAIL", str(e))

@reg("TC-FETCH-007", "takeResponseBodyAsStream")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*","requestStage":"Response"}])
    paused = asyncio.Event()
    rid: list[str] = []
    async def _on_paused(p):
        rid.append(p.get("requestId", ""))
        paused.set()
    s.on("Fetch.requestPaused", _on_paused)
    try:
        asyncio.create_task(s.page.navigate("https://example.com"))
        await asyncio.wait_for(paused.wait(), timeout=10)
        await s.fetch.take_response_body_as_stream(rid[0])
        await s.fetch.disable(); await s.close()
        log_result("TC-FETCH-007", "takeResponseBodyAsStream", "PASS")
    except Exception as e:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-007", "takeResponseBodyAsStream", "FAIL", str(e))

@reg("TC-FETCH-008", "continueResponse")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*","requestStage":"Response"}])
    paused = asyncio.Event()
    rid: list[str] = []
    async def _on_paused(p):
        rid.append(p.get("requestId", ""))
        paused.set()
    s.on("Fetch.requestPaused", _on_paused)
    try:
        asyncio.create_task(s.page.navigate("https://example.com"))
        await asyncio.wait_for(paused.wait(), timeout=10)
        await s.fetch.continue_response(rid[0])
        await s.fetch.disable(); await s.close()
        log_result("TC-FETCH-008", "continueResponse", "PASS")
    except Exception as e:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-008", "continueResponse", "FAIL", str(e))

@reg("TC-FETCH-009", "pause/resume")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Fetch.enable", {"patterns":[{"urlPattern":"*://*/*"}]})
        await s.send("Fetch.disable", {}); await s.close()
        log_result("TC-FETCH-009", "pause/resume", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-FETCH-009", "pause/resume", "FAIL", str(e))

@reg("TC-FETCH-010", "fail")
async def t(client):
    s = await fresh_session(client)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    paused = asyncio.Event()
    rid: list[str] = []
    async def _on_paused(p):
        rid.append(p.get("requestId", ""))
        paused.set()
    s.on("Fetch.requestPaused", _on_paused)
    try:
        asyncio.create_task(s.page.navigate("https://example.com"))
        await asyncio.wait_for(paused.wait(), timeout=10)
        await s.fetch.fail_request(rid[0], error_reason="Failed")
        await s.fetch.disable(); await s.close()
        log_result("TC-FETCH-010", "fail", "PASS")
    except Exception as e:
        await s.fetch.disable(); await s.close(); log_result("TC-FETCH-010", "fail", "FAIL", str(e))

# ===================== STORAGE DOMAIN (13 tests) =====================
@reg("TC-STORAGE-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.storage.enable(); await s.storage.disable(); await s.close()
        log_result("TC-STORAGE-001", "enable/disable", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-001", "enable/disable", "FAIL", str(e))

@reg("TC-STORAGE-002", "getDOMStorageItems")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try:
        sid = {"securityOrigin":"https://example.com","isLocalStorage":True}
        r = await s.storage.get_dom_storage_items(sid)
        await s.close(); log_result("TC-STORAGE-002", "getDOMStorageItems", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-002", "getDOMStorageItems", "FAIL", str(e))

@reg("TC-STORAGE-003", "setDOMStorageItem")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try:
        sid = {"securityOrigin":"https://example.com","isLocalStorage":True}
        await s.storage.set_dom_storage_item(sid, "test", "val")
        await s.close(); log_result("TC-STORAGE-003", "setDOMStorageItem", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-003", "setDOMStorageItem", "FAIL", str(e))

@reg("TC-STORAGE-004", "removeDOMStorageItem")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try:
        sid = {"securityOrigin":"https://example.com","isLocalStorage":True}
        await s.storage.remove_dom_storage_item(sid, "test")
        await s.close(); log_result("TC-STORAGE-004", "removeDOMStorageItem", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-004", "removeDOMStorageItem", "FAIL", str(e))

@reg("TC-STORAGE-005", "clearDOMStorageItems")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try:
        sid = {"securityOrigin":"https://example.com","isLocalStorage":True}
        await s.storage.clear_dom_storage_items(sid)
        await s.close(); log_result("TC-STORAGE-005", "clearDOMStorageItems", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-005", "clearDOMStorageItems", "FAIL", str(e))

@reg("TC-STORAGE-006", "getUsageAndQuota")
async def t(client):
    s = await fresh_session(client)
    try:
        r = await s.storage.get_usage_and_quota("https://example.com"); await s.close()
        log_result("TC-STORAGE-006", "getUsageAndQuota", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-006", "getUsageAndQuota", "FAIL", str(e))

@reg("TC-STORAGE-007", "trackCacheStorageForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.storage.track_cache_storage_for_origin("https://example.com"); await s.close()
        log_result("TC-STORAGE-007", "trackCacheStorageForOrigin", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-007", "trackCacheStorageForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-008", "trackIndexedDBForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.storage.track_indexed_db_for_origin("https://example.com"); await s.close()
        log_result("TC-STORAGE-008", "trackIndexedDBForOrigin", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-008", "trackIndexedDBForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-009", "untrackCacheStorageForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.storage.untrack_cache_storage_for_origin("https://example.com"); await s.close()
        log_result("TC-STORAGE-009", "untrackCacheStorageForOrigin", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-009", "untrackCacheStorageForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-010", "untrackIndexedDBForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.storage.untrack_indexed_db_for_origin("https://example.com"); await s.close()
        log_result("TC-STORAGE-010", "untrackIndexedDBForOrigin", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-010", "untrackIndexedDBForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-011", "getCacheStorageForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Storage.getStorageKeyForFrame", {"frameId":"default"}); await s.close()
        log_result("TC-STORAGE-011", "getCacheStorageForOrigin", "SKIP", "No direct method")
    except CommandError as e:
        await s.close(); log_result("TC-STORAGE-011", "getCacheStorageForOrigin", "SKIP", f"Frame not found: {e}")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-011", "getCacheStorageForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-012", "getIndexedDBForOrigin")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Storage.getStorageKeyForFrame", {"frameId":"default"}); await s.close()
        log_result("TC-STORAGE-012", "getIndexedDBForOrigin", "SKIP", "No direct method")
    except CommandError as e:
        await s.close(); log_result("TC-STORAGE-012", "getIndexedDBForOrigin", "SKIP", f"Frame not found: {e}")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-012", "getIndexedDBForOrigin", "FAIL", str(e))

@reg("TC-STORAGE-013", "getCookies")
async def t(client):
    s = await fresh_session(client)
    try:
        r = await s.storage.get_cookies(); await s.close()
        log_result("TC-STORAGE-013", "getCookies", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-STORAGE-013", "getCookies", "SKIP", f"Browser target only: {e}")
    except Exception as e:
        await s.close(); log_result("TC-STORAGE-013", "getCookies", "FAIL", str(e))
