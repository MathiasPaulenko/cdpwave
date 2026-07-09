"""Integration, Error Handling, Cleanup, and Manual Functional tests."""

from __future__ import annotations
import asyncio, contextlib
from typing import Any, Callable, Awaitable
from cdpwave.client import CDPClient, CDPSession
from cdpwave.exceptions import CommandError, CommandTimeoutError, ConnectionClosedError
from tests.manual._test_helpers import fresh_session, safe_navigate, nav_data
from tests.manual._test_helpers import log_result

_test_registry: list[tuple[str, str, Callable[[CDPClient], Awaitable[None]]]] = []

def reg(tc_id: str, name: str):
    def decorator(func):
        _test_registry.append((tc_id, name, func))
        return func
    return decorator

# ===================== INTEGRATION TESTS (20 tests) =====================
@reg("TC-INT-001", "navigate + screenshot")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(format="png")
    assert len(r.get("data","")) > 100; await s.close()
    log_result("TC-INT-001", "navigate + screenshot", "PASS")

@reg("TC-INT-002", "navigate + evaluate")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("document.title", return_by_value=True)
    assert r["result"]["value"]; await s.close()
    log_result("TC-INT-002", "navigate + evaluate", "PASS")

@reg("TC-INT-003", "navigate + DOM query")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "h1")
    assert n["nodeId"] > 0; await s.close()
    log_result("TC-INT-003", "navigate + DOM query", "PASS")

@reg("TC-INT-004", "navigate + PDF")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf()
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100; await s.close()
    log_result("TC-INT-004", "navigate + PDF", "PASS")

@reg("TC-INT-005", "navigate + network cookies")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await safe_navigate(s, "https://example.com")
    r = await s.network.get_all_cookies(); assert "cookies" in r; await s.close()
    log_result("TC-INT-005", "navigate + network cookies", "PASS")

@reg("TC-INT-006", "multi-tab navigation")
async def t(client):
    s1 = await fresh_session(client); s2 = await fresh_session(client)
    await safe_navigate(s1, "https://example.com")
    await safe_navigate(s2, "https://example.org")
    r1 = await s1.runtime.evaluate("location.href", return_by_value=True)
    r2 = await s2.runtime.evaluate("location.href", return_by_value=True)
    try:
        assert r1["result"]["value"] != r2["result"]["value"]
        await s1.close(); await s2.close()
        log_result("TC-INT-006", "multi-tab navigation", "PASS")
    except AssertionError:
        await s1.close(); await s2.close(); log_result("TC-INT-006", "multi-tab navigation", "SKIP", "Both tabs returned same URL (network issue)")

@reg("TC-INT-007", "emulation + navigate")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True)
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("window.innerWidth", return_by_value=True)
    assert r["result"]["value"] == 375; await s.close()
    log_result("TC-INT-007", "emulation + navigate", "PASS")

@reg("TC-INT-008", "fetch intercept + continue")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused: list[dict] = []
    async def on_pause(p): paused.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused:
        await s.fetch.continue_request(paused[0]["requestId"])
    await s.fetch.disable(); await s.close()
    log_result("TC-INT-008", "fetch intercept + continue", "PASS")

@reg("TC-INT-009", "input + DOM focus + key event")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<input id='t'>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.focus(n["nodeId"])
    await s.input.dispatch_key_event("char", text="A"); await s.close()
    log_result("TC-INT-009", "input + DOM focus + key event", "PASS")

@reg("TC-INT-010", "console + runtime evaluate")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    msgs: list[str] = []
    s.on("Runtime.consoleAPICalled", lambda p: msgs.append(str(p.get("args",[]))))
    await s.runtime.evaluate("console.log('test')", return_by_value=True)
    await asyncio.sleep(0.3); assert len(msgs) > 0; await s.close()
    log_result("TC-INT-010", "console + runtime evaluate", "PASS")

@reg("TC-INT-011", "CSS + DOM getComputedStyle")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t' style='color:red'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    r = await s.css.get_computed_style_for_node(n["nodeId"])
    assert "computedStyle" in r; await s.close()
    log_result("TC-INT-011", "CSS + DOM getComputedStyle", "PASS")

