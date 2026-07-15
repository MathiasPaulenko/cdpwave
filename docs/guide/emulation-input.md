# Emulation & Input

cdpwave provides full coverage of the `Emulation` and `Input` CDP domains,
letting you simulate devices, throttle CPU, disable features, and dispatch
input events — everything needed to test responsive layouts, simulate
mobile conditions, and automate user interaction.

## Emulation

The `Emulation` domain overrides browser behavior and appearance. These
overrides persist until you clear them or close the session. Each
override is independent — you can combine device metrics with CPU
throttling, timezone, and geolocation simultaneously.

### Device metrics

Simulate a mobile viewport by overriding width, height, device scale
factor, and mobile flag:

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

Parameters:

- **`width`** — viewport width in CSS pixels.
- **`height`** — viewport height in CSS pixels.
- **`device_scale_factor`** — pixel ratio (1 = standard, 2 = Retina,
  3 = high-DPI mobile).
- **`mobile`** — whether the viewport is a mobile device. Affects
  `viewport` meta tag behavior and touch event handling.

!!! tip "Always clear overrides"
    Call `clear_device_metrics_override()` when done to restore the
    browser's default viewport. This is especially important when
    reusing a session across multiple test cases.

### CPU throttling

Simulate a slow CPU to test performance under load:

```python
await session.emulation.set_cpu_throttling_rate(rate=4.0)
# ... run your tests ...
await session.emulation.set_cpu_throttling_rate(rate=1.0)
```

`rate` is a multiplier — `4.0` means tasks take 4x longer. This helps
reproduce performance issues that only appear on slow devices.

### Disable JavaScript

Test how a page renders without JavaScript:

```python
await session.emulation.set_javascript_disabled(True)
await session.page.reload()
# ... inspect the no-JS rendering ...
await session.emulation.set_javascript_disabled(False)
```

### Hide scrollbars

Useful for clean screenshots without scrollbar artifacts:

```python
await session.emulation.set_scrollbars_hidden(True)
screenshot = await session.page.capture_screenshot()
await session.emulation.set_scrollbars_hidden(False)
```

### Auto dark mode

Force dark mode regardless of the system setting:

```python
await session.emulation.set_auto_dark_mode_override(True)
# Page now renders in dark mode
```

### Geolocation

Override the browser's geolocation. Useful for testing location-based
features:

```python
await session.emulation.set_geolocation_override(
    latitude=37.7749,
    longitude=-122.4194,
    accuracy=100,
)
```

!!! note "Permissions"
    The page must have geolocation permission granted. Use
    `client.browser.grant_permissions(permissions=["geolocation"])`
    to grant it programmatically.

### Timezone

Override the system timezone:

```python
await session.emulation.set_timezone_override("America/Los_Angeles")
```

This affects `Date` objects, `Intl` APIs, and any timezone-dependent
JavaScript.

### Touch events

Enable touch event emulation for mouse interactions:

```python
await session.emulation.set_emit_touch_events_for_mouse(
    enabled=True,
    configuration="mobile",
)
```

`configuration` can be `"mobile"` or `"desktop"`. This makes mouse
events also fire touch events, useful for testing touch handlers on
a desktop browser.

### Cookie disable

Prevent `document.cookie` from working:

```python
await session.emulation.set_document_cookie_disabled(True)
# document.cookie will now return empty string
```

## Input

The `Input` domain dispatches raw input events to the page. These are
low-level events — they go directly to the browser's input pipeline,
not through JavaScript. This means they trigger full event chains
including default actions.

### Key event types

| Type | Description | When to use |
|---|---|---|
| `keyDown` | Key pressed down | Start of a key press |
| `keyUp` | Key released | End of a key press |
| `char` | Character input | Typing text (one per char) |
| `rawKeyDown` | Raw key down (no IME) | Non-character keys |

### Modifier flags

