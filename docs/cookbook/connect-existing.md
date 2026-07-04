# Connect to an Existing Browser

If Chrome is already running with remote debugging enabled, connect to it instead of launching a new process.

## Start Chrome manually

```bash
google-chrome --remote-debugging-port=9222 --headless=new
```

Or on Windows:

```powershell
chrome.exe --remote-debugging-port=9222 --headless=new
```

## Connect with cdpwave

```python
from cdpwave import CDPClient

client = await CDPClient.connect(host="localhost", port=9222)
```

`CDPClient.connect` uses HTTP discovery (`/json/version`) to find the WebSocket URL. No browser process is managed — closing the client only closes the WebSocket, not the browser.

## List and connect to pages

```python
pages = await client.get_pages()
for target in pages:
    print(f"{target.target_id} | {target.title} | {target.url}")

if pages:
    page = await client.connect_to_page(pages[0].target_id)
    result = await page.runtime.evaluate("document.title", return_by_value=True)
    print(result["result"]["value"])
    await page.close()
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.connect(host="localhost", port=9222) as client:
        pages = await client.get_pages()
        for t in pages:
            print(f"  {t.target_id} | {t.type} | {t.title} | {t.url}")

        if pages:
            page = await client.connect_to_page(pages[0].target_id)
            result = await page.runtime.evaluate("document.title", return_by_value=True)
            print(f"Title: {result['result']['value']}")
            await page.close()

asyncio.run(main())
```
