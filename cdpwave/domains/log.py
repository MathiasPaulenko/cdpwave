"""Log domain: browser log entries and violation reporting."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class LogDomain(BaseDomain):
    """Wrapper for the CDP Log domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Log domain events.

        Activates reporting of log entries from the browser, including
        console messages, JavaScript errors, and network violations.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Log domain events.

        Stops reporting of log entries. Existing entries remain until
        cleared.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.disable")

    async def clear(self) -> dict[str, Any]:
        """Clear all accumulated log entries.

        Removes all buffered log entries from the browser. Future
        entries will continue to be reported if the domain is enabled.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.clear")

    async def start_violations_report(
        self,
        config: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Start reporting violations.

        Args:
            config: List of violation config dicts (``name`` and ``threshold``).
        """
        return await self._call(
            "Log.startViolationsReport",
            {"config": config},
        )

    async def start_violation_report(
        self,
        config: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Start reporting violations.

        Deprecated alias for ``start_violations_report``.
        """
        return await self.start_violations_report(config)

    async def stop_violations_report(self) -> dict[str, Any]:
        """Stop reporting violations.

        Stops the violation reporting that was started by
        ``start_violations_report``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Log.stopViolationsReport")

    async def stop_violation_report(self) -> dict[str, Any]:
        """Stop reporting violations.

        Deprecated alias for ``stop_violations_report``.
        """
        return await self.stop_violations_report()
