# Migrating from pychrome

pychrome is a threading-based CDP wrapper. cdpwave is a modern async-first replacement with full CDP coverage, type hints, and browser detection.

## Key differences

| Aspect | pychrome | cdpwave |
|---|---|---|
| Paradigm | Threading | asyncio |
| Sessions | Legacy (one WS per tab) | Flatten (one WS for all) |
| Browser launcher | No | Yes (auto-detection) |
| Typing | No type hints | mypy --strict |
| CDP coverage | Dynamic (everything is dynamic) | All 60 domains, 689 typed methods |
| API | `tab.Page.navigate(url=...)` | `await session.page.navigate("...")` |
| Context manager | No | Yes |
| Events | Sync callbacks | Async handlers with error isolation |
| Escape hatch | Dynamic (everything is dynamic) | `session.send("Method", params)` |

## API equivalence

| pychrome | cdpwave |
|---|---|
| `pychrome.Browser(url="http://127.0.0.1:9222")` | `await CDPClient.connect(host="127.0.0.1", port=9222)` |
| `tab = browser.new_tab()` | `session = await client.new_page()` |
| `tab.start()` | Automatic (no explicit start) |
| `tab.Page.navigate(url="https://example.com")` | `await session.page.navigate("https://example.com")` |
| `tab.Runtime.evaluate(expression="document.title")` | `await session.runtime.evaluate("document.title", return_by_value=True)` |
| `tab.Page.captureScreenshot()` | `await session.page.capture_screenshot()` |
| `tab.stop()` | `await session.close()` |
| `browser.close_tab(tab)` | `await session.close()` or `await session.target.close_target(session.target_id)` |
| `tab.set_listener("Page.loadEventFired", cb)` | `session.on("Page.loadEventFired", async_handler)` |

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
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await session.close()

asyncio.run(main())
```

## Key migration notes

1. **No `tab.start()`** — sessions are ready immediately after `new_page()` or `connect_to_page()`.
2. **No `tab.wait()`** — use `session.wait_for_load_state()`, `session.wait_for_navigation()`, or `session.wait_for_selector()` instead of blocking waits.
3. **Sync API** — for simple scripts that mirror pychrome's sync style, use `from cdpwave.sync import SyncCDPClient` for a synchronous wrapper.
4. **Async handlers** — event handlers must be `async def`, not regular functions.
5. **Full domain access** — all 60 CDP domains are typed properties: `session.page`, `session.runtime`, `session.network`, `session.dom`, `session.debugger`, `session.fetch`, `session.emulation`, `session.input`, etc.
6. **Browser detection** — `CDPClient.launch()` finds and starts Chrome automatically. No need to run Chrome separately.
7. **Flatten sessions** — all tabs share one WebSocket connection via `sessionId` multiplexing.
8. **Context manager** — use `async with` for guaranteed cleanup. No manual `stop()` / `close_tab()`.
9. **Typed wrappers** — unlike pychrome where everything is dynamic, cdpwave provides typed methods with docstrings and IDE autocomplete for all 689 CDP commands.
