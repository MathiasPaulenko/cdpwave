"""Manual smoke test for cdpwave — exercises all major features against a real browser.

Usage:
    python -m tests.manual_smoke

Or:
    python tests/manual_smoke.py

This script launches a headless Chrome, runs through every major feature,
and prints a PASS/FAIL summary. It does NOT use pytest — it's meant for
manual verification before releases.
"""

from __future__ import annotations

import asyncio
import base64
import sys
import traceback
from dataclasses import dataclass, field

from cdpwave import CDPClient, CDPSession


@dataclass
class Result:
    name: str
    passed: bool
    detail: str = ""
    error: str = ""


@dataclass
class SmokeReport:
    results: list[Result] = field(default_factory=list)

    def add(self, name: str, detail: str = "", error: str = "") -> None:
        self.results.append(
            Result(name=name, passed=not error, detail=detail, error=error)
        )

    def print_summary(self) -> bool:
        print("\n" + "=" * 70)
        print("  cdpwave manual smoke test — results")
        print("=" * 70)
        passed = 0
        failed = 0
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            line = f"  [{status}] {r.name}"
            if r.detail:
                line += f" — {r.detail}"
            if r.error:
                line += f"\n         ERROR: {r.error}"
            print(line)
            if r.passed:
                passed += 1
            else:
                failed += 1
        print("=" * 70)
        print(f"  {passed} passed, {failed} failed, {passed + failed} total")
        print("=" * 70 + "\n")
        return failed == 0


async def test_launch_and_connect(report: SmokeReport) -> CDPClient:
    """Test 1: Launch browser via CDPClient.launch()."""
    try:
        client = await CDPClient.launch(headless=True)
        ver = await client.browser.get_version()
        report.add("launch", f"browser launched, version={ver.get('product', '')}")
        return client
    except Exception:
        report.add("launch", error=traceback.format_exc())
        raise


async def test_version(report: SmokeReport, client: CDPClient) -> None:
    """Test 2: Browser.get_version via escape hatch."""
    try:
        result = await client.send("Browser.getVersion")
        protocol = result.get("protocolVersion", "")
        product = result.get("product", "")
        report.add("browser.get_version", f"protocol={protocol}, product={product}")
    except Exception:
        report.add("browser.get_version", error=traceback.format_exc())


async def test_new_page_and_navigation(
    report: SmokeReport, client: CDPClient
) -> CDPSession:
    """Test 3: Create a new page and navigate."""
    try:
        session = await client.new_page()
        await session.page.enable()
        await session.runtime.enable()

        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired", timeout=15)
        report.add("new_page + navigate", "navigated to example.com, loadEventFired received")
        return session
    except Exception:
        report.add("new_page + navigate", error=traceback.format_exc())
        raise


async def test_wait_for_event(report: SmokeReport, session: CDPSession) -> None:
    """Test 4: wait_for_event helper (already used in test 3, but verify explicitly)."""
    try:
        await session.page.navigate("https://example.com")
        params = await session.wait_for_event("Page.loadEventFired", timeout=15)
        report.add(
            "wait_for_event",
            f"received Page.loadEventFired, params keys={list(params.keys())}",
        )
    except Exception:
        report.add("wait_for_event", error=traceback.format_exc())


async def test_js_evaluation(report: SmokeReport, session: CDPSession) -> None:
    """Test 5: Runtime.evaluate."""
    try:
        result = await session.runtime.evaluate("1 + 2 + 3")
        value = result.get("result", {}).get("value")
        assert value == 6, f"Expected 6, got {value}"
        report.add("runtime.evaluate", f"1+2+3 = {value}")
    except Exception:
        report.add("runtime.evaluate", error=traceback.format_exc())


async def test_js_object(report: SmokeReport, session: CDPSession) -> None:
    """Test 6: Remote objects — evaluate, get properties, release."""
    try:
        result = await session.runtime.evaluate(
            "({name: 'cdpwave', version: 2, features: ['cdp', 'async', 'browser']})",
            return_by_value=False,
        )
        object_id = result.get("result", {}).get("objectId")
        assert object_id, "No objectId returned"

        props = await session.runtime.get_properties(object_id)
        prop_names = [p.get("name") for p in props.get("result", [])]
        assert "name" in prop_names, f"name not in {prop_names}"

        await session.runtime.release_object(object_id)
        report.add("remote_objects", f"properties={prop_names}, released OK")
    except Exception:
        report.add("remote_objects", error=traceback.format_exc())