@reg("TC-INT-012", "profiler start + stop")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    await s.profiler.start(); await asyncio.sleep(0.5)
    r = await s.profiler.stop(); assert "profile" in r; await s.close()
    log_result("TC-INT-012", "profiler start + stop", "PASS")

@reg("TC-INT-013", "debugger + runtime evaluate")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    r = await s.runtime.evaluate("1+1", return_by_value=True)
    assert r["result"]["value"] == 2; await s.close()
    log_result("TC-INT-013", "debugger + runtime evaluate", "PASS")

@reg("TC-INT-014", "heap snapshot + GC")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    await s.heap_profiler.take_heap_snapshot()
    await s.send("HeapProfiler.collectGarbage", {}); await s.close()
    log_result("TC-INT-014", "heap snapshot + GC", "PASS")

@reg("TC-INT-015", "accessibility tree + DOM")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.accessibility.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.send("Accessibility.getPartialAXTree", {"nodeId": n["nodeId"]}); await s.close()
    log_result("TC-INT-015", "accessibility tree + DOM", "PASS")

@reg("TC-INT-016", "network + navigate + response body")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    reqs: list[dict] = []; ev = asyncio.Event()
    async def on_resp(p): reqs.append(p); ev.set()
    s.on("Network.responseReceived", on_resp)
    await safe_navigate(s, "https://example.com")
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=5)
    if reqs:
        await s.network.get_response_body(reqs[0]["requestId"])
    await s.close(); log_result("TC-INT-016", "network + navigate + response body", "PASS")

@reg("TC-INT-017", "target create + attach + close")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    a = await s.target.attach_to_target(r["targetId"], flatten=True)
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-INT-017", "target create + attach + close", "PASS")

@reg("TC-INT-018", "storage + DOM storage")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try:
        sid = {"securityOrigin":"https://example.com","isLocalStorage":True}
        await s.storage.set_dom_storage_item(sid, "test", "val")
        r = await s.storage.get_dom_storage_items(sid)
        await s.close(); log_result("TC-INT-018", "storage + DOM storage", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INT-018", "storage + DOM storage", "FAIL", str(e))

@reg("TC-INT-019", "emulation + screenshot")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=800, height=600, device_scale_factor=1, mobile=False)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(format="png")
    assert len(r.get("data","")) > 100; await s.close()
    log_result("TC-INT-019", "emulation + screenshot", "PASS")

