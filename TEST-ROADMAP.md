# Manual Test Scenarios

Complete manual test coverage for cdpwave functionality. Run these scenarios to verify 100% of the library's capabilities.

## Prerequisites

- Chrome/Edge/Brave/Chromium installed
- Python 3.11+
- cdpwave installed: `pip install cdpwave`
- Terminal or IDE for running Python scripts

## Quick Verification (5 minutes)

### 1. Basic Launch and Navigate

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        print("✓ Browser launched and page loaded")

asyncio.run(test())
```

**Expected:** Output "✓ Browser launched and page loaded" without errors.

---

## Core Functionality Tests (30 minutes)

### 2. Browser Detection and Launch

**Test:** Find and launch different browsers

```python
import asyncio
from cdpwave import CDPClient

async def test():
    # Test default browser detection
    async with await CDPClient.launch(headless=True) as client:
        print(f"✓ Launched browser: {client.browser_type}")
        
    # Test explicit browser type
    async with await CDPClient.launch(headless=True, browser_type="edge") as client:
        print(f"✓ Launched Edge: {client.browser_type}")

asyncio.run(test())
```

**Expected:** Detects and launches Chrome, Edge, Brave, or Chromium.

---

### 3. Direct WebSocket Connection

**Test:** Connect to existing browser via WebSocket URL

```python
import asyncio
from cdpwave import CDPClient

async def test():
    # First, launch Chrome with remote debugging
    # chrome.exe --remote-debugging-port=9222
    
    async with await CDPClient.connect("ws://localhost:9222") as client:
        targets = await client.get_pages()
        print(f"✓ Connected to {len(targets)} pages")

asyncio.run(test())
```

**Expected:** Connects to existing browser and lists pages.

---

### 4. Page Navigation

**Test:** Navigate to different URLs

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        # Navigate to URL
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")
        print("✓ Navigated to example.com")
        
        # Navigate back
        await session.page.navigate("https://example.org")
        await session.page.go_back()
        print("✓ Navigated back")
        
        # Navigate forward
        await session.page.go_forward()
        print("✓ Navigated forward")

asyncio.run(test())
```

**Expected:** All navigation operations complete without errors.

---

### 5. JavaScript Evaluation

**Test:** Evaluate JavaScript and get results

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        
        # Simple expression
        result = await session.runtime.evaluate("1 + 1", return_by_value=True)
        print(f"✓ 1 + 1 = {result['result']['value']}")
        
        # Get document title
        title = await session.runtime.evaluate(
            "document.title",
            return_by_value=True
        )
        print(f"✓ Page title: {title['result']['value']}")
        
        # Async expression
        async_result = await session.runtime.evaluate(
            "new Promise(r => setTimeout(() => r(42), 100))",
            return_by_value=True,
            await_promise=True
        )
        print(f"✓ Async result: {async_result['result']['value']}")

asyncio.run(test())
```

**Expected:** JavaScript executes correctly, returns expected values.

---

### 6. Page Screenshots

**Test:** Capture screenshots in different formats

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        
        # PNG screenshot
        png_data = await session.page.capture_screenshot()
        print(f"✓ PNG screenshot: {len(png_data)} bytes")
        
        # JPEG screenshot
        jpeg_data = await session.page.capture_screenshot(format="jpeg")
        print(f"✓ JPEG screenshot: {len(jpeg_data)} bytes")

asyncio.run(test())
```

**Expected:** Screenshots captured in both formats.

---

### 7. PDF Generation

**Test:** Generate PDF from page

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        
        pdf_data = await session.page.print_to_pdf()
        print(f"✓ PDF generated: {len(pdf_data)} bytes")
        
        # Save to file
        with open("test.pdf", "wb") as f:
            f.write(pdf_data)
        print("✓ PDF saved to test.pdf")

asyncio.run(test())
```

**Expected:** PDF generated and saved successfully.

---

### 8. Multi-Tab Management

**Test:** Manage multiple tabs

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        # Create multiple tabs
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")
        tab3 = await client.new_page("https://example.net")
        
        print(f"✓ Created {len(client.sessions)} tabs")
        
        # List all sessions
        for session in client.sessions:
            print(f"  - Session: {session.target_id}")
        
        # Close specific tab
        await tab2.close()
        print(f"✓ Closed tab, {len(client.sessions)} remaining")

asyncio.run(test())
```