async def test_dom_inspection(report: SmokeReport, session: CDPSession) -> None:
    """Test 7: DOM.getDocument + querySelector."""
    try:
        await session.dom.enable()
        doc = await session.dom.get_document(depth=1)
        root_node = doc.get("root", {})
        node_name = root_node.get("nodeName", "")
        assert node_name == "#document", f"Expected #document, got {node_name}"

        title_result = await session.runtime.evaluate(
            "document.title",
            return_by_value=True,
        )
        title = title_result.get("result", {}).get("value", "")
        report.add("dom_inspection", f"root={node_name}, title='{title}'")
    except Exception:
        report.add("dom_inspection", error=traceback.format_exc())


async def test_screenshot(report: SmokeReport, session: CDPSession) -> None:
    """Test 8: Page.captureScreenshot (tests max_size=None fix)."""
    try:
        result = await session.page.capture_screenshot(format="png")
        data = result.get("data", "")
        assert len(data) > 100, f"Screenshot data too small: {len(data)} bytes"
        decoded = base64.b64decode(data)
        assert len(decoded) > 1000, f"Decoded screenshot too small: {len(decoded)} bytes"
        assert decoded[:8] == b"\x89PNG\r\n\x1a\n", "Not a valid PNG"
        report.add("screenshot", f"PNG {len(decoded)} bytes (base64 {len(data)} chars)")
    except Exception:
        report.add("screenshot", error=traceback.format_exc())


async def test_pdf(report: SmokeReport, session: CDPSession) -> None:
    """Test 9: Page.printToPDF."""
    try:
        result = await session.page.print_to_pdf()
        data = result.get("data", "")
        assert len(data) > 100, f"PDF data too small: {len(data)} bytes"
        decoded = base64.b64decode(data)
        assert decoded[:4] == b"%PDF", "Not a valid PDF"
        report.add("print_to_pdf", f"PDF {len(decoded)} bytes")
    except Exception:
        report.add("print_to_pdf", error=traceback.format_exc())


async def test_network_monitoring(report: SmokeReport, session: CDPSession) -> None:
    """Test 10: Network.enable + request events."""
    try:
        requests_seen: list[str] = []

        async def on_request(params: dict) -> None:
            url = params.get("request", {}).get("url", "")
            if url:
                requests_seen.append(url)

        await session.network.enable()
        session.on("Network.requestWillBeSent", on_request)

        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired", timeout=15)

        assert len(requests_seen) > 0, "No requests captured"
        has_example = any("example.com" in r for r in requests_seen)
        assert has_example, f"example.com not in requests: {requests_seen[:5]}"
        report.add("network_monitoring", f"{len(requests_seen)} requests captured")
    except Exception:
        report.add("network_monitoring", error=traceback.format_exc())


async def test_cookies(report: SmokeReport, session: CDPSession) -> None:
    """Test 11: Network.setCookie + getCookies."""
    try:
        await session.network.set_cookie(
            name="test_cookie",
            value="cdpwave_smoke",
            domain="example.com",
            path="/",
        )
        cookies = await session.network.get_cookies(urls=["https://example.com"])
        cookie_list = cookies.get("cookies", [])
        found = any(c.get("name") == "test_cookie" for c in cookie_list)
        assert found, f"test_cookie not found in {len(cookie_list)} cookies"
        report.add("cookies", f"set + get cookie OK, {len(cookie_list)} total cookies")
    except Exception:
        report.add("cookies", error=traceback.format_exc())


async def test_emulation(report: SmokeReport, session: CDPSession) -> None:
    """Test 12: Emulation.setDeviceMetricsOverride + clear."""
    try:
        await session.emulation.set_device_metrics_override(
            width=375,
            height=667,
            device_scale_factor=2.0,
            mobile=True,
        )
        metrics = await session.page.get_layout_metrics()
        vw = metrics.get("cssLayoutViewport", {}).get("clientWidth", 0)
        assert vw == 375, f"Expected width 375, got {vw}"

        await session.emulation.clear_device_metrics_override()
        report.add("emulation", f"device metrics 375x667 applied, viewport width={vw}")
    except Exception:
        report.add("emulation", error=traceback.format_exc())


