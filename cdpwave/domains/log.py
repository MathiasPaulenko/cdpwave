"""Log domain: browser log entries and violation reporting."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class LogDomain(BaseDomain):
    """Wrapper for the CDP Log domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Log domain events."""
        return await self._call("Log.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Log domain events."""
        return await self._call("Log.disable")

    async def clear(self) -> dict[str, Any]:
        """Clear all log entries."""
        return await self._call("Log.clear")

    async def start_violation_report(
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

    async def stop_violation_report(self) -> dict[str, Any]:
        """Stop reporting violations."""
        return await self._call("Log.stopViolationsReport")
