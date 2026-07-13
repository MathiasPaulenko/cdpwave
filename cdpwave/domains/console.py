"""Console domain: deprecated console domain for console messages.

Deprecated in favor of ``Runtime.consoleAPICalled`` events, but still
useful for clearing console messages.

Events:
    Console.messageAdded: Issued when new console message is added.
        Parameters:
            message (dict): Console message that has been added. A
                ConsoleMessage with fields:
                source (str): Message source. One of ``xml``,
                    ``javascript``, ``network``, ``console-api``,
                    ``storage``, ``appcache``, ``rendering``,
                    ``security``, ``other``, ``deprecation``,
                    ``worker``.
                level (str): Message severity. One of ``log``,
                    ``warning``, ``error``, ``debug``, ``info``.
                text (str): Message text.
                url (str, optional): URL of the message origin.
                line (int, optional): Line number in the resource that
                    generated this message (1-based).
                column (int, optional): Column number in the resource
                    that generated this message (1-based).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ConsoleDomain(BaseDomain):
    """Wrapper for the CDP Console domain.

    Deprecated in favor of ``Runtime.consoleAPICalled`` events,
    but still useful for clearing console messages.

    Events:
        Console.messageAdded: Issued when new console message is added.
            Parameters:
                message (dict): Console message that has been added.
                    See module docstring for ConsoleMessage fields.
    """

    async def clear_messages(self) -> dict[str, Any]:
        """Does nothing.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.clearMessages")

    async def disable(self) -> dict[str, Any]:
        """Disables console domain, prevents further console messages from
        being reported to the client.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables console domain, sends the messages collected so far to the
        client by means of the messageAdded notification.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Console.enable")
