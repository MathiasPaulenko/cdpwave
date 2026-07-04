# Migrating from pychrome

pychrome is a threading-based CDP wrapper. cdpwave is a modern async-first replacement with type hints and browser detection.

## Key differences

| Aspect | pychrome | cdpwave |
|---|---|---|
| Paradigm | Threading | asyncio |
| Sessions | Legacy (one WS per tab) | Flatten (one WS for all) |
| Browser launcher | No | Yes (auto-detection) |
| Typing | No type hints | mypy --strict |
| API | `tab.Page.navigate(url=...)` | `await page.page.navigate("...")` |
| Context manager | No | Yes |
| Events | Sync callbacks | Async handlers with error isolation |
| Escape hatch | Dynamic (everything is dynamic) | `session.send("Method", params)` |

## API equivalence

| pychrome | cdpwave |
|---|---|
| `pychrome.Browser(url="http://127.0.0.1:9222")` | `await CDPClient.connect(host="127.0.0.1", port=9222)` |
| `tab = browser.new_tab()` | `page = await client.new_page()` |
| `tab.start()` | Automatic (no explicit start) |
| `tab.Page.navigate(url="https://example.com")` | `await page.page.navigate("https://example.com")` |
| `tab.Runtime.evaluate(expression="document.title")` | `await page.runtime.evaluate("document.title", return_by_value=True)` |
| `tab.Page.captureScreenshot()` | `await page.page.capture_screenshot()` |
| `tab.stop()` | `await page.close()` |
| `browser.close_tab(tab)` | `await page.close()` or `await page.target.close_target(page.target_id)` |
| `tab.set_listener("Page.loadEventFired", cb)` | `page.on("Page.loadEventFired", async_handler)` |

## Migration example

### pychrome

```python
import pychrome

browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab = browser.new_tab()
tab.start()
tab.Page.navigate(url="https://example.com")
tab.wait(timeout=5)
result = tab.Runtime.evaluate(expression="document.title")
print(result["result"]["value"])
tab.stop()
browser.close_tab(tab)
```

### cdpwave

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.connect(host="127.0.0.1", port=9222) as client:
        page = await client.new_page("https://example.com")
        result = await page.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await page.close()

asyncio.run(main())
```

## Key migration notes

1. **No `tab.start()`** — sessions are ready immediately after `new_page()` or `connect_to_page()`.
2. **No `tab.wait()`** — use events with `asyncio.Event` or poll with `runtime.evaluate`.
3. **Async handlers** — event handlers must be `async def`, not regular functions.
4. **Domain properties** — use `page.page`, `page.runtime`, `page.network`, etc. instead of `tab.Page`, `tab.Runtime`.
5. **Browser detection** — `CDPClient.launch()` finds and starts Chrome automatically. No need to run Chrome separately.
6. **Flatten sessions** — all tabs share one WebSocket connection via `sessionId` multiplexing.
7. **Context manager** — use `async with` for guaranteed cleanup. No manual `stop()` / `close_tab()`.
