# Events

The Chrome DevTools Protocol is event-driven. After enabling a domain,
the browser sends events as JSON messages over the WebSocket. cdpwave
routes these events to your async handlers via an event dispatcher.

## The event model

```
Browser  →  WebSocket  →  cdpwave EventDispatcher  →  Your handlers
```

1. You call `session.on("Event.name", handler)` to register a handler.
2. The browser sends an event message with a `method` field and
   `params` field.
3. cdpwave matches the `method` to registered handlers and calls each
   one with the `params` dict.
4. Handlers run concurrently as asyncio tasks.

### Session vs browser events

Events come in two scopes:

- **Session events** — have a `sessionId` field. They come from a
  specific tab/target. Register them on `session.on()`.
- **Browser events** — have no `sessionId`. They come from the browser
  itself (target discovery, detached sessions). Register them on
  `client.on()`.

```python
# Session event — from a specific tab
session.on("Page.loadEventFired", handler)

# Browser event — from the browser itself
client.on("Target.targetCreated", handler)
```

## Subscribe to events

Use `session.on()` to register an async handler:

```python
async def on_load(params: dict) -> None:
    print("Page loaded!")

session.on("Page.loadEventFired", on_load)
```

The handler must be an `async` function that accepts a single `dict`
argument — the event parameters. The handler is called every time the
event fires.

### Return value

`on()` returns a `Subscription` object:

```python
sub = session.on("Page.loadEventFired", on_load)
```

## Unsubscribe

### Via Subscription object

```python
sub = session.on("Page.loadEventFired", on_load)
# ... later
sub.unsubscribe()
```

### Via session.off()

```python
session.off("Page.loadEventFired", on_load)
```

`off()` removes a specific handler by reference. If the same handler
was registered multiple times, all instances are removed.

## Error isolation

If a handler raises an exception, cdpwave catches it and logs the
error. Other handlers for the same event still run:

```python
async def bad_handler(_: dict) -> None:
    raise ValueError("oops")

async def good_handler(params: dict) -> None:
    print("Still works!")

session.on("Page.loadEventFired", bad_handler)
session.on("Page.loadEventFired", good_handler)
# bad_handler raises, good_handler still runs
```

This design ensures one buggy handler doesn't break the entire event
pipeline. The exception is logged to the `cdpwave.events` logger.

!!! note "No silent failures"
    While exceptions are caught, you should still handle errors in your
    handlers. Use try/except for expected failures and let unexpected
    ones propagate to the logger for debugging.

## Multiple handlers

Register multiple handlers for the same event. All are called in
registration order:

```python
session.on("Page.loadEventFired", handler_a)
session.on("Page.loadEventFired", handler_b)
```

Both `handler_a` and `handler_b` are called when `Page.loadEventFired`
fires. They run as separate asyncio tasks, so they execute concurrently.

## Browser-level events

`CDPClient` also has an `on()` method for browser-level events —
events without a `sessionId`:

```python
async def on_target_created(params: dict) -> None:
    print(f"New target: {params['targetInfo']['url']}")

client.on("Target.targetCreated", on_target_created)
```

Common browser-level events:

- **`Target.targetCreated`** — a new tab, window, or worker was created.
- **`Target.targetDestroyed`** — a target was closed.
- **`Target.attachedToTarget`** — a session was attached to a target.
- **`Target.detachedFromTarget`** — a session was detached.

## Common events

| Event | When | Scope | Requires |
|---|---|---|---|
| `Page.loadEventFired` | Page `load` event | Session | `Page.enable` |
| `Page.frameNavigated` | Frame navigated | Session | `Page.enable` |
| `Page.lifecycleEvent` | Lifecycle state change | Session | `Page.enable` |
| `Runtime.consoleAPICalled` | `console.log()` called | Session | `Runtime.enable` |
| `Runtime.exceptionThrown` | Uncaught JS exception | Session | `Runtime.enable` |
| `Runtime.bindingCalled` | JS binding invoked | Session | `Runtime.enable` + `add_binding` |
| `Network.requestWillBeSent` | HTTP request about to be sent | Session | `Network.enable` |
| `Network.responseReceived` | HTTP response headers received | Session | `Network.enable` |
| `Network.loadingFinished` | Response body downloaded | Session | `Network.enable` |
| `Network.loadingFailed` | Request failed | Session | `Network.enable` |
| `Target.targetCreated` | New target created | Browser | `Target.setDiscoverTargets` |
| `Target.detachedFromTarget` | Session detached | Browser | — |

!!! note "Domain enable required"
    Most events require the corresponding domain to be enabled first.
    For example, `Page.*` events need `session.page.enable()`,
    `Network.*` events need `session.network.enable()`. Without
    enabling, the browser doesn't send the events.

## Event patterns

### One-shot event (wait once)

Wait for an event to fire exactly once, then stop listening:

```python
import asyncio

loaded = asyncio.Event()

async def on_load(_: dict) -> None:
    loaded.set()

sub = session.on("Page.loadEventFired", on_load)
await session.page.navigate("https://example.com")
await asyncio.wait_for(loaded.wait(), timeout=10.0)
sub.unsubscribe()
```

### Collect events

Accumulate events for later analysis:

```python
requests: list[dict] = []

async def on_request(params: dict) -> None:
    requests.append(params)

session.on("Network.requestWillBeSent", on_request)
# ... navigate and wait ...
print(f"Captured {len(requests)} requests")
```

### Filter events

Only handle events that match a condition:

```python
async def on_response(params: dict) -> None:
    resp = params["response"]
    if resp["status"] >= 400:
        print(f"Error: {resp['status']} {resp['url']}")

session.on("Network.responseReceived", on_response)
```

### Transform and forward

Convert CDP events into a simpler format for your application:

```python
async def on_console(params: dict) -> None:
    level = params["type"]  # "log", "warn", "error"
    args = [a.get("value", a.get("description", "?")) for a in params["args"]]
    message = " ".join(str(v) for v in args)
    # Forward to your logging system
    print(f"[{level.upper()}] {message}")

session.on("Runtime.consoleAPICalled", on_console)
```

### Event with timeout

Always use timeouts when waiting for events to avoid hanging:

```python
try:
    await asyncio.wait_for(loaded.wait(), timeout=10.0)
except asyncio.TimeoutError:
    print("Page didn't load within 10 seconds")
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.runtime.enable()
        await session.page.enable()

        # Capture console output
        async def on_console(params: dict) -> None:
            msg_type = params["type"]
            args = [a.get("value", a.get("description", "?")) for a in params["args"]]
            print(f"[console.{msg_type}] {' '.join(str(v) for v in args)}")

        # Capture JS exceptions
        async def on_exception(params: dict) -> None:
            details = params["exceptionDetails"]
            print(f"JS error: {details['text']}")

        # Wait for page load
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Runtime.consoleAPICalled", on_console)
        session.on("Runtime.exceptionThrown", on_exception)
        session.on("Page.loadEventFired", on_load)

        await session.page.navigate("about:blank")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        await session.runtime.evaluate("console.log('hello from JS')")
        await session.runtime.evaluate("undefinedVar.foo")  # triggers exception
        await asyncio.sleep(1)

        await session.close()

asyncio.run(main())
```
