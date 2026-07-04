# Multi-Tab Management

cdpwave uses **flatten sessions** — a single WebSocket connection that
multiplexes multiple targets (tabs, workers, iframes) via session IDs.
This means you can control many tabs simultaneously without opening
multiple WebSocket connections.

## How flatten sessions work

```text
┌─────────────────────────────────────┐
│           CDPClient                  │
│  ┌─────────────────────────────┐    │
│  │     Single WebSocket         │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐│    │
│  │  │Tab 1 │ │Tab 2 │ │Worker││    │
│  │  │sess A│ │sess B│ │sess C││    │
│  │  └──────┘ └──────┘ └──────┘│    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

Each `CDPSession` has a unique `sessionId`. When you send a command,
cdpwave attaches the session ID to the message. When the browser sends
an event, cdpwave routes it to the correct session based on the
`sessionId` field.

Benefits of flatten sessions:

- **Single connection** — one WebSocket handles all targets.
- **Lightweight** — creating a new session is a cheap round-trip.
- **Isolated events** — each session has its own event handlers.
- **Concurrent commands** — commands to different sessions can be
  sent concurrently.

## Create a new page

```python
session1 = await client.new_page("https://example.com")
session2 = await client.new_page("https://www.python.org")
```

`new_page()` creates a new browser tab, attaches a session to it, and
returns a `CDPSession`. You can optionally pass a URL to navigate
immediately.

Each `CDPSession` has its own domain properties (`page`, `runtime`,
`network`, etc.) and event dispatcher. Commands and events are
isolated per session.

## List existing pages

```python
pages = await client.get_pages()
for target in pages:
    print(f"{target.target_id} | {target.title} | {target.url}")
```

`get_pages()` returns all page-type targets in the browser. Each target
has:

- **`target_id`** — unique identifier for the target.
- **`title`** — page title.
- **`url`** — current URL.
- **`type`** — target type (`"page"`, `"background_page"`,
  `"service_worker"`, `"shared_worker"`, `"browser"`, `"other"`).

## Connect to an existing page

If a tab already exists (e.g., the browser was launched with a start
URL), you can attach a session to it:

```python
pages = await client.get_pages()
if pages:
    session = await client.connect_to_page(pages[0].target_id)
    result = await session.runtime.evaluate("document.title", return_by_value=True)
    print(result["result"]["value"])
    await session.close()
```

## Session isolation

Each `CDPSession` is completely independent:

- **Separate domain state** — enabling `Page` on one session doesn't
  affect another.
- **Separate event handlers** — events from one session don't trigger
  handlers on another.
- **Separate command IDs** — commands are correlated per session.

```python
tab1 = await client.new_page("https://example.com")
tab2 = await client.new_page("https://example.org")

# Each has its own event handlers
async def on_load1(_: dict) -> None:
    print("Tab 1 loaded")

async def on_load2(_: dict) -> None:
    print("Tab 2 loaded")

tab1.on("Page.loadEventFired", on_load1)
tab2.on("Page.loadEventFired", on_load2)

await tab1.page.enable()
await tab2.page.enable()
```

## Concurrent tabs

Run operations on multiple tabs simultaneously using `asyncio.gather`:

```python
import asyncio
from cdpwave import CDPClient, CDPSession

async def fetch_title(client: CDPClient, url: str) -> str:
    session = await client.new_page(url)
    result = await session.runtime.evaluate("document.title", return_by_value=True)
    title = result["result"]["value"]
    await session.close()
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

### Concurrency best practices

- **Limit concurrent tabs** — each tab consumes memory. For large
  batches, use a semaphore to limit concurrent tabs (e.g., 5-10).
- **Use timeouts per tab** — a slow page shouldn't block the entire
  batch. Wrap each tab's operations in `asyncio.wait_for`.
- **Close sessions when done** — unclosed sessions leak resources.
  Use `session.close()` or the context manager.

```python
sem = asyncio.Semaphore(5)

async def fetch_title_limited(client: CDPClient, url: str) -> str:
    async with sem:
        return await fetch_title(client, url)
```

## Close a page

```python
await session.close()
```

This detaches the session and closes the target. The `session.is_closed`
property returns `True` after close. After closing, the session can no
longer be used — commands will raise `SessionClosedError`.

## Close via target

```python
await session.target.close_target(session.target_id)
```

The session's `is_closed` property will become `True` when the browser
sends `Target.detachedFromTarget`.

## Close one tab, keep others

```python
session1 = await client.new_page("https://example.com")
session2 = await client.new_page("https://example.com")

await session1.close()
assert session1.is_closed

# session2 still works
result = await session2.runtime.evaluate("document.title", return_by_value=True)
print(result["result"]["value"])  # "Example Domain"

await session2.close()
```

## Target discovery

Enable target discovery to receive events when new targets are created
or destroyed:

```python
await client.target.set_discover_targets(discover=True)

async def on_created(params: dict) -> None:
    info = params["targetInfo"]
    print(f"Created: {info['type']} {info['url']}")

async def on_destroyed(params: dict) -> None:
    print(f"Destroyed: {params['targetId']}")

client.on("Target.targetCreated", on_created)
client.on("Target.targetDestroyed", on_destroyed)
```

This is useful for monitoring browser activity — for example, detecting
when a page opens a popup or creates a service worker.

## Auto-attach to child targets

Automatically attach to new child targets (iframes, workers):

```python
await client.target.set_auto_attach(
    auto_attach=True,
    wait_for_debugger_on_start=True,
    flatten=True,
)
```

With `flatten=True`, new child targets get flatten sessions
automatically. Listen for `Target.attachedToTarget` to get the session:

```python
async def on_attached(params: dict) -> None:
    target_info = params["targetInfo"]
    session_id = params["sessionId"]
    print(f"Attached to {target_info['type']}: {target_info['url']}")

client.on("Target.attachedToTarget", on_attached)
```

## Cleanup

When `client.close()` is called, all open sessions are closed
automatically. Using `async with` ensures this happens even on errors.

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        # Create multiple tabs
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")

        await tab1.page.enable()
        await tab2.page.enable()

        # Wait for both to load
        loaded1 = asyncio.Event()
        loaded2 = asyncio.Event()

        async def on_load1(_: dict) -> None:
            loaded1.set()

        async def on_load2(_: dict) -> None:
            loaded2.set()

        tab1.on("Page.loadEventFired", on_load1)
        tab2.on("Page.loadEventFired", on_load2)

        await asyncio.wait_for(loaded1.wait(), timeout=10.0)
        await asyncio.wait_for(loaded2.wait(), timeout=10.0)

        # Get titles concurrently
        async def get_title(session) -> str:
            result = await session.runtime.evaluate(
                "document.title", return_by_value=True
            )
            return result["result"]["value"]

        title1, title2 = await asyncio.gather(
            get_title(tab1),
            get_title(tab2),
        )
        print(f"Tab 1: {title1}")
        print(f"Tab 2: {title2}")

        # List all pages
        pages = await client.get_pages()
        print(f"\n{len(pages)} pages:")
        for p in pages:
            print(f"  {p.target_id} | {p.title} | {p.url}")

        await tab1.close()
        await tab2.close()

asyncio.run(main())
```
