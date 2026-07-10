# cdpwave

[![CI](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/ci.yml)
[![Tests](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/test.yml/badge.svg)](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/test.yml)
[![Docs](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/docs.yml/badge.svg)](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/docs.yml)
[![Release](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/release.yml/badge.svg)](https://github.com/MathiasPaulenko/cdpwave/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/cdpwave.svg)](https://pypi.org/project/cdpwave/)
[![Python](https://img.shields.io/pypi/pyversions/cdpwave.svg)](https://pypi.org/project/cdpwave/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Chrome DevTools Protocol for Python — direct, typed, async.

cdpwave talks to Chrome over a raw WebSocket. No Node.js, no ChromeDriver, no browser downloads. Just pure Python with full type hints and async-first design.

## Why cdpwave?

- **Full CDP coverage** — all 60 CDP domains implemented with 685 typed methods
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
- **Integration tested** — 322 integration tests against a real Chromium browser covering all domains

## Install

```bash
pip install cdpwave
```

## Quick start

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

## Documentation

Full documentation at [mathiaspaulenko.github.io/cdpwave](https://mathiaspaulenko.github.io/cdpwave/).

- [Quickstart](https://mathiaspaulenko.github.io/cdpwave/quickstart/) — 10-minute tutorial
- [Guide](https://mathiaspaulenko.github.io/cdpwave/guide/installation/) — in-depth feature coverage
- [Cookbook](https://mathiaspaulenko.github.io/cdpwave/cookbook/connect-existing/) — common recipes
- [API Reference](https://mathiaspaulenko.github.io/cdpwave/api/client/) — auto-generated docs
- [Migration](https://mathiaspaulenko.github.io/cdpwave/migration/pyppeteer/) — from pyppeteer or pychrome

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on
development setup, code style, testing, and pull request process.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Security

Found a vulnerability? See [SECURITY.md](SECURITY.md) for responsible disclosure.

## License

MIT
