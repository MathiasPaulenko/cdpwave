# Test Roadmap

Comprehensive test plan for 100% coverage of cdpwave functionality.

## Overview

cdpwave implements **48 CDP domains** with **~386 typed methods**. This roadmap outlines a complete testing strategy to ensure all functionality is thoroughly tested.

### Current Test Status

| Category | Tests | Coverage | Status |
|----------|-------|----------|--------|
| Unit tests | 537 | 89% | ✅ |
| Manual smoke test | 34 | Core features | ✅ |
| Integration tests | 0 | 0% | ❌ |
| Edge case tests | Partial | ~40% | ⚠️ |
| Error handling tests | Partial | ~50% | ⚠️ |

---

## Domain Testing Matrix

### Tier 1: Core Domains (Critical Path)

These domains are used in every workflow and require comprehensive testing.

| Domain | Methods | Unit Tests | Integration Tests | Edge Cases | Status |
|--------|---------|------------|-------------------|------------|--------|
| **Page** | 27 | ✅ | ⚠️ | ⚠️ | 80% |
| **Runtime** | 20 | ✅ | ⚠️ | ⚠️ | 75% |
| **Target** | 12 | ✅ | ⚠️ | ⚠️ | 70% |
| **Network** | 17 | ✅ | ⚠️ | ❌ | 60% |
| **DOM** | 26 | ✅ | ❌ | ❌ | 50% |
| **Browser** | 9 | ✅ | ⚠️ | ⚠️ | 70% |

#### Page Domain Tests (27 methods)

**Existing unit tests:** ✅
- enable/disable
- navigate (with referrer, transition_type)
- reload
- goBack/goForward
- captureScreenshot (with clip, format)
- printToPDF
- getLayoutMetrics
- getNavigationHistory
- setDocumentContent
- getFrameTree
- setBypassCSP
- crash
- close
- bringToFront
- handleJavaScriptDialog
- createIsolatedWorld
- captureSnapshot
- getResourceTree
- getResourceContent
- resetNavigationHistory
- navigateToHistoryEntry
- setWebLifecycleState
- setInterceptFileChooserDialog
- getAppManifest
- addScriptToEvaluateOnNewDocument
- removeScriptToEvaluateOnNewDocument

**Missing integration tests:**
- [ ] Screenshot with viewport clip (real browser)
- [ ] PDF with printBackground, margins, pageRanges
- [ ] Lifecycle state transitions (active, hidden, frozen)
- [ ] File chooser dialog interception
- [ ] JavaScript dialog (alert, confirm, prompt) handling
- [ ] App manifest parsing
- [ ] Script injection timing (before load vs after)
- [ ] Resource content encoding (base64, text)
- [ ] Frame tree with nested iframes
- [ ] Navigation history with multiple entries

**Missing edge cases:**
- [ ] Navigate to invalid URL
- [ ] Screenshot when page is not loaded
- [ ] PDF generation with non-HTML content
- [ ] Lifecycle state during navigation
- [ ] Dialog when no dialog is present
- [ ] Isolated world with same name
- [ ] Resource content for non-existent resources
- [ ] Navigation history with circular references

**Missing error handling:**
- [ ] CDP error on navigate (target crashed)
- [ ] Timeout on long PDF generation
- [ ] Permission denied for file chooser
- [ ] Invalid lifecycle state
- [ ] Target closed during screenshot

---

#### Runtime Domain Tests (20 methods)

**Existing unit tests:** ✅
- enable/disable
- evaluate (with context, returnByValue, awaitPromise)
- callFunctionOn
- releaseObject/releaseObjectGroup
- getProperties
- compileScript
- runScript
- queryObjects
- globalLexicalScopeNames
- getExceptionDetails
- addBinding/removeBinding
- getHeapUsage
- getIsolateId
- collectGarbage
- terminateExecution
- setCustomObjectFormatterEnabled

**Missing integration tests:**
- [ ] Evaluate with complex objects (Date, RegExp, Map)
- [ ] CallFunctionOn with thisArg
- [ ] Remote object properties (accessors, symbols)
- [ ] Object groups and release timing
- [ ] CompileScript and runScript with source maps
- [ ] QueryObjects for custom classes
- [ ] Lexical scope with nested functions
- [ ] Exception details stack traces
- [ ] Binding called from multiple contexts
- [ ] Custom object formatter
- [ ] Heap usage during heavy operations
- [ ] Garbage collection timing

