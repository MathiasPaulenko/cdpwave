"""Ads domain: ad metrics inspection."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AdsDomain(BaseDomain):
    """Wrapper for the CDP Ads domain.

    Provides access to ad-related metrics for testing
    ad rendering and performance.
    """

    async def get_ad_metrics(self) -> dict[str, Any]:
        """Get ad metrics for the current page.

        Returns:
            Dict with ad metrics data.
        """
        return await self._call("Ads.getAdMetrics")
