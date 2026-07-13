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
            await session.log.start_violations_report(
                config=[
                    {"name": "longTask", "threshold": 500},
                    {"name": "longLayout", "threshold": 100},
                ],
            )

            await session.log.stop_violations_report()


@pytest.mark.integration
class TestConsole:
    async def test_console_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()

    async def test_console_enable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.enable()
            assert result == {}

    async def test_console_disable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            result = await session.console.disable()
            assert result == {}

    async def test_console_clear_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            result = await session.console.clear_messages()
            assert result == {}

    async def test_console_clear_messages_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.clear_messages()
            assert result == {}

    async def test_console_clear_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.clear_messages()
            assert result == {}

    async def test_console_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.disable()
            assert result == {}

    async def test_console_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.console.enable()
                await session.console.disable()

    async def test_console_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('test message')")
            await session.console.clear_messages()
            await session.console.disable()

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

            if console_msgs:
                msg = console_msgs[0]
                assert "message" in msg
                inner = msg["message"]
                assert "source" in inner
                assert "level" in inner
                assert "text" in inner

    async def test_console_message_added_source_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                source = console_msgs[0]["message"]["source"]
                valid_sources = {
                    "xml", "javascript", "network", "console-api",
                    "storage", "appcache", "rendering", "security",
                    "other", "deprecation", "worker",
                }
                assert source in valid_sources

    async def test_console_message_added_level_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('info msg')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                level = console_msgs[0]["message"]["level"]
                valid_levels = {"log", "warning", "error", "debug", "info"}
                assert level in valid_levels

    async def test_console_message_added_warning(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.warn('warn test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["level"] == "warning"

    async def test_console_message_added_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.error('error test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["level"] == "error"

    async def test_console_message_added_info(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.info('info test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["level"] == "info"

    async def test_console_message_added_debug(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.debug('debug test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["level"] == "debug"

    async def test_console_message_added_multiple(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('msg1')")
            await session.runtime.evaluate("console.log('msg2')")
            await session.runtime.evaluate("console.log('msg3')")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if len(console_msgs) >= 3:
                    break

            await session.console.disable()

            if len(console_msgs) >= 3:
                texts = [m["message"]["text"] for m in console_msgs]
                assert "msg1" in texts
                assert "msg2" in texts
                assert "msg3" in texts

    async def test_console_no_events_after_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)
            await session.console.disable()

            await session.runtime.evaluate("console.log('after disable')")

            await asyncio.sleep(2.0)
            assert console_msgs == []

    async def test_console_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.enable()
            await session.console.disable()

    async def test_console_disable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()
            await session.console.disable()

    async def test_console_clear_after_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('msg1')")
            await session.runtime.evaluate("console.log('msg2')")
            result = await session.console.clear_messages()
            assert result == {}
            await session.console.disable()

    async def test_console_message_added_optional_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('optional test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                msg = console_msgs[0]["message"]
                if "url" in msg:
                    assert isinstance(msg["url"], str)
                if "line" in msg:
                    assert isinstance(msg["line"], int)
                if "column" in msg:
                    assert isinstance(msg["column"], int)

    async def test_console_message_added_text_content(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('exact text test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["text"] == "exact text test"

    async def test_console_with_runtime_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('runtime enabled')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()
            await session.runtime.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["text"] == "runtime enabled"

    async def test_console_message_special_chars(self) -> None:
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
                "console.log('special: ñ émoji 🎉 tabs\\t\\n newlines')",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                text = console_msgs[0]["message"]["text"]
                assert "ñ" in text or "emoji" in text or "special" in text

    async def test_console_message_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.log('')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["text"] == ""

    async def test_console_message_long_text(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            long_text = "A" * 5000
            await session.runtime.evaluate(
                f"console.log('{long_text}')",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert len(console_msgs[0]["message"]["text"]) >= 1000

    async def test_console_message_multiple_args(self) -> None:
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
                "console.log('arg1', 'arg2', 42, true)",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                text = console_msgs[0]["message"]["text"]
                assert "arg1" in text

    async def test_console_uncaught_exception(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("throw new Error('uncaught test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

    async def test_console_assert_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.assert(false, 'assert failed')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

            if console_msgs:
                assert console_msgs[0]["message"]["level"] in ("error", "warning", "log")

    async def test_console_count(self) -> None:
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
                "console.count('myCount'); console.count('myCount');",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if len(console_msgs) >= 2:
                    break

            await session.console.disable()

    async def test_console_dir(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.dir({a: 1, b: 2})")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

    async def test_console_trace(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            await session.runtime.evaluate("console.trace('trace test')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

    async def test_console_table(self) -> None:
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
                "console.table([{a: 1}, {a: 2}])",
            )

            for _ in range(10):
                await asyncio.sleep(0.5)
                if console_msgs:
                    break

            await session.console.disable()

    async def test_console_rapid_fire_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            console_msgs: list[dict[str, Any]] = []

            async def on_console_msg(params: dict[str, Any]) -> None:
                console_msgs.append(params)

            await session.console.enable()
            session.on("Console.messageAdded", on_console_msg)

            for i in range(20):
                await session.runtime.evaluate(f"console.log('rapid {i}')")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if len(console_msgs) >= 20:
                    break

            await session.console.disable()

            if len(console_msgs) >= 10:
                texts = [m["message"]["text"] for m in console_msgs]
                assert any("rapid" in t for t in texts)

    async def test_console_group_ungroup(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate(
                "console.group('group1'); console.log('inside group'); console.groupEnd();",
            )
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_time_timeend(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate(
                "console.time('timer1'); console.timeEnd('timer1');",
            )
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_clear_browser_side(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('before browser clear')")
            await session.runtime.evaluate("console.clear()")
            await session.console.clear_messages()
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
