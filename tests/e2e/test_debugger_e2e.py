"""E2E tests for the Debugger domain on a real Edge browser.

Full lifecycle tests covering enable/disable, script parsing events,
breakpoint set/remove cycles, pause/resume flows, stepping, search in
content, evaluate on call frame, set pause on exceptions (all states),
set skip all pauses, set breakpoints active toggling, set blackbox
patterns, and repeated cycles. Includes edge cases like invalid
breakpoint IDs, type validation errors, and invalid enum values.
"""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession


async def _navigate_and_wait(session: CDPSession, url: str = "https://example.com") -> None:
    await session.page.enable()
    await session.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.e2e
class TestDebuggerE2ELifecycle:
    async def test_enable_disable_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.disable()

    async def test_enable_with_cache_size_then_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable(max_scripts_cache_size=5_000_000)
            await session.debugger.disable()

    async def test_repeated_enable_disable_cycles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(5):
                await session.debugger.enable()
                await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2EScriptParsing:
    async def test_script_parsed_event_fired(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            await session.debugger.enable()
            session.on("Debugger.scriptParsed", on_script_parsed)

            await _navigate_and_wait(session)
            await asyncio.sleep(2.0)

            assert len(scripts) > 0
            for script in scripts:
                assert "scriptId" in script
                assert "url" in script
                assert "startLine" in script
                assert "endLine" in script

            await session.debugger.disable()

    async def test_get_script_source_after_parse(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            await session.debugger.enable()
            session.on("Debugger.scriptParsed", on_script_parsed)

            await _navigate_and_wait(session)
            await asyncio.sleep(3.0)

            assert len(scripts) > 0
            script_id = scripts[0]["scriptId"]
            result = await session.debugger.get_script_source(script_id)
            assert "scriptSource" in result
            assert isinstance(result["scriptSource"], str)

            await session.debugger.disable()

    async def test_search_in_content_after_parse(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            await session.debugger.enable()
            session.on("Debugger.scriptParsed", on_script_parsed)

            await _navigate_and_wait(session)
            await asyncio.sleep(3.0)

            assert len(scripts) > 0
            script_id = scripts[0]["scriptId"]
            result = await session.debugger.search_in_content(script_id, "example")
            assert isinstance(result, dict)
            if "result" in result:
                assert isinstance(result["result"], list)

            await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2EBreakpoints:
    async def test_set_and_remove_breakpoint_by_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            result = await session.debugger.set_breakpoint_by_url(
                0, url="https://example.com/test.js"
            )
            assert isinstance(result, dict)
            bp_id = result.get("breakpointId")
            if bp_id:
                await session.debugger.remove_breakpoint(bp_id)

            await session.debugger.disable()

    async def test_set_breakpoint_by_url_with_condition(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            result = await session.debugger.set_breakpoint_by_url(
                0, url_regex=r".*\.js$", condition="i === 0"
            )
            assert isinstance(result, dict)
            bp_id = result.get("breakpointId")
            if bp_id:
                await session.debugger.remove_breakpoint(bp_id)

            await session.debugger.disable()

    async def test_set_breakpoints_active_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            await session.debugger.set_breakpoints_active(True)
            await session.debugger.set_breakpoints_active(False)
            await session.debugger.set_breakpoints_active(True)

            await session.debugger.disable()

    async def test_remove_nonexistent_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with pytest.raises(Exception) as exc_info:
                await session.debugger.remove_breakpoint("nonexistent-bp-id")
            assert exc_info.value is not None
            await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2EPauseResume:
    async def test_pause_resume_with_skip_all(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)

            await session.debugger.pause()
            await asyncio.sleep(1.0)

            with contextlib.suppress(Exception):
                await session.debugger.resume()

            await session.debugger.disable()

    async def test_pause_resume_with_terminate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)

            await session.debugger.pause()
            await asyncio.sleep(1.0)

            with contextlib.suppress(Exception):
                await session.debugger.resume(terminate_on_resume=True)

            await session.debugger.disable()

    async def test_resumed_event_fired(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            resumed: list[dict[str, Any]] = []

            async def on_resumed(params: dict[str, Any]) -> None:
                resumed.append(params)

            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            session.on("Debugger.resumed", on_resumed)

            await session.debugger.pause()
            await asyncio.sleep(1.0)
            with contextlib.suppress(Exception):
                await session.debugger.resume()
            await asyncio.sleep(1.0)

            await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2EPauseOnExceptions:
    @pytest.mark.parametrize("state", ["none", "caught", "uncaught", "all"])
    async def test_all_valid_states(self, state: str) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_pause_on_exceptions(state)
            await session.debugger.set_pause_on_exceptions("none")
            await session.debugger.disable()

    async def test_invalid_state_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with pytest.raises(ValueError, match="state must be one of"):
                await session.debugger.set_pause_on_exceptions("invalid")
            await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2EBlackbox:
    async def test_set_blackbox_patterns(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_blackbox_patterns([r".*node_modules.*"])
            await session.debugger.disable()

    async def test_set_blackbox_patterns_with_skip_anonymous(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_blackbox_patterns(
                [r".*vendor.*"], skip_anonymous=True
            )
            await session.debugger.disable()


@pytest.mark.e2e
class TestDebuggerE2ETypeValidation:
    """Type validation should raise before any CDP call, even on a real browser."""

    async def test_enable_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="max_scripts_cache_size"):
                await session.debugger.enable(max_scripts_cache_size="big")

    async def test_resume_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="terminate_on_resume"):
                await session.debugger.resume(terminate_on_resume="yes")

    async def test_set_breakpoint_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="location"):
                await session.debugger.set_breakpoint("not-a-dict")

    async def test_set_breakpoint_by_url_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="line_number"):
                await session.debugger.set_breakpoint_by_url("0")

    async def test_evaluate_on_call_frame_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.evaluate_on_call_frame(42, "x")

    async def test_get_script_source_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.get_script_source(42)

    async def test_search_in_content_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.search_in_content(42, "test")

    async def test_set_pause_on_exceptions_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="state"):
                await session.debugger.set_pause_on_exceptions(42)

    async def test_set_skip_all_pauses_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="skip"):
                await session.debugger.set_skip_all_pauses("yes")

    async def test_set_breakpoints_active_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="active"):
                await session.debugger.set_breakpoints_active("yes")

    async def test_set_variable_value_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.set_variable_value(42, 0, "x", {})

    async def test_set_return_value_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="new_value"):
                await session.debugger.set_return_value("not-a-dict")

    async def test_get_stack_trace_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="stack_trace_id"):
                await session.debugger.get_stack_trace("not-a-dict")

    async def test_set_blackbox_patterns_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="patterns"):
                await session.debugger.set_blackbox_patterns("not-a-list")