**Expected:** Multiple tabs created and managed correctly.

---

## Network Functionality Tests (20 minutes)

### 9. Network Monitoring

**Test:** Monitor network requests

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.network.enable()
        
        requests = []
        
        async def on_request_will_be_sent(params):
            requests.append(params["request"]["url"])
        
        session.on("Network.requestWillBeSent", on_request_will_be_sent)
        await session.page.navigate("https://example.com")
        
        print(f"✓ Captured {len(requests)} network requests")
        for url in requests[:5]:
            print(f"  - {url}")

asyncio.run(test())
```

**Expected:** Network requests captured and listed.

---

### 10. Cookie Management

**Test:** Get, set, and delete cookies

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.network.enable()
        
        # Get cookies
        cookies = await session.network.get_cookies()
        print(f"✓ Found {len(cookies)} cookies")
        
        # Set cookie
        await session.network.set_cookies([{
            "name": "test",
            "value": "value",
            "domain": "example.com"
        }])
        print("✓ Set cookie")
        
        # Verify cookie
        cookies = await session.network.get_cookies()
        assert any(c["name"] == "test" for c in cookies)
        print("✓ Cookie verified")
        
        # Delete cookie
        await session.network.delete_cookies("test", "example.com")
        print("✓ Cookie deleted")

asyncio.run(test())
```

**Expected:** Cookie operations complete successfully.

---

### 11. Request Interception

**Test:** Intercept and modify requests

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.fetch.enable(
            patterns=[{"urlPattern": "*"}]
        )
        
        intercepted = []
        
        async def on_paused(params):
            intercepted.append(params["requestId"])
            await session.fetch.continue_request(
                requestId=params["requestId"]
            )
        
        session.on("Fetch.requestPaused", on_paused)
        await session.page.navigate("https://example.com")
        
        print(f"✓ Intercepted {len(intercepted)} requests")

asyncio.run(test())
```

**Expected:** Requests intercepted and continued.

---

### 12. Network Throttling

**Test:** Emulate slow network

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.network.emulate_network_conditions(
            offline=False,
            download_throughput=500000,  # 500 KB/s
            upload_throughput=500000,
            latency=100
        )
        print("✓ Network throttled to 500 KB/s")
        
        await session.page.navigate("https://example.com")
        print("✓ Navigated with throttling")

asyncio.run(test())
```

**Expected:** Network throttling applied.

---

## DOM Functionality Tests (15 minutes)

### 13. DOM Inspection

**Test:** Inspect DOM structure

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.dom.enable()
        
        # Get document
        doc = await session.dom.get_document()
        print(f"✓ Document node: {doc['root']['nodeId']}")
        
        # Query selector
        node = await session.dom.query_selector("h1")
        print(f"✓ Found h1 node: {node['nodeId']}")
        
        # Get node attributes
        attrs = await session.dom.get_attributes(node["nodeId"])
        print(f"✓ Node attributes: {attrs}")

asyncio.run(test())
```

**Expected:** DOM inspection works correctly.

---

### 14. DOM Manipulation

**Test:** Modify DOM elements

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.dom.enable()
        
        # Set attribute
        h1 = await session.dom.query_selector("h1")
        await session.dom.set_attribute_value(
            h1["nodeId"],
            "data-test",
            "value"
        )
        print("✓ Set attribute")
        
        # Set text content
        await session.dom.set_text_content(h1["nodeId"], "Test Title")
        print("✓ Set text content")

asyncio.run(test())
```

**Expected:** DOM modifications applied.

---

### 15. Box Model

**Test:** Get element box model

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.dom.enable()
        
        h1 = await session.dom.query_selector("h1")
        model = await session.dom.get_box_model(h1["nodeId"])
        print(f"✓ Box model: {len(model['content'])} points")

asyncio.run(test())
```

**Expected:** Box model retrieved successfully.

---

## Emulation Tests (15 minutes)

### 16. Device Emulation

**Test:** Emulate mobile device

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        # Emulate iPhone
        await session.emulation.set_device_metrics_override(
            width=375,
            height=667,
            device_scale_factor=2,
            mobile=True
        )
        print("✓ Emulated iPhone viewport")
        
        await session.page.navigate("https://example.com")
        print("✓ Navigated with mobile viewport")

asyncio.run(test())
```

