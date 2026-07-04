# cdpwave

Chrome DevTools Protocol for Python — direct, typed, async.

cdpwave talks to Chrome over a raw WebSocket. No Node.js, no ChromeDriver, no browser downloads. Just pure Python with full type hints and async-first design.

## Why cdpwave?

- **Direct WebSocket** — single connection to Chrome's DevTools Protocol, no intermediate layers
- **Fully typed** — `mypy --strict` across the entire codebase, IDE autocomplete everywhere
- **Async-first** — built on `asyncio`, no threading, no blocking calls
- **Browser detection** — finds Chrome, Edge, Brave, or Chromium already on your system
- **Flatten sessions** — one WebSocket for all tabs via `Target.attachToTarget` + `sessionId`
- **Escape hatch** — `session.send("Any.CDPMethod", params)` for uncovered domains
- **HTTP discovery** — typed access to `/json/version` and `/json/list` endpoints
- **MIT licensed** — permissive, compatible with any use

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

## Next steps

- [Quickstart](quickstart.md) — 10-minute tutorial
- [Guide](guide/installation.md) — in-depth coverage of each feature
- [Cookbook](cookbook/connect-existing.md) — recipes for common scenarios
- [API Reference](api/client.md) — auto-generated docs for every class
- [Migration](migration/pyppeteer.md) — coming from pyppeteer or pychrome
