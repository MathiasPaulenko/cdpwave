"""CrashReportContext domain: crash report context inspection."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CrashReportContextDomain(BaseDomain):
    """Wrapper for the CDP CrashReportContext domain.

    Provides access to crash report context entries.
    """

    async def get_entries(self) -> dict[str, Any]:
        """Get crash report context entries.

        Returns:
            Dict with ``entries`` list.
        """
        return await self._call("CrashReportContext.getEntries")
