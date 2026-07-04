"""Debugger domain: breakpoints, stepping, and script inspection."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DebuggerDomain(BaseDomain):
    """Wrapper for the CDP Debugger domain.

    Provides breakpoint management, stepping controls, script parsing,
    and evaluation on call frames for JavaScript debugging.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Debugger domain."""
        return await self._call("Debugger.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Debugger domain."""
        return await self._call("Debugger.disable")

    async def pause(self) -> dict[str, Any]:
        """Pause script execution on the next JavaScript statement."""
        return await self._call("Debugger.pause")

    async def resume(self) -> dict[str, Any]:
        """Resume script execution after a pause."""
        return await self._call("Debugger.resume")

    async def step_over(self) -> dict[str, Any]:
        """Step over the next function call."""
        return await self._call("Debugger.stepOver")

    async def step_into(self) -> dict[str, Any]:
        """Step into the next function call."""
        return await self._call("Debugger.stepInto")

    async def step_out(self) -> dict[str, Any]:
        """Step out of the current function."""
        return await self._call("Debugger.stepOut")

    async def set_breakpoint(
        self,
        location: dict[str, Any],
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Set a breakpoint at a script location.

        Args:
            location: Dict with ``scriptId``, ``lineNumber``, and
                optional ``columnNumber``.
            condition: Optional breakpoint condition expression.

        Returns:
            Dict with ``breakpointId`` and the actual ``locations`` list.
        """
        params: dict[str, Any] = {"location": location}
        if condition is not None:
            params["condition"] = condition
        return await self._call("Debugger.setBreakpoint", params)

    async def set_breakpoint_by_url(
        self,
        url: str,
        line_number: int,
        column_number: int | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Set a breakpoint by script URL.

        Args:
            url: Script URL to set the breakpoint in.
            line_number: Zero-based line number.
            column_number: Optional zero-based column number.
            condition: Optional breakpoint condition expression.

        Returns:
            Dict with ``breakpointId`` and ``locations`` list.
        """
        params: dict[str, Any] = {"url": url, "lineNumber": line_number}
        if column_number is not None:
            params["columnNumber"] = column_number
        if condition is not None:
            params["condition"] = condition
        return await self._call("Debugger.setBreakpointByUrl", params)

    async def remove_breakpoint(self, breakpoint_id: str) -> dict[str, Any]:
        """Remove a breakpoint by ID.

        Args:
            breakpoint_id: The breakpoint ID returned by set_breakpoint.
        """
        return await self._call(
            "Debugger.removeBreakpoint",
            {"breakpointId": breakpoint_id},
        )

    async def set_pause_on_exceptions(
        self,
        state: str,
    ) -> dict[str, Any]:
        """Set pause on exceptions mode.

        Args:
            state: ``"none"``, ``"uncaught"``, or ``"all"``.
        """
        return await self._call(
            "Debugger.setPauseOnExceptions",
            {"state": state},
        )

    async def evaluate_on_call_frame(
        self,
        call_frame_id: str,
        expression: str,
        object_group: str | None = None,
        include_command_line_api: bool | None = None,
        silent: bool | None = None,
        return_by_value: bool | None = None,
        generate_preview: bool | None = None,
        throw_on_side_effect: bool | None = None,
    ) -> dict[str, Any]:
        """Evaluate an expression in the context of a call frame.

        Args:
            call_frame_id: Call frame ID from the current pause state.
            expression: JavaScript expression to evaluate.
            object_group: Optional object group name.
            include_command_line_api: Whether to include command line API.
            silent: Whether to suppress exceptions.
            return_by_value: Whether to return by value.
            generate_preview: Whether to generate preview.
            throw_on_side_effect: Whether to throw on side effects.

        Returns:
            Dict with ``result``, ``exceptionDetails`` (if any).
        """
        params: dict[str, Any] = {
            "callFrameId": call_frame_id,
            "expression": expression,
        }
        if object_group is not None:
            params["objectGroup"] = object_group
        if include_command_line_api is not None:
            params["includeCommandLineAPI"] = include_command_line_api
        if silent is not None:
            params["silent"] = silent
        if return_by_value is not None:
            params["returnByValue"] = return_by_value
        if generate_preview is not None:
            params["generatePreview"] = generate_preview
        if throw_on_side_effect is not None:
            params["throwOnSideEffect"] = throw_on_side_effect
        return await self._call("Debugger.evaluateOnCallFrame", params)

    async def get_script_source(
        self,
        script_id: str,
    ) -> dict[str, Any]:
        """Get the source code of a script.

        Args:
            script_id: Script ID from ``Debugger.scriptParsed`` event.

        Returns:
            Dict with ``scriptSource`` string.
        """
        return await self._call(
            "Debugger.getScriptSource",
            {"scriptId": script_id},
        )

    async def get_stack_trace(self) -> dict[str, Any]:
        """Get the current call stack trace.

        Returns:
            Dict with ``stackTrace`` containing ``callFrames``.
        """
        return await self._call("Debugger.getStackTrace", {})

    async def get_possible_breakpoints(
        self,
        start: dict[str, Any],
        end: dict[str, Any] | None = None,
        restrict_to_function: bool | None = None,
    ) -> dict[str, Any]:
        """Get possible breakpoint locations for a range.

        Args:
            start: Start location dict with ``scriptId``, ``lineNumber``.
            end: Optional end location dict.
            restrict_to_function: Whether to restrict to the current function.

        Returns:
            Dict with ``locations`` list.
        """
        params: dict[str, Any] = {"start": start}
        if end is not None:
            params["end"] = end
        if restrict_to_function is not None:
            params["restrictToFunction"] = restrict_to_function
        return await self._call("Debugger.getPossibleBreakpoints", params)

    async def set_skip_all_pauses(self, skip: bool) -> dict[str, Any]:
        """Skip all pauses until further notice.

        Args:
            skip: Whether to skip all pauses.
        """
        return await self._call(
            "Debugger.setSkipAllPauses",
            {"skip": skip},
        )
