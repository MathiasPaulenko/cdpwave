# Quickstart

This tutorial takes about 10 minutes. You'll learn to launch Chrome, navigate, evaluate JavaScript, listen to events, manage multiple tabs, and clean up.

## Install

```bash
pip install cdpwave
```

cdpwave detects Chrome, Edge, Brave, or Chromium on your system. No browser download needed.

## First script

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.page.enable()

        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        print(result["result"]["value"])  # "Example Domain"

        await session.close()

asyncio.run(main())
```

Run it:

```bash
python script.py
```

## Events

Listen to page events with async handlers:

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()

        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)
        print("Page loaded!")

        await session.close()

asyncio.run(main())
```

## Multi-tab

Open multiple tabs concurrently — all share a single WebSocket:

```python
import asyncio
from cdpwave import CDPClient

async def fetch_title(client: CDPClient, url: str) -> str:
    session = await client.new_page(url)
    result = await session.runtime.evaluate("document.title", return_by_value=True)
    title = result["result"]["value"]
    await session.close()
    return title

async def main() -> None:
    urls = ["https://example.com", "https://www.python.org"]

    async with await CDPClient.launch(headless=True) as client:
        tasks = [fetch_title(client, url) for url in urls]
        titles = await asyncio.gather(*tasks)
        for url, title in zip(urls, titles, strict=True):
            print(f"{url} -> {title}")

asyncio.run(main())
```

## Cleanup

`CDPClient` and `CDPSession` both support `async with`. When the context exits, everything is cleaned up — WebSocket closed, browser terminated, temp directory removed:

```python
async with await CDPClient.launch(headless=True) as client:
    async with await client.new_page() as session:
        await session.page.navigate("https://example.com")
    # session.close() called automatically
# client.close() called automatically — browser terminated
```

Even if an exception occurs inside the `async with` block, cleanup is guaranteed.

## What's next?

- [Guide: Browser Launch](guide/browser-launch.md) — launch options, connecting to existing browsers
- [Guide: Events](guide/events.md) — handler isolation, subscriptions, common events
- [Guide: Emulation & Input](guide/emulation-input.md) — device metrics, keyboard, mouse, touch
- [Guide: Fetch & Network Interception](guide/fetch-network.md) — intercept, mock, block requests
- [Guide: Performance & Profiling](guide/performance-profiling.md) — CPU profiling, heap snapshots, tracing
- [Guide: Debugging](guide/debugging.md) — breakpoints, stepping, variable inspection
- [Guide: Storage & Cache](guide/storage-cache.md) — cookies, IndexedDB, Cache API
- [Guide: Advanced Domains](guide/advanced-domains.md) — Accessibility, CSS, Overlay, Security, WebAuthn, DOMSnapshot, DOMStorage, FedCM, WebAudio, and more
- [Cookbook: Escape Hatch](cookbook/escape-hatch.md) — send raw CDP commands
- [API Reference](api/client.md) — full auto-generated API docs for all 60 domains
