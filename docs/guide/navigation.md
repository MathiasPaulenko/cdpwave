# Navigation

## Navigate to a URL

```python
await session.page.enable()
await session.page.navigate("https://example.com")
```

`Page.navigate` returns a dict with `frameId` and `loaderId`:

```python
result = await session.page.navigate("https://example.com")
print(result["frameId"])
```

## Navigate with referrer

```python
await session.page.navigate(
    "https://example.com",
    referrer="https://google.com",
)
```

## Reload

```python
await session.page.reload()
```

Reload with cache bypass:

```python
await session.page.reload(ignore_cache=True)
```

## Stop loading

```python
await session.page.stop()
```

Or via the escape hatch:

```python
await session.send("Page.stopLoading")
```

## Wait strategies

cdpwave doesn't include auto-wait in v1. Use events with `asyncio` primitives:

### Wait for page load

```python
import asyncio

loaded = asyncio.Event()

async def on_load(_: dict) -> None:
    loaded.set()

session.on("Page.loadEventFired", on_load)
await session.page.navigate("https://example.com")
await asyncio.wait_for(loaded.wait(), timeout=10.0)
```

### Wait for a condition

```python
for _ in range(20):
    await asyncio.sleep(0.5)
    result = await session.runtime.evaluate(
        "document.title", return_by_value=True
    )
    title = result.get("result", {}).get("value", "")
    if title:
        break
```

### Wait for network idle

```python
pending = 0
idle = asyncio.Event()

async def on_request(_: dict) -> None:
    nonlocal pending
    pending += 1

async def on_response(_: dict) -> None:
    nonlocal pending
    pending -= 1
    if pending == 0:
        idle.set()

session.on("Network.requestWillBeSent", on_request)
session.on("Network.responseReceived", on_response)
await session.page.navigate("https://example.com")
await asyncio.wait_for(idle.wait(), timeout=15.0)
```
