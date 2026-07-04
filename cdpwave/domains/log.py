from typing import Any

from cdpwave.domains.base import BaseDomain


class LogDomain(BaseDomain):
    async def enable(self) -> dict[str, Any]:
        return await self._call("Log.enable")

    async def disable(self) -> dict[str, Any]:
        return await self._call("Log.disable")

    async def clear(self) -> dict[str, Any]:
        return await self._call("Log.clear")

    async def start_violation_report(
        self,
        config: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return await self._call(
            "Log.startViolationsReport",
            {"config": config},
        )

    async def stop_violation_report(self) -> dict[str, Any]:
        return await self._call("Log.stopViolationsReport")
