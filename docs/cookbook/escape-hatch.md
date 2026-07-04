# Escape Hatch

cdpwave covers all 48 CDP domains with 386 typed methods. For any CDP command
that doesn't have a dedicated wrapper — or for experimental/new commands —
use `session.send()` — the escape hatch.

## Basic usage

```python
result = await session.send("Emulation.setDeviceMetricsOverride", {
    "width": 375,
    "height": 812,
    "deviceScaleFactor": 3,
    "mobile": True,
})
```

`send()` takes a CDP method name and an optional params dict. It returns the
raw response dict.

## No params

```python
await session.send("Page.stopLoading")
```

Or pass `None` explicitly:

```python
await session.send("Page.stopLoading", None)
```

## When to use the escape hatch

- **Experimental commands** — new CDP methods not yet wrapped
- **Rarely used commands** — niche commands that don't warrant a wrapper
- **Custom params** — when you need raw control over the params dict
- **Quick prototyping** — test a CDP command before wrapping it

## Emulation example

Set device metrics, take a mobile screenshot, then clear:

```python
await session.emulation.set_device_metrics_override(
    width=375, height=812, device_scale_factor=3, mobile=True,
)

screenshot = await session.page.capture_screenshot(format="png")

await session.emulation.clear_device_metrics_override()
```

## Input simulation

Type text character by character:

```python
for char in "cdpwave":
    await session.input.dispatch_key_event(
        type_="char", text=char,
    )
```

Press Enter:

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

## Performance tracing

```python
await session.performance.enable()
metrics = await session.performance.get_metrics()
for metric in metrics["metrics"]:
    print(f"{metric['name']}: {metric['value']}")
```

## Error handling

`send()` raises `CommandError` if the CDP method doesn't exist or the params
are invalid:

```python
from cdpwave import CommandError

try:
    await session.send("NonExistent.method")
except CommandError as e:
    print(f"CDP error: {e.code} {e.message}")
```

## Typed wrappers vs escape hatch

| Aspect | Typed wrapper | Escape hatch |
|---|---|---|
| Type hints | Full (params + return) | None (raw dicts) |
| IDE autocomplete | Yes | No |
| Validation | Pythonic params | Manual dict |
| Documentation | Docstrings | CDP spec |
| Coverage | 386 methods | All CDP commands |

Prefer typed wrappers when available. Use `send()` only for commands without
a wrapper or when you need raw control.