| Value | Modifier |
|---|---|
| `0` | None |
| `1` | Alt |
| `2` | Control |
| `4` | Meta (Cmd on macOS) |
| `8` | Shift |

### Keyboard

Type a string character by character:

```python
for char in "Hello, World!":
    await session.input.dispatch_key_event(
        type_="char",
        text=char,
    )
```

!!! tip "char vs keyDown"
    Use `char` events for typing text — they generate the correct
    `keypress` events and handle IME properly. Use `keyDown`/`keyUp`
    for non-character keys like Enter, Escape, or arrow keys.

Press a key (Enter):

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
# Press Control
await session.input.dispatch_key_event(
    type_="keyDown",
    key="ControlLeft",
    code="ControlLeft",
    windows_virtual_key_code=162,
)
# Press C while Control is held
await session.input.dispatch_key_event(
    type_="keyDown",
    key="c",
    code="KeyC",
    windows_virtual_key_code=67,
    modifiers=2,  # 2 = Control
)
# Release C
await session.input.dispatch_key_event(
    type_="keyUp",
    key="c",
    code="KeyC",
    windows_virtual_key_code=67,
)
# Release Control
await session.input.dispatch_key_event(
    type_="keyUp",
    key="ControlLeft",
    code="ControlLeft",
    windows_virtual_key_code=162,
)
```

### Mouse

Mouse events use CSS pixel coordinates relative to the viewport.

| Parameter | Description |
|---|---|
| `x`, `y` | Coordinates in CSS pixels |
| `button` | `"left"`, `"right"`, `"middle"`, or `"none"` |
| `click_count` | Number of clicks (1 = single, 2 = double) |
| `delta_x`, `delta_y` | Scroll deltas (for `mouseWheel`) |

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

!!! warning "Always pair press and release"
    A `mousePressed` without a matching `mouseReleased` leaves the
    browser in a pressed state, which can cause unexpected behavior
    in subsequent interactions.

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

Right-click (context menu):

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
    delta_y=300,  # positive = scroll down
)
```

### Touch

Touch events use a list of touch points. Each point has `x`, `y`, and
optional `radiusX`, `radiusY`, `force`, `id`.

Tap (touchStart + touchEnd):

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

Drag events require `data` with `items` — each item has `mimeType`
and `data`:

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

Emulate a pinch-to-zoom gesture via mouse:

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

Override sensor readings to test sensor-dependent web APIs:

```python
await session.sensor.set_sensor_override(
    type_="accelerometer",
    reading={"x": 0, "y": 9.8, "z": 0},
)
```

Supported sensor types: `"accelerometer"`, `"gyroscope"`,
`"magnetometer"`, `"ambient-light-sensor"`, `"proximity"`.

## Device orientation

Override device orientation (alpha = z-axis rotation, beta = x-axis,
gamma = y-axis):

```python
await session.device_orientation.set_device_orientation_override(
    alpha=0,
    beta=90,
    gamma=0,
)
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()

        # Emulate iPhone 12
        await session.emulation.set_device_metrics_override(
            width=390,
            height=844,
            device_scale_factor=3,
            mobile=True,
        )
        await session.emulation.set_geolocation_override(
            latitude=37.7749,
            longitude=-122.4194,
            accuracy=100,
        )
        await session.emulation.set_timezone_override("America/Los_Angeles")

        # Navigate
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        # Click a button
        await session.input.dispatch_mouse_event(
            type_="mousePressed",
            x=195,
            y=400,
            button="left",
            click_count=1,
        )
        await session.input.dispatch_mouse_event(
            type_="mouseReleased",
            x=195,
            y=400,
            button="left",
            click_count=1,
        )

        # Take a mobile screenshot
        import base64
        screenshot = await session.page.capture_screenshot(format="png")
        with open("mobile.png", "wb") as f:
            f.write(base64.b64decode(screenshot["data"]))

        # Clean up overrides
        await session.emulation.clear_device_metrics_override()

        await session.close()

asyncio.run(main())
```
