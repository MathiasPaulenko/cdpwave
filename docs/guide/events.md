# Events

## Subscribe to events

Use `session.on()` to register an async handler:

```python
async def on_load(params: dict) -> None:
    print("Page loaded!")

page.on("Page.loadEventFired", on_load)
```

## Unsubscribe

`on()` returns a `Subscription` object. Call `unsubscribe()` to remove the handler:

```python
sub = page.on("Page.loadEventFired", on_load)
# ... later
sub.unsubscribe()
```

Or use `session.off()`:

```python
page.off("Page.loadEventFired", on_load)
```

## Error isolation

If a handler raises an exception, it is caught and logged. Other handlers for the same event still run:

```python
async def bad_handler(_: dict) -> None:
    raise ValueError("oops")

async def good_handler(params: dict) -> None:
    print("Still works!")

page.on("Page.loadEventFired", bad_handler)
page.on("Page.loadEventFired", good_handler)
# bad_handler raises, good_handler still runs
```

## Multiple handlers

Register multiple handlers for the same event. All are called in registration order:

```python
page.on("Page.loadEventFired", handler_a)
page.on("Page.loadEventFired", handler_b)
```

## Browser-level events

`CDPClient` also has an `on()` method for browser-level events (events without a `sessionId`):

```python
async def on_target_created(params: dict) -> None:
    print(f"New target: {params['targetInfo']['url']}")

client.on("Target.targetCreated", on_target_created)
```

## Common events

| Event | When | Scope |
|---|---|---|
| `Page.loadEventFired` | Page finished loading | Session |
| `Page.frameNavigated` | Frame navigated | Session |
| `Runtime.consoleAPICalled` | `console.log()` called | Session |
| `Runtime.exceptionThrown` | Uncaught JS exception | Session |
| `Network.requestWillBeSent` | HTTP request about to be sent | Session |
| `Network.responseReceived` | HTTP response received | Session |
| `Target.targetCreated` | New target (tab) created | Browser |
| `Target.detachedFromTarget` | Session detached by browser | Browser |

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        page = await client.new_page()
        await page.runtime.enable()

        async def on_console(params: dict) -> None:
            msg_type = params["type"]
            args = [a.get("value", a.get("description", "?")) for a in params["args"]]
            print(f"[console.{msg_type}] {' '.join(str(v) for v in args)}")

        page.on("Runtime.consoleAPICalled", on_console)
        await page.page.navigate("about:blank")
        await page.runtime.evaluate("console.log('hello from JS')")
        await asyncio.sleep(1)
        await page.close()

asyncio.run(main())
```
