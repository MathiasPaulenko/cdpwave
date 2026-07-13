"""Functional tests for Performance and Profiler domains."""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


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


@pytest.mark.integration
class TestPerformance:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            await session.performance.disable()

    async def test_get_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.enable()
            result = await session.performance.get_metrics()
            assert "metrics" in result
            metric_names = [m["name"] for m in result["metrics"]]
            assert "JSHeapUsedSize" in metric_names
            await session.performance.disable()

    async def test_set_time_domain(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.performance.set_time_domain("timeTicks")


@pytest.mark.integration
class TestProfiler:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.disable()

    async def test_start_stop_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.start()

            await session.runtime.evaluate(
                "for (let i = 0; i < 10000; i++) { Math.sqrt(i); }"
            )

            result = await session.profiler.stop()
            assert "profile" in result
            profile = result["profile"]
            assert "nodes" in profile
            assert len(profile["nodes"]) > 0

            await session.profiler.disable()

    async def test_precise_coverage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()

            await session.profiler.start_precise_coverage(
                call_count=True,
                detailed=True,
            )

            await session.runtime.evaluate(
                "function add(a, b) { return a + b; } "
                "add(1, 2); add(3, 4);"
            )

            result = await session.profiler.take_precise_coverage()
            assert "result" in result
            assert len(result["result"]) > 0

            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_best_effort_coverage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()

            await session.runtime.evaluate("1 + 1")

            result = await session.profiler.get_best_effort_coverage()
            assert "result" in result

            await session.profiler.disable()

    async def test_set_sampling_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.set_sampling_interval(500)
            await session.profiler.start()
            await session.profiler.stop()
            await session.profiler.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.enable()
            await session.profiler.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.disable()

    async def test_stop_without_start_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(CommandError):
                await session.profiler.stop()
            await session.profiler.disable()

    async def test_start_precise_coverage_default_flags(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            result = await session.profiler.start_precise_coverage()
            assert "timestamp" in result
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_start_precise_coverage_allow_triggered_updates(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            result = await session.profiler.start_precise_coverage(
                call_count=True,
                detailed=True,
                allow_triggered_updates=True,
            )
            assert "timestamp" in result
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_take_precise_coverage_returns_timestamp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.start_precise_coverage(call_count=True)
            await session.runtime.evaluate("1 + 1")
            result = await session.profiler.take_precise_coverage()
            assert "result" in result
            assert "timestamp" in result
            assert isinstance(result["timestamp"], (int, float))
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_precise_coverage_with_detailed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.start_precise_coverage(
                call_count=True,
                detailed=True,
            )
            await session.runtime.evaluate(
                "function f(x) { return x * 2; } f(5); f(10);"
            )
            result = await session.profiler.take_precise_coverage()
            assert len(result["result"]) > 0
            for entry in result["result"]:
                assert "scriptId" in entry
                assert "url" in entry
                assert "functions" in entry
                for func in entry["functions"]:
                    assert "functionName" in func
                    assert "ranges" in func
                    assert "isBlockCoverage" in func
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_set_sampling_interval_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="interval must be an int"):
                await session.profiler.set_sampling_interval("500")  # type: ignore[arg-type]
            with pytest.raises(TypeError, match="interval must be an int"):
                await session.profiler.set_sampling_interval(True)  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_start_precise_coverage_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="call_count must be a bool"):
                await session.profiler.start_precise_coverage(call_count="yes")  # type: ignore[arg-type]
            with pytest.raises(TypeError, match="detailed must be a bool"):
                await session.profiler.start_precise_coverage(detailed=1)  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_full_profile_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.set_sampling_interval(100)
            await session.profiler.start()
            await session.runtime.evaluate(
                "for (let i = 0; i < 50000; i++) { Math.sqrt(i); }"
            )
            result = await session.profiler.stop()
            profile = result["profile"]
            assert "nodes" in profile
            assert "startTime" in profile
            assert "endTime" in profile
            assert profile["startTime"] <= profile["endTime"]
            await session.profiler.disable()

    async def test_coverage_reset_on_take(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.profiler.start_precise_coverage(call_count=True)
            await session.runtime.evaluate("1 + 1; 2 + 2;")
            first = await session.profiler.take_precise_coverage()
            await session.profiler.take_precise_coverage()
            assert len(first["result"]) > 0
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_best_effort_coverage_structure(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            await session.runtime.evaluate("function g(x) { return x + 1; } g(1);")
            result = await session.profiler.get_best_effort_coverage()
            assert "result" in result
            assert isinstance(result["result"], list)
            await session.profiler.disable()
