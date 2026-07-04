# Browser Launch

## Launch headless

The simplest way to start:

```python
from cdpwave import CDPClient

client = await CDPClient.launch(headless=True)
```

This detects an installed browser, launches it with `--headless=new`, and connects via WebSocket.

## Launch headed

For debugging, launch with a visible window:

```python
client = await CDPClient.launch(headless=False)
```

## Custom browser path

Specify a browser binary explicitly:

```python
client = await CDPClient.launch(browser_path="/usr/bin/google-chrome")
```

Or use the `CDPWAVE_BROWSER_PATH` environment variable.

## Custom port

By default, cdpwave picks a free port automatically. To use a specific port:

```python
client = await CDPClient.launch(port=9222)
```

## Extra arguments

Pass additional Chrome flags:

```python
client = await CDPClient.launch(
    extra_args=["--disable-gpu", "--window-size=1920,1080"],
)
```

## User data directory

Use a persistent profile:

```python
client = await CDPClient.launch(user_data_dir="/tmp/my-profile")
```

If omitted, a temporary directory is created and cleaned up on close.

## Launch timeout

Control how long to wait for the browser to start:

```python
client = await CDPClient.launch(timeout=30.0)  # default: 10.0
```

Raises `LaunchTimeoutError` if the browser doesn't respond in time.

## Connect to an existing browser

If Chrome is already running with `--remote-debugging-port=9222`:

```python
client = await CDPClient.connect(host="localhost", port=9222)
```

This uses HTTP discovery (`/json/version`) to find the WebSocket endpoint. No browser process is managed by cdpwave in this mode.

## Context manager

Always use `async with` for guaranteed cleanup:

```python
async with await CDPClient.launch(headless=True) as client:
    # work with client
    pass
# Browser terminated, WebSocket closed, temp dir removed
```

Even if an exception occurs, cleanup is guaranteed.

## CI environments

cdpwave automatically adds `--no-sandbox` when it detects CI environments (`CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, `JENKINS_URL`).

See [Headless & Docker](../cookbook/headless.md) for Docker-specific configuration.