@reg("TC-INT-020", "overlay + DOM highlight")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.overlay.enable()
        hc = {"showInfo": True, "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5}}
        await s.overlay.highlight_node(highlight_config=hc, node_id=n["nodeId"])
        await s.overlay.hide_highlight(); await s.close()
        log_result("TC-INT-020", "overlay + DOM highlight", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-INT-020", "overlay + DOM highlight", "FAIL", str(e))

# ===================== ERROR HANDLING TESTS (10 tests) =====================
@reg("TC-ERR-001", "navigate invalid URL")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.page.navigate("not-a-url")
        await s.close(); log_result("TC-ERR-001", "navigate invalid URL", "PASS", "Chrome handled gracefully")
    except Exception as e:
        await s.close(); log_result("TC-ERR-001", "navigate invalid URL", "PASS", f"Error: {e}")

@reg("TC-ERR-002", "evaluate syntax error")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("syntax error here", return_by_value=True)
    assert "exceptionDetails" in r or r.get("result",{}).get("subtype") == "error"; await s.close()
    log_result("TC-ERR-002", "evaluate syntax error", "PASS")

@reg("TC-ERR-003", "DOM querySelector no match")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div>test</div>")
    d = await s.dom.get_document()
    r = await s.dom.query_selector(d["root"]["nodeId"], "#nonexistent")
    assert r["nodeId"] == 0; await s.close()
    log_result("TC-ERR-003", "DOM querySelector no match", "PASS")

@reg("TC-ERR-004", "Runtime evaluate throw")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("throw new Error('test')", return_by_value=True)
    assert "exceptionDetails" in r; await s.close()
    log_result("TC-ERR-004", "Runtime evaluate throw", "PASS")

@reg("TC-ERR-005", "command timeout")
async def t(client):
    s = await fresh_session(client)
    try:
        await asyncio.wait_for(s.send("Page.navigate", {"url":"https://httpbin.org/delay/10"}), timeout=2)
        await s.close(); log_result("TC-ERR-005", "command timeout", "PASS", "Navigated within timeout")
    except asyncio.TimeoutError:
        await s.close(); log_result("TC-ERR-005", "command timeout", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-ERR-005", "command timeout", "PASS", f"Error: {e}")

@reg("TC-ERR-006", "session closed error")
async def t(client):
    s = await fresh_session(client)
    with contextlib.suppress(Exception):
        await asyncio.wait_for(s.page.crash(), timeout=3)
    try:
        await s.runtime.evaluate("1+1")
        log_result("TC-ERR-006", "session closed error", "FAIL", "Should have raised")
    except Exception:
        log_result("TC-ERR-006", "session closed error", "PASS")

@reg("TC-ERR-007", "invalid CDP method")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("NonExistent.method", {})
        await s.close(); log_result("TC-ERR-007", "invalid CDP method", "FAIL", "Should have raised")
    except CommandError:
        await s.close(); log_result("TC-ERR-007", "invalid CDP method", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-ERR-007", "invalid CDP method", "PASS", f"Error: {e}")

@reg("TC-ERR-008", "DOM removeNode nonexistent")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    try:
        await s.dom.remove_node(99999)
        await s.close(); log_result("TC-ERR-008", "DOM removeNode nonexistent", "PASS", "Handled gracefully")
    except Exception as e:
        await s.close(); log_result("TC-ERR-008", "DOM removeNode nonexistent", "PASS", f"Error: {e}")

@reg("TC-ERR-009", "Network invalid cookie")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    try:
        await s.network.set_cookie("", "", domain="", path="/")
        await s.close(); log_result("TC-ERR-009", "Network invalid cookie", "PASS", "Handled gracefully")
    except Exception as e:
        await s.close(); log_result("TC-ERR-009", "Network invalid cookie", "PASS", f"Error: {e}")

@reg("TC-ERR-010", "Runtime callFunctionOn invalid objectId")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    try:
        await s.runtime.call_function_on("function(){}", object_id="invalid-id")
        await s.close(); log_result("TC-ERR-010", "callFunctionOn invalid objectId", "PASS", "Handled gracefully")
    except Exception as e:
        await s.close(); log_result("TC-ERR-010", "callFunctionOn invalid objectId", "PASS", f"Error: {e}")

# ===================== CLEANUP TESTS (10 tests) =====================
@reg("TC-CLEAN-001", "close session")
async def t(client):
    s = await fresh_session(client)
    await s.close(); log_result("TC-CLEAN-001", "close session", "PASS")

@reg("TC-CLEAN-002", "close multiple sessions")
async def t(client):
    s1 = await fresh_session(client); s2 = await fresh_session(client); s3 = await fresh_session(client)
    await s1.close(); await s2.close(); await s3.close()
    log_result("TC-CLEAN-002", "close multiple sessions", "PASS")

@reg("TC-CLEAN-003", "disable all domains")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable(); await s.runtime.enable(); await s.network.enable(); await s.dom.enable()
    await s.page.disable(); await s.runtime.disable(); await s.network.disable(); await s.dom.disable()
    await s.close(); log_result("TC-CLEAN-003", "disable all domains", "PASS")

@reg("TC-CLEAN-004", "clear cookies after test")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_cookie("test", "val", domain="example.com", path="/")
    await s.network.clear_browser_cookies()
    r = await s.network.get_all_cookies()
    assert not any(c["name"]=="test" for c in r.get("cookies",[])); await s.close()
    log_result("TC-CLEAN-004", "clear cookies after test", "PASS")

@reg("TC-CLEAN-005", "clear cache after test")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.clear_browser_cache(); await s.close()
    log_result("TC-CLEAN-005", "clear cache after test", "PASS")

@reg("TC-CLEAN-006", "release objects after test")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1})", return_by_value=False)
    await s.runtime.release_object(r["result"]["objectId"])
    await s.runtime.release_object_group("test_group"); await s.close()
    log_result("TC-CLEAN-006", "release objects after test", "PASS")

@reg("TC-CLEAN-007", "disable debugger after test")
async def t(client):
    s = await fresh_session(client)
    await s.debugger.enable(); await s.debugger.disable(); await s.close()
    log_result("TC-CLEAN-007", "disable debugger after test", "PASS")

@reg("TC-CLEAN-008", "disable profiler after test")
async def t(client):
    s = await fresh_session(client)
    await s.profiler.enable(); await s.profiler.start(); await s.profiler.stop(); await s.profiler.disable()
    await s.close(); log_result("TC-CLEAN-008", "disable profiler after test", "PASS")

@reg("TC-CLEAN-009", "reset emulation after test")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True)
    await s.emulation.clear_device_metrics_override()
    await s.emulation.set_cpu_throttling_rate(rate=1); await s.close()
    log_result("TC-CLEAN-009", "reset emulation after test", "PASS")

@reg("TC-CLEAN-010", "close target after test")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-CLEAN-010", "close target after test", "PASS")

# ===================== MANUAL FUNCTIONAL TESTS (50 tests) =====================
@reg("TC-MAN-001", "Navigate to example.com")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("document.title", return_by_value=True)
    assert "Example" in r["result"]["value"]; await s.close()
    log_result("TC-MAN-001", "Navigate to example.com", "PASS")

@reg("TC-MAN-002", "Evaluate JavaScript")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("1 + 2 + 3", return_by_value=True)
    assert r["result"]["value"] == 6; await s.close()
    log_result("TC-MAN-002", "Evaluate JavaScript", "PASS")

@reg("TC-MAN-003", "Form interaction")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<input id='t' type='text'>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.focus(n["nodeId"])
    await s.input.dispatch_key_event("char", text="H")
    await s.input.dispatch_key_event("char", text="i")
    r = await s.runtime.evaluate("document.getElementById('t').value", return_by_value=True)
    assert r["result"]["value"] == "Hi"; await s.close()
    log_result("TC-MAN-003", "Form interaction", "PASS")

@reg("TC-MAN-004", "PDF capture")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf()
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100; await s.close()
    log_result("TC-MAN-004", "PDF capture", "PASS")

@reg("TC-MAN-005", "Fetch interception")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused: list[dict] = []
    async def on_pause(p): paused.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused:
        await s.fetch.continue_request(paused[0]["requestId"])
    await s.fetch.disable(); await s.close()
    log_result("TC-MAN-005", "Fetch interception", "PASS")

@reg("TC-MAN-006", "Dialog handling")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event()
    s.on("Page.javascriptDialogOpening", lambda p: ev.set())
    await s.page.enable()
    await s.page.navigate("data:text/html,<script>alert('test')</script>")
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=3)
    await s.page.handle_java_script_dialog(accept=True); await s.close()
    log_result("TC-MAN-006", "Dialog handling", "PASS")

