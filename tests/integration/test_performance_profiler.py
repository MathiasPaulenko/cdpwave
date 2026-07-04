"""Functional tests for Performance and Profiler domains."""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession


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
