"""Debugger domain: breakpoints, stepping, and script inspection.

Provides commands, types, and events for the Debugger domain.

Events:
    Debugger.breakpointResolved: Fired when a breakpoint is resolved
        to a script location. Params: ``breakpointId`` (string),
        ``location`` (Location).
    Debugger.paused: Fired when the virtual machine stops on a
        breakpoint, exception, or other stop criteria. Params:
        ``callFrames`` (list[CallFrame]), ``reason`` (string),
        ``data`` (object), ``hitBreakpoints`` (list[string]),
        ``asyncStackTrace`` (StackTrace), ``asyncStackTraceId``
        (StackTraceId).
    Debugger.resumed: Fired when the virtual machine resumes
        execution. No params.
    Debugger.scriptFailedToParse: Fired when the VM fails to parse
        a script. Params: ``scriptId`` (string), ``url`` (string),
        ``error`` (string), plus line/column offsets.
    Debugger.scriptParsed: Fired when the VM parses a script.
        Params: ``scriptId`` (string), ``url`` (string),
        ``startLine`` (int), ``startColumn`` (int), ``endLine`` (int),
        ``endColumn`` (int), ``executionContextId`` (int),
        ``hash`` (string), ``sourceMapURL`` (string),
        ``hasSourceURL`` (bool), ``isModule`` (bool), ``length`` (int),
        ``scriptLanguage`` (string).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DebuggerDomain(BaseDomain):
    """Wrapper for the CDP Debugger domain.

    Provides breakpoint management, stepping controls, script parsing,
    and evaluation on call frames for JavaScript debugging.

    Events:
        ``Debugger.breakpointResolved`` — fired when a breakpoint is
            resolved to a script location. Params: ``breakpointId``
            (string), ``location`` (Location).
        ``Debugger.paused`` — fired when the VM stops on a breakpoint,
            exception, or other stop criteria. Params: ``callFrames``
            (list[CallFrame]), ``reason`` (string), ``data`` (object),
            ``hitBreakpoints`` (list[string]), ``asyncStackTrace``
            (StackTrace), ``asyncStackTraceId`` (StackTraceId).
        ``Debugger.resumed`` — fired when the VM resumes execution.
            No params.
        ``Debugger.scriptFailedToParse`` — fired when the VM fails to
            parse a script. Params: ``scriptId`` (string), ``url``
            (string), ``error`` (string), plus line/column offsets.
        ``Debugger.scriptParsed`` — fired when the VM parses a script.
            Params: ``scriptId`` (string), ``url`` (string),
            ``startLine`` (int), ``startColumn`` (int), ``endLine``
            (int), ``endColumn`` (int), ``executionContextId`` (int),
            ``hash`` (string), ``sourceMapURL`` (string),
            ``hasSourceURL`` (bool), ``isModule`` (bool), ``length``
            (int), ``scriptLanguage`` (string).
    """

    async def continue_to_location(
        self,
        location: dict[str, Any],
        target_call_frames: str | None = None,
    ) -> dict[str, Any]:
        """Continue execution until a specific location is reached.

        Args:
            location: Dict with ``scriptId``, ``lineNumber``, and
                optional ``columnNumber``.
            target_call_frames: Deprecated. Controls which call frames
                to continue to. Use ``"current"`` for current only.

        Returns:
            Response dict from the CDP.
        """
        if not isinstance(location, dict):
            raise TypeError("location must be a dict")
        params: dict[str, Any] = {"location": location}
        if target_call_frames is not None:
            if not isinstance(target_call_frames, str):
                raise TypeError(
                    "target_call_frames must be a string or None"
                )
            params["targetCallFrames"] = target_call_frames
        return await self._call("Debugger.continueToLocation", params)

    async def disable(self) -> dict[str, Any]:
        """Disable the Debugger domain.

        Deactivates JavaScript debugging and removes all breakpoints.
        Call frames will no longer be reported.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Debugger.disable")

    async def disassemble_wasm_module(
        self,
        script_id: str,
    ) -> dict[str, Any]:
        """Disassemble a Wasm module and return the first chunk.

        Experimental. For large modules, returns a stream from which
        additional chunks can be read via ``next_wasm_disassembly_chunk``.

        Args:
            script_id: Id of the script to disassemble.

        Returns:
            Dict with ``streamId``, ``totalNumberOfLines``,
            ``functionBodyOffsets``, and ``chunk``.
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        return await self._call(
            "Debugger.disassembleWasmModule",
            {"scriptId": script_id},
        )

    async def enable(
        self,
        max_scripts_cache_size: int | None = None,
    ) -> dict[str, Any]:
        """Enable the Debugger domain.

        Activates JavaScript debugging, which allows setting breakpoints,
        stepping through code, and inspecting call frames. Must be called
        before using any other Debugger method.

        Args:
            max_scripts_cache_size: Maximum size in bytes of collected
                scripts the debugger can hold. No limit if omitted.

        Returns:
            Response dict from the CDP. May contain ``debuggerId``.
        """
        params: dict[str, Any] = {}
        if max_scripts_cache_size is not None:
            if not isinstance(max_scripts_cache_size, int):
                raise TypeError("max_scripts_cache_size must be an int or None")
            params["maxScriptsCacheSize"] = max_scripts_cache_size
        return await self._call("Debugger.enable", params or None)

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
        timeout: float | None = None,
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
            timeout: Terminate execution after timing out (milliseconds).

        Returns:
            Dict with ``result``, ``exceptionDetails`` (if any).
        """
        if not isinstance(call_frame_id, str):
            raise TypeError("call_frame_id must be a string")
        if not isinstance(expression, str):
            raise TypeError("expression must be a string")
        params: dict[str, Any] = {
            "callFrameId": call_frame_id,
            "expression": expression,
        }
        if object_group is not None:
            if not isinstance(object_group, str):
                raise TypeError("object_group must be a string or None")
            params["objectGroup"] = object_group
        if include_command_line_api is not None:
            if not isinstance(include_command_line_api, bool):
                raise TypeError(
                    "include_command_line_api must be a bool or None"
                )
            params["includeCommandLineAPI"] = include_command_line_api
        if silent is not None:
            if not isinstance(silent, bool):
                raise TypeError("silent must be a bool or None")
            params["silent"] = silent
        if return_by_value is not None:
            if not isinstance(return_by_value, bool):
                raise TypeError("return_by_value must be a bool or None")
            params["returnByValue"] = return_by_value
        if generate_preview is not None:
            if not isinstance(generate_preview, bool):
                raise TypeError("generate_preview must be a bool or None")
            params["generatePreview"] = generate_preview
        if throw_on_side_effect is not None:
            if not isinstance(throw_on_side_effect, bool):
                raise TypeError(
                    "throw_on_side_effect must be a bool or None"
                )
            params["throwOnSideEffect"] = throw_on_side_effect
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("timeout must be a number or None")
            params["timeout"] = timeout
        return await self._call("Debugger.evaluateOnCallFrame", params)

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
            restrict_to_function: Whether to restrict to the current
                function.

        Returns:
            Dict with ``locations`` list.
        """
        if not isinstance(start, dict):
            raise TypeError("start must be a dict")
        params: dict[str, Any] = {"start": start}
        if end is not None:
            if not isinstance(end, dict):
                raise TypeError("end must be a dict or None")
            params["end"] = end
        if restrict_to_function is not None:
            if not isinstance(restrict_to_function, bool):
                raise TypeError(
                    "restrict_to_function must be a bool or None"
                )
            params["restrictToFunction"] = restrict_to_function
        return await self._call("Debugger.getPossibleBreakpoints", params)

    async def get_script_source(
        self,
        script_id: str,
    ) -> dict[str, Any]:
        """Get the source code of a script.

        Args:
            script_id: Script ID from ``Debugger.scriptParsed`` event.

        Returns:
            Dict with ``scriptSource`` string and optional ``bytecode``
            (base64-encoded, for Wasm scripts).
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        return await self._call(
            "Debugger.getScriptSource",
            {"scriptId": script_id},
        )

    async def get_stack_trace(
        self,
        stack_trace_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Get stack trace with a given stack trace ID.

        Experimental. Returns stack trace with given ``stackTraceId``.

        Args:
            stack_trace_id: ``Runtime.StackTraceId`` dict with ``id``
                (string) and optional ``debuggerId`` (string).

        Returns:
            Dict with ``stackTrace`` containing ``callFrames``.
        """
        if not isinstance(stack_trace_id, dict):
            raise TypeError("stack_trace_id must be a dict")
        return await self._call(
            "Debugger.getStackTrace",
            {"stackTraceId": stack_trace_id},
        )

    async def get_wasm_bytecode(
        self,
        script_id: str,
    ) -> dict[str, Any]:
        """Get Wasm bytecode for a script.

        Deprecated. Use ``get_script_source`` instead.

        Args:
            script_id: Id of the Wasm script to get bytecode for.

        Returns:
            Dict with ``bytecode`` (base64-encoded string).
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        return await self._call(
            "Debugger.getWasmBytecode",
            {"scriptId": script_id},
        )

    async def next_wasm_disassembly_chunk(
        self,
        stream_id: str,
    ) -> dict[str, Any]:
        """Get the next chunk of Wasm disassembly.

        Experimental. If disassembly is complete, the stream ID is
        invalidated and an empty chunk is returned. Subsequent calls
        for the invalid stream will return errors.

        Args:
            stream_id: Stream ID from ``disassemble_wasm_module``.

        Returns:
            Dict with ``chunk`` (WasmDisassemblyChunk).
        """
        if not isinstance(stream_id, str):
            raise TypeError("stream_id must be a string")
        return await self._call(
            "Debugger.nextWasmDisassemblyChunk",
            {"streamId": stream_id},
        )

    async def pause(self) -> dict[str, Any]:
        """Pause script execution on the next JavaScript statement."""
        return await self._call("Debugger.pause")

    async def pause_on_async_call(
        self,
        parent_stack_trace_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Pause on the next async call with the given stack trace.

        Experimental. Deprecated.

        Args:
            parent_stack_trace_id: ``Runtime.StackTraceId`` dict.

        Returns:
            Response dict from the CDP.
        """
        if not isinstance(parent_stack_trace_id, dict):
            raise TypeError("parent_stack_trace_id must be a dict")
        return await self._call(
            "Debugger.pauseOnAsyncCall",
            {"parentStackTraceId": parent_stack_trace_id},
        )

    async def remove_breakpoint(
        self,
        breakpoint_id: str,
    ) -> dict[str, Any]:
        """Remove a breakpoint by ID.

        Args:
            breakpoint_id: The breakpoint ID returned by set_breakpoint.
        """
        if not isinstance(breakpoint_id, str):
            raise TypeError("breakpoint_id must be a string")
        return await self._call(
            "Debugger.removeBreakpoint",
            {"breakpointId": breakpoint_id},
        )

    async def restart_frame(
        self,
        call_frame_id: str,
        mode: str,
    ) -> dict[str, Any]:
        """Restart a particular call frame from the beginning.

        The mode parameter must be set to ``"StepInto"``. Execution
        continues until the beginning of the restarted frame, at which
        point a ``Debugger.paused`` event is fired.

        Args:
            call_frame_id: Call frame ID to restart.
            mode: Must be ``"StepInto"``.

        Returns:
            Dict with ``callFrames``, ``asyncStackTrace``, and
            ``asyncStackTraceId`` (all deprecated, use paused event).
        """
        if not isinstance(call_frame_id, str):
            raise TypeError("call_frame_id must be a string")
        if not isinstance(mode, str):
            raise TypeError("mode must be a string")
        valid_modes = {"StepInto"}
        if mode not in valid_modes:
            raise ValueError(
                f"mode must be one of {sorted(valid_modes)}"
            )
        return await self._call(
            "Debugger.restartFrame",
            {"callFrameId": call_frame_id, "mode": mode},
        )

    async def resume(
        self,
        terminate_on_resume: bool | None = None,
    ) -> dict[str, Any]:
        """Resume script execution after a pause.

        Continues execution from the current paused position until the
        next breakpoint or the script completes.

        Args:
            terminate_on_resume: If True, terminate execution upon
                resuming. Allows further JavaScript evaluation until
                the paused code is actually resumed.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {}
        if terminate_on_resume is not None:
            if not isinstance(terminate_on_resume, bool):
                raise TypeError("terminate_on_resume must be a bool or None")
            params["terminateOnResume"] = terminate_on_resume
        return await self._call("Debugger.resume", params or None)

    async def search_in_content(
        self,
        script_id: str,
        query: str,
        case_sensitive: bool | None = None,
        is_regex: bool | None = None,
    ) -> dict[str, Any]:
        """Search for a string in a script's content.

        Args:
            script_id: Script ID to search in.
            query: Search query.
            case_sensitive: Whether the search is case sensitive.
            is_regex: Whether the query is a regex.

        Returns:
            Dict with ``result`` list of matches.
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        params: dict[str, Any] = {
            "scriptId": script_id,
            "query": query,
        }
        if case_sensitive is not None:
            if not isinstance(case_sensitive, bool):
                raise TypeError(
                    "case_sensitive must be a bool or None"
                )
            params["caseSensitive"] = case_sensitive
        if is_regex is not None:
            if not isinstance(is_regex, bool):
                raise TypeError("is_regex must be a bool or None")
            params["isRegex"] = is_regex
        return await self._call("Debugger.searchInContent", params)

    async def set_async_call_stack_depth(
        self,
        max_depth: int,
    ) -> dict[str, Any]:
        """Enable or disable async call stack tracking.

        Args:
            max_depth: Maximum depth of async call stacks. Setting to
                0 effectively disables collecting async call stacks.
        """
        if not isinstance(max_depth, int):
            raise TypeError("max_depth must be an int")
        return await self._call(
            "Debugger.setAsyncCallStackDepth",
            {"maxDepth": max_depth},
        )

    async def set_blackbox_execution_contexts(
        self,
        execution_context_ids: list[str],
    ) -> dict[str, Any]:
        """Replace blackbox execution contexts.

        Experimental. Forces backend to skip stepping/pausing in scripts
        in these execution contexts.

        Args:
            execution_context_ids: Array of execution context unique ids
                for the debugger to ignore.
        """
        if not isinstance(execution_context_ids, list):
            raise TypeError("execution_context_ids must be a list")
        return await self._call(
            "Debugger.setBlackboxExecutionContexts",
            {"executionContextIds": execution_context_ids},
        )

    async def set_blackbox_patterns(
        self,
        patterns: list[str],
        skip_anonymous: bool | None = None,
    ) -> dict[str, Any]:
        """Set patterns to blackbox scripts (skip stepping into).

        Experimental. Forces backend to skip stepping/pausing in scripts
        with url matching one of the patterns.

        Args:
            patterns: List of regex patterns to blackbox.
            skip_anonymous: If True, also ignore scripts with no
                source url.
        """
        if not isinstance(patterns, list):
            raise TypeError("patterns must be a list")
        params: dict[str, Any] = {"patterns": patterns}
        if skip_anonymous is not None:
            if not isinstance(skip_anonymous, bool):
                raise TypeError(
                    "skip_anonymous must be a bool or None"
                )
            params["skipAnonymous"] = skip_anonymous
        return await self._call(
            "Debugger.setBlackboxPatterns", params,
        )

    async def set_blackboxed_ranges(
        self,
        script_id: str,
        positions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set blackboxed ranges for a script.

        Experimental. Makes backend skip steps in the script in
        blackboxed ranges. Positions array contains positions where
        blackbox state is changed. First interval isn't blackboxed.
        Array should be sorted.

        Args:
            script_id: Id of the script.
            positions: List of ScriptPosition dicts.
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        if not isinstance(positions, list):
            raise TypeError("positions must be a list")
        return await self._call(
            "Debugger.setBlackboxedRanges",
            {"scriptId": script_id, "positions": positions},
        )

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
            Dict with ``breakpointId`` and the actual ``location``.
        """
        if not isinstance(location, dict):
            raise TypeError("location must be a dict")
        params: dict[str, Any] = {"location": location}
        if condition is not None:
            if not isinstance(condition, str):
                raise TypeError("condition must be a string or None")
            params["condition"] = condition
        return await self._call("Debugger.setBreakpoint", params)

    async def set_breakpoint_by_url(
        self,
        line_number: int,
        url: str | None = None,
        url_regex: str | None = None,
        script_hash: str | None = None,
        column_number: int | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Set a breakpoint by script URL, regex, or hash.

        Either ``url``, ``url_regex``, or ``script_hash``
        should be specified.

        Args:
            line_number: Zero-based line number.
            url: Exact script URL to set the breakpoint in.
            url_regex: Regex pattern to match script URLs.
            script_hash: Script hash to set the breakpoint in.
            column_number: Optional zero-based column number.
            condition: Optional breakpoint condition expression.

        Returns:
            Dict with ``breakpointId`` and ``locations`` list.
        """
        if not isinstance(line_number, int):
            raise TypeError("line_number must be an int")
        params: dict[str, Any] = {"lineNumber": line_number}
        if url is not None:
            if not isinstance(url, str):
                raise TypeError("url must be a string or None")
            params["url"] = url
        if url_regex is not None:
            if not isinstance(url_regex, str):
                raise TypeError("url_regex must be a string or None")
            params["urlRegex"] = url_regex
        if script_hash is not None:
            if not isinstance(script_hash, str):
                raise TypeError("script_hash must be a string or None")
            params["scriptHash"] = script_hash
        if column_number is not None:
            if not isinstance(column_number, int):
                raise TypeError("column_number must be an int or None")
            params["columnNumber"] = column_number
        if condition is not None:
            if not isinstance(condition, str):
                raise TypeError("condition must be a string or None")
            params["condition"] = condition
        return await self._call("Debugger.setBreakpointByUrl", params)

    async def set_breakpoint_on_function_call(
        self,
        object_id: str,
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Set a breakpoint before each call to the given function.

        Experimental. If another function was created from the same
        source as the given one, calling it will also trigger the
        breakpoint.

        Args:
            object_id: Object ID of the function.
            condition: Optional breakpoint condition.

        Returns:
            Dict with ``breakpointId``.
        """
        if not isinstance(object_id, str):
            raise TypeError("object_id must be a string")
        params: dict[str, Any] = {"objectId": object_id}
        if condition is not None:
            if not isinstance(condition, str):
                raise TypeError("condition must be a string or None")
            params["condition"] = condition
        return await self._call(
            "Debugger.setBreakpointOnFunctionCall", params,
        )

    async def set_breakpoints_active(self, active: bool) -> dict[str, Any]:
        """Enable or disable all breakpoints.

        Args:
            active: Whether breakpoints should be active.
        """
        if not isinstance(active, bool):
            raise TypeError("active must be a bool")
        return await self._call(
            "Debugger.setBreakpointsActive",
            {"active": active},
        )

    async def set_instrumentation_breakpoint(
        self,
        instrumentation: str,
    ) -> dict[str, Any]:
        """Set instrumentation breakpoint.

        Args:
            instrumentation: Instrumentation name. Either
                ``"beforeScriptExecution"`` or
                ``"beforeScriptWithSourceMapExecution"``.

        Returns:
            Dict with ``breakpointId``.
        """
        if not isinstance(instrumentation, str):
            raise TypeError("instrumentation must be a string")
        valid = {
            "beforeScriptExecution",
            "beforeScriptWithSourceMapExecution",
        }
        if instrumentation not in valid:
            raise ValueError(
                f"instrumentation must be one of {sorted(valid)}"
            )
        return await self._call(
            "Debugger.setInstrumentationBreakpoint",
            {"instrumentation": instrumentation},
        )

    async def set_pause_on_exceptions(
        self,
        state: str,
    ) -> dict[str, Any]:
        """Set pause on exceptions mode.

        Args:
            state: ``"none"``, ``"caught"``, ``"uncaught"``, or
                ``"all"``.
        """
        if not isinstance(state, str):
            raise TypeError("state must be a string")
        valid_states = {"none", "caught", "uncaught", "all"}
        if state not in valid_states:
            raise ValueError(
                f"state must be one of {sorted(valid_states)}"
            )
        return await self._call(
            "Debugger.setPauseOnExceptions",
            {"state": state},
        )

    async def set_return_value(
        self,
        new_value: dict[str, Any],
    ) -> dict[str, Any]:
        """Set the return value of the current function.

        Experimental. Only valid when paused at a return statement.

        Args:
            new_value: New return value as a call argument dict.
        """
        if not isinstance(new_value, dict):
            raise TypeError("new_value must be a dict")
        return await self._call(
            "Debugger.setReturnValue",
            {"newValue": new_value},
        )

    async def set_script_source(
        self,
        script_id: str,
        source: str,
        dry_run: bool | None = None,
        allow_top_frame_editing: bool | None = None,
    ) -> dict[str, Any]:
        """Set the source code of a script.

        Args:
            script_id: Script ID from ``Debugger.scriptParsed`` event.
            source: New source code string.
            dry_run: If true, only check for errors without actually
                modifying the script.
            allow_top_frame_editing: Experimental. If true, allow
                changing the function on top of the stack.

        Returns:
            Dict with ``callFrames``, ``stackChanged``, and ``status``.
        """
        if not isinstance(script_id, str):
            raise TypeError("script_id must be a string")
        if not isinstance(source, str):
            raise TypeError("source must be a string")
        params: dict[str, Any] = {
            "scriptId": script_id,
            "source": source,
        }
        if dry_run is not None:
            if not isinstance(dry_run, bool):
                raise TypeError("dry_run must be a bool or None")
            params["dryRun"] = dry_run
        if allow_top_frame_editing is not None:
            if not isinstance(allow_top_frame_editing, bool):
                raise TypeError(
                    "allow_top_frame_editing must be a bool or None"
                )
            params["allowTopFrameEditing"] = allow_top_frame_editing
        return await self._call("Debugger.setScriptSource", params)

    async def set_skip_all_pauses(self, skip: bool) -> dict[str, Any]:
        """Skip all pauses until further notice.

        Args:
            skip: Whether to skip all pauses.
        """
        if not isinstance(skip, bool):
            raise TypeError("skip must be a bool")
        return await self._call(
            "Debugger.setSkipAllPauses",
            {"skip": skip},
        )

    async def set_variable_value(
        self,
        call_frame_id: str,
        scope_number: int,
        variable_name: str,
        new_value: dict[str, Any],
    ) -> dict[str, Any]:
        """Set the value of a variable in a call frame.

        Deprecated. Object-based scopes are not supported and must be
        mutated manually.

        Args:
            call_frame_id: Call frame ID from the paused state.
            scope_number: Scope number (0-based).
            variable_name: Variable name to set.
            new_value: New value as a remote object call argument.
        """
        if not isinstance(call_frame_id, str):
            raise TypeError("call_frame_id must be a string")
        if not isinstance(scope_number, int):
            raise TypeError("scope_number must be an int")
        if not isinstance(variable_name, str):
            raise TypeError("variable_name must be a string")
        if not isinstance(new_value, dict):
            raise TypeError("new_value must be a dict")
        return await self._call(
            "Debugger.setVariableValue",
            {
                "callFrameId": call_frame_id,
                "scopeNumber": scope_number,
                "variableName": variable_name,
                "newValue": new_value,
            },
        )

    async def step_into(
        self,
        break_on_async_call: bool | None = None,
        skip_list: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Step into the next function call.

        Advances to the first line inside the next function call,
        allowing line-by-line inspection of called functions.

        Args:
            break_on_async_call: Experimental. If True, pause on the
                first async task scheduled before the next pause.
            skip_list: Experimental. Location ranges to skip during
                step into.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {}
        if break_on_async_call is not None:
            if not isinstance(break_on_async_call, bool):
                raise TypeError("break_on_async_call must be a bool or None")
            params["breakOnAsyncCall"] = break_on_async_call
        if skip_list is not None:
            if not isinstance(skip_list, list):
                raise TypeError("skip_list must be a list or None")
            params["skipList"] = skip_list
        return await self._call("Debugger.stepInto", params or None)

    async def step_out(self) -> dict[str, Any]:
        """Step out of the current function.

        Continues execution until the current function returns, then
        pauses at the statement after the calling function.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Debugger.stepOut")

    async def step_over(
        self,
        skip_list: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Step over the next function call.

        Advances to the next line in the current function, skipping over
        any function calls rather than stepping into them.

        Args:
            skip_list: Experimental. Location ranges to skip during
                step over.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {}
        if skip_list is not None:
            if not isinstance(skip_list, list):
                raise TypeError("skip_list must be a list or None")
            params["skipList"] = skip_list
        return await self._call("Debugger.stepOver", params or None)