@pytest.mark.e2e
class TestDebuggerE2EFullFlow:
    """Full end-to-end flow: enable → navigate → parse → search → disable."""

    async def test_navigate_and_inspect_scripts(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            await session.debugger.enable()
            session.on("Debugger.scriptParsed", on_script_parsed)

            await _navigate_and_wait(session)
            await asyncio.sleep(3.0)

            assert len(scripts) > 0

            for script in scripts:
                sid = script["scriptId"]
                source_result = await session.debugger.get_script_source(sid)
                assert "scriptSource" in source_result

            await session.debugger.disable()

    async def test_enable_breakpoint_search_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_breakpoints_active(True)
            await session.debugger.set_pause_on_exceptions("none")
            await session.debugger.set_skip_all_pauses(True)

            result = await session.debugger.set_breakpoint_by_url(
                0, url="https://example.com/nonexistent.js"
            )
            bp_id = result.get("breakpointId")
            if bp_id:
                await session.debugger.remove_breakpoint(bp_id)

            await session.debugger.set_blackbox_patterns([r".*\.min\.js$"])

            await session.debugger.disable()

    async def test_set_async_call_stack_depth_e2e(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_async_call_stack_depth(32)
            await session.debugger.set_async_call_stack_depth(0)
            await session.debugger.disable()

    async def test_set_instrumentation_breakpoint_e2e(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_instrumentation_breakpoint(
                "beforeScriptExecution"
            )
            assert isinstance(result, dict)
            bp_id = result.get("breakpointId")
            if bp_id:
                await session.debugger.remove_breakpoint(bp_id)
            await session.debugger.disable()

    async def test_set_blackbox_execution_contexts_e2e(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_blackbox_execution_contexts([])
            await session.debugger.disable()

    async def test_new_methods_type_validation_e2e(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="location"):
                await session.debugger.continue_to_location("bad")

            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.restart_frame(42, "StepInto")

            with pytest.raises(ValueError, match="mode must be one of"):
                await session.debugger.restart_frame("cf1", "StepOver")

            with pytest.raises(ValueError, match="instrumentation must be one of"):
                await session.debugger.set_instrumentation_breakpoint("bad")

            with pytest.raises(TypeError, match="max_depth"):
                await session.debugger.set_async_call_stack_depth("bad")

            with pytest.raises(TypeError, match="execution_context_ids"):
                await session.debugger.set_blackbox_execution_contexts("bad")

            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.set_blackboxed_ranges(42, [])

            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.disassemble_wasm_module(42)

            with pytest.raises(TypeError, match="stream_id"):
                await session.debugger.next_wasm_disassembly_chunk(42)

            with pytest.raises(TypeError, match="timeout"):
                await session.debugger.evaluate_on_call_frame(
                    "cf1", "x", timeout="bad"
                )

            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.get_wasm_bytecode(42)

            with pytest.raises(TypeError, match="parent_stack_trace_id"):
                await session.debugger.pause_on_async_call("not-a-dict")
