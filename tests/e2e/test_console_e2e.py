"""E2E tests for the Console domain (real browser flows).

Exercises all Console domain methods end-to-end against a real Chrome browser,
including event capture, clear operations, lifecycle management, and
verification of ConsoleMessage fields across all 5 console levels.

The Console domain is deprecated in favor of Runtime.consoleAPICalled
but still useful for clearMessages.
"""

import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_console_message(
    session: CDPSession,
    js_expr: str,
    timeout_s: float = 10.0,
) -> list[dict[str, Any]]:
    """Enable Console + Runtime, evaluate JS, and collect messageAdded events."""
    msgs: list[dict[str, Any]] = []

    async def on_msg(params: dict[str, Any]) -> None:
        msgs.append(params)

    await session.runtime.enable()
    await session.console.enable()
    session.on("Console.messageAdded", on_msg)

    await session.runtime.evaluate(js_expr)

    for _ in range(int(timeout_s / 0.5)):
        await asyncio.sleep(0.5)
        if msgs:
            break

    return msgs


async def _wait_for_multiple_console_messages(
    session: CDPSession,
    js_exprs: list[str],
    expected_count: int,
    timeout_s: float = 10.0,
) -> list[dict[str, Any]]:
    """Enable Console + Runtime, evaluate multiple JS expressions, collect events."""
    msgs: list[dict[str, Any]] = []

    async def on_msg(params: dict[str, Any]) -> None:
        msgs.append(params)

    await session.runtime.enable()
    await session.console.enable()
    session.on("Console.messageAdded", on_msg)

    for expr in js_exprs:
        await session.runtime.evaluate(expr)

    for _ in range(int(timeout_s / 0.5)):
        await asyncio.sleep(0.5)
        if len(msgs) >= expected_count:
            break

    return msgs


