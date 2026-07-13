"""Log domain: provides access to log entries.

Events:
    Log.entryAdded: Issued when new message was logged.
        Parameters:
            entry (dict): The entry. A LogEntry with fields:
                source (str): Log entry source. One of ``xml``,
                    ``javascript``, ``network``, ``storage``,
                    ``appcache``, ``rendering``, ``security``,
                    ``deprecation``, ``worker``, ``violation``,
                    ``intervention``, ``recommendation``, ``other``.
                level (str): Log entry severity. One of ``verbose``,
                    ``info``, ``warning``, ``error``.
                text (str): Logged text.
                category (str, optional): Entry category. One of
                    ``cors``.
                timestamp (float): Timestamp when this entry was
                    added.
                url (str, optional): URL of the resource if known.
                lineNumber (int, optional): Line number in the
                    resource.
                stackTrace (dict, optional): JavaScript stack trace.
                networkRequestId (str, optional): Identifier of the
                    network request associated with this entry.
                workerId (str, optional): Identifier of the worker
                    associated with this entry.
                args (list, optional): Call arguments.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class LogDomain(BaseDomain):
    """Wrapper for the CDP Log domain.

    Provides access to log entries.

    Events:
        Log.entryAdded: Issued when new message was logged.
            Parameters:
                entry (dict): The entry. See module docstring for
                    LogEntry fields.
    """

    async def clear(self) -> dict[str, Any]:
        """Clears the log.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.clear")

    async def disable(self) -> dict[str, Any]:
        """Disables log domain, prevents further log entries from being reported to the client.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables log domain, sends the entries collected so far to the
        client by means of the entryAdded notification.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.enable")

    async def start_violations_report(
        self,
        config: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Start violation reporting.

        Args:
            config: Configuration for violations. A list of
                ViolationSetting dicts, each with:
                ``name`` (str): Violation type. One of ``longTask``,
                ``longLayout``, ``blockedEvent``, ``blockedParser``,
                ``discouragedAPIUse``, ``handler``, ``recurringHandler``.
                ``threshold`` (float): Time threshold to trigger upon.
        """
        return await self._call(
            "Log.startViolationsReport",
            {"config": config},
        )

    async def stop_violations_report(self) -> dict[str, Any]:
        """Stop violation reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.stopViolationsReport")
