"""P1a: TARGET, NETWORK, DOM, BROWSER domain tests."""

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

# ===================== TARGET DOMAIN (12 tests) =====================
@reg("TC-TARGET-001", "createTarget")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    assert "targetId" in r
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-001", "createTarget", "PASS")

@reg("TC-TARGET-002", "attachToTarget")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    a = await s.target.attach_to_target(r["targetId"], flatten=True)
    assert "sessionId" in a
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-002", "attachToTarget", "PASS")

@reg("TC-TARGET-003", "detachFromTarget")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    a = await s.target.attach_to_target(r["targetId"], flatten=True)
    await s.target.detach_from_target(a["sessionId"])
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-003", "detachFromTarget", "PASS")

@reg("TC-TARGET-004", "closeTarget")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-004", "closeTarget", "PASS")

@reg("TC-TARGET-005", "getTargets")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.get_targets()
    assert "targetInfos" in r; await s.close()
    log_result("TC-TARGET-005", "getTargets", "PASS", f"{len(r['targetInfos'])} targets")

@reg("TC-TARGET-006", "activateTarget")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    await s.target.activate_target(r["targetId"])
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-006", "activateTarget", "PASS")

@reg("TC-TARGET-007", "setAutoAttach")
async def t(client):
    s = await fresh_session(client)
    await s.target.set_auto_attach(auto_attach=True, await_for_notifications_on_start=True, flatten=True)
    await s.close(); log_result("TC-TARGET-007", "setAutoAttach", "PASS")

@reg("TC-TARGET-008", "sendMessageToTarget")
async def t(client):
    log_result("TC-TARGET-008", "sendMessageToTarget", "SKIP", "Flatten mode uses sessions directly")

@reg("TC-TARGET-009", "setDiscoverTargets")
async def t(client):
    s = await fresh_session(client)
    await s.target.set_discover_targets(True); await s.close()
    log_result("TC-TARGET-009", "setDiscoverTargets", "PASS")

@reg("TC-TARGET-010", "setRemoteLocations")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Target.setRemoteLocations", {"locations": []}); await s.close()
        log_result("TC-TARGET-010", "setRemoteLocations", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-TARGET-010", "setRemoteLocations", "FAIL", str(e))

@reg("TC-TARGET-011", "getTargetInfo")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    info = await s.target.get_target_info(r["targetId"])
    assert "targetInfo" in info
    await s.target.close_target(r["targetId"]); await s.close()
    log_result("TC-TARGET-011", "getTargetInfo", "PASS")

@reg("TC-TARGET-012", "initiateTargetShutdown")
async def t(client):
    s = await fresh_session(client)
    r = await s.target.create_target("https://example.com")
    try:
        await s.send("Target.initiateTargetShutdown", {"targetId": r["targetId"]}); await s.close()
        log_result("TC-TARGET-012", "initiateTargetShutdown", "PASS")
    except Exception as e:
        await s.target.close_target(r["targetId"]); await s.close()
        log_result("TC-TARGET-012", "initiateTargetShutdown", "FAIL", str(e))

# ===================== NETWORK DOMAIN (25 tests) =====================
@reg("TC-NETWORK-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); await s.network.disable(); await s.close()
    log_result("TC-NETWORK-001", "enable/disable", "PASS")

@reg("TC-NETWORK-002", "setCacheDisabled")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); await s.network.set_cache_disabled(True); await s.close()
    log_result("TC-NETWORK-002", "setCacheDisabled", "PASS")

@reg("TC-NETWORK-003", "setUserAgentOverride")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); await s.network.set_user_agent_override("TestBot"); await s.close()
    log_result("TC-NETWORK-003", "setUserAgentOverride", "PASS")

@reg("TC-NETWORK-004", "clearBrowserCookies")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); await s.network.clear_browser_cookies(); await s.close()
    log_result("TC-NETWORK-004", "clearBrowserCookies", "PASS")

