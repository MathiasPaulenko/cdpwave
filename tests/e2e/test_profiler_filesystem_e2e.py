"""E2E tests for the Profiler and FileSystem domains (real browser flows).

Full end-to-end flows against a real Edge browser, including
complete profiling lifecycle, precise code coverage, best-effort
coverage, sampling interval, type validation, raw command sending,
and FileSystem directory access.
"""

import asyncio
import inspect

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


async def _run_cpu_intensive_js(page: CDPSession) -> None:
    await page.runtime.enable()
    await page.runtime.evaluate(
        """
        new Promise((resolve) => {
            for (let i = 0; i < 100000; i++) { Math.sqrt(i); }
            resolve('done');
        })
        """,
        return_by_value=True,
        await_promise=True,
    )


@pytest.mark.e2e
class TestProfilerE2E:
    async def test_full_profile_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            await session.profiler.set_sampling_interval(100)
            await session.profiler.start()
            await _run_cpu_intensive_js(session)
            result = await session.profiler.stop()
            assert "profile" in result
            profile = result["profile"]
            assert "nodes" in profile
            assert len(profile["nodes"]) > 0
            assert "startTime" in profile
            assert "endTime" in profile
            assert profile["startTime"] <= profile["endTime"]
            assert "samples" in profile
            assert "timeDeltas" in profile
            await session.profiler.disable()

    async def test_precise_coverage_full_flow(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            result = await session.profiler.start_precise_coverage(
                call_count=True,
                detailed=True,
            )
            assert "timestamp" in result
            await session.runtime.evaluate(
                "function add(a, b) { return a + b; } "
                "add(1, 2); add(3, 4); add(5, 6);"
            )
            coverage = await session.profiler.take_precise_coverage()
            assert "result" in coverage
            assert "timestamp" in coverage
            assert isinstance(coverage["timestamp"], (int, float))
            assert len(coverage["result"]) > 0
            for entry in coverage["result"]:
                assert "scriptId" in entry
                assert "url" in entry
                assert "functions" in entry
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_best_effort_coverage_full_flow(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            await session.runtime.evaluate(
                "function g(x) { return x * 3; } g(1); g(2);"
            )
            result = await session.profiler.get_best_effort_coverage()
            assert "result" in result
            assert isinstance(result["result"], list)
            await session.profiler.disable()

    async def test_coverage_reset_on_double_take(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            await session.profiler.start_precise_coverage(call_count=True)
            await session.runtime.evaluate("1 + 1; 2 + 2; 3 + 3;")
            first = await session.profiler.take_precise_coverage()
            assert len(first["result"]) > 0
            second = await session.profiler.take_precise_coverage()
            assert "result" in second
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            await session.profiler.disable()
            await session.profiler.enable()
            await session.profiler.disable()

    async def test_stop_without_start_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            with pytest.raises(CommandError):
                await session.profiler.stop()
            await session.profiler.disable()

    async def test_set_sampling_interval_before_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            await session.profiler.set_sampling_interval(50)
            await session.profiler.start()
            await _run_cpu_intensive_js(session)
            result = await session.profiler.stop()
            assert "profile" in result
            await session.profiler.disable()

    async def test_type_error_set_sampling_interval_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="interval must be an int"):
                await session.profiler.set_sampling_interval("100")  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_type_error_set_sampling_interval_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="interval must be an int"):
                await session.profiler.set_sampling_interval(True)  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_type_error_start_precise_coverage_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="call_count must be a bool"):
                await session.profiler.start_precise_coverage(call_count="yes")  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_type_error_start_precise_coverage_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="detailed must be a bool"):
                await session.profiler.start_precise_coverage(detailed=1)  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_type_error_start_precise_coverage_allow_triggered(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.profiler.enable()
            with pytest.raises(TypeError, match="allow_triggered_updates must be a bool"):
                await session.profiler.start_precise_coverage(allow_triggered_updates="no")  # type: ignore[arg-type]
            await session.profiler.disable()

    async def test_raw_send_profiler_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send("Profiler.enable")
            await session.send("Profiler.start")
            await _run_cpu_intensive_js(session)
            result = await session.send("Profiler.stop")
            assert "profile" in result
            await session.send("Profiler.disable")

    async def test_all_methods_are_coroutines(self) -> None:
        from cdpwave.domains.profiler import ProfilerDomain
        from tests.unit.fake_sender import FakeSender
        domain = ProfilerDomain(FakeSender({}))
        for name in (
            "disable", "enable", "get_best_effort_coverage",
            "set_sampling_interval", "start", "start_precise_coverage",
            "stop", "stop_precise_coverage", "take_precise_coverage",
        ):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_method_count(self) -> None:
        from cdpwave.domains.profiler import ProfilerDomain
        methods = [
            m for m in dir(ProfilerDomain)
            if not m.startswith("_") and callable(getattr(ProfilerDomain, m))
        ]
        assert len(methods) == 9

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        from cdpwave.domains.profiler import ProfilerDomain
        from tests.unit.fake_sender import FakeSender
        domain = ProfilerDomain(FakeSender({}))
        assert isinstance(domain, BaseDomain)

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.profiler is not None

    async def test_precise_coverage_with_allow_triggered_updates(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.profiler.enable()
            result = await session.profiler.start_precise_coverage(
                call_count=True,
                detailed=True,
                allow_triggered_updates=True,
            )
            assert "timestamp" in result
            await session.runtime.evaluate("1 + 1")
            coverage = await session.profiler.take_precise_coverage()
            assert "result" in coverage
            await session.profiler.stop_precise_coverage()
            await session.profiler.disable()


@pytest.mark.e2e
class TestFileSystemE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.file_system is not None

    async def test_get_directory_with_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components=["root"],
                )
                assert isinstance(result, dict)
            except CommandError as exc:
                if "not found" in str(exc).lower() or "not supported" in str(exc).lower():
                    pytest.skip("FileSystem.getDirectory not available in this browser version")
                raise

    async def test_get_directory_with_bucket_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components=["root"],
                    bucket_name="test-bucket",
                )
                assert isinstance(result, dict)
            except CommandError as exc:
                if "not found" in str(exc).lower() or "not supported" in str(exc).lower():
                    pytest.skip("FileSystem.getDirectory not available in this browser version")
                raise

    async def test_type_error_storage_key_not_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="storage_key must be a str"):
                await session.file_system.get_directory(
                    storage_key=123,  # type: ignore[arg-type]
                    path_components=["root"],
                )

    async def test_type_error_path_components_not_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="path_components must be a list"):
                await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components="root",  # type: ignore[arg-type]
                )

    async def test_type_error_path_component_element_not_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"path_components\[0\] must be a str"):
                await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components=[42],  # type: ignore[list-item]
                )

    async def test_type_error_bucket_name_not_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="bucket_name must be a str"):
                await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components=["root"],
                    bucket_name=123,  # type: ignore[arg-type]
                )

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        from cdpwave.domains.file_system import FileSystemDomain
        from tests.unit.fake_sender import FakeSender
        domain = FileSystemDomain(FakeSender({}))
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        from cdpwave.domains.file_system import FileSystemDomain
        from tests.unit.fake_sender import FakeSender
        domain = FileSystemDomain(FakeSender({}))
        for name in ("get_directory",):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_method_count(self) -> None:
        from cdpwave.domains.file_system import FileSystemDomain
        methods = [
            m for m in dir(FileSystemDomain)
            if not m.startswith("_") and callable(getattr(FileSystemDomain, m))
        ]
        assert len(methods) == 1

    async def test_raw_send_filesystem_get_directory(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.send(
                    "FileSystem.getDirectory",
                    {
                        "bucketFileSystemLocator": {
                            "storageKey": "https://example.com",
                            "pathComponents": ["root"],
                        }
                    },
                )
                assert isinstance(result, dict)
            except CommandError as exc:
                if "not found" in str(exc).lower() or "not supported" in str(exc).lower():
                    pytest.skip("FileSystem.getDirectory not available in this browser version")
                raise
