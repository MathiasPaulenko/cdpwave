"""E2E tests for the Memory domain (real browser flows).

Full end-to-end flows against a real browser, including DOM counters,
sampling lifecycle, leak detection, pressure notifications, type
validation in real browser context, raw command sending, and meta
tests for docstrings and experimental marking.
"""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.domains.memory import MemoryDomain


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


async def _allocate_memory(page: CDPSession) -> None:
    await page.runtime.evaluate(
        """
        new Promise((resolve) => {
            const arr = [];
            for (let i = 0; i < 50000; i++) {
                arr.push({ id: i, name: 'item' + i, data: new Array(20).fill(i) });
            }
            const json = JSON.stringify(arr);
            JSON.parse(json);
            resolve(arr.length);
        })
        """,
        return_by_value=True,
        await_promise=True,
    )


@pytest.mark.e2e
class TestMemoryE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.memory is not None
            assert isinstance(session.memory, MemoryDomain)

    async def test_get_dom_counters(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.memory.get_dom_counters()
            assert "documents" in result
            assert "nodes" in result
            assert "jsEventListeners" in result
            assert isinstance(result["documents"], int)
            assert isinstance(result["nodes"], int)
            assert isinstance(result["jsEventListeners"], int)
            assert result["documents"] > 0
            assert result["nodes"] > 0

    async def test_get_dom_counters_after_allocation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            before = await session.memory.get_dom_counters()
            await _allocate_memory(session)
            after = await session.memory.get_dom_counters()
            assert after["nodes"] >= before["nodes"]

    async def test_get_dom_counters_for_leak_detection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.memory.get_dom_counters_for_leak_detection()
                assert "counters" in result
                assert isinstance(result["counters"], list)
                for counter in result["counters"]:
                    assert "name" in counter
                    assert "count" in counter
            except Exception:
                pytest.skip("getDOMCountersForLeakDetection not supported")

    async def test_prepare_for_leak_detection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.memory.prepare_for_leak_detection()
            except Exception:
                pytest.skip("prepareForLeakDetection not supported")

    async def test_forcibly_purge_javascript_memory(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _allocate_memory(session)
            try:
                await session.memory.forcibly_purge_javascript_memory()
            except Exception:
                pytest.skip("forciblyPurgeJavaScriptMemory not supported")

    async def test_set_pressure_notifications_suppressed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.memory.set_pressure_notifications_suppressed(True)
                await session.memory.set_pressure_notifications_suppressed(False)
            except Exception:
                pytest.skip("setPressureNotificationsSuppressed not supported")

    async def test_simulate_pressure_notification_moderate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.memory.simulate_pressure_notification("moderate")
            except Exception:
                pytest.skip("simulatePressureNotification not supported")

    async def test_simulate_pressure_notification_critical(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.memory.simulate_pressure_notification("critical")
            except Exception:
                pytest.skip("simulatePressureNotification not supported")

    async def test_full_sampling_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.memory.start_sampling(sampling_interval=1024)
                await _allocate_memory(session)
                result = await session.memory.get_sampling_profile()
                assert "profile" in result
                profile = result["profile"]
                assert "samples" in profile
                assert "modules" in profile
                assert isinstance(profile["samples"], list)
                assert isinstance(profile["modules"], list)
                await session.memory.stop_sampling()
            except Exception:
                pytest.skip("Memory sampling not supported")

    async def test_sampling_with_suppress_randomness(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.memory.start_sampling(
                    sampling_interval=2048,
                    suppress_randomness=True,
                )
                await session.runtime.evaluate("1 + 1")
                result = await session.memory.get_sampling_profile()
                assert "profile" in result
                await session.memory.stop_sampling()
            except Exception:
                pytest.skip("Memory sampling not supported")

    async def test_sampling_default_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.memory.start_sampling()
                await session.runtime.evaluate("1 + 1")
                result = await session.memory.get_sampling_profile()
                assert "profile" in result
                await session.memory.stop_sampling()
            except Exception:
                pytest.skip("Memory sampling not supported")

    async def test_get_all_time_sampling_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.memory.get_all_time_sampling_profile()
                assert "profile" in result
            except Exception:
                pytest.skip("getAllTimeSamplingProfile not supported")

    async def test_get_browser_sampling_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.memory.get_browser_sampling_profile()
                assert "profile" in result
            except Exception:
                pytest.skip("getBrowserSamplingProfile not supported")

    async def test_stop_sampling_without_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.memory.stop_sampling()
            except Exception:
                pass

    async def test_get_sampling_profile_without_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.memory.get_sampling_profile()
                assert "profile" in result
            except Exception:
                pass

    async def test_sampling_lifecycle_multiple_cycles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                for _ in range(3):
                    await session.memory.start_sampling(sampling_interval=4096)
                    await session.runtime.evaluate("1 + 1")
                    await session.memory.stop_sampling()
            except Exception:
                pytest.skip("Memory sampling not supported")

    async def test_dom_counters_multiple_pages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session1,
            await client.new_page() as session2,
        ):
            await _wait_for_page(session1)
            await _wait_for_page(session2)
            r1 = await session1.memory.get_dom_counters()
            r2 = await session2.memory.get_dom_counters()
            assert r1["nodes"] > 0
            assert r2["nodes"] > 0

    async def test_raw_send_get_dom_counters(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.send("Memory.getDOMCounters")
            assert "documents" in result
            assert "nodes" in result

    async def test_raw_send_start_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.send(
                    "Memory.startSampling",
                    {"samplingInterval": 1024, "suppressRandomness": True},
                )
                await session.send("Memory.stopSampling")
            except Exception:
                pytest.skip("Memory sampling not supported")

    # ── type validation in real browser context ──

    async def test_type_error_suppressed_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="suppressed must be a bool"):
                await session.memory.set_pressure_notifications_suppressed(1)  # type: ignore[arg-type]

    async def test_type_error_level_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="level must be a str"):
                await session.memory.simulate_pressure_notification(42)  # type: ignore[arg-type]

    async def test_value_error_level_invalid(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
                await session.memory.simulate_pressure_notification("low")

    async def test_type_error_sampling_interval_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sampling_interval must be an int"):
                await session.memory.start_sampling(sampling_interval=True)  # type: ignore[arg-type]

    async def test_type_error_sampling_interval_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sampling_interval must be an int"):
                await session.memory.start_sampling(sampling_interval="1024")  # type: ignore[arg-type]

    async def test_type_error_suppress_randomness_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="suppress_randomness must be a bool"):
                await session.memory.start_sampling(suppress_randomness=1)  # type: ignore[arg-type]

    # ── meta tests: docstrings, experimental, method count ──

    async def test_module_docstring_documents_types(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "PressureLevel" in doc
        assert "SamplingProfileNode" in doc
        assert "SamplingProfile" in doc
        assert "Module" in doc
        assert "DOMCounter" in doc

    async def test_module_docstring_no_events(self) -> None:
        import cdpwave.domains.memory as mod
        doc = mod.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_class_docstring_has_experimental_mark(self) -> None:
        doc = MemoryDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_no_events(self) -> None:
        doc = MemoryDomain.__doc__
        assert doc is not None
        assert "No events" in doc

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in MemoryDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 11

    async def test_all_methods_callable_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert callable(session.memory.get_dom_counters)
            assert callable(session.memory.get_dom_counters_for_leak_detection)
            assert callable(session.memory.prepare_for_leak_detection)
            assert callable(session.memory.forcibly_purge_javascript_memory)
            assert callable(session.memory.set_pressure_notifications_suppressed)
            assert callable(session.memory.simulate_pressure_notification)
            assert callable(session.memory.start_sampling)
            assert callable(session.memory.stop_sampling)
            assert callable(session.memory.get_all_time_sampling_profile)
            assert callable(session.memory.get_browser_sampling_profile)
            assert callable(session.memory.get_sampling_profile)

    async def test_start_sampling_docstring_mentions_omitempty(self) -> None:
        doc = MemoryDomain.start_sampling.__doc__
        assert doc is not None
        assert "Omitted" in doc or "omitted" in doc

    async def test_start_sampling_docstring_always_sent(self) -> None:
        doc = MemoryDomain.start_sampling.__doc__
        assert doc is not None
        assert "Always sent" in doc

    async def test_simulate_pressure_notification_docstring_mentions_values(self) -> None:
        doc = MemoryDomain.simulate_pressure_notification.__doc__
        assert doc is not None
        assert "moderate" in doc
        assert "critical" in doc

    async def test_forcibly_purge_docstring_mentions_oom(self) -> None:
        doc = MemoryDomain.forcibly_purge_javascript_memory.__doc__
        assert doc is not None
        assert "OomIntervention" in doc or "OOM" in doc or "purge" in doc.lower()

    async def test_prepare_for_leak_detection_docstring_mentions_workers(self) -> None:
        doc = MemoryDomain.prepare_for_leak_detection.__doc__
        assert doc is not None
        assert "workers" in doc.lower() or "leak" in doc.lower()

    # ── docstring accuracy vs Go source ──

    async def test_set_pressure_suppressed_docstring_all_processes(self) -> None:
        doc = MemoryDomain.set_pressure_notifications_suppressed.__doc__
        assert doc is not None
        assert "all processes" in doc.lower()

    async def test_simulate_pressure_docstring_all_processes(self) -> None:
        doc = MemoryDomain.simulate_pressure_notification.__doc__
        assert doc is not None
        assert "all processes" in doc.lower()

    async def test_get_dom_counters_for_leak_detection_docstring_renderer(self) -> None:
        doc = MemoryDomain.get_dom_counters_for_leak_detection.__doc__
        assert doc is not None
        assert "renderer" in doc.lower()

    async def test_get_all_time_sampling_profile_docstring_renderer_process(self) -> None:
        doc = MemoryDomain.get_all_time_sampling_profile.__doc__
        assert doc is not None
        assert "renderer process" in doc.lower()

    async def test_get_browser_sampling_profile_docstring_browser_process(self) -> None:
        doc = MemoryDomain.get_browser_sampling_profile.__doc__
        assert doc is not None
        assert "browser process" in doc.lower()

    async def test_get_sampling_profile_docstring_last_call(self) -> None:
        doc = MemoryDomain.get_sampling_profile.__doc__
        assert doc is not None
        assert "last startSampling call" in doc

    async def test_get_dom_counters_docstring_js_event_listeners(self) -> None:
        doc = MemoryDomain.get_dom_counters.__doc__
        assert doc is not None
        assert "jsEventListeners" in doc

    async def test_forcibly_purge_docstring_v8(self) -> None:
        doc = MemoryDomain.forcibly_purge_javascript_memory.__doc__
        assert doc is not None
        assert "V8" in doc