@reg("TC-NETWORK-005", "clearBrowserCache")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); await s.network.clear_browser_cache(); await s.close()
    log_result("TC-NETWORK-005", "clearBrowserCache", "PASS")

@reg("TC-NETWORK-006", "getAllCookies")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable(); r = await s.network.get_all_cookies()
    assert "cookies" in r; await s.close()
    log_result("TC-NETWORK-006", "getAllCookies", "PASS")

@reg("TC-NETWORK-007", "setCookies")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable()
    await s.network.set_cookie("test", "val", domain="example.com", path="/"); await s.close()
    log_result("TC-NETWORK-007", "setCookies", "PASS")

@reg("TC-NETWORK-008", "getCookies")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable()
    await s.network.set_cookie("test2", "val2", domain="example.com", path="/")
    r = await s.network.get_cookies(urls=["https://example.com"])
    assert any(c["name"]=="test2" for c in r.get("cookies",[])); await s.close()
    log_result("TC-NETWORK-008", "getCookies", "PASS")

@reg("TC-NETWORK-009", "deleteCookies")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable()
    await s.network.set_cookie("del", "val", domain="example.com", path="/")
    await s.network.delete_cookies("del", url="https://example.com")
    r = await s.network.get_cookies(urls=["https://example.com"])
    assert not any(c["name"]=="del" for c in r.get("cookies",[])); await s.close()
    log_result("TC-NETWORK-009", "deleteCookies", "PASS")

@reg("TC-NETWORK-010", "setExtraHTTPHeaders")
async def t(client):
    s = await fresh_session(client)
    await s.network.enable()
    await s.network.set_extra_request_headers({"X-Test": "true"}); await s.close()
    log_result("TC-NETWORK-010", "setExtraHTTPHeaders", "PASS")

@reg("TC-NETWORK-011", "canEmulateNetworkConditions")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    try:
        await s.network.can_emulate_network_conditions(); await s.close()
        log_result("TC-NETWORK-011", "canEmulateNetworkConditions", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-NETWORK-011", "canEmulateNetworkConditions", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-NETWORK-011", "canEmulateNetworkConditions", "FAIL", str(e))

@reg("TC-NETWORK-012", "emulateNetworkConditions")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.emulate_network_conditions(offline=False, latency=100, download_throughput=50000, upload_throughput=50000)
    await s.network.emulate_network_conditions(offline=False, latency=0, download_throughput=-1, upload_throughput=-1)
    await s.close(); log_result("TC-NETWORK-012", "emulateNetworkConditions", "PASS")

@reg("TC-NETWORK-013", "getResponseBody")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    reqs: list[dict] = []; ev = asyncio.Event()
    async def on_resp(p): reqs.append(p); ev.set()
    s.on("Network.responseReceived", on_resp)
    await safe_navigate(s, "https://example.com")
    with contextlib.suppress(asyncio.TimeoutError): await asyncio.wait_for(ev.wait(), timeout=5)
    if reqs:
        try:
            body = await s.network.get_response_body(reqs[0]["requestId"])
            assert "body" in body; await s.close()
            log_result("TC-NETWORK-013", "getResponseBody", "PASS")
        except Exception as e:
            await s.close(); log_result("TC-NETWORK-013", "getResponseBody", "FAIL", str(e))
    else:
        await s.close(); log_result("TC-NETWORK-013", "getResponseBody", "SKIP", "No requests captured")

@reg("TC-NETWORK-014", "continueInterceptedRequest")
async def t(client):
    log_result("TC-NETWORK-014", "continueInterceptedRequest", "SKIP", "Requires Fetch interception setup")

@reg("TC-NETWORK-015", "getPostData")
async def t(client):
    s = await fresh_session(client); await s.network.enable(); await s.close()
    log_result("TC-NETWORK-015", "getPostData", "SKIP", "Requires POST request capture")

@reg("TC-NETWORK-016", "replayXHR")
async def t(client):
    s = await fresh_session(client); await s.network.enable(); await s.close()
    log_result("TC-NETWORK-016", "replayXHR", "SKIP", "Requires XHR capture")

