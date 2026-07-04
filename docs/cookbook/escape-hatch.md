# Escape Hatch

cdpwave covers 7 CDP domains in v1: Page, Runtime, Network, DOM, Target, Log, and Console. For any other CDP domain, use `session.send()` — the escape hatch.

## Basic usage

```python
result = await page.send("Emulation.setDeviceMetricsOverride", {
    "width": 375,
    "height": 812,
    "deviceScaleFactor": 3,
    "mobile": True,
})
```

`send()` takes a CDP method name and an optional params dict. It returns the raw response dict.

## No params

```python
await page.send("Page.stopLoading")
```

Or pass `None` explicitly:

```python
await page.send("Page.stopLoading", None)
```

## Emulation example

Set device metrics, take a mobile screenshot, then clear:

```python
await page.send("Emulation.setDeviceMetricsOverride", {
    "width": 375,
    "height": 812,
    "deviceScaleFactor": 3,
    "mobile": True,
})

screenshot = await page.page.capture_screenshot(format="png")

await page.send("Emulation.clearDeviceMetricsOverride")
```

## Input simulation

Type text character by character:

```python
for char in "cdpwave":
    await page.send("Input.dispatchKeyEvent", {
        "type": "char",
        "text": char,
    })
```

Press Enter:

```python
await page.send("Input.dispatchKeyEvent", {
    "type": "keyDown",
    "key": "Enter",
    "code": "Enter",
    "windowsVirtualKeyCode": 13,
})
await page.send("Input.dispatchKeyEvent", {
    "type": "keyUp",
    "key": "Enter",
    "code": "Enter",
    "windowsVirtualKeyCode": 13,
})
```

## Performance tracing

```python
await page.send("Performance.enable")
metrics = await page.send("Performance.getMetrics")
for metric in metrics["metrics"]:
    print(f"{metric['name']}: {metric['value']}")
```

## Error handling

`send()` raises `CommandError` if the CDP method doesn't exist or the params are invalid:

```python
from cdpwave import CommandError

try:
    await page.send("NonExistent.method")
except CommandError as e:
    print(f"CDP error: {e.code} {e.message}")
```

## When to use the escape hatch

- **Emulation** — device metrics, geolocation, timezone
- **Input** — keyboard, mouse, touch events
- **Performance** — metrics, tracing
- **Fetch** — request interception (v1.1+ will cover this)
- **Animation** — playback rate control
- **Any new CDP domain** — before it gets a typed wrapper
