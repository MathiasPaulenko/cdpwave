# Multi-Tab

cdpwave uses flatten sessions — a single WebSocket connection manages all tabs via `Target.attachToTarget` and `sessionId`.

## Create a new page

```python
page1 = await client.new_page("https://example.com")
page2 = await client.new_page("https://www.python.org")
```

Each `CDPSession` has its own domain properties (`page`, `runtime`, `network`, etc.) and event dispatcher.

## List existing pages

```python
pages = await client.get_pages()
for target in pages:
    print(f"{target.target_id} | {target.title} | {target.url}")
```

## Connect to an existing page

```python
pages = await client.get_pages()
if pages:
    page = await client.connect_to_page(pages[0].target_id)
    result = await page.runtime.evaluate("document.title", return_by_value=True)
    print(result["result"]["value"])
    await page.close()
```

## Close a page

```python
await page.close()
```

This detaches the session and closes the target. The `page.is_closed` property returns `True` after close.

## Close via target

```python
await page.target.close_target(page.target_id)
```

The session's `is_closed` property will become `True` when the browser sends `Target.detachedFromTarget`.

## Concurrent tabs

```python
import asyncio
from cdpwave import CDPClient, CDPSession

async def fetch_title(client: CDPClient, url: str) -> str:
    page = await client.new_page(url)
    result = await page.runtime.evaluate("document.title", return_by_value=True)
    title = result["result"]["value"]
    await page.close()
    return title

async def main() -> None:
    urls = ["https://example.com", "https://www.python.org"]

    async with await CDPClient.launch(headless=True) as client:
        tasks = [fetch_title(client, url) for url in urls]
        titles = await asyncio.gather(*tasks)
        for url, title in zip(urls, titles, strict=True):
            print(f"{url} -> {title}")

asyncio.run(main())
```

## Close one tab, keep others

```python
page1 = await client.new_page("https://example.com")
page2 = await client.new_page("https://example.com")

await page1.close()
assert page1.is_closed

# page2 still works
result = await page2.runtime.evaluate("document.title", return_by_value=True)
print(result["result"]["value"])  # "Example Domain"

await page2.close()
```

## Cleanup

When `client.close()` is called, all open sessions are closed automatically. Using `async with` ensures this happens even on errors.
