"""E2E tests for the Performance domain (real browser flows).

Full end-to-end flows against a real Chrome browser, including
complete lifecycle, navigation with JS, raw command sending,
and edge cases.
"""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError

_VERR = "time_domain must be 'timeTicks' or 'threadTicks'"


async def _wait_for_page(page: CDPSession) -> str:
    await page.page.enable()
    nav_result = await page.page.navigate("https://example.com")
    frame_id = nav_result.get("frameId", "")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True,
        )
        if result.get("result", {}).get("value"):
            break
    return frame_id


async def _run_heavy_js(page: CDPSession) -> None:
    await page.runtime.enable()
    await page.runtime.evaluate(
        """
        new Promise((resolve) => {
            const arr = [];
            for (let i = 0; i < 100000; i++) {
                arr.push({ id: i, name: 'item' + i, data: new Array(10).fill(i) });
            }
            const json = JSON.stringify(arr);
            JSON.parse(json);
            resolve('done');
        })
        """,
        return_by_value=True,
        await_promise=True,
    )


@pytest.mark.e2e
class TestPerformanceE2E:
    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result1 = await session.performance.get_metrics()
            assert "metrics" in result1
            await session.performance.disable()
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            result2 = await session.performance.get_metrics()
            assert "metrics" in result2
            await session.performance.disable()

    async def test_navigate_heavy_js_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            await _run_heavy_js(session)
            result = await session.performance.get_metrics()
            assert "metrics" in result
            assert len(result["metrics"]) > 0
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in names
            await session.performance.disable()

    async def test_set_time_domain_before_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
            await session.performance.disable()

    async def test_set_time_domain_after_enable_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            with pytest.raises(CommandError):
                await session.performance.set_time_domain("timeTicks")
            await session.performance.disable()

    async def test_get_metrics_multiple_times(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result1 = await session.performance.get_metrics()
            await asyncio.sleep(0.5)
            result2 = await session.performance.get_metrics()
            assert "metrics" in result1
            assert "metrics" in result2
            v1 = next(
                (m["value"] for m in result1["metrics"] if m["name"] == "JSHeapUsedSize"),
                None,
            )
            v2 = next(
                (m["value"] for m in result2["metrics"] if m["name"] == "JSHeapUsedSize"),
                None,
            )
            if v1 is not None and v2 is not None:
                assert v1 > 0
                assert v2 > 0
            await session.performance.disable()

    async def test_raw_send_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("Performance.enable")
            await session.send("Performance.disable")

    async def test_raw_send_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send("Performance.enable")
            result = await session.send("Performance.getMetrics")
            assert "metrics" in result
            await session.send("Performance.disable")

    async def test_raw_send_set_time_domain(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send(
                "Performance.setTimeDomain",
                {"timeDomain": "timeTicks"},
            )
            await session.send("Performance.enable")
            await session.send("Performance.disable")

    async def test_raw_send_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("Performance.enable")
            await session.send("Performance.disable")

    async def test_set_time_domain_invalid_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.performance.set_time_domain("invalidValue")

    async def test_all_methods_return_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            assert isinstance(await session.performance.set_time_domain("timeTicks"), dict)
            assert isinstance(await session.performance.enable(), dict)
            assert isinstance(await session.performance.get_metrics(), dict)
            assert isinstance(await session.performance.disable(), dict)

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.performance.enable()
            assert isinstance(result, dict)
            await session.performance.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            result = await session.performance.disable()
            assert isinstance(result, dict)

    async def test_get_metrics_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert isinstance(result, dict)
            await session.performance.disable()

    async def test_set_time_domain_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.performance.set_time_domain("timeTicks")
            assert isinstance(result, dict)

    async def test_enable_with_time_domain_time_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable(time_domain="timeTicks")
            result = await session.performance.get_metrics()
            assert "metrics" in result
            await session.performance.disable()

    async def test_enable_with_time_domain_thread_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable(time_domain="threadTicks")
            result = await session.performance.get_metrics()
            assert "metrics" in result
            await session.performance.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.performance.enable()
                await session.performance.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            await session.performance.enable()
            await session.performance.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.disable()

    async def test_get_metrics_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.performance.get_metrics()
            assert "metrics" in result
            assert isinstance(result["metrics"], list)

    async def test_metrics_have_name_and_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            for metric in result["metrics"]:
                assert "name" in metric
                assert "value" in metric
                assert isinstance(metric["name"], str)
                assert isinstance(metric["value"], (int, float))
            await session.performance.disable()

    async def test_metrics_include_js_heap_and_nodes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in names
            assert "Nodes" in names
            await session.performance.disable()

    async def test_concurrent_enable_and_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await asyncio.gather(
                session.performance.enable(),
                session.performance.get_metrics(),
            )
            await session.performance.disable()

    async def test_full_lifecycle_with_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result1 = await session.performance.get_metrics()
            assert len(result1["metrics"]) > 0

            await _run_heavy_js(session)
            result2 = await session.performance.get_metrics()
            assert len(result2["metrics"]) > 0

            await session.performance.disable()

    async def test_set_time_domain_thread_ticks_before_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("threadTicks")
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
            await session.performance.disable()

    async def test_get_metrics_after_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            await session.performance.disable()
            result = await session.performance.get_metrics()
            assert "metrics" in result

    async def test_set_time_domain_none_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string"):
                await session.performance.set_time_domain(None)

    async def test_set_time_domain_int_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string"):
                await session.performance.set_time_domain(42)

    async def test_set_time_domain_list_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string"):
                await session.performance.set_time_domain(["timeTicks"])

    async def test_enable_int_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string or None"):
                await session.performance.enable(time_domain=42)

    async def test_enable_list_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string or None"):
                await session.performance.enable(time_domain=["timeTicks"])

    async def test_enable_bool_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string or None"):
                await session.performance.enable(time_domain=True)

    async def test_enable_none_does_not_raise(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable(time_domain=None)
            await session.performance.disable()

    async def test_enable_invalid_value_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.performance.enable(time_domain="wallTime")

    async def test_set_time_domain_empty_string_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.performance.set_time_domain("")

    async def test_full_lifecycle_with_set_time_domain_first(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            r1 = await session.performance.get_metrics()
            assert len(r1["metrics"]) > 0
            await session.performance.disable()
            await session.performance.set_time_domain("threadTicks")
            await session.performance.enable()
            r2 = await session.performance.get_metrics()
            assert len(r2["metrics"]) > 0
            await session.performance.disable()

    async def test_get_metrics_after_heavy_js_heap_grows(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            r1 = await session.performance.get_metrics()
            await _run_heavy_js(session)
            await asyncio.sleep(0.5)
            r2 = await session.performance.get_metrics()
            assert len(r1["metrics"]) > 0
            assert len(r2["metrics"]) > 0
            heap1 = next(
                (m["value"] for m in r1["metrics"] if m["name"] == "JSHeapUsedSize"),
                0,
            )
            heap2 = next(
                (m["value"] for m in r2["metrics"] if m["name"] == "JSHeapUsedSize"),
                0,
            )
            assert heap2 >= heap1
            await session.performance.disable()

    async def test_enable_with_empty_string_time_domain(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable(time_domain="")
            result = await session.performance.get_metrics()
            assert "metrics" in result
            await session.performance.disable()

    async def test_enable_disable_enable_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            await session.performance.disable()
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
            assert len(result["metrics"]) > 0
            await session.performance.disable()

    async def test_concurrent_get_metrics_5x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            results = await asyncio.gather(
                *[session.performance.get_metrics() for _ in range(5)],
            )
            for r in results:
                assert "metrics" in r
                assert len(r["metrics"]) > 0
            await session.performance.disable()

    async def test_concurrent_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await asyncio.gather(
                session.performance.enable(),
                session.performance.disable(),
            )

    async def test_raw_send_enable_with_time_domain(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send(
                "Performance.enable",
                {"timeDomain": "timeTicks"},
            )
            result = await session.send("Performance.getMetrics")
            assert "metrics" in result
            await session.send("Performance.disable")

    async def test_raw_send_set_time_domain_thread_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send(
                "Performance.setTimeDomain",
                {"timeDomain": "threadTicks"},
            )
            await session.send("Performance.enable")
            await session.send("Performance.disable")

    async def test_get_metrics_has_js_heap_total_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapTotalSize" in names
            await session.performance.disable()

    async def test_get_metrics_has_event_listeners(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            names = [m["name"] for m in result["metrics"]]
            assert "JSEventListeners" in names
            await session.performance.disable()

    async def test_metrics_count_at_least_5(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert len(result["metrics"]) >= 5
            await session.performance.disable()

    async def test_repeated_enable_5x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(5):
                await session.performance.enable()
            await session.performance.disable()

    async def test_repeated_disable_5x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            for _ in range(5):
                await session.performance.disable()

    async def test_enable_with_time_domain_then_set_time_domain_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable(time_domain="timeTicks")
            with pytest.raises(CommandError):
                await session.performance.set_time_domain("threadTicks")
            await session.performance.disable()

    async def test_get_metrics_jsheap_used_size_positive(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            heap = next(
                (m for m in result["metrics"] if m["name"] == "JSHeapUsedSize"),
                None,
            )
            assert heap is not None
            assert heap["value"] > 0
            await session.performance.disable()

    async def test_get_metrics_nodes_positive(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            nodes = next(
                (m for m in result["metrics"] if m["name"] == "Nodes"),
                None,
            )
            assert nodes is not None
            assert nodes["value"] > 0
            await session.performance.disable()

    async def test_full_cycle_with_navigation_and_heavy_js(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            r1 = await session.performance.get_metrics()
            assert len(r1["metrics"]) > 0
            await _run_heavy_js(session)
            r2 = await session.performance.get_metrics()
            assert len(r2["metrics"]) > 0
            await session.performance.disable()
            assert isinstance(r1, dict)
            assert isinstance(r2, dict)

    async def test_set_time_domain_thread_ticks_full_flow(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("threadTicks")
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert len(result["metrics"]) > 0
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in names
            assert "Nodes" in names
            await session.performance.disable()
