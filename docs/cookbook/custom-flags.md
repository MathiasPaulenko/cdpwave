# Custom Flags

## Extra arguments

Pass additional Chrome command-line flags via `extra_args`:

```python
client = await CDPClient.launch(
    extra_args=[
        "--disable-gpu",
        "--window-size=1920,1080",
        "--lang=en-US",
    ],
)
```

## Common flags

| Flag | Description |
|---|---|
| `--disable-gpu` | Disable GPU acceleration |
| `--disable-dev-shm-usage` | Use `/tmp` instead of `/dev/shm` |
| `--no-sandbox` | Disable sandbox (CI/Docker) |
| `--window-size=W,H` | Set initial window size |
| `--lang=xx-XX` | Set browser language |
| `--proxy-server=host:port` | Use a proxy |
| `--user-agent=...` | Set custom user agent |
| `--incognito` | Launch in incognito mode |
| `--mute-audio` | Mute audio output |
| `--disable-extensions` | Disable all extensions |

## Environment variables

Override browser detection without changing code:

| Variable | Description |
|---|---|
| `CDPWAVE_BROWSER_PATH` | Path to any Chromium-based browser |
| `CDPWAVE_CHROME_PATH` | Path to Chrome |
| `CDPWAVE_EDGE_PATH` | Path to Edge |
| `CDPWAVE_BRAVE_PATH` | Path to Brave |
| `CDPWAVE_CHROMIUM_PATH` | Path to Chromium |

## Proxy example

```python
client = await CDPClient.launch(
    extra_args=["--proxy-server=http://proxy.example.com:8080"],
)
```

## Incognito

```python
client = await CDPClient.launch(
    extra_args=["--incognito"],
)
```

## Custom user data directory

Use a persistent profile across sessions:

```python
client = await CDPClient.launch(
    user_data_dir="/path/to/profile",
)
```

When omitted, a temporary directory is created and cleaned up automatically on `close()`.