**Missing edge cases:**
- [ ] Evaluate with syntax errors
- [ ] CallFunctionOn on non-existent object
- [ ] Release object that doesn't exist
- [ ] GetProperties on non-object
- [ ] CompileScript with invalid syntax
- [ ] QueryObjects for built-in types
- [ ] Binding with same name twice
- [ ] Terminate execution during long-running script

**Missing error handling:**
- [ ] CDP error on evaluate (execution context destroyed)
- [ ] Timeout on long-running script
- [ ] Invalid object ID
- [ ] Invalid execution context ID
- [ ] Script execution limit exceeded

---

#### Target Domain Tests (12 methods)

**Existing unit tests:** ✅
- createTarget
- attachToTarget (flatten=True/False)
- detachFromTarget
- closeTarget
- getTargets
- activateTarget
- setAutoAttach
- sendMessageToTarget
- setDiscoverTargets

**Missing integration tests:**
- [ ] Create target with specific URL
- [ ] Attach to target with sessionId
- [ ] Multi-tab session management
- [ ] Target discovery filtering
- [ ] Auto-attach to new targets
- [ ] Cross-target message passing
- [ ] Target lifecycle events (created, destroyed, attached, detached)

**Missing edge cases:**
- [ ] Attach to non-existent target
- [ ] Close target that doesn't exist
- [ ] Activate already active target
- [ ] Send message to detached target
- [ ] Auto-attach with invalid filter

**Missing error handling:**
- [ ] Target crashed during attach
- [ ] Target closed during operation
- [ ] Invalid target ID format
- [ ] Permission denied for target access

---

#### Network Domain Tests (17 methods)

**Existing unit tests:** ✅
- enable/disable
- setCacheDisabled
- setUserAgentOverride
- clearBrowserCookies/clearBrowserCache
- getAllCookies
- setCookies
- getCookies
- deleteCookies
- setExtraHTTPHeaders
- canEmulateNetworkConditions
- setCacheDisabled
- getResponseBody
- getResponseBodyForInterception
- takeResponseBodyForInterceptionAsStream
- continueInterceptedRequest
- getPostData
- replayXHR

**Missing integration tests:**
- [ ] Request/response headers inspection
- [ ] Cookie management (SameSite, HttpOnly, Secure)
- [ ] Cache behavior with different modes
- [ ] Network throttling (offline, slow 3G)
- [ ] Request interception and modification
- [ ] Response body streaming
- [ ] XHR replay with modified body
- [ ] Websocket connection monitoring
- [ ] Mixed content (HTTP/HTTPS)
- [ ] Cookie domain/path matching
- [ ] Extra headers with special characters

**Missing edge cases:**
- [ ] Invalid cookie format
- [ ] Request with no response
- [ ] Response body too large
- [ ] Interception without continue
- [ ] Replay already replayed XHR
- [ ] Headers with duplicate names
- [ ] Cookie with invalid domain

**Missing error handling:**
- [ ] Network error (DNS, connection refused)
- [ ] Timeout on response
- [ ] Invalid interception ID
- [ ] Permission denied for cookies
- [ ] Request cancelled

---

#### DOM Domain Tests (26 methods)

**Existing unit tests:** ✅
- enable/disable
- getDocument
- getFlattenedDocument
- collectClassNamesFromSubtree
- querySelector/querySelectorAll
- removeNode
- setAttributeValue
- setAttributesAsText
- removeAttribute
- setTextContent
- getBoxModel
- getContentQuads
- getHighlightObjectForTest
- describeNode
- focus
- scrollIntoViewIfNeeded
- setFileInputFiles
- performSearch
- getSearchResults
- discardSearchResults
- requestChildNodes
- requestNode
- setChildNodes
- getOuterHTML
- setOuterHTML

**Missing integration tests:**
- [ ] DOM mutation observation
- [ ] Shadow DOM traversal
- [ ] File input with multiple files
- [ ] Text content with special characters
- [ ] Box model with transforms
- [ ] Content quads for rotated elements
- [ ] Search across entire document
- [ ] Attribute mutation tracking
- [ ] Child nodes lazy loading
- [ ] Outer HTML with script tags
- [ ] Focus on hidden elements

