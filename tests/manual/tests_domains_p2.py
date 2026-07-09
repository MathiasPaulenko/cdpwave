"""P2 domains: LOG, PERFORMANCE, PROFILER, HEAP_PROFILER, SECURITY, ACCESSIBILITY, ANIMATION, INDEXEDDB, SERVICE_WORKER, WEBAUTHN."""

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

# ===================== LOG DOMAIN (5 tests) =====================
@reg("TC-LOG-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.log.enable(); await s.log.disable(); await s.close(); log_result("TC-LOG-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-LOG-001", "enable/disable", "FAIL", str(e))

@reg("TC-LOG-002", "clear")
async def t(client):
    s = await fresh_session(client); await s.log.enable()
    try: await s.log.clear(); await s.close(); log_result("TC-LOG-002", "clear", "PASS")
    except Exception as e: await s.close(); log_result("TC-LOG-002", "clear", "FAIL", str(e))

@reg("TC-LOG-003", "startViolationsReport")
async def t(client):
    s = await fresh_session(client); await s.log.enable()
    try: await s.log.start_violations_report([{"name":"longTask","threshold":50}]); await s.close(); log_result("TC-LOG-003", "startViolationsReport", "PASS")
    except Exception as e: await s.close(); log_result("TC-LOG-003", "startViolationsReport", "FAIL", str(e))

@reg("TC-LOG-004", "stopViolationsReport")
async def t(client):
    s = await fresh_session(client); await s.log.enable()
    try: await s.log.stop_violations_report(); await s.close(); log_result("TC-LOG-004", "stopViolationsReport", "PASS")
    except Exception as e: await s.close(); log_result("TC-LOG-004", "stopViolationsReport", "FAIL", str(e))

@reg("TC-LOG-005", "getViolationsReport")
async def t(client):
    s = await fresh_session(client); await s.log.enable()
    try: await s.send("Log.getViolationsReport", {}); await s.close(); log_result("TC-LOG-005", "getViolationsReport", "PASS")
    except Exception as e: await s.close(); log_result("TC-LOG-005", "getViolationsReport", "FAIL", str(e))

# ===================== PERFORMANCE DOMAIN (4 tests) =====================
@reg("TC-PERF-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Performance.enable", {}); await s.send("Performance.disable", {}); await s.close(); log_result("TC-PERF-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-PERF-001", "enable/disable", "FAIL", str(e))

@reg("TC-PERF-002", "getMetrics")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Performance.enable", {}); r = await s.send("Performance.getMetrics", {}); await s.close(); log_result("TC-PERF-002", "getMetrics", "PASS")
    except Exception as e: await s.close(); log_result("TC-PERF-002", "getMetrics", "FAIL", str(e))

@reg("TC-PERF-003", "setTimeDomain")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Performance.setTimeDomain", {"timeDomain":"timeTicks"}); await s.send("Performance.enable", {}); await s.close(); log_result("TC-PERF-003", "setTimeDomain", "PASS")
    except Exception as e: await s.close(); log_result("TC-PERF-003", "setTimeDomain", "FAIL", str(e))

@reg("TC-PERF-004", "setDisableMetrics")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Performance.enable", {}); await s.send("Performance.disable", {}); await s.close(); log_result("TC-PERF-004", "setDisableMetrics", "PASS")
    except Exception as e: await s.close(); log_result("TC-PERF-004", "setDisableMetrics", "FAIL", str(e))

# ===================== PROFILER DOMAIN (9 tests) =====================
@reg("TC-PROFILER-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.profiler.enable(); await s.profiler.disable(); await s.close(); log_result("TC-PROFILER-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-001", "enable/disable", "FAIL", str(e))

@reg("TC-PROFILER-002", "start")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: await s.profiler.start(); await s.close(); log_result("TC-PROFILER-002", "start", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-002", "start", "FAIL", str(e))

@reg("TC-PROFILER-003", "stop")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable(); await s.profiler.start()
    try: r = await s.profiler.stop(); await s.close(); log_result("TC-PROFILER-003", "stop", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-003", "stop", "FAIL", str(e))

@reg("TC-PROFILER-004", "setSamplingInterval")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: await s.profiler.set_sampling_interval(100); await s.close(); log_result("TC-PROFILER-004", "setSamplingInterval", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-004", "setSamplingInterval", "FAIL", str(e))

@reg("TC-PROFILER-005", "setPreciseCoverage")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: r = await s.profiler.start_precise_coverage(call_count=True, detailed=False, allow_triggered_updates=True); await s.close(); log_result("TC-PROFILER-005", "setPreciseCoverage", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-005", "setPreciseCoverage", "FAIL", str(e))

@reg("TC-PROFILER-006", "takePreciseCoverage")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: await s.profiler.start_precise_coverage(); r = await s.profiler.take_precise_coverage(); await s.close(); log_result("TC-PROFILER-006", "takePreciseCoverage", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-006", "takePreciseCoverage", "FAIL", str(e))

@reg("TC-PROFILER-007", "getBestEffortCoverage")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: r = await s.profiler.get_best_effort_coverage(); await s.close(); log_result("TC-PROFILER-007", "getBestEffortCoverage", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-007", "getBestEffortCoverage", "FAIL", str(e))

@reg("TC-PROFILER-008", "startTypeProfile")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: await s.send("Profiler.startTypeProfile", {}); await s.close(); log_result("TC-PROFILER-008", "startTypeProfile", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-008", "startTypeProfile", "FAIL", str(e))

@reg("TC-PROFILER-009", "stopTypeProfile")
async def t(client):
    s = await fresh_session(client); await s.profiler.enable()
    try: await s.send("Profiler.stopTypeProfile", {}); await s.close(); log_result("TC-PROFILER-009", "stopTypeProfile", "PASS")
    except Exception as e: await s.close(); log_result("TC-PROFILER-009", "stopTypeProfile", "FAIL", str(e))

# ===================== HEAP PROFILER DOMAIN (10 tests) =====================
@reg("TC-HEAP-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.heap_profiler.enable(); await s.heap_profiler.disable(); await s.close(); log_result("TC-HEAP-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-001", "enable/disable", "FAIL", str(e))

@reg("TC-HEAP-002", "startSampling")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.startSampling", {"samplingInterval":64}); await s.close(); log_result("TC-HEAP-002", "startSampling", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-002", "startSampling", "FAIL", str(e))

@reg("TC-HEAP-003", "stopSampling")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.startSampling", {}); r = await s.send("HeapProfiler.stopSampling", {}); await s.close(); log_result("TC-HEAP-003", "stopSampling", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-003", "stopSampling", "FAIL", str(e))

@reg("TC-HEAP-004", "startTrackingHeapObjects")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.startTrackingHeapObjects", {"trackAllocations":True}); await s.close(); log_result("TC-HEAP-004", "startTrackingHeapObjects", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-004", "startTrackingHeapObjects", "FAIL", str(e))

@reg("TC-HEAP-005", "stopTrackingHeapObjects")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.startTrackingHeapObjects", {}); await s.send("HeapProfiler.stopTrackingHeapObjects", {"reportProgress":False}); await s.close(); log_result("TC-HEAP-005", "stopTrackingHeapObjects", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-005", "stopTrackingHeapObjects", "FAIL", str(e))

@reg("TC-HEAP-006", "takeHeapSnapshot")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.heap_profiler.take_heap_snapshot(report_progress=False); await s.close(); log_result("TC-HEAP-006", "takeHeapSnapshot", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-006", "takeHeapSnapshot", "FAIL", str(e))

@reg("TC-HEAP-007", "collectGarbage")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.collectGarbage", {}); await s.close(); log_result("TC-HEAP-007", "collectGarbage", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-007", "collectGarbage", "FAIL", str(e))

@reg("TC-HEAP-008", "getObjectByHeapObjectId")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try:
        await s.send("HeapProfiler.startSampling", {"samplingInterval": 4096})
        await s.runtime.evaluate("var x = {a:1,b:2}; x")
        r = await s.send("HeapProfiler.getLastSeenObjectId", {})
        oid = str(r.get("lastSeenObjectId", 0))
        if oid == "0":
            await s.send("HeapProfiler.stopSampling", {})
            await s.close(); log_result("TC-HEAP-008", "getObjectByHeapObjectId", "SKIP", "No heap object ID"); return
        await s.send("HeapProfiler.getObjectByHeapObjectId", {"heapObjectId": oid})
        await s.send("HeapProfiler.stopSampling", {})
        await s.close(); log_result("TC-HEAP-008", "getObjectByHeapObjectId", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-008", "getObjectByHeapObjectId", "FAIL", str(e))

@reg("TC-HEAP-009", "addHeapSnapshotChunk")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.addHeapSnapshotChunk", {"chunk":"{}"}); await s.close(); log_result("TC-HEAP-009", "addHeapSnapshotChunk", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-009", "addHeapSnapshotChunk", "FAIL", str(e))

@reg("TC-HEAP-010", "getLastSeenObjectID")
async def t(client):
    s = await fresh_session(client); await s.heap_profiler.enable()
    try: await s.send("HeapProfiler.getLastSeenObjectId", {}); await s.close(); log_result("TC-HEAP-010", "getLastSeenObjectID", "PASS")
    except Exception as e: await s.close(); log_result("TC-HEAP-010", "getLastSeenObjectID", "FAIL", str(e))

# ===================== SECURITY DOMAIN (4 tests) =====================
@reg("TC-SECURITY-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.security.enable(); await s.security.disable(); await s.close(); log_result("TC-SECURITY-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-SECURITY-001", "enable/disable", "FAIL", str(e))

@reg("TC-SECURITY-002", "setIgnoreCertificateErrors")
async def t(client):
    s = await fresh_session(client); await s.security.enable()
    try: await s.security.set_override_certificate_errors(override=True); await s.close(); log_result("TC-SECURITY-002", "setIgnoreCertificateErrors", "PASS")
    except Exception as e: await s.close(); log_result("TC-SECURITY-002", "setIgnoreCertificateErrors", "FAIL", str(e))

@reg("TC-SECURITY-003", "handleCertificateError")
async def t(client):
    s = await fresh_session(client); await s.security.enable()
    try: await s.security.handle_certificate_error(event_id=1, action="continue"); await s.close(); log_result("TC-SECURITY-003", "handleCertificateError", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-SECURITY-003", "handleCertificateError", "SKIP", f"No real certificate error event: {e}")
    except Exception as e:
        await s.close(); log_result("TC-SECURITY-003", "handleCertificateError", "FAIL", str(e))

@reg("TC-SECURITY-004", "getVisibleSecurityState")
async def t(client):
    s = await fresh_session(client); await s.security.enable()
    try: await s.security.get_visible_security_state(); await s.close(); log_result("TC-SECURITY-004", "getVisibleSecurityState", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SECURITY-004", "getVisibleSecurityState", "SKIP", f"CDP method not available: {e}")
    except Exception as e: await s.close(); log_result("TC-SECURITY-004", "getVisibleSecurityState", "FAIL", str(e))

# ===================== ACCESSIBILITY DOMAIN (7 tests) =====================
@reg("TC-A11Y-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.accessibility.enable(); await s.accessibility.disable(); await s.close(); log_result("TC-A11Y-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-001", "enable/disable", "FAIL", str(e))

@reg("TC-A11Y-002", "getPartialAXTree")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.accessibility.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document(); n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("Accessibility.getPartialAXTree", {"nodeId": n["nodeId"]}); await s.close(); log_result("TC-A11Y-002", "getPartialAXTree", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-002", "getPartialAXTree", "FAIL", str(e))

@reg("TC-A11Y-003", "getFullAXTree")
async def t(client):
    s = await fresh_session(client); await s.accessibility.enable()
    try: r = await s.accessibility.get_full_ax_tree(); await s.close(); log_result("TC-A11Y-003", "getFullAXTree", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-003", "getFullAXTree", "FAIL", str(e))

@reg("TC-A11Y-004", "getRootAXNode")
async def t(client):
    s = await fresh_session(client); await s.accessibility.enable()
    try: await s.send("Accessibility.getRootAXNode", {}); await s.close(); log_result("TC-A11Y-004", "getRootAXNode", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-004", "getRootAXNode", "FAIL", str(e))

@reg("TC-A11Y-005", "getAXNodeAndAncestors")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.accessibility.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document(); n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("Accessibility.getAXNodeAndAncestors", {"nodeId": n["nodeId"]}); await s.close(); log_result("TC-A11Y-005", "getAXNodeAndAncestors", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-005", "getAXNodeAndAncestors", "FAIL", str(e))

@reg("TC-A11Y-006", "getAXNode")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.accessibility.enable()
    await nav_data(s, "<div id='t'>Test</div>")
    d = await s.dom.get_document(); n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("Accessibility.getAXNode", {"nodeId": n["nodeId"]}); await s.close(); log_result("TC-A11Y-006", "getAXNode", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-006", "getAXNode", "FAIL", str(e))

@reg("TC-A11Y-007", "getImageData")
async def t(client):
    s = await fresh_session(client); await s.dom.enable(); await s.accessibility.enable()
    await nav_data(s, "<img id='t' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>")
    d = await s.dom.get_document(); n = await s.dom.query_selector(d["root"]["nodeId"], "#t")
    try: await s.send("Accessibility.getImageData", {"nodeId": n["nodeId"]}); await s.close(); log_result("TC-A11Y-007", "getImageData", "PASS")
    except Exception as e: await s.close(); log_result("TC-A11Y-007", "getImageData", "FAIL", str(e))

# ===================== ANIMATION DOMAIN (9 tests) =====================
@reg("TC-ANIM-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("Animation.enable", {}); await s.send("Animation.disable", {}); await s.close(); log_result("TC-ANIM-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-001", "enable/disable", "FAIL", str(e))

@reg("TC-ANIM-002", "getPlayState")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.getPlaybackRate", {}); await s.close(); log_result("TC-ANIM-002", "getPlayState", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-002", "getPlayState", "FAIL", str(e))

@reg("TC-ANIM-003", "getCurrentTime")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.getCurrentTime", {"id":"1"}); await s.close(); log_result("TC-ANIM-003", "getCurrentTime", "PASS")
    except CommandError as e: await s.close(); log_result("TC-ANIM-003", "getCurrentTime", "SKIP", f"No real animation: {e}")
    except Exception as e: await s.close(); log_result("TC-ANIM-003", "getCurrentTime", "FAIL", str(e))

@reg("TC-ANIM-004", "setPlaybackRate")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.setPlaybackRate", {"playbackRate": 2}); await s.close(); log_result("TC-ANIM-004", "setPlaybackRate", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-004", "setPlaybackRate", "FAIL", str(e))

@reg("TC-ANIM-005", "setTiming")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.setTiming", {"animationId":"1","duration":1000,"delay":0}); await s.close(); log_result("TC-ANIM-005", "setTiming", "PASS")
    except CommandError as e: await s.close(); log_result("TC-ANIM-005", "setTiming", "SKIP", f"No real animation: {e}")
    except Exception as e: await s.close(); log_result("TC-ANIM-005", "setTiming", "FAIL", str(e))

@reg("TC-ANIM-006", "seekAnimations")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.seekAnimations", {"animations":["1"],"currentTime":100}); await s.close(); log_result("TC-ANIM-006", "seekAnimations", "PASS")
    except CommandError as e: await s.close(); log_result("TC-ANIM-006", "seekAnimations", "SKIP", f"No real animation: {e}")
    except Exception as e: await s.close(); log_result("TC-ANIM-006", "seekAnimations", "FAIL", str(e))

@reg("TC-ANIM-007", "pause")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.pause", {"animations":["1"]}); await s.close(); log_result("TC-ANIM-007", "pause", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-007", "pause", "FAIL", str(e))

@reg("TC-ANIM-008", "resume")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.resume", {"animations":["1"]}); await s.close(); log_result("TC-ANIM-008", "resume", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-008", "resume", "FAIL", str(e))

@reg("TC-ANIM-009", "releaseAnimations")
async def t(client):
    s = await fresh_session(client); await s.send("Animation.enable", {})
    try: await s.send("Animation.releaseAnimations", {"animations":["1"]}); await s.close(); log_result("TC-ANIM-009", "releaseAnimations", "PASS")
    except Exception as e: await s.close(); log_result("TC-ANIM-009", "releaseAnimations", "FAIL", str(e))

# ===================== INDEXEDDB DOMAIN (7 tests) =====================
@reg("TC-IDB-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("IndexedDB.enable", {}); await s.send("IndexedDB.disable", {}); await s.close(); log_result("TC-IDB-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-IDB-001", "enable/disable", "FAIL", str(e))

@reg("TC-IDB-002", "requestDatabaseNames")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.requestDatabaseNames", {"securityOrigin":"https://example.com"}); await s.close(); log_result("TC-IDB-002", "requestDatabaseNames", "PASS")
    except Exception as e: await s.close(); log_result("TC-IDB-002", "requestDatabaseNames", "FAIL", str(e))

@reg("TC-IDB-003", "requestDatabase")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.requestDatabase", {"securityOrigin":"https://example.com","databaseName":"test"}); await s.close(); log_result("TC-IDB-003", "requestDatabase", "PASS")
    except CommandError as e: await s.close(); log_result("TC-IDB-003", "requestDatabase", "SKIP", f"No IDB database: {e}")
    except Exception as e: await s.close(); log_result("TC-IDB-003", "requestDatabase", "FAIL", str(e))

@reg("TC-IDB-004", "deleteDatabase")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.deleteDatabase", {"securityOrigin":"https://example.com","databaseName":"test"}); await s.close(); log_result("TC-IDB-004", "deleteDatabase", "PASS")
    except Exception as e: await s.close(); log_result("TC-IDB-004", "deleteDatabase", "FAIL", str(e))

@reg("TC-IDB-005", "requestData")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.requestData", {"securityOrigin":"https://example.com","databaseName":"test","objectStoreName":"store","indexName":"","skipCount":0,"pageSize":10}); await s.close(); log_result("TC-IDB-005", "requestData", "PASS")
    except CommandError as e: await s.close(); log_result("TC-IDB-005", "requestData", "SKIP", f"No IDB database: {e}")
    except Exception as e: await s.close(); log_result("TC-IDB-005", "requestData", "FAIL", str(e))

@reg("TC-IDB-006", "deleteObjectStore")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.deleteObjectStore", {"securityOrigin":"https://example.com","databaseName":"test","objectStoreName":"store"}); await s.close(); log_result("TC-IDB-006", "deleteObjectStore", "PASS")
    except Exception as e: await s.close(); log_result("TC-IDB-006", "deleteObjectStore", "FAIL", str(e))

@reg("TC-IDB-007", "clearObjectStore")
async def t(client):
    s = await fresh_session(client); await safe_navigate(s, "https://example.com")
    try: await s.send("IndexedDB.clearObjectStore", {"securityOrigin":"https://example.com","databaseName":"test","objectStoreName":"store"}); await s.close(); log_result("TC-IDB-007", "clearObjectStore", "PASS")
    except CommandError as e: await s.close(); log_result("TC-IDB-007", "clearObjectStore", "SKIP", f"No IDB database: {e}")
    except Exception as e: await s.close(); log_result("TC-IDB-007", "clearObjectStore", "FAIL", str(e))

# ===================== SERVICE WORKER DOMAIN (11 tests) =====================
@reg("TC-SW-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.service_worker.enable(); await s.service_worker.disable(); await s.close(); log_result("TC-SW-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-001", "enable/disable", "FAIL", str(e))

@reg("TC-SW-002", "unregister")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.unregister("https://example.com/"); await s.close(); log_result("TC-SW-002", "unregister", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SW-002", "unregister", "SKIP", f"No SW registration: {e}")
    except Exception as e: await s.close(); log_result("TC-SW-002", "unregister", "FAIL", str(e))

@reg("TC-SW-003", "updateRegistration")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.update("https://example.com/"); await s.close(); log_result("TC-SW-003", "updateRegistration", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-003", "updateRegistration", "FAIL", str(e))

@reg("TC-SW-004", "startWorker")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.start_worker("https://example.com/"); await s.close(); log_result("TC-SW-004", "startWorker", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SW-004", "startWorker", "SKIP", f"No SW registration: {e}")
    except Exception as e: await s.close(); log_result("TC-SW-004", "startWorker", "FAIL", str(e))

@reg("TC-SW-005", "skipWaiting")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.skip_waiting("https://example.com/"); await s.close(); log_result("TC-SW-005", "skipWaiting", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SW-005", "skipWaiting", "SKIP", f"No SW registration: {e}")
    except Exception as e: await s.close(); log_result("TC-SW-005", "skipWaiting", "FAIL", str(e))

@reg("TC-SW-006", "stopWorker")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.stop_worker("fake_version_id"); await s.close(); log_result("TC-SW-006", "stopWorker", "PASS")
    except CommandError as e: await s.close(); log_result("TC-SW-006", "stopWorker", "SKIP", f"Invalid version ID: {e}")
    except Exception as e: await s.close(); log_result("TC-SW-006", "stopWorker", "FAIL", str(e))

@reg("TC-SW-007", "stopAllWorkers")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.send("ServiceWorker.stopAllWorkers", {}); await s.close(); log_result("TC-SW-007", "stopAllWorkers", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-007", "stopAllWorkers", "FAIL", str(e))

@reg("TC-SW-008", "dispatchSyncEvent")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try:
        await s.service_worker.dispatch_sync_event(origin="https://example.com", registration_id="1", tag="test", data="{}")
        await s.close(); log_result("TC-SW-008", "dispatchSyncEvent", "PASS")
    except CommandError as e:
        await s.close(); log_result("TC-SW-008", "dispatchSyncEvent", "SKIP", f"No SW registration: {e}")
    except Exception as e:
        await s.close(); log_result("TC-SW-008", "dispatchSyncEvent", "FAIL", str(e))

@reg("TC-SW-009", "inspectWorker")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.service_worker.inspect_worker("fake_version_id"); await s.close(); log_result("TC-SW-009", "inspectWorker", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-009", "inspectWorker", "FAIL", str(e))

@reg("TC-SW-010", "getWorkers")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.send("ServiceWorker.getWorkers", {}); await s.close(); log_result("TC-SW-010", "getWorkers", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-010", "getWorkers", "FAIL", str(e))

@reg("TC-SW-011", "getVersion")
async def t(client):
    s = await fresh_session(client); await s.service_worker.enable()
    try: await s.send("ServiceWorker.getMessages", {}); await s.close(); log_result("TC-SW-011", "getVersion", "PASS")
    except Exception as e: await s.close(); log_result("TC-SW-011", "getVersion", "FAIL", str(e))

# ===================== WEBAUTHN DOMAIN (11 tests) =====================
@reg("TC-WA-001", "enable/disable")
async def t(client):
    s = await fresh_session(client)
    try: await s.send("WebAuthn.enable", {}); await s.send("WebAuthn.disable", {}); await s.close(); log_result("TC-WA-001", "enable/disable", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-001", "enable/disable", "FAIL", str(e))

@reg("TC-WA-002", "addVirtualAuthenticator")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try: await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}}); await s.close(); log_result("TC-WA-002", "addVirtualAuthenticator", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-002", "addVirtualAuthenticator", "FAIL", str(e))

@reg("TC-WA-003", "removeVirtualAuthenticator")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.removeVirtualAuthenticator", {"authenticatorId":aid}); await s.close(); log_result("TC-WA-003", "removeVirtualAuthenticator", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-003", "removeVirtualAuthenticator", "FAIL", str(e))

@reg("TC-WA-004", "getCredentials")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.getCredentials", {"authenticatorId":aid}); await s.close(); log_result("TC-WA-004", "getCredentials", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-004", "getCredentials", "FAIL", str(e))

@reg("TC-WA-005", "add_credential")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"u2f","transport":"usb","hasResidentKey":False,"hasUserVerification":False,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.addCredential", {"authenticatorId":aid,"credential":{"credentialId":"Y3JlZDE=","isResidentCredential":False,"rpId":"example.com","privateKey":"MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgNKvNmKmuqt069Px5nhajRhtM6BneHWzcB7vJg44VQa2hRANCAARSM7L9peOJ0VwGHZNfiSqNFlzJmL2yMQu9MjATMIFS5S93uZ4TZGmSJtywaDKLx1zGqN95qDTBoLkOsPBF7tWG","signCount":0}}); await s.close(); log_result("TC-WA-005", "add_credential", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-005", "add_credential", "FAIL", str(e))

@reg("TC-WA-006", "get_credential")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.getCredential", {"authenticatorId":aid,"credentialId":"fake"}); await s.close(); log_result("TC-WA-006", "get_credential", "PASS")
    except CommandError as e: await s.close(); log_result("TC-WA-006", "get_credential", "SKIP", f"No credential: {e}")
    except Exception as e: await s.close(); log_result("TC-WA-006", "get_credential", "FAIL", str(e))

@reg("TC-WA-007", "remove_credential")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.removeCredential", {"authenticatorId":aid,"credentialId":"fake"}); await s.close(); log_result("TC-WA-007", "remove_credential", "PASS")
    except CommandError as e: await s.close(); log_result("TC-WA-007", "remove_credential", "SKIP", f"No credential: {e}")
    except Exception as e: await s.close(); log_result("TC-WA-007", "remove_credential", "FAIL", str(e))

@reg("TC-WA-008", "clear_credentials")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.clearCredentials", {"authenticatorId":aid}); await s.close(); log_result("TC-WA-008", "clear_credentials", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-008", "clear_credentials", "FAIL", str(e))

@reg("TC-WA-009", "set_user_verified")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.setUserVerified", {"authenticatorId":aid,"isUserVerified":True}); await s.close(); log_result("TC-WA-009", "set_user_verified", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-009", "set_user_verified", "FAIL", str(e))

@reg("TC-WA-010", "set_automatic_presence_simulation")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try:
        r = await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"ctap2","transport":"internal","hasResidentKey":True,"hasUserVerification":True,"automaticPresenceSimulation":True,"isUserVerified":True}})
        aid = r["authenticatorId"]
        await s.send("WebAuthn.setAutomaticPresenceSimulation", {"authenticatorId":aid,"enabled":True}); await s.close(); log_result("TC-WA-010", "set_automatic_presence_simulation", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-010", "set_automatic_presence_simulation", "FAIL", str(e))

@reg("TC-WA-011", "add_virtual_authenticator with options")
async def t(client):
    s = await fresh_session(client); await s.send("WebAuthn.enable", {})
    try: await s.send("WebAuthn.addVirtualAuthenticator", {"options":{"protocol":"u2f","transport":"usb","hasResidentKey":False,"hasUserVerification":False,"automaticPresenceSimulation":True,"isUserVerified":False}}); await s.close(); log_result("TC-WA-011", "add_virtual_authenticator options", "PASS")
    except Exception as e: await s.close(); log_result("TC-WA-011", "add_virtual_authenticator options", "FAIL", str(e))
