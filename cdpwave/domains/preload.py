"""Preload domain: control speculative loading and prefetching."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PreloadDomain(BaseDomain):
    """Wrapper for the CDP Preload domain.

    Provides control over speculative loading, prefetching, and
    prerendering of pages for performance optimization.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Preload domain."""
        return await self._call("Preload.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Preload domain."""
        return await self._call("Preload.disable")

    async def get_preload_policy(self) -> dict[str, Any]:
        """Get the current preload policy.

        Returns:
            Dict with ``preloadPolicy`` string.
        """
        return await self._call("Preload.getPreloadPolicy")

    async def set_preload_policy(
        self,
        preload_policy: str,
    ) -> dict[str, Any]:
        """Set the preload policy.

        Args:
            preload_policy: Policy name (e.g. ``"always"``,
                ``"no-preload"``, ``"eligible-non-mobile"``).
        """
        return await self._call(
            "Preload.setPreloadPolicy",
            {"preloadPolicy": preload_policy},
        )