**Missing edge cases:**
- [ ] Query selector with invalid syntax
- [ ] Remove non-existent node
- [ ] Set attribute on non-element
- [ ] Set file input on non-input
- [ ] Scroll element not in viewport
- [ ] Search with empty query
- [ ] Get node with invalid ID
- [ ] Set outer HTML that creates invalid DOM

**Missing error handling:**
- [ ] Node not found
- [ ] Node detached from document
- [ ] Invalid node ID
- [ ] Permission denied for file access
- [ ] DOM mutation blocked by CSP

---

#### Browser Domain Tests (9 methods)

**Existing unit tests:** ✅
- getVersion
- getCommandLine
- getHistogram
- getHistograms
- getCPUProfile
- getHeapProfile
- resetHistograms
- getBrowserCommandLine
- getBounds

**Missing integration tests:**
- [ ] Version info parsing
- [ ] Command line flags inspection
- [ ] Histogram metrics collection
- [ ] CPU profiling over time
- [ ] Heap snapshot analysis
- [ ] Browser bounds with multiple monitors

**Missing edge cases:**
- [ ] Get version during browser startup
- [ ] Histogram with empty name
- [ ] CPU profile with no samples
- [ ] Heap profile with no objects
- [ ] Bounds on headless browser

**Missing error handling:**
- [ ] Browser not responding
- [ ] Permission denied for metrics
- [ ] Histogram not found

---

### Tier 2: High-Value Domains

| Domain | Methods | Unit Tests | Integration Tests | Edge Cases | Status |
|--------|---------|------------|-------------------|------------|--------|
| **Emulation** | 26 | ✅ | ⚠️ | ⚠️ | 60% |
| **Input** | 11 | ✅ | ⚠️ | ❌ | 50% |
| **Fetch** | 10 | ✅ | ⚠️ | ❌ | 50% |
| **CSS** | 14 | ✅ | ❌ | ❌ | 40% |
| **Storage** | 13 | ✅ | ⚠️ | ❌ | 50% |
| **Overlay** | 15 | ✅ | ❌ | ❌ | 30% |
| **Debugger** | 22 | ✅ | ❌ | ❌ | 40% |

#### Emulation Domain Tests (26 methods)

**Existing unit tests:** ✅
- setDeviceMetricsOverride
- clearDeviceMetricsOverride
- setGeolocationOverride
- clearGeolocationOverride
- setCPUThrottlingRate
- setUserAgentOverride
- setTouchEmulationEnabled
- setEmulatedMedia
- clearEmulatedMedia
- setTimezoneOverride
- clearTimezoneOverride

**Missing integration tests:**
- [ ] Device metrics with viewport and scale
- [ ] Geolocation with high accuracy
- [ ] CPU throttling impact on performance
- [ ] User agent spoofing detection
- [ ] Touch emulation with gestures
- [ ] Dark mode media query
- [ ] Reduced motion media query
- [ ] Timezone with DST transitions
- [ ] Screen orientation
- [ ] Idle emulation
- [ ] Virtual sensors (accelerometer, gyroscope)
- [ ] Bluetooth emulation

**Missing edge cases:**
- [ ] Invalid device metrics (negative values)
- [ ] Geolocation outside valid ranges
- [ ] CPU throttling with zero rate
- [ ] User agent with invalid format
- [ ] Media feature not supported
- [ ] Timezone with invalid IANA name

**Missing error handling:**
- [ ] Permission denied for geolocation
- [ ] Device metrics not supported
- [ ] Virtual sensors not available

---

#### Input Domain Tests (11 methods)

**Existing unit tests:** ✅
- dispatchKeyEvent
- dispatchMouseEvent
- dispatchTouchEvent
- emulateTouchFromMouseEvent
- synthesizePinchGesture
- synthesizeScrollGesture
- synthesizeTapGesture
- insertText
- setIgnoreInputEvents
- dragIntercepted

