"""CSS domain: inspect and manipulate CSS styles and stylesheets."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CSSDomain(BaseDomain):
    """Wrapper for the CDP CSS domain.

    Provides inspection and manipulation of CSS styles, stylesheets,
    computed styles, and the CSS layout tree.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the CSS domain.

        Activates CSS domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("CSS.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the CSS domain.

        Deactivates CSS domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("CSS.disable")

    async def get_inline_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get inline styles for a DOM node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle`` and ``attributesStyle``.
        """
        return await self._call(
            "CSS.getInlineStyles",
            {"nodeId": node_id},
        )

    async def get_inline_styles(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get inline styles for a DOM node.

        Alias for ``get_inline_styles_for_node``.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle`` and ``attributesStyle``.
        """
        return await self.get_inline_styles_for_node(node_id)

    async def get_matched_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get matched styles for a DOM node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle``, ``attributesStyle``,
            ``matchedCSSRules``, ``pseudoElements``, ``inherited``.
        """
        return await self._call(
            "CSS.getMatchedStylesForNode",
            {"nodeId": node_id},
        )

    async def get_platform_fonts_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get platform fonts for a DOM node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``fonts`` list.
        """
        return await self._call(
            "CSS.getPlatformFontsForNode",
            {"nodeId": node_id},
        )

    async def get_computed_style_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get computed styles for a DOM node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``computedStyle`` list of name/value pairs.
        """
        return await self._call(
            "CSS.getComputedStyleForNode",
            {"nodeId": node_id},
        )

    async def get_layout_tree_and_styles(
        self,
        node_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """Get the layout tree and computed styles.

        Args:
            node_ids: Optional list of node IDs to query.

        Returns:
            Dict with ``layoutTree`` and ``computedStyles``.
        """
        params: dict[str, Any] = {}
        if node_ids is not None:
            params["nodeIds"] = node_ids
        return await self._call("CSS.getLayoutTreeAndStyles", params)

    async def get_stylesheet_text(
        self,
        stylesheet_id: str,
    ) -> dict[str, Any]:
        """Get the text content of a stylesheet.

        Args:
            stylesheet_id: Stylesheet ID.

        Returns:
            Dict with ``text`` string.
        """
        return await self._call(
            "CSS.getStyleSheetText",
            {"styleSheetId": stylesheet_id},
        )

    async def set_stylesheet_text(
        self,
        stylesheet_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Set the text content of a stylesheet.

        Args:
            stylesheet_id: Stylesheet ID.
            text: New text content.
        """
        return await self._call(
            "CSS.setStyleSheetText",
            {"styleSheetId": stylesheet_id, "text": text},
        )

    async def get_media_queries(self) -> dict[str, Any]:
        """Get all media queries.

        Returns:
            Dict with ``medias`` list.
        """
        return await self._call("CSS.getMediaQueries")

    async def add_rule(
        self,
        style_sheet_id: str,
        rule_text: str,
        location: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a CSS rule to a stylesheet.

        Args:
            style_sheet_id: Stylesheet ID to add the rule to.
            rule_text: CSS rule text (e.g. ``".cls { color: red; }"``).
            location: Optional location dict for insertion point.

        Returns:
            Dict with ``rule`` CSSRule object.
        """
        params: dict[str, Any] = {
            "styleSheetId": style_sheet_id,
            "ruleText": rule_text,
        }
        if location is not None:
            params["location"] = location
        return await self._call("CSS.addRule", params)

    async def set_rule_style(
        self,
        style_sheet_id: str,
        selector: str,
        style_text: str,
    ) -> dict[str, Any]:
        """Set the style text of a CSS rule in a stylesheet.

        Args:
            style_sheet_id: The stylesheet ID.
            selector: The selector of the rule to update.
            style_text: The new style text (e.g. ``"color: green"``).

        Returns:
            Response dict from ``CSS.setStyleTexts``.
        """
        return await self._call(
            "CSS.setStyleTexts",
            {
                "edits": [
                    {
                        "styleSheetId": style_sheet_id,
                        "text": style_text,
                    }
                ]
            },
        )

    async def set_style_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        style_text: str,
    ) -> dict[str, Any]:
        """Set the text of a CSS style in a stylesheet.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict with ``startLine``, ``startColumn``,
                ``endLine``, ``endColumn``.
            style_text: New CSS style text.
        """
        return await self._call(
            "CSS.setStyleTexts",
            {
                "edits": [
                    {
                        "styleSheetId": style_sheet_id,
                        "range": range_start,
                        "text": style_text,
                    }
                ],
            },
        )

    async def set_rule_selector(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        selector: str,
    ) -> dict[str, Any]:
        """Set the selector of a CSS rule.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            selector: New selector text.
        """
        return await self._call(
            "CSS.setRuleSelector",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "selector": selector,
            },
        )

    async def create_style_sheet(
        self,
        frame_id: str,
    ) -> dict[str, Any]:
        """Create a new stylesheet in the given frame.

        Args:
            frame_id: Frame ID to create the stylesheet in.

        Returns:
            Dict with ``styleSheetId``.
        """
        return await self._call(
            "CSS.createStyleSheet",
            {"frameId": frame_id},
        )

    async def get_background_colors(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get background colors for a node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``backgroundColors`` list.
        """
        return await self._call(
            "CSS.getBackgroundColors",
            {"nodeId": node_id},
        )

    async def force_pseudo_state(
        self,
        node_id: int,
        pseudo_state: list[str],
    ) -> dict[str, Any]:
        """Force a pseudo state on a node.

        Args:
            node_id: DOM node ID.
            pseudo_state: List of pseudo states (e.g. ``["hover"]``).
        """
        return await self._call(
            "CSS.forcePseudoState",
            {"nodeId": node_id, "forcedPseudoClasses": pseudo_state},
        )

    async def start_rule_usage_tracking(self) -> dict[str, Any]:
        """Start rule usage tracking."""
        return await self._call("CSS.startRuleUsageTracking")

    async def stop_rule_usage_tracking(self) -> dict[str, Any]:
        """Stop rule usage tracking."""
        return await self._call("CSS.stopRuleUsageTracking")

    async def take_coverage_delta(self) -> dict[str, Any]:
        """Get coverage delta for CSS rules."""
        return await self._call("CSS.takeCoverageDelta")
