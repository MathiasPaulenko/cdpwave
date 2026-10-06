<p align="center">
  <img src="https://raw.githubusercontent.com/MathiasPaulenko/cdpwave/main/docs/assets/images/logo-wide.svg" alt="cdpwave" width="480">
</p>

<h3 align="center">Chrome DevTools Protocol for Python — direct, typed, async</h3>

<p align="center">
  <strong>60 CDP domains · 692 typed methods · zero Node.js · zero ChromeDriver · zero browser downloads</strong>
</p>

---

[![CI](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/cdpwave.svg)](https://pypi.org/project/cdpwave/)
[![Python](https://img.shields.io/pypi/pyversions/cdpwave.svg)](https://pypi.org/project/cdpwave/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://mathiaspaulenko.github.io/cdpwave/)

> Chrome DevTools Protocol for Python — direct, typed, async. cdpwave talks to Chrome over a raw WebSocket. No Node.js, no ChromeDriver, no browser downloads. Just pure Python with full type hints and async-first design.

## Quick demo

**30 seconds to your first CDP call.**

```bash
pip install cdpwave
```

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])  # "Example Domain"
        await session.close()

asyncio.run(main())
```

## Why cdpwave?

cdpwave is a low-level Chrome DevTools Protocol client for Python. It talks directly to Chrome's WebSocket endpoint — no Node.js, no ChromeDriver, no Selenium, no Playwright. Just pure async Python with full type hints.

It is the CDP backend that powers [wavexis](https://github.com/MathiasPaulenko/wavexis) and [wavexis-mcp](https://github.com/MathiasPaulenko/wavexis-mcp).

### Key features

- **Broad CDP coverage** — 60 domains with 692 typed methods (~95% of the protocol), plus `session.send()` for the rest
- **Direct WebSocket** — single connection to Chrome's DevTools Protocol, no intermediate layers
- **Fully typed** — `mypy --strict` across the entire codebase, IDE autocomplete everywhere
- **Async-first** — built on `asyncio`, no threading, no blocking calls
- **Browser detection** — finds Chrome, Edge, Brave, or Chromium already on your system
- **Flatten sessions** — one WebSocket for all tabs via `Target.attachToTarget` + `sessionId`
- **Escape hatch** — `session.send("Any.CDPMethod", params)` for any uncovered command
- **HTTP discovery** — typed access to `/json/version` and `/json/list` endpoints
- **WebSocket keepalive** — automatic ping/pong with configurable interval and timeout
- **Direct WebSocket URL** — `CDPClient.connect(ws_url=...)` bypasses HTTP discovery
- **Event helpers** — `session.wait_for_event()` and `session.on()` for async event handling
- **Multi-tab sessions** — `client.sessions` property tracks all active sessions
- **1437 integration tests** — against a real Chromium browser covering all domains

### How it works

```text
Your Python code
  → CDPClient.launch() finds and starts Chrome
    → Connects to Chrome's WebSocket endpoint
      → session.runtime.evaluate("document.title")
        → Chrome executes and returns the result
      ← Typed response parsed into Python dicts
    ← Session stays open for chained calls
  ← Browser closes on context exit
```

### Core concepts

- **CDPClient** — The top-level client. Launches Chrome, manages the WebSocket connection, and creates sessions.
- **Session** — A CDP target (tab, page, worker). Each session has its own method namespace (`session.runtime`, `session.page`, `session.network`, etc.).
- **Domain** — A CDP namespace like `Runtime`, `Page`, `Network`, `DOM`. Each domain has typed methods with full parameter validation.
- **Escape hatch** — `session.send("Any.CDPMethod", params)` lets you call any CDP method, even if cdpwave doesn't have a typed wrapper for it.

## Requirements

- Python 3.11 or higher
- A Chromium-based browser (Chrome, Edge, Brave, or Chromium) already installed
- No Node.js, no ChromeDriver, no separate Chromium download

## Install

```bash
pip install cdpwave
```

## Quick start

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    # Launch Chrome and connect
    async with await CDPClient.launch(headless=True) as client:
        # Open a new tab
        session = await client.new_page("https://example.com")

        # Evaluate JavaScript
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        print(result["result"]["value"])  # "Example Domain"

        # Take a screenshot (data is base64-encoded PNG)
        screenshot = await session.page.capture_screenshot()
        with open("screenshot.png", "wb") as f:
            import base64
            f.write(base64.b64decode(screenshot["data"]))

        # Navigate somewhere else
        await session.page.navigate("https://example.org")
        await session.close()

asyncio.run(main())
```

## Connect to an existing browser

```python
from cdpwave import CDPClient

# Connect to a browser already running with --remote-debugging-port
async with await CDPClient.connect(host="localhost", port=9222) as client:
    session = await client.new_page("https://example.com")
    # ...
```

## Export to PDF

```python
import base64

session = await client.new_page("https://example.com")
await session.wait_for_load_state("load")

pdf = await session.page.print_to_pdf(print_background=True)
with open("page.pdf", "wb") as f:
    f.write(base64.b64decode(pdf["data"]))
```

## Emulate a mobile device

```python
# iPhone-sized viewport with a mobile user agent
await session.emulation.set_device_metrics_override(
    width=390, height=844, device_scale_factor=3, mobile=True
)
await session.emulation.set_user_agent_override(
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
await session.page.navigate("https://example.com")
```

## Intercept and mock requests

```python
async def on_request_paused(params):
    await session.fetch.fulfill_request(
        params["requestId"],
        response_code=200,
        response_headers=[{"name": "Content-Type", "value": "application/json"}],
        body=base64.b64encode(b'{"mocked": true}').decode(),
    )

await session.fetch.enable(patterns=[{"urlPattern": "*/api/*"}])
session.on("Fetch.requestPaused", on_request_paused)
await session.page.navigate("https://example.com")
```

## Type into a page

```python
document = await session.dom.get_document()
node = await session.dom.query_selector(
    document["root"]["nodeId"], "input[name=q]"
)
await session.dom.focus(node["nodeId"])
await session.input.insert_text("hello world")
await session.input.dispatch_key_event("keyDown", key="Enter", code="Enter")
await session.input.dispatch_key_event("keyUp", key="Enter", code="Enter")
```

## Multi-tab sessions

```python
async with await CDPClient.launch() as client:
    tab1 = await client.new_page("https://example.com")
    tab2 = await client.new_page("https://example.org")

    # Each tab is an independent session — screenshot one while the
    # other keeps running
    shot = await tab1.page.capture_screenshot()
    title2 = await tab2.runtime.evaluate("document.title", return_by_value=True)
```

## Synchronous API

Same surface without `async`/`await` — useful for scripts and REPLs:

```python
from cdpwave.sync import SyncCDPClient

with SyncCDPClient.launch(headless=True) as client:
    page = client.new_page("https://example.com")
    result = page.runtime.evaluate("document.title", return_by_value=True)
    print(result["result"]["value"])
```

## Escape hatch

Call any CDP method, even if cdpwave doesn't have a typed wrapper:

```python
result = await session.send("Performance.getMetrics", {})
print(result["metrics"])
```

## Event handling

```python
async with await CDPClient.launch() as client:
    session = await client.new_page()

    # Watch every request the page makes
    await session.network.enable()

    def on_request(params):
        print(f"→ {params['request']['method']} {params['request']['url']}")

    session.on("Network.requestWillBeSent", on_request)
    await session.page.navigate("https://example.com")

    # Wait for the page load event
    await session.wait_for_load_state("load")
```

## Documentation

Full documentation at **[mathiaspaulenko.github.io/cdpwave](https://mathiaspaulenko.github.io/cdpwave/)**

- [Quickstart](https://mathiaspaulenko.github.io/cdpwave/quickstart/) — 10-minute tutorial
- [Guide](https://mathiaspaulenko.github.io/cdpwave/guide/installation/) — in-depth feature coverage
- [Cookbook](https://mathiaspaulenko.github.io/cdpwave/cookbook/connect-existing/) — common recipes
- [API Reference](https://mathiaspaulenko.github.io/cdpwave/api/client/) — auto-generated docs
- [Migration](https://mathiaspaulenko.github.io/cdpwave/migration/pyppeteer/) — from pyppeteer or pychrome

## Ecosystem

cdpwave is part of the Wave ecosystem — browser automation tools in 100% Python:

| Project | Description |
|---------|-------------|
| **[cdpwave](https://github.com/MathiasPaulenko/cdpwave)** | Chrome DevTools Protocol client (this repo) |
| **[bidiwave](https://github.com/MathiasPaulenko/bidiwave)** | WebDriver BiDi client — cross-browser, W3C standard |
| **[wavexis](https://github.com/MathiasPaulenko/wavexis)** | Browser automation CLI — wraps cdpwave + bidiwave |
| **[wavexis-mcp](https://github.com/MathiasPaulenko/wavexis-mcp)** | MCP server — 220 browser automation tools for LLMs |

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on
development setup, code style, testing, and pull request process.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Security

Found a vulnerability? See [SECURITY.md](SECURITY.md) for responsible disclosure.

## License

MIT