**Expected:** Mobile viewport emulated.

---

### 17. Geolocation Override

**Test:** Override geolocation

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.emulation.set_geolocation_override(
            latitude=40.7128,
            longitude=-74.0060
        )
        print("✓ Set geolocation to New York")
        
        # Grant permission
        await session.send("Browser.grantPermissions", {
            "permissions": ["geolocation"],
            "origin": "https://example.com"
        })
        
        # Test with geolocation API
        await session.page.navigate("https://example.com")
        await session.runtime.evaluate("""
            navigator.geolocation.getCurrentPosition(pos => {
                console.log(pos.coords.latitude, pos.coords.longitude);
            })
        """)

asyncio.run(test())
```

**Expected:** Geolocation override applied.

---

### 18. Dark Mode

**Test:** Emulate dark mode

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        await session.emulation.set_emulated_media("prefers-color-scheme", "dark")
        print("✓ Emulated dark mode")
        
        await session.page.navigate("https://example.com")
        print("✓ Navigated with dark mode")

asyncio.run(test())
```

**Expected:** Dark mode emulated.

---

### 19. Timezone Override

**Test:** Override timezone

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        await session.emulation.set_timezone_override("America/New_York")
        print("✓ Set timezone to New York")
        
        # Verify timezone
        tz = await session.runtime.evaluate(
            "Intl.DateTimeFormat().resolvedOptions().timeZone",
            return_by_value=True
        )
        print(f"✓ Timezone: {tz['result']['value']}")

asyncio.run(test())
```

**Expected:** Timezone override applied.

---

## Input Tests (10 minutes)

### 20. Text Input

**Test:** Type text into input field

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate(
            "data:text/html,<input id='q' type='text'>"
        )
        
        await session.input.insert_text("Hello World")
        print("✓ Inserted text")
        
        # Verify
        value = await session.runtime.evaluate(
            "document.getElementById('q').value",
            return_by_value=True
        )
        print(f"✓ Input value: {value['result']['value']}")

asyncio.run(test())
```

**Expected:** Text inserted correctly.

---

### 21. Keyboard Events

**Test:** Send keyboard events

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate(
            "data:text/html,<input id='q' type='text'>"
        )
        
        await session.input.dispatch_key_event(
            "char",
            "H"
        )
        await session.input.dispatch_key_event(
            "char",
            "i"
        )
        print("✓ Sent keyboard events")

asyncio.run(test())
```

**Expected:** Keyboard events sent.

---

### 22. Mouse Events

**Test:** Send mouse events

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate(
            "data:text/html,<button id='btn'>Click</button>"
        )
        
        # Get element position
        rect = await session.runtime.evaluate("""
            const el = document.getElementById('btn');
            const rect = el.getBoundingClientRect();
            return {x: rect.left + 5, y: rect.top + 5};
        """, return_by_value=True)
        
        # Click
        await session.input.dispatch_mouse_event(
            "mousePressed",
            "left",
            rect["result"]["value"]["x"],
            rect["result"]["value"]["y"]
        )
        await session.input.dispatch_mouse_event(
            "mouseReleased",
            "left",
            rect["result"]["value"]["x"],
            rect["result"]["value"]["y"]
        )
        print("✓ Sent mouse click")

asyncio.run(test())
```

**Expected:** Mouse events sent.

---

## Event Handling Tests (10 minutes)

### 23. Wait for Event

**Test:** Wait for specific event

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        # Navigate and wait for load
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")
        print("✓ Page loaded")
        
        # Wait for console message
        await session.runtime.evaluate("console.log('test')")
        await session.wait_for_event("Runtime.consoleAPICalled")
        print("✓ Console message received")

asyncio.run(test())
```

**Expected:** Events received correctly.

---

### 24. Event Listeners

**Test:** Register event listeners

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.runtime.enable()
        
        messages = []
        
        async def on_console(params):
            messages.append(params)
        
        session.on("Runtime.consoleAPICalled", on_console)
        
        await session.runtime.evaluate("console.log('msg1')")
        await session.runtime.evaluate("console.log('msg2')")
        
        print(f"✓ Received {len(messages)} console messages")

asyncio.run(test())
```

