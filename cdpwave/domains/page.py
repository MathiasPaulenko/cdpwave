"""Page domain: navigation, screenshots, and PDF generation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PageDomain(BaseDomain):
    """Wrapper for the CDP Page domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Page domain events."""
        return await self._call("Page.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Page domain events."""
        return await self._call("Page.disable")

    async def navigate(
        self,
        url: str,
        referrer: str | None = None,
        transition_type: str | None = None,
    ) -> dict[str, Any]:
        """Navigate the page to a URL.

        Args:
            url: The URL to navigate to.
            referrer: Optional referrer URL.
            transition_type: Optional transition type hint.

        Returns:
            Response dict containing ``frameId`` and ``loaderId``.
        """
        params: dict[str, Any] = {"url": url}
        if referrer is not None:
            params["referrer"] = referrer
        if transition_type is not None:
            params["transitionType"] = transition_type
        return await self._call("Page.navigate", params)

    async def reload(self, ignore_cache: bool = False) -> dict[str, Any]:
        """Reload the current page.

        Args:
            ignore_cache: If True, bypass the browser cache.
        """
        return await self._call(
            "Page.reload",
            {"ignoreCache": ignore_cache},
        )

    async def stop(self) -> dict[str, Any]:
        """Stop all pending navigations."""
        return await self._call("Page.stop")

    async def capture_screenshot(
        self,
        format: str = "png",
        quality: int = 80,
        clip: dict[str, Any] | None = None,
        from_surface: bool = True,
        capture_beyond_viewport: bool = False,
    ) -> dict[str, Any]:
        """Capture a screenshot of the page.

        Args:
            format: Image format (``"png"`` or ``"jpeg"``).
            quality: JPEG quality (0-100). Ignored for PNG.
            clip: Optional clip region dict with x, y, width, height, scale.
            from_surface: Capture from the surface rather than the view.
            capture_beyond_viewport: Capture content beyond the viewport.

        Returns:
            Response dict containing base64-encoded ``data``.
        """
        params: dict[str, Any] = {
            "format": format,
            "quality": quality,
            "fromSurface": from_surface,
            "captureBeyondViewport": capture_beyond_viewport,
        }
        if clip is not None:
            params["clip"] = clip
        return await self._call("Page.captureScreenshot", params)

    async def print_to_pdf(
        self,
        landscape: bool = False,
        display_header_footer: bool = False,
        print_background: bool = False,
        scale: float = 1.0,
        paper_width: float = 8.5,
        paper_height: float = 11.0,
        margin_top: float = 0.4,
        margin_bottom: float = 0.4,
        margin_left: float = 0.4,
        margin_right: float = 0.4,
    ) -> dict[str, Any]:
        """Print the page to PDF.

        Args:
            landscape: Use landscape orientation.
            display_header_footer: Include header/footer.
            print_background: Print background graphics.
            scale: Scale factor (0.1 to 2.0).
            paper_width: Paper width in inches.
            paper_height: Paper height in inches.
            margin_top: Top margin in inches.
            margin_bottom: Bottom margin in inches.
            margin_left: Left margin in inches.
            margin_right: Right margin in inches.

        Returns:
            Response dict containing base64-encoded ``data``.
        """
        return await self._call(
            "Page.printToPDF",
            {
                "landscape": landscape,
                "displayHeaderFooter": display_header_footer,
                "printBackground": print_background,
                "scale": scale,
                "paperWidth": paper_width,
                "paperHeight": paper_height,
                "marginTop": margin_top,
                "marginBottom": margin_bottom,
                "marginLeft": margin_left,
                "marginRight": margin_right,
            },
        )

    async def get_layout_metrics(self) -> dict[str, Any]:
        """Return page layout metrics (viewport, content size)."""
        return await self._call("Page.getLayoutMetrics")

    async def get_navigation_history(self) -> dict[str, Any]:
        """Return the navigation history of the page."""
        return await self._call("Page.getNavigationHistory")
