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
        page = await client.new_page("https://example.com")
        await page.page.enable()

        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        print(result["result"]["value"])  # "Example Domain"

        await page.close()

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
        page = await client.new_page()
        await page.page.enable()

        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        page.on("Page.loadEventFired", on_load)
        await page.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)
        print("Page loaded!")

        await page.close()

asyncio.run(main())
```

## Multi-tab

Open multiple tabs concurrently — all share a single WebSocket:

```python
import asyncio
from cdpwave import CDPClient

async def fetch_title(client: CDPClient, url: str) -> str:
    page = await client.new_page(url)
    result = await page.runtime.evaluate("document.title", return_by_value=True)
    title = result["result"]["value"]
    await page.close()
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
    async with await client.new_page() as page:
        await page.page.navigate("https://example.com")
    # page.close() called automatically
# client.close() called automatically — browser terminated
```

Even if an exception occurs inside the `async with` block, cleanup is guaranteed.

## What's next?

- [Guide: Browser Launch](guide/browser-launch.md) — launch options, connecting to existing browsers
- [Guide: Events](guide/events.md) — handler isolation, subscriptions, common events
- [Cookbook: Escape Hatch](cookbook/escape-hatch.md) — send raw CDP commands for uncovered domains
- [API Reference](api/client.md) — full auto-generated API docs