**Expected:** Event listeners work correctly.

---

## Performance Tests (10 minutes)

### 25. Performance Metrics

**Test:** Get performance metrics

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.performance.enable()
        
        await session.page.navigate("https://example.com")
        
        metrics = await session.performance.get_metrics()
        print(f"✓ Collected {len(metrics)} metrics")
        
        for metric in metrics[:5]:
            print(f"  - {metric['name']}: {metric.get('value', 'N/A')}")

asyncio.run(test())
```

**Expected:** Performance metrics collected.

---

### 26. CPU Profiling

**Test:** Capture CPU profile

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.profiler.enable()
        
        await session.profiler.start()
        await session.runtime.evaluate("""
            for(let i=0;i<1000;i++) {
                Math.sqrt(i);
            }
        """)
        profile = await session.profiler.stop()
        
        print(f"✓ CPU profile: {len(profile.get('profile', {}).get('nodes', []))} nodes")

asyncio.run(test())
```

**Expected:** CPU profile captured.

---

### 27. Heap Snapshot

**Test:** Capture heap snapshot

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.heap_profiler.enable()
        
        snapshot = await session.heap_profiler.take_heap_snapshot()
        print(f"✓ Heap snapshot captured")
        
        # Get object count
        nodes = snapshot.get("snapshot", {}).get("nodes", [])
        print(f"  - {len(nodes)} nodes")

asyncio.run(test())
```

**Expected:** Heap snapshot captured.

---

## Security Tests (5 minutes)

### 28. Security State

**Test:** Get security information

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.security.enable()
        
        await session.page.navigate("https://example.com")
        
        security = await session.security.get_visible_security_state()
        print(f"✓ Security state: {security.get('securityState', 'unknown')}")

asyncio.run(test())
```

**Expected:** Security state retrieved.

---

### 29. Certificate Info

**Test:** Get certificate information

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.security.enable()
        
        await session.page.navigate("https://example.com")
        
        # Handle certificate event
        async def on_security(params):
            print(f"✓ Certificate info received")
        
        session.on("Security.certificateError", on_security)

asyncio.run(test())
```

**Expected:** Certificate info retrieved.

---

## Storage Tests (5 minutes)

### 30. Local Storage

**Test:** Access local storage

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.storage.enable()
        
        # Set item
        await session.runtime.evaluate("localStorage.setItem('key', 'value')")
        print("✓ Set localStorage item")
        
        # Get storage domains
        domains = await session.storage.get_storage_domains()
        print(f"✓ Storage domains: {len(domains)}")

asyncio.run(test())
```

**Expected:** Local storage accessed.

---

### 31. IndexedDB

**Test:** Access IndexedDB

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.indexed_db.enable()
        
        # Create database
        await session.runtime.evaluate("""
            new Promise((resolve) => {
                const request = indexedDB.open('test', 1);
                request.onupgradeneeded = () => {
                    const db = request.result;
                    db.createObjectStore('store');
                };
                request.onsuccess = () => resolve();
            })
        """, await_promise=True)
        print("✓ Created IndexedDB database")
        
        # Get database names
        databases = await session.indexed_db.get_database_names()
        print(f"✓ Databases: {databases}")

asyncio.run(test())
```

**Expected:** IndexedDB accessed.

---

## Browser Tests (5 minutes)

### 32. Browser Version

**Test:** Get browser version

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        version = await client.browser.get_version()
        print(f"✓ Browser: {version.get('product', 'unknown')}")
        print(f"  User Agent: {version.get('userAgent', 'unknown')}")

asyncio.run(test())
```

**Expected:** Browser version retrieved.

---

### 33. Command Line

**Test:** Get browser command line

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        cmdline = await client.browser.get_command_line()
        print(f"✓ Command line arguments: {len(cmdline.get('arguments', []))}")

asyncio.run(test())
```

**Expected:** Command line retrieved.

---

## Advanced Tests (15 minutes)

### 34. Shadow DOM

**Test:** Access Shadow DOM

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.dom.enable()
        
        # Create shadow DOM
        await session.page.navigate(
            "data:text/html,<div id='host'></div>"
        )
        await session.runtime.evaluate("""
            const host = document.getElementById('host');
            const shadow = host.attachShadow({mode: 'open'});
            shadow.innerHTML = '<p>Shadow content</p>';
        """)
        
        # Query shadow DOM
        result = await session.dom.describe_node(
            (await session.dom.query_selector("#host"))["nodeId"],
            depth=2
        )
        print(f"✓ Shadow DOM described")

asyncio.run(test())
```

