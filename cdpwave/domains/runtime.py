"""Runtime domain: JavaScript evaluation and remote object management."""

from typing import Any, cast

from cdpwave.domains.base import BaseDomain
from cdpwave.types import (
    RuntimeAwaitPromiseResult,
    RuntimeCallFunctionOnResult,
    RuntimeCompileScriptResult,
    RuntimeEvaluateResult,
    RuntimeGetExceptionDetailsResult,
    RuntimeGetHeapUsageResult,
    RuntimeGetIsolateIdResult,
    RuntimeGetPropertiesResult,
    RuntimeGlobalLexicalScopeNamesResult,
    RuntimeQueryObjectsResult,
    RuntimeRunScriptResult,
)


class RuntimeDomain(BaseDomain):
    """Wrapper for the CDP Runtime domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Runtime domain events.

        Activates reporting of execution contexts, console API calls,
        exceptions, and binding notifications. Must be called before
        evaluating JavaScript or listening to Runtime events.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Runtime domain events.

        Stops reporting of execution contexts, console calls, and
        exceptions. Remote objects remain valid until released.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.disable")

    async def evaluate(
        self,
        expression: str,
        return_by_value: bool = True,
        await_promise: bool = False,
        user_gesture: bool = False,
        object_group: str | None = None,
        generate_preview: bool = False,
        silent: bool = False,
        execution_context_id: int | None = None,
        include_command_line_api: bool | None = None,
        throw_on_side_effect: bool = False,
        timeout: int | None = None,
        disable_breaks: bool = False,
        repl_mode: bool = False,
        allow_unsafe_eval_blocked_by_csp: bool = True,
        unique_context_id: str | None = None,
        serialization_options: dict[str, Any] | None = None,
    ) -> RuntimeEvaluateResult:
        """Evaluate a JavaScript expression.

        Args:
            expression: JavaScript expression to evaluate.
            return_by_value: Return the result as a JSON value.
            await_promise: Await any returned Promise before resolving.
            user_gesture: Treat the evaluation as a user gesture.
            object_group: Optional name for the object group for remote objects.
            generate_preview: Generate preview for the result object.
            silent: If True, do not report exceptions thrown.
            execution_context_id: Optional context to evaluate in.
            include_command_line_api: Whether to include the command line API.
            throw_on_side_effect: Throw if evaluation has side effects.
            timeout: Timeout in milliseconds.
            disable_breaks: Disable breakpoints during evaluation.
            repl_mode: Execute in REPL mode.
            allow_unsafe_eval_blocked_by_csp: Allow unsafe eval blocked by CSP.
            unique_context_id: Alternative context ID (string).
            serialization_options: Serialization options dict.

        Returns:
            Response dict containing ``result`` with the evaluation result,
            and ``exceptionDetails`` (if an exception was thrown).

        Raises:
            ValueError: If both ``execution_context_id`` and
                ``unique_context_id`` are provided.
        """
        if execution_context_id is not None and unique_context_id is not None:
            raise ValueError(
                "execution_context_id and unique_context_id are "
                "mutually exclusive"
            )
        params: dict[str, Any] = {"expression": expression}
        if return_by_value:
            params["returnByValue"] = return_by_value
        if await_promise:
            params["awaitPromise"] = await_promise
        if user_gesture:
            params["userGesture"] = user_gesture
        if object_group is not None:
            params["objectGroup"] = object_group
        if generate_preview:
            params["generatePreview"] = generate_preview
        if silent:
            params["silent"] = silent
        if execution_context_id is not None:
            params["contextId"] = execution_context_id
        if include_command_line_api is not None:
            params["includeCommandLineAPI"] = include_command_line_api
        if throw_on_side_effect:
            params["throwOnSideEffect"] = throw_on_side_effect
        if timeout is not None:
            params["timeout"] = timeout
        if disable_breaks:
            params["disableBreaks"] = disable_breaks
        if repl_mode:
            params["replMode"] = repl_mode
        if not allow_unsafe_eval_blocked_by_csp:
            params["allowUnsafeEvalBlockedByCSP"] = allow_unsafe_eval_blocked_by_csp
        if unique_context_id is not None:
            params["uniqueContextId"] = unique_context_id
        if serialization_options is not None:
            params["serializationOptions"] = serialization_options
        return cast("RuntimeEvaluateResult", await self._call("Runtime.evaluate", params))

    async def call_function_on(
        self,
        function_declaration: str,
        object_id: str | None = None,
        execution_context_id: int | None = None,
        args: list[dict[str, Any]] | None = None,
        return_by_value: bool = True,
        await_promise: bool = False,
        generate_preview: bool = False,
        silent: bool = False,
        object_group: str | None = None,
        user_gesture: bool = False,
        throw_on_side_effect: bool = False,
        unique_context_id: str | None = None,
        serialization_options: dict[str, Any] | None = None,
    ) -> RuntimeCallFunctionOnResult:
        """Call a function on a remote object or in a context.

        Either ``object_id``, ``execution_context_id``, or
        ``unique_context_id`` must be provided.

        Args:
            function_declaration: JavaScript function declaration string.
            object_id: ID of the remote object to call on.
            execution_context_id: Context to call the function in.
            args: Optional list of argument dicts.
            return_by_value: Return the result as a JSON value.
            await_promise: Await any returned Promise before resolving.
            generate_preview: Generate preview for the result object.
            silent: If True, do not report exceptions thrown.
            object_group: Optional name for the object group.
            user_gesture: Treat the call as a user gesture.
            throw_on_side_effect: Throw if call has side effects.
            unique_context_id: Alternative context ID (string).
            serialization_options: Serialization options dict.

        Returns:
            Response dict containing ``result`` with the call result,
            and ``exceptionDetails`` (if an exception was thrown).

        Raises:
            ValueError: If none of ``object_id``, ``execution_context_id``,
                or ``unique_context_id`` is provided, or if more than one
                is provided (they are mutually exclusive).
        """
        provided = [
            p is not None
            for p in (object_id, execution_context_id, unique_context_id)
        ]
        if sum(provided) == 0:
            raise ValueError(
                "Either object_id, execution_context_id, or "
                "unique_context_id must be provided"
            )
        if sum(provided) > 1:
            raise ValueError(
                "object_id, execution_context_id, and "
                "unique_context_id are mutually exclusive"
            )
        params: dict[str, Any] = {"functionDeclaration": function_declaration}
        if return_by_value:
            params["returnByValue"] = return_by_value
        if await_promise:
            params["awaitPromise"] = await_promise
        if object_id is not None:
            params["objectId"] = object_id
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        if args is not None:
            params["arguments"] = args
        if generate_preview:
            params["generatePreview"] = generate_preview
        if silent:
            params["silent"] = silent
        if object_group is not None:
            params["objectGroup"] = object_group
        if user_gesture:
            params["userGesture"] = user_gesture
        if throw_on_side_effect:
            params["throwOnSideEffect"] = throw_on_side_effect
        if unique_context_id is not None:
            params["uniqueContextId"] = unique_context_id
        if serialization_options is not None:
            params["serializationOptions"] = serialization_options
        return cast(
            "RuntimeCallFunctionOnResult",
            await self._call("Runtime.callFunctionOn", params),
        )

    async def release_object(self, object_id: str) -> dict[str, Any]:
        """Release a remote object by its object ID.

        Frees the object on the browser side. After calling this, the
        object ID is no longer valid and must not be used.

        Args:
            object_id: Remote object ID returned from ``evaluate`` or
                ``call_function_on``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Runtime.releaseObject",
            {"objectId": object_id},
        )

    async def release_object_group(self, object_group: str) -> dict[str, Any]:
        """Release all remote objects in a named group.

        Objects assigned to a group via ``evaluate`` or
        ``call_function_on`` can be released in bulk with this method.

        Args:
            object_group: Name of the object group to release.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Runtime.releaseObjectGroup",
            {"objectGroup": object_group},
        )

    async def get_properties(
        self,
        object_id: str,
        own_properties: bool = False,
        accessor_properties_only: bool | None = None,
        generate_preview: bool = False,
        non_indexed_properties_only: bool | None = None,
    ) -> RuntimeGetPropertiesResult:
        """Get properties of a remote object.

        Args:
            object_id: ID of the remote object.
            own_properties: If True, return only own properties (not
                inherited from the prototype chain).
            accessor_properties_only: If True, return only accessor properties.
            generate_preview: Generate preview for the property values.
            non_indexed_properties_only: If True, return only non-indexed
                properties.

        Returns:
            Response dict containing ``result`` with property descriptors,
            ``internalProperties``, ``privateProperties``, and
            ``exceptionDetails`` (if any).
        """
        params: dict[str, Any] = {"objectId": object_id}
        if own_properties:
            params["ownProperties"] = own_properties
        if accessor_properties_only is not None:
            params["accessorPropertiesOnly"] = accessor_properties_only
        if generate_preview:
            params["generatePreview"] = generate_preview
        if non_indexed_properties_only is not None:
            params["nonIndexedPropertiesOnly"] = non_indexed_properties_only
        return cast("RuntimeGetPropertiesResult", await self._call("Runtime.getProperties", params))

    async def add_binding(
        self,
        name: str,
        execution_context_id: int | None = None,
        execution_context_name: str | None = None,
    ) -> dict[str, Any]:
        """Add a binding that exposes a Python callback to JavaScript.

        After calling this, JS code can call ``window.<name>()`` which
        triggers a ``Runtime.bindingCalled`` event with the callback result.

        Args:
            name: Name of the binding (becomes ``window.<name>`` in JS).
            execution_context_id: Deprecated. Optional context to add the
                binding in. Use ``execution_context_name`` instead.
            execution_context_name: Optional context name to add the binding in.

        Returns:
            Response dict from the CDP.

        Raises:
            ValueError: If both ``execution_context_id`` and
                ``execution_context_name`` are provided.
        """
        if execution_context_id is not None and execution_context_name is not None:
            raise ValueError(
                "execution_context_id and execution_context_name are "
                "mutually exclusive"
            )
        params: dict[str, Any] = {"name": name}
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        if execution_context_name is not None:
            params["executionContextName"] = execution_context_name
        return await self._call("Runtime.addBinding", params)

    async def remove_binding(self, name: str) -> dict[str, Any]:
        """Remove a previously added binding.

        Args:
            name: Name of the binding to remove.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.removeBinding", {"name": name})

    async def compile_script(
        self,
        expression: str,
        source_url: str = "",
        persist_script: bool = False,
        execution_context_id: int | None = None,
    ) -> RuntimeCompileScriptResult:
        """Compile a JavaScript expression without executing it.

        Args:
            expression: JavaScript expression to compile.
            source_url: Source URL for the script.
            persist_script: Whether the script should persist.
            execution_context_id: Optional execution context ID.

        Returns:
            Dict with ``scriptId``, ``exceptionDetails`` (if any).
        """
        if not isinstance(expression, str):
            raise TypeError("expression must be a string")
        if not isinstance(source_url, str):
            raise TypeError("source_url must be a string")
        if not isinstance(persist_script, bool):
            raise TypeError("persist_script must be a bool")
        params: dict[str, Any] = {
            "expression": expression,
            "sourceURL": source_url,
        }
        if persist_script:
            params["persistScript"] = persist_script
        if execution_context_id is not None:
            if isinstance(execution_context_id, bool) or not isinstance(execution_context_id, int):
                raise TypeError("execution_context_id must be an int or None")
            params["executionContextId"] = execution_context_id
        return cast("RuntimeCompileScriptResult", await self._call("Runtime.compileScript", params))

    async def run_script(
        self,
        script_id: str,
        execution_context_id: int | None = None,
        await_promise: bool = False,
        return_by_value: bool = False,
        object_group: str | None = None,
        silent: bool = False,
        include_command_line_api: bool | None = None,
        generate_preview: bool = False,
    ) -> RuntimeRunScriptResult:
        """Run a previously compiled script.

        Args:
            script_id: Script ID from ``compile_script``.
            execution_context_id: Optional execution context ID.
            await_promise: Await any returned Promise.
            return_by_value: Return the result as a JSON value.
            object_group: Optional object group for remote objects.
            silent: If True, do not report exceptions thrown.
            include_command_line_api: Whether to include the command line API.
            generate_preview: Generate preview for the result object.

        Returns:
            Response dict containing ``result`` with the run result,
            and ``exceptionDetails`` (if an exception was thrown).
        """
        params: dict[str, Any] = {
            "scriptId": script_id,
        }
        if await_promise:
            params["awaitPromise"] = await_promise
        if return_by_value:
            params["returnByValue"] = return_by_value
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        if object_group is not None:
            params["objectGroup"] = object_group
        if silent:
            params["silent"] = silent
        if include_command_line_api is not None:
            params["includeCommandLineAPI"] = include_command_line_api
        if generate_preview:
            params["generatePreview"] = generate_preview
        return cast("RuntimeRunScriptResult", await self._call("Runtime.runScript", params))

    async def run_if_waiting_for_debugger(self) -> dict[str, Any]:
        """Run if the page is waiting for a debugger to attach.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.runIfWaitingForDebugger")

    async def get_exception_details(
        self,
        error_object_id: str,
    ) -> RuntimeGetExceptionDetailsResult:
        """Get details for an error object.

        Args:
            error_object_id: Object ID of the error.

        Returns:
            Dict with ``exceptionDetails``.
        """
        return cast("RuntimeGetExceptionDetailsResult", await self._call(
            "Runtime.getExceptionDetails",
            {"errorObjectId": error_object_id},
        ))

    async def query_objects(
        self,
        prototype_object_id: str,
        object_group: str | None = None,
    ) -> RuntimeQueryObjectsResult:
        """Query objects with a given prototype.

        Args:
            prototype_object_id: Object ID of the prototype.
            object_group: Optional object group for the results.

        Returns:
            Dict with ``objects`` remote object.
        """
        params: dict[str, Any] = {"prototypeObjectId": prototype_object_id}
        if object_group is not None:
            params["objectGroup"] = object_group
        return cast("RuntimeQueryObjectsResult", await self._call("Runtime.queryObjects", params))

    async def global_lexical_scope_names(
        self,
        execution_context_id: int | None = None,
    ) -> RuntimeGlobalLexicalScopeNamesResult:
        """Get global lexical scope names (let/const/class).

        Args:
            execution_context_id: Optional execution context ID.

        Returns:
            Dict with ``names`` list of strings.
        """
        params: dict[str, Any] = {}
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        return cast("RuntimeGlobalLexicalScopeNamesResult", await self._call(
            "Runtime.globalLexicalScopeNames",
            params if params else None,
        ))

    async def get_heap_usage(self) -> RuntimeGetHeapUsageResult:
        """Get the current JavaScript heap usage.

        Returns:
            Dict with ``usedSize``, ``totalSize``,
            ``embedderHeapUsedSize``, and ``backingStorageSize`` in bytes.
        """
        return cast("RuntimeGetHeapUsageResult", await self._call("Runtime.getHeapUsage"))

    async def set_async_call_stack_depth(self, depth: int) -> dict[str, Any]:
        """Set the maximum depth of async call stacks.

        Args:
            depth: Maximum async call stack depth (0 to disable).

        Returns:
            Response dict from the CDP.

        Raises:
            ValueError: If ``depth`` is negative.
        """
        if depth < 0:
            raise ValueError("depth must be >= 0")
        return await self._call(
            "Runtime.setAsyncCallStackDepth",
            {"maxDepth": depth},
        )

    async def terminate_execution(self) -> dict[str, Any]:
        """Terminate the current JavaScript execution.

        This will abort the current script execution immediately.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.terminateExecution")

    async def await_promise(
        self,
        promise_object_id: str,
        return_by_value: bool = False,
        generate_preview: bool = False,
    ) -> RuntimeAwaitPromiseResult:
        """Await a Promise remote object.

        Args:
            promise_object_id: Object ID of the Promise.
            return_by_value: Return the result as a JSON value.
            generate_preview: Generate preview for the result object.

        Returns:
            Dict with ``result`` remote object, and ``exceptionDetails``
            (if the promise was rejected).
        """
        params: dict[str, Any] = {
            "promiseObjectId": promise_object_id,
        }
        if return_by_value:
            params["returnByValue"] = return_by_value
        if generate_preview:
            params["generatePreview"] = generate_preview
        return cast("RuntimeAwaitPromiseResult", await self._call("Runtime.awaitPromise", params))

    async def discard_console_entries(self) -> dict[str, Any]:
        """Discard all collected console entries.

        Clears the buffer of console API calls that were accumulated
        since ``enable`` was called. Does not affect future entries.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.discardConsoleEntries")

    async def get_isolate_id(self) -> RuntimeGetIsolateIdResult:
        """Get the isolate id.

        Returns:
            Dict with ``id`` string.
        """
        return cast("RuntimeGetIsolateIdResult", await self._call("Runtime.getIsolateId"))

    async def collect_garbage(self) -> dict[str, Any]:
        """Run garbage collection.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.collectGarbage")

    async def set_custom_object_formatter_enabled(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable custom object formatter.

        Args:
            enabled: Whether to enable custom object formatting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Runtime.setCustomObjectFormatterEnabled",
            {"enabled": enabled},
        )

    async def set_max_call_stack_size_to_capture(
        self,
        size: int,
    ) -> dict[str, Any]:
        """Set the maximum call stack size to capture.

        Args:
            size: Maximum call stack size to capture.

        Returns:
            Response dict from the CDP.

        Raises:
            ValueError: If ``size`` is negative.
        """
        if size < 0:
            raise ValueError("size must be >= 0")
        return await self._call(
            "Runtime.setMaxCallStackSizeToCapture",
            {"size": size},
        )
