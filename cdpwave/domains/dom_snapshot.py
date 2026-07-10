"""DOMSnapshot domain wrapper for efficient DOM capture."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMSnapshotDomain(BaseDomain):
    """DOMSnapshot domain for capturing flattened DOM snapshots.

    Provides efficient capture of the full DOM tree (including iframes,
    shadow DOM, template contents) along with layout and computed style
    information in a single call.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the DOM snapshot agent for the current page."""
        return await self._call("DOMSnapshot.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the DOM snapshot agent for the current page."""
        return await self._call("DOMSnapshot.disable")

    async def capture_snapshot(
        self,
        computed_styles: list[str] | None = None,
        include_paint_order: bool | None = None,
        include_dom_rects: bool | None = None,
        include_blended_background_colors: bool | None = None,
        include_text_color_opacities: bool | None = None,
    ) -> dict[str, Any]:
        """Capture a document snapshot with full DOM tree and computed styles.

        Returns a flattened array of documents containing the full DOM tree
        (including iframes, template contents, and imported documents),
        along with layout and whitelisted computed style information.
        Shadow DOM in the returned tree is flattened.

        Args:
            computed_styles: Whitelist of computed styles to return.
            include_paint_order: Whether to include layout object paint orders.
            include_dom_rects: Whether to include DOM rectangles
                (offsetRects, clientRects, scrollRects).
            include_blended_background_colors: Whether to include blended
                background colors (experimental).
            include_text_color_opacities: Whether to include text color
                opacity (experimental).

        Returns:
            Dict with ``documents`` (array of DocumentSnapshot) and
            ``strings`` (shared string table).
        """
        params: dict[str, Any] = {}
        if computed_styles is not None:
            params["computedStyles"] = computed_styles
        if include_paint_order is not None:
            params["includePaintOrder"] = include_paint_order
        if include_dom_rects is not None:
            params["includeDOMRects"] = include_dom_rects
        if include_blended_background_colors is not None:
            params["includeBlendedBackgroundColors"] = include_blended_background_colors
        if include_text_color_opacities is not None:
            params["includeTextColorOpacities"] = include_text_color_opacities
        return await self._call("DOMSnapshot.captureSnapshot", params)

    async def get_snapshot(
        self,
        computed_style_whitelist: list[str],
        include_event_listeners: bool | None = None,
        include_paint_order: bool | None = None,
        include_user_agent_shadow_tree: bool | None = None,
    ) -> dict[str, Any]:
        """Get a DOM snapshot (deprecated, prefer ``capture_snapshot``).

        Args:
            computed_style_whitelist: Whitelist of computed style names.
            include_event_listeners: Whether to include event listeners.
            include_paint_order: Whether to include paint order.
            include_user_agent_shadow_tree: Whether to include UA shadow tree.

        Returns:
            Dict with ``domNodes``, ``layoutTreeNodes``, ``computedStyles``.
        """
        params: dict[str, Any] = {
            "computedStyleWhitelist": computed_style_whitelist,
        }
        if include_event_listeners is not None:
            params["includeEventListeners"] = include_event_listeners
        if include_paint_order is not None:
            params["includePaintOrder"] = include_paint_order
        if include_user_agent_shadow_tree is not None:
            params["includeUserAgentShadowTree"] = include_user_agent_shadow_tree
        return await self._call("DOMSnapshot.getSnapshot", params)
