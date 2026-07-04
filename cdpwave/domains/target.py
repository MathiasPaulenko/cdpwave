from typing import Any

from cdpwave.domains.base import BaseDomain


class TargetDomain(BaseDomain):
    async def create_target(self, url: str) -> dict[str, Any]:
        return await self._call("Target.createTarget", {"url": url})

    async def attach_to_target(
        self,
        target_id: str,
        flatten: bool = True,
    ) -> dict[str, Any]:
        return await self._call(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": flatten},
        )

    async def detach_from_target(self, session_id: str) -> dict[str, Any]:
        return await self._call(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> dict[str, Any]:
        return await self._call("Target.closeTarget", {"targetId": target_id})

    async def get_targets(self) -> dict[str, Any]:
        return await self._call("Target.getTargets")

    async def set_auto_attach(
        self,
        auto_attach: bool,
        flatten: bool = True,
    ) -> dict[str, Any]:
        return await self._call(
            "Target.setAutoAttach",
            {"autoAttach": auto_attach, "flatten": flatten},
        )