**Missing integration tests:**
- [ ] Keyboard shortcuts (Ctrl+C, Ctrl+V)
- [ ] Mouse drag and drop
- [ ] Touch pinch zoom
- [ ] Touch scroll with momentum
- [ ] Text insertion with special characters
- [ ] Input event sequence (keydown, input, keyup)
- [ ] Drag over droppable elements
- [ ] Ignore input during dialogs

**Missing edge cases:**
- [ ] Dispatch event to detached element
- [ ] Invalid key code
- [ ] Touch with too many fingers
- [ ] Pinch with zero scale
- [ ] Scroll with zero delta
- [ ] Insert text into non-editable

**Missing error handling:**
- [ ] Element not found
- [ ] Permission denied for input
- [ ] Input blocked by focus

---

#### Fetch Domain Tests (10 methods)

**Existing unit tests:** ✅
- enable/disable
- failRequest
- fulfillRequest
- continueRequest
- continueWithAuth
- getResponseBody
- takeResponseBodyAsStream
- continueResponse
- pause/fail

**Missing integration tests:**
- [ ] Request modification (headers, body)
- [ ] Response mocking (status, headers, body)
- [ ] Authentication challenges
- [ ] Request/response streaming
- [ ] Request pausing and resuming
- [ ] Cross-origin requests
- [ ] WebSocket interception
- [ ] Service worker requests

**Missing edge cases:**
- [ ] Fulfill with invalid status code
- [ ] Continue with missing request ID
- [ ] Auth with invalid credentials
- [ ] Stream body too large
- [ ] Pause already paused request

**Missing error handling:**
- [ ] Request ID not found
- [ ] Response body not available
- [ ] Auth challenge failed
- [ ] Permission denied for interception

---

### Tier 3: Supporting Domains

These domains provide specialized functionality. Testing priority is lower but still important.

| Domain | Methods | Unit Tests | Status |
|--------|---------|------------|--------|
| **Accessibility** | 7 | ✅ | 40% |
| **Animation** | 9 | ✅ | 30% |
| **Audits** | 4 | ✅ | 20% |
| **BackgroundService** | 4 | ✅ | 20% |
| **CacheStorage** | 4 | ✅ | 30% |
| **Cast** | 5 | ✅ | 10% |
| **Console** | 3 | ✅ | 30% |
| **CSS** | 14 | ✅ | 40% |
| **Debugger** | 22 | ✅ | 40% |
| **DeviceAccess** | 4 | ✅ | 20% |
| **DeviceOrientation** | 2 | ✅ | 20% |
| **DOMDebugger** | 6 | ✅ | 30% |
| **DOMSnapshot** | - | ❌ | 0% |
| **DOMStorage** | - | ❌ | 0% |
| **EventBreakpoints** | 4 | ✅ | 20% |
| **Extensions** | 4 | ✅ | 20% |
| **Fetch** | 10 | ✅ | 50% |
| **HeadlessExperimental** | 3 | ✅ | 10% |
| **HeapProfiler** | 10 | ✅ | 30% |
| **IndexedDB** | 7 | ✅ | 20% |
| **Inspector** | 2 | ✅ | 20% |
| **IO** | 3 | ✅ | 10% |
| **LayerTree** | 7 | ✅ | 20% |
| **Log** | 5 | ✅ | 40% |
| **Media** | 4 | ✅ | 10% |
| **Memory** | 8 | ✅ | 30% |
| **Overlay** | 15 | ✅ | 30% |
| **Performance** | 4 | ✅ | 40% |
| **PerformanceTimeline** | 4 | ✅ | 20% |
| **Preload** | 4 | ✅ | 20% |
| **Profiler** | 9 | ✅ | 30% |
| **PWA** | 3 | ✅ | 10% |
| **Runtime** | 20 | ✅ | 75% |
| **Schema** | 1 | ✅ | 10% |
| **Security** | 4 | ✅ | 30% |
| **Sensor** | 4 | ✅ | 10% |
| **ServiceWorker** | 11 | ✅ | 20% |
| **Storage** | 13 | ✅ | 50% |
| **SystemInfo** | 4 | ✅ | 30% |
| **Target** | 12 | ✅ | 70% |
| **Tethering** | 2 | ✅ | 10% |
| **Tracing** | 5 | ✅ | 30% |
| **WebAuthn** | 4 | ✅ | 10% |
| **Worker** | 2 | ✅ | 10% |

