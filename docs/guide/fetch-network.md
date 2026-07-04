# Fetch & Network Interception

cdpwave provides full coverage of the `Fetch` and `Network` domains for
request interception, mocking, blocking, and network condition emulation.

## Enabling Fetch interception

```python
await session.fetch.enable(
    patterns=[
        {"urlPattern": "*://api.example.com/*", "requestStage": "Request"},
    ],
)
```

## Intercepting requests

Listen for `Fetch.requestPaused` events and decide whether to continue,
modify, or block each request:

```python
import asyncio
from cdpwave import CDPSession

async def handle_requests(session: CDPSession) -> None:
    paused = asyncio.Event()

    async def on_request_paused(event: dict) -> None:
        request = event["request"]
        url = request["url"]

        if "api.example.com/blocked" in url:
            await session.fetch.fail_request(
                request_id=event["requestId"],
                error_reason="Failed",
            )
        elif "api.example.com/mock" in url:
            await session.fetch.fulfill_request(
                request_id=event["requestId"],
                status_code=200,
                response_headers=[{"name": "Content-Type", "value": "application/json"}],
                body='{"mocked": true}',
            )
        else:
            await session.fetch.continue_request(
                request_id=event["requestId"],
            )

    session.on("Fetch.requestPaused", on_request_paused)
    await session.fetch.enable(
        patterns=[{"urlPattern": "*://api.example.com/*"}],
    )
```

## Modifying requests

Change the URL, method, headers, or POST data:

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

## Continuing with auth

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

## Getting request POST data

```python
post_data = await session.fetch.get_request_post_data(
    request_id=event["requestId"],
)
print(post_data["postData"])
```

## Response body as stream

```python
stream = await session.fetch.take_response_body_as_stream(
    request_id=event["requestId"],
)
# Read the stream with IO.read
data = await session.io.read(handle=stream["stream"], offset=0, size=1024)
```

## Disabling Fetch

```python
await session.fetch.disable()
```

---

## Network monitoring

### Enable network events

```python
await session.network.enable(
    max_post_data_size=1024 * 1024,  # 1MB
)
```

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

```python
body = await session.network.get_response_body(request_id="req123")
print(body["body"])
```

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

## URL blocking

Block specific URLs from loading:

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

# Reset
await session.network.emulate_network_conditions(
    offline=False,
    latency=0,
    download_throughput=-1,
    upload_throughput=-1,
)
```

## Cache

Disable cache (forces all requests to hit the network):

```python
await session.network.set_cache_disabled(True)
```

## Loading network resources

Load a resource directly without going through the page:

```python
result = await session.network.load_network_resource(
    frame_id="frame1",
    url="https://example.com/data.json",
    options={"disableCache": True},
)
```
