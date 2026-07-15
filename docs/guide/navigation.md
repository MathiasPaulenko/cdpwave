# Navigation

The Page domain controls browser navigation: loading URLs, reloading,
stopping, and managing history. This guide covers the most common
navigation patterns and wait strategies.

## Prerequisites

Enable the Page domain before using navigation methods or listening
to page events:

```python
await session.page.enable()
```

`Page.enable` activates lifecycle events such as `Page.loadEventFired`,
`Page.frameNavigated`, and `Page.lifecycleEvent`. Without it, you won't
receive any page-related events.

## Navigate to a URL

```python
result = await session.page.navigate("https://example.com")
```

`Page.navigate` returns a dict with `frameId` and `loaderId`:

```python
result = await session.page.navigate("https://example.com")
print(result["frameId"])
print(result["loaderId"])
```

- **`frameId`** — the frame that navigated. The top-level frame is
  always present; iframes have their own IDs.
- **`loaderId`** — a unique identifier for this load. Useful for
  correlating network requests with a specific navigation.

### Navigate with a referrer

Set the `Referer` header for the navigation request:

```python
await session.page.navigate(
    "https://example.com",
    referrer="https://google.com",
)
```

This is useful for testing analytics, access control, or simulating
traffic from a specific source.

### Transition types

Pass a `transition_type` to indicate how the navigation was triggered.
The browser uses this for features like back/forward button styling:

```python
await session.page.navigate(
    "https://example.com",
    transition_type="link",
)
```

Common values: `"link"`, `"typed"`, `"reload"`, `"back_forward"`,
`"auto_subframe"`, `"manual_subframe"`.

## Reload

```python
await session.page.reload()
```

Bypass the cache on reload — equivalent to Ctrl+Shift+R:

```python
await session.page.reload(ignore_cache=True)
```

## Stop loading

Abort all pending navigations and resource loads:

```python
await session.page.stop()
```

This is equivalent to pressing the stop button in the browser. Any
in-flight requests are cancelled.

## Navigation history

### Get history

```python
history = await session.page.get_navigation_history()
print(history["currentIndex"])
for entry in history["entries"]:
    print(f"  {entry['id']}: {entry['url']}")
```

The history contains:

- **`currentIndex`** — index of the current entry in the `entries` list.
- **`entries`** — list of navigation entries, each with `id`, `url`,
  `title`, and `transitionType`.

### Navigate to a history entry

```python
history = await session.page.get_navigation_history()
entry_id = history["entries"][0]["id"]
await session.page.navigate_to_history_entry(entry_id)
```

This is the equivalent of clicking back or forward in the browser.

### Reset history

```python
await session.page.reset_navigation_history()
```

Clears all navigation entries. The current page remains loaded, but the
back/forward buttons will have no history to navigate through.

## Wait strategies

cdpwave provides built-in wait helpers on `CDPSession` for common wait
patterns. You can also combine navigation with `asyncio` primitives for
custom conditions.

### Built-in helpers

| Method | Waits for |
|---|---|
| `session.wait_for_load_state("load")` | `Page.loadEventFired` |
| `session.wait_for_load_state("DOMContentLoaded")` | `Page.lifecycleEvent` with `DOMContentLoaded` |
| `session.wait_for_navigation(url="example.com")` | `Page.frameNavigated` matching URL |
| `session.wait_for_selector("#btn", timeout=10)` | Element matching CSS selector |
| `session.wait_for_network_idle(idle_time=0.5)` | All network requests finished |

```python
await session.page.navigate("https://example.com")
await session.wait_for_load_state("load")
```

### Wait for page load

Listen for `Page.loadEventFired`, which fires when the page's `load`
event completes:

```python
import asyncio

loaded = asyncio.Event()

async def on_load(_: dict) -> None:
    loaded.set()

session.on("Page.loadEventFired", on_load)
await session.page.navigate("https://example.com")
await asyncio.wait_for(loaded.wait(), timeout=10.0)
```

**How it works**: `Page.loadEventFired` is the CDP equivalent of the
browser's `window.onload` event. It fires after all resources (images,
stylesheets, scripts) have been downloaded. If you only need the DOM
to be ready (faster), listen for `Page.lifecycleEvent` with
`params["name"] == "DOMContentLoaded"` instead:

```python
dom_ready = asyncio.Event()

async def on_lifecycle(params: dict) -> None:
    if params["name"] == "DOMContentLoaded":
        dom_ready.set()

session.on("Page.lifecycleEvent", on_lifecycle)
await session.page.navigate("https://example.com")
await asyncio.wait_for(dom_ready.wait(), timeout=10.0)
```

### Wait for a specific condition