---

## Integration Test Plan

### Phase 1: Core Workflows (Priority 1)

Tests that cover the most common user workflows.

```python
# tests/integration/test_core_workflows.py

class TestNavigationWorkflow:
    async def test_navigate_and_wait_for_load(self):
        """Navigate to URL and wait for load event."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page("https://example.com")
            await session.wait_for_event("Page.loadEventFired")
            assert session is not None

    async def test_navigate_back_and_forward(self):
        """Navigate through history."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page("https://example.com")
            await session.page.navigate("https://example.org")
            await session.page.navigate("https://example.net")
            await session.page.go_back()
            await session.page.go_forward()

    async def test_multi_tab_navigation(self):
        """Navigate multiple tabs concurrently."""
        async with await CDPClient.launch(headless=True) as client:
            tab1 = await client.new_page("https://example.com")
            tab2 = await client.new_page("https://example.org")
            await tab1.wait_for_event("Page.loadEventFired")
            await tab2.wait_for_event("Page.loadEventFired")
```

### Phase 2: Domain-Specific Workflows (Priority 2)

Tests for specific domain capabilities.

```python
# tests/integration/test_domain_workflows.py

class TestNetworkWorkflow:
    async def test_intercept_and_modify_request(self):
        """Intercept network request and modify headers."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            await session.fetch.enable()
            intercepted = []

            async def on_paused(params):
                intercepted.append(params["requestId"])
                await session.fetch.continue_request(
                    requestId=params["requestId"],
                    headers={"X-Custom": "value"}
                )

            session.on("Fetch.requestPaused", on_paused)
            await session.page.navigate("https://example.com")
            assert len(intercepted) > 0

class TestEmulationWorkflow:
    async def test_device_emulation(self):
        """Emulate mobile device."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            await session.emulation.set_device_metrics_override(
                width=375, height=667, deviceScaleFactor=2, mobile=True
            )
            await session.page.navigate("https://example.com")
            # Verify viewport is mobile size
```

### Phase 3: Edge Case Workflows (Priority 3)

Tests for error conditions and edge cases.

```python
# tests/integration/test_edge_cases.py

class TestErrorHandling:
    async def test_navigation_timeout(self):
        """Test timeout on slow navigation."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            with pytest.raises(CommandTimeoutError):
                await session.page.navigate("http://slow.example.com", timeout=1)

    async def test_invalid_javascript(self):
        """Test evaluation of invalid JavaScript."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            with pytest.raises(CommandError):
                await session.runtime.evaluate("invalid javascript syntax")

    async def test_target_crash(self):
        """Test behavior when target crashes."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            await session.page.crash()
            # Verify session is closed
```

---

## Performance Test Plan

### Metrics to Track

- **Connection time**: Time to establish WebSocket connection
- **Command latency**: Round-trip time for CDP commands
- **Event latency**: Time from event to handler invocation
- **Memory usage**: Memory consumption over time
- **CPU usage**: CPU consumption during heavy operations

### Test Scenarios

```python
# tests/performance/test_performance.py

class TestPerformance:
    async def test_command_latency(self):
        """Measure average command latency."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            latencies = []
            for _ in range(100):
                start = time.perf_counter()
                await session.runtime.evaluate("1+1")
                latencies.append(time.perf_counter() - start)
            avg_latency = sum(latencies) / len(latencies)
            assert avg_latency < 0.1  # 100ms threshold

    async def test_memory_leak(self):
        """Detect memory leaks over many operations."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            initial_heap = await session.performance.get_metrics()
            for _ in range(1000):
                await session.page.navigate("https://example.com")
            final_heap = await session.performance.get_metrics()
            # Memory should not grow significantly
```

---

## Security Test Plan

### Test Scenarios

- **Input validation**: Test with malformed CDP commands
- **Resource limits**: Test with large messages, many events
- **Permission checks**: Test domain permissions
- **Data exfiltration**: Ensure no data leaks
- **Injection attacks**: Test with malicious JavaScript

