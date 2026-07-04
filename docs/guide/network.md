# Network

## Enable network monitoring

```python
await session.network.enable()
```

## Monitor requests

```python
async def on_request(params: dict) -> None:
    req = params["request"]
    print(f"{req['method']} {req['url']}")

session.on("Network.requestWillBeSent", on_request)
```

## Monitor responses

```python
async def on_response(params: dict) -> None:
    resp = params["response"]
    print(f"{resp['status']} {resp['mimeType']}")

session.on("Network.responseReceived", on_response)
```

## Cookies

### Get cookies

```python
result = await session.network.get_cookies(urls=["https://example.com"])
for cookie in result["cookies"]:
    print(f"{cookie['name']}={cookie['value']}")
```

### Set a cookie

```python
await session.network.set_cookie(
    name="session_id",
    value="abc123",
    url="https://example.com",
    secure=True,
    http_only=True,
)
```

### Delete a cookie

```python
await session.network.delete_cookies("session_id", url="https://example.com")
```

### Clear all cookies

```python
await session.network.clear_browser_cookies()
```

## User agent override

```python
await session.network.set_user_agent_override(
    "cdpwave-bot/1.0",
    accept_language="en-US",
    platform="TestOS",
)
```

## Cache control

Disable cache:

```python
await session.network.set_cache_disabled(True)
```

Clear browser cache:

```python
await session.network.clear_browser_cache()
```

## Emulate network conditions

```python
await session.network.emulate_network_conditions(
    offline=False,
    latency=200,  # ms
    download_throughput=500_000,  # bytes/s
    upload_throughput=500_000,
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
                "status": None,
            }

        async def on_response(params: dict) -> None:
            req_id = params["requestId"]
            if req_id in requests:
                requests[req_id]["status"] = params["response"]["status"]

        session.on("Network.requestWillBeSent", on_request)
        session.on("Network.responseReceived", on_response)

        await session.page.navigate("https://example.com")
        await asyncio.sleep(2)

        for info in requests.values():
            print(f"{info['method']:6s} {info.get('status', '?')} {info['url']}")

        await session.close()

asyncio.run(main())
```
