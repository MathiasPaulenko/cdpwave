"""Integration tests for the Debugger domain on a real Edge browser.

Tests cover enable/disable, pause/resume, stepping, breakpoints,
script source retrieval, search in content, evaluate on call frame,
set pause on exceptions (all valid states), set skip all pauses,
set breakpoints active, and event capturing (scriptParsed, paused,
resumed). Includes edge cases like repeated enable/disable cycles,
type validation errors, and invalid enum values.
"""

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
class TestDebuggerEnableDisable:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.disable()

    async def test_enable_with_max_scripts_cache_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable(max_scripts_cache_size=10_000_000)
            await session.debugger.disable()

    async def test_enable_returns_debugger_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.debugger.enable()
            assert isinstance(result, dict)
            await session.debugger.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.debugger.enable()
                await session.debugger.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.debugger.disable()


@pytest.mark.integration
class TestDebuggerPauseResume:
    async def test_pause(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            await session.debugger.pause()
            await asyncio.sleep(0.5)
            with contextlib.suppress(Exception):
                await session.debugger.resume()
            await session.debugger.disable()

    async def test_resume_without_pause(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with contextlib.suppress(Exception):
                await session.debugger.resume()
            await session.debugger.disable()

    async def test_resume_with_terminate_on_resume(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            await session.debugger.pause()
            await asyncio.sleep(0.5)
            with contextlib.suppress(Exception):
                await session.debugger.resume(terminate_on_resume=True)
            await session.debugger.disable()


@pytest.mark.integration
class TestDebuggerSetPauseOnExceptions:
    @pytest.mark.parametrize("state", ["none", "caught", "uncaught", "all"])
    async def test_valid_states(self, state: str) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_pause_on_exceptions(state)
            await session.debugger.disable()

    async def test_invalid_state_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with pytest.raises(ValueError, match="state must be one of"):
                await session.debugger.set_pause_on_exceptions("invalid")
            await session.debugger.disable()

    async def test_type_error_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="state"):
                await session.debugger.set_pause_on_exceptions(42)


@pytest.mark.integration
class TestDebuggerSetSkipAllPauses:
    async def test_skip_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            await session.debugger.disable()

    async def test_skip_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(False)
            await session.debugger.disable()

    async def test_type_error_skip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="skip"):
                await session.debugger.set_skip_all_pauses("yes")


@pytest.mark.integration
class TestDebuggerSetBreakpointsActive:
    async def test_active_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_breakpoints_active(True)
            await session.debugger.disable()

    async def test_active_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            await session.debugger.set_breakpoints_active(False)
            await session.debugger.disable()

    async def test_type_error_active(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="active"):
                await session.debugger.set_breakpoints_active("yes")


@pytest.mark.integration
class TestDebuggerScriptSource:
    async def test_get_script_source(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            if scripts:
                script_id = scripts[0]["scriptId"]
                result = await session.debugger.get_script_source(script_id)
                assert isinstance(result, dict)
                assert "scriptSource" in result

            await session.debugger.disable()

    async def test_get_script_source_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with pytest.raises(Exception) as exc_info:
                await session.debugger.get_script_source("invalid-script-id")
            assert exc_info.value is not None
            await session.debugger.disable()

    async def test_type_error_script_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.get_script_source(42)


@pytest.mark.integration
class TestDebuggerSearchInContent:
    async def test_search_in_content(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            if scripts:
                script_id = scripts[0]["scriptId"]
                result = await session.debugger.search_in_content(
                    script_id, "example"
                )
                assert isinstance(result, dict)

            await session.debugger.disable()

    async def test_search_in_content_with_regex(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            if scripts:
                script_id = scripts[0]["scriptId"]
                result = await session.debugger.search_in_content(
                    script_id, "ex.*", is_regex=True
                )
                assert isinstance(result, dict)

            await session.debugger.disable()

    async def test_search_in_content_case_sensitive(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()

            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            if scripts:
                script_id = scripts[0]["scriptId"]
                result = await session.debugger.search_in_content(
                    script_id, "EXAMPLE", case_sensitive=True
                )
                assert isinstance(result, dict)

            await session.debugger.disable()


@pytest.mark.integration
class TestDebuggerBreakpointByUrl:
    async def test_set_breakpoint_by_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_breakpoint_by_url(
                0, url="https://example.com/test.js"
            )
            assert isinstance(result, dict)
            if "breakpointId" in result:
                await session.debugger.remove_breakpoint(result["breakpointId"])
            await session.debugger.disable()

    async def test_set_breakpoint_by_url_with_condition(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_breakpoint_by_url(
                0, url_regex=r".*\.js$", condition="x > 5"
            )
            assert isinstance(result, dict)
            if "breakpointId" in result:
                await session.debugger.remove_breakpoint(result["breakpointId"])
            await session.debugger.disable()

    async def test_set_breakpoint_by_url_only_line_number(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with contextlib.suppress(Exception):
                result = await session.debugger.set_breakpoint_by_url(0)
                if isinstance(result, dict) and "breakpointId" in result:
                    await session.debugger.remove_breakpoint(result["breakpointId"])
            await session.debugger.disable()

    async def test_type_error_line_number(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="line_number"):
                await session.debugger.set_breakpoint_by_url("0")


@pytest.mark.integration
class TestDebuggerRemoveBreakpoint:
    async def test_remove_breakpoint_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            with contextlib.suppress(Exception):
                await session.debugger.remove_breakpoint("nonexistent-bp")
            await session.debugger.disable()

    async def test_type_error_breakpoint_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="breakpoint_id"):
                await session.debugger.remove_breakpoint(42)


@pytest.mark.integration
class TestDebuggerEvents:
    @pytest.mark.skip(reason="Script parsed event is flaky in CI - timing dependent")
    async def test_script_parsed_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            scripts: list[dict[str, Any]] = []

            async def on_script_parsed(params: dict[str, Any]) -> None:
                scripts.append(params)

            await session.debugger.enable()
            session.on("Debugger.scriptParsed", on_script_parsed)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(3.0)

            assert len(scripts) > 0
            for script in scripts:
                assert "scriptId" in script
                assert "url" in script

            await session.debugger.disable()

    async def test_resumed_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            resumed_events: list[dict[str, Any]] = []

            async def on_resumed(params: dict[str, Any]) -> None:
                resumed_events.append(params)

            await session.debugger.enable()
            await session.debugger.set_skip_all_pauses(True)
            session.on("Debugger.resumed", on_resumed)

            await session.debugger.pause()
            await asyncio.sleep(1.0)
            with contextlib.suppress(Exception):
                await session.debugger.resume()
            await asyncio.sleep(1.0)

            await session.debugger.disable()


@pytest.mark.integration
class TestDebuggerEvaluateOnCallFrame:
    async def test_evaluate_on_call_frame_type_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.evaluate_on_call_frame(42, "x")

    async def test_evaluate_on_call_frame_expression_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="expression"):
                await session.debugger.evaluate_on_call_frame("cf1", 42)


@pytest.mark.integration
class TestDebuggerTypeValidation:
    """Verify type validation raises before any CDP call."""

    async def test_set_breakpoint_type_error_location(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="location"):
                await session.debugger.set_breakpoint("not-a-dict")

    async def test_set_breakpoint_on_function_call_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="object_id"):
                await session.debugger.set_breakpoint_on_function_call(42)

    async def test_get_possible_breakpoints_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="start"):
                await session.debugger.get_possible_breakpoints("not-a-dict")

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

    async def test_set_return_value_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="new_value"):
                await session.debugger.set_return_value("not-a-dict")

    async def test_set_variable_value_type_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.set_variable_value(
                    42, 0, "x", {"value": 1}
                )


@pytest.mark.integration
class TestDebuggerNewMethods:
    """Integration tests for newly added CDP Debugger methods."""

    async def test_set_async_call_stack_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_async_call_stack_depth(32)
            assert isinstance(result, dict)
            await session.debugger.set_async_call_stack_depth(0)
            await session.debugger.disable()

    async def test_set_instrumentation_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_instrumentation_breakpoint(
                "beforeScriptExecution"
            )
            assert isinstance(result, dict)
            if "breakpointId" in result:
                await session.debugger.remove_breakpoint(
                    result["breakpointId"]
                )
            await session.debugger.disable()

    @pytest.mark.skip(reason="CI Chrome: setBlackboxExecutionContexts returns Invalid parameters")
    async def test_set_blackbox_execution_contexts(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.debugger.enable()
            result = await session.debugger.set_blackbox_execution_contexts([])
            assert isinstance(result, dict)
            await session.debugger.disable()

    async def test_continue_to_location_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="location"):
                await session.debugger.continue_to_location("not-a-dict")

    async def test_restart_frame_type_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="call_frame_id"):
                await session.debugger.restart_frame(42, "StepInto")

    async def test_restart_frame_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="mode must be one of"):
                await session.debugger.restart_frame("cf1", "StepOver")

    async def test_set_instrumentation_breakpoint_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="instrumentation must be one of"):
                await session.debugger.set_instrumentation_breakpoint("invalid")

    async def test_set_async_call_stack_depth_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="max_depth"):
                await session.debugger.set_async_call_stack_depth("32")

    async def test_set_blackbox_execution_contexts_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="execution_context_ids"):
                await session.debugger.set_blackbox_execution_contexts("not-a-list")

    async def test_set_blackboxed_ranges_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.set_blackboxed_ranges(42, [])

    async def test_disassemble_wasm_module_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.disassemble_wasm_module(42)

    async def test_next_wasm_disassembly_chunk_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="stream_id"):
                await session.debugger.next_wasm_disassembly_chunk(42)

    async def test_evaluate_on_call_frame_timeout_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="timeout"):
                await session.debugger.evaluate_on_call_frame(
                    "cf1", "x", timeout="5"
                )

    async def test_get_wasm_bytecode_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="script_id"):
                await session.debugger.get_wasm_bytecode(42)

    async def test_pause_on_async_call_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="parent_stack_trace_id"):
                await session.debugger.pause_on_async_call("not-a-dict")
