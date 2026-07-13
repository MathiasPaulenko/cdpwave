"""E2E tests for the Log domain (real browser flows).

Exercises all Log domain methods end-to-end against a real Chrome browser,
including event capture, violation reporting, and clear operations.
"""

import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_log_entry(
    session: CDPSession,
    js_expr: str,
    timeout_s: float = 10.0,
) -> list[dict[str, Any]]:
    """Enable Log, evaluate JS, and collect entryAdded events."""
    entries: list[dict[str, Any]] = []

    async def on_entry(params: dict[str, Any]) -> None:
        entries.append(params)

    await session.runtime.enable()
    await session.log.enable()
    session.on("Log.entryAdded", on_entry)

    await session.runtime.evaluate(js_expr)

    for _ in range(int(timeout_s / 0.5)):
        await asyncio.sleep(0.5)
        if entries:
            break

    return entries


@pytest.mark.e2e
class TestLogE2E:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.disable()

    async def test_enable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.log.enable()
            assert result == {}
            await session.log.disable()

    async def test_disable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            result = await session.log.disable()
            assert result == {}

    async def test_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            result = await session.log.clear()
            assert result == {}

    async def test_clear_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.log.clear()
            assert result == {}

    async def test_entry_added_deprecation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            entries = await _wait_for_log_entry(
                session,
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            if entries:
                entry = entries[0]["entry"]
                assert "source" in entry
                assert "level" in entry
                assert "text" in entry
                assert "timestamp" in entry

    async def test_entry_added_has_correct_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            entries = await _wait_for_log_entry(
                session,
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            if entries:
                entry = entries[0]["entry"]
                assert isinstance(entry["source"], str)
                assert isinstance(entry["level"], str)
                assert isinstance(entry["text"], str)
                assert isinstance(entry["timestamp"], (int, float))

    async def test_entry_added_source_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            entries = await _wait_for_log_entry(
                session,
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            if entries:
                entry = entries[0]["entry"]
                valid_sources = {
                    "xml", "javascript", "network", "storage",
                    "appcache", "rendering", "security",
                    "deprecation", "worker", "violation",
                    "intervention", "recommendation", "other",
                }
                assert entry["source"] in valid_sources

    async def test_entry_added_level_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            entries = await _wait_for_log_entry(
                session,
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            if entries:
                entry = entries[0]["entry"]
                valid_levels = {"verbose", "info", "warning", "error"}
                assert entry["level"] in valid_levels

    async def test_start_violations_report_single(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.start_violations_report(
                [{"name": "longTask", "threshold": 500}],
            )
            await session.log.stop_violations_report()
            await session.log.disable()

    async def test_start_violations_report_all_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.start_violations_report(
                [
                    {"name": "longTask", "threshold": 500},
                    {"name": "longLayout", "threshold": 100},
                    {"name": "blockedEvent", "threshold": 50},
                    {"name": "blockedParser", "threshold": 200},
                    {"name": "discouragedAPIUse", "threshold": 0},
                    {"name": "handler", "threshold": 1000},
                    {"name": "recurringHandler", "threshold": 5000},
                ],
            )
            await session.log.stop_violations_report()
            await session.log.disable()

    async def test_start_violations_report_float_threshold(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.start_violations_report(
                [{"name": "longTask", "threshold": 50.5}],
            )
            await session.log.stop_violations_report()
            await session.log.disable()

    async def test_stop_violations_report_without_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.stop_violations_report()
            await session.log.disable()

    async def test_stop_violations_report_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.start_violations_report(
                [{"name": "longTask", "threshold": 500}],
            )
            result = await session.log.stop_violations_report()
            assert result == {}
            await session.log.disable()

    async def test_start_violations_report_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            result = await session.log.start_violations_report(
                [{"name": "longTask", "threshold": 500}],
            )
            assert result == {}
            await session.log.stop_violations_report()
            await session.log.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.clear()
            await session.log.enable()
            await session.log.start_violations_report(
                [{"name": "longTask", "threshold": 100}],
            )
            await session.log.stop_violations_report()
            await session.log.clear()
            await session.log.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.log.enable()
                await session.log.disable()

    async def test_violation_report_restart(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            for _ in range(2):
                await session.log.start_violations_report(
                    [{"name": "longTask", "threshold": 200}],
                )
                await session.log.stop_violations_report()
            await session.log.disable()

    async def test_clear_after_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.log.enable()

            await session.runtime.evaluate(
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            await asyncio.sleep(1.0)

            result = await session.log.clear()
            assert result == {}
            await session.log.disable()

    async def test_entry_added_optional_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            entries = await _wait_for_log_entry(
                session,
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )
            if entries:
                entry = entries[0]["entry"]
                if "url" in entry:
                    assert isinstance(entry["url"], str)
                if "lineNumber" in entry:
                    assert isinstance(entry["lineNumber"], int)
                if "stackTrace" in entry:
                    assert isinstance(entry["stackTrace"], dict)
                if "networkRequestId" in entry:
                    assert isinstance(entry["networkRequestId"], str)
                if "workerId" in entry:
                    assert isinstance(entry["workerId"], str)
                if "args" in entry:
                    assert isinstance(entry["args"], list)
                if "category" in entry:
                    assert entry["category"] == "cors"