async def test_input_keyboard(report: SmokeReport, session: CDPSession) -> None:
    """Test 13: Input.insertText — type into an input field."""
    try:
        await session.page.navigate("data:text/html,<input id='q' type='text' autofocus>")
        await asyncio.sleep(0.5)
        await session.runtime.evaluate("document.getElementById('q').focus()")
        await session.input.insert_text("ab")

        value = await session.runtime.evaluate(
            "document.getElementById('q').value",
            return_by_value=True,
        )
        val = value.get("result", {}).get("value", "")
        assert val == "ab", f"Expected 'ab', got '{val}'"
        report.add("input_keyboard", f"inserted 'ab' into input, value='{val}'")
    except Exception:
        report.add("input_keyboard", error=traceback.format_exc())


async def test_performance_metrics(report: SmokeReport, session: CDPSession) -> None:
    """Test 14: Performance.enable + getMetrics."""
    try:
        await session.performance.enable()
        metrics = await session.performance.get_metrics()
        metric_list = metrics.get("metrics", [])
        names = [m.get("name") for m in metric_list]
        assert "JSHeapUsedSize" in names, f"JSHeapUsedSize not in {names}"
        report.add("performance_metrics", f"{len(metric_list)} metrics, has JSHeapUsedSize")
    except Exception:
        report.add("performance_metrics", error=traceback.format_exc())


async def test_profiler(report: SmokeReport, session: CDPSession) -> None:
    """Test 15: Profiler.start + stop (CPU profile)."""
    try:
        await session.profiler.enable()
        await session.profiler.start()
        await session.runtime.evaluate("Math.sqrt(12345.6789) * Math.PI")
        result = await session.profiler.stop()
        profile = result.get("profile", {})
        nodes = profile.get("nodes", [])
        assert len(nodes) > 0, "No profile nodes"
        report.add("profiler", f"CPU profile with {len(nodes)} nodes")
    except Exception:
        report.add("profiler", error=traceback.format_exc())


async def test_heap_profiler(report: SmokeReport, session: CDPSession) -> None:
    """Test 16: HeapProfiler.takeHeapSnapshot (tests max_size=None with large data)."""
    try:
        await session.heap_profiler.enable()
        await session.heap_profiler.take_heap_snapshot()
        report.add("heap_profiler", "heap snapshot taken OK")
    except Exception:
        report.add("heap_profiler", error=traceback.format_exc())


async def test_log_domain(report: SmokeReport, session: CDPSession) -> None:
    """Test 17: Log.enable + console entry via Runtime."""
    try:
        log_entries: list[str] = []
        console_entries: list[str] = []

        async def on_log_entry(params: dict) -> None:
            entry = params.get("entry", {})
            log_entries.append(entry.get("text", ""))

        async def on_console_api(params: dict) -> None:
            args = params.get("args", [])
            text = " ".join(str(a.get("value", a.get("description", ""))) for a in args)
            console_entries.append(text)

        await session.log.enable()
        session.on("Log.entryAdded", on_log_entry)
        session.on("Runtime.consoleAPICalled", on_console_api)

        await session.runtime.evaluate("console.log('cdpwave smoke test log')")
        await asyncio.sleep(1.0)

        all_entries = log_entries + console_entries
        assert any("cdpwave" in e for e in all_entries), f"No matching log entry in {all_entries}"
        source = "Log.entryAdded" if log_entries else "Runtime.consoleAPICalled"
        report.add("log_domain", f"captured via {source}: {all_entries}")
    except Exception:
        report.add("log_domain", error=traceback.format_exc())


async def test_fetch_interception(report: SmokeReport, session: CDPSession) -> None:
    """Test 18: Fetch.enable + continueRequest."""
    try:
        intercepted: list[str] = []

        async def on_paused(params: dict) -> None:
            req_id = params.get("requestId", "")
            url = params.get("request", {}).get("url", "")
            intercepted.append(url)
            await session.fetch.continue_request(request_id=req_id)

        await session.fetch.enable(
            patterns=[{"urlPattern": "*example.com*", "requestStage": "Request"}],
        )
        session.on("Fetch.requestPaused", on_paused)

        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired", timeout=15)

        assert len(intercepted) > 0, "No requests intercepted"
        report.add("fetch_interception", f"{len(intercepted)} requests intercepted + continued")
    except Exception:
        report.add("fetch_interception", error=traceback.format_exc())


