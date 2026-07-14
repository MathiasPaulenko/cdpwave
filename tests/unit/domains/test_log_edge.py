"""Edge-case tests for the Log domain — validation branches only.

Targets every TypeError/ValueError raise in LogDomain to push
coverage from 77% to >=90%.
"""

import pytest

from cdpwave.domains.log import LogDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestLogEdgeValidation:
    async def test_start_violations_report_config_not_list(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(TypeError, match="config must be a list"):
            await d.start_violations_report("not-a-list")  # type: ignore[arg-type]

    async def test_start_violations_report_entry_not_dict(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(TypeError, match="config\\[0\\] must be a dict"):
            await d.start_violations_report(["not-a-dict"])  # type: ignore[list-item]

    async def test_start_violations_report_missing_name(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(ValueError, match="config\\[0\\] must contain 'name'"):
            await d.start_violations_report([{"threshold": 1.0}])

    async def test_start_violations_report_missing_threshold(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(ValueError, match="config\\[0\\] must contain 'threshold'"):
            await d.start_violations_report([{"name": "longTask"}])

    async def test_start_violations_report_name_not_str(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(TypeError, match="config\\[0\\]\\['name'\\] must be a string"):
            await d.start_violations_report([{"name": 123, "threshold": 1.0}])

    async def test_start_violations_report_name_invalid(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(ValueError, match="config\\[0\\]\\['name'\\] must be one of"):
            await d.start_violations_report([{"name": "invalid", "threshold": 1.0}])

    async def test_start_violations_report_threshold_not_number(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(TypeError, match="config\\[0\\]\\['threshold'\\] must be a number"):
            await d.start_violations_report([{"name": "longTask", "threshold": "x"}])

    async def test_start_violations_report_threshold_bool(self) -> None:
        d = LogDomain(FakeSender({}))
        with pytest.raises(TypeError, match="config\\[0\\]\\['threshold'\\] must be a number"):
            await d.start_violations_report([{"name": "longTask", "threshold": True}])
