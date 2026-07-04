"""Runtime domain: JavaScript evaluation and remote object management."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class RuntimeDomain(BaseDomain):
    """Wrapper for the CDP Runtime domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Runtime domain events."""
        return await self._call("Runtime.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Runtime domain events."""
        return await self._call("Runtime.disable")

    async def evaluate(
        self,
        expression: str,
        return_by_value: bool = True,
        await_promise: bool = False,
        user_gesture: bool = False,
    ) -> dict[str, Any]:
        """Evaluate a JavaScript expression.

        Args:
            expression: JavaScript expression to evaluate.
            return_by_value: Return the result as a JSON value.
            await_promise: Await any returned Promise before resolving.
            user_gesture: Treat the evaluation as a user gesture.

        Returns:
            Response dict containing ``result`` with the evaluation result.
        """
        return await self._call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": return_by_value,
                "awaitPromise": await_promise,
                "userGesture": user_gesture,
            },
        )

    async def call_function_on(
        self,
        object_id: str,
        function_declaration: str,
        args: list[dict[str, Any]] | None = None,
        return_by_value: bool = True,
        await_promise: bool = False,
    ) -> dict[str, Any]:
        """Call a function on a remote object.

        Args:
            object_id: ID of the remote object to call on.
            function_declaration: JavaScript function declaration string.
            args: Optional list of argument dicts.
            return_by_value: Return the result as a JSON value.
            await_promise: Await any returned Promise before resolving.

        Returns:
            Response dict containing ``result``.
        """
        params: dict[str, Any] = {
            "objectId": object_id,
            "functionDeclaration": function_declaration,
            "returnByValue": return_by_value,
            "awaitPromise": await_promise,
        }
        if args is not None:
            params["arguments"] = args
        return await self._call("Runtime.callFunctionOn", params)

    async def release_object(self, object_id: str) -> dict[str, Any]:
        """Release a remote object by ID."""
        return await self._call(
            "Runtime.releaseObject",
            {"objectId": object_id},
        )

    async def release_object_group(self, object_group: str) -> dict[str, Any]:
        """Release all objects in a named group."""
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
