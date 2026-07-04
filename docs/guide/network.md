# Network

The Network domain provides visibility into all HTTP traffic generated
by the page. You can monitor requests and responses, read response
bodies, manage cookies, control cache, block URLs, and emulate network
conditions.

## Prerequisites

Enable the Network domain before monitoring traffic:

```python
await session.network.enable()
```

`Network.enable` activates request/response events. You can optionally
pass `max_total_buffer_size`, `max_resource_buffer_size`, and
`max_post_data_size` to control buffer limits.

## The request lifecycle

When a page loads, the browser generates a sequence of network events
for each resource. Understanding this sequence is key to working with
network data:

```
Network.requestWillBeSent
    ↓
Network.requestWillBeSentExtraInfo  (optional, includes cookies)
    ↓
Network.responseReceived
    ↓
Network.loadingFinished   OR   Network.loadingFailed
```

- **`requestWillBeSent`** — fires when a request is about to be sent.
  Contains the URL, method, headers, and request ID.
- **`responseReceived`** — fires when response headers are received.
  Contains status, headers, MIME type, and timing.
- **`loadingFinished`** — fires when the response body is fully
  downloaded. Call `get_response_body` after this.
- **`loadingFailed`** — fires if the request fails (network error,
  blocked, cancelled).

Each request has a unique `requestId` that appears in all related
events. Use it to correlate requests with responses and bodies.

## Monitor requests

```python
async def on_request(params: dict) -> None:
    req = params["request"]
    print(f"{req['method']} {req['url']}")

session.on("Network.requestWillBeSent", on_request)
```

The `request` object contains:

- **`url`** — the request URL.
- **`method`** — HTTP method (GET, POST, etc.).
- **`headers`** — dict of request headers.
- **`postData`** — request body (for POST/PUT, if within buffer size).
- **`initialPriority`** — resource priority (`VeryHigh`, `High`,
  `Medium`, `Low`, `VeryLow`).
- **`resourceType`** — type hint (`Document`, `Stylesheet`, `Image`,
  `Script`, `XHR`, `Fetch`, etc.).

### Request initiator

The `initiator` field tells you what triggered the request:

```python
async def on_request(params: dict) -> None:
    init = params["initiator"]
    print(f"  Type: {init['type']}")  # "script", "parser", "preload", "other"
    if "stack" in init:
        print(f"  Call stack: {init['stack']['callFrames'][0]['functionName']}")
```

## Monitor responses

```python
async def on_response(params: dict) -> None:
    resp = params["response"]
    print(f"{resp['status']} {resp['mimeType']} {resp['url']}")

session.on("Network.responseReceived", on_response)
```

The `response` object contains:

- **`url`** — the response URL (may differ from request URL after
  redirects).
- **`status`** — HTTP status code (200, 404, 500, etc.).
- **`statusText`** — status text ("OK", "Not Found").
- **`headers`** — dict of response headers.
- **`mimeType`** — MIME type (`text/html`, `application/json`, etc.).
- **`remoteIPAddress`** — server IP address.
- **`timing`** — detailed timing breakdown (DNS, connect, send, wait,
  receive).

### Response timing

The `timing` object provides a waterfall breakdown:

```python
async def on_response(params: dict) -> None:
    timing = params["response"].get("timing", {})
    if timing:
        print(f"  DNS:     {timing.get('dnsLookupTime', 0):.0f}ms")
        print(f"  Connect: {timing.get('connectTime', 0):.0f}ms")
        print(f"  Send:    {timing.get('sendStart', 0):.0f}ms")
        print(f"  Wait:    {timing.get('receiveHeadersEnd', 0):.0f}ms")
```

## Read response bodies

After `Network.loadingFinished` fires, you can fetch the response body:

```python
bodies: dict[str, str] = {}

async def on_finished(params: dict) -> None:
    req_id = params["requestId"]
    try:
        body = await session.network.get_response_body(req_id)
        bodies[req_id] = body["body"]
        if body.get("base64Encoded"):
            import base64
            data = base64.b64decode(body["body"])
        else:
            data = body["body"].encode("utf-8")
        print(f"  Body: {len(data)} bytes")
    except Exception:
        pass  # body may be evicted from buffer

session.on("Network.loadingFinished", on_finished)
```

!!! warning "Buffer eviction"
    Response bodies are kept in a buffer with limited size. If the page
    makes many requests, older bodies may be evicted before you read
    them. Increase the buffer with `max_resource_buffer_size` in
    `Network.enable`.

## Cookies

### Get cookies

