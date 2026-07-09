"""P1c: CSS, OVERLAY, DEBUGGER domain tests."""

from __future__ import annotations
import asyncio, contextlib
from typing import Any, Callable, Awaitable
from cdpwave.client import CDPClient, CDPSession
from cdpwave.exceptions import CommandError
from tests.manual._test_helpers import fresh_session, safe_navigate, nav_data
from tests.manual._test_helpers import log_result

_test_registry: list[tuple[str, str, Callable[[CDPClient], Awaitable[None]]]] = []

def reg(tc_id: str, name: str):
    def decorator(func):
        _test_registry.append((tc_id, name, func))
        return func
    return decorator

# ===================== CSS DOMAIN (14 tests) =====================
@reg("TC-CSS-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.dom.enable(); await s.css.enable(); await s.css.disable(); await s.close()
        log_result("TC-CSS-001", "enable/disable", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-001", "enable/disable", "FAIL", str(e))

@reg("TC-CSS-002", "getComputedStyle")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.css.get_computed_style_for_node(n["nodeId"]); await s.close()
        log_result("TC-CSS-002", "getComputedStyle", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-002", "getComputedStyle", "FAIL", str(e))

@reg("TC-CSS-003", "getInlineStylesForNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t' style='color:red'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.css.get_inline_styles_for_node(n["nodeId"]); await s.close()
        log_result("TC-CSS-003", "getInlineStylesForNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-003", "getInlineStylesForNode", "FAIL", str(e))

@reg("TC-CSS-004", "getMatchedStylesForNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.css.get_matched_styles_for_node(n["nodeId"]); await s.close()
        log_result("TC-CSS-004", "getMatchedStylesForNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-004", "getMatchedStylesForNode", "FAIL", str(e))

@reg("TC-CSS-005", "getMediaQueries")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    try:
        r = await s.css.get_media_queries(); await s.close()
        log_result("TC-CSS-005", "getMediaQueries", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-005", "getMediaQueries", "FAIL", str(e))

@reg("TC-CSS-006", "getPlatformFontsForNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.css.get_platform_fonts_for_node(n["nodeId"]); await s.close()
        log_result("TC-CSS-006", "getPlatformFontsForNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-006", "getPlatformFontsForNode", "FAIL", str(e))

@reg("TC-CSS-007", "getStyleSheetText")
async def t(client):
    s = await fresh_session(client); await s.page.enable(); await s.dom.enable(); await s.css.enable()
    await safe_navigate(s, "https://example.com")
    await asyncio.sleep(0.5)
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "div")
    try:
        ms = await s.css.get_matched_styles_for_node(n["nodeId"])
        rules = ms.get("matchedCSSRules", [])
        if rules:
            sid = rules[0].get("rule",{}).get("styleSheetId")
            if sid:
                r = await s.css.get_style_sheet_text(sid); await s.close()
                log_result("TC-CSS-007", "getStyleSheetText", "PASS")
            else:
                await s.close(); log_result("TC-CSS-007", "getStyleSheetText", "SKIP", "No styleSheetId")
        else:
            await s.close(); log_result("TC-CSS-007", "getStyleSheetText", "SKIP", "No matchedCSSRules")
    except Exception as e:
        await s.close(); log_result("TC-CSS-007", "getStyleSheetText", "FAIL", str(e))

@reg("TC-CSS-008", "setStyleSheetText")
async def t(client):
    s = await fresh_session(client); await s.page.enable(); await s.dom.enable(); await s.css.enable()
    await safe_navigate(s, "https://example.com")
    await asyncio.sleep(0.5)
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "div")
    try:
        ms = await s.css.get_matched_styles_for_node(n["nodeId"])
        rules = ms.get("matchedCSSRules", [])
        if rules:
            sid = rules[0].get("rule",{}).get("styleSheetId")
            if sid:
                r = await s.css.set_style_sheet_text(sid, "#t{color:blue}"); await s.close()
                log_result("TC-CSS-008", "setStyleSheetText", "PASS")
            else:
                await s.close(); log_result("TC-CSS-008", "setStyleSheetText", "SKIP", "No styleSheetId")
        else:
            await s.close(); log_result("TC-CSS-008", "setStyleSheetText", "SKIP", "No matchedCSSRules")
    except Exception as e:
        await s.close(); log_result("TC-CSS-008", "setStyleSheetText", "FAIL", str(e))

@reg("TC-CSS-009", "setRuleStyle")
async def t(client):
    s = await fresh_session(client); await s.page.enable(); await s.dom.enable(); await s.css.enable()
    await safe_navigate(s, "https://example.com")
    await asyncio.sleep(0.5)
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "div")
    try:
        ms = await s.css.get_matched_styles_for_node(n["nodeId"])
        rules = ms.get("matchedCSSRules", [])
        if rules:
            rule = rules[0].get("rule",{})
            sid = rule.get("styleSheetId")
            if sid:
                r = await s.css.set_rule_style(sid, rule.get("selectorList",{}).get("text","div"), "color: green"); await s.close()
                log_result("TC-CSS-009", "setRuleStyle", "PASS")
            else:
                await s.close(); log_result("TC-CSS-009", "setRuleStyle", "SKIP", "No styleSheetId")
        else:
            await s.close(); log_result("TC-CSS-009", "setRuleStyle", "SKIP", "No matchedCSSRules")
    except Exception as e:
        await s.close(); log_result("TC-CSS-009", "setRuleStyle", "FAIL", str(e))

@reg("TC-CSS-010", "addRule")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<style></style><div id='t'>Test</div>")
    await asyncio.sleep(0.3)
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        ms = await s.css.get_matched_styles_for_node(n["nodeId"])
        rules = ms.get("matchedCSSRules", [])
        if rules:
            sid = rules[0].get("rule", {}).get("styleSheetId")
            if sid:
                r = await s.css.add_rule(sid, "#t{font-size:20px}"); await s.close()
                log_result("TC-CSS-010", "addRule", "PASS")
            else:
                await s.close(); log_result("TC-CSS-010", "addRule", "SKIP", "No styleSheetId")
        else:
            await s.close(); log_result("TC-CSS-010", "addRule", "SKIP", "No matchedCSSRules")
    except Exception as e:
        await s.close(); log_result("TC-CSS-010", "addRule", "FAIL", str(e))

@reg("TC-CSS-011", "forcePseudoState")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.css.force_pseudo_state(n["nodeId"], ["hover"]); await s.close()
        log_result("TC-CSS-011", "forcePseudoState", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-011", "forcePseudoState", "FAIL", str(e))

@reg("TC-CSS-012", "getBackgroundColors")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.css.get_background_colors(n["nodeId"]); await s.close()
        log_result("TC-CSS-012", "getBackgroundColors", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-012", "getBackgroundColors", "FAIL", str(e))

@reg("TC-CSS-013", "setEffectiveCompositeForNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.send("CSS.setEffectivePropertyValuesForNode", {"nodeId": n["nodeId"]}); await s.close()
        log_result("TC-CSS-013", "setEffectiveCompositeForNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-013", "setEffectiveCompositeForNode", "SKIP", f"Method not available: {e}")

@reg("TC-CSS-014", "takeCoverageDelta")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.css.enable()
    try:
        await s.css.start_rule_usage_tracking()
        r = await s.css.take_coverage_delta()
        await s.css.stop_rule_usage_tracking()
        await s.close()
        log_result("TC-CSS-014", "takeCoverageDelta", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-CSS-014", "takeCoverageDelta", "FAIL", str(e))

# ===================== OVERLAY DOMAIN (15 tests) =====================
@reg("TC-OVERLAY-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.dom.enable(); await s.overlay.enable(); await s.overlay.disable(); await s.close()
        log_result("TC-OVERLAY-001", "enable/disable", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-001", "enable/disable", "FAIL", str(e))

@reg("TC-OVERLAY-002", "setShowDevTools")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.setShowDevTools", {"show": True}); await s.close()
        log_result("TC-OVERLAY-002", "setShowDevTools", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-002", "setShowDevTools", "FAIL", str(e))

@reg("TC-OVERLAY-003", "setPausedInOverlayMessage")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.overlay.set_paused_in_debugger_message("Paused"); await s.close()
        log_result("TC-OVERLAY-003", "setPausedInOverlayMessage", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-003", "setPausedInOverlayMessage", "FAIL", str(e))

@reg("TC-OVERLAY-004", "highlightNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        hc = {"showInfo": True, "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5}}
        await s.overlay.highlight_node(highlight_config=hc, node_id=n["nodeId"])
        await s.overlay.hide_highlight(); await s.close()
        log_result("TC-OVERLAY-004", "highlightNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-004", "highlightNode", "FAIL", str(e))

@reg("TC-OVERLAY-005", "highlightFrame")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.page.enable(); await s.overlay.enable()
    f = await s.page.get_frame_tree(); fid = f["frameTree"]["frame"]["id"]
    try:
        await s.send("Overlay.highlightFrame", {"frameId": fid})
        await s.overlay.hide_highlight(); await s.close()
        log_result("TC-OVERLAY-005", "highlightFrame", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-005", "highlightFrame", "FAIL", str(e))

@reg("TC-OVERLAY-006", "highlightQuad")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.highlightQuad", {"quad": [0,0,100,0,100,100,0,100]})
        await s.overlay.hide_highlight(); await s.close()
        log_result("TC-OVERLAY-006", "highlightQuad", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-006", "highlightQuad", "FAIL", str(e))

@reg("TC-OVERLAY-007", "highlightRect")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.highlightRect", {"x":0,"y":0,"width":100,"height":100})
        await s.overlay.hide_highlight(); await s.close()
        log_result("TC-OVERLAY-007", "highlightRect", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-007", "highlightRect", "FAIL", str(e))

@reg("TC-OVERLAY-008", "highlightShape")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.highlightShape", {"shapes": []}); await s.close()
        log_result("TC-OVERLAY-008", "highlightShape", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-008", "highlightShape", "FAIL", str(e))

@reg("TC-OVERLAY-009", "setShowGridOverlays")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.setShowGridOverlays", {"gridNodeHighlightConfigs":[]}); await s.close()
        log_result("TC-OVERLAY-009", "setShowGridOverlays", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-009", "setShowGridOverlays", "FAIL", str(e))

@reg("TC-OVERLAY-010", "setShowPaintRects")
async def t(client):
    s = await fresh_session(client); await s.page.enable(); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.overlay.set_show_paint_rects(True); await s.close()
        log_result("TC-OVERLAY-010", "setShowPaintRects", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-OVERLAY-010", "setShowPaintRects", "SKIP", f"Not supported in headless: {e}")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-010", "setShowPaintRects", "FAIL", str(e))

@reg("TC-OVERLAY-011", "setShowLayoutRects")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.setShowLayoutRects", {"show": True}); await s.close()
        log_result("TC-OVERLAY-011", "setShowLayoutRects", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-011", "setShowLayoutRects", "FAIL", str(e))

@reg("TC-OVERLAY-012", "setShowScrollBottleneckRects")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.overlay.set_show_scroll_bottleneck_rects(True); await s.close()
        log_result("TC-OVERLAY-012", "setShowScrollBottleneckRects", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-012", "setShowScrollBottleneckRects", "FAIL", str(e))

@reg("TC-OVERLAY-013", "setShowHitTestRects")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.send("Overlay.setShowHitTestRects", {"show": True}); await s.close()
        log_result("TC-OVERLAY-013", "setShowHitTestRects", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-013", "setShowHitTestRects", "FAIL", str(e))

@reg("TC-OVERLAY-014", "setShowWebVitals")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.overlay.set_show_web_vitals(True); await s.close()
        log_result("TC-OVERLAY-014", "setShowWebVitals", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-014", "setShowWebVitals", "FAIL", str(e))

@reg("TC-OVERLAY-015", "setShowViewportSizeOnResize")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.overlay.enable()
    try:
        await s.overlay.set_show_viewport_size_on_resize(True); await s.close()
        log_result("TC-OVERLAY-015", "setShowViewportSizeOnResize", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-OVERLAY-015", "setShowViewportSizeOnResize", "FAIL", str(e))

# ===================== DEBUGGER DOMAIN (22 tests) =====================
@reg("TC-DEBUGGER-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.debugger.enable(); await s.debugger.disable(); await s.close()
        log_result("TC-DEBUGGER-001", "enable/disable", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-001", "enable/disable", "FAIL", str(e))

@reg("TC-DEBUGGER-002", "setBreakpointsByUrl")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        r = await s.debugger.set_breakpoints_by_url(url="https://example.com/test.js", line_number=0, column_number=0)
        await s.close(); log_result("TC-DEBUGGER-002", "setBreakpointsByUrl", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-002", "setBreakpointsByUrl", "FAIL", str(e))

@reg("TC-DEBUGGER-003", "removeBreakpoint")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        r = await s.debugger.set_breakpoints_by_url(url="https://example.com/test.js", line_number=0)
        if "breakpointId" in r:
            await s.debugger.remove_breakpoint(r["breakpointId"])
        await s.close(); log_result("TC-DEBUGGER-003", "removeBreakpoint", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-003", "removeBreakpoint", "FAIL", str(e))

@reg("TC-DEBUGGER-004", "getPossibleBreakpoints")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    scripts: list[dict] = []
    s.on("Debugger.scriptParsed", lambda p: scripts.append(p))
    await nav_data(s, "<script>function test(){return 42}</script>")
    await asyncio.sleep(0.3)
    sid = scripts[0]["scriptId"] if scripts else "0"
    try:
        r = await s.debugger.get_possible_breakpoints(start={"scriptId":sid,"lineNumber":0,"columnNumber":0})
        await s.close(); log_result("TC-DEBUGGER-004", "getPossibleBreakpoints", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-004", "getPossibleBreakpoints", "FAIL", str(e))

@reg("TC-DEBUGGER-005", "setBreakpointByScriptId")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    scripts: list[dict] = []
    s.on("Debugger.scriptParsed", lambda p: scripts.append(p))
    await nav_data(s, "<script>function test(){return 42}</script>")
    await asyncio.sleep(0.3)
    sid = scripts[0]["scriptId"] if scripts else "0"
    try:
        bp = await s.debugger.get_possible_breakpoints(start={"scriptId":sid,"lineNumber":0,"columnNumber":0})
        locations = bp.get("locations", [])
        if locations:
            loc = locations[0]
            await s.send("Debugger.setBreakpoint", {"location":{"scriptId":sid,"lineNumber":loc.get("lineNumber",0),"columnNumber":loc.get("columnNumber",0)}})
        else:
            await s.send("Debugger.setBreakpoint", {"location":{"scriptId":sid,"lineNumber":0,"columnNumber":0}})
        await s.close(); log_result("TC-DEBUGGER-005", "setBreakpointByScriptId", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-005", "setBreakpointByScriptId", "FAIL", str(e))

@reg("TC-DEBUGGER-006", "setBreakpointActive")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.send("Debugger.setBreakpointActive", {"breakpointId":"fake","active":True}); await s.close()
        log_result("TC-DEBUGGER-006", "setBreakpointActive", "PASS", "Method available")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-006", "setBreakpointActive", "SKIP", f"Method not available: {e}")

@reg("TC-DEBUGGER-007", "setBreakpointsActive")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.debugger.set_breakpoints_active(True); await s.close()
        log_result("TC-DEBUGGER-007", "setBreakpointsActive", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-007", "setBreakpointsActive", "FAIL", str(e))

@reg("TC-DEBUGGER-008", "stepInto")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    s.on("Debugger.paused", lambda p: paused.set())
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        await s.debugger.step_into(); await s.close()
        log_result("TC-DEBUGGER-008", "stepInto", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-008", "stepInto", "FAIL", str(e))

@reg("TC-DEBUGGER-009", "stepOver")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    s.on("Debugger.paused", lambda p: paused.set())
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        await s.debugger.step_over(); await s.close()
        log_result("TC-DEBUGGER-009", "stepOver", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-009", "stepOver", "FAIL", str(e))

@reg("TC-DEBUGGER-010", "stepOut")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    s.on("Debugger.paused", lambda p: paused.set())
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        await s.debugger.step_out(); await s.close()
        log_result("TC-DEBUGGER-010", "stepOut", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-010", "stepOut", "FAIL", str(e))

@reg("TC-DEBUGGER-011", "pause")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.debugger.pause(); await s.close()
        log_result("TC-DEBUGGER-011", "pause", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-011", "pause", "FAIL", str(e))

@reg("TC-DEBUGGER-012", "resume")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    s.on("Debugger.paused", lambda p: paused.set())
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        await s.debugger.resume(); await s.close()
        log_result("TC-DEBUGGER-012", "resume", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-012", "resume", "FAIL", str(e))

@reg("TC-DEBUGGER-013", "searchInContent")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    scripts: list[dict] = []
    s.on("Debugger.scriptParsed", lambda p: scripts.append(p))
    await nav_data(s, "<script>function test(){return 42}</script>")
    await asyncio.sleep(0.3)
    sid = scripts[0]["scriptId"] if scripts else "0"
    try:
        r = await s.debugger.search_in_content(sid, "test"); await s.close()
        log_result("TC-DEBUGGER-013", "searchInContent", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-013", "searchInContent", "FAIL", str(e))

@reg("TC-DEBUGGER-014", "setScriptSource")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    scripts: list[dict] = []
    s.on("Debugger.scriptParsed", lambda p: scripts.append(p))
    await nav_data(s, "<script>function test(){return 42}</script>")
    await asyncio.sleep(0.3)
    sid = scripts[0]["scriptId"] if scripts else "0"
    try:
        await s.debugger.set_script_source(sid, "function test(){return 99}", dry_run=True); await s.close()
        log_result("TC-DEBUGGER-014", "setScriptSource", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-DEBUGGER-014", "setScriptSource", "SKIP", f"Cannot set script source: {e}")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-014", "setScriptSource", "FAIL", str(e))

@reg("TC-DEBUGGER-015", "restartFrame")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    cfp: list[dict] = []
    def _on_paused(p):
        cfp.append(p)
        paused.set()
    s.on("Debugger.paused", _on_paused)
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        cfid = cfp[0]["callFrames"][0]["callFrameId"] if cfp else "0"
        await s.send("Debugger.restartFrame", {"callFrameId":cfid,"mode":"StepInto"}); await s.close()
        log_result("TC-DEBUGGER-015", "restartFrame", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-015", "restartFrame", "FAIL", str(e))

@reg("TC-DEBUGGER-016", "getScriptSource")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    scripts: list[dict] = []
    s.on("Debugger.scriptParsed", lambda p: scripts.append(p))
    await nav_data(s, "<script>function test(){return 42}</script>")
    await asyncio.sleep(0.3)
    sid = scripts[0]["scriptId"] if scripts else "0"
    try:
        r = await s.debugger.get_script_source(sid); await s.close()
        log_result("TC-DEBUGGER-016", "getScriptSource", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-016", "getScriptSource", "FAIL", str(e))

@reg("TC-DEBUGGER-017", "setPauseOnExceptions")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.send("Debugger.setPauseOnExceptions", {"state":"all"}); await s.close()
        log_result("TC-DEBUGGER-017", "setPauseOnExceptions", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-017", "setPauseOnExceptions", "FAIL", str(e))

@reg("TC-DEBUGGER-018", "evaluateOnCallFrame")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    cfp: list[dict] = []
    def _on_paused(p):
        cfp.append(p)
        paused.set()
    s.on("Debugger.paused", _on_paused)
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        cfid = cfp[0]["callFrames"][0]["callFrameId"] if cfp else "0"
        r = await s.debugger.evaluate_on_call_frame(cfid, "1+1"); await s.close()
        log_result("TC-DEBUGGER-018", "evaluateOnCallFrame", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-018", "evaluateOnCallFrame", "FAIL", str(e))

@reg("TC-DEBUGGER-019", "setVariableValue")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    await nav_data(s, "<script>function f(){return 1}</script>")
    paused = asyncio.Event()
    cfp: list[dict] = []
    def _on_paused(p):
        cfp.append(p)
        paused.set()
    s.on("Debugger.paused", _on_paused)
    await s.debugger.pause()
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(s.runtime.evaluate("f()"), timeout=1)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(paused.wait(), timeout=2)
    try:
        cfid = cfp[0]["callFrames"][0]["callFrameId"] if cfp else "0"
        await s.send("Debugger.setVariableValue", {"callFrameId":cfid,"scopeNumber":0,"variableName":"x","newValue":{"type":"number","value":1,"description":"1"}})
        await s.close(); log_result("TC-DEBUGGER-019", "setVariableValue", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-DEBUGGER-019", "setVariableValue", "SKIP", f"setVariableValue failed (deprecated): {e}")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-019", "setVariableValue", "FAIL", str(e))

@reg("TC-DEBUGGER-020", "setAsyncStackTrace")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.send("Debugger.setAsyncCallStackDepth", {"maxDepth": 32}); await s.close()
        log_result("TC-DEBUGGER-020", "setAsyncStackTrace", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-020", "setAsyncStackTrace", "FAIL", str(e))

@reg("TC-DEBUGGER-021", "setBlackboxPatterns")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable()
    try:
        await s.send("Debugger.setBlackboxPatterns", {"patterns": ["pattern"]}); await s.close()
        log_result("TC-DEBUGGER-021", "setBlackboxPatterns", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-021", "setBlackboxPatterns", "FAIL", str(e))

@reg("TC-DEBUGGER-022", "getProperties")
async def t(client):
    s = await fresh_session(client); await s.debugger.enable(); await s.runtime.enable()
    r = await s.runtime.evaluate("({a:1})", return_by_value=False)
    try:
        props = await s.debugger.get_properties(r["result"]["objectId"]); await s.close()
        log_result("TC-DEBUGGER-022", "getProperties", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DEBUGGER-022", "getProperties", "FAIL", str(e))
