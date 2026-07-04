"""HeadlessExperimental domain: headless mode control (experimental)."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class HeadlessExperimentalDomain(BaseDomain):
    """Wrapper for the CDP HeadlessExperimental domain.

    Provides control over headless window bounds for testing
    viewport-dependent behavior in headless mode.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the HeadlessExperimental domain.

        Activates HeadlessExperimental domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeadlessExperimental.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the HeadlessExperimental domain.

        Deactivates HeadlessExperimental domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeadlessExperimental.disable")

    async def set_window_bounds(
        self,
        window_id: int | None = None,
        bounds: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set headless window bounds.

        Args:
            window_id: Optional window ID. Defaults to the current window.
            bounds: Bounds dict with optional ``left``, ``top``,
                ``width``, ``height``, and ``windowState`` fields.
        """
        params: dict[str, Any] = {}
        if window_id is not None:
            params["windowId"] = window_id
        if bounds is not None:
            params["bounds"] = bounds
        return await self._call(
            "HeadlessExperimental.setWindowBounds", params
        )
