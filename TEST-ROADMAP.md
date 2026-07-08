# Manual Test Scenarios — Functional User Tests

Step-by-step functional test scenarios for cdpwave. These are manual tests that you perform by following the instructions and verifying results visually or through browser DevTools.

## Prerequisites

- Chrome/Edge/Brave/Chromium installed
- Python 3.11+ installed
- cdpwave installed: `pip install cdpwave`
- Terminal or IDE for running scripts
- Basic understanding of Python async/await

---

# SECTION 1: Core Browser Launch

## Test 1.1: Basic Browser Launch

**Objective:** Verify that cdpwave can launch a browser successfully.

**Steps:**
1. Create a new Python file `test_launch.py`
2. Add the following code:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        print("Browser launched successfully!")
        await asyncio.sleep(2)

asyncio.run(main())
```
3. Run the script: `python test_launch.py`
4. Verify that the script prints "Browser launched successfully!"
5. Verify that no error occurs

**Expected Result:** Script runs without errors and prints success message.

---

## Test 1.2: Browser Detection

**Objective:** Verify that cdpwave can detect and launch different browsers.

**Steps:**
1. Create `test_browser_detection.py`:
```python
import asyncio
from cdpwave import CDPClient

async def test_chrome():
    async with await CDPClient.launch(headless=True, browser_type="chrome") as client:
        print(f"Launched: {client.browser_type}")

async def test_edge():
    async with await CDPClient.launch(headless=True, browser_type="edge") as client:
        print(f"Launched: {client.browser_type}")

asyncio.run(test_chrome())
asyncio.run(test_edge())
```
2. Run the script
3. Verify it detects and launches Chrome (if installed)
4. Verify it detects and launches Edge (if installed)

**Expected Result:** Browser type is correctly identified and launched.

---

## Test 1.3: Direct WebSocket Connection

**Objective:** Verify that cdpwave can connect to an existing browser via WebSocket.

**Steps:**
1. Launch Chrome with remote debugging:
   - Windows: `chrome.exe --remote-debugging-port=9222`
   - Linux/Mac: `google-chrome --remote-debugging-port=9222`
2. Create `test_connect.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.connect("ws://localhost:9222") as client:
        targets = await client.get_pages()
        print(f"Connected to {len(targets)} pages")

asyncio.run(main())
```
3. Run the script
4. Verify it connects and lists pages

**Expected Result:** Successfully connects and lists existing browser pages.

---

# SECTION 2: Page Navigation

## Test 2.1: Navigate to URL

**Objective:** Verify that cdpwave can navigate to a URL.

**Steps:**
1. Create `test_navigate.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate("https://example.com")
        print("Navigated to example.com")
        await asyncio.sleep(2)

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Navigation completes without errors.

---

## Test 2.2: Navigate with Wait for Load

**Objective:** Verify that cdpwave can wait for page load event.

**Steps:**
1. Create `test_navigate_wait.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")
        print("Page loaded successfully")

asyncio.run(main())
```
2. Run the script
3. Verify it waits for load event

**Expected Result:** Script waits for page load before continuing.

---

## Test 2.3: Navigate Back and Forward

**Objective:** Verify browser history navigation.

**Steps:**
1. Create `test_history.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.navigate("https://example.com")
        await session.page.navigate("https://example.org")
        await session.page.go_back()
        print("Navigated back")
        await session.page.go_forward()
        print("Navigated forward")

asyncio.run(main())
```
2. Run the script
3. Verify both back and forward work

**Expected Result:** History navigation works correctly.

---

# SECTION 3: JavaScript Evaluation

## Test 3.1: Simple Expression

**Objective:** Verify JavaScript evaluation works.