async def test_multi_tab(report: SmokeReport, client: CDPClient) -> None:
    """Test 19: Multiple tabs via new_page + sessions property."""
    try:
        tab1 = await client.new_page("https://example.com")
        await tab1.page.enable()
        await tab1.runtime.enable()
        await tab1.page.navigate("https://example.com")
        await tab1.wait_for_event("Page.loadEventFired", timeout=15)

        tab2 = await client.new_page("https://www.iana.org/domains/reserved")
        await tab2.page.enable()
        await tab2.runtime.enable()
        await tab2.page.navigate("https://www.iana.org/domains/reserved")
        await tab2.wait_for_event("Page.loadEventFired", timeout=15)

        sessions = client.sessions
        assert len(sessions) >= 2, f"Expected >=2 sessions, got {len(sessions)}"

        title1 = await tab1.runtime.evaluate("document.title", return_by_value=True)
        title2 = await tab2.runtime.evaluate("document.title", return_by_value=True)
        t1 = title1.get("result", {}).get("value", "")
        t2 = title2.get("result", {}).get("value", "")

        await tab1.close()
        await tab2.close()

        remaining = client.sessions
        assert len(remaining) < len(sessions), "Sessions not removed after close"

        report.add(
            "multi_tab",
            f"tab1='{t1}', tab2='{t2}', sessions before={len(sessions)}, after={len(remaining)}",
        )
    except Exception:
        report.add("multi_tab", error=traceback.format_exc())


async def test_target_cleanup(report: SmokeReport, client: CDPClient) -> None:
    """Test 20: Target is closed when session.close() is called (not just detached)."""
    try:
        session = await client.new_page("https://example.com")
        target_id = session._target_id

        targets_before = await client.get_pages()
        count_before = sum(1 for t in targets_before if t.target_id == target_id)
        assert count_before == 1, f"Target {target_id} not found before close"

        await session.close()
        await asyncio.sleep(0.5)

        targets_after = await client.get_pages()
        count_after = sum(1 for t in targets_after if t.target_id == target_id)
        assert count_after == 0, f"Target {target_id} still open after close"

        report.add(
            "target_cleanup",
            f"target closed on session.close() (before={count_before}, after={count_after})",
        )
    except Exception:
        report.add("target_cleanup", error=traceback.format_exc())


async def test_connect_ws_url(report: SmokeReport, client: CDPClient) -> None:
    """Test 21: CDPClient.connect(ws_url=...) — connect directly via WebSocket URL."""
    try:
        ws_url = client._connection._url
        client2 = await CDPClient.connect(ws_url=ws_url)
        assert client2.is_connected, "client2 not connected"
        session = await client2.new_page("https://example.com")
        await session.page.enable()
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired", timeout=15)
        title = await session.runtime.evaluate("document.title", return_by_value=True)
        t = title.get("result", {}).get("value", "")
        await session.close()
        await client2.close()
        report.add("connect_ws_url", f"connected via ws_url, title='{t}'")
    except Exception:
        report.add("connect_ws_url", error=traceback.format_exc())


async def test_security_domain(report: SmokeReport, session: CDPSession) -> None:
    """Test 22: Security.enable + security state events."""
    try:
        await session.security.enable()
        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired", timeout=15)
        report.add("security_domain", "enabled + navigated OK")
    except Exception:
        report.add("security_domain", error=traceback.format_exc())


async def test_storage_domain(report: SmokeReport, session: CDPSession) -> None:
    """Test 23: Storage.getCookies."""
    try:
        await session.network.set_cookie(
            name="storage_test",
            value="abc123",
            domain="example.com",
            path="/",
        )
        cookies = await session.storage.get_cookies()
        cookie_list = cookies.get("cookies", [])
        found = any(c.get("name") == "storage_test" for c in cookie_list)
        assert found, "storage_test cookie not found via Storage.getCookies"
        report.add("storage_domain", f"Storage.getCookies returned {len(cookie_list)} cookies")
    except Exception:
        report.add("storage_domain", error=traceback.format_exc())


async def test_system_info(report: SmokeReport, client: CDPClient) -> None:
    """Test 24: SystemInfo.getInfo."""
    try:
        result = await client.send("SystemInfo.getInfo")
        gpu = result.get("gpu", {}).get("devices", [])
        report.add("system_info", f"GPU devices: {len(gpu)}")
    except Exception:
        report.add("system_info", error=traceback.format_exc())