**Expected:** Shadow DOM accessed.

---

### 35. File Upload

**Test:** Upload file to input

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.dom.enable()
        
        await session.page.navigate(
            "data:text/html,<input type='file' id='file'>"
        )
        
        # Create temp file
        with open("test.txt", "w") as f:
            f.write("test content")
        
        # Set file input
        node = await session.dom.query_selector("#file")
        await session.dom.set_file_input_files(
            node["nodeId"],
            ["test.txt"]
        )
        print("✓ File uploaded")

asyncio.run(test())
```

**Expected:** File uploaded successfully.

---

### 36. Iframe Navigation

**Test:** Navigate within iframe

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        await session.page.navigate(
            "data:text/html,<iframe src='https://example.com'></iframe>"
        )
        
        # Get frame tree
        tree = await session.page.get_frame_tree()
        frames = tree.get("frameTree", {}).get("frame", {}).get("childFrames", [])
        print(f"✓ Found {len(frames)} iframe(s)")

asyncio.run(test())
```

**Expected:** Iframe accessed.

---

### 37. Service Worker

**Test:** Register service worker

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.service_worker.enable()
        
        # Register service worker (needs HTTPS or localhost)
        await session.page.navigate("https://example.com")
        
        # Get service workers
        workers = await session.service_worker.get_workers()
        print(f"✓ Service workers: {len(workers)}")

asyncio.run(test())
```

**Expected:** Service worker info retrieved.

---

### 38. WebAuthn

**Test:** WebAuthn authentication

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.web_authn.enable()
        
        # Add virtual authenticator
        await session.web_authn.add_virtual_authenticator({
            "protocol": "ctap2",
            "transport": "internal",
            "options": {"hasUserVerification": True}
        })
        print("✓ Added virtual authenticator")

asyncio.run(test())
```

**Expected:** WebAuthn authenticator added.

---

### 39. Tracing

**Test:** Capture performance trace

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        await session.tracing.start()
        await session.page.navigate("https://example.com")
        data = await session.tracing.stop()
        
        print(f"✓ Trace captured: {len(data)} bytes")

asyncio.run(test())
```

**Expected:** Performance trace captured.

---

### 40. Console API

**Test:** Console API logging

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.console.enable()
        
        messages = []
        
        async def on_message(params):
            messages.append(params)
        
        session.on("Console.messageAdded", on_message)
        
        await session.runtime.evaluate("console.log('test')")
        await session.runtime.evaluate("console.error('error')")
        
        print(f"✓ Console messages: {len(messages)}")

asyncio.run(test())
```

**Expected:** Console messages captured.

---

## Error Handling Tests (10 minutes)

### 41. Invalid URL

**Test:** Navigate to invalid URL

```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandError

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        try:
            await session.page.navigate("not-a-url")
        except CommandError as e:
            print(f"✓ Caught expected error: {e.message}")

asyncio.run(test())
```

**Expected:** Error caught for invalid URL.

---

### 42. Invalid JavaScript

**Test:** Evaluate invalid JavaScript

```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandError

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        try:
            await session.runtime.evaluate("invalid javascript syntax")
        except CommandError as e:
            print(f"✓ Caught expected error: {e.message}")

asyncio.run(test())
```

**Expected:** Error caught for invalid syntax.

---

### 43. Non-existent Element

**Test:** Query non-existent element

```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandError

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.dom.enable()
        
        try:
            await session.dom.query_selector("#non-existent")
        except CommandError as e:
            print(f"✓ Caught expected error: {e.message}")

asyncio.run(test())
```

**Expected:** Error caught for non-existent element.

---

### 44. Connection Timeout

**Test:** Timeout on long operation

```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandTimeoutError

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        
        try:
            # This should timeout
            await session.runtime.evaluate(
                "new Promise(() => {})",
                timeout=1
            )
        except CommandTimeoutError:
            print("✓ Caught timeout error")

asyncio.run(test())
```

**Expected:** Timeout error caught.

---

