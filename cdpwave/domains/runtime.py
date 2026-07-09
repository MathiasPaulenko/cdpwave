"""Runtime domain: JavaScript evaluation and remote object management."""

from typing import Any

from cdpwave.domains.base import BaseDomain


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
    ) -> dict[str, Any]:
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

        Returns:
            Response dict containing ``result`` with the evaluation result.
        """
        params: dict[str, Any] = {"expression": expression}
        if not return_by_value:
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
        return await self._call("Runtime.evaluate", params)

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
    ) -> dict[str, Any]:
        """Call a function on a remote object or in a context.

        Either ``object_id`` or ``execution_context_id`` must be provided.
        If neither is given, the function runs in the default context.

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

        Returns:
            Response dict containing ``result``.
        """
        params: dict[str, Any] = {
            "functionDeclaration": function_declaration,
            "returnByValue": return_by_value,
            "awaitPromise": await_promise,
        }
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
        return await self._call("Runtime.callFunctionOn", params)

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
        own_properties: bool = True,
    ) -> dict[str, Any]:
        """Get properties of a remote object.

        Args:
            object_id: ID of the remote object.
            own_properties: If True, return only own properties.

        Returns:
            Response dict containing ``result`` with property descriptors.
        """
        return await self._call(
            "Runtime.getProperties",
            {
                "objectId": object_id,
                "ownProperties": own_properties,
            },
        )

    async def add_binding(self, name: str) -> dict[str, Any]:
        """Add a binding that exposes a Python callback to JavaScript.

        After calling this, JS code can call ``window.<name>()`` which
        triggers a ``Runtime.bindingCalled`` event with the callback result.

        Args:
            name: Name of the binding (becomes ``window.<name>`` in JS).
        """
        return await self._call("Runtime.addBinding", {"name": name})

    async def remove_binding(self, name: str) -> dict[str, Any]:
        """Remove a previously added binding.

        Args:
            name: Name of the binding to remove.
        """
        return await self._call("Runtime.removeBinding", {"name": name})

    async def compile_script(
        self,
        expression: str,
        source_url: str = "",
        persist_script: bool = False,
        execution_context_id: int | None = None,
    ) -> dict[str, Any]:
        """Compile a JavaScript expression without executing it.

        Args:
            expression: JavaScript expression to compile.
            source_url: Source URL for the script.
            persist_script: Whether the script should persist.
            execution_context_id: Optional execution context ID.

        Returns:
            Dict with ``scriptId``, ``exceptionDetails`` (if any).
        """
        params: dict[str, Any] = {
            "expression": expression,
            "sourceURL": source_url,
            "persistScript": persist_script,
        }
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        return await self._call("Runtime.compileScript", params)

    async def run_script(
        self,
        script_id: str,
        execution_context_id: int | None = None,
        await_promise: bool = False,
        return_by_value: bool = False,
    ) -> dict[str, Any]:
        """Run a previously compiled script.

        Args:
            script_id: Script ID from ``compile_script``.
            execution_context_id: Optional execution context ID.
            await_promise: Await any returned Promise.
            return_by_value: Return the result as a JSON value.
        """
        params: dict[str, Any] = {
            "scriptId": script_id,
            "awaitPromise": await_promise,
            "returnByValue": return_by_value,
        }
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        return await self._call("Runtime.runScript", params)

    async def run_if_waiting_for_debugger(self) -> dict[str, Any]:
        """Run if the page is waiting for a debugger to attach."""
        return await self._call("Runtime.runIfWaitingForDebugger")

    async def get_exception_details(
        self,
        error_object_id: str,
    ) -> dict[str, Any]:
        """Get details for an error object.

        Args:
            error_object_id: Object ID of the error.

        Returns:
            Dict with ``exceptionDetails``.
        """
        return await self._call(
            "Runtime.getExceptionDetails",
            {"errorObjectId": error_object_id},
        )

    async def query_objects(
        self,
        prototype_object_id: str,
        object_group: str | None = None,
    ) -> dict[str, Any]:
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
        return await self._call("Runtime.queryObjects", params)

    async def global_lexical_scope_names(
        self,
        execution_context_id: int | None = None,
    ) -> dict[str, Any]:
        """Get global lexical scope names (let/const/class).

        Args:
            execution_context_id: Optional execution context ID.

        Returns:
            Dict with ``names`` list of strings.
        """
        params: dict[str, Any] = {}
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        return await self._call(
            "Runtime.globalLexicalScopeNames",
            params if params else None,
        )

    async def get_heap_usage(self) -> dict[str, Any]:
        """Get the current JavaScript heap usage.

        Returns:
            Dict with ``usedSize`` and ``totalSize`` in bytes.
        """
        return await self._call("Runtime.getHeapUsage")

    async def set_async_call_stack_depth(self, depth: int) -> dict[str, Any]:
        """Set the maximum depth of async call stacks.

        Args:
            depth: Maximum async call stack depth (0 to disable).
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
        """
        return await self._call("Runtime.terminateExecution")

    async def await_promise(
        self,
        promise_object_id: str,
        return_by_value: bool = False,
    ) -> dict[str, Any]:
        """Await a Promise remote object.

        Args:
            promise_object_id: Object ID of the Promise.
            return_by_value: Return the result as a JSON value.

        Returns:
            Dict with ``result`` remote object.
        """
        return await self._call(
            "Runtime.awaitPromise",
            {
                "promiseObjectId": promise_object_id,
                "returnByValue": return_by_value,
            },
        )

    async def discard_console_entries(self) -> dict[str, Any]:
        """Discard all collected console entries.

        Clears the buffer of console API calls that were accumulated
        since ``enable`` was called. Does not affect future entries.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Runtime.discardConsoleEntries")

    async def get_isolate_id(self) -> dict[str, Any]:
        """Get the isolate id.

        Returns:
            Dict with ``isolateId`` string.
        """
        return await self._call("Runtime.getIsolateId")

    async def collect_garbage(self) -> dict[str, Any]:
        """Run garbage collection."""
        return await self._call("Runtime.collectGarbage")

    async def set_custom_object_formatter_enabled(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable custom object formatter.

        Args:
            enabled: Whether to enable custom object formatting.
        """
        return await self._call(
            "Runtime.setCustomObjectFormatterEnabled",
            {"enabled": enabled},
        )
