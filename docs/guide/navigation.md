# Navigation

## Navigate to a URL

```python
await page.page.enable()
await page.page.navigate("https://example.com")
```

`Page.navigate` returns a dict with `frameId` and `loaderId`:

```python
result = await page.page.navigate("https://example.com")
print(result["frameId"])
```

## Navigate with referrer

```python
await page.page.navigate(
    "https://example.com",
    referrer="https://google.com",
)
```

## Reload

```python
await page.page.reload()
```

Reload with cache bypass:

```python
await page.page.reload(ignore_cache=True)
```

## Stop loading

```python
await page.page.stop()
```

Or via the escape hatch:

```python
await page.send("Page.stopLoading")
```

## Wait strategies

cdpwave doesn't include auto-wait in v1. Use events with `asyncio` primitives:

### Wait for page load

```python
import asyncio

loaded = asyncio.Event()

async def on_load(_: dict) -> None:
    loaded.set()

page.on("Page.loadEventFired", on_load)
await page.page.navigate("https://example.com")
await asyncio.wait_for(loaded.wait(), timeout=10.0)
```

### Wait for a condition

```python
for _ in range(20):
    await asyncio.sleep(0.5)
    result = await page.runtime.evaluate(
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

page.on("Network.requestWillBeSent", on_request)
page.on("Network.responseReceived", on_response)
await page.page.navigate("https://example.com")
await asyncio.wait_for(idle.wait(), timeout=15.0)
```
