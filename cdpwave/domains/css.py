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
            "CSS.getInlineStylesForNode",
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

    async def collect_class_names(
        self,
        style_sheet_id: str,
    ) -> dict[str, Any]:
        """Collect class names from a stylesheet.

        Args:
            style_sheet_id: Stylesheet ID.

        Returns:
            Dict with ``classNames`` list.
        """
        return await self._call(
            "CSS.collectClassNames",
            {"styleSheetId": style_sheet_id},
        )

    async def force_starting_style(
        self,
        node_id: int,
        starting_style: dict[str, Any],
    ) -> dict[str, Any]:
        """Force a starting style on a node.

        Args:
            node_id: DOM node ID.
            starting_style: Starting style dict.
        """
        return await self._call(
            "CSS.forceStartingStyle",
            {"nodeId": node_id, "startingStyle": starting_style},
        )

    async def get_animated_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get animated styles for a node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``animations`` and ``transitions``.
        """
        return await self._call(
            "CSS.getAnimatedStylesForNode",
            {"nodeId": node_id},
        )

    async def get_environment_variables(self) -> dict[str, Any]:
        """Get CSS environment variables.

        Returns:
            Dict with ``envVars`` list.
        """
        return await self._call("CSS.getEnvironmentVariables")

    async def get_layers_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get layers for a node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``layerId`` and ``compositedLayers``.
        """
        return await self._call(
            "CSS.getLayersForNode",
            {"nodeId": node_id},
        )

    async def get_location_for_selector(
        self,
        style_sheet_id: str,
        selector_text: str,
    ) -> dict[str, Any]:
        """Get the source range for a selector in a stylesheet.

        Args:
            style_sheet_id: Stylesheet ID.
            selector_text: Selector text to find.

        Returns:
            Dict with ``range`` SourceRange.
        """
        return await self._call(
            "CSS.getLocationForSelector",
            {
                "styleSheetId": style_sheet_id,
                "selectorText": selector_text,
            },
        )

    async def get_longhand_properties(
        self,
        style_sheet_id: str,
        shorthand_name: str,
    ) -> dict[str, Any]:
        """Get longhand properties for a shorthand.

        Args:
            style_sheet_id: Stylesheet ID.
            shorthand_name: Shorthand property name.

        Returns:
            Dict with ``properties`` list.
        """
        return await self._call(
            "CSS.getLonghandProperties",
            {
                "styleSheetId": style_sheet_id,
                "shorthandName": shorthand_name,
            },
        )

    async def resolve_values(
        self,
        values: list[str],
        node_id: int | None = None,
    ) -> dict[str, Any]:
        """Resolve CSS values.

        Args:
            values: List of CSS values to resolve.
            node_id: Optional DOM node ID for context.

        Returns:
            Dict with ``values`` list of resolved values.
        """
        params: dict[str, Any] = {"values": values}
        if node_id is not None:
            params["nodeId"] = node_id
        return await self._call("CSS.resolveValues", params)

    async def set_container_query_condition_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set container query condition text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New condition text.
        """
        return await self._call(
            "CSS.setContainerQueryConditionText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def set_container_query_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set container query text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New container query text.
        """
        return await self._call(
            "CSS.setContainerQueryText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def set_effective_property_value_for_node(
        self,
        node_id: int,
        property_name: str,
        value: str,
    ) -> dict[str, Any]:
        """Set effective property value for a node.

        Args:
            node_id: DOM node ID.
            property_name: CSS property name.
            value: Property value.
        """
        return await self._call(
            "CSS.setEffectivePropertyValueForNode",
            {
                "nodeId": node_id,
                "propertyName": property_name,
                "value": value,
            },
        )

    async def set_keyframe_key(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        key_text: str,
    ) -> dict[str, Any]:
        """Set keyframe key.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            key_text: New keyframe key text.
        """
        return await self._call(
            "CSS.setKeyframeKey",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "keyText": key_text,
            },
        )

    async def set_local_fonts_enabled(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable local fonts.

        Args:
            enabled: Whether to enable local fonts.
        """
        return await self._call(
            "CSS.setLocalFontsEnabled",
            {"enabled": enabled},
        )

    async def set_media_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set media query text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New media query text.
        """
        return await self._call(
            "CSS.setMediaText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def set_navigation_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set navigation text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New navigation text.
        """
        return await self._call(
            "CSS.setNavigationText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def set_property_rule_property_name(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        name: str,
    ) -> dict[str, Any]:
        """Set property rule property name.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            name: New property name.
        """
        return await self._call(
            "CSS.setPropertyRulePropertyName",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "name": name,
            },
        )

    async def set_scope_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set scope text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New scope text.
        """
        return await self._call(
            "CSS.setScopeText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def set_supports_text(
        self,
        style_sheet_id: str,
        range_start: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Set supports query text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_start: Source range dict.
            text: New supports query text.
        """
        return await self._call(
            "CSS.setSupportsText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_start,
                "text": text,
            },
        )

    async def take_computed_style_updates(self) -> dict[str, Any]:
        """Get computed style updates.

        Returns:
            Dict with ``nodeIds`` list of updated nodes.
        """
        return await self._call("CSS.takeComputedStyleUpdates")

    async def track_computed_style_updates(
        self,
        properties_to_track: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Track computed style updates for properties.

        Args:
            properties_to_track: List of property configs to track.
        """
        return await self._call(
            "CSS.trackComputedStyleUpdates",
            {"propertiesToTrack": properties_to_track},
        )

    async def track_computed_style_updates_for_node(
        self,
        node_id: int,
        properties_to_track: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Track computed style updates for a specific node.

        Args:
            node_id: DOM node ID.
            properties_to_track: List of property configs to track.
        """
        return await self._call(
            "CSS.trackComputedStyleUpdatesForNode",
            {
                "nodeId": node_id,
                "propertiesToTrack": properties_to_track,
            },
        )