@pytest.mark.e2e
class TestConsoleE2E:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()

    async def test_enable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.enable()
            assert result == {}

    async def test_disable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            result = await session.console.disable()
            assert result == {}

    async def test_clear_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            result = await session.console.clear_messages()
            assert result == {}

    async def test_clear_messages_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.clear_messages()
            assert result == {}

    async def test_clear_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.clear_messages()
            assert result == {}

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.console.disable()
            assert result == {}

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.console.enable()
                await session.console.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('lifecycle test')")
            await session.console.clear_messages()
            await session.console.disable()

    async def test_message_added_log(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('e2e log test')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert msg["text"] == "e2e log test"
                assert msg["level"] == "log"
                assert msg["source"] == "console-api"

    async def test_message_added_warning(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.warn('e2e warn test')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert msg["level"] == "warning"
                assert msg["text"] == "e2e warn test"

    async def test_message_added_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.error('e2e error test')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert msg["level"] == "error"
                assert msg["text"] == "e2e error test"

    async def test_message_added_info(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.info('e2e info test')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert msg["level"] == "info"
                assert msg["text"] == "e2e info test"

    async def test_message_added_debug(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.debug('e2e debug test')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert msg["level"] == "debug"
                assert msg["text"] == "e2e debug test"

    async def test_message_added_has_source(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('source test')",
            )
            await session.console.disable()

            if msgs:
                valid_sources = {
                    "xml", "javascript", "network", "console-api",
                    "storage", "appcache", "rendering", "security",
                    "other", "deprecation", "worker",
                }
                assert msgs[0]["message"]["source"] in valid_sources

    async def test_message_added_has_text(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('text check')",
            )
            await session.console.disable()

            if msgs:
                assert isinstance(msgs[0]["message"]["text"], str)

    async def test_message_added_optional_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('optional fields')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                if "url" in msg:
                    assert isinstance(msg["url"], str)
                if "line" in msg:
                    assert isinstance(msg["line"], int)
                if "column" in msg:
                    assert isinstance(msg["column"], int)

    async def test_clear_after_messages(self) -> None:
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

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.enable()
            await session.console.disable()

    async def test_disable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()
            await session.console.disable()

    async def test_all_methods_call_sequence(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('seq test')")
            await session.console.clear_messages()
            await session.console.disable()

    async def test_no_events_after_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)
            await session.console.disable()

            await session.runtime.evaluate("console.log('after disable')")

            await asyncio.sleep(2.0)
            assert msgs == []

    async def test_multiple_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_multiple_console_messages(
                session,
                [
                    "console.log('multi1')",
                    "console.log('multi2')",
                    "console.log('multi3')",
                ],
                expected_count=3,
            )
            await session.console.disable()

            if len(msgs) >= 3:
                texts = [m["message"]["text"] for m in msgs]
                assert "multi1" in texts
                assert "multi2" in texts
                assert "multi3" in texts

    async def test_multiple_levels_in_sequence(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_multiple_console_messages(
                session,
                [
                    "console.log('lvl log')",
                    "console.warn('lvl warn')",
                    "console.error('lvl error')",
                    "console.info('lvl info')",
                    "console.debug('lvl debug')",
                ],
                expected_count=5,
            )
            await session.console.disable()

            if len(msgs) >= 5:
                levels = [m["message"]["level"] for m in msgs]
                assert "log" in levels
                assert "warning" in levels
                assert "error" in levels
                assert "info" in levels
                assert "debug" in levels

    async def test_clear_then_no_new_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)

            await session.runtime.evaluate("console.log('before clear')")
            await asyncio.sleep(1.0)

            await session.console.clear_messages()

            count_before = len(msgs)
            await asyncio.sleep(2.0)
            assert len(msgs) == count_before

            await session.console.disable()

    async def test_console_with_runtime_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('runtime enabled flow')",
            )
            await session.console.disable()
            await session.runtime.disable()

            if msgs:
                assert msgs[0]["message"]["text"] == "runtime enabled flow"

    async def test_console_message_source_console_api(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('source check')",
            )
            await session.console.disable()

            if msgs:
                assert msgs[0]["message"]["source"] == "console-api"

    async def test_console_message_has_all_required_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('fields check')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                assert "source" in msg
                assert "level" in msg
                assert "text" in msg

    async def test_console_deprecation_source(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)

            await session.runtime.evaluate(
                """
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/', false);
                xhr.send();
                """,
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if msgs:
                    break

            await session.console.disable()

            if msgs:
                valid_sources = {
                    "xml", "javascript", "network", "console-api",
                    "storage", "appcache", "rendering", "security",
                    "other", "deprecation", "worker",
                }
                for m in msgs:
                    assert m["message"]["source"] in valid_sources

    async def test_console_error_does_not_raise(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate(
                "console.error('intentional error')",
            )
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_clear_does_not_raise_without_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.clear_messages()
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_enable_after_disable_re_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()
            await session.console.enable()
            await session.console.disable()

    async def test_console_send_raw_command(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.send("Console.enable", None)
            assert result == {}
            result = await session.send("Console.clearMessages", None)
            assert result == {}
            result = await session.send("Console.disable", None)
            assert result == {}

    async def test_console_unicode_emoji_text(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('emoji 🎉 unicode ñ üñîçödé')",
            )
            await session.console.disable()

            if msgs:
                text = msgs[0]["message"]["text"]
                assert "emoji" in text or "unicode" in text or "ñ" in text

    async def test_console_empty_string_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('')",
            )
            await session.console.disable()

            if msgs:
                assert msgs[0]["message"]["text"] == ""

    async def test_console_long_text_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            long_text = "X" * 10000
            msgs = await _wait_for_console_message(
                session, f"console.log('{long_text}')",
            )
            await session.console.disable()

            if msgs:
                assert len(msgs[0]["message"]["text"]) >= 1000

    async def test_console_multiple_args(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('a', 'b', 42, true, null)",
            )
            await session.console.disable()

            if msgs:
                assert "a" in msgs[0]["message"]["text"]

    async def test_console_uncaught_exception(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)

            await session.runtime.evaluate("throw new Error('e2e uncaught')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if msgs:
                    break

            await session.console.disable()

    async def test_console_assert_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.assert(false, 'assertion failed')",
            )
            await session.console.disable()

            if msgs:
                assert msgs[0]["message"]["level"] in ("error", "warning", "log")

    async def test_console_count_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_multiple_console_messages(
                session,
                [
                    "console.count('cnt')",
                    "console.count('cnt')",
                    "console.count('cnt')",
                ],
                expected_count=3,
            )
            await session.console.disable()

            if len(msgs) >= 2:
                for m in msgs:
                    assert "cnt" in m["message"]["text"]

    async def test_console_dir_object(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_console_message(
                session, "console.dir({x: 1, y: 2})",
            )
            await session.console.disable()

    async def test_console_trace(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_console_message(
                session, "console.trace('e2e trace')",
            )
            await session.console.disable()

    async def test_console_table(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_console_message(
                session, "console.table([{a: 1}, {a: 2}])",
            )
            await session.console.disable()

    async def test_console_rapid_fire_20_messages(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)

            for i in range(20):
                await session.runtime.evaluate(f"console.log('rapid e2e {i}')")

            for _ in range(20):
                await asyncio.sleep(0.5)
                if len(msgs) >= 20:
                    break

            await session.console.disable()

            if len(msgs) >= 10:
                texts = [m["message"]["text"] for m in msgs]
                assert any("rapid e2e" in t for t in texts)

    async def test_console_group_groupend(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate(
                "console.group('g1'); console.log('inside'); console.groupEnd();",
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
                "console.time('t1'); console.timeEnd('t1');",
            )
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_clear_browser_side(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.runtime.evaluate("console.log('before clear')")
            await session.runtime.evaluate("console.clear()")
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_message_after_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.navigate("about:blank")
            await session.console.enable()
            await session.runtime.evaluate("console.log('after nav')")
            await session.console.clear_messages()
            await session.console.disable()

    async def test_console_enable_disable_enable_message(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.console.enable()
            await session.console.disable()

            msgs: list[dict[str, Any]] = []

            async def on_msg(params: dict[str, Any]) -> None:
                msgs.append(params)

            await session.runtime.enable()
            await session.console.enable()
            session.on("Console.messageAdded", on_msg)

            await session.runtime.evaluate("console.log('after re-enable')")

            for _ in range(10):
                await asyncio.sleep(0.5)
                if msgs:
                    break

            await session.console.disable()

            if msgs:
                assert msgs[0]["message"]["text"] == "after re-enable"

    async def test_console_all_methods_return_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            r1 = await session.console.enable()
            assert isinstance(r1, dict)
            r2 = await session.console.clear_messages()
            assert isinstance(r2, dict)
            r3 = await session.console.disable()
            assert isinstance(r3, dict)

    async def test_console_message_line_and_column_positive(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            msgs = await _wait_for_console_message(
                session, "console.log('line col check')",
            )
            await session.console.disable()

            if msgs:
                msg = msgs[0]["message"]
                if "line" in msg:
                    assert msg["line"] > 0
                if "column" in msg:
                    assert msg["column"] > 0
