# Migrating from pyppeteer

pyppeteer is unmaintained (last release: Feb 2024 alpha). cdpwave is a modern, typed, async-first replacement.

## Key differences

| Aspect | pyppeteer | cdpwave |
|---|---|
| Maintenance | Dead | Active |
| Browser | Downloads Chromium (~150MB) | Detects existing browser |
| API style | Puppeteer port (camelCase) | Pythonic (snake_case, type hints) |
| Typing | No type hints | mypy --strict |
| Sessions | One WebSocket per tab | Flatten (one WebSocket for all) |
| CDP access | Not exposed | Typed domains + escape hatch |
| Context manager | Yes | Yes |
| Dependencies | websockets, pyppeteer-chromium | websockets, pydantic |

## API equivalence

| pyppeteer | cdpwave |
|---|---|
| `await launch(headless=True)` | `await CDPClient.launch(headless=True)` |
| `browser = await launch()` | `async with await CDPClient.launch() as client:` |
| `page = await browser.newPage()` | `page = await client.new_page()` |
| `await page.goto(url)` | `await page.page.navigate(url)` |
| `await page.title()` | `result = await page.runtime.evaluate("document.title", return_by_value=True)` |
| `await page.screenshot()` | `await page.page.capture_screenshot()` |
| `await page.pdf()` | `await page.page.print_to_pdf()` |
| `await page.evaluate(expr)` | `await page.runtime.evaluate(expr, return_by_value=True)` |
| `await page.reload()` | `await page.page.reload()` |
| `await page.close()` | `await page.close()` |
| `await browser.close()` | `await client.close()` |
| `page.on('load', handler)` | `page.on("Page.loadEventFired", handler)` |
| `page.on('console', handler)` | `page.on("Runtime.consoleAPICalled", handler)` |
| `await page.cookies()` | `await page.network.get_cookies()` |
| `await page.setCookie(...)` | `await page.network.set_cookie(...)` |
| `await page.waitForSelector(sel)` | Manual: poll with `dom.query_selector` |
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
        page = await client.new_page("https://example.com")
        result = await page.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await page.close()

asyncio.run(main())
```

## Key migration notes

1. **No auto-wait** — pyppeteer auto-waits for navigation. In cdpwave, use `Page.loadEventFired` with `asyncio.Event`.
2. **No high-level API** — `page.click()`, `page.type()` don't exist in v1. Use DOM + escape hatch (`Input.dispatchKeyEvent`).
3. **Domain access** — CDP domains are properties: `page.page`, `page.runtime`, `page.network`, `page.dom`.
4. **Event names** — Use raw CDP event names: `"Page.loadEventFired"` not `"load"`.
5. **Flatten sessions** — All tabs share one WebSocket. No per-tab connection overhead.
