# Practical Migration Guide

This guide helps you migrate from pyppeteer, pychrome, or raw CDP
to cdpwave. It covers the most common automation patterns.

## Quick start

### Async (recommended)

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.wait_for_load_state("load")
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True,
        )
        print(result["result"]["value"])

asyncio.run(main())
```

### Sync (for simple scripts)

```python
from cdpwave.sync import SyncCDPClient

with SyncCDPClient.launch(headless=True) as client:
    page = client.new_page("https://example.com")
    page.run(page.wait_for_load_state("load"))
    result = page.run(page.runtime.evaluate(
        "document.title", return_by_value=True,
    ))
    print(result["result"]["value"])
```

## Common patterns

### Navigate and wait

| Pattern | Code |
|---|---|
| Navigate + wait for load | `await session.page.navigate(url)` then `await session.wait_for_load_state("load")` |
| Wait for navigation to URL | `await session.wait_for_navigation(url="example.com")` |
| Wait for DOMContentLoaded | `await session.wait_for_load_state("DOMContentLoaded")` |
| Wait for network idle | `await session.wait_for_network_idle(idle_time=0.5)` |

### Find and interact with elements

```python
# Wait for a selector
node_id = await session.wait_for_selector("#submit-btn", timeout=10)

# Get attributes
attrs = await session.dom.get_attributes(node_id)

# Click via input domain
await session.input.dispatch_mouse_event(
    "mousePressed", x=100, y=100, button="left", click_count=1,
)
await session.input.dispatch_mouse_event(
    "mouseReleased", x=100, y=100, button="left", click_count=1,
)

# Type text
await session.input.insert_text("Hello, world!")
```

### Screenshots and PDFs

```python
# Screenshot
result = await session.page.capture_screenshot(format="png")
with open("screenshot.png", "wb") as f:
    import base64
    f.write(base64.b64decode(result["data"]))

# PDF
result = await session.page.print_to_pdf()
with open("page.pdf", "wb") as f:
    import base64
    f.write(base64.b64decode(result["data"]))
```

### Cookies

```python
# Get cookies
result = await session.network.get_cookies(urls=["https://example.com"])
cookies = result["cookies"]

# Set cookie
await session.network.set_cookie(
    name="session", value="abc123",
    domain="example.com", path="/",
)
```

### Request interception

```python
# Enable Fetch domain
await session.fetch.enable(
    patterns=[{"urlPattern": "*", "requestStage": "Request"}],
)

# Handle requests
async def on_request(params: dict) -> None:
    request_id = params["requestId"]
    await session.fetch.continue_request(request_id)

session.on("Fetch.requestPaused", on_request)
```

### Console and errors

```python
async def on_console(params: dict) -> None:
    print(f"Console: {params['args']}")

async def on_exception(params: dict) -> None:
    print(f"Exception: {params['exceptionDetails']}")

session.on("Runtime.consoleAPICalled", on_console)
session.on("Runtime.exceptionThrown", on_exception)
```

### Device emulation

```python
await session.emulation.set_device_metrics_override(
    width=375, height=667, device_scale_factor=2, mobile=True,
)
```

## Migration cheat sheet

| Task | pyppeteer | pychrome | cdpwave |
|---|---|---|---|
| Launch | `await launch()` | `pychrome.Browser(url=...)` | `await CDPClient.launch()` or `await CDPClient.connect()` |
| New page | `await browser.newPage()` | `browser.new_tab()` | `await client.new_page()` |
| Navigate | `await page.goto(url)` | `tab.Page.navigate(url=...)` | `await session.page.navigate(url)` |
| Evaluate JS | `await page.evaluate(expr)` | `tab.Runtime.evaluate(expression=...)` | `await session.runtime.evaluate(expr, return_by_value=True)` |
| Screenshot | `await page.screenshot()` | `tab.Page.captureScreenshot()` | `await session.page.capture_screenshot()` |
| PDF | `await page.pdf()` | — | `await session.page.print_to_pdf()` |
| Wait selector | `await page.waitForSelector(sel)` | `tab.wait(timeout)` | `await session.wait_for_selector(sel)` |
| Wait load | `await page.waitForNavigation()` | `tab.wait(timeout)` | `await session.wait_for_load_state("load")` |
| Get cookies | `await page.cookies()` | `tab.Network.getCookies()` | `await session.network.get_cookies()` |
| Set cookie | `await page.setCookie(...)` | `tab.Network.setCookie(...)` | `await session.network.set_cookie(...)` |
| Event listener | `page.on('console', cb)` | `tab.set_listener("Page.loadEventFired", cb)` | `session.on("Page.loadEventFired", async_cb)` |
| Close page | `await page.close()` | `tab.stop()` | `await session.close()` |
| Close browser | `await browser.close()` | `browser.close()` | `await client.close()` |

## See also

- [Migration from pyppeteer](../migration/pyppeteer.md)
- [Migration from pychrome](../migration/pychrome.md)
- [Quickstart](../quickstart.md)