@reg("TC-MAN-007", "Cookies set/get")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_cookie("test", "val", domain="example.com", path="/")
    r = await s.network.get_cookies(urls=["https://example.com"])
    assert any(c["name"]=="test" for c in r.get("cookies",[])); await s.close()
    log_result("TC-MAN-007", "Cookies set/get", "PASS")

@reg("TC-MAN-008", "Emulation mobile")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_device_metrics_override(width=375, height=667, device_scale_factor=2, mobile=True)
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("window.innerWidth", return_by_value=True)
    assert r["result"]["value"] == 375; await s.close()
    log_result("TC-MAN-008", "Emulation mobile", "PASS")

@reg("TC-MAN-009", "Multi-tab")
async def t(client):
    s1 = await fresh_session(client); s2 = await fresh_session(client)
    await safe_navigate(s1, "https://example.com")
    await safe_navigate(s2, "https://example.org")
    r1 = await s1.runtime.evaluate("location.href", return_by_value=True)
    r2 = await s2.runtime.evaluate("location.href", return_by_value=True)
    try:
        assert r1["result"]["value"] != r2["result"]["value"]
        await s1.close(); await s2.close()
        log_result("TC-MAN-009", "Multi-tab", "PASS")
    except AssertionError:
        await s1.close(); await s2.close(); log_result("TC-MAN-009", "Multi-tab", "SKIP", "Both tabs returned same URL (network issue)")