```python
result = await session.network.get_cookies(urls=["https://example.com"])
for cookie in result["cookies"]:
    print(f"{cookie['name']}={cookie['value']}")
```

Without `urls`, returns cookies for the current page's URL. Pass
multiple URLs to get cookies for multiple domains.

Each cookie contains:

- **`name`**, **`value`** — cookie name and value.
- **`domain`** — domain the cookie applies to.
- **`path`** — path scope.
- **`expires`** — expiration timestamp (Unix epoch seconds). `-1` for
  session cookies.
- **`size`** — cookie size in bytes.
- **`httpOnly`** — whether the cookie is HTTP-only.
- **`secure`** — whether the cookie requires HTTPS.
- **`sameSite`** — SameSite policy (`"Strict"`, `"Lax"`, `"None"`).

### Set a cookie

```python
await session.network.set_cookie(
    name="session_id",
    value="abc123",
    url="https://example.com",
    secure=True,
    http_only=True,
    same_site="Lax",
)
```

You must provide either `url` or both `domain` and `path`. The `url`
approach is simpler — the browser derives domain and path from it.

### Delete a cookie

```python
await session.network.delete_cookies("session_id", url="https://example.com")
```

### Clear all cookies

```python
await session.network.clear_browser_cookies()
```

!!! warning "This clears ALL cookies"
    `clear_browser_cookies` removes every cookie in the browser, not
    just for the current page. Use `delete_cookies` for targeted
    removal.

### Get all cookies (all domains)

```python
result = await session.network.get_all_cookies()
for cookie in result["cookies"]:
    print(f"{cookie['domain']} {cookie['name']}={cookie['value']}")
```

## Headers

### Extra HTTP headers

Add custom headers to all requests:

```python
await session.network.set_extra_http_headers({
    "X-Custom-Header": "cdpwave",
    "Authorization": "Bearer token123",
})
```

These headers are added to every request the page makes. Clear them
with an empty dict:

```python
await session.network.set_extra_http_headers({})
```

### User agent override

```python
await session.network.set_user_agent_override(
    "cdpwave-bot/1.0",
    accept_language="en-US",
    platform="TestOS",
)
```

The override applies to all requests and also changes
`navigator.userAgent` in JavaScript.

## Cache control

### Disable cache

```python
await session.network.set_cache_disabled(True)
```

When cache is disabled, every request is sent to the server without
checking the local cache. This is equivalent to DevTools' "Disable
cache" checkbox.

### Clear browser cache

```python
await session.network.clear_browser_cache()
```

Removes all cached responses from the browser's HTTP cache.

## Request blocking

Block specific URLs from loading:

```python
await session.network.set_blocked_urls([
    "*.doubleclick.net/*",
    "https://ads.example.com/*",
    "*.css",  # block all stylesheets
])
```

Blocked requests fire `Network.loadingFailed` with
`params["blockedReason"]` set to `"InspectedByClient"`.

Clear the block list:

```python
await session.network.set_blocked_urls([])
```

## Network emulation

Simulate network conditions for testing:

```python
await session.network.emulate_network_conditions(
    offline=False,
    latency=200,  # ms
    download_throughput=500_000,  # bytes/s
    upload_throughput=500_000,
)
```

Parameters:

- **`offline`** — simulate complete disconnection.
- **`latency`** — added delay per request in milliseconds.
- **`download_throughput`** — max download speed in bytes/s. `-1` for
  unlimited.
- **`upload_throughput`** — max upload speed in bytes/s.

Reset to normal:

```python
await session.network.emulate_network_conditions(
    offline=False,
    latency=0,
    download_throughput=-1,
    upload_throughput=-1,
)
```

## Full monitoring example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.network.enable()

        requests: dict[str, dict] = {}

        async def on_request(params: dict) -> None:
            requests[params["requestId"]] = {
                "url": params["request"]["url"],
                "method": params["request"]["method"],
                "type": params["type"],
                "status": None,
                "mime": None,
            }

        async def on_response(params: dict) -> None:
            req_id = params["requestId"]
            if req_id in requests:
                requests[req_id]["status"] = params["response"]["status"]
                requests[req_id]["mime"] = params["response"]["mimeType"]

        session.on("Network.requestWillBeSent", on_request)
        session.on("Network.responseReceived", on_response)

        await session.page.navigate("https://example.com")
        await asyncio.sleep(2)

        for info in requests.values():
            print(f"{info['method']:6s} {info.get('status', '?'):>3} {info['type']:>10} {info['url']}")

        await session.close()

asyncio.run(main())
```