async def test_emulation_media(report: SmokeReport, session: CDPSession) -> None:
    """Test 25: Emulation.setEmulatedMedia (dark mode)."""
    try:
        await session.emulation.set_emulated_media(
            media="",
            features=[{"name": "prefers-color-scheme", "value": "dark"}],
        )
        result = await session.runtime.evaluate(
            "window.matchMedia('(prefers-color-scheme: dark)').matches",
            return_by_value=True,
        )
        is_dark = result.get("result", {}).get("value", False)
        assert is_dark is True, f"Expected dark mode, got {is_dark}"
        report.add("emulation_media", f"prefers-color-scheme=dark -> {is_dark}")
    except Exception:
        report.add("emulation_media", error=traceback.format_exc())


async def test_emulation_timezone(report: SmokeReport, session: CDPSession) -> None:
    """Test 26: Emulation.setTimezoneOverride."""
    try:
        await session.emulation.set_timezone_override("Asia/Tokyo")
        result = await session.runtime.evaluate(
            "Intl.DateTimeFormat().resolvedOptions().timeZone",
            return_by_value=True,
        )
        tz = result.get("result", {}).get("value", "")
        assert tz == "Asia/Tokyo", f"Expected Asia/Tokyo, got {tz}"
        await session.emulation.clear_timezone_override()
        report.add("emulation_timezone", f"timezone overridden to {tz}")
    except Exception:
        report.add("emulation_timezone", error=traceback.format_exc())


async def test_emulation_geolocation(report: SmokeReport, session: CDPSession) -> None:
    """Test 27: Emulation.setGeolocationOverride."""
    try:
        await session.emulation.set_geolocation_override(
            latitude=40.7128,
            longitude=-74.0060,
            accuracy=1.0,
        )
        await session.send("Browser.grantPermissions", {
            "permissions": ["geolocation"],
            "origin": "https://example.com",
        })
        result = await session.runtime.evaluate(
            """(function() {
                return new Promise((resolve) => {
                    navigator.geolocation.getCurrentPosition(
                        (p) => resolve({lat: p.coords.latitude, lng: p.coords.longitude}),
                        (e) => resolve({error: e.message})
                    );
                });
            })()""",
            return_by_value=True,
            await_promise=True,
        )
        coords = result.get("result", {}).get("value", {})
        lat = coords.get("lat", 0)
        lng = coords.get("lng", 0)
        if lat == 0 and lng == 0:
            err = coords.get("error", "unknown")
            report.add(
                "emulation_geolocation",
                error=f"Geolocation returned empty: {coords}, error={err}",
            )
        else:
            assert abs(lat - 40.7128) < 0.01, f"Expected lat ~40.7128, got {lat}"
            assert abs(lng - (-74.0060)) < 0.01, f"Expected lng ~-74.006, got {lng}"
            await session.emulation.clear_geolocation_override()
            report.add("emulation_geolocation", f"lat={lat}, lng={lng}")
    except Exception:
        report.add("emulation_geolocation", error=traceback.format_exc())


async def test_emulation_cpu_throttle(report: SmokeReport, session: CDPSession) -> None:
    """Test 28: Emulation.setCPUThrottlingRate."""
    try:
        await session.emulation.set_cpu_throttling_rate(rate=4.0)
        await session.emulation.set_cpu_throttling_rate(rate=1.0)
        report.add("emulation_cpu_throttle", "set 4x then reset to 1x OK")
    except Exception:
        report.add("emulation_cpu_throttle", error=traceback.format_exc())


async def test_emulation_user_agent(report: SmokeReport, session: CDPSession) -> None:
    """Test 29: Emulation.setUserAgentOverride."""
    try:
        custom_ua = "cdpwave-smoke-test/2.0 (like Gecko)"
        await session.emulation.set_user_agent_override(user_agent=custom_ua)
        result = await session.runtime.evaluate(
            "navigator.userAgent",
            return_by_value=True,
        )
        ua = result.get("result", {}).get("value", "")
        assert ua == custom_ua, f"Expected '{custom_ua}', got '{ua}'"
        report.add("emulation_user_agent", f"UA overridden to '{ua}'")
    except Exception:
        report.add("emulation_user_agent", error=traceback.format_exc())


async def test_page_lifecycle(report: SmokeReport, session: CDPSession) -> None:
    """Test 30: Page.setWebLifecycleState (freeze + active)."""
    try:
        await session.page.set_web_lifecycle_state("frozen")
        await session.page.set_web_lifecycle_state("active")
        report.add("page_lifecycle", "frozen -> active OK")
    except Exception:
        report.add("page_lifecycle", error=traceback.format_exc())


