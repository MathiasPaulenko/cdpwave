from typing import Any

from cdpwave.types import CommandSender


class BaseDomain:
    def __init__(self, send: CommandSender) -> None:
        self._send = send

    async def _call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._send(method, params)