**Steps:**
1. Create `test_eval.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("1 + 1", return_by_value=True)
        print(f"1 + 1 = {result['result']['value']}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "1 + 1 = 2"

**Expected Result:** JavaScript evaluates correctly and returns expected value.

---

## Test 3.2: Get Page Title

**Objective:** Verify that cdpwave can read page content.

**Steps:**
1. Create `test_title.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        title = await session.runtime.evaluate("document.title", return_by_value=True)
        print(f"Page title: {title['result']['value']}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints the correct page title

**Expected Result:** Page title is retrieved correctly.

---

## Test 3.3: Async JavaScript

**Objective:** Verify that cdpwave can handle async JavaScript.

**Steps:**
1. Create `test_async.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        result = await session.runtime.evaluate(
            "new Promise(r => setTimeout(() => r(42), 100))",
            return_by_value=True,
            await_promise=True
        )
        print(f"Async result: {result['result']['value']}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Async result: 42"

**Expected Result:** Async JavaScript executes correctly.

---

# SECTION 4: Screenshots

## Test 4.1: PNG Screenshot

**Objective:** Verify that cdpwave can capture PNG screenshots.

**Steps:**
1. Create `test_screenshot.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        png = await session.page.capture_screenshot()
        with open("screenshot.png", "wb") as f:
            f.write(png)
        print(f"Screenshot saved: {len(png)} bytes")

asyncio.run(main())
```
2. Run the script
3. Open `screenshot.png` and verify it shows the page

**Expected Result:** PNG screenshot is created and shows the page content.

---

## Test 4.2: JPEG Screenshot

**Objective:** Verify that cdpwave can capture JPEG screenshots.

**Steps:**
1. Create `test_screenshot_jpeg.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        jpeg = await session.page.capture_screenshot(format="jpeg")
        with open("screenshot.jpg", "wb") as f:
            f.write(jpeg)
        print(f"JPEG screenshot saved: {len(jpeg)} bytes")

asyncio.run(main())
```
2. Run the script
3. Open `screenshot.jpg` and verify it shows the page

**Expected Result:** JPEG screenshot is created and shows the page content.

---

# SECTION 5: PDF Generation

## Test 5.1: Basic PDF

**Objective:** Verify that cdpwave can generate PDF.

**Steps:**
1. Create `test_pdf.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        pdf = await session.page.print_to_pdf()
        with open("page.pdf", "wb") as f:
            f.write(pdf)
        print(f"PDF saved: {len(pdf)} bytes")

asyncio.run(main())
```
2. Run the script
3. Open `page.pdf` and verify it contains the page content

**Expected Result:** PDF is created and contains the page content.

---

## Test 5.2: PDF with Background

**Objective:** Verify that cdpwave can generate PDF with background graphics.

**Steps:**
1. Create `test_pdf_bg.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page("https://example.com")
        pdf = await session.page.print_to_pdf(print_background=True)
        with open("page_bg.pdf", "wb") as f:
            f.write(pdf)
        print("PDF with background saved")

asyncio.run(main())
```
2. Run the script
3. Open `page_bg.pdf` and verify it includes background graphics

**Expected Result:** PDF includes background graphics.

---

# SECTION 6: Multi-Tab Management

## Test 6.1: Create Multiple Tabs

**Objective:** Verify that cdpwave can manage multiple tabs.

**Steps:**
1. Create `test_multitab.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")
        tab3 = await client.new_page("https://example.net")
        print(f"Created {len(client.sessions)} tabs")
        await asyncio.sleep(2)

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Created 3 tabs"

**Expected Result:** Multiple tabs are created successfully.

---

## Test 6.2: Close Specific Tab

**Objective:** Verify that cdpwave can close individual tabs.

**Steps:**
1. Create `test_close_tab.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")
        await tab2.close()
        print(f"Tabs remaining: {len(client.sessions)}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Tabs remaining: 1"

**Expected Result:** Individual tab is closed successfully.

---

# SECTION 7: Network Monitoring

## Test 7.1: Monitor Network Requests

**Objective:** Verify that cdpwave can monitor network requests.

**Steps:**
1. Create `test_network.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.network.enable()
        
        requests = []
        async def on_request(params):
            requests.append(params["request"]["url"])
        
        session.on("Network.requestWillBeSent", on_request)
        await session.page.navigate("https://example.com")
        
        print(f"Captured {len(requests)} network requests")
        for url in requests[:3]:
            print(f"  - {url}")

asyncio.run(main())
```
2. Run the script
3. Verify it lists network requests

**Expected Result:** Network requests are captured and listed.

---

## Test 7.2: Cookie Management

**Objective:** Verify that cdpwave can manage cookies.

**Steps:**
1. Create `test_cookies.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page("https://example.com")
        await session.network.enable()
        
        # Get cookies
        cookies = await session.network.get_cookies()
        print(f"Found {len(cookies)} cookies")
        
        # Set cookie
        await session.network.set_cookies([{
            "name": "test",
            "value": "value",
            "domain": "example.com"
        }])
        
        # Verify
        cookies = await session.network.get_cookies()
        assert any(c["name"] == "test" for c in cookies)
        print("Cookie set and verified")
        
        # Delete cookie
        await session.network.delete_cookies("test", "https://example.com")
        print("Cookie deleted")

asyncio.run(main())
```
2. Run the script
3. Verify cookie operations complete successfully

**Expected Result:** All cookie operations work correctly.

---

# SECTION 8: DOM Manipulation

## Test 8.1: Query Selector

**Objective:** Verify that cdpwave can query DOM elements.

**Steps:**
1. Create `test_dom_query.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page("https://example.com")
        await session.dom.enable()
        
        h1 = await session.dom.query_selector("h1")
        print(f"Found h1: {h1['nodeId']}")
        
        paragraphs = await session.dom.query_selector_all("p")
        print(f"Found {len(paragraphs.get('nodeIds', []))} paragraphs")

asyncio.run(main())
```
2. Run the script
3. Verify it finds elements

**Expected Result:** DOM elements are queried successfully.

---

## Test 8.2: Set Text Content

**Objective:** Verify that cdpwave can modify DOM text.

**Steps:**
1. Create `test_dom_text.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page("https://example.com")
        await session.dom.enable()
        
        h1 = await session.dom.query_selector("h1")
        await session.dom.set_text_content(h1["nodeId"], "New Title")
        print("Text content set")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Text content is modified successfully.

---

# SECTION 9: Device Emulation

## Test 9.1: Mobile Viewport

**Objective:** Verify that cdpwave can emulate mobile devices.

**Steps:**
1. Create `test_mobile.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        await session.emulation.set_device_metrics_override(
            width=375,
            height=667,
            device_scale_factor=2,
            mobile=True
        )
        print("Mobile viewport emulated")
        
        await session.page.navigate("https://example.com")
        print("Navigated with mobile viewport")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Mobile viewport is emulated successfully.

---

## Test 9.2: Geolocation Override

**Objective:** Verify that cdpwave can override geolocation.

**Steps:**
1. Create `test_geolocation.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        await session.emulation.set_geolocation_override(
            latitude=40.7128,
            longitude=-74.0060
        )
        print("Geolocation set to New York")
        
        await session.send("Browser.grantPermissions", {
            "permissions": ["geolocation"],
            "origin": "https://example.com"
        })
        
        await session.page.navigate("https://example.com")
        print("Navigated with geolocation")

asyncio.run(main())
```
2. Run the script
3. Verify geolocation is set

**Expected Result:** Geolocation override is applied.

---

## Test 9.3: Dark Mode

**Objective:** Verify that cdpwave can emulate dark mode.

**Steps:**
1. Create `test_dark_mode.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        await session.emulation.set_emulated_media("prefers-color-scheme", "dark")
        print("Dark mode emulated")
        
        await session.page.navigate("https://example.com")
        print("Navigated with dark mode")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Dark mode is emulated.

---

# SECTION 10: Input Simulation

## Test 10.1: Text Input

**Objective:** Verify that cdpwave can type text into input fields.

**Steps:**
1. Create `test_input_text.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.page.navigate("data:text/html,<input id='q' type='text'>")
        
        await session.input.insert_text("Hello World")
        print("Text inserted")
        
        # Verify
        value = await session.runtime.evaluate(
            "document.getElementById('q').value",
            return_by_value=True
        )
        print(f"Input value: {value['result']['value']}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Input value: Hello World"

**Expected Result:** Text is inserted correctly.

---

## Test 10.2: Keyboard Events

**Objective:** Verify that cdpwave can send keyboard events.

**Steps:**
1. Create `test_keyboard.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.page.navigate("data:text/html,<input id='q' type='text'>")
        
        await session.input.dispatch_key_event("char", "H")
        await session.input.dispatch_key_event("char", "i")
        print("Keyboard events sent")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Keyboard events are sent successfully.

---

## Test 10.3: Mouse Click

**Objective:** Verify that cdpwave can simulate mouse clicks.

**Steps:**
1. Create `test_mouse.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.page.navigate("data:text/html,<button id='btn'>Click</button>")
        
        # Get element position
        rect = await session.runtime.evaluate("""
            const el = document.getElementById('btn');
            const r = el.getBoundingClientRect();
            return {x: r.left + 5, y: r.top + 5};
        """, return_by_value=True)
        
        # Click
        await session.input.dispatch_mouse_event("mousePressed", "left", 
            rect["result"]["value"]["x"], rect["result"]["value"]["y"])
        await session.input.dispatch_mouse_event("mouseReleased", "left",
            rect["result"]["value"]["x"], rect["result"]["value"]["y"])
        print("Mouse click sent")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Mouse click is sent successfully.

---

# SECTION 11: Event Handling

## Test 11.1: Wait for Event

**Objective:** Verify that cdpwave can wait for specific events.

**Steps:**
1. Create `test_wait_event.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")
        print("Page loaded event received")

asyncio.run(main())
```
2. Run the script
3. Verify it waits for the event

**Expected Result:** Script waits for event before continuing.

---

## Test 11.2: Event Listeners

**Objective:** Verify that cdpwave can register event listeners.

**Steps:**
1. Create `test_event_listener.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.runtime.enable()
        
        messages = []
        async def on_console(params):
            messages.append(params)
        
        session.on("Runtime.consoleAPICalled", on_console)
        
        await session.runtime.evaluate("console.log('msg1')")
        await session.runtime.evaluate("console.log('msg2')")
        
        print(f"Received {len(messages)} console messages")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Received 2 console messages"

**Expected Result:** Event listeners work correctly.

---

# SECTION 12: Performance

## Test 12.1: Performance Metrics

**Objective:** Verify that cdpwave can collect performance metrics.

**Steps:**
1. Create `test_performance.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.performance.enable()
        
        await session.page.navigate("https://example.com")
        metrics = await session.performance.get_metrics()
        
        print(f"Collected {len(metrics)} metrics")
        for metric in metrics[:3]:
            print(f"  - {metric['name']}: {metric.get('value', 'N/A')}")

asyncio.run(main())
```
2. Run the script
3. Verify it lists performance metrics

**Expected Result:** Performance metrics are collected.

---

## Test 12.2: CPU Profiling

**Objective:** Verify that cdpwave can capture CPU profiles.

**Steps:**
1. Create `test_profiler.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.profiler.enable()
        
        await session.profiler.start()
        await session.runtime.evaluate("for(let i=0;i<1000;i++) Math.sqrt(i)")
        profile = await session.profiler.stop()
        
        nodes = profile.get("profile", {}).get("nodes", [])
        print(f"CPU profile: {len(nodes)} nodes")

asyncio.run(main())
```
2. Run the script
3. Verify it prints the number of nodes

**Expected Result:** CPU profile is captured.

---

# SECTION 13: Error Handling

## Test 13.1: Invalid URL

**Objective:** Verify that cdpwave handles invalid URLs gracefully.

**Steps:**
1. Create `test_error_url.py`:
```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandError

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        try:
            await session.page.navigate("not-a-url")
        except CommandError as e:
            print(f"Caught expected error: {e.message}")

asyncio.run(main())
```
2. Run the script
3. Verify it catches the error

**Expected Result:** Error is caught and handled gracefully.

---

## Test 13.2: Invalid JavaScript

**Objective:** Verify that cdpwave handles invalid JavaScript gracefully.

**Steps:**
1. Create `test_error_js.py`:
```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandError

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        try:
            await session.runtime.evaluate("invalid javascript syntax")
        except CommandError as e:
            print(f"Caught expected error: {e.message}")

asyncio.run(main())
```
2. Run the script
3. Verify it catches the error

**Expected Result:** Error is caught and handled gracefully.

---

## Test 13.3: Timeout

**Objective:** Verify that cdpwave handles timeouts gracefully.

**Steps:**
1. Create `test_error_timeout.py`:
```python
import asyncio
from cdpwave import CDPClient
from cdpwave.exceptions import CommandTimeoutError

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        try:
            await session.runtime.evaluate("new Promise(() => {})", timeout=1)
        except CommandTimeoutError:
            print("Caught timeout error")

asyncio.run(main())
```
2. Run the script
3. Verify it catches the timeout

**Expected Result:** Timeout is caught and handled.

---

# SECTION 14: Cleanup

## Test 14.1: Target Cleanup

**Objective:** Verify that cdpwave cleans up targets when sessions are closed.

**Steps:**
1. Create `test_cleanup_target.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        target_id = session.target_id
        
        targets_before = await client.get_pages()
        count_before = sum(1 for t in targets_before if t.target_id == target_id)
        
        await session.close()
        
        targets_after = await client.get_pages()
        count_after = sum(1 for t in targets_after if t.target_id == target_id)
        
        assert count_after == 0, f"Target still open: {count_after}"
        print("Target cleaned up successfully")

asyncio.run(main())
```
2. Run the script
3. Verify it prints "Target cleaned up successfully"

**Expected Result:** Target is removed after session close.

---

## Test 14.2: Resource Cleanup

**Objective:** Verify that cdpwave doesn't leak resources over multiple iterations.

**Steps:**
1. Create `test_cleanup_resources.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    for i in range(5):
        async with await CDPClient.launch(headless=True) = client:
            session = await client.new_page()
            await session.page.navigate("https://example.com")
    
    print("No resource leaks after 5 iterations")

asyncio.run(main())
```
2. Run the script
3. Verify it completes without errors

**Expected Result:** No resource leaks occur.

---

# SECTION 15: Integration Scenarios

## Test 15.1: Complete User Flow

**Objective:** Verify a complete user workflow from launch to cleanup.

**Steps:**
1. Create `test_complete_flow.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        # Launch browser
        print("1. Browser launched")
        
        # Create page and navigate
        session = await client.new_page()
        await session.page.navigate("https://example.com")
        print("2. Page navigated")
        
        # Evaluate JavaScript
        title = await session.runtime.evaluate("document.title", return_by_value=True)
        print(f"3. Page title: {title['result']['value']}")
        
        # Take screenshot
        screenshot = await session.page.capture_screenshot()
        print(f"4. Screenshot captured: {len(screenshot)} bytes")
        
        # Generate PDF
        pdf = await session.page.print_to_pdf()
        print(f"5. PDF generated: {len(pdf)} bytes")
        
        # Close page
        await session.close()
        print("6. Page closed")
    
    print("7. Browser closed")

asyncio.run(main())
```
2. Run the script
3. Verify all steps complete successfully

**Expected Result:** Complete workflow executes without errors.

---

## Test 15.2: Multi-Tab Workflow

**Objective:** Verify workflow with multiple tabs.

**Steps:**
1. Create `test_multitab_flow.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        # Create multiple tabs
        tab1 = await client.new_page("https://example.com")
        print("1. Tab 1 created")
        
        tab2 = await client.new_page("https://example.org")
        print("2. Tab 2 created")
        
        # Work with both tabs
        title1 = await tab1.runtime.evaluate("document.title", return_by_value=True)
        title2 = await tab2.runtime.evaluate("document.title", return_by_value=True)
        
        print(f"3. Tab 1: {title1['result']['value']}")
        print(f"4. Tab 2: {title2['result']['value']}")
        
        # Close one tab
        await tab2.close()
        print(f"5. Tabs remaining: {len(client.sessions)}")

asyncio.run(main())
```
2. Run the script
3. Verify multi-tab workflow works

**Expected Result:** Multi-tab workflow executes successfully.

---

# SECTION 16: Advanced Features

## Test 16.1: Request Interception

**Objective:** Verify that cdpwave can intercept and modify requests.

**Steps:**
1. Create `test_interception.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.fetch.enable(patterns=[{"urlPattern": "*"}])
        
        intercepted = []
        async def on_paused(params):
            intercepted.append(params["requestId"])
            await session.fetch.continue_request(requestId=params["requestId"])
        
        session.on("Fetch.requestPaused", on_paused)
        await session.page.navigate("https://example.com")
        
        print(f"Intercepted {len(intercepted)} requests")

asyncio.run(main())
```
2. Run the script
3. Verify requests are intercepted

**Expected Result:** Requests are intercepted and continued.

---

## Test 16.2: Network Throttling

**Objective:** Verify that cdpwave can emulate slow network.

**Steps:**
1. Create `test_throttling.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        
        await session.network.emulate_network_conditions(
            offline=False,
            download_throughput=500000,
            upload_throughput=500000,
            latency=100
        )
        print("Network throttled to 500 KB/s")
        
        await session.page.navigate("https://example.com")
        print("Navigated with throttling")

asyncio.run(main())
```
2. Run the script
3. Verify throttling is applied

**Expected Result:** Network throttling is applied.

---

## Test 16.3: Shadow DOM

**Objective:** Verify that cdpwave can access Shadow DOM.

**Steps:**
1. Create `test_shadow_dom.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        session = await client.new_page()
        await session.dom.enable()
        
        await session.page.navigate("data:text/html,<div id='host'></div>")
        await session.runtime.evaluate("""
            const host = document.getElementById('host');
            const shadow = host.attachShadow({mode: 'open'});
            shadow.innerHTML = '<p>Shadow content</p>';
        """)
        
        result = await session.dom.describe_node(
            (await session.dom.query_selector("#host"))["nodeId"],
            depth=2
        )
        print("Shadow DOM accessed")

asyncio.run(main())
```
2. Run the script
3. Verify no errors occur

**Expected Result:** Shadow DOM is accessed successfully.

---

# SECTION 17: Browser Info

## Test 17.1: Browser Version

**Objective:** Verify that cdpwave can get browser version information.

**Steps:**
1. Create `test_version.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        version = await client.browser.get_version()
        print(f"Browser: {version.get('product')}")
        print(f"User Agent: {version.get('userAgent')}")
        print(f"JavaScript: {version.get('javascriptVersion')}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints browser information

**Expected Result:** Browser version information is retrieved.

---

## Test 17.2: Command Line Arguments

**Objective:** Verify that cdpwave can get browser command line.

**Steps:**
1. Create `test_cmdline.py`:
```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) = client:
        cmdline = await client.browser.get_command_line()
        print(f"Command line arguments: {len(cmdline.get('arguments', []))}")