async def test_runtime_binding(report: SmokeReport, session: CDPSession) -> None:
    """Test 31: Runtime.addBinding + bindingCalled event."""
    try:
        binding_events: list[str] = []

        async def on_binding(params: dict) -> None:
            binding_events.append(params.get("payload", ""))

        await session.runtime.add_binding("smokeBinding")
        session.on("Runtime.bindingCalled", on_binding)

        await session.runtime.evaluate("window.smokeBinding('hello from JS')")
        await asyncio.sleep(0.5)

        assert any("hello" in e for e in binding_events), f"No binding event in {binding_events}"
        await session.runtime.remove_binding("smokeBinding")
        report.add("runtime_binding", f"binding called with: {binding_events}")
    except Exception:
        report.add("runtime_binding", error=traceback.format_exc())


async def test_page_bypass_csp(report: SmokeReport, session: CDPSession) -> None:
    """Test 32: Page.setBypassCSP."""
    try:
        await session.page.set_bypass_csp(enabled=True)
        await session.page.set_bypass_csp(enabled=False)
        report.add("page_bypass_csp", "enabled + disabled OK")
    except Exception:
        report.add("page_bypass_csp", error=traceback.format_exc())


async def test_network_emulation(report: SmokeReport, session: CDPSession) -> None:
    """Test 33: Network.emulateNetworkConditions."""
    try:
        await session.network.emulate_network_conditions(
            offline=False,
            latency=100,
            download_throughput=500_000,
            upload_throughput=500_000,
        )
        await session.network.emulate_network_conditions(
            offline=False,
            latency=0,
            download_throughput=-1,
            upload_throughput=-1,
        )
        report.add("network_emulation", "set 100ms latency then reset OK")
    except Exception:
        report.add("network_emulation", error=traceback.format_exc())


async def test_network_block_urls(report: SmokeReport, session: CDPSession) -> None:
    """Test 34: Network.setBlockedURLs."""
    try:
        await session.network.set_blocked_urls(["*.css"])
        await session.network.set_blocked_urls([])
        report.add("network_block_urls", "block *.css then clear OK")
    except Exception:
        report.add("network_block_urls", error=traceback.format_exc())


async def main() -> int:
    report = SmokeReport()

    print("\n  cdpwave manual smoke test")
    print("  Launching headless Chrome and testing all major features...\n")

    try:
        client = await test_launch_and_connect(report)
    except Exception:
        report.print_summary()
        return 1

    await test_version(report, client)

    try:
        session = await test_new_page_and_navigation(report, client)
    except Exception:
        await client.close()
        report.print_summary()
        return 1

    # Core features
    await test_wait_for_event(report, session)
    await test_js_evaluation(report, session)
    await test_js_object(report, session)
    await test_dom_inspection(report, session)
    await test_screenshot(report, session)
    await test_pdf(report, session)
    await test_network_monitoring(report, session)
    await test_cookies(report, session)

    # Emulation
    await test_emulation(report, session)
    await test_emulation_media(report, session)
    await test_emulation_timezone(report, session)
    await test_emulation_geolocation(report, session)
    await test_emulation_cpu_throttle(report, session)
    await test_emulation_user_agent(report, session)

    # Input
    await test_input_keyboard(report, session)

    # Performance & profiling
    await test_performance_metrics(report, session)
    await test_profiler(report, session)
    await test_heap_profiler(report, session)

    # Log & security
    await test_log_domain(report, session)
    await test_security_domain(report, session)

    # Storage
    await test_storage_domain(report, session)

    # Runtime bindings
    await test_runtime_binding(report, session)

    # Page features
    await test_page_lifecycle(report, session)
    await test_page_bypass_csp(report, session)

    # Network features
    await test_network_emulation(report, session)
    await test_network_block_urls(report, session)

    # Fetch interception (run last on this session as it modifies state)
    await test_fetch_interception(report, session)

    # Close the first session
    await session.close()

    # Multi-tab + sessions property
    await test_multi_tab(report, client)

    # Target cleanup
    await test_target_cleanup(report, client)

    # System info (browser-level)
    await test_system_info(report, client)

    # Connect via ws_url
    await test_connect_ws_url(report, client)

    # Cleanup
    await client.close()

    all_passed = report.print_summary()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
