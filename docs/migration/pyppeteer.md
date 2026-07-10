# Migrating from pyppeteer

pyppeteer is unmaintained (last release: Feb 2024 alpha). cdpwave is a modern, typed, async-first replacement with full CDP coverage.

## Key differences

| Aspect | pyppeteer | cdpwave |
|---|---|---|
| Maintenance | Dead | Active |
| Browser | Downloads Chromium (~150MB) | Detects existing browser |
| API style | Puppeteer port (camelCase) | Pythonic (snake_case, type hints) |
| Typing | No type hints | mypy --strict |
| CDP coverage | 7 domains | All 60 domains, 685 methods |
| Sessions | One WebSocket per tab | Flatten (one WebSocket for all) |
| CDP access | Not exposed | Typed domains + escape hatch |
| Context manager | Yes | Yes |
| Dependencies | websockets, pyppeteer-chromium | websockets, pydantic |

## API equivalence

| pyppeteer | cdpwave |
|---|---|
| `await launch(headless=True)` | `await CDPClient.launch(headless=True)` |
| `browser = await launch()` | `async with await CDPClient.launch() as client:` |
| `page = await browser.newPage()` | `session = await client.new_page()` |
| `await page.goto(url)` | `await session.page.navigate(url)` |
| `await page.title()` | `result = await session.runtime.evaluate("document.title", return_by_value=True)` |
| `await page.screenshot()` | `await session.page.capture_screenshot()` |
| `await page.pdf()` | `await session.page.print_to_pdf()` |
| `await page.evaluate(expr)` | `await session.runtime.evaluate(expr, return_by_value=True)` |
| `await page.reload()` | `await session.page.reload()` |
| `await page.close()` | `await session.close()` |
| `await browser.close()` | `await client.close()` |
| `page.on('load', handler)` | `session.on("Page.loadEventFired", handler)` |
| `page.on('console', handler)` | `session.on("Runtime.consoleAPICalled", handler)` |
| `await page.cookies()` | `await session.network.get_cookies()` |
| `await page.setCookie(...)` | `await session.network.set_cookie(...)` |
| `await page.waitForSelector(sel)` | `await session.wait_for_selector(sel)` |
| `await page.click(sel)` | Manual: `dom.query_selector` + `dom.focus` + escape hatch |

## Migration example

### pyppeteer

```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto("https://example.com")
    title = await page.title()
    print(title)
    await browser.close()

asyncio.run(main())
```

### cdpwave

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await session.close()

asyncio.run(main())
```

## Key migration notes

1. **Wait helpers** — cdpwave now provides `session.wait_for_navigation()`, `session.wait_for_selector()`, `session.wait_for_load_state()`, and `session.wait_for_network_idle()` as direct replacements for pyppeteer's `waitFor*` methods.
2. **Sync API** — for simple scripts, use `from cdpwave.sync import SyncCDPClient` as a drop-in replacement without async/await.
3. **Full CDP access** — all 60 domains are available as typed properties: `session.page`, `session.runtime`, `session.network`, `session.dom`, `session.debugger`, `session.fetch`, `session.emulation`, `session.input`, etc.
4. **Event names** — Use raw CDP event names: `"Page.loadEventFired"` not `"load"`.
5. **Flatten sessions** — All tabs share one WebSocket. No per-tab connection overhead.
6. **Input simulation** — use `session.input.dispatch_key_event()` and `session.input.dispatch_mouse_event()` instead of `page.click()` / `page.type()`.
7. **Request interception** — use `session.fetch` domain instead of `page.setRequestInterception()`.
8. **Device emulation** — use `session.emulation.set_device_metrics_override()` instead of `page.emulate()`.
