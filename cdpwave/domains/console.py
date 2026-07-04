"""Console domain: deprecated console message clearing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ConsoleDomain(BaseDomain):
    """Wrapper for the CDP Console domain.

    Deprecated in favor of ``Runtime.consoleAPICalled`` events,
    but still useful for clearing console messages.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable Console domain events."""
        return await self._call("Console.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Console domain events."""
        return await self._call("Console.disable")

    async def clear_messages(self) -> dict[str, Any]:
        """Clear all console messages."""
        return await self._call("Console.clearMessages")
