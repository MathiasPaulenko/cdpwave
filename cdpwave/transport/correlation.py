"""Command correlation via asyncio Futures for matching CDP request/response pairs."""

import asyncio
from typing import Any


class Correlator:
    """Matches CDP command IDs to their responses via asyncio Futures."""

    def __init__(self) -> None:
        self._next_id: int = 0
        self._pending: dict[int, asyncio.Future[dict[str, Any]]] = {}

    def next_id(self) -> int:
        """Return the next monotonically increasing command ID.

        The ID grows without bound. In practice this is not an issue:
        at 1000 commands/second it would take ~136 years to reach
        ``2**32``. Python ints are arbitrary precision so no overflow
        occurs, and CDP implementations accept large IDs.
        """
        self._next_id += 1
        return self._next_id

    def register(self, cmd_id: int) -> asyncio.Future[dict[str, Any]]:
        """Register a pending command and return its response Future.

        Args:
            cmd_id: The command ID to track.

        Returns:
            A Future that will be resolved with the response dict.
        """
        fut: asyncio.Future[dict[str, Any]] = asyncio.get_running_loop().create_future()
        self._pending[cmd_id] = fut
        return fut

    def resolve(self, cmd_id: int, result: dict[str, Any]) -> None:
        """Resolve a pending command's Future with a successful result.

        Args:
            cmd_id: The command ID to resolve.
            result: The CDP response result dict.
        """
        fut = self._pending.pop(cmd_id, None)
        if fut is not None and not fut.done():
            fut.set_result(result)

    def reject(self, cmd_id: int, error: Exception) -> None:
        """Reject a pending command's Future with an exception.

        Args:
            cmd_id: The command ID to reject.
            error: The exception to set on the Future.
        """
        fut = self._pending.pop(cmd_id, None)
        if fut is not None and not fut.done():
            fut.set_exception(error)

    def reject_all(self, error: Exception) -> None:
        """Reject all pending commands with the given exception.

        Used when the connection closes unexpectedly.

        Args:
            error: The exception to set on all pending Futures.
        """
        for fut in self._pending.values():
            if not fut.done():
                fut.set_exception(error)
        self._pending.clear()

    @property
    def pending_count(self) -> int:
        """Number of commands currently awaiting a response."""
        return len(self._pending)
