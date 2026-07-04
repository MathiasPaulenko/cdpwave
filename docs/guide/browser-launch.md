# Browser Launch

cdpwave can launch a browser process and connect to it automatically,
or connect to an already-running browser. This guide covers all launch
options and their trade-offs.

## Browser detection

When you call `CDPClient.launch()`, cdpwave searches for an installed
browser in the following order:

1. **`browser_path` argument** — if provided, uses this path directly.
2. **`CDPWAVE_BROWSER_PATH` env var** — falls back to this if set.
3. **System detection** — scans common install locations for Chrome,
   Edge, and Brave on Windows, macOS, and Linux.

If no browser is found, `BrowserNotFoundError` is raised.

### Supported browsers

| Browser | Windows | macOS | Linux |
|---|---|---|---|
| Chrome | Yes | Yes | Yes |
| Edge | Yes | Yes | Yes |
| Brave | Yes | Yes | Yes |

## Launch headless

The simplest way to start — no visible window, ideal for automation:

```python
from cdpwave import CDPClient

client = await CDPClient.launch(headless=True)
```

This launches the browser with `--headless=new` (the modern headless
mode), connects via WebSocket, and returns a `CDPClient`.

### Headless vs headed

| Mode | `headless` | Visible | Use case |
|---|---|---|---|
| Headless | `True` | No | Automation, CI, scraping |
| Headed | `False` | Yes | Debugging, visual inspection |

Headless mode is faster and uses less memory. Use headed mode when you
need to see what the browser is doing — for example, debugging a
navigation issue or verifying visual output.

## Launch headed

For debugging, launch with a visible window:

```python
client = await CDPClient.launch(headless=False)
```

The browser window appears on your desktop. You can interact with it
manually while cdpwave controls it programmatically.

## Custom browser path

Specify a browser binary explicitly — useful for portable installs or
specific browser versions:

```python
client = await CDPClient.launch(browser_path="/usr/bin/google-chrome")
```

Or set the `CDPWAVE_BROWSER_PATH` environment variable:

```bash
export CDPWAVE_BROWSER_PATH=/path/to/chrome
```

```python
client = await CDPClient.launch()  # uses env var
```

## Custom port

By default, cdpwave picks a free port automatically. To use a specific
port (useful for debugging or when firewall rules apply):

```python
client = await CDPClient.launch(port=9222)
```

If the port is already in use, the launch will fail with
`LaunchTimeoutError`.

## Extra arguments

Pass additional Chrome command-line flags:

```python
client = await CDPClient.launch(
    extra_args=[
        "--disable-gpu",
        "--window-size=1920,1080",
        "--lang=en-US",
    ],
)
```

### Common flags

| Flag | Purpose |
|---|---|
| `--disable-gpu` | Disable GPU acceleration (useful in containers) |
| `--window-size=W,H` | Set initial window dimensions |
| `--disable-extensions` | Disable all extensions |
| `--disable-popup-blocking` | Allow popups |
| `--start-maximized` | Maximize window on launch |
| `--auto-open-devtools-for-tabs` | Open DevTools for each tab |
| `--proxy-server=host:port` | Use a proxy server |

!!! warning "Conflicting flags"
    Don't pass `--remote-debugging-port` or `--headless` — cdpwave
    manages these internally. Conflicting values may cause unexpected
    behavior.

## User data directory

Use a persistent profile to preserve cookies, localStorage, and
extensions between sessions:

```python
client = await CDPClient.launch(user_data_dir="/tmp/my-profile")
```

If omitted, a temporary directory is created and cleaned up on close.
This is the recommended approach for most automation tasks — a fresh
profile ensures consistent results.

### When to use a persistent profile

- **Login sessions** — preserve authentication across runs.
- **Extension testing** — load extensions that persist state.
- **Performance** — avoid re-initializing the profile on each run.

### When to use a temporary profile

- **Testing** — ensure a clean state every run.
- **Scraping** — avoid cookie consent dialogs and cached data.
- **CI** — reproducible results across environments.

## Launch timeout

Control how long to wait for the browser to start:

```python
client = await CDPClient.launch(timeout=30.0)  # default: 10.0
```

If the browser doesn't respond within the timeout, raises
`LaunchTimeoutError`. Increase the timeout for slow systems or when
loading a large persistent profile.

## Connect to an existing browser

If Chrome is already running with `--remote-debugging-port=9222`:

```python
client = await CDPClient.connect(host="localhost", port=9222)
```

This uses HTTP discovery (`/json/version`) to find the WebSocket
endpoint and connects to it. No browser process is managed by cdpwave
in this mode — you're responsible for starting and stopping the
browser.

### When to use connect vs launch

| Mode | Method | Process management | Use case |
|---|---|---|---|
| Launch | `CDPClient.launch()` | cdpwave manages | Most automation |
| Connect | `CDPClient.connect()` | You manage | Attach to existing browser |

Use `connect` when:

- The browser is already running (e.g., user's Chrome with a profile).
- You need a specific browser configuration that cdpwave's launcher
  doesn't support.
- You're running in an environment where process spawning is
  restricted.

## Context manager

Always use `async with` for guaranteed cleanup:

```python
async with await CDPClient.launch(headless=True) as client:
    session = await client.new_page("https://example.com")
    # work with session
    await session.close()
# Browser terminated, WebSocket closed, temp dir removed
```

Even if an exception occurs, cleanup is guaranteed:

- The browser process is terminated.
- The WebSocket connection is closed.
- The temporary user data directory is removed (if applicable).

### Manual cleanup

If you don't use the context manager, call `close()` explicitly:

```python
client = await CDPClient.launch(headless=True)
try:
    session = await client.new_page()
    # work with session
finally:
    await client.close()
```

## CI environments

cdpwave automatically adds `--no-sandbox` when it detects CI
environments via these env vars: `CI`, `GITHUB_ACTIONS`, `GITLAB_CI`,
`JENKINS_URL`.

### Docker considerations

In Docker containers, you may also need:

- `--disable-gpu` — GPU acceleration isn't available in containers.
- `--disable-dev-shm-usage` — avoid `/dev/shm` exhaustion. cdpwave
  adds this automatically when `/dev/shm` is small.
- `--ipc=host` — shared memory for rendering (Docker run flag, not
  Chrome flag).

See [Headless & Docker](../cookbook/headless.md) for Docker-specific
configuration and Dockerfile examples.

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(
        headless=True,
        extra_args=["--window-size=1920,1080"],
        timeout=15.0,
    ) as client:
        session = await client.new_page("https://example.com")
        await session.page.enable()

        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        print(f"Title: {result['result']['value']}")

        await session.close()

asyncio.run(main())
```