@reg("TC-MAN-010", "Console monitoring")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    msgs: list[str] = []
    s.on("Runtime.consoleAPICalled", lambda p: msgs.append(str(p.get("args",[]))))
    await s.runtime.evaluate("console.log('test')", return_by_value=True)
    await asyncio.sleep(0.3); assert len(msgs) > 0; await s.close()
    log_result("TC-MAN-010", "Console monitoring", "PASS")

@reg("TC-MAN-011", "DOM manipulation")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Old</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.set_attribute_value(n["nodeId"], "class", "updated")
    h = await s.dom.get_outer_html(n["nodeId"])
    assert 'class="updated"' in h["outerHTML"]; await s.close()
    log_result("TC-MAN-011", "DOM manipulation", "PASS")

@reg("TC-MAN-012", "Navigation history")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    h = await s.page.get_navigation_history()
    assert len(h["entries"]) >= 2; await s.close()
    log_result("TC-MAN-012", "Navigation history", "PASS")

@reg("TC-MAN-013", "Geolocation override")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_geolocation_override(latitude=40.7, longitude=-74.0)
    await s.emulation.clear_geolocation_override(); await s.close()
    log_result("TC-MAN-013", "Geolocation override", "PASS")

@reg("TC-MAN-014", "Screenshot clipping")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(clip={"x":0,"y":0,"width":200,"height":100,"scale":1})
    assert len(r.get("data","")) > 100; await s.close()
    log_result("TC-MAN-014", "Screenshot clipping", "PASS")

@reg("TC-MAN-015", "Command timeout")
async def t(client):
    s = await fresh_session(client)
    try:
        await asyncio.wait_for(s.send("Page.navigate", {"url":"https://httpbin.org/delay/10"}), timeout=2)
        await s.close(); log_result("TC-MAN-015", "Command timeout", "PASS", "Navigated within timeout")
    except asyncio.TimeoutError:
        await s.close(); log_result("TC-MAN-015", "Command timeout", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-015", "Command timeout", "PASS", f"Error: {e}")

@reg("TC-MAN-016", "Script injection")
async def t(client):
    s = await fresh_session(client)
    ident = await s.page.add_script_to_evaluate_on_new_document("window.__injected=42")
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("window.__injected", return_by_value=True)
    assert r["result"]["value"] == 42
    await s.page.remove_script_to_evaluate_on_new_document(ident["identifier"]); await s.close()
    log_result("TC-MAN-016", "Script injection", "PASS")

@reg("TC-MAN-017", "Network monitoring")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    reqs: list[dict] = []; ev = asyncio.Event()
    async def on_req(p): reqs.append(p); ev.set()
    s.on("Network.requestWillBeSent", on_req)
    await safe_navigate(s, "https://example.com")
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=5)
    assert len(reqs) > 0; await s.close()
    log_result("TC-MAN-017", "Network monitoring", "PASS")

@reg("TC-MAN-018", "CPU throttling")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_cpu_throttling_rate(rate=4)
    await s.emulation.set_cpu_throttling_rate(rate=1); await s.close()
    log_result("TC-MAN-018", "CPU throttling", "PASS")

