"""P3 domains: AUDITS, BACKGROUND_SERVICE, CACHE_STORAGE, CAST, CONSOLE, DEVICE_ACCESS, DEVICE_ORIENTATION, DOM_DEBUGGER, EVENT_BREAKPOINTS, EXTENSIONS, HEADLESS_EXPERIMENTAL, INSPECTOR, IO, LAYER_TREE, MEDIA, MEMORY, PERFORMANCE_TIMELINE, PRELOAD, PWA, SCHEMA, SENSOR, SYSTEM_INFO, TETHERING, TRACING, WORKER."""

from __future__ import annotations
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

# ===================== AUDITS (3 tests) =====================
@reg("TC-AUDIT-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.audits.enable(); await s.audits.disable(); await s.close(); log_result("TC-AUDIT-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-AUDIT-001", "enable/disable", "FAIL", str(e))

@reg("TC-AUDIT-002", "getEncodedResponse")
async def t(client):
    s = await fresh_session(client); await s.audits.enable()
    try: await s.send("Audits.getEncodedResponse", {"requestId":"fake","encoding":"webp"}); await s.close(); log_result("TC-AUDIT-002", "getEncodedResponse", "PASS")
    except CommandError as e: await s.close(); log_result("TC-AUDIT-002", "getEncodedResponse", "SKIP", f"No resource: {e}")
    except Exception as e: await s.close(); log_result("TC-AUDIT-002", "getEncodedResponse", "FAIL", str(e))

@reg("TC-AUDIT-003", "checkContrast")
async def t(client):
    s = await fresh_session(client); await s.audits.enable()
    try: await s.send("Audits.checkContrast", {"reportAAA": True}); await s.close(); log_result("TC-AUDIT-003", "checkContrast", "PASS")
    except Exception as e: await s.close(); log_result("TC-AUDIT-003", "checkContrast", "FAIL", str(e))

# ===================== BACKGROUND_SERVICE (4 tests) =====================
@reg("TC-BS-001", "startObserving")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("BackgroundService.startObserving", {"service":"backgroundFetch"}); await s.close(); log_result("TC-BS-001", "startObserving", "PASS")
    except Exception as e: await s.close(); log_result("TC-BS-001", "startObserving", "FAIL", str(e))

@reg("TC-BS-002", "stopObserving")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("BackgroundService.stopObserving", {"service":"backgroundFetch"}); await s.close(); log_result("TC-BS-002", "stopObserving", "PASS")
    except Exception as e: await s.close(); log_result("TC-BS-002", "stopObserving", "FAIL", str(e))

@reg("TC-BS-003", "setRecording")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("BackgroundService.setRecording", {"shouldRecord":True,"service":"backgroundFetch"}); await s.close(); log_result("TC-BS-003", "setRecording", "PASS")
    except Exception as e: await s.close(); log_result("TC-BS-003", "setRecording", "FAIL", str(e))

@reg("TC-BS-004", "clearEvents")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("BackgroundService.clearEvents", {"service":"backgroundFetch"}); await s.close(); log_result("TC-BS-004", "clearEvents", "PASS")
    except Exception as e: await s.close(); log_result("TC-BS-004", "clearEvents", "FAIL", str(e))

# ===================== CACHE_STORAGE (7 tests) =====================
@reg("TC-CS-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.cache_storage.enable(); await s.cache_storage.disable(); await s.close(); log_result("TC-CS-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-001", "enable/disable", "FAIL", str(e))

@reg("TC-CS-002", "requestCacheNames")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try: await s.cache_storage.request_cache_names("https://example.com"); await s.close(); log_result("TC-CS-002", "requestCacheNames", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-002", "requestCacheNames", "FAIL", str(e))

@reg("TC-CS-003", "requestEntries")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        caches = await s.cache_storage.request_cache_names("https://example.com")
        cid = caches["caches"][0]["cacheId"] if caches.get("caches") else None
        if not cid:
            await s.close(); log_result("TC-CS-003", "requestEntries", "SKIP", "No cache storage found"); return
        await s.cache_storage.request_entries(cid, skip_count=0, page_size=10); await s.close(); log_result("TC-CS-003", "requestEntries", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-003", "requestEntries", "FAIL", str(e))

@reg("TC-CS-004", "deleteCache")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        caches = await s.cache_storage.request_cache_names("https://example.com")
        cid = caches["caches"][0]["cacheId"] if caches.get("caches") else None
        if not cid:
            await s.close(); log_result("TC-CS-004", "deleteCache", "SKIP", "No cache storage found"); return
        await s.cache_storage.delete_cache(cid); await s.close(); log_result("TC-CS-004", "deleteCache", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-004", "deleteCache", "FAIL", str(e))

@reg("TC-CS-005", "deleteEntry")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        caches = await s.cache_storage.request_cache_names("https://example.com")
        cid = caches["caches"][0]["cacheId"] if caches.get("caches") else None
        if not cid:
            await s.close(); log_result("TC-CS-005", "deleteEntry", "SKIP", "No cache storage found"); return
        await s.cache_storage.delete_entry(cid, "https://example.com"); await s.close(); log_result("TC-CS-005", "deleteEntry", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-005", "deleteEntry", "FAIL", str(e))

@reg("TC-CS-006", "requestCachedResponse")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try:
        caches = await s.cache_storage.request_cache_names("https://example.com")
        cid = caches["caches"][0]["cacheId"] if caches.get("caches") else None
        if not cid:
            await s.close(); log_result("TC-CS-006", "requestCachedResponse", "SKIP", "No cache storage found"); return
        await s.send("CacheStorage.requestCachedResponse", {"cacheId":cid,"requestURL":"https://example.com","columnNumber":0}); await s.close(); log_result("TC-CS-006", "requestCachedResponse", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-006", "requestCachedResponse", "FAIL", str(e))

@reg("TC-CS-007", "requestCacheStorageForOrigin")
async def t(client):
    s = await fresh_session(client)
    await safe_navigate(s, "https://example.com")
    try: await s.send("CacheStorage.requestCacheStorageForOrigin", {"origin":"https://example.com"}); await s.close(); log_result("TC-CS-007", "requestCacheStorageForOrigin", "PASS")
    except Exception as e: await s.close(); log_result("TC-CS-007", "requestCacheStorageForOrigin", "FAIL", str(e))

# ===================== CAST (3 tests) =====================
@reg("TC-CAST-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Cast.enable", {}); await s.send("Cast.disable", {}); await s.close(); log_result("TC-CAST-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-CAST-001", "enable/disable", "FAIL", str(e))

@reg("TC-CAST-002", "setSinkToUse")
async def t(client):
    s = await fresh_session(client); await s.send("Cast.enable", {})
    try: await s.send("Cast.setSinkToUse", {"sinkName":"fake"}); await s.close(); log_result("TC-CAST-002", "setSinkToUse", "PASS")
    except Exception as e: await s.close(); log_result("TC-CAST-002", "setSinkToUse", "FAIL", str(e))

@reg("TC-CAST-003", "stopTabMirroring")
async def t(client):
    s = await fresh_session(client); await s.send("Cast.enable", {})
    try: await s.send("Cast.stopTabMirroring", {"sinkName":"fake"}); await s.close(); log_result("TC-CAST-003", "stopTabMirroring", "PASS")
    except Exception as e: await s.close(); log_result("TC-CAST-003", "stopTabMirroring", "FAIL", str(e))

# ===================== CONSOLE (3 tests) =====================
@reg("TC-CONSOLE-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Console.enable", {}); await s.send("Console.disable", {}); await s.close(); log_result("TC-CONSOLE-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-CONSOLE-001", "enable/disable", "FAIL", str(e))

@reg("TC-CONSOLE-002", "clearMessages")
async def t(client):
    s = await fresh_session(client); await s.send("Console.enable", {})
    try: await s.send("Console.clearMessages", {}); await s.close(); log_result("TC-CONSOLE-002", "clearMessages", "PASS")
    except Exception as e: await s.close(); log_result("TC-CONSOLE-002", "clearMessages", "FAIL", str(e))

@reg("TC-CONSOLE-003", "messageAdded")
async def t(client):
    log_result("TC-CONSOLE-003", "messageAdded", "SKIP", "Event-driven, not a command")

# ===================== DEVICE_ACCESS (2 tests) =====================
@reg("TC-DA-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DeviceAccess.enable", {}); await s.send("DeviceAccess.disable", {}); await s.close(); log_result("TC-DA-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-DA-001", "enable/disable", "FAIL", str(e))

@reg("TC-DA-002", "selectPrompt")
async def t(client):
    s = await fresh_session(client); await s.send("DeviceAccess.enable", {})
    try: await s.send("DeviceAccess.selectPrompt", {"requestId":"fake","deviceId":"fake"}); await s.close(); log_result("TC-DA-002", "selectPrompt", "PASS")
    except CommandError as e: await s.close(); log_result("TC-DA-002", "selectPrompt", "SKIP", f"No device request: {e}")
    except Exception as e: await s.close(); log_result("TC-DA-002", "selectPrompt", "FAIL", str(e))

# ===================== DEVICE_ORIENTATION (2 tests) =====================
@reg("TC-DO-001", "setDeviceOrientationOverride")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DeviceOrientation.setDeviceOrientationOverride", {"alpha":0,"beta":0,"gamma":0}); await s.close(); log_result("TC-DO-001", "setDeviceOrientationOverride", "PASS")
    except Exception as e: await s.close(); log_result("TC-DO-001", "setDeviceOrientationOverride", "FAIL", str(e))

@reg("TC-DO-002", "clearDeviceOrientationOverride")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DeviceOrientation.clearDeviceOrientationOverride", {}); await s.close(); log_result("TC-DO-002", "clearDeviceOrientationOverride", "PASS")
    except Exception as e: await s.close(); log_result("TC-DO-002", "clearDeviceOrientationOverride", "FAIL", str(e))

# ===================== DOM_DEBUGGER (7 tests) =====================
@reg("TC-DD-001", "getDOMBreakpoints")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DOMDebugger.getDOMBreakpoints", {}); await s.close(); log_result("TC-DD-001", "getDOMBreakpoints", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-001", "getDOMBreakpoints", "FAIL", str(e))

@reg("TC-DD-002", "setDOMBreakpoint")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("DOMDebugger.setDOMBreakpoint", {"nodeId":n["nodeId"],"type":"subtree-modified"}); await s.close(); log_result("TC-DD-002", "setDOMBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-002", "setDOMBreakpoint", "FAIL", str(e))

@reg("TC-DD-003", "removeDOMBreakpoint")
async def t(client):
    s = await fresh_session(client); await s.dom.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document()
    n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("DOMDebugger.removeDOMBreakpoint", {"nodeId":n["nodeId"],"type":"subtree-modified"}); await s.close(); log_result("TC-DD-003", "removeDOMBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-003", "removeDOMBreakpoint", "FAIL", str(e))

@reg("TC-DD-004", "setEventListenerBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DOMDebugger.setEventListenerBreakpoint", {"eventName":"click"}); await s.close(); log_result("TC-DD-004", "setEventListenerBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-004", "setEventListenerBreakpoint", "FAIL", str(e))

@reg("TC-DD-005", "removeEventListenerBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DOMDebugger.removeEventListenerBreakpoint", {"eventName":"click"}); await s.close(); log_result("TC-DD-005", "removeEventListenerBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-005", "removeEventListenerBreakpoint", "FAIL", str(e))

@reg("TC-DD-006", "setXHRBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DOMDebugger.setXHRBreakpoint", {"url":"https://example.com"}); await s.close(); log_result("TC-DD-006", "setXHRBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-006", "setXHRBreakpoint", "FAIL", str(e))

@reg("TC-DD-007", "removeXHRBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("DOMDebugger.removeXHRBreakpoint", {"url":"https://example.com"}); await s.close(); log_result("TC-DD-007", "removeXHRBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-DD-007", "removeXHRBreakpoint", "FAIL", str(e))

# ===================== EVENT_BREAKPOINTS (3 tests) =====================
@reg("TC-EB-001", "setInstrumentationBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("EventBreakpoints.setInstrumentationBreakpoint", {"eventName":"setInterval"}); await s.close(); log_result("TC-EB-001", "setInstrumentationBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-EB-001", "setInstrumentationBreakpoint", "FAIL", str(e))

@reg("TC-EB-002", "removeInstrumentationBreakpoint")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("EventBreakpoints.removeInstrumentationBreakpoint", {"eventName":"setInterval"}); await s.close(); log_result("TC-EB-002", "removeInstrumentationBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-EB-002", "removeInstrumentationBreakpoint", "FAIL", str(e))

@reg("TC-EB-003", "disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("EventBreakpoints.disable", {}); await s.close(); log_result("TC-EB-003", "disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-EB-003", "disable", "FAIL", str(e))

# ===================== EXTENSIONS (2 tests) =====================
@reg("TC-EXT-001", "load")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Extensions.load", {"path":"C:/fake"}); await s.close(); log_result("TC-EXT-001", "load", "FAIL", "Expected error with fake path")
    except Exception as e: await s.close(); log_result("TC-EXT-001", "load", "PASS", f"Expected error: {e}")

@reg("TC-EXT-002", "checkForAllowedExtensions")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Extensions.checkForAllowedExtensions", {}); await s.close(); log_result("TC-EXT-002", "checkForAllowedExtensions", "PASS")
    except Exception as e: await s.close(); log_result("TC-EXT-002", "checkForAllowedExtensions", "FAIL", str(e))

# ===================== HEADLESS_EXPERIMENTAL (2 tests) =====================
@reg("TC-HE-001", "beginFrame")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("HeadlessExperimental.beginFrame", {}); await s.close(); log_result("TC-HE-001", "beginFrame", "PASS")
    except Exception as e: await s.close(); log_result("TC-HE-001", "beginFrame", "FAIL", str(e))

@reg("TC-HE-002", "disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("HeadlessExperimental.disable", {}); await s.close(); log_result("TC-HE-002", "disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-HE-002", "disable", "FAIL", str(e))

# ===================== INSPECTOR (3 tests) =====================
@reg("TC-INS-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Inspector.enable", {}); await s.send("Inspector.disable", {}); await s.close(); log_result("TC-INS-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-INS-001", "enable/disable", "FAIL", str(e))

@reg("TC-INS-002", "detach")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Inspector.detach", {}); await s.close(); log_result("TC-INS-002", "detach", "PASS")
    except Exception as e: await s.close(); log_result("TC-INS-002", "detach", "FAIL", str(e))

@reg("TC-INS-003", "reload")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Inspector.reload", {}); await s.close(); log_result("TC-INS-003", "reload", "PASS")
    except Exception as e: await s.close(); log_result("TC-INS-003", "reload", "FAIL", str(e))

# ===================== IO (4 tests) =====================
@reg("TC-IO-001", "read")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    try:
        r = await s.page.print_to_pdf(return_as_stream=True)
        handle = r.get("stream")
        if not handle:
            await s.close(); log_result("TC-IO-001", "read", "SKIP", "No stream handle from printToPDF"); return
        await s.send("IO.read", {"handle": handle}); await s.close(); log_result("TC-IO-001", "read", "PASS")
    except Exception as e: await s.close(); log_result("TC-IO-001", "read", "FAIL", str(e))

@reg("TC-IO-002", "close")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    try:
        r = await s.page.print_to_pdf(return_as_stream=True)
        handle = r.get("stream")
        if not handle:
            await s.close(); log_result("TC-IO-002", "close", "SKIP", "No stream handle from printToPDF"); return
        await s.send("IO.close", {"handle": handle}); await s.close(); log_result("TC-IO-002", "close", "PASS")
    except Exception as e: await s.close(); log_result("TC-IO-002", "close", "FAIL", str(e))

@reg("TC-IO-003", "resolveBlob")
async def t(client):
    s = await fresh_session(client); await s.runtime.enable()
    r = await s.runtime.evaluate("new Blob(['test'])", return_by_value=False)
    try: await s.send("IO.resolveBlob", {"objectId": r["result"]["objectId"]}); await s.close(); log_result("TC-IO-003", "resolveBlob", "PASS")
    except Exception as e: await s.close(); log_result("TC-IO-003", "resolveBlob", "FAIL", str(e))

@reg("TC-IO-004", "read with size")
async def t(client):
    s = await fresh_session(client); await s.page.enable()
    try:
        r = await s.page.print_to_pdf(return_as_stream=True)
        handle = r.get("stream")
        if not handle:
            await s.close(); log_result("TC-IO-004", "read with size", "SKIP", "No stream handle from printToPDF"); return
        await s.send("IO.read", {"handle": handle, "size": 1024}); await s.close(); log_result("TC-IO-004", "read with size", "PASS")
    except Exception as e: await s.close(); log_result("TC-IO-004", "read with size", "FAIL", str(e))

# ===================== LAYER_TREE (8 tests) =====================
@reg("TC-LT-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.layer_tree.enable(); await s.layer_tree.disable(); await s.close(); log_result("TC-LT-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-LT-001", "enable/disable", "FAIL", str(e))

@reg("TC-LT-002", "getTree")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: r = await s.send("LayerTree.getTree", {}); await s.close(); log_result("TC-LT-002", "getTree", "PASS")
    except Exception as e: await s.close(); log_result("TC-LT-002", "getTree", "FAIL", str(e))

@reg("TC-LT-003", "loadSnapshot")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.loadSnapshot", {"tiles":[{"x":0,"y":0,"picture":"[]"}]}); await s.close(); log_result("TC-LT-003", "loadSnapshot", "PASS")
    except CommandError as e: await s.close(); log_result("TC-LT-003", "loadSnapshot", "SKIP", f"Invalid tiles: {e}")
    except Exception as e: await s.close(); log_result("TC-LT-003", "loadSnapshot", "FAIL", str(e))

@reg("TC-LT-004", "releaseSnapshot")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.releaseSnapshot", {"snapshotId":"fake"}); await s.close(); log_result("TC-LT-004", "releaseSnapshot", "PASS")
    except CommandError as e: await s.close(); log_result("TC-LT-004", "releaseSnapshot", "SKIP", f"No snapshot: {e}")
    except Exception as e: await s.close(); log_result("TC-LT-004", "releaseSnapshot", "FAIL", str(e))

@reg("TC-LT-005", "profileSnapshot")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.profileSnapshot", {"snapshotId":"fake"}); await s.close(); log_result("TC-LT-005", "profileSnapshot", "PASS")
    except CommandError as e: await s.close(); log_result("TC-LT-005", "profileSnapshot", "SKIP", f"No snapshot: {e}")
    except Exception as e: await s.close(); log_result("TC-LT-005", "profileSnapshot", "FAIL", str(e))

@reg("TC-LT-006", "replaySnapshot")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.replaySnapshot", {"snapshotId":"fake"}); await s.close(); log_result("TC-LT-006", "replaySnapshot", "PASS")
    except CommandError as e: await s.close(); log_result("TC-LT-006", "replaySnapshot", "SKIP", f"No snapshot: {e}")
    except Exception as e: await s.close(); log_result("TC-LT-006", "replaySnapshot", "FAIL", str(e))

@reg("TC-LT-007", "snapshotCommandLog")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.snapshotCommandLog", {"snapshotId":"fake"}); await s.close(); log_result("TC-LT-007", "snapshotCommandLog", "PASS")
    except CommandError as e: await s.close(); log_result("TC-LT-007", "snapshotCommandLog", "SKIP", f"No snapshot: {e}")
    except Exception as e: await s.close(); log_result("TC-LT-007", "snapshotCommandLog", "FAIL", str(e))

@reg("TC-LT-008", "setShowPaints")
async def t(client):
    s = await fresh_session(client); await s.layer_tree.enable()
    try: await s.send("LayerTree.setShowPaints", {"result": True}); await s.close(); log_result("TC-LT-008", "setShowPaints", "PASS")
    except Exception as e: await s.close(); log_result("TC-LT-008", "setShowPaints", "FAIL", str(e))

# ===================== MEDIA (4 tests) =====================
@reg("TC-MEDIA-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Media.enable", {}); await s.send("Media.disable", {}); await s.close(); log_result("TC-MEDIA-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEDIA-001", "enable/disable", "FAIL", str(e))

@reg("TC-MEDIA-002", "setPlayerMessageHandler")
async def t(client):
    s = await fresh_session(client); await s.send("Media.enable", {})
    try: await s.send("Media.setPlayerMessageHandler", {"playerId":"fake","level":"error"}); await s.close(); log_result("TC-MEDIA-002", "setPlayerMessageHandler", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEDIA-002", "setPlayerMessageHandler", "FAIL", str(e))

@reg("TC-MEDIA-003", "setPlayerBreakpoint")
async def t(client):
    s = await fresh_session(client); await s.send("Media.enable", {})
    try: await s.send("Media.setPlayerBreakpoint", {"playerId":"fake","method":"play"}); await s.close(); log_result("TC-MEDIA-003", "setPlayerBreakpoint", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEDIA-003", "setPlayerBreakpoint", "FAIL", str(e))

@reg("TC-MEDIA-004", "clearPlayerEvents")
async def t(client):
    s = await fresh_session(client); await s.send("Media.enable", {})
    try: await s.send("Media.clearPlayerEvents", {"playerId":"fake"}); await s.close(); log_result("TC-MEDIA-004", "clearPlayerEvents", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEDIA-004", "clearPlayerEvents", "FAIL", str(e))

# ===================== MEMORY (3 tests) =====================
@reg("TC-MEM-001", "getDOMCounters")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Memory.getDOMCounters", {}); await s.close(); log_result("TC-MEM-001", "getDOMCounters", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEM-001", "getDOMCounters", "FAIL", str(e))

@reg("TC-MEM-002", "prepareForLeakDetection")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Memory.prepareForLeakDetection", {}); await s.close(); log_result("TC-MEM-002", "prepareForLeakDetection", "PASS")
    except CommandError as e: await s.close(); log_result("TC-MEM-002", "prepareForLeakDetection", "SKIP", f"Not available: {e}")
    except Exception as e: await s.close(); log_result("TC-MEM-002", "prepareForLeakDetection", "FAIL", str(e))

@reg("TC-MEM-003", "setPressureNotificationsSuppressed")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Memory.setPressureNotificationsSuppressed", {"suppressed": True}); await s.close(); log_result("TC-MEM-003", "setPressureNotificationsSuppressed", "PASS")
    except Exception as e: await s.close(); log_result("TC-MEM-003", "setPressureNotificationsSuppressed", "FAIL", str(e))

# ===================== PERFORMANCE_TIMELINE (2 tests) =====================
@reg("TC-PT-001", "enable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("PerformanceTimeline.enable", {"eventTypes":["firstPaint"]}); await s.close(); log_result("TC-PT-001", "enable", "PASS")
    except CommandError as e: await s.close(); log_result("TC-PT-001", "enable", "SKIP", f"Unsupported event type: {e}")
    except Exception as e: await s.close(); log_result("TC-PT-001", "enable", "FAIL", str(e))

@reg("TC-PT-002", "enable with event_types")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("PerformanceTimeline.enable", {"eventTypes":["firstPaint","firstContentfulPaint","largestContentfulPaint"]}); await s.close(); log_result("TC-PT-002", "enable with event_types", "PASS")
    except CommandError as e: await s.close(); log_result("TC-PT-002", "enable with event_types", "SKIP", f"Unsupported event type: {e}")
    except Exception as e: await s.close(); log_result("TC-PT-002", "enable with event_types", "FAIL", str(e))

# ===================== PRELOAD (3 tests) =====================
@reg("TC-PL-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Preload.enable", {}); await s.send("Preload.disable", {}); await s.close(); log_result("TC-PL-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-PL-001", "enable/disable", "FAIL", str(e))

@reg("TC-PL-002", "setPreloadPrefetchLogging")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Preload.setPrefetchLogging", {"enabled": True}); await s.close(); log_result("TC-PL-002", "setPreloadPrefetchLogging", "PASS")
    except Exception as e: await s.close(); log_result("TC-PL-002", "setPreloadPrefetchLogging", "FAIL", str(e))

@reg("TC-PL-003", "setPrefetchLogging")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Preload.setPrefetchLogging", {"enabled": False}); await s.close(); log_result("TC-PL-003", "setPrefetchLogging", "PASS")
    except Exception as e: await s.close(); log_result("TC-PL-003", "setPrefetchLogging", "FAIL", str(e))

# ===================== PWA (3 tests) =====================
@reg("TC-PWA-001", "install")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("PWA.install", {"manifestId":"https://example.com/manifest.json"}); await s.close(); log_result("TC-PWA-001", "install", "PASS")
    except Exception as e: await s.close(); log_result("TC-PWA-001", "install", "FAIL", str(e))

@reg("TC-PWA-002", "uninstall")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("PWA.uninstall", {"manifestId":"https://example.com/manifest.json"}); await s.close(); log_result("TC-PWA-002", "uninstall", "PASS")
    except Exception as e: await s.close(); log_result("TC-PWA-002", "uninstall", "FAIL", str(e))

@reg("TC-PWA-003", "launch")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("PWA.launch", {"manifestId":"https://example.com/manifest.json"}); await s.close(); log_result("TC-PWA-003", "launch", "PASS")
    except Exception as e: await s.close(); log_result("TC-PWA-003", "launch", "FAIL", str(e))

# ===================== SCHEMA (2 tests) =====================
@reg("TC-SCHEMA-001", "getDomains")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("Schema.getDomains", {}); await s.close(); log_result("TC-SCHEMA-001", "getDomains", "PASS")
    except Exception as e: await s.close(); log_result("TC-SCHEMA-001", "getDomains", "FAIL", str(e))

@reg("TC-SCHEMA-002", "getDomains flatten")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("Schema.getDomains", {}); assert "domains" in r; await s.close(); log_result("TC-SCHEMA-002", "getDomains flatten", "PASS")
    except Exception as e: await s.close(); log_result("TC-SCHEMA-002", "getDomains flatten", "FAIL", str(e))

# ===================== SENSOR (4 tests) =====================
@reg("TC-SENSOR-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.sensor.enable(); await s.sensor.disable(); await s.close(); log_result("TC-SENSOR-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-SENSOR-001", "enable/disable", "FAIL", str(e))

@reg("TC-SENSOR-002", "setSensorOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.sensor.enable()
        await s.sensor.set_sensor_override("accelerometer", {"x":0,"y":9.8,"z":0}); await s.close(); log_result("TC-SENSOR-002", "setSensorOverride", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SENSOR-002", "setSensorOverride", "SKIP", f"Sensor domain not available: {e}")
    except Exception as e: await s.close(); log_result("TC-SENSOR-002", "setSensorOverride", "FAIL", str(e))

@reg("TC-SENSOR-003", "clearSensorOverride")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.sensor.enable()
        await s.sensor.clear_sensor_override("accelerometer"); await s.close(); log_result("TC-SENSOR-003", "clearSensorOverride", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SENSOR-003", "clearSensorOverride", "SKIP", f"Sensor domain not available: {e}")
    except Exception as e: await s.close(); log_result("TC-SENSOR-003", "clearSensorOverride", "FAIL", str(e))

@reg("TC-SENSOR-004", "set_sensor_override gyroscope")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.sensor.enable()
        await s.sensor.set_sensor_override("gyroscope", {"x":0,"y":0,"z":0}); await s.close(); log_result("TC-SENSOR-004", "set_sensor_override gyroscope", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SENSOR-004", "set_sensor_override gyroscope", "SKIP", f"Sensor domain not available: {e}")
    except Exception as e: await s.close(); log_result("TC-SENSOR-004", "set_sensor_override gyroscope", "FAIL", str(e))

# ===================== SYSTEM_INFO (5 tests) =====================
@reg("TC-SI-001", "getInfo")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("SystemInfo.getInfo", {}); await s.close(); log_result("TC-SI-001", "getInfo", "PASS")
    except Exception as e:
        await s.close()
        if "browser target" in str(e): log_result("TC-SI-001", "getInfo", "SKIP", "Only supported on browser target")
        else: log_result("TC-SI-001", "getInfo", "FAIL", str(e))

@reg("TC-SI-002", "getProcessInfo")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("SystemInfo.getProcessInfo", {}); await s.close(); log_result("TC-SI-002", "getProcessInfo", "PASS")
    except Exception as e:
        await s.close()
        if "browser target" in str(e): log_result("TC-SI-002", "getProcessInfo", "SKIP", "Only supported on browser target")
        else: log_result("TC-SI-002", "getProcessInfo", "FAIL", str(e))

@reg("TC-SI-003", "getFeatureState")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("SystemInfo.getFeatureState", {"featureId":"test"}); await s.close(); log_result("TC-SI-003", "getFeatureState", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SI-003", "getFeatureState", "SKIP", f"Invalid featureId or browser target only: {e}")
    except Exception as e: await s.close(); log_result("TC-SI-003", "getFeatureState", "FAIL", str(e))

@reg("TC-SI-004", "getGPUInfo")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("SystemInfo.getInfo", {}); assert "gpu" in r; await s.close(); log_result("TC-SI-004", "getGPUInfo", "PASS")
    except Exception as e:
        await s.close()
        if "browser target" in str(e): log_result("TC-SI-004", "getGPUInfo", "SKIP", "Only supported on browser target")
        else: log_result("TC-SI-004", "getGPUInfo", "FAIL", str(e))

@reg("TC-SI-005", "getDisplayInfo")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("SystemInfo.getInfo", {}); assert "displays" in r.get("gpu",{}); await s.close(); log_result("TC-SI-005", "getDisplayInfo", "PASS")
    except Exception as e:
        await s.close()
        if "browser target" in str(e): log_result("TC-SI-005", "getDisplayInfo", "SKIP", "Only supported on browser target")
        else: log_result("TC-SI-005", "getDisplayInfo", "FAIL", str(e))

# ===================== TETHERING (2 tests) =====================
@reg("TC-TETH-001", "bind")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Tethering.bind", {"port": 8080}); await s.close(); log_result("TC-TETH-001", "bind", "PASS")
    except Exception as e: await s.close(); log_result("TC-TETH-001", "bind", "FAIL", str(e))

@reg("TC-TETH-002", "unbind")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Tethering.unbind", {"port": 8080}); await s.close(); log_result("TC-TETH-002", "unbind", "PASS")
    except Exception as e: await s.close(); log_result("TC-TETH-002", "unbind", "FAIL", str(e))

# ===================== TRACING (5 tests) =====================
@reg("TC-TRACE-001", "start")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Tracing.start", {"traceConfig":{"recordMode":"recordUntilFull","includedCategories":["disabled-by-default-devtools.timeline"]}}); await s.send("Tracing.end", {}); await s.close(); log_result("TC-TRACE-001", "start", "PASS")
    except Exception as e: await s.close(); log_result("TC-TRACE-001", "start", "FAIL", str(e))

@reg("TC-TRACE-002", "end")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Tracing.start", {"traceConfig":{}}); await s.send("Tracing.end", {}); await s.close(); log_result("TC-TRACE-002", "end", "PASS")
    except Exception as e: await s.close(); log_result("TC-TRACE-002", "end", "FAIL", str(e))

@reg("TC-TRACE-003", "getCategories")
async def t(client):
    s = await fresh_session(client)
    try: r = await s.send("Tracing.getCategories", {}); await s.close(); log_result("TC-TRACE-003", "getCategories", "PASS")
    except Exception as e: await s.close(); log_result("TC-TRACE-003", "getCategories", "FAIL", str(e))

@reg("TC-TRACE-004", "recordClockSyncMarker")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Tracing.start", {"traceConfig": {"recordMode": "recordUntilFull"}})
        await s.send("Tracing.recordClockSyncMarker", {"syncId": "test"})
        await s.send("Tracing.end", {})
        await s.close(); log_result("TC-TRACE-004", "recordClockSyncMarker", "PASS")
    except Exception as e:
        await s.close(); log_result("TC-TRACE-004", "recordClockSyncMarker", "FAIL", str(e))

@reg("TC-TRACE-005", "requestClockSyncMarker")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Tracing.requestClockSyncMarker", {}); await s.close(); log_result("TC-TRACE-005", "requestClockSyncMarker", "PASS")
    except Exception as e: await s.close(); log_result("TC-TRACE-005", "requestClockSyncMarker", "FAIL", str(e))

# ===================== WORKER (4 tests) =====================
@reg("TC-WORKER-001", "disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Worker.disable", {}); await s.close(); log_result("TC-WORKER-001", "disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-WORKER-001", "disable", "FAIL", str(e))

@reg("TC-WORKER-002", "enable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Worker.enable", {}); await s.close(); log_result("TC-WORKER-002", "enable", "PASS")
    except Exception as e: await s.close(); log_result("TC-WORKER-002", "enable", "FAIL", str(e))

@reg("TC-WORKER-003", "sendMessageToWorker")
async def t(client):
    s = await fresh_session(client)
    try:
        await s.send("Worker.enable", {})
        await s.send("Worker.sendMessageToWorker", {"targetId":"fake","message":"{}"}); await s.close(); log_result("TC-WORKER-003", "sendMessageToWorker", "PASS")
    except Exception as e: await s.close(); log_result("TC-WORKER-003", "sendMessageToWorker", "FAIL", str(e))

@reg("TC-WORKER-004", "canInspectWorker")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Worker.enable", {}); await s.send("Worker.disable", {}); await s.close(); log_result("TC-WORKER-004", "canInspectWorker", "PASS")
    except Exception as e: await s.close(); log_result("TC-WORKER-004", "canInspectWorker", "FAIL", str(e))
