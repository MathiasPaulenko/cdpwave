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

_VALID_VIOLATION_NAMES = frozenset({
    "longTask",
    "longLayout",
    "blockedEvent",
    "blockedParser",
    "discouragedAPIUse",
    "handler",
    "recurringHandler",
})


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
        if not isinstance(config, list):
            raise TypeError("config must be a list")
        for i, entry in enumerate(config):
            if not isinstance(entry, dict):
                raise TypeError(f"config[{i}] must be a dict")
            if "name" not in entry:
                raise ValueError(f"config[{i}] must contain 'name'")
            if "threshold" not in entry:
                raise ValueError(f"config[{i}] must contain 'threshold'")
            name = entry["name"]
            if not isinstance(name, str):
                raise TypeError(f"config[{i}]['name'] must be a string")
            if name not in _VALID_VIOLATION_NAMES:
                raise ValueError(
                    f"config[{i}]['name'] must be one of "
                    f"{sorted(_VALID_VIOLATION_NAMES)}"
                )
            threshold = entry["threshold"]
            if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
                raise TypeError(f"config[{i}]['threshold'] must be a number")
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
