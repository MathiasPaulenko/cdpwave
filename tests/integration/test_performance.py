"""Integration tests for the Performance domain (real browser).

Exercises all Performance domain methods against a real Chrome browser,
including enable/disable, getMetrics, setTimeDomain, raw send,
concurrency, and edge cases.
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


@pytest.mark.integration
class TestPerformanceIntegration:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            await session.performance.disable()

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

    async def test_get_metrics_after_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
            assert isinstance(result["metrics"], list)
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in names
            await session.performance.disable()

    async def test_get_metrics_has_name_and_value(self) -> None:
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

    async def test_get_metrics_includes_nodes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            names = [m["name"] for m in result["metrics"]]
            assert "Nodes" in names
            await session.performance.disable()

    async def test_set_time_domain_time_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            await session.performance.disable()

    async def test_set_time_domain_thread_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.set_time_domain("threadTicks")
            await session.performance.enable()
            await session.performance.disable()

    async def test_set_time_domain_before_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
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
            await session.performance.enable()
            with pytest.raises(CommandError):
                await session.performance.set_time_domain("timeTicks")
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

    async def test_enable_repeated_10x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(10):
                await session.performance.enable()
            await session.performance.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
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

    async def test_disable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            await session.performance.disable()
            await session.performance.disable()

    async def test_set_time_domain_invalid_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.performance.set_time_domain("invalidValue")

    async def test_get_metrics_returns_dict_after_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            await session.performance.get_metrics()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1)
            result = await session.performance.get_metrics()
            assert isinstance(result, dict)
            assert "metrics" in result
            await session.performance.disable()

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
                await session.performance.set_time_domain(123)

    async def test_enable_int_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="time_domain must be a string or None"):
                await session.performance.enable(time_domain=123)

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

    async def test_set_time_domain_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.performance.set_time_domain("")

    async def test_get_metrics_metrics_are_dicts(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            for metric in result["metrics"]:
                assert isinstance(metric, dict)
            await session.performance.disable()

    async def test_get_metrics_names_are_strings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            for metric in result["metrics"]:
                assert isinstance(metric["name"], str)
            await session.performance.disable()

    async def test_get_metrics_values_are_numeric(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            result = await session.performance.get_metrics()
            for metric in result["metrics"]:
                assert isinstance(metric["value"], (int, float))
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

    async def test_enable_then_get_metrics_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.enable()
            r1 = await session.performance.get_metrics()
            r2 = await session.performance.get_metrics()
            assert "metrics" in r1
            assert "metrics" in r2
            assert len(r1["metrics"]) > 0
            assert len(r2["metrics"]) > 0
            await session.performance.disable()

    async def test_set_time_domain_thread_ticks_before_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.set_time_domain("threadTicks")
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
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
            await session.performance.disable()

    async def test_concurrent_set_time_domain_5x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await asyncio.gather(
                *[session.performance.set_time_domain("timeTicks") for _ in range(5)],
            )
            await session.performance.enable()
            await session.performance.disable()

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
            await session.performance.disable()

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

    async def test_set_time_domain_then_enable_then_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.performance.set_time_domain("timeTicks")
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert len(result["metrics"]) > 0
            names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in names
            await session.performance.disable()