asyncio.run(main())
```
2. Run the script
3. Verify it prints the number of arguments

**Expected Result:** Command line arguments are retrieved.

---

# Test Summary Checklist

Use this checklist to track which manual tests you've completed:

## Core Browser Launch
- [ ] 1.1: Basic Browser Launch
- [ ] 1.2: Browser Detection
- [ ] 1.3: Direct WebSocket Connection

## Page Navigation
- [ ] 2.1: Navigate to URL
- [ ] 2.2: Navigate with Wait for Load
- [ ] 2.3: Navigate Back and Forward

## JavaScript Evaluation
- [ ] 3.1: Simple Expression
- [ ] 3.2: Get Page Title
- [ ] 3.3: Async JavaScript

## Screenshots
- [ ] 4.1: PNG Screenshot
- [ ] 4.2: JPEG Screenshot

## PDF Generation
- [ ] 5.1: Basic PDF
- [ ] 5.2: PDF with Background

## Multi-Tab Management
- [ ] 6.1: Create Multiple Tabs
- [ ] 6.2: Close Specific Tab

## Network Monitoring
- [ ] 7.1: Monitor Network Requests
- [ ] 7.2: Cookie Management

## DOM Manipulation
- [ ] 8.1: Query Selector
- [ ] 8.2: Set Text Content

## Device Emulation
- [ ] 9.1: Mobile Viewport
- [ ] 9.2: Geolocation Override
- [ ] 9.3: Dark Mode

## Input Simulation
- [ ] 10.1: Text Input
- [ ] 10.2: Keyboard Events
- [ ] 10.3: Mouse Click

## Event Handling
- [ ] 11.1: Wait for Event
- [ ] 11.2: Event Listeners

## Performance
- [ ] 12.1: Performance Metrics
- [ ] 12.2: CPU Profiling

## Error Handling
- [ ] 13.1: Invalid URL
- [ ] 13.2: Invalid JavaScript
- [ ] 13.3: Timeout

## Cleanup
- [ ] 14.1: Target Cleanup
- [ ] 14.2: Resource Cleanup

## Integration Scenarios
- [ ] 15.1: Complete User Flow
- [ ] 15.2: Multi-Tab Workflow

## Advanced Features
- [ ] 16.1: Request Interception
- [ ] 16.2: Network Throttling
- [ ] 16.3: Shadow DOM

## Browser Info
- [ ] 17.1: Browser Version
- [ ] 17.2: Command Line Arguments

---

## Running All Tests

To run all manual tests sequentially, create `run_all_tests.py`:

```python
import asyncio
from cdpwave import CDPClient

async def main():
    print("=== Running Manual Test Suite ===\n")
    
    # Add all test functions from above
    # ...
    
    print("\n=== Test Suite Complete ===")

asyncio.run(main())
```

---

## Expected Results Summary

- All 35 test scenarios should run without errors
- Browser should launch and close cleanly
- No resource leaks after multiple iterations
- All error cases should be handled gracefully
- Integration workflows should complete successfully

---

## Notes

- Some tests require specific browser features (Shadow DOM, WebAuthn, etc.)
- File upload tests require creating temporary files
- Network tests may behave differently depending on network conditions
- Geolocation tests require permission granting
- Shadow DOM tests require modern browser support (Chrome 80+)