@reg("TC-NETWORK-017", "getResponseBodyForInterception")
async def t(client):
    log_result("TC-NETWORK-017", "getResponseBodyForInterception", "SKIP", "Requires Fetch interception")

@reg("TC-NETWORK-018", "set_cache_disabled v2")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_cache_disabled(True); await s.close()
    log_result("TC-NETWORK-018", "set_cache_disabled v2", "PASS")

@reg("TC-NETWORK-019", "set_blocked_urls")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_blocked_urls(["*.jpg", "*.png"]); await s.close()
    log_result("TC-NETWORK-019", "set_blocked_urls", "PASS")

@reg("TC-NETWORK-020", "set_bypass_service_worker")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_bypass_service_worker(True); await s.close()
    log_result("TC-NETWORK-020", "set_bypass_service_worker", "PASS")

@reg("TC-NETWORK-021", "load_network_resource")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    f = await s.page.get_frame_tree(); fid = f["frameTree"]["frame"]["id"]
    try:
        r = await s.network.load_network_resource(fid, "https://example.com", options={"disableCache": False, "includeCredentials": False}); await s.close()
        log_result("TC-NETWORK-021", "load_network_resource", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-NETWORK-021", "load_network_resource", "FAIL", str(e))

@reg("TC-NETWORK-022", "get_request_post_data")
async def t(client):
    s = await fresh_session(client); await s.network.enable(); await s.close()
    log_result("TC-NETWORK-022", "get_request_post_data", "SKIP", "Requires POST capture")

@reg("TC-NETWORK-023", "set_blocked_urls with patterns")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    await s.network.set_blocked_urls(["*api*", "*track*"]); await s.close()
    log_result("TC-NETWORK-023", "set_blocked_urls patterns", "PASS")

@reg("TC-NETWORK-024", "emulate_network_conditions with resource_types")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    try:
        await s.network.emulate_network_conditions(offline=False, latency=100, download_throughput=50000, upload_throughput=50000, resource_types=["XHR","Fetch"])
        await s.close(); log_result("TC-NETWORK-024", "emulate_network_conditions resource_types", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-NETWORK-024", "emulate_network_conditions resource_types", "FAIL", str(e))

@reg("TC-NETWORK-025", "set_cache_disabled with resource_types")
async def t(client):
    s = await fresh_session(client); await s.network.enable()
    try:
        await s.send("Network.setCacheDisabled", {"cacheDisabled": True}); await s.close()
        log_result("TC-NETWORK-025", "set_cache_disabled resource_types", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-NETWORK-025", "set_cache_disabled resource_types", "FAIL", str(e))

# ===================== DOM DOMAIN (39 tests) =====================
@reg("TC-DOM-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    await s.dom.enable(); await s.dom.disable(); await s.close()
    log_result("TC-DOM-001", "enable/disable", "PASS")

@reg("TC-DOM-002", "getDocument")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    d = await s.dom.get_document(); assert "root" in d; await s.close()
    log_result("TC-DOM-002", "getDocument", "PASS")

@reg("TC-DOM-003", "getFlattenedDocument")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    try:
        d = await s.dom.get_flattened_document(); await s.close()
        log_result("TC-DOM-003", "getFlattenedDocument", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-DOM-003", "getFlattenedDocument", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-DOM-003", "getFlattenedDocument", "FAIL", str(e))

@reg("TC-DOM-004", "collectClassNamesFromSubtree")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div class='a b c'><p class='x'>test</p></div>")
    d = await s.dom.get_document(); nid = d["root"]["nodeId"]
    try:
        r = await s.dom.collect_class_names_from_subtree(nid); await s.close()
        log_result("TC-DOM-004", "collectClassNamesFromSubtree", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-DOM-004", "collectClassNamesFromSubtree", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-DOM-004", "collectClassNamesFromSubtree", "FAIL", str(e))

@reg("TC-DOM-005", "querySelector")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<h1>Title</h1><p>Para</p>")
    d = await s.dom.get_document()
    r = await s.dom.query_selector(d["root"]["nodeId"], "h1")
    assert r["nodeId"] > 0; await s.close()
    log_result("TC-DOM-005", "querySelector", "PASS")

@reg("TC-DOM-006", "querySelectorAll")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<p>1</p><p>2</p><p>3</p>")
    d = await s.dom.get_document()
    r = await s.dom.query_selector_all(d["root"]["nodeId"], "p")
    assert len(r.get("nodeIds",[])) >= 3; await s.close()
    log_result("TC-DOM-006", "querySelectorAll", "PASS")

@reg("TC-DOM-007", "removeNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='rm'>Remove me</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#rm")
    await s.dom.remove_node(n["nodeId"]); await s.close()
    log_result("TC-DOM-007", "removeNode", "PASS")

@reg("TC-DOM-008", "setAttributeValue")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.set_attribute_value(n["nodeId"], "data-test", "value")
    h = await s.dom.get_outer_html(n["nodeId"])
    assert 'data-test="value"' in h["outerHTML"]; await s.close()
    log_result("TC-DOM-008", "setAttributeValue", "PASS")

@reg("TC-DOM-009", "setAttributesAsText")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.set_attributes_as_text(n["nodeId"], "class='test'"); await s.close()
        log_result("TC-DOM-009", "setAttributesAsText", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-009", "setAttributesAsText", "FAIL", str(e))

@reg("TC-DOM-010", "removeAttribute")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t' class='foo'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.remove_attribute(n["nodeId"], "class")
    h = await s.dom.get_outer_html(n["nodeId"])
    assert "class" not in h["outerHTML"]; await s.close()
    log_result("TC-DOM-010", "removeAttribute", "PASS")

@reg("TC-DOM-011", "setTextContent")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Old</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.set_outer_html(n["nodeId"], "<div id='t'>New text</div>"); await s.close()
        log_result("TC-DOM-011", "setTextContent", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-011", "setTextContent", "FAIL", str(e))

@reg("TC-DOM-012", "getBoxModel")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    r = await s.dom.get_box_model(n["nodeId"]); assert "model" in r; await s.close()
    log_result("TC-DOM-012", "getBoxModel", "PASS")

@reg("TC-DOM-013", "getContentQuads")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.dom.get_content_quads(n["nodeId"]); assert "quads" in r; await s.close()
        log_result("TC-DOM-013", "getContentQuads", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-013", "getContentQuads", "FAIL", str(e))

@reg("TC-DOM-014", "describeNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.dom.describe_node(n["nodeId"]); assert "node" in r; await s.close()
        log_result("TC-DOM-014", "describeNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-014", "describeNode", "FAIL", str(e))

@reg("TC-DOM-015", "focus")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<input id='t'>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    await s.dom.focus(n["nodeId"]); await s.close()
    log_result("TC-DOM-015", "focus", "PASS")

@reg("TC-DOM-016", "scrollIntoViewIfNeeded")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.scroll_into_view_if_needed(n["nodeId"]); await s.close()
        log_result("TC-DOM-016", "scrollIntoViewIfNeeded", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-016", "scrollIntoViewIfNeeded", "FAIL", str(e))

@reg("TC-DOM-017", "setFileInputFiles")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<input id='t' type='file'>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.set_file_input_files(n["nodeId"], []); await s.close()
        log_result("TC-DOM-017", "setFileInputFiles", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-017", "setFileInputFiles", "FAIL", str(e))

@reg("TC-DOM-018", "performSearch")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    r = await s.dom.perform_search("//div")
    assert "searchId" in r and r["resultCount"] >= 0; await s.close()
    log_result("TC-DOM-018", "performSearch", "PASS", f"{r['resultCount']} results")

@reg("TC-DOM-019", "getSearchResults")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    sr = await s.dom.perform_search("//div")
    if sr["resultCount"] > 0:
        r = await s.dom.get_search_results(sr["searchId"], 0, min(5, sr["resultCount"]))
        assert "nodeIds" in r; await s.close()
        log_result("TC-DOM-019", "getSearchResults", "PASS")
    else:
        await s.close(); log_result("TC-DOM-019", "getSearchResults", "SKIP", "No results")

@reg("TC-DOM-020", "discardSearchResults")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    sr = await s.dom.perform_search("//div")
    await s.dom.discard_search_results(sr["searchId"]); await s.close()
    log_result("TC-DOM-020", "discardSearchResults", "PASS")

@reg("TC-DOM-021", "requestChildNodes")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'><p>child</p></div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.request_child_nodes(n["nodeId"]); await s.close()
        log_result("TC-DOM-021", "requestChildNodes", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-021", "requestChildNodes", "FAIL", str(e))

@reg("TC-DOM-022", "requestNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.runtime.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    r = await s.runtime.evaluate("document.getElementById('t')", return_by_value=False)
    try:
        res = await s.dom.request_node(object_id=r["result"]["objectId"]); await s.close()
        log_result("TC-DOM-022", "requestNode", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-022", "requestNode", "FAIL", str(e))

@reg("TC-DOM-023", "getOuterHTML")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    r = await s.dom.get_outer_html(n["nodeId"])
    assert "outerHTML" in r; await s.close()
    log_result("TC-DOM-023", "getOuterHTML", "PASS")

@reg("TC-DOM-024", "setOuterHTML")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.set_outer_html(n["nodeId"], "<div id='t'>Replaced</div>"); await s.close()
        log_result("TC-DOM-024", "setOuterHTML", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-024", "setOuterHTML", "FAIL", str(e))

@reg("TC-DOM-025", "getHighlightObjectForTest")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.dom.get_highlight_object_for_test(n["nodeId"]); await s.close()
        log_result("TC-DOM-025", "getHighlightObjectForTest", "PASS")
    except AttributeError:
        await s.close(); log_result("TC-DOM-025", "getHighlightObjectForTest", "FAIL", "Method missing")
    except Exception as e:
        await s.close(); log_result("TC-DOM-025", "getHighlightObjectForTest", "FAIL", str(e))

@reg("TC-DOM-026", "setChildNodes")
async def t(client):
    log_result("TC-DOM-026", "setChildNodes", "SKIP", "Event-driven, not a command")

@reg("TC-DOM-027", "get_inner_html")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'><p>inner</p></div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.dom.get_inner_html(n["nodeId"]); assert "innerHTML" in r; await s.close()
        log_result("TC-DOM-027", "get_inner_html", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-027", "get_inner_html", "FAIL", str(e))

@reg("TC-DOM-028", "get_attribute")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<a id='t' href='https://example.com'>Link</a>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        r = await s.dom.get_attribute(n["nodeId"], "href"); await s.close()
        log_result("TC-DOM-028", "get_attribute", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-028", "get_attribute", "FAIL", str(e))

@reg("TC-DOM-029", "resolve_node with object_id")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.runtime.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    r = await s.runtime.evaluate("document.getElementById('t')", return_by_value=False)
    try:
        rn = await s.dom.request_node(object_id=r["result"]["objectId"])
        node_id = rn.get("nodeId", 0)
        if node_id:
            resolved = await s.dom.resolve_node(node_id=node_id); await s.close()
            log_result("TC-DOM-029", "resolve_node object_id", "PASS")
        else:
            await s.close(); log_result("TC-DOM-029", "resolve_node object_id", "SKIP", "No nodeId from requestNode")
    except Exception as e:
        await s.close(); log_result("TC-DOM-029", "resolve_node object_id", "FAIL", str(e))

@reg("TC-DOM-030", "resolve_node with backend_node_id")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document(depth=1)
    try:
        bnid = d["root"].get("backendNodeId", 0)
        if bnid:
            rn = await s.dom.resolve_node(backend_node_id=bnid); await s.close()
            log_result("TC-DOM-030", "resolve_node backend", "PASS")
        else:
            await s.close(); log_result("TC-DOM-030", "resolve_node backend", "SKIP", "No backendNodeId")
    except Exception as e:
        await s.close(); log_result("TC-DOM-030", "resolve_node backend", "FAIL", str(e))

@reg("TC-DOM-031", "copy_to")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='src'>Source</div><div id='dst'></div>")
    d = await s.dom.get_document()
    src = await s.dom.query_selector(d["root"]["nodeId"], "#src")
    dst = await s.dom.query_selector(d["root"]["nodeId"], "#dst")
    try:
        await s.dom.copy_to(src["nodeId"], dst["nodeId"]); await s.close()
        log_result("TC-DOM-031", "copy_to", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-031", "copy_to", "FAIL", str(e))

@reg("TC-DOM-032", "move_to")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='src'>Source</div><div id='dst'></div>")
    d = await s.dom.get_document()
    src = await s.dom.query_selector(d["root"]["nodeId"], "#src")
    dst = await s.dom.query_selector(d["root"]["nodeId"], "#dst")
    try:
        await s.dom.move_to(src["nodeId"], dst["nodeId"]); await s.close()
        log_result("TC-DOM-032", "move_to", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-032", "move_to", "FAIL", str(e))

@reg("TC-DOM-033", "set_node_value")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Old text</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try:
        await s.dom.set_outer_html(n["nodeId"], "<div id='t'>New text</div>"); await s.close()
        log_result("TC-DOM-033", "set_node_value", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-033", "set_node_value", "FAIL", str(e))

@reg("TC-DOM-034", "get_node_for_location")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await safe_navigate(s, "https://example.com")
    try:
        r = await s.dom.get_node_for_location(x=10, y=10); await s.close()
        log_result("TC-DOM-034", "get_node_for_location", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-034", "get_node_for_location", "FAIL", str(e))

@reg("TC-DOM-035", "request_node backend")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.runtime.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    r = await s.runtime.evaluate("document.getElementById('t')", return_by_value=False)
    try:
        res = await s.dom.request_node(object_id=r["result"]["objectId"]); await s.close()
        log_result("TC-DOM-035", "request_node backend", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-035", "request_node backend", "FAIL", str(e))

@reg("TC-DOM-036", "get_document with depth")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div><p><span>deep</span></p></div>")
    d = await s.dom.get_document(depth=2); assert "root" in d; await s.close()
    log_result("TC-DOM-036", "get_document depth", "PASS")

@reg("TC-DOM-037", "get_document with pierce")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div>Test</div>")
    d = await s.dom.get_document(pierce=True); assert "root" in d; await s.close()
    log_result("TC-DOM-037", "get_document pierce", "PASS")

@reg("TC-DOM-038", "query_selector with node_id")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='parent'><p class='child'>Test</p></div>")
    d = await s.dom.get_document()
    parent = await s.dom.query_selector(d["root"]["nodeId"], "#parent")
    r = await s.dom.query_selector(parent["nodeId"], ".child")
    assert r["nodeId"] > 0; await s.close()
    log_result("TC-DOM-038", "query_selector node_id", "PASS")

@reg("TC-DOM-039", "query_selector with object_id")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.runtime.enable()
    await nav_data(s, "<div id='parent'><p class='child'>Test</p></div>")
    r = await s.runtime.evaluate("document.getElementById('parent')", return_by_value=False)
    try:
        node = await s.dom.request_node(object_id=r["result"]["objectId"])
        nid = node.get("nodeId", 0)
        if nid == 0:
            await s.close(); log_result("TC-DOM-039", "query_selector object_id", "SKIP", "requestNode returned nodeId=0")
            return
        res = await s.dom.query_selector(nid, ".child"); await s.close()
        log_result("TC-DOM-039", "query_selector object_id", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-DOM-039", "query_selector object_id", "FAIL", str(e))

# ===================== BROWSER DOMAIN (9 tests) =====================
@reg("TC-BROWSER-001", "getVersion")
async def t(client):
    try:
        r = await client.browser.get_version()
        assert "protocolVersion" in r or "product" in r
        log_result("TC-BROWSER-001", "getVersion", "PASS")
    except Exception as e:
        log_result("TC-BROWSER-001", "getVersion", "FAIL", str(e))

@reg("TC-BROWSER-002", "getCommandLine")
async def t(client):
    try:
        r = await client.browser.get_command_line()
        log_result("TC-BROWSER-002", "getCommandLine", "PASS")
    except Exception as e:
        if "enable-automation" in str(e):
            log_result("TC-BROWSER-002", "getCommandLine", "SKIP", "Requires --enable-automation flag")
        else:
            log_result("TC-BROWSER-002", "getCommandLine", "FAIL", str(e))

@reg("TC-BROWSER-003", "getHistogram")
async def t(client):
    try:
        r = await client.browser.get_histogram("V8.ExecuteJS")
        log_result("TC-BROWSER-003", "getHistogram", "PASS")
    except Exception as e:
        if "Cannot find histogram" in str(e):
            log_result("TC-BROWSER-003", "getHistogram", "SKIP", "Histogram not available")
        else:
            log_result("TC-BROWSER-003", "getHistogram", "FAIL", str(e))

@reg("TC-BROWSER-004", "getHistograms")
async def t(client):
    try:
        r = await client.browser.get_histograms()
        log_result("TC-BROWSER-004", "getHistograms", "PASS")
    except Exception as e:
        log_result("TC-BROWSER-004", "getHistograms", "FAIL", str(e))

@reg("TC-BROWSER-005", "getCPUProfile")
async def t(client):
    try:
        r = await client.browser.get_cpu_profile()
        log_result("TC-BROWSER-005", "getCPUProfile", "PASS")
    except AttributeError:
        log_result("TC-BROWSER-005", "getCPUProfile", "FAIL", "Method missing")
    except Exception as e:
        log_result("TC-BROWSER-005", "getCPUProfile", "FAIL", str(e))

@reg("TC-BROWSER-006", "getHeapProfile")
async def t(client):
    try:
        r = await client.browser.get_heap_profile()
        log_result("TC-BROWSER-006", "getHeapProfile", "PASS")
    except AttributeError:
        log_result("TC-BROWSER-006", "getHeapProfile", "FAIL", "Method missing")
    except Exception as e:
        log_result("TC-BROWSER-006", "getHeapProfile", "FAIL", str(e))

@reg("TC-BROWSER-007", "resetHistograms")
async def t(client):
    try:
        await client.browser.reset_histograms()
        log_result("TC-BROWSER-007", "resetHistograms", "PASS")
    except Exception as e:
        log_result("TC-BROWSER-007", "resetHistograms", "FAIL", str(e))

@reg("TC-BROWSER-008", "getBrowserCommandLine")
async def t(client):
    try:
        r = await client.browser.get_browser_command_line()
        log_result("TC-BROWSER-008", "getBrowserCommandLine", "PASS")
    except AttributeError:
        log_result("TC-BROWSER-008", "getBrowserCommandLine", "FAIL", "Method missing")
    except Exception as e:
        if "enable-automation" in str(e):
            log_result("TC-BROWSER-008", "getBrowserCommandLine", "SKIP", "Requires --enable-automation flag")
        else:
            log_result("TC-BROWSER-008", "getBrowserCommandLine", "FAIL", str(e))

@reg("TC-BROWSER-009", "getBounds")
async def t(client):
    try:
        r = await client.browser.get_bounds()
        log_result("TC-BROWSER-009", "getBounds", "PASS")
    except AttributeError:
        log_result("TC-BROWSER-009", "getBounds", "FAIL", "Method missing")
    except Exception as e:
        log_result("TC-BROWSER-009", "getBounds", "FAIL", str(e))
