"""Console domain: deprecated console message clearing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ConsoleDomain(BaseDomain):
    """Wrapper for the CDP Console domain.

    Deprecated in favor of ``Runtime.consoleAPICalled`` events,
    but still useful for clearing console messages.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable Console domain events.

        Deprecated: prefer ``Runtime.enable`` and listen for
        ``Runtime.consoleAPICalled`` events instead.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Console domain events.

        Deprecated: prefer ``Runtime.disable`` instead.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.disable")

    async def clear_messages(self) -> dict[str, Any]:
        """Clear all accumulated console messages.

        Removes all buffered console messages from the browser.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.clearMessages")
