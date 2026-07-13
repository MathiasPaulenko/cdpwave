"""DOMSnapshot domain wrapper for efficient DOM capture.

Experimental. Provides commands for capturing flattened DOM snapshots
including the full DOM tree (iframes, shadow DOM, template contents)
along with layout and computed style information.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMSnapshotDomain(BaseDomain):
    """DOMSnapshot domain for capturing flattened DOM snapshots.

    Experimental. Provides efficient capture of the full DOM tree
    (including iframes, shadow DOM, template contents) along with layout
    and computed style information in a single call.
    """

    async def capture_snapshot(
        self,
        computed_styles: list[str],
        include_paint_order: bool = False,
        include_dom_rects: bool = False,
        include_blended_background_colors: bool = False,
        include_text_color_opacities: bool = False,
    ) -> dict[str, Any]:
        """Capture a document snapshot with full DOM tree and computed styles.

        Returns a flattened array of documents containing the full DOM tree
        (including iframes, template contents, and imported documents),
        along with layout and whitelisted computed style information.
        Shadow DOM in the returned tree is flattened.

        Args:
            computed_styles: Whitelist of computed styles to return.
            include_paint_order: Whether to include layout object paint
                orders into the snapshot.
            include_dom_rects: Whether to include DOM rectangles
                (offsetRects, clientRects, scrollRects) into the snapshot.
            include_blended_background_colors: Experimental. Whether to
                include blended background colors in the snapshot.
            include_text_color_opacities: Experimental. Whether to include
                text color opacity in the snapshot.

        Returns:
            Dict with ``documents`` (array of DocumentSnapshot) and
            ``strings`` (shared string table).
        """
        if not isinstance(computed_styles, list):
            raise TypeError("computed_styles must be a list")
        if not isinstance(include_paint_order, bool):
            raise TypeError("include_paint_order must be a bool")
        if not isinstance(include_dom_rects, bool):
            raise TypeError("include_dom_rects must be a bool")
        if not isinstance(include_blended_background_colors, bool):
            raise TypeError("include_blended_background_colors must be a bool")
        if not isinstance(include_text_color_opacities, bool):
            raise TypeError("include_text_color_opacities must be a bool")
        params: dict[str, Any] = {
            "computedStyles": computed_styles,
            "includePaintOrder": include_paint_order,
            "includeDOMRects": include_dom_rects,
            "includeBlendedBackgroundColors": include_blended_background_colors,
            "includeTextColorOpacities": include_text_color_opacities,
        }
        return await self._call("DOMSnapshot.captureSnapshot", params)

    async def disable(self) -> dict[str, Any]:
        """Disable the DOM snapshot agent for the given page.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("DOMSnapshot.disable")

    async def enable(self) -> dict[str, Any]:
        """Enable the DOM snapshot agent for the given page.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("DOMSnapshot.enable")

    async def get_snapshot(
        self,
        computed_style_whitelist: list[str],
        include_event_listeners: bool | None = None,
        include_paint_order: bool | None = None,
        include_user_agent_shadow_tree: bool | None = None,
    ) -> dict[str, Any]:
        """Get a DOM snapshot.

        Deprecated. Use ``capture_snapshot`` instead.

        Args:
            computed_style_whitelist: Whitelist of computed style names.
            include_event_listeners: Whether to retrieve details of DOM
                listeners (default false).
            include_paint_order: Whether to include the paint order index
                of LayoutTreeNodes (default false).
            include_user_agent_shadow_tree: Whether to include UA shadow
                tree in the snapshot (default false).

        Returns:
            Dict with ``domNodes``, ``layoutTreeNodes``, and
            ``computedStyles``.
        """
        if not isinstance(computed_style_whitelist, list):
            raise TypeError("computed_style_whitelist must be a list")
        params: dict[str, Any] = {
            "computedStyleWhitelist": computed_style_whitelist,
        }
        if include_event_listeners is not None:
            if not isinstance(include_event_listeners, bool):
                raise TypeError(
                    "include_event_listeners must be a bool or None"
                )
            params["includeEventListeners"] = include_event_listeners
        if include_paint_order is not None:
            if not isinstance(include_paint_order, bool):
                raise TypeError("include_paint_order must be a bool or None")
            params["includePaintOrder"] = include_paint_order
        if include_user_agent_shadow_tree is not None:
            if not isinstance(include_user_agent_shadow_tree, bool):
                raise TypeError(
                    "include_user_agent_shadow_tree must be a bool or None"
                )
            params["includeUserAgentShadowTree"] = include_user_agent_shadow_tree
        return await self._call("DOMSnapshot.getSnapshot", params)