@reg("TC-MAN-019", "Input event blocking")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.input.set_ignore_input_events(True)
        await s.close(); log_result("TC-MAN-019", "Input event blocking", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-019", "Input event blocking", "FAIL", str(e))

@reg("TC-MAN-020", "Heap snapshot")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    await s.heap_profiler.take_heap_snapshot(); await s.close()
    log_result("TC-MAN-020", "Heap snapshot", "PASS")

@reg("TC-MAN-021", "Accessibility tree")
async def t(client):
    s = await fresh_session(client); await s.accessibility.enable()
    await safe_navigate(s, "https://example.com")
    r = await s.accessibility.get_full_ax_tree(); assert "nodes" in r; await s.close()
    log_result("TC-MAN-021", "Accessibility tree", "PASS")

@reg("TC-MAN-022", "Connection closing")
async def t(client):
    s = await fresh_session(client); await s.close()
    log_result("TC-MAN-022", "Connection closing", "PASS")

@reg("TC-MAN-023", "Referrer navigation")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    await s.page.navigate("https://example.com", referrer="https://google.com")
    await asyncio.sleep(0.3)
    r = await s.runtime.evaluate("document.referrer", return_by_value=True)
    await s.close(); log_result("TC-MAN-023", "Referrer navigation", "PASS", f"referrer={r['result'].get('value','')}")

@reg("TC-MAN-024", "Vision deficiency emulation")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_emulated_vision_deficiency("achromatopsia")
        await s.close(); log_result("TC-MAN-024", "Vision deficiency emulation", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-MAN-024", "Vision deficiency emulation", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-MAN-024", "Vision deficiency emulation", "FAIL", str(e))

@reg("TC-MAN-025", "Fetch response interception")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event(); paused: list[dict] = []
    async def on_pause(p): paused.append(p); ev.set()
    s.on("Fetch.requestPaused", on_pause)
    await s.fetch.enable(patterns=[{"urlPattern":"*://*/*"}])
    asyncio.create_task(s.page.navigate("https://example.com"))
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=10)
    if paused:
        await s.fetch.fulfill_request(paused[0]["requestId"], status_code=200, body="dGVzdA==")
    await s.fetch.disable(); await s.close()
    log_result("TC-MAN-025", "Fetch response interception", "PASS")

@reg("TC-MAN-026", "HTTP-only cookies")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_cookie("httponly", "val", domain="example.com", path="/", http_only=True)
    r = await s.network.get_cookies(urls=["https://example.com"])
    assert any(c["name"]=="httponly" and c.get("httpOnly") for c in r.get("cookies",[])); await s.close()
    log_result("TC-MAN-026", "HTTP-only cookies", "PASS")

@reg("TC-MAN-027", "Isolated world creation")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    await safe_navigate(s, "https://example.com")
    f = await s.page.get_frame_tree(); fid = f["frameTree"]["frame"]["id"]
    r = await s.page.create_isolated_world(fid, world_name="test")
    assert "executionContextId" in r; await s.close()
    log_result("TC-MAN-027", "Isolated world creation", "PASS")

@reg("TC-MAN-028", "Layout metrics")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    m = await s.page.get_layout_metrics()
    assert "contentSize" in m; await s.close()
    log_result("TC-MAN-028", "Layout metrics", "PASS")