Poll the page until a condition is met. Useful when you don't know
which event to listen for:

```python
for _ in range(20):
    await asyncio.sleep(0.5)
    result = await session.runtime.evaluate(
        "document.title", return_by_value=True
    )
    title = result.get("result", {}).get("value", "")
    if title:
        break
```

This polls every 500ms for up to 10 seconds. Adjust the range and
sleep interval to control the timeout and frequency.

### Wait for network idle

Track pending requests and signal when all have completed. This is
useful for single-page applications that load data dynamically:

```python
pending: set[str] = set()
idle = asyncio.Event()

async def on_request(params: dict) -> None:
    req_id = params.get("requestId")
    if req_id:
        pending.add(req_id)

async def on_loading_finished(params: dict) -> None:
    req_id = params.get("requestId")
    if req_id:
        pending.discard(req_id)
    if not pending:
        idle.set()

async def on_loading_failed(params: dict) -> None:
    req_id = params.get("requestId")
    if req_id:
        pending.discard(req_id)
    if not pending:
        idle.set()

session.on("Network.requestWillBeSent", on_request)
session.on("Network.loadingFinished", on_loading_finished)
session.on("Network.loadingFailed", on_loading_failed)
await session.network.enable()
await session.page.navigate("https://example.com")
await asyncio.wait_for(idle.wait(), timeout=15.0)
```

!!! note "Network.enable required"
    You must call `session.network.enable()` before listening to
    `Network.*` events. Without it, the browser won't report network
    activity.

!!! warning "Race conditions"
    The simple set-based approach above may miss requests that complete
    before the handler is registered. For production code, register
    handlers *before* navigating.

### Wait for a specific URL

Combine `Page.frameNavigated` with a URL check:

```python
navigated = asyncio.Event()

async def on_frame_navigated(params: dict) -> None:
    if params["frame"]["url"] == "https://example.com":
        navigated.set()

session.on("Page.frameNavigated", on_frame_navigated)
await session.page.navigate("https://example.com")
await asyncio.wait_for(navigated.wait(), timeout=10.0)
```

## Frame tree

A page can contain multiple frames (the main frame plus iframes).
Inspect the full frame tree:

```python
tree = await session.page.get_frame_tree()
root = tree["frameTree"]["frame"]
print(f"Root frame: {root['id']} -> {root['url']}")

for child in tree["frameTree"].get("childFrames", []):
    print(f"  Child: {child['frame']['id']} -> {child['frame']['url']}")
```

Each frame has:

- **`id`** — unique frame identifier used by other CDP commands.
- **`url`** — the URL currently loaded in the frame.
- **`name`** — optional frame name (set via `<iframe name="...">`).
- **`securityOrigin`** — the security origin of the frame's content.
- **`mimeType`** — content type of the loaded document.

## Script injection

### Inject once

Evaluate a script on the current page:

```python
await session.runtime.evaluate("window.myFlag = true")
```

### Inject on every new document

Add a script that runs before any other scripts on every navigation.
Useful for polyfills, API overrides, or test harnesses:

```python
result = await session.page.add_script_to_evaluate_on_new_document(
    source="window.myFlag = true;"
)
script_id = result["identifier"]

# Later, remove it
await session.page.remove_script_to_evaluate_on_new_document(script_id)
```

The script executes in every frame, including new iframes, before any
page scripts run. This is the CDP equivalent of Puppeteer's
`page.evaluateOnNewDocument`.

## CSP bypass

Disable Content Security Policy for testing purposes:

```python
await session.page.set_bypass_csp(True)
```

This allows inline scripts, remote scripts, and other CSP-restricted
resources to load without restrictions. Useful for injecting test
scripts into pages with strict CSP rules.

!!! warning "Security"
    Never use CSP bypass in production. It disables a critical browser
    security feature.

## Lifecycle states

Freeze or activate a page's lifecycle:

```python
await session.page.set_web_lifecycle_state("frozen")
# ... later
await session.page.set_web_lifecycle_state("active")
```

A frozen page suspends timers, animations, and network requests. This
is useful for simulating mobile background behavior or conserving
resources.

## Full example

A complete navigation script with event-based waiting:

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()
        await session.network.enable()

        loaded = asyncio.Event()
        requests: list[dict] = []

        async def on_load(_: dict) -> None:
            loaded.set()

        async def on_request(params: dict) -> None:
            requests.append(params["request"])

        session.on("Page.loadEventFired", on_load)
        session.on("Network.requestWillBeSent", on_request)

        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        print(f"Loaded with {len(requests)} requests")
        for req in requests:
            print(f"  {req['method']} {req['url']}")

        await session.close()

asyncio.run(main())
```
