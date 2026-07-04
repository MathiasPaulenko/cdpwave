# Installation

## Requirements

- Python 3.11 or higher
- A Chromium-based browser installed (Chrome, Edge, Brave, or Chromium)

cdpwave uses the browser already on your system. It does not download anything.

## Install

```bash
pip install cdpwave
```

## Development install

For contributing or running tests:

```bash
git clone https://github.com/MathiasPaulenko/cdpwave.git
cd cdpwave
pip install -e ".[dev]"
```

## Verify

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        page = await client.new_page("about:blank")
        result = await page.runtime.evaluate("1 + 1", return_by_value=True)
        print(result["result"]["value"])  # 2
        await page.close()

asyncio.run(main())
```

If this prints `2`, you're ready to go.

## Browser detection

cdpwave searches for browsers in this order:

1. Chrome
2. Edge
3. Brave
4. Chromium

You can override the browser path with environment variables:

| Variable | Description |
|---|---|
| `CDPWAVE_BROWSER_PATH` | Path to any Chromium-based browser executable |
| `CDPWAVE_CHROME_PATH` | Path to Chrome specifically |
| `CDPWAVE_EDGE_PATH` | Path to Edge specifically |
| `CDPWAVE_BRAVE_PATH` | Path to Brave specifically |
| `CDPWAVE_CHROMIUM_PATH` | Path to Chromium specifically |

See [Browser Launch](browser-launch.md) for more options.
