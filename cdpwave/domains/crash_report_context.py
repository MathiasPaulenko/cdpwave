"""CrashReportContext domain: crash report context inspection.

This domain is **experimental**.

Depends on: Page.

Types:
    CrashReportContextEntry

Commands:
    getEntries

Events:
    (none)
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CrashReportContextDomain(BaseDomain):
    """Wrapper for the CDP CrashReportContext domain.

    This domain is **experimental**.

    Exposes the current state of the CrashReportContext API,
    providing access to crash report context entries across all
    frames in the page.
    """

    async def get_entries(self) -> dict[str, Any]:
        """Return all entries in the CrashReportContext across all frames.

        Returns:
            Dict with ``entries`` key containing a list of
            ``CrashReportContextEntry`` objects. Each entry has
            ``key`` (string), ``value`` (string), and ``frameId``
            (Page.FrameId).
        """
        return await self._call("CrashReportContext.getEntries")
