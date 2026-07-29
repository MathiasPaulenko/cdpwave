<p align="center">
  <img src="https://raw.githubusercontent.com/MathiasPaulenko/cdpwave/main/docs/assets/images/logo-wide.svg" alt="cdpwave" width="480">
</p>

<h3 align="center">Chrome DevTools Protocol for Python — direct, typed, async</h3>

<p align="center">
  <strong>60 CDP domains · 689 typed methods · zero Node.js · zero ChromeDriver · zero browser downloads</strong>
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

- **Full CDP coverage** — all 60 CDP domains implemented with 689 typed methods
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
- **1424 integration tests** — against a real Chromium browser covering all domains

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

        # Take a screenshot
        screenshot = await session.page.capture_screenshot()
        with open("screenshot.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))

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

## Multi-tab sessions

```python
async with await CDPClient.launch() as client:
    tab1 = await client.new_page("https://example.com")
    tab2 = await client.new_page("https://example.org")

    # Work on both tabs independently
    title1 = await tab1.runtime.evaluate("document.title", return_by_value=True)
    title2 = await tab2.runtime.evaluate("document.title", return_by_value=True)

    print(title1["result"]["value"])  # "Example Domain"
    print(title2["result"]["value"])  # "IANA-managed domains"
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
    session = await client.new_page("https://example.com")

    # Listen for console messages
    def on_console(msg):
        print(f"[console] {msg['args']}")

    session.on("Runtime.consoleAPICalled", on_console)

    # Wait for a specific event
    await session.wait_for_event("Page.loadEventFired")
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
