"""Unit tests for the Debugger domain.

Covers all 25 Debugger commands with FakeSender — parameter
verification, type/enum validation, optional-bool omission, return
values, CommandError propagation, method parity, coroutine checks,
concurrency, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise CommandError(self._code, self._message)


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Debugger.disable"

    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = DebuggerDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "Debugger.enable"

    async def test_params_none_when_no_args(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_max_scripts_cache_size(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.enable(max_scripts_cache_size=10000)
        _, params = fake.last_call
        assert params is not None
        assert params["maxScriptsCacheSize"] == 10000

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.enable(max_scripts_cache_size=10000)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"maxScriptsCacheSize"}

    async def test_type_error_max_scripts_cache_size(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="max_scripts_cache_size"):
            await domain.enable(max_scripts_cache_size="10000")  # type: ignore[arg-type]

    async def test_returns_response(self) -> None:
        fake = FakeSender({"debuggerId": "dbg-1"})
        domain = DebuggerDomain(fake)
        result = await domain.enable()
        assert result == {"debuggerId": "dbg-1"}


# ---------------------------------------------------------------------------
# pause
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPause:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.pause()
        method, _ = fake.last_call
        assert method == "Debugger.pause"

    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.pause()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# resume
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestResume:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume()
        method, _ = fake.last_call
        assert method == "Debugger.resume"

    async def test_params_none_when_no_args(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume()
        _, params = fake.last_call
        assert params is None

    async def test_terminate_on_resume_true(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume(terminate_on_resume=True)
        _, params = fake.last_call
        assert params is not None
        assert params["terminateOnResume"] is True

    async def test_terminate_on_resume_false(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume(terminate_on_resume=False)
        _, params = fake.last_call
        assert params is not None
        assert params["terminateOnResume"] is False

    async def test_terminate_on_resume_omitted_when_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume(terminate_on_resume=None)
        _, params = fake.last_call
        assert params is None

    async def test_type_error_terminate_on_resume(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="terminate_on_resume"):
            await domain.resume(terminate_on_resume="yes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# step_into
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStepInto:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_into()
        method, _ = fake.last_call
        assert method == "Debugger.stepInto"

    async def test_params_none_when_no_args(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_into()
        _, params = fake.last_call
        assert params is None

    async def test_break_on_async_call(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_into(break_on_async_call=True)
        _, params = fake.last_call
        assert params is not None
        assert params["breakOnAsyncCall"] is True

    async def test_skip_list(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        skip = [{"scriptId": "s1", "lineNumber": 0, "endLineNumber": 5}]
        await domain.step_into(skip_list=skip)
        _, params = fake.last_call
        assert params is not None
        assert params["skipList"] == skip

    async def test_both_params(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        skip = [{"scriptId": "s1", "lineNumber": 0}]
        await domain.step_into(break_on_async_call=False, skip_list=skip)
        _, params = fake.last_call
        assert params is not None
        assert params["breakOnAsyncCall"] is False
        assert params["skipList"] == skip

    async def test_type_error_break_on_async_call(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="break_on_async_call"):
            await domain.step_into(break_on_async_call="yes")  # type: ignore[arg-type]

    async def test_type_error_skip_list(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="skip_list"):
            await domain.step_into(skip_list="not-a-list")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# step_out
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStepOut:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_out()
        method, _ = fake.last_call
        assert method == "Debugger.stepOut"

    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_out()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# step_over
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStepOver:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_over()
        method, _ = fake.last_call
        assert method == "Debugger.stepOver"

    async def test_params_none_when_no_args(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_over()
        _, params = fake.last_call
        assert params is None

    async def test_skip_list(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        skip = [{"scriptId": "s1", "lineNumber": 0}]
        await domain.step_over(skip_list=skip)
        _, params = fake.last_call
        assert params is not None
        assert params["skipList"] == skip

    async def test_type_error_skip_list(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="skip_list"):
            await domain.step_over(skip_list=42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_breakpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBreakpoint:
    async def test_method(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "location": {}})
        domain = DebuggerDomain(fake)
        loc = {"scriptId": "s1", "lineNumber": 10}
        await domain.set_breakpoint(loc)
        method, _ = fake.last_call
        assert method == "Debugger.setBreakpoint"

    async def test_required_location(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "location": {}})
        domain = DebuggerDomain(fake)
        loc = {"scriptId": "s1", "lineNumber": 10, "columnNumber": 5}
        await domain.set_breakpoint(loc)
        _, params = fake.last_call
        assert params is not None
        assert params["location"] == loc

    async def test_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "location": {}})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 0}, condition="x > 5")
        _, params = fake.last_call
        assert params is not None
        assert params["condition"] == "x > 5"

    async def test_condition_omitted_when_none(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "location": {}})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 0})
        _, params = fake.last_call
        assert params is not None
        assert "condition" not in params

    async def test_type_error_location(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="location"):
            await domain.set_breakpoint("not-a-dict")  # type: ignore[arg-type]

    async def test_type_error_condition(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="condition"):
            await domain.set_breakpoint(
                {"scriptId": "s1", "lineNumber": 0}, condition=42  # type: ignore[arg-type]
            )

    async def test_returns_response(self) -> None:
        resp = {"breakpointId": "bp1", "location": {"scriptId": "s1", "lineNumber": 10}}
        fake = FakeSender(resp)
        domain = DebuggerDomain(fake)
        result = await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 10})
        assert result == resp


# ---------------------------------------------------------------------------
# set_breakpoint_by_url
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBreakpointByUrl:
    async def test_method(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(10, url="https://example.com/test.js")
        method, _ = fake.last_call
        assert method == "Debugger.setBreakpointByUrl"

    async def test_required_line_number(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(42)
        _, params = fake.last_call
        assert params is not None
        assert params["lineNumber"] == 42

    async def test_url(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0, url="https://example.com/test.js")
        _, params = fake.last_call
        assert params is not None
        assert params["url"] == "https://example.com/test.js"

    async def test_url_regex(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0, url_regex=r".*test\.js$")
        _, params = fake.last_call
        assert params is not None
        assert params["urlRegex"] == r".*test\.js$"

    async def test_script_hash(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0, script_hash="abc123")
        _, params = fake.last_call
        assert params is not None
        assert params["scriptHash"] == "abc123"

    async def test_column_number(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0, url="https://example.com/test.js", column_number=5)
        _, params = fake.last_call
        assert params is not None
        assert params["columnNumber"] == 5

    async def test_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0, url="https://example.com/test.js", condition="x > 5")
        _, params = fake.last_call
        assert params is not None
        assert params["condition"] == "x > 5"

    async def test_all_params(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(
            10,
            url="https://example.com/test.js",
            url_regex=None,
            script_hash=None,
            column_number=3,
            condition="i === 0",
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"lineNumber", "url", "columnNumber", "condition"}

    async def test_only_line_number(self) -> None:
        fake = FakeSender({"breakpointId": "bp1", "locations": []})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_by_url(0)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"lineNumber"}

    async def test_type_error_line_number(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="line_number"):
            await domain.set_breakpoint_by_url("10")  # type: ignore[arg-type]

    async def test_type_error_url(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="url"):
            await domain.set_breakpoint_by_url(0, url=42)  # type: ignore[arg-type]

    async def test_type_error_column_number(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="column_number"):
            await domain.set_breakpoint_by_url(0, column_number="5")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_breakpoint_on_function_call
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBreakpointOnFunctionCall:
    async def test_method(self) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj-1")
        method, _ = fake.last_call
        assert method == "Debugger.setBreakpointOnFunctionCall"

    async def test_required_object_id(self) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj-1")
        _, params = fake.last_call
        assert params is not None
        assert params["objectId"] == "obj-1"

    async def test_condition(self) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj-1", condition="x > 5")
        _, params = fake.last_call
        assert params is not None
        assert params["condition"] == "x > 5"

    async def test_condition_omitted_when_none(self) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint_on_function_call("obj-1")
        _, params = fake.last_call
        assert params is not None
        assert "condition" not in params

    async def test_type_error_object_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="object_id"):
            await domain.set_breakpoint_on_function_call(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_breakpoints_active
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBreakpointsActive:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoints_active(True)
        method, _ = fake.last_call
        assert method == "Debugger.setBreakpointsActive"

    async def test_active_true(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoints_active(True)
        _, params = fake.last_call
        assert params is not None
        assert params["active"] is True

    async def test_active_false(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoints_active(False)
        _, params = fake.last_call
        assert params is not None
        assert params["active"] is False

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="active"):
            await domain.set_breakpoints_active("yes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# evaluate_on_call_frame
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEvaluateOnCallFrame:
    async def test_method(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "1 + 1")
        method, _ = fake.last_call
        assert method == "Debugger.evaluateOnCallFrame"

    async def test_required_params(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "1 + 1")
        _, params = fake.last_call
        assert params is not None
        assert params["callFrameId"] == "cf1"
        assert params["expression"] == "1 + 1"

    async def test_object_group(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", object_group="console")
        _, params = fake.last_call
        assert params is not None
        assert params["objectGroup"] == "console"

    async def test_include_command_line_api(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", include_command_line_api=True)
        _, params = fake.last_call
        assert params is not None
        assert params["includeCommandLineAPI"] is True

    async def test_silent(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", silent=True)
        _, params = fake.last_call
        assert params is not None
        assert params["silent"] is True

    async def test_return_by_value(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", return_by_value=True)
        _, params = fake.last_call
        assert params is not None
        assert params["returnByValue"] is True

    async def test_generate_preview(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", generate_preview=True)
        _, params = fake.last_call
        assert params is not None
        assert params["generatePreview"] is True

    async def test_throw_on_side_effect(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", throw_on_side_effect=True)
        _, params = fake.last_call
        assert params is not None
        assert params["throwOnSideEffect"] is True

    async def test_all_bools_false(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame(
            "cf1", "x",
            include_command_line_api=False,
            silent=False,
            return_by_value=False,
            generate_preview=False,
            throw_on_side_effect=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["includeCommandLineAPI"] is False
        assert params["silent"] is False
        assert params["returnByValue"] is False
        assert params["generatePreview"] is False
        assert params["throwOnSideEffect"] is False

    async def test_all_optionals_omitted_when_none(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"callFrameId", "expression"}

    async def test_type_error_call_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="call_frame_id"):
            await domain.evaluate_on_call_frame(42, "x")  # type: ignore[arg-type]

    async def test_type_error_expression(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="expression"):
            await domain.evaluate_on_call_frame("cf1", 42)  # type: ignore[arg-type]

    async def test_type_error_object_group(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="object_group"):
            await domain.evaluate_on_call_frame("cf1", "x", object_group=42)  # type: ignore[arg-type]

    async def test_type_error_include_command_line_api(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="include_command_line_api"):
            await domain.evaluate_on_call_frame(
                "cf1", "x", include_command_line_api="yes"  # type: ignore[arg-type]
            )

    async def test_type_error_silent(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="silent"):
            await domain.evaluate_on_call_frame("cf1", "x", silent="yes")  # type: ignore[arg-type]

    async def test_type_error_throw_on_side_effect(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="throw_on_side_effect"):
            await domain.evaluate_on_call_frame(
                "cf1", "x", throw_on_side_effect="yes"  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# get_possible_breakpoints
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetPossibleBreakpoints:
    async def test_method(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        await domain.get_possible_breakpoints(start)
        method, _ = fake.last_call
        assert method == "Debugger.getPossibleBreakpoints"

    async def test_required_start(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        await domain.get_possible_breakpoints(start)
        _, params = fake.last_call
        assert params is not None
        assert params["start"] == start

    async def test_end(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        start = {"scriptId": "s1", "lineNumber": 0}
        end = {"scriptId": "s1", "lineNumber": 10}
        await domain.get_possible_breakpoints(start, end=end)
        _, params = fake.last_call
        assert params is not None
        assert params["end"] == end

    async def test_restrict_to_function(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        await domain.get_possible_breakpoints(
            {"scriptId": "s1", "lineNumber": 0}, restrict_to_function=True
        )
        _, params = fake.last_call
        assert params is not None
        assert params["restrictToFunction"] is True

    async def test_optionals_omitted_when_none(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        await domain.get_possible_breakpoints({"scriptId": "s1", "lineNumber": 0})
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"start"}

    async def test_type_error_start(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="start"):
            await domain.get_possible_breakpoints("not-a-dict")  # type: ignore[arg-type]

    async def test_type_error_end(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="end"):
            await domain.get_possible_breakpoints(
                {"scriptId": "s1", "lineNumber": 0}, end="not-a-dict"  # type: ignore[arg-type]
            )

    async def test_type_error_restrict_to_function(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="restrict_to_function"):
            await domain.get_possible_breakpoints(
                {"scriptId": "s1", "lineNumber": 0}, restrict_to_function="yes"  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# get_script_source
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetScriptSource:
    async def test_method(self) -> None:
        fake = FakeSender({"scriptSource": "var x = 1;"})
        domain = DebuggerDomain(fake)
        await domain.get_script_source("s1")
        method, _ = fake.last_call
        assert method == "Debugger.getScriptSource"

    async def test_required_script_id(self) -> None:
        fake = FakeSender({"scriptSource": "var x = 1;"})
        domain = DebuggerDomain(fake)
        await domain.get_script_source("s1")
        _, params = fake.last_call
        assert params is not None
        assert params["scriptId"] == "s1"

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.get_script_source(42)  # type: ignore[arg-type]

    async def test_returns_response(self) -> None:
        fake = FakeSender({"scriptSource": "var x = 1;"})
        domain = DebuggerDomain(fake)
        result = await domain.get_script_source("s1")
        assert result == {"scriptSource": "var x = 1;"}


# ---------------------------------------------------------------------------
# get_stack_trace
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetStackTrace:
    async def test_method(self) -> None:
        fake = FakeSender({"stackTrace": {"callFrames": []}})
        domain = DebuggerDomain(fake)
        await domain.get_stack_trace({"id": "st1"})
        method, _ = fake.last_call
        assert method == "Debugger.getStackTrace"

    async def test_required_stack_trace_id(self) -> None:
        fake = FakeSender({"stackTrace": {"callFrames": []}})
        domain = DebuggerDomain(fake)
        stid = {"id": "st1", "debuggerId": "dbg1"}
        await domain.get_stack_trace(stid)
        _, params = fake.last_call
        assert params is not None
        assert params["stackTraceId"] == stid

    async def test_type_error_stack_trace_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="stack_trace_id"):
            await domain.get_stack_trace("not-a-dict")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# remove_breakpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRemoveBreakpoint:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.remove_breakpoint("bp1")
        method, _ = fake.last_call
        assert method == "Debugger.removeBreakpoint"

    async def test_required_breakpoint_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.remove_breakpoint("bp1")
        _, params = fake.last_call
        assert params is not None
        assert params["breakpointId"] == "bp1"

    async def test_type_error_breakpoint_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="breakpoint_id"):
            await domain.remove_breakpoint(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# search_in_content
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSearchInContent:
    async def test_method(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test")
        method, _ = fake.last_call
        assert method == "Debugger.searchInContent"

    async def test_required_params(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test")
        _, params = fake.last_call
        assert params is not None
        assert params["scriptId"] == "s1"
        assert params["query"] == "test"

    async def test_case_sensitive_true(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test", case_sensitive=True)
        _, params = fake.last_call
        assert params is not None
        assert params["caseSensitive"] is True

    async def test_case_sensitive_false(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test", case_sensitive=False)
        _, params = fake.last_call
        assert params is not None
        assert params["caseSensitive"] is False

    async def test_is_regex_true(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test", is_regex=True)
        _, params = fake.last_call
        assert params is not None
        assert params["isRegex"] is True

    async def test_optionals_omitted_when_none(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"scriptId", "query"}

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.search_in_content(42, "test")  # type: ignore[arg-type]

    async def test_type_error_query(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="query"):
            await domain.search_in_content("s1", 42)  # type: ignore[arg-type]

    async def test_type_error_case_sensitive(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="case_sensitive"):
            await domain.search_in_content("s1", "test", case_sensitive="yes")  # type: ignore[arg-type]

    async def test_type_error_is_regex(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="is_regex"):
            await domain.search_in_content("s1", "test", is_regex="yes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_blackbox_patterns
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBlackboxPatterns:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns([".*node_modules.*"])
        method, _ = fake.last_call
        assert method == "Debugger.setBlackboxPatterns"

    async def test_required_patterns(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        patterns = [".*vendor.*", ".*test.*"]
        await domain.set_blackbox_patterns(patterns)
        _, params = fake.last_call
        assert params is not None
        assert params["patterns"] == patterns

    async def test_skip_anonymous_true(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns([".*"], skip_anonymous=True)
        _, params = fake.last_call
        assert params is not None
        assert params["skipAnonymous"] is True

    async def test_skip_anonymous_omitted_when_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns([".*"])
        _, params = fake.last_call
        assert params is not None
        assert "skipAnonymous" not in params

    async def test_type_error_patterns(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="patterns"):
            await domain.set_blackbox_patterns("not-a-list")  # type: ignore[arg-type]

    async def test_type_error_skip_anonymous(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="skip_anonymous"):
            await domain.set_blackbox_patterns([".*"], skip_anonymous="yes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_pause_on_exceptions
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetPauseOnExceptions:
    @pytest.mark.parametrize("state", ["none", "caught", "uncaught", "all"])
    async def test_valid_states(self, state: str) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_pause_on_exceptions(state)
        method, params = fake.last_call
        assert method == "Debugger.setPauseOnExceptions"
        assert params is not None
        assert params["state"] == state

    async def test_type_error_state(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="state"):
            await domain.set_pause_on_exceptions(42)  # type: ignore[arg-type]

    @pytest.mark.parametrize("invalid", ["", "None", "NONE", "All", "caught ", "UNCAUGHT"])
    async def test_value_error_invalid_state(self, invalid: str) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(ValueError, match="state must be one of"):
            await domain.set_pause_on_exceptions(invalid)


# ---------------------------------------------------------------------------
# set_return_value
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetReturnValue:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_return_value({"value": 42})
        method, _ = fake.last_call
        assert method == "Debugger.setReturnValue"

    async def test_required_new_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        val = {"value": 42, "type": "number"}
        await domain.set_return_value(val)
        _, params = fake.last_call
        assert params is not None
        assert params["newValue"] == val

    async def test_type_error_new_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="new_value"):
            await domain.set_return_value("not-a-dict")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_script_source
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetScriptSource:
    async def test_method(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;")
        method, _ = fake.last_call
        assert method == "Debugger.setScriptSource"

    async def test_required_params(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;")
        _, params = fake.last_call
        assert params is not None
        assert params["scriptId"] == "s1"
        assert params["source"] == "var x = 1;"

    async def test_dry_run_true(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;", dry_run=True)
        _, params = fake.last_call
        assert params is not None
        assert params["dryRun"] is True

    async def test_dry_run_false(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;", dry_run=False)
        _, params = fake.last_call
        assert params is not None
        assert params["dryRun"] is False

    async def test_allow_top_frame_editing(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;", allow_top_frame_editing=True)
        _, params = fake.last_call
        assert params is not None
        assert params["allowTopFrameEditing"] is True

    async def test_optionals_omitted_when_none(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "var x = 1;")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"scriptId", "source"}

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.set_script_source(42, "x")  # type: ignore[arg-type]

    async def test_type_error_source(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="source"):
            await domain.set_script_source("s1", 42)  # type: ignore[arg-type]

    async def test_type_error_dry_run(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="dry_run"):
            await domain.set_script_source("s1", "x", dry_run="yes")  # type: ignore[arg-type]

    async def test_type_error_allow_top_frame_editing(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="allow_top_frame_editing"):
            await domain.set_script_source(
                "s1", "x", allow_top_frame_editing="yes"  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# set_skip_all_pauses
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetSkipAllPauses:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_skip_all_pauses(True)
        method, _ = fake.last_call
        assert method == "Debugger.setSkipAllPauses"

    async def test_skip_true(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_skip_all_pauses(True)
        _, params = fake.last_call
        assert params is not None
        assert params["skip"] is True

    async def test_skip_false(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_skip_all_pauses(False)
        _, params = fake.last_call
        assert params is not None
        assert params["skip"] is False

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="skip"):
            await domain.set_skip_all_pauses("yes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_variable_value
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetVariableValue:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_variable_value("cf1", 0, "x", {"value": 42})
        method, _ = fake.last_call
        assert method == "Debugger.setVariableValue"

    async def test_all_required_params(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_variable_value("cf1", 2, "myVar", {"value": 42})
        _, params = fake.last_call
        assert params is not None
        assert params["callFrameId"] == "cf1"
        assert params["scopeNumber"] == 2
        assert params["variableName"] == "myVar"
        assert params["newValue"] == {"value": 42}

    async def test_type_error_call_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="call_frame_id"):
            await domain.set_variable_value(42, 0, "x", {"value": 1})  # type: ignore[arg-type]

    async def test_type_error_scope_number(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="scope_number"):
            await domain.set_variable_value("cf1", "0", "x", {"value": 1})  # type: ignore[arg-type]

    async def test_type_error_variable_name(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="variable_name"):
            await domain.set_variable_value("cf1", 0, 42, {"value": 1})  # type: ignore[arg-type]

    async def test_type_error_new_value(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="new_value"):
            await domain.set_variable_value("cf1", 0, "x", "not-a-dict")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Method parity, signatures, and structural tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    def test_inherits_basedomain(self) -> None:
        assert issubclass(DebuggerDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        methods = [
            "continue_to_location", "disable", "disassemble_wasm_module",
            "enable", "evaluate_on_call_frame",
            "get_possible_breakpoints", "get_script_source",
            "get_stack_trace", "get_wasm_bytecode",
            "next_wasm_disassembly_chunk",
            "pause", "pause_on_async_call",
            "remove_breakpoint", "restart_frame", "resume",
            "search_in_content",
            "set_async_call_stack_depth",
            "set_blackbox_execution_contexts", "set_blackbox_patterns",
            "set_blackboxed_ranges",
            "set_breakpoint", "set_breakpoint_by_url",
            "set_breakpoint_on_function_call", "set_breakpoints_active",
            "set_instrumentation_breakpoint",
            "set_pause_on_exceptions",
            "set_return_value", "set_script_source",
            "set_skip_all_pauses", "set_variable_value",
            "step_into", "step_out", "step_over",
        ]
        for name in methods:
            attr = getattr(DebuggerDomain, name)
            assert inspect.iscoroutinefunction(attr), f"{name} is not a coroutine"

    def test_no_extra_methods_beyond_expected(self) -> None:
        expected = {
            "continue_to_location", "disable", "disassemble_wasm_module",
            "enable", "evaluate_on_call_frame",
            "get_possible_breakpoints", "get_script_source",
            "get_stack_trace", "get_wasm_bytecode",
            "next_wasm_disassembly_chunk",
            "pause", "pause_on_async_call",
            "remove_breakpoint", "restart_frame", "resume",
            "search_in_content",
            "set_async_call_stack_depth",
            "set_blackbox_execution_contexts", "set_blackbox_patterns",
            "set_blackboxed_ranges",
            "set_breakpoint", "set_breakpoint_by_url",
            "set_breakpoint_on_function_call", "set_breakpoints_active",
            "set_instrumentation_breakpoint",
            "set_pause_on_exceptions",
            "set_return_value", "set_script_source",
            "set_skip_all_pauses", "set_variable_value",
            "step_into", "step_out", "step_over",
        }
        actual = {
            name for name, val in inspect.getmembers(DebuggerDomain, predicate=inspect.isfunction)
            if not name.startswith("_") and not name.startswith("test")
        }
        extra = actual - expected
        missing = expected - actual
        assert actual == expected, f"Unexpected: {extra}, missing: {missing}"


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagation:
    async def test_command_error_disable(self) -> None:
        domain = DebuggerDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.disable()

    async def test_command_error_enable(self) -> None:
        domain = DebuggerDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.enable()

    async def test_command_error_set_breakpoint(self) -> None:
        domain = DebuggerDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 0})

    async def test_command_error_evaluate_on_call_frame(self) -> None:
        domain = DebuggerDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.evaluate_on_call_frame("cf1", "x")

    async def test_command_error_set_pause_on_exceptions(self) -> None:
        domain = DebuggerDomain(ErrorSender())
        with pytest.raises(CommandError):
            await domain.set_pause_on_exceptions("none")


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_concurrent_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await asyncio.gather(domain.enable(), domain.disable())
        assert len(fake.calls) == 2
        assert fake.calls[0][0] == "Debugger.enable"
        assert fake.calls[1][0] == "Debugger.disable"

    async def test_concurrent_set_breakpoints(self) -> None:
        fake = FakeSender({"breakpointId": "bp", "location": {}})
        domain = DebuggerDomain(fake)
        loc = {"scriptId": "s1", "lineNumber": 0}
        await asyncio.gather(
            domain.set_breakpoint(loc),
            domain.set_breakpoint(loc),
            domain.set_breakpoint(loc),
        )
        assert len(fake.calls) == 3
        for _, params in fake.calls:
            assert params is not None
            assert params["location"] == loc


# ---------------------------------------------------------------------------
# Optional bool edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOptionalBoolEdgeCases:
    """Verify optional bools are only sent when explicitly passed, not when None."""

    async def test_resume_false_is_sent(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.resume(terminate_on_resume=False)
        _, params = fake.last_call
        assert params is not None
        assert params["terminateOnResume"] is False

    async def test_step_into_false_break_on_async_call_is_sent(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.step_into(break_on_async_call=False)
        _, params = fake.last_call
        assert params is not None
        assert params["breakOnAsyncCall"] is False

    async def test_search_in_content_both_bools_false(self) -> None:
        fake = FakeSender({"result": []})
        domain = DebuggerDomain(fake)
        await domain.search_in_content("s1", "test", case_sensitive=False, is_regex=False)
        _, params = fake.last_call
        assert params is not None
        assert params["caseSensitive"] is False
        assert params["isRegex"] is False

    async def test_set_blackbox_patterns_skip_anonymous_false(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_patterns([".*"], skip_anonymous=False)
        _, params = fake.last_call
        assert params is not None
        assert params["skipAnonymous"] is False

    async def test_set_script_source_dry_run_false(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "x", dry_run=False)
        _, params = fake.last_call
        assert params is not None
        assert params["dryRun"] is False

    async def test_set_script_source_allow_top_frame_editing_false(self) -> None:
        fake = FakeSender({"callFrames": [], "stackChanged": False, "status": "OK"})
        domain = DebuggerDomain(fake)
        await domain.set_script_source("s1", "x", allow_top_frame_editing=False)
        _, params = fake.last_call
        assert params is not None
        assert params["allowTopFrameEditing"] is False

    async def test_get_possible_breakpoints_restrict_to_function_false(self) -> None:
        fake = FakeSender({"locations": []})
        domain = DebuggerDomain(fake)
        await domain.get_possible_breakpoints(
            {"scriptId": "s1", "lineNumber": 0}, restrict_to_function=False
        )
        _, params = fake.last_call
        assert params is not None
        assert params["restrictToFunction"] is False


# ---------------------------------------------------------------------------
# Repetition / stability
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRepetition:
    async def test_enable_disable_repeated(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10

    async def test_set_pause_on_exceptions_all_states_repeated(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        for state in ["none", "caught", "uncaught", "all"]:
            await domain.set_pause_on_exceptions(state)
        assert len(fake.calls) == 4

    async def test_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 0})
        first = fake.calls[0][1]
        await domain.set_breakpoint({"scriptId": "s1", "lineNumber": 0})
        second = fake.calls[1][1]
        assert first is not None
        assert second is not None
        assert first is not second


# ---------------------------------------------------------------------------
# Docstring and signature checks
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDocstrings:
    def test_module_docstring_mentions_events(self) -> None:
        import cdpwave.domains.debugger as mod
        assert "Events" in mod.__doc__ or "events" in mod.__doc__

    def test_class_docstring_mentions_events(self) -> None:
        assert "Events" in DebuggerDomain.__doc__ or "events" in DebuggerDomain.__doc__

    def test_class_docstring_mentions_breakpoint(self) -> None:
        assert "breakpoint" in DebuggerDomain.__doc__.lower()

    @pytest.mark.parametrize("method_name", [
        "continue_to_location", "disable", "disassemble_wasm_module",
        "enable", "evaluate_on_call_frame",
        "get_possible_breakpoints", "get_script_source",
        "get_stack_trace", "get_wasm_bytecode",
        "next_wasm_disassembly_chunk",
        "pause", "pause_on_async_call",
        "remove_breakpoint", "restart_frame", "resume",
        "search_in_content",
        "set_async_call_stack_depth",
        "set_blackbox_execution_contexts", "set_blackbox_patterns",
        "set_blackboxed_ranges",
        "set_breakpoint", "set_breakpoint_by_url",
        "set_breakpoint_on_function_call", "set_breakpoints_active",
        "set_instrumentation_breakpoint",
        "set_pause_on_exceptions",
        "set_return_value", "set_script_source",
        "set_skip_all_pauses", "set_variable_value",
        "step_into", "step_out", "step_over",
    ])
    def test_method_has_docstring(self, method_name: str) -> None:
        method = getattr(DebuggerDomain, method_name)
        assert method.__doc__ is not None
        assert len(method.__doc__.strip()) > 10


# ---------------------------------------------------------------------------
# continue_to_location
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestContinueToLocation:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.continue_to_location(
            {"scriptId": "1", "lineNumber": 10}
        )
        method, _ = fake.last_call
        assert method == "Debugger.continueToLocation"

    async def test_required_location(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        loc = {"scriptId": "s1", "lineNumber": 5}
        await domain.continue_to_location(loc)
        _, params = fake.last_call
        assert params is not None
        assert params["location"] == loc

    async def test_target_call_frames(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.continue_to_location(
            {"scriptId": "1", "lineNumber": 0},
            target_call_frames="current",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["targetCallFrames"] == "current"

    async def test_omits_target_call_frames_when_none(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.continue_to_location({"scriptId": "1", "lineNumber": 0})
        _, params = fake.last_call
        assert params is not None
        assert "targetCallFrames" not in params

    async def test_type_error_location(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="location"):
            await domain.continue_to_location("not-a-dict")  # type: ignore[arg-type]

    async def test_type_error_target_call_frames(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="target_call_frames"):
            await domain.continue_to_location(
                {"scriptId": "1", "lineNumber": 0},
                target_call_frames=42,  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# disassemble_wasm_module
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisassembleWasmModule:
    async def test_method(self) -> None:
        fake = FakeSender({"streamId": "st1", "totalNumberOfLines": 100})
        domain = DebuggerDomain(fake)
        await domain.disassemble_wasm_module("script1")
        method, params = fake.last_call
        assert method == "Debugger.disassembleWasmModule"
        assert params == {"scriptId": "script1"}

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.disassemble_wasm_module(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# next_wasm_disassembly_chunk
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestNextWasmDisassemblyChunk:
    async def test_method(self) -> None:
        fake = FakeSender({"chunk": {"lines": []}})
        domain = DebuggerDomain(fake)
        await domain.next_wasm_disassembly_chunk("stream1")
        method, params = fake.last_call
        assert method == "Debugger.nextWasmDisassemblyChunk"
        assert params == {"streamId": "stream1"}

    async def test_type_error_stream_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="stream_id"):
            await domain.next_wasm_disassembly_chunk(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# restart_frame
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRestartFrame:
    async def test_method(self) -> None:
        fake = FakeSender({"callFrames": []})
        domain = DebuggerDomain(fake)
        await domain.restart_frame("cf1", "StepInto")
        method, params = fake.last_call
        assert method == "Debugger.restartFrame"
        assert params == {"callFrameId": "cf1", "mode": "StepInto"}

    async def test_type_error_call_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="call_frame_id"):
            await domain.restart_frame(42, "StepInto")  # type: ignore[arg-type]

    async def test_type_error_mode(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="mode"):
            await domain.restart_frame("cf1", 42)  # type: ignore[arg-type]

    async def test_value_error_invalid_mode(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(ValueError, match="mode must be one of"):
            await domain.restart_frame("cf1", "StepOver")


# ---------------------------------------------------------------------------
# set_async_call_stack_depth
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetAsyncCallStackDepth:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_async_call_stack_depth(32)
        method, params = fake.last_call
        assert method == "Debugger.setAsyncCallStackDepth"
        assert params == {"maxDepth": 32}

    async def test_zero_disables(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_async_call_stack_depth(0)
        _, params = fake.last_call
        assert params == {"maxDepth": 0}

    async def test_type_error_max_depth(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="max_depth"):
            await domain.set_async_call_stack_depth("32")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_instrumentation_breakpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetInstrumentationBreakpoint:
    @pytest.mark.parametrize("instrumentation", [
        "beforeScriptExecution",
        "beforeScriptWithSourceMapExecution",
    ])
    async def test_valid_instrumentation(
        self, instrumentation: str
    ) -> None:
        fake = FakeSender({"breakpointId": "bp1"})
        domain = DebuggerDomain(fake)
        await domain.set_instrumentation_breakpoint(instrumentation)
        method, params = fake.last_call
        assert method == "Debugger.setInstrumentationBreakpoint"
        assert params == {"instrumentation": instrumentation}

    async def test_type_error_instrumentation(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="instrumentation"):
            await domain.set_instrumentation_breakpoint(42)  # type: ignore[arg-type]

    async def test_value_error_invalid_instrumentation(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(ValueError, match="instrumentation must be one of"):
            await domain.set_instrumentation_breakpoint("invalid")


# ---------------------------------------------------------------------------
# set_blackbox_execution_contexts
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBlackboxExecutionContexts:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_execution_contexts(["ctx1", "ctx2"])
        method, params = fake.last_call
        assert method == "Debugger.setBlackboxExecutionContexts"
        assert params == {"executionContextIds": ["ctx1", "ctx2"]}

    async def test_empty_list(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        await domain.set_blackbox_execution_contexts([])
        _, params = fake.last_call
        assert params == {"executionContextIds": []}

    async def test_type_error(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="execution_context_ids"):
            await domain.set_blackbox_execution_contexts("not-a-list")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# set_blackboxed_ranges
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetBlackboxedRanges:
    async def test_method(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        positions = [{"lineNumber": 0, "columnNumber": 0}]
        await domain.set_blackboxed_ranges("s1", positions)
        method, params = fake.last_call
        assert method == "Debugger.setBlackboxedRanges"
        assert params == {"scriptId": "s1", "positions": positions}

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.set_blackboxed_ranges(42, [])  # type: ignore[arg-type]

    async def test_type_error_positions(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="positions"):
            await domain.set_blackboxed_ranges("s1", "not-a-list")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# evaluate_on_call_frame timeout
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEvaluateOnCallFrameTimeout:
    async def test_timeout_int(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", timeout=5000)
        _, params = fake.last_call
        assert params is not None
        assert params["timeout"] == 5000

    async def test_timeout_float(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x", timeout=5.5)
        _, params = fake.last_call
        assert params is not None
        assert params["timeout"] == 5.5

    async def test_omits_timeout_when_none(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        await domain.evaluate_on_call_frame("cf1", "x")
        _, params = fake.last_call
        assert params is not None
        assert "timeout" not in params

    async def test_type_error_timeout(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="timeout"):
            await domain.evaluate_on_call_frame("cf1", "x", timeout="5")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# get_wasm_bytecode
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetWasmBytecode:
    async def test_sends_correct_params(self) -> None:
        fake = FakeSender({"result": {"bytecode": "AGVzbW=="}})
        domain = DebuggerDomain(fake)
        await domain.get_wasm_bytecode("script1")
        method, params = fake.last_call
        assert method == "Debugger.getWasmBytecode"
        assert params == {"scriptId": "script1"}

    async def test_type_error_script_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="script_id"):
            await domain.get_wasm_bytecode(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# pause_on_async_call
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPauseOnAsyncCall:
    async def test_sends_correct_params(self) -> None:
        fake = FakeSender({"result": {}})
        domain = DebuggerDomain(fake)
        trace_id = {"id": "abc", "debuggerId": "dbg1"}
        await domain.pause_on_async_call(trace_id)
        method, params = fake.last_call
        assert method == "Debugger.pauseOnAsyncCall"
        assert params == {"parentStackTraceId": trace_id}

    async def test_type_error_parent_stack_trace_id(self) -> None:
        fake = FakeSender({})
        domain = DebuggerDomain(fake)
        with pytest.raises(TypeError, match="parent_stack_trace_id"):
            await domain.pause_on_async_call("not-a-dict")  # type: ignore[arg-type]
