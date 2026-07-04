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
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Profiler.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = ProfilerDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Profiler.disable", None)

    async def test_start(self) -> None:
        fake = FakeSender({"timestamp": 12345.0})
        domain = ProfilerDomain(fake)
        result = await domain.start()
        assert fake.last_call == ("Profiler.start", None)
        assert "timestamp" in result

    async def test_stop(self) -> None:
        fake = FakeSender({"profile": {"nodes": [], "samples": []}})
        domain = ProfilerDomain(fake)
        result = await domain.stop()
        assert fake.last_call == ("Profiler.stop", None)
        assert "profile" in result

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

    async def test_stop_precise_coverage(self) -> None:
        fake = FakeSender({"timestamp": 200.0})
        domain = ProfilerDomain(fake)
        await domain.stop_precise_coverage()
        assert fake.last_call == ("Profiler.stopPreciseCoverage", None)

    async def test_take_precise_coverage(self) -> None:
        fake = FakeSender({"result": []})
        domain = ProfilerDomain(fake)
        result = await domain.take_precise_coverage()
        assert fake.last_call == ("Profiler.takePreciseCoverage", None)
        assert "result" in result

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
