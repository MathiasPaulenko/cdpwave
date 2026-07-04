from typing import Any

from cdpwave.domains.base import BaseDomain


class ConsoleDomain(BaseDomain):
    async def enable(self) -> dict[str, Any]:
        return await self._call("Console.enable")

    async def disable(self) -> dict[str, Any]:
        return await self._call("Console.disable")

    async def clear_messages(self) -> dict[str, Any]:
        return await self._call("Console.clearMessages")