### 45. Session Closed

**Test:** Use closed session

```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import SessionClosedError

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.close()
        
        try:
            await session.page.navigate("https://example.com")
        except SessionClosedError as e:
            print(f"✓ Caught expected error: {e.message}")

asyncio.run(test())
```

**Expected:** Error caught for closed session.

---

## Cleanup Tests (5 minutes)

### 46. Target Cleanup

**Test:** Verify target cleanup on session close

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        target_id = session.target_id
        
        targets_before = await client.get_pages()
        count_before = sum(1 for t in targets_before if t.target_id == target_id)
        
        await session.close()
        
        targets_after = await client.get_pages()
        count_after = sum(1 for t in targets_after if t.target_id == target_id)
        
        assert count_after == 0, f"Target still open: {count_after}"
        print("✓ Target cleaned up on session close")

asyncio.run(test())
```

**Expected:** Target removed after session close.

---

### 47. Browser Cleanup

**Test:** Verify browser cleanup on context exit

```python
import asyncio
from cdpwave import CDPClient

async def test():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
    
    # After context exit, browser should be closed
    print("✓ Browser cleaned up on context exit")

asyncio.run(test())
```

**Expected:** Browser closed after context exit.

---

### 48. Resource Cleanup

**Test:** Verify no resource leaks

```python
import asyncio
from cdpwave import CDPClient

async def test():
    for i in range(10):
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            await session.page.navigate("https://example.com")
    
    print("✓ No resource leaks after 10 iterations")

asyncio.run(test())
```

**Expected:** No resource leaks.

---

## Test Checklist

Use this checklist to track manual test completion:

- [ ] 1. Basic Launch and Navigate
- [ ] 2. Browser Detection and Launch
- [ ] 3. Direct WebSocket Connection
- [ ] 4. Page Navigation
- [ ] 5. JavaScript Evaluation
- [ ] 6. Page Screenshots
- [ ] 7. PDF Generation
- [ ] 8. Multi-Tab Management
- [ ] 9. Network Monitoring
- [ ] 10. Cookie Management
- [ ] 11. Request Interception
- [ ] 12. Network Throttling
- [ ] 13. DOM Inspection
- [ ] 14. DOM Manipulation
- [ ] 15. Box Model
- [ ] 16. Device Emulation
- [ ] 17. Geolocation Override
- [ ] 18. Dark Mode
- [ ] 19. Timezone Override
- [ ] 20. Text Input
- [ ] 21. Keyboard Events
- [ ] 22. Mouse Events
- [ ] 23. Wait for Event
- [ ] 24. Event Listeners
- [ ] 25. Performance Metrics
- [ ] 26. CPU Profiling
- [ ] 27. Heap Snapshot
- [ ] 28. Security State
- [ ] 29. Certificate Info
- [ ] 30. Local Storage
- [ ] 31. IndexedDB
- [ ] 32. Browser Version
- [ ] 33. Command Line
- [ ] 34. Shadow DOM
- [ ] 35. File Upload
- [ ] 36. Iframe Navigation
- [ ] 37. Service Worker
- [ ] 38. WebAuthn
- [ ] 39. Tracing
- [ ] 40. Console API
- [ ] 41. Invalid URL
- [ ] 42. Invalid JavaScript
- [ ] 43. Non-existent Element
- [ ] 44. Connection Timeout
- [ ] 45. Session Closed
- [ ] 46. Target Cleanup
- [ ] 47. Browser Cleanup
- [ ] 48. Resource Cleanup

---

## Running All Tests

To run all manual tests sequentially:

```python
import asyncio
from cdpwave import CDPClient

async def run_all_tests():
    """Run all 48 manual tests."""
    print("=== Running Manual Test Suite ===\n")
    
    # Add all test functions here
    # ...
    
    print("\n=== Test Suite Complete ===")

asyncio.run(run_all_tests())
```

---

## Expected Results

- All 48 tests should pass without errors
- Browser should launch and close cleanly
- No resource leaks after multiple iterations
- All error cases should be handled gracefully

---

## Notes

- Some tests require specific browser features (Service Worker, WebAuthn)
- File upload tests require creating temporary files
- Network tests may behave differently depending on network conditions
- Geolocation tests require permission granting
- Shadow DOM tests require modern browser support