```python
# tests/security/test_security.py

class TestSecurity:
    async def test_command_injection(self):
        """Test that commands are properly escaped."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            # Attempt to inject CDP command
            with pytest.raises(CommandError):
                await session.send("Runtime.evaluate", {
                    "expression": "chrome.debugger.sendCommand('Target.closeTarget')"
                })

    async def test_large_message_handling(self):
        """Test handling of very large messages."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            large_string = "x" * 10_000_000  # 10MB
            await session.runtime.evaluate(f"'{large_string}'")

    async def test_event_flooding(self):
        """Test handling of event flooding."""
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page()
            event_count = 0

            async def on_console(params):
                nonlocal event_count
                event_count += 1

            session.on("Runtime.consoleAPICalled", on_console)
            # Generate many console.log events
            await session.runtime.evaluate("for(let i=0;i<10000;i++)console.log(i)")
            # Should handle gracefully without crash
```

---

## Implementation Timeline

### Week 1-2: Core Integration Tests
- [ ] Phase 1: Core workflows (navigation, multi-tab)
- [ ] Phase 2: Page domain integration tests
- [ ] Phase 2: Runtime domain integration tests

### Week 3-4: High-Value Integration Tests
- [ ] Phase 2: Network domain integration tests
- [ ] Phase 2: Emulation domain integration tests
- [ ] Phase 2: Input domain integration tests
- [ ] Phase 2: Fetch domain integration tests

### Week 5-6: Edge Case Tests
- [ ] Phase 3: Error handling tests
- [ ] Phase 3: Invalid input tests
- [ ] Phase 3: Timeout tests
- [ ] Phase 3: Crash recovery tests

### Week 7-8: Performance & Security
- [ ] Performance benchmarks
- [ ] Memory leak tests
- [ ] Security validation tests
- [ ] Resource limit tests

### Week 9-10: Tier 3 Domains
- [ ] CSS domain integration tests
- [ ] Storage domain integration tests
- [ ] Debugger domain integration tests
- [ ] Remaining Tier 3 domains

---

## Success Criteria

### Coverage Goals

- **Unit test coverage**: ≥95% (currently 89%)
- **Integration test coverage**: ≥80% of critical paths
- **Edge case coverage**: ≥70% of identified edge cases
- **Error handling coverage**: ≥80% of error conditions

### Quality Goals

- All tests pass on every commit
- No flaky tests (tests that sometimes fail)
- Test execution time < 5 minutes for full suite
- Integration tests run in CI with Chrome headless

### Documentation Goals

- Every test has a docstring explaining what it tests
- Test names clearly describe the scenario
- Complex tests have comments explaining setup

---

## Running Tests

### Unit Tests (No browser required)

```bash
python -m pytest tests/unit/ -v --cov=cdpwave --cov-report=term-missing
```

### Integration Tests (Requires Chrome)

```bash
python -m pytest tests/integration/ -v --integration
```

### Manual Smoke Test

```bash
python tests/manual_smoke.py
```

### Full Test Suite

```bash
python -m pytest tests/ -v --cov=cdpwave --cov-report=html
```

---

## Test Writing Guidelines

### Unit Tests

- Use `FakeSender` pattern for mocking CDP responses
- Test both success and error paths
- Verify exact CDP method and params sent
- Keep tests focused on one behavior

### Integration Tests

- Use real Chrome (headless in CI, local for debugging)
- Test complete workflows, not individual methods
- Clean up resources (close sessions, browser)
- Use `pytest.mark.integration` marker

### Edge Case Tests

- Test boundary conditions (empty, null, max values)
- Test error conditions (network errors, timeouts)
- Test concurrent operations
- Test resource exhaustion

### Performance Tests

- Measure actual latency, not just functionality
- Run multiple iterations for statistical significance
- Set clear thresholds for acceptable performance
- Track metrics over time for regression detection

---

## Contributing Tests

When adding new functionality:

1. **Add unit tests** for all new methods (use `FakeSender`)
2. **Add integration tests** for new workflows
3. **Update this roadmap** with new test requirements
4. **Ensure coverage** doesn't drop below 95%
5. **Run full test suite** before committing

Test files should follow naming convention:
- Unit tests: `tests/unit/test_<module>.py`
- Domain tests: `tests/unit/domains/test_<domain>.py`
- Integration tests: `tests/integration/test_<feature>.py`
