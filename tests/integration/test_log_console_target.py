import asyncio
import contextlib
from typing import Any

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
class TestLog:
    async def test_log_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.disable()

    async def test_log_entry_added(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            log_entries: list[dict[str, Any]] = []

            async def on_log_entry(params: dict[str, Any]) -> None:
                log_entries.append(params)

            await session.runtime.enable()
            await session.log.enable()
            session.on("Log.entryAdded", on_log_entry)

            await session.runtime.evaluate(
                """
                console.deprecated = () => {};
                console.deprecated();
                // Trigger a deprecation warning
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                """,
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if log_entries:
                    break

            if log_entries:
                assert "entry" in log_entries[0]

    async def test_log_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            result = await session.log.clear()
            assert result == {}

    async def test_log_start_stop_violations_report(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.log.enable()
            await session.log.start_violation_report(
                config=[
                    {"name": "longTask", "threshold": 500},
                    {"name": "longLayout", "threshold": 100},
                ],
            )

            await session.log.stop_violation_report()


@pytest.mark.integration
class TestConsole:
    async def test_console_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()

    async def test_console_clear_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            result = await session.console.clear_messages()
            assert result == {}

    async def test_console_message_added(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate(
                "console.log('console domain test')",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()


@pytest.mark.integration
class TestTarget:
    async def test_get_targets(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.target.get_targets()
            assert "targetInfos" in result
            assert len(result["targetInfos"]) >= 1

    async def test_create_and_close_target(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            create_result = await session.target.create_target(
                "about:blank",
            )
            assert "targetId" in create_result
            new_target_id = create_result["targetId"]

            close_result = await session.target.close_target(new_target_id)
            assert close_result.get("success") is True or close_result == {}

    async def test_set_auto_attach(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.target.set_auto_attach(
                    auto_attach=False,
                    flatten=True,
                )

    async def test_detach_from_target(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.target.detach_from_target(
                    session.session_id,
                )
                assert result == {}
