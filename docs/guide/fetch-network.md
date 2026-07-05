# Fetch & Network Interception

cdpwave provides full coverage of the `Fetch` and `Network` domains for
request interception, mocking, blocking, and network condition emulation.

## Fetch vs Network

The `Fetch` and `Network` domains serve different purposes:

| Aspect | `Fetch` | `Network` |
|---|---|---|
| Purpose | Intercept and modify requests | Monitor and inspect traffic |
| Control | Pause, modify, mock, block | Observe, query, block by URL |
| Overhead | High (pauses every matching request) | Low (passive observation) |
| Use case | Mocking APIs, modifying headers | Logging, analytics, cookie management |

Use `Fetch` when you need to **change** what the browser sends or
receives. Use `Network` when you need to **observe** what the browser
sends or receives.

## Fetch domain

The `Fetch` domain intercepts requests at the network layer. When a
request matches your patterns, the browser **pauses** it and sends a
`Fetch.requestPaused` event. You must then either continue, fulfill,
or fail the request — otherwise it hangs indefinitely.

### Request stages

| Stage | `requestStage` | When it pauses |
|---|---|---|
| Before sending | `"Request"` | Before the request hits the network |
| After response headers | `"Response"` | After headers arrive, before body |

### Enabling Fetch interception

```python
await session.fetch.enable(
    patterns=[
        {"urlPattern": "*://api.example.com/*", "requestStage": "Request"},
    ],
)
```

`patterns` is a list of match objects:

- **`urlPattern`** — glob pattern (`*` matches any chars). Use
  `*://domain/*` to match all requests to a domain.
- **`requestStage`** — `"Request"` to intercept before sending,
  `"Response"` to intercept after headers arrive.

!!! warning "Every matching request is paused"
    If you enable Fetch with a broad pattern, **every** matching
    request will hang until you respond. Always handle
    `Fetch.requestPaused` events and call `continue_request`,
    `fulfill_request`, or `fail_request` for each one.

### Intercepting requests

Listen for `Fetch.requestPaused` events and decide whether to
continue, modify, or block each request:

```python
import asyncio
from cdpwave import CDPSession

async def handle_requests(session: CDPSession) -> None:
    async def on_request_paused(event: dict) -> None:
        request = event["request"]
        url = request["url"]

        if "api.example.com/blocked" in url:
            # Block the request
            await session.fetch.fail_request(
                request_id=event["requestId"],
                error_reason="Failed",
            )
        elif "api.example.com/mock" in url:
            # Return a mock response
            await session.fetch.fulfill_request(
                request_id=event["requestId"],
                status_code=200,
                response_headers=[{"name": "Content-Type", "value": "application/json"}],
                body='{"mocked": true}',
            )
        else:
            # Let the request proceed normally
            await session.fetch.continue_request(
                request_id=event["requestId"],
            )

    session.on("Fetch.requestPaused", on_request_paused)
    await session.fetch.enable(
        patterns=[{"urlPattern": "*://api.example.com/*"}],
    )
```

### Three actions for a paused request

| Action | Method | Effect |
|---|---|---|
| Continue | `continue_request()` | Let request proceed (optionally modified) |
| Fulfill | `fulfill_request()` | Return a synthetic response |
| Fail | `fail_request()` | Cancel with an error |

### Modifying requests

Change the URL, method, headers, or POST data before the request
reaches the network:

```python
async def on_request_paused(event: dict) -> None:
    await session.fetch.continue_request(
        request_id=event["requestId"],
        url="https://api.example.com/v2/endpoint",
        method="POST",
        headers=[{"name": "Authorization", "value": "Bearer token123"}],
        post_data='{"key": "value"}',
    )
```

Only the fields you provide are overridden — others keep their
original values.

### Mocking responses

Return a synthetic response without hitting the network:

```python
await session.fetch.fulfill_request(
    request_id=event["requestId"],
    status_code=200,
    response_headers=[
        {"name": "Content-Type", "value": "application/json"},
        {"name": "Access-Control-Allow-Origin", "value": "*"},
    ],
    body='{"users": [{"id": 1, "name": "Alice"}]}',
)
```

!!! note "Body encoding"
    The `body` parameter must be a base64-encoded string. cdpwave
    handles the encoding automatically — pass plain text and it will
    be encoded for you.

### Continuing with auth

Provide credentials for a 401 response:

```python
await session.fetch.continue_with_auth(
    request_id=event["requestId"],
    auth_challenge_response={
        "response": "ProvideCredentials",
        "username": "user",
        "password": "pass",
    },
)
```

Auth response types:

- **`"Default"`** — cancel the auth challenge.
- **`"CancelAuth"`** — cancel and don't retry.
- **`"ProvideCredentials"`** — supply username/password.

### Getting request POST data

Retrieve the POST data of a paused request:

```python
post_data = await session.fetch.get_request_post_data(
    request_id=event["requestId"],
)
print(post_data["postData"])
```

### Response body as stream

Take the response body as a stream for large responses:

```python
stream = await session.fetch.take_response_body_as_stream(
    request_id=event["requestId"],
)
# Read the stream with IO.read
data = await session.io.read(handle=stream["stream"], offset=0, size=1024)
```

### Disabling Fetch

```python
await session.fetch.disable()
```

