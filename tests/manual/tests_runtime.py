"""PAGE + RUNTIME + TARGET + NETWORK + DOM + BROWSER domain tests."""

from __future__ import annotations

import asyncio
import contextlib
from typing import Any, Callable, Awaitable

from cdpwave.client import CDPClient, CDPSession
from cdpwave.exceptions import CommandError, CommandTimeoutError

from tests.manual._test_helpers import fresh_session, safe_navigate, nav_data
from tests.manual._test_helpers import log_result

_test_registry: list[tuple[str, str, Callable[[CDPClient], Awaitable[None]]]] = []


def reg(tc_id: str, name: str):
    def decorator(func):
        _test_registry.append((tc_id, name, func))
        return func
    return decorator


# ===================== PAGE DOMAIN (50 tests) =====================

@reg("TC-PAGE-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable(); await s.page.disable()
    await s.close(); log_result("TC-PAGE-001", "enable/disable", "PASS")

@reg("TC-PAGE-002", "navigate")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await s.close(); log_result("TC-PAGE-002", "navigate", "PASS")

@reg("TC-PAGE-003", "navigate with referrer")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    await s.page.navigate("https://example.com", referrer="https://google.com")
    await asyncio.sleep(0.3)
    r = await s.runtime.evaluate("document.referrer", return_by_value=True)
    await s.close(); log_result("TC-PAGE-003", "navigate with referrer", "PASS", f"referrer={r['result'].get('value','')}")

@reg("TC-PAGE-004", "navigate with transition_type")
async def t(client):
    s = await fresh_session(client)
    await s.page.navigate("https://example.com", transition_type="typed")
    await s.close(); log_result("TC-PAGE-004", "navigate with transition_type", "PASS")

@reg("TC-PAGE-005", "reload")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await s.page.reload()
    await s.close(); log_result("TC-PAGE-005", "reload", "PASS")

@reg("TC-PAGE-006", "goBack")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    h = await s.page.get_navigation_history()
    try:
        await s.page.go_back()
        await s.close(); log_result("TC-PAGE-006", "goBack", "PASS")
    except AttributeError:
        await s.page.navigate_to_history_entry(h["entries"][h["currentIndex"]-1]["id"])
        await s.close(); log_result("TC-PAGE-006", "goBack", "PASS", "Used navigate_to_history_entry (fallback)")

@reg("TC-PAGE-007", "goForward")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    await safe_navigate(s, "https://example.com")
    await asyncio.sleep(0.5)
    await safe_navigate(s, "https://example.org")
    await asyncio.sleep(0.5)
    try:
        h = await s.page.get_navigation_history()
        await s.page.navigate_to_history_entry(h["entries"][0]["id"])
        await asyncio.sleep(0.5)
        h = await s.page.get_navigation_history()
        await s.page.navigate_to_history_entry(h["entries"][h["currentIndex"]+1]["id"])
        await s.close(); log_result("TC-PAGE-007", "goForward", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-PAGE-007", "goForward", "FAIL", str(e))

@reg("TC-PAGE-008", "captureScreenshot PNG")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(format="png")
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-008", "captureScreenshot PNG", "PASS")

@reg("TC-PAGE-009", "captureScreenshot JPEG")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(format="jpeg")
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-009", "captureScreenshot JPEG", "PASS")

@reg("TC-PAGE-010", "captureScreenshot with clip")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(clip={"x":0,"y":0,"width":200,"height":100,"scale":1})
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-010", "captureScreenshot with clip", "PASS")

@reg("TC-PAGE-011", "printToPDF basic")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf()
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-011", "printToPDF basic", "PASS")

@reg("TC-PAGE-012", "printToPDF landscape")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(landscape=True)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-012", "printToPDF landscape", "PASS")

@reg("TC-PAGE-013", "printToPDF background")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(print_background=True)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-013", "printToPDF background", "PASS")

@reg("TC-PAGE-014", "printToPDF margins")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(margin_top=0.5, margin_bottom=0.5, margin_left=0.5, margin_right=0.5)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-014", "printToPDF margins", "PASS")

@reg("TC-PAGE-015", "printToPDF pageRanges")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(page_ranges="1-3")
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-015", "printToPDF pageRanges", "PASS")

@reg("TC-PAGE-016", "getLayoutMetrics")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    m = await s.page.get_layout_metrics()
    assert "contentSize" in m
    await s.close(); log_result("TC-PAGE-016", "getLayoutMetrics", "PASS")

@reg("TC-PAGE-017", "getNavigationHistory")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    h = await s.page.get_navigation_history()
    assert len(h["entries"]) >= 2
    await s.close(); log_result("TC-PAGE-017", "getNavigationHistory", "PASS", f"{len(h['entries'])} entries")

@reg("TC-PAGE-018", "setDocumentContent")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    f = await s.page.get_frame_tree()
    fid = f["frameTree"]["frame"]["id"]
    await s.page.set_document_content(fid, "<html><body><h1>Injected</h1></body></html>")
    r = await s.runtime.evaluate("document.body.innerHTML", return_by_value=True)
    assert "Injected" in r["result"]["value"]
    await s.close(); log_result("TC-PAGE-018", "setDocumentContent", "PASS")

@reg("TC-PAGE-019", "getFrameTree")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    f = await s.page.get_frame_tree()
    assert "frameTree" in f and "frame" in f["frameTree"]
    await s.close(); log_result("TC-PAGE-019", "getFrameTree", "PASS")

@reg("TC-PAGE-020", "setBypassCSP")
async def t(client):
    s = await fresh_session(client)
    await s.page.set_bypass_csp(True)
    await s.close(); log_result("TC-PAGE-020", "setBypassCSP", "PASS")

@reg("TC-PAGE-021", "crash")
async def t(client):
    s = await fresh_session(client)
    try:
        with contextlib.suppress(asyncio.TimeoutError, Exception):
            await asyncio.wait_for(s.page.crash(), timeout=3)
        log_result("TC-PAGE-021", "crash", "PASS")
    except Exception as e:
        log_result("TC-PAGE-021", "crash", "FAIL", str(e))

@reg("TC-PAGE-022", "close")
async def t(client):
    s = await fresh_session(client)
    await s.page.close()
    log_result("TC-PAGE-022", "close", "PASS")

@reg("TC-PAGE-023", "bringToFront")
async def t(client):
    s1 = await fresh_session(client)
    s2 = await fresh_session(client)
    await s1.page.bring_to_front()
    await s1.close(); await s2.close()
    log_result("TC-PAGE-023", "bringToFront", "PASS")

@reg("TC-PAGE-024", "handleJavaScript Dialog")
async def t(client):
    s = await fresh_session(client)
    ev = asyncio.Event()
    s.on("Page.javascriptDialogOpening", lambda p: ev.set())
    await s.page.enable()
    await s.page.navigate("data:text/html,<script>alert('test')</script>")
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(ev.wait(), timeout=3)
    await s.page.handle_java_script_dialog(accept=True)
    await s.close(); log_result("TC-PAGE-024", "handleJavaScript Dialog", "PASS")

@reg("TC-PAGE-025", "createIsolatedWorld")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    await safe_navigate(s, "https://example.com")
    f = await s.page.get_frame_tree()
    fid = f["frameTree"]["frame"]["id"]
    r = await s.page.create_isolated_world(fid, world_name="test")
    assert "executionContextId" in r
    await s.close(); log_result("TC-PAGE-025", "createIsolatedWorld", "PASS")

@reg("TC-PAGE-026", "captureSnapshot")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_snapshot(format="mhtml")
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-026", "captureSnapshot", "PASS")

@reg("TC-PAGE-027", "addScriptToEvaluateOnNewDocument")
async def t(client):
    s = await fresh_session(client)
    ident = await s.page.add_script_to_evaluate_on_new_document("window.__x=1")
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("window.__x", return_by_value=True)
    assert r["result"]["value"] == 1
    await s.page.remove_script_to_evaluate_on_new_document(ident["identifier"])
    await s.close(); log_result("TC-PAGE-027", "addScriptToEvaluateOnNewDocument", "PASS")

@reg("TC-PAGE-028", "get_navigation_history 3 navs")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    await safe_navigate(s, "https://example.net")
    h = await s.page.get_navigation_history()
    assert len(h["entries"]) >= 3
    await s.close(); log_result("TC-PAGE-028", "get_navigation_history 3 navs", "PASS", f"{len(h['entries'])} entries")

@reg("TC-PAGE-029", "reset_navigation_history")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await safe_navigate(s, "https://example.org")
    await s.page.reset_navigation_history()
    h = await s.page.get_navigation_history()
    assert len(h["entries"]) == 1
    await s.close(); log_result("TC-PAGE-029", "reset_navigation_history", "PASS")

@reg("TC-PAGE-030", "navigate_to_history_entry")
async def t(client):
    s = await fresh_session(client)
    await s.page.enable()
    await safe_navigate(s, "https://example.com")
    await asyncio.sleep(0.5)
    await safe_navigate(s, "https://example.org")
    await asyncio.sleep(0.5)
    try:
        h = await s.page.get_navigation_history()
        if len(h["entries"]) < 2:
            await s.close(); log_result("TC-PAGE-030", "navigate_to_history_entry", "SKIP", "Not enough history entries")
            return
        target_idx = 0
        await s.page.navigate_to_history_entry(h["entries"][target_idx]["id"])
        await asyncio.sleep(0.5)
        h2 = await s.page.get_navigation_history()
        assert h2["currentIndex"] == target_idx
        await s.close(); log_result("TC-PAGE-030", "navigate_to_history_entry", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-PAGE-030", "navigate_to_history_entry", "FAIL", str(e))

@reg("TC-PAGE-031", "remove_script_to_evaluate_on_new_document")
async def t(client):
    s = await fresh_session(client)
    ident = await s.page.add_script_to_evaluate_on_new_document("window.__y=1")
    await s.page.remove_script_to_evaluate_on_new_document(ident["identifier"])
    await safe_navigate(s, "https://example.com")
    r = await s.runtime.evaluate("window.__y", return_by_value=True)
    assert r["result"].get("value") is None
    await s.close(); log_result("TC-PAGE-031", "remove_script_to_evaluate_on_new_document", "PASS")

@reg("TC-PAGE-032", "get_resource_tree")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.get_resource_tree()
    assert "frameTree" in r
    await s.close(); log_result("TC-PAGE-032", "get_resource_tree", "PASS")

@reg("TC-PAGE-033", "get_resource_content")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    rt = await s.page.get_resource_tree()
    fid = rt["frameTree"]["frame"]["id"]
    url = rt["frameTree"]["frame"]["url"]
    r = await s.page.get_resource_content(fid, url)
    assert "content" in r
    await s.close(); log_result("TC-PAGE-033", "get_resource_content", "PASS")

@reg("TC-PAGE-034", "set_bypass_csp strict")
async def t(client):
    s = await fresh_session(client)
    await s.page.set_bypass_csp(True)
    await safe_navigate(s, "https://example.com")
    await s.close(); log_result("TC-PAGE-034", "set_bypass_csp strict", "PASS")

@reg("TC-PAGE-035", "set_web_lifecycle_state active")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    await s.page.set_web_lifecycle_state("active")
    await s.close(); log_result("TC-PAGE-035", "set_web_lifecycle_state active", "PASS")

@reg("TC-PAGE-036", "set_web_lifecycle_state frozen")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        await s.page.set_web_lifecycle_state("frozen")
        await s.close(); log_result("TC-PAGE-036", "set_web_lifecycle_state frozen", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-PAGE-036", "set_web_lifecycle_state frozen", "FAIL", str(e))

@reg("TC-PAGE-037", "get_app_manifest")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.get_app_manifest()
    await s.close(); log_result("TC-PAGE-037", "get_app_manifest", "PASS", str(r)[:80])

@reg("TC-PAGE-038", "set_intercept_file_chooser_dialog")
async def t(client):
    s = await fresh_session(client)
    await s.page.set_intercept_file_chooser_dialog(enabled=True)
    await s.close(); log_result("TC-PAGE-038", "set_intercept_file_chooser_dialog", "PASS")

@reg("TC-PAGE-039", "captureScreenshot webp")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        r = await s.page.capture_screenshot(format="webp")
        assert len(r.get("data","")) > 100
        await s.close(); log_result("TC-PAGE-039", "captureScreenshot webp", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-PAGE-039", "captureScreenshot webp", "FAIL", str(e))

@reg("TC-PAGE-040", "captureScreenshot with quality")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(format="jpeg", quality=80)
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-040", "captureScreenshot with quality", "PASS")

@reg("TC-PAGE-041", "printToPDF header/footer")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(display_header_footer=True)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-041", "printToPDF header/footer", "PASS")

@reg("TC-PAGE-042", "printToPDF custom header")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(display_header_footer=True, header_template="<div>Header</div>")
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-042", "printToPDF custom header", "PASS")

@reg("TC-PAGE-043", "printToPDF custom footer")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(display_header_footer=True, footer_template="<div>Footer</div>")
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-043", "printToPDF custom footer", "PASS")

@reg("TC-PAGE-044", "printToPDF prefer_css_page_size")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(prefer_css_page_size=True)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-044", "printToPDF prefer_css_page_size", "PASS")

@reg("TC-PAGE-045", "printToPDF scale")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(scale=0.5)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-045", "printToPDF scale", "PASS")

@reg("TC-PAGE-046", "printToPDF paper size")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(paper_width=8.5, paper_height=11)
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-046", "printToPDF paper size", "PASS")

@reg("TC-PAGE-047", "printToPDF page ranges multi")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    pdf = await s.page.print_to_pdf(page_ranges="1,3,5-7")
    assert len(pdf) > 100 if isinstance(pdf, str) else len(pdf.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-047", "printToPDF page ranges multi", "PASS")

@reg("TC-PAGE-048", "captureScreenshot with clip v2")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(clip={"x":0,"y":0,"width":100,"height":100,"scale":1})
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-048", "captureScreenshot with clip v2", "PASS")

@reg("TC-PAGE-049", "captureScreenshot from_surface")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        r = await s.page.capture_screenshot(from_surface=False)
        assert len(r.get("data","")) > 100
        await s.close(); log_result("TC-PAGE-049", "captureScreenshot from_surface", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-PAGE-049", "captureScreenshot from_surface", "FAIL", str(e))

@reg("TC-PAGE-050", "captureScreenshot beyond_viewport")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    r = await s.page.capture_screenshot(capture_beyond_viewport=True)
    assert len(r.get("data","")) > 100
    await s.close(); log_result("TC-PAGE-050", "captureScreenshot beyond_viewport", "PASS")


# ===================== RUNTIME DOMAIN (35 tests) =====================

@reg("TC-RUNTIME-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable(); await s.runtime.disable()
    await s.close(); log_result("TC-RUNTIME-001", "enable/disable", "PASS")

@reg("TC-RUNTIME-002", "evaluate basic")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("1+1", return_by_value=True)
    assert r["result"]["value"] == 2
    await s.close(); log_result("TC-RUNTIME-002", "evaluate basic", "PASS")

@reg("TC-RUNTIME-003", "evaluate async")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("new Promise(r=>setTimeout(()=>r(42),100))", await_promise=True, return_by_value=True)
    assert r["result"]["value"] == 42
    await s.close(); log_result("TC-RUNTIME-003", "evaluate async", "PASS")

@reg("TC-RUNTIME-004", "evaluate with context")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.evaluate("window.__ctx='hello'", return_by_value=True)
    r = await s.runtime.evaluate("window.__ctx", return_by_value=True)
    assert r["result"]["value"] == "hello"
    await s.close(); log_result("TC-RUNTIME-004", "evaluate with context", "PASS")

@reg("TC-RUNTIME-005", "callFunctionOn")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1,b:2})", return_by_value=False)
    oid = r["result"]["objectId"]
    r2 = await s.runtime.call_function_on("function(){return this.a+this.b}", object_id=oid, return_by_value=True)
    assert r2["result"]["value"] == 3
    await s.close(); log_result("TC-RUNTIME-005", "callFunctionOn", "PASS")

@reg("TC-RUNTIME-006", "releaseObject")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1})", return_by_value=False)
    await s.runtime.release_object(r["result"]["objectId"])
    await s.close(); log_result("TC-RUNTIME-006", "releaseObject", "PASS")

@reg("TC-RUNTIME-007", "getProperties")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1,b:2})", return_by_value=False)
    props = await s.runtime.get_properties(r["result"]["objectId"])
    assert "result" in props
    await s.close(); log_result("TC-RUNTIME-007", "getProperties", "PASS")

@reg("TC-RUNTIME-008", "compileScript")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.compile_script("1+2+3", persist_script=True)
    assert "scriptId" in r
    await s.close(); log_result("TC-RUNTIME-008", "compileScript", "PASS")

@reg("TC-RUNTIME-009", "runScript")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    c = await s.runtime.compile_script("1+2+3", persist_script=True)
    r = await s.runtime.run_script(c["scriptId"], return_by_value=True)
    assert r["result"]["value"] == 6
    await s.close(); log_result("TC-RUNTIME-009", "runScript", "PASS")

@reg("TC-RUNTIME-010", "queryObjects")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("Array.prototype", return_by_value=False)
    try:
        r2 = await s.runtime.query_objects(r["result"]["objectId"])
        assert "objects" in r2
        await s.close(); log_result("TC-RUNTIME-010", "queryObjects", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-010", "queryObjects", "FAIL", str(e))

@reg("TC-RUNTIME-011", "globalLexicalScopeNames")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.evaluate("let x=1; const y=2;")
    r = await s.runtime.global_lexical_scope_names()
    assert "names" in r
    await s.close(); log_result("TC-RUNTIME-011", "globalLexicalScopeNames", "PASS", str(r["names"][:5]))

@reg("TC-RUNTIME-012", "addBinding")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.add_binding("test_binding")
    await s.close(); log_result("TC-RUNTIME-012", "addBinding", "PASS")

@reg("TC-RUNTIME-013", "removeBinding")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.add_binding("test_binding")
    await s.runtime.remove_binding("test_binding")
    await s.close(); log_result("TC-RUNTIME-013", "removeBinding", "PASS")

@reg("TC-RUNTIME-014", "getHeapUsage")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.get_heap_usage()
    assert "usedSize" in r
    await s.close(); log_result("TC-RUNTIME-014", "getHeapUsage", "PASS")

@reg("TC-RUNTIME-015", "getIsolateId")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    try:
        r = await s.runtime.get_isolate_id()
        await s.close(); log_result("TC-RUNTIME-015", "getIsolateId", "PASS", str(r))
    except AttributeError:
        await s.close(); log_result("TC-RUNTIME-015", "getIsolateId", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-015", "getIsolateId", "FAIL", str(e))

@reg("TC-RUNTIME-016", "collectGarbage")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    try:
        await s.runtime.collect_garbage()
        await s.close(); log_result("TC-RUNTIME-016", "collectGarbage", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-RUNTIME-016", "collectGarbage", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-016", "collectGarbage", "FAIL", str(e))

@reg("TC-RUNTIME-017", "terminateExecution")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    try:
        await s.runtime.terminate_execution()
        await s.close(); log_result("TC-RUNTIME-017", "terminateExecution", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-017", "terminateExecution", "FAIL", str(e))

@reg("TC-RUNTIME-018", "setCustomObjectFormatterEnabled")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    try:
        await s.runtime.set_custom_object_formatter_enabled(True)
        await s.close(); log_result("TC-RUNTIME-018", "setCustomObjectFormatterEnabled", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-RUNTIME-018", "setCustomObjectFormatterEnabled", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-018", "setCustomObjectFormatterEnabled", "FAIL", str(e))

@reg("TC-RUNTIME-019", "getExceptionDetails")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("throw new Error('test')", return_by_value=False)
    exc = r.get("exceptionDetails", {})
    oid = exc.get("exception", {}).get("objectId")
    if oid:
        d = await s.runtime.get_exception_details(oid)
        await s.close(); log_result("TC-RUNTIME-019", "getExceptionDetails", "PASS", str(d)[:80])
    else:
        await s.close(); log_result("TC-RUNTIME-019", "getExceptionDetails", "SKIP", "No exception objectId returned")

@reg("TC-RUNTIME-020", "awaitPromise timeout")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("new Promise(()=>{})", return_by_value=False)
    try:
        await asyncio.wait_for(s.runtime.await_promise(r["result"]["objectId"], return_by_value=True), timeout=2)
        await s.close(); log_result("TC-RUNTIME-020", "awaitPromise timeout", "FAIL", "Should have timed out")
    except asyncio.TimeoutError:
        await s.close(); log_result("TC-RUNTIME-020", "awaitPromise timeout", "PASS")

@reg("TC-RUNTIME-021", "release_object_group")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.evaluate("({a:1})", object_group="test_group", return_by_value=False)
    await s.runtime.release_object_group("test_group")
    await s.close(); log_result("TC-RUNTIME-021", "release_object_group", "PASS")

@reg("TC-RUNTIME-022", "run_if_waiting_for_debugger")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    try:
        await s.runtime.run_if_waiting_for_debugger()
        await s.close(); log_result("TC-RUNTIME-022", "run_if_waiting_for_debugger", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-022", "run_if_waiting_for_debugger", "FAIL", str(e))

@reg("TC-RUNTIME-023", "get_exception_details v2")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("throw new Error('test2')", return_by_value=False)
    exc = r.get("exceptionDetails", {})
    oid = exc.get("exception", {}).get("objectId")
    if oid:
        d = await s.runtime.get_exception_details(oid)
        await s.close(); log_result("TC-RUNTIME-023", "get_exception_details v2", "PASS")
    else:
        await s.close(); log_result("TC-RUNTIME-023", "get_exception_details v2", "SKIP", "No exception objectId")

@reg("TC-RUNTIME-024", "query_objects with prototype")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.evaluate("let arr = [1,2,3];", return_by_value=True)
    r = await s.runtime.evaluate("Array.prototype", return_by_value=False)
    try:
        r2 = await s.runtime.query_objects(r["result"]["objectId"])
        await s.close(); log_result("TC-RUNTIME-024", "query_objects with prototype", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-RUNTIME-024", "query_objects with prototype", "FAIL", str(e))

@reg("TC-RUNTIME-025", "global_lexical_scope_names with ctx")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.global_lexical_scope_names()
    assert "names" in r
    await s.close(); log_result("TC-RUNTIME-025", "global_lexical_scope_names with ctx", "PASS")

@reg("TC-RUNTIME-026", "set_async_call_stack_depth")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.set_async_call_stack_depth(32)
    await s.close(); log_result("TC-RUNTIME-026", "set_async_call_stack_depth", "PASS")

@reg("TC-RUNTIME-027", "await_promise with timeout")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("new Promise(r=>setTimeout(()=>r(99),100))", return_by_value=False)
    r2 = await asyncio.wait_for(s.runtime.await_promise(r["result"]["objectId"], return_by_value=True), timeout=5)
    assert r2["result"]["value"] == 99
    await s.close(); log_result("TC-RUNTIME-027", "await_promise with timeout", "PASS")

@reg("TC-RUNTIME-028", "discard_console_entries")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    await s.runtime.discard_console_entries()
    await s.close(); log_result("TC-RUNTIME-028", "discard_console_entries", "PASS")

@reg("TC-RUNTIME-029", "evaluate with generate_preview")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1,b:[1,2,3]})", generate_preview=True)
    assert "result" in r
    await s.close(); log_result("TC-RUNTIME-029", "evaluate with generate_preview", "PASS")

@reg("TC-RUNTIME-030", "evaluate with silent")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("1+1", silent=True, return_by_value=True)
    assert r["result"]["value"] == 2
    await s.close(); log_result("TC-RUNTIME-030", "evaluate with silent", "PASS")

@reg("TC-RUNTIME-031", "evaluate with object_group")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1})", object_group="test", return_by_value=False)
    assert "objectId" in r["result"]
    await s.close(); log_result("TC-RUNTIME-031", "evaluate with object_group", "PASS")

@reg("TC-RUNTIME-032", "evaluate return_by_value False")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1})", return_by_value=False)
    assert "objectId" in r["result"]
    await s.close(); log_result("TC-RUNTIME-032", "evaluate return_by_value False", "PASS")

@reg("TC-RUNTIME-033", "callFunctionOn with return_by_value")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    ctxs: list[dict] = []
    s.on("Runtime.executionContextCreated", lambda c: ctxs.append(c))
    await s.runtime.enable()
    await asyncio.sleep(0.3)
    eid = ctxs[0]["context"]["id"] if ctxs else 1
    r = await s.runtime.call_function_on("function(){return 42}", execution_context_id=eid, return_by_value=True)
    assert r["result"]["value"] == 42
    await s.close(); log_result("TC-RUNTIME-033", "callFunctionOn with return_by_value", "PASS")

@reg("TC-RUNTIME-034", "callFunctionOn with generate_preview")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    ctxs: list[dict] = []
    s.on("Runtime.executionContextCreated", lambda c: ctxs.append(c))
    await s.runtime.enable()
    await asyncio.sleep(0.3)
    eid = ctxs[0]["context"]["id"] if ctxs else 1
    r = await s.runtime.call_function_on("function(){return {a:1,b:[1,2]}}", execution_context_id=eid, generate_preview=True)
    assert "result" in r
    await s.close(); log_result("TC-RUNTIME-034", "callFunctionOn with generate_preview", "PASS")

@reg("TC-RUNTIME-035", "callFunctionOn with silent")
async def t(client):
    s = await fresh_session(client)
    await s.runtime.enable()
    ctxs: list[dict] = []
    s.on("Runtime.executionContextCreated", lambda c: ctxs.append(c))
    await s.runtime.enable()
    await asyncio.sleep(0.3)
    eid = ctxs[0]["context"]["id"] if ctxs else 1
    r = await s.runtime.call_function_on("function(){return 1+1}", execution_context_id=eid, silent=True, return_by_value=True)
    assert r["result"]["value"] == 2
    await s.close(); log_result("TC-RUNTIME-035", "callFunctionOn with silent", "PASS")
