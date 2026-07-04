from typing import Any

from cdpwave.domains.base import BaseDomain


class RuntimeDomain(BaseDomain):
    async def enable(self) -> dict[str, Any]:
        return await self._call("Runtime.enable")

    async def disable(self) -> dict[str, Any]:
        return await self._call("Runtime.disable")

    async def evaluate(
        self,
        expression: str,
        return_by_value: bool = True,
        await_promise: bool = False,
        user_gesture: bool = False,
    ) -> dict[str, Any]:
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
        return await self._call(
            "Runtime.releaseObject",
            {"objectId": object_id},
        )

    async def release_object_group(self, object_group: str) -> dict[str, Any]:
        return await self._call(
            "Runtime.releaseObjectGroup",
            {"objectGroup": object_group},
        )

    async def get_properties(
        self,
        object_id: str,
        own_properties: bool = True,
    ) -> dict[str, Any]:
        return await self._call(
            "Runtime.getProperties",
            {
                "objectId": object_id,
                "ownProperties": own_properties,
            },
        )