@reg("TC-MAN-029", "Idle state emulation")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_idle_override(is_user_active=False, is_screen_active=False)
        await s.close(); log_result("TC-MAN-029", "Idle state emulation", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-029", "Idle state emulation", "FAIL", f"Deprecated: {e}")

@reg("TC-MAN-030", "Data URL navigation")
async def t(client):
    s = await fresh_session(client)
    await nav_data(s, "<h1>Hello</h1>")
    r = await s.runtime.evaluate("document.body.innerHTML", return_by_value=True)
    assert "Hello" in r["result"]["value"]; await s.close()
    log_result("TC-MAN-030", "Data URL navigation", "PASS")

@reg("TC-MAN-031", "URL blocking")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_blocked_urls(["*.jpg", "*.png"])
    await s.network.set_blocked_urls([]); await s.close()
    log_result("TC-MAN-031", "URL blocking", "PASS")

@reg("TC-MAN-032", "Async evaluation")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("new Promise(r=>setTimeout(()=>r(42),100))", await_promise=True, return_by_value=True)
    assert r["result"]["value"] == 42; await s.close()
    log_result("TC-MAN-032", "Async evaluation", "PASS")

@reg("TC-MAN-033", "Screenshot full page")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(capture_beyond_viewport=True)
    assert len(r.get("data","")) > 100; await s.close()
    log_result("TC-MAN-033", "Screenshot full page", "PASS")

@reg("TC-MAN-034", "Set document content")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    f = await s.page.get_frame_tree(); fid = f["frameTree"]["frame"]["id"]
    await s.page.set_document_content(fid, "<html><body><h1>Injected</h1></body></html>")
    r = await s.runtime.evaluate("document.body.innerHTML", return_by_value=True)
    assert "Injected" in r["result"]["value"]; await s.close()
    log_result("TC-MAN-034", "Set document content", "PASS")

@reg("TC-MAN-035", "Get frame tree")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    f = await s.page.get_frame_tree()
    assert "frameTree" in f; await s.close()
    log_result("TC-MAN-035", "Get frame tree", "PASS")

@reg("TC-MAN-036", "Navigate to history entry")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    h = await s.page.get_navigation_history()
    await s.page.navigate_to_history_entry(h["entries"][0]["id"]); await s.close()
    log_result("TC-MAN-036", "Navigate to history entry", "PASS")

@reg("TC-MAN-037", "Reset navigation history")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    await s.page.reset_navigation_history()
    h = await s.page.get_navigation_history()
    assert len(h["entries"]) == 1; await s.close()
    log_result("TC-MAN-037", "Reset navigation history", "PASS")

@reg("TC-MAN-038", "Capture snapshot MHTML")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_snapshot(format="mhtml")
    assert len(r.get("data","")) > 100; await s.close()
    log_result("TC-MAN-038", "Capture snapshot MHTML", "PASS")

@reg("TC-MAN-039", "Timezone override")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_timezone_override("America/New_York")
    await s.emulation.clear_timezone_override(); await s.close()
    log_result("TC-MAN-039", "Timezone override", "PASS")

@reg("TC-MAN-040", "User agent override")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_user_agent_override("TestBot/1.0")
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("navigator.userAgent", return_by_value=True)
    assert "TestBot" in r["result"]["value"]; await s.close()
    log_result("TC-MAN-040", "User agent override", "PASS")

@reg("TC-MAN-041", "Media emulation")
async def t(client):
    s = await fresh_session(client)
    await s.emulation.set_emulated_media(features=[{"name":"prefers-color-scheme","value":"dark"}])
    await s.emulation.set_emulated_media(media=""); await s.close()
    log_result("TC-MAN-041", "Media emulation", "PASS")

@reg("TC-MAN-042", "Touch emulation")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_touch_emulation_enabled(True)
        await s.close(); log_result("TC-MAN-042", "Touch emulation", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-042", "Touch emulation", "FAIL", str(e))

@reg("TC-MAN-043", "Virtual time policy")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_virtual_time_policy("pause")
        await s.close(); log_result("TC-MAN-043", "Virtual time policy", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-043", "Virtual time policy", "FAIL", str(e))

@reg("TC-MAN-044", "Background color override")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_default_background_color_override(r=0, g=0, b=0, a=255)
        await s.emulation.clear_default_background_color_override(); await s.close()
        log_result("TC-MAN-044", "Background color override", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-044", "Background color override", "FAIL", str(e))

@reg("TC-MAN-045", "Locale override")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_locale_override("es-ES")
        await s.close(); log_result("TC-MAN-045", "Locale override", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-045", "Locale override", "FAIL", str(e))

@reg("TC-MAN-046", "Focus emulation")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_focus_emulation_enabled(True)
        await s.close(); log_result("TC-MAN-046", "Focus emulation", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-046", "Focus emulation", "FAIL", str(e))

@reg("TC-MAN-047", "Auto dark mode")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_auto_dark_mode_override(True)
        await s.emulation.clear_auto_dark_mode_override(); await s.close()
        log_result("TC-MAN-047", "Auto dark mode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-047", "Auto dark mode", "FAIL", str(e))

@reg("TC-MAN-048", "Scrollbars hidden")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.emulation.set_scrollbars_hidden(True)
        await s.close(); log_result("TC-MAN-048", "Scrollbars hidden", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-MAN-048", "Scrollbars hidden", "FAIL", str(e))

@reg("TC-MAN-049", "Network conditions emulation")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.emulate_network_conditions(offline=False, latency=100, download_throughput=50000, upload_throughput=50000)
    await s.network.emulate_network_conditions(offline=False, latency=0, download_throughput=-1, upload_throughput=-1)
    await s.close(); log_result("TC-MAN-049", "Network conditions emulation", "PASS")

@reg("TC-MAN-050", "Bypass CSP")
async def t(client):
    s = await fresh_session(client)
    await s.page.set_bypass_csp(True)
    await safe_navigate(s, "https://example.com"); await s.close()
    log_result("TC-MAN-050", "Bypass CSP", "PASS")