After disabling, requests are no longer paused. Always disable when
done to avoid hanging requests.

## Network domain

The `Network` domain provides passive monitoring and management of
network activity. Unlike `Fetch`, it doesn't pause requests — it
observes them and lets you query data after the fact.

### Enable network events

```python
await session.network.enable(
    max_post_data_size=1024 * 1024,  # 1MB
)
```

`max_post_data_size` controls how much POST data is included in
`Network.requestWillBeSent` events. Set to `0` to exclude POST data
entirely.

### Request lifecycle events

```
requestWillBeSent → responseReceived → loadingFinished
                                              ↘ loadingFailed
```

| Event | When | Key fields |
|---|---|---|
| `requestWillBeSent` | Request about to be sent | `request.method`, `request.url`, `request.headers` |
| `responseReceived` | Response headers received | `response.status`, `response.headers`, `response.mimeType` |
| `loadingFinished` | Response body fully downloaded | `requestId` |
| `loadingFailed` | Request failed | `errorText`, `canceled` |

### Listen to requests

```python
async def on_request(event: dict) -> None:
    print(f"→ {event['request']['method']} {event['request']['url']}")

async def on_response(event: dict) -> None:
    print(f"← {event['response']['status']} {event['response']['url']}")

session.on("Network.requestWillBeSent", on_request)
session.on("Network.responseReceived", on_response)
```

### Get response body

Fetch the response body after `loadingFinished`:

```python
body = await session.network.get_response_body(request_id="req123")
print(body["body"])  # base64-encoded
```

!!! note "Timing"
    You can only get the response body after `loadingFinished` has
    fired. Calling it before will return an error.

### Get request POST data

```python
post = await session.network.get_request_post_data(request_id="req123")
print(post["postData"])
```

## Cookies

### Get all cookies

```python
cookies = await session.network.get_all_cookies()
for cookie in cookies["cookies"]:
    print(f"{cookie['name']}={cookie['value']} domain={cookie['domain']}")
```

`get_all_cookies()` returns cookies from all contexts. Each cookie
has `name`, `value`, `domain`, `path`, `secure`, `httpOnly`,
`sameSite`, and `expires`.

### Set a cookie

```python
await session.network.set_cookie(
    name="session",
    value="abc123",
    domain="example.com",
    path="/",
    secure=True,
    http_only=True,
    same_site="Lax",
)
```

### Clear cookies

```python
await session.network.clear_browser_cookies()
```

This clears **all** cookies in the browser. Use with caution in
multi-tab scenarios.

## URL blocking

Block specific URLs from loading — a simpler alternative to Fetch
interception when you only need to block:

```python
await session.network.set_blocked_urls([
    "*://ads.example.com/*",
    "*://tracker.example.com/*",
    "*://*.doubleclick.net/*",
])
```

To unblock:

```python
await session.network.set_blocked_urls([])
```

## Service worker bypass

Bypass service workers for all network requests:

```python
await session.network.set_bypass_service_worker(True)
```

This forces requests to go directly to the network, ignoring any
service worker that might intercept them.

## Network conditions

Emulate offline, slow 3G, or custom conditions:

```python
# Offline
await session.network.emulate_network_conditions(
    offline=True,
    latency=0,
    download_throughput=-1,
    upload_throughput=-1,
)

# Slow 3G
await session.network.emulate_network_conditions(
    offline=False,
    latency=400,  # ms
    download_throughput=500 * 1024 / 8,  # 500 Kbps
    upload_throughput=500 * 1024 / 8,
)

# Reset to normal
await session.network.emulate_network_conditions(
    offline=False,
    latency=0,
    download_throughput=-1,  # -1 = unlimited
    upload_throughput=-1,
)
```

Throughput is in bytes per second. Use `-1` for unlimited.

## Cache

Disable cache (forces all requests to hit the network):

```python
await session.network.set_cache_disabled(True)
```

This is equivalent to DevTools' "Disable cache" checkbox. Useful for
ensuring fresh data during testing.

## Loading network resources

Load a resource directly without going through the page's fetch
pipeline:

```python
result = await session.network.load_network_resource(
    frame_id="frame1",
    url="https://example.com/data.json",
    options={"disableCache": True},
)
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.network.enable()
        await session.page.enable()

        # Block ads
        await session.network.set_blocked_urls([
            "*://*.doubleclick.net/*",
            "*://ads.example.com/*",
        ])

        # Intercept API calls
        async def on_request_paused(event: dict) -> None:
            url = event["request"]["url"]

            if "/api/mock" in url:
                await session.fetch.fulfill_request(
                    request_id=event["requestId"],
                    status_code=200,
                    response_headers=[
                        {"name": "Content-Type", "value": "application/json"}
                    ],
                    body='{"intercepted": true}',
                )
            else:
                await session.fetch.continue_request(
                    request_id=event["requestId"],
                )

        session.on("Fetch.requestPaused", on_request_paused)
        await session.fetch.enable(
            patterns=[{"urlPattern": "*://api.example.com/*"}],
        )

        # Log network activity
        requests: list[dict] = []

        async def on_request(event: dict) -> None:
            requests.append(event)

        session.on("Network.requestWillBeSent", on_request)

        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=15.0)

        print(f"Captured {len(requests)} requests")

        await session.fetch.disable()
        await session.close()

asyncio.run(main())
```
