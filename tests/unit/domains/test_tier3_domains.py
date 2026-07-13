"""Unit tests for Performance and Profiler domains (Tier 3)."""

import pytest

from cdpwave.domains.performance import PerformanceDomain
from cdpwave.domains.profiler import ProfilerDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestPerformanceDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Performance.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Performance.disable", None)

    async def test_get_metrics(self) -> None:
        fake = FakeSender(
            {"metrics": [{"name": "JSHeapUsedSize", "value": 1000000}]}
        )
        domain = PerformanceDomain(fake)
        result = await domain.get_metrics()
        assert fake.last_call == ("Performance.getMetrics", None)
        assert "metrics" in result
        assert result["metrics"][0]["name"] == "JSHeapUsedSize"

    async def test_set_time_domain(self) -> None:
        fake = FakeSender({})
        domain = PerformanceDomain(fake)
        await domain.set_time_domain("timeTicks")
        assert fake.last_call == (
            "Performance.setTimeDomain",
            {"timeDomain": "timeTicks"},
        )


@pytest.mark.unit
class TestProfilerDomain:
    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Profiler.disable", None)

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Profiler.enable", None)

    async def test_get_best_effort_coverage(self) -> None:
        fake = FakeSender({"result": []})
        domain = ProfilerDomain(fake)
        result = await domain.get_best_effort_coverage()
        assert fake.last_call == ("Profiler.getBestEffortCoverage", None)
        assert "result" in result

    async def test_set_sampling_interval(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.set_sampling_interval(500)
        assert fake.last_call == (
            "Profiler.setSamplingInterval",
            {"interval": 500},
        )

    async def test_set_sampling_interval_type_error(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="interval must be an int"):
            await domain.set_sampling_interval("500")  # type: ignore[arg-type]

    async def test_start(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        result = await domain.start()
        assert fake.last_call == ("Profiler.start", None)
        assert result == {}

    async def test_start_precise_coverage_defaults(self) -> None:
        fake = FakeSender({"timestamp": 100.0})
        domain = ProfilerDomain(fake)
        await domain.start_precise_coverage()
        method, params = fake.last_call
        assert method == "Profiler.startPreciseCoverage"
        assert params is not None
        assert params["callCount"] is False
        assert params["detailed"] is False
        assert params["allowTriggeredUpdates"] is False

    async def test_start_precise_coverage_with_options(self) -> None:
        fake = FakeSender({"timestamp": 100.0})
        domain = ProfilerDomain(fake)
        await domain.start_precise_coverage(
            call_count=True,
            detailed=True,
            allow_triggered_updates=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["callCount"] is True
        assert params["detailed"] is True
        assert params["allowTriggeredUpdates"] is True

    async def test_start_precise_coverage_type_error_call_count(self) -> None:
        fake = FakeSender({"timestamp": 100.0})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="call_count must be a bool"):
            await domain.start_precise_coverage(call_count="yes")  # type: ignore[arg-type]

    async def test_start_precise_coverage_type_error_detailed(self) -> None:
        fake = FakeSender({"timestamp": 100.0})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="detailed must be a bool"):
            await domain.start_precise_coverage(detailed=1)  # type: ignore[arg-type]

    async def test_start_precise_coverage_type_error_allow_triggered(self) -> None:
        fake = FakeSender({"timestamp": 100.0})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="allow_triggered_updates must be a bool"):
            await domain.start_precise_coverage(allow_triggered_updates="yes")  # type: ignore[arg-type]

    async def test_stop(self) -> None:
        fake = FakeSender({"profile": {"nodes": [], "samples": []}})
        domain = ProfilerDomain(fake)
        result = await domain.stop()
        assert fake.last_call == ("Profiler.stop", None)
        assert "profile" in result

    async def test_stop_precise_coverage(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.stop_precise_coverage()
        assert fake.last_call == ("Profiler.stopPreciseCoverage", None)

    async def test_take_precise_coverage(self) -> None:
        fake = FakeSender({"result": [], "timestamp": 200.0})
        domain = ProfilerDomain(fake)
        result = await domain.take_precise_coverage()
        assert fake.last_call == ("Profiler.takePreciseCoverage", None)
        assert "result" in result
        assert "timestamp" in result

    async def test_set_sampling_interval_bool_true_rejected(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="interval must be an int"):
            await domain.set_sampling_interval(True)  # type: ignore[arg-type]

    async def test_set_sampling_interval_bool_false_rejected(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        with pytest.raises(TypeError, match="interval must be an int"):
            await domain.set_sampling_interval(False)  # type: ignore[arg-type]

    async def test_set_sampling_interval_zero(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.set_sampling_interval(0)
        assert fake.last_call == (
            "Profiler.setSamplingInterval",
            {"interval": 0},
        )

    async def test_set_sampling_interval_negative(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.set_sampling_interval(-100)
        assert fake.last_call == (
            "Profiler.setSamplingInterval",
            {"interval": -100},
        )

    async def test_set_sampling_interval_large(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.set_sampling_interval(2**31 - 1)
        _, params = fake.last_call
        assert params is not None
        assert params["interval"] == 2**31 - 1

    async def test_enable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_disable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_start_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        result = await domain.start()
        assert result == {}

    async def test_stop_precise_coverage_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        result = await domain.stop_precise_coverage()
        assert result == {}

    async def test_stop_profile_structure(self) -> None:
        profile_data = {
            "nodes": [{"id": 1, "callFrame": {}}],
            "startTime": 1000.0,
            "endTime": 2000.0,
            "samples": [1],
            "timeDeltas": [100],
        }
        fake = FakeSender({"profile": profile_data})
        domain = ProfilerDomain(fake)
        result = await domain.stop()
        assert result["profile"] == profile_data
        assert result["profile"]["nodes"][0]["id"] == 1
        assert result["profile"]["startTime"] == 1000.0
        assert result["profile"]["endTime"] == 2000.0

    async def test_start_precise_coverage_returns_timestamp(self) -> None:
        fake = FakeSender({"timestamp": 42.5})
        domain = ProfilerDomain(fake)
        result = await domain.start_precise_coverage()
        assert result["timestamp"] == 42.5

    async def test_take_precise_coverage_returns_timestamp(self) -> None:
        fake = FakeSender({
            "result": [{"scriptId": "1", "url": "", "functions": []}],
            "timestamp": 99.9,
        })
        domain = ProfilerDomain(fake)
        result = await domain.take_precise_coverage()
        assert result["timestamp"] == 99.9
        assert isinstance(result["result"], list)
        assert result["result"][0]["scriptId"] == "1"

    async def test_get_best_effort_coverage_returns_result(self) -> None:
        fake = FakeSender({"result": [{"scriptId": "1", "url": "test.js", "functions": []}]})
        domain = ProfilerDomain(fake)
        result = await domain.get_best_effort_coverage()
        assert isinstance(result["result"], list)
        assert result["result"][0]["url"] == "test.js"

    async def test_all_methods_are_coroutines(self) -> None:
        import inspect
        domain = ProfilerDomain(FakeSender({}))
        for name in (
            "disable", "enable", "get_best_effort_coverage",
            "set_sampling_interval", "start", "start_precise_coverage",
            "stop", "stop_precise_coverage", "take_precise_coverage",
        ):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(ProfilerDomain)
            if not m.startswith("_") and callable(getattr(ProfilerDomain, m))
        ]
        assert len(methods) == 9

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        domain = ProfilerDomain(FakeSender({}))
        assert isinstance(domain, BaseDomain)

    async def test_module_docstring_documents_console_profile_finished(self) -> None:
        import cdpwave.domains.profiler as mod
        assert "Profiler.consoleProfileFinished" in mod.__doc__
        assert "id" in mod.__doc__
        assert "location" in mod.__doc__
        assert "profile" in mod.__doc__
        assert "title" in mod.__doc__

    async def test_module_docstring_documents_console_profile_started(self) -> None:
        import cdpwave.domains.profiler as mod
        assert "Profiler.consoleProfileStarted" in mod.__doc__
        assert "console.profile()" in mod.__doc__

    async def test_module_docstring_documents_precise_coverage_delta_update(self) -> None:
        import cdpwave.domains.profiler as mod
        assert "Profiler.preciseCoverageDeltaUpdate" in mod.__doc__
        assert "occasion" in mod.__doc__
        assert "timestamp" in mod.__doc__
        assert "result" in mod.__doc__

    async def test_class_docstring_documents_all_three_events(self) -> None:
        doc = ProfilerDomain.__doc__
        assert doc is not None
        assert "Profiler.consoleProfileFinished" in doc
        assert "Profiler.consoleProfileStarted" in doc
        assert "Profiler.preciseCoverageDeltaUpdate" in doc

    async def test_class_docstring_precise_coverage_delta_update_has_occasion(self) -> None:
        doc = ProfilerDomain.__doc__
        assert doc is not None
        assert "occasion" in doc

    async def test_class_docstring_precise_coverage_delta_update_marked_experimental(self) -> None:
        doc = ProfilerDomain.__doc__
        assert doc is not None
        idx = doc.index("preciseCoverageDeltaUpdate")
        segment = doc[idx:]
        assert "Experimental" in segment
