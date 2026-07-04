# Emulation & Input

cdpwave provides full coverage of the `Emulation` and `Input` CDP domains,
letting you simulate devices, throttle CPU, disable features, and dispatch
input events.

## Emulation

### Device metrics

Simulate a mobile viewport:

```python
await session.emulation.set_device_metrics_override(
    width=375,
    height=812,
    device_scale_factor=3,
    mobile=True,
)

screenshot = await session.page.capture_screenshot(format="png")

await session.emulation.clear_device_metrics_override()
```

### CPU throttling

Simulate a slow CPU (4x slowdown):

```python
await session.emulation.set_cpu_throttling_rate(rate=4.0)
# ... run your tests ...
await session.emulation.set_cpu_throttling_rate(rate=1.0)
```

### Disable JavaScript

```python
await session.emulation.set_javascript_disabled(True)
# JS is now disabled — all scripts will not execute
await session.page.reload()
# ... inspect the no-JS rendering ...
await session.emulation.set_javascript_disabled(False)
```

### Hide scrollbars

```python
await session.emulation.set_scrollbars_hidden(True)
screenshot = await session.page.capture_screenshot()
await session.emulation.set_scrollbars_hidden(False)
```

### Auto dark mode

```python
await session.emulation.set_auto_dark_mode_override(True)
# Page now renders in dark mode regardless of system setting
```

### Geolocation

```python
await session.emulation.set_geolocation_override(
    latitude=37.7749,
    longitude=-122.4194,
    accuracy=100,
)
```

### Timezone

```python
await session.emulation.set_timezone_override("America/Los_Angeles")
```

### Touch events

Enable touch event emulation for mouse:

```python
await session.emulation.set_emit_touch_events_for_mouse(
    enabled=True,
    configuration="mobile",
)
```

### Cookie disable

```python
await session.emulation.set_document_cookie_disabled(True)
# document.cookie will now return empty string
```

## Input

### Keyboard

Type a string:

```python
for char in "Hello, World!":
    await session.input.dispatch_key_event(
        type_="char",
        text=char,
    )
```

Press a key:

```python
await session.input.dispatch_key_event(
    type_="keyDown",
    key="Enter",
    code="Enter",
    windows_virtual_key_code=13,
)
await session.input.dispatch_key_event(
    type_="keyUp",
    key="Enter",
    code="Enter",
    windows_virtual_key_code=13,
)
```

Key combinations (Ctrl+C):

```python
await session.input.dispatch_key_event(
    type_="keyDown",
    key="ControlLeft",
    code="ControlLeft",
    windows_virtual_key_code=162,
)
await session.input.dispatch_key_event(
    type_="keyDown",
    key="c",
    code="KeyC",
    windows_virtual_key_code=67,
    modifiers=2,  # 2 = Control
)
await session.input.dispatch_key_event(
    type_="keyUp",
    key="c",
    code="KeyC",
    windows_virtual_key_code=67,
)
await session.input.dispatch_key_event(
    type_="keyUp",
    key="ControlLeft",
    code="ControlLeft",
    windows_virtual_key_code=162,
)
```

### Mouse

Click at coordinates:

```python
await session.input.dispatch_mouse_event(
    type_="mousePressed",
    x=100,
    y=200,
    button="left",
    click_count=1,
)
await session.input.dispatch_mouse_event(
    type_="mouseReleased",
    x=100,
    y=200,
    button="left",
    click_count=1,
)
```

Double-click:

```python
await session.input.dispatch_mouse_event(
    type_="mousePressed",
    x=100,
    y=200,
    button="left",
    click_count=2,
)
await session.input.dispatch_mouse_event(
    type_="mouseReleased",
    x=100,
    y=200,
    button="left",
    click_count=2,
)
```

Right-click:

```python
await session.input.dispatch_mouse_event(
    type_="mousePressed",
    x=100,
    y=200,
    button="right",
    click_count=1,
)
await session.input.dispatch_mouse_event(
    type_="mouseReleased",
    x=100,
    y=200,
    button="right",
    click_count=1,
)
```

Mouse wheel scroll:

```python
await session.input.dispatch_mouse_event(
    type_="mouseWheel",
    x=100,
    y=200,
    delta_x=0,
    delta_y=300,
)
```

### Touch

Tap:

```python
await session.input.dispatch_touch_event(
    type_="touchStart",
    touch_points=[{"x": 100, "y": 200}],
)
await session.input.dispatch_touch_event(
    type_="touchEnd",
    touch_points=[],
)
```

### Drag and drop

```python
await session.input.dispatch_drag_event(
    type_="dragEnter",
    x=100,
    y=200,
    data={"items": [{"mimeType": "text/plain", "data": "Hello"}]},
)
await session.input.dispatch_drag_event(
    type_="drop",
    x=200,
    y=300,
    data={"items": [{"mimeType": "text/plain", "data": "Hello"}]},
)
```

### Pinch zoom

```python
await session.input.emulate_touch_from_mouse_event(
    type_="mouseMoved",
    x=200,
    y=300,
    button="none",
    delta_x=0,
    delta_y=0,
    modifiers=0,
    timestamp=0,
)
```

## Sensors

Override accelerometer readings:

```python
await session.sensor.set_sensor_override(
    type_="accelerometer",
    reading={"x": 0, "y": 9.8, "z": 0},
)
```

## Device orientation

```python
await session.device_orientation.set_device_orientation_override(
    alpha=0,
    beta=90,
    gamma=0,
)
```
