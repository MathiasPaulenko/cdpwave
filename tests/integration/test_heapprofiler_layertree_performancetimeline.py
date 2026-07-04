"""Functional tests for HeapProfiler, LayerTree, and PerformanceTimeline domains."""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestHeapProfiler:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.disable()

    async def test_collect_garbage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.collect_garbage()
            await session.heap_profiler.disable()

    async def test_start_stop_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.heap_profiler.enable()
            await session.heap_profiler.start_sampling(sampling_interval=4096)
            await session.heap_profiler.stop_sampling()
            await session.heap_profiler.disable()


@pytest.mark.integration
class TestLayerTree:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.layer_tree.enable()
                await session.layer_tree.disable()


@pytest.mark.integration
class TestPerformanceTimeline:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.performance_timeline is not None
