# Troubleshooting

This page documents known limitations and platform-specific behaviour
that may affect your tests.

## Fetch interception blocks navigation

When `Fetch.enable` intercepts requests with a broad pattern (e.g.
`*://*/*`), `Page.navigate` will block until the paused request is
handled. The `Fetch.requestPaused` event arrives **after** navigate is
already waiting.

**Solution**: Register a `Fetch.requestPaused` handler before
navigating, and use `asyncio.create_task` to navigate without blocking:

```python
import asyncio

ev = asyncio.Event()
paused: list[dict] = []

async def on_pause(event: dict) -> None:
    paused.append(event)
    ev.set()

session.on("Fetch.requestPaused", on_pause)
await session.fetch.enable(patterns=[{"urlPattern": "*://*/*"}])

# Navigate in a task so we can wait for the event
asyncio.create_task(session.page.navigate("https://example.com"))
await asyncio.wait_for(ev.wait(), timeout=10)

if paused:
    await session.fetch.continue_request(paused[0]["requestId"])

await session.fetch.disable()
```

## Infinite loops corrupt the session

`Runtime.evaluate("while(true){}")` will timeout (expected), but
afterwards **all subsequent commands on that session also timeout**.
Chrome cannot interrupt running JavaScript, so the session becomes
unusable.

**Solution**: Create a new session after a timeout caused by an
infinite loop:

```python
import asyncio

try:
    await asyncio.wait_for(session.runtime.evaluate("while(true){}"), timeout=2)
except asyncio.TimeoutError:
    await session.close()
    session = await client.new_page()  # fresh session
```

## Removed CDP commands in modern Chrome

Chrome evolves rapidly and some CDP commands have been removed or
deprecated. Calling a removed command returns
`CommandError: [-32601] 'X.method' wasn't found`.

Known removed/deprecated commands include:

| Domain | Removed commands |
|---|---|
| `Emulation` | `setIdleOverride`, `clearIdleOverride`, `setDisabledSensors`, `setScrollPositionOverride`, `setFocusEmulationEnabled`, `clearDefaultBackgroundColorOverride` |
| `Overlay` | `setShowDevTools` |
| `Debugger` | `setBreakpointActive` |
| `Log` | `getViolationsReport` |
| `Profiler` | `startTypeProfile`, `stopTypeProfile` |
| `HeapProfiler` | `addHeapSnapshotChunk`, `getLastSeenObjectId` |
| `Security` | `getVisibleSecurityState` |
| `Accessibility` | `getAXNode`, `getImageData` |
| `Animation` | `pause`, `resume` |
| `ServiceWorker` | `update`, `inspectWorker`, `getWorkers`, `getMessages` |
| `Sensor` | `enable`, `setSensorOverride`, `clearSensorOverride` |
| `DOMStorage` | `enable`, `disable` |

**Solution**: Use `session.send("Method.name", params)` as an escape
hatch for commands that may not exist, and wrap calls in
`try/except CommandError` to handle removals gracefully.

## SystemInfo only works on the browser target

`SystemInfo.getInfo` and related commands only work when sent to the
**browser target**, not page targets.

**Solution**: Use `client.send()` to send commands to the browser target:

```python
# Send a command to the browser target (not a page session)
result = await client.send("SystemInfo.getInfo")
```

## Page.crash may not return

`Page.crash` kills the renderer process, which may prevent the
command response from being delivered. This results in a
`CommandTimeoutError`.

**Solution**: Use a short timeout and suppress the expected error:

```python
import asyncio, contextlib

with contextlib.suppress(asyncio.TimeoutError, Exception):
    await asyncio.wait_for(session.page.crash(), timeout=3)
```

## DOM must be enabled before Overlay, CSS, and DOMDebugger

Chrome requires `DOM.enable()` to be called before enabling `Overlay`,
`CSS`, or `DOMDebugger` domains. Otherwise you get
`CommandError: [-32000] DOM should be enabled first`.

```python
await session.dom.enable()
await session.css.enable()
await session.overlay.enable()
```
