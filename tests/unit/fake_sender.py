from typing import Any

from cdpwave.types import CommandSender


class FakeSender:
    def __init__(self, response: dict[str, Any] | None = None) -> None:
        self._response = response or {}
        self._calls: list[tuple[str, dict[str, Any] | None]] = []

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._calls.append((method, params))
        return self._response

    @property
    def calls(self) -> list[tuple[str, dict[str, Any] | None]]:
        return self._calls

    @property
    def last_call(self) -> tuple[str, dict[str, Any] | None]:
        return self._calls[-1]

    def set_response(self, response: dict[str, Any]) -> None:
        self._response = response

    def as_sender(self) -> CommandSender:
        return self
