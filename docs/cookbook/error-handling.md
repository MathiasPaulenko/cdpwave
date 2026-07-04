# Error Handling

## Exception hierarchy

All cdpwave exceptions inherit from `CDPError`:

```
CDPError
├── ConnectionClosedError    # WebSocket closed
├── CommandError             # CDP error response (has .code, .message)
├── CommandTimeoutError      # Command didn't respond in time
├── SessionClosedError       # Session closed by browser
├── BrowserNotFoundError     # No browser found on system
├── DiscoveryError           # HTTP discovery failed
├── LaunchTimeoutError       # Browser didn't start in time
└── LaunchError              # Browser crashed during startup
```

## Catch specific exceptions

```python
from cdpwave import (
    CDPError,
    CommandError,
    CommandTimeoutError,
    BrowserNotFoundError,
)

try:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        result = await session.runtime.evaluate("document.title", return_by_value=True)
except BrowserNotFoundError:
    print("Install Chrome or set CDPWAVE_BROWSER_PATH")
except CommandTimeoutError:
    print("Command timed out — browser may be overloaded")
except CommandError as e:
    print(f"CDP error {e.code}: {e.message}")
except CDPError as e:
    print(f"cdpwave error: {e}")
```

## CommandError details

`CommandError` includes the CDP error code and message:

```python
try:
    await session.send("NonExistent.method")
except CommandError as e:
    print(f"Code: {e.code}")    # -32601
    print(f"Message: {e.message}")  # "'NonExistent.method' wasn't found"
    print(f"Data: {e.data}")    # None or dict
```

## Session closed

If the browser closes a tab (e.g., `window.close()` in JS), the session becomes closed. Further `send()` calls raise `SessionClosedError`:

```python
from cdpwave import SessionClosedError

try:
    await session.runtime.evaluate("window.close()")
    await asyncio.sleep(1)
    await session.runtime.evaluate("1 + 1")
except SessionClosedError:
    print("Session was closed by the browser")
```

## Launch failures

```python
from cdpwave import LaunchTimeoutError, LaunchError

try:
    client = await CDPClient.launch(timeout=5.0)
except LaunchTimeoutError:
    print("Browser didn't start within 5 seconds")
except LaunchError as e:
    print(f"Browser crashed: {e}")
```

## Cleanup is guaranteed

`async with` ensures cleanup even when exceptions occur:

```python
async with await CDPClient.launch(headless=True) as client:
    raise ValueError("something went wrong")
# client.close() still runs — browser terminated, WebSocket closed
```

`close()` is idempotent and never raises. Calling it multiple times is safe.

## Best practices

- Always use `async with` for `CDPClient` and `CDPSession`
- Catch `BrowserNotFoundError` to give helpful install instructions
- Catch `CommandTimeoutError` for slow pages or overloaded browsers
- Let `CDPError` be the catch-all for unexpected cdpwave issues
- Don't catch `SessionClosedError` unless you have recovery logic
