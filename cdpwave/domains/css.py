"""CSS domain: inspect and manipulate CSS styles and stylesheets.

This domain exposes CSS read/write operations. All CSS objects
(stylesheets, rules, and styles) have an associated id used in subsequent
operations on the related object. Each object type has a specific id
structure, and those are not interchangeable between objects of different
kinds. CSS objects can be loaded using the get*ForNode() calls (which accept
a DOM node id). A client can also keep track of stylesheets via the
styleSheetAdded/styleSheetRemoved events and subsequently load the required
stylesheet contents using the getStyleSheet[Text]() methods.

Events:
    CSS.fontsUpdated: fires whenever a web font is updated. A non-empty font
        parameter indicates a successfully loaded web font. Params: ``font``
        (FontFace, optional).
    CSS.mediaQueryResultChanged: fires whenever a MediaQuery result changes
        (for example, after a browser window has been resized.) The current
        implementation considers only viewport-dependent media features.
        No params.
    CSS.styleSheetAdded: fired whenever an active document stylesheet is
        added. Params: ``header`` (StyleSheetHeader).
    CSS.styleSheetChanged: fired whenever a stylesheet is changed as a result
        of the client operation. Params: ``styleSheetId`` (str).
    CSS.styleSheetRemoved: fired whenever an active document stylesheet is
        removed. Params: ``styleSheetId`` (str).
    CSS.computedStyleUpdated: [no description]. Params: ``nodeId`` (int).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CSSDomain(BaseDomain):
    """Wrapper for the CDP CSS domain.

    This domain exposes CSS read/write operations. All CSS objects
    (stylesheets, rules, and styles) have an associated id used in subsequent
    operations on the related object.

    Events:
        ``CSS.fontsUpdated`` -- fires whenever a web font is updated.
            Params: ``font`` (FontFace, optional).
        ``CSS.mediaQueryResultChanged`` -- fires whenever a MediaQuery result
            changes. No params.
        ``CSS.styleSheetAdded`` -- fired whenever an active document
            stylesheet is added. Params: ``header`` (StyleSheetHeader).
        ``CSS.styleSheetChanged`` -- fired whenever a stylesheet is changed
            as a result of the client operation. Params: ``styleSheetId``
            (str).
        ``CSS.styleSheetRemoved`` -- fired whenever an active document
            stylesheet is removed. Params: ``styleSheetId`` (str).
        ``CSS.computedStyleUpdated`` -- [no description]. Params: ``nodeId``
            (int).
    """

    async def add_rule(
        self,
        style_sheet_id: str,
        rule_text: str,
        location: dict[str, Any],
        node_for_property_syntax_validation: int | None = None,
    ) -> dict[str, Any]:
        """Insert a new rule with the given ruleText in a stylesheet with
        given styleSheetId, at the position specified by location.

        Args:
            style_sheet_id: The css style sheet identifier where a new rule
                should be inserted.
            rule_text: The text of a new rule.
            location: Text position of a new rule in the target style sheet.
                SourceRange dict with ``startLine``, ``startColumn``,
                ``endLine``, ``endColumn``.
            node_for_property_syntax_validation: NodeId for the DOM node in
                whose context custom property declarations for registered
                properties should be validated. If omitted, declarations in
                the new rule text can only be validated statically, which may
                produce incorrect results if the declaration contains a
                var() for example.

        Returns:
            Dict with ``rule`` CSSRule object.
        """
        params: dict[str, Any] = {
            "styleSheetId": style_sheet_id,
            "ruleText": rule_text,
            "location": location,
        }
        if node_for_property_syntax_validation:
            params["nodeForPropertySyntaxValidation"] = (
                node_for_property_syntax_validation
            )
        return await self._call("CSS.addRule", params)

    async def collect_class_names(
        self,
        style_sheet_id: str,
    ) -> dict[str, Any]:
        """Returns all class names from specified stylesheet.

        Args:
            style_sheet_id: Stylesheet ID.

        Returns:
            Dict with ``classNames`` list.
        """
        return await self._call(
            "CSS.collectClassNames",
            {"styleSheetId": style_sheet_id},
        )

    async def create_style_sheet(
        self,
        frame_id: str,
        force: bool = False,
    ) -> dict[str, Any]:
        """Creates a new special "via-inspector" stylesheet in the frame with
        given frameId.

        Args:
            frame_id: Identifier of the frame where "via-inspector"
                stylesheet should be created.
            force: If true, creates a new stylesheet for every call. If
                false, returns a stylesheet previously created by a call
                with force=false for the frame's document if it exists or
                creates a new stylesheet.

        Returns:
            Dict with ``styleSheetId``.
        """
        return await self._call(
            "CSS.createStyleSheet",
            {"frameId": frame_id, "force": force},
        )

    async def disable(self) -> dict[str, Any]:
        """Disables the CSS agent for the given page.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("CSS.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables the CSS agent for the given page.

        Clients should not assume that the CSS agent has been enabled until
        the result of this command is received.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("CSS.enable")

    async def force_pseudo_state(
        self,
        node_id: int,
        forced_pseudo_classes: list[str],
    ) -> dict[str, Any]:
        """Ensures that the given node will have specified pseudo-classes
        whenever its style is computed by the browser.

        Args:
            node_id: The element id for which to force the pseudo state.
            forced_pseudo_classes: Element pseudo classes to force when
                computing the element's style.
        """
        return await self._call(
            "CSS.forcePseudoState",
            {"nodeId": node_id, "forcedPseudoClasses": forced_pseudo_classes},
        )

    async def force_starting_style(
        self,
        node_id: int,
        forced: bool,
    ) -> dict[str, Any]:
        """Ensures that the given node is in its starting-style state.

        Args:
            node_id: The element id for which to force the starting-style
                state.
            forced: Boolean indicating if this is on or off.
        """
        return await self._call(
            "CSS.forceStartingStyle",
            {"nodeId": node_id, "forced": forced},
        )

    async def get_background_colors(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            node_id: Id of the node to get background colors for.

        Returns:
            Dict with ``backgroundColors`` list, ``computedFontSize`` str,
            ``computedFontWeight`` str.
        """
        return await self._call(
            "CSS.getBackgroundColors",
            {"nodeId": node_id},
        )

    async def get_computed_style_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Returns the computed style for a DOM node identified by nodeId.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``computedStyle`` list and ``extraFields``.
        """
        return await self._call(
            "CSS.getComputedStyleForNode",
            {"nodeId": node_id},
        )

    async def resolve_values(
        self,
        values: list[str],
        node_id: int,
        property_name: str = "",
        pseudo_type: str = "",
        pseudo_identifier: str = "",
    ) -> dict[str, Any]:
        """Resolve the specified values in the context of the provided
        element.

        For example, a value of '1em' is evaluated according to the computed
        'font-size' of the element and a value 'calc(1px + 2px)' will be
        resolved to '3px'. If the propertyName was specified the values are
        resolved as if they were property's declaration. If a value cannot be
        parsed according to the provided property syntax, the value is parsed
        using combined syntax as if null propertyName was provided. If the
        value cannot be resolved even then, return the provided value without
        any changes. Note: this function currently does not resolve CSS
        random() function, it returns unmodified random() function parts.

        Args:
            values: Cascade-dependent keywords (revert/revert-layer) do not
                work.
            node_id: Id of the node in whose context the expression is
                evaluated.
            property_name: Only longhands and custom property names are
                accepted.
            pseudo_type: Pseudo element type, only works for pseudo elements
                that generate elements in the tree, such as ::before and
                ::after.
            pseudo_identifier: Pseudo element custom ident.

        Returns:
            Dict with ``results`` list.
        """
        params: dict[str, Any] = {
            "values": values,
            "nodeId": node_id,
        }
        if property_name:
            params["propertyName"] = property_name
        if pseudo_type:
            params["pseudoType"] = pseudo_type
        if pseudo_identifier:
            params["pseudoIdentifier"] = pseudo_identifier
        return await self._call("CSS.resolveValues", params)

    async def get_longhand_properties(
        self,
        shorthand_name: str,
        value: str,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            shorthand_name: Shorthand property name.
            value: Shorthand value.

        Returns:
            Dict with ``longhandProperties`` list.
        """
        return await self._call(
            "CSS.getLonghandProperties",
            {"shorthandName": shorthand_name, "value": value},
        )

    async def get_inline_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Returns the styles defined inline (explicitly in the "style"
        attribute and implicitly, using DOM attributes) for a DOM node
        identified by nodeId.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle`` and ``attributesStyle``.
        """
        return await self._call(
            "CSS.getInlineStylesForNode",
            {"nodeId": node_id},
        )

    async def get_animated_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Returns the styles coming from animations & transitions including
        the animation & transition styles coming from inheritance chain.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``animationStyles``, ``transitionsStyle``,
            ``inherited``.
        """
        return await self._call(
            "CSS.getAnimatedStylesForNode",
            {"nodeId": node_id},
        )

    async def get_matched_styles_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Returns requested styles for a DOM node identified by nodeId.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle``, ``attributesStyle``,
            ``matchedCSSRules``, ``pseudoElements``, ``inherited``,
            ``inheritedPseudoElements``, ``cssKeyframesRules``,
            ``cssPositionTryRules``, ``activePositionFallbackIndex``,
            ``cssPropertyRules``, ``cssPropertyRegistrations``,
            ``cssAtRules``, ``parentLayoutNodeId``, ``cssFunctionRules``.
        """
        return await self._call(
            "CSS.getMatchedStylesForNode",
            {"nodeId": node_id},
        )

    async def get_environment_variables(self) -> dict[str, Any]:
        """Returns the values of the default UA-defined environment variables
        used in env().

        Returns:
            Dict with ``environmentVariables``.
        """
        return await self._call("CSS.getEnvironmentVariables")

    async def get_media_queries(self) -> dict[str, Any]:
        """Returns all media queries parsed by the rendering engine.

        Returns:
            Dict with ``medias`` list.
        """
        return await self._call("CSS.getMediaQueries")

    async def get_platform_fonts_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Requests information about platform fonts which we used to render
        child TextNodes in the given node.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``fonts`` list of PlatformFontUsage.
        """
        return await self._call(
            "CSS.getPlatformFontsForNode",
            {"nodeId": node_id},
        )

    async def get_style_sheet_text(
        self,
        style_sheet_id: str,
    ) -> dict[str, Any]:
        """Returns the current textual content for a stylesheet.

        Args:
            style_sheet_id: Stylesheet ID.

        Returns:
            Dict with ``text`` string.
        """
        return await self._call(
            "CSS.getStyleSheetText",
            {"styleSheetId": style_sheet_id},
        )

    async def get_layers_for_node(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Returns all layers parsed by the rendering engine for the tree
        scope of a node.

        Given a DOM element identified by nodeId, getLayersForNode returns
        the root layer for the nearest ancestor document or shadow root.
        The layer root contains the full layer tree for the tree scope and
        their ordering.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``rootLayer`` LayerData.
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
        """Given a CSS selector text and a style sheet ID, getLocationForSelector
        returns an array of locations of the CSS selector in the style sheet.

        Args:
            style_sheet_id: Stylesheet ID.
            selector_text: Selector text to find.

        Returns:
            Dict with ``ranges`` list of SourceRange.
        """
        return await self._call(
            "CSS.getLocationForSelector",
            {
                "styleSheetId": style_sheet_id,
                "selectorText": selector_text,
            },
        )

    async def track_computed_style_updates_for_node(
        self,
        node_id: int | None = None,
    ) -> dict[str, Any]:
        """Starts tracking the given node for the computed style updates.

        Whenever the computed style is updated for node, it queues a
        computedStyleUpdated event with throttling. There can only be 1 node
        tracked for computed style updates so passing a new node id removes
        tracking from the previous node. Pass undefined to disable tracking.

        Args:
            node_id: DOM node ID to track. Omit to disable tracking.
        """
        params: dict[str, Any] = {}
        if node_id:
            params["nodeId"] = node_id
        return await self._call(
            "CSS.trackComputedStyleUpdatesForNode",
            params,
        )

    async def track_computed_style_updates(
        self,
        properties_to_track: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Starts tracking the given computed styles for updates.

        The specified array of properties replaces the one previously
        specified. Pass empty array to disable tracking. Use
        takeComputedStyleUpdates to retrieve the list of nodes that had
        properties modified. The changes to computed style properties are
        only tracked for nodes pushed to the front-end by the DOM agent. If
        no changes to the tracked properties occur after the node has been
        pushed to the front-end, no updates will be issued for the node.

        Args:
            properties_to_track: List of ComputedStyleProperty configs to
                track.
        """
        return await self._call(
            "CSS.trackComputedStyleUpdates",
            {"propertiesToTrack": properties_to_track},
        )

    async def take_computed_style_updates(self) -> dict[str, Any]:
        """Polls the next batch of computed style updates.

        Returns:
            Dict with ``nodeIds`` list of updated node IDs.
        """
        return await self._call("CSS.takeComputedStyleUpdates")

    async def set_effective_property_value_for_node(
        self,
        node_id: int,
        property_name: str,
        value: str,
    ) -> dict[str, Any]:
        """Find a rule with the given active property for the given node and
        set the new value for this property.

        Args:
            node_id: The element id for which to set property.
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

    async def set_property_rule_property_name(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        property_name: str,
    ) -> dict[str, Any]:
        """Modifies the property rule property name.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            property_name: New property name.

        Returns:
            Dict with ``propertyName`` Value.
        """
        return await self._call(
            "CSS.setPropertyRulePropertyName",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "propertyName": property_name,
            },
        )

    async def set_keyframe_key(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        key_text: str,
    ) -> dict[str, Any]:
        """Modifies the keyframe rule key text.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            key_text: New keyframe key text.

        Returns:
            Dict with ``keyText`` Value.
        """
        return await self._call(
            "CSS.setKeyframeKey",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "keyText": key_text,
            },
        )

    async def set_media_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Modifies the expression of a media at-rule.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            text: New media query text.

        Returns:
            Dict with ``media`` Media.
        """
        return await self._call(
            "CSS.setMediaText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "text": text,
            },
        )

    async def set_container_query_condition_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """[no description].

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            text: New container query condition text.

        Returns:
            Dict with ``containerQuery`` ContainerQuery.
        """
        return await self._call(
            "CSS.setContainerQueryConditionText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "text": text,
            },
        )

    async def set_supports_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Modifies the expression of a supports at-rule.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            text: New supports query text.

        Returns:
            Dict with ``supports`` Supports.
        """
        return await self._call(
            "CSS.setSupportsText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "text": text,
            },
        )

    async def set_navigation_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Modifies the expression of a navigation at-rule.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            text: New navigation text.

        Returns:
            Dict with ``navigation`` Navigation.
        """
        return await self._call(
            "CSS.setNavigationText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "text": text,
            },
        )

    async def set_scope_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        text: str,
    ) -> dict[str, Any]:
        """Modifies the expression of a scope at-rule.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            text: New scope text.

        Returns:
            Dict with ``scope`` Scope.
        """
        return await self._call(
            "CSS.setScopeText",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "text": text,
            },
        )

    async def set_rule_selector(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        selector: str,
    ) -> dict[str, Any]:
        """Modifies the rule selector.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict.
            selector: New selector text.

        Returns:
            Dict with ``selectorList`` SelectorList.
        """
        return await self._call(
            "CSS.setRuleSelector",
            {
                "styleSheetId": style_sheet_id,
                "range": range_,
                "selector": selector,
            },
        )

    async def set_style_sheet_text(
        self,
        style_sheet_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Sets the new stylesheet text.

        Args:
            style_sheet_id: Stylesheet ID.
            text: New text content.

        Returns:
            Dict with ``sourceMapURL`` string.
        """
        return await self._call(
            "CSS.setStyleSheetText",
            {"styleSheetId": style_sheet_id, "text": text},
        )

    async def set_style_texts(
        self,
        edits: list[dict[str, Any]],
        node_for_property_syntax_validation: int | None = None,
    ) -> dict[str, Any]:
        """Applies specified style edits one after another in the given
        order.

        Args:
            edits: List of StyleDeclarationEdit dicts, each with
                ``styleSheetId``, ``text``, and optional ``range``.
            node_for_property_syntax_validation: NodeId for the DOM node in
                whose context custom property declarations for registered
                properties should be validated. If omitted, declarations in
                the new rule text can only be validated statically, which may
                produce incorrect results if the declaration contains a
                var() for example.

        Returns:
            Dict with ``styles`` list of Style.
        """
        params: dict[str, Any] = {"edits": edits}
        if node_for_property_syntax_validation:
            params["nodeForPropertySyntaxValidation"] = (
                node_for_property_syntax_validation
            )
        return await self._call("CSS.setStyleTexts", params)

    async def start_rule_usage_tracking(self) -> dict[str, Any]:
        """Enables the selector recording.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("CSS.startRuleUsageTracking")

    async def stop_rule_usage_tracking(self) -> dict[str, Any]:
        """Stop tracking rule usage and return the list of rules that were
        used since last call to takeCoverageDelta (or since start of
        coverage instrumentation).

        Returns:
            Dict with ``ruleUsage`` list.
        """
        return await self._call("CSS.stopRuleUsageTracking")

    async def take_coverage_delta(self) -> dict[str, Any]:
        """Obtain list of rules that became used since last call to this
        method (or since start of coverage instrumentation).

        Returns:
            Dict with ``coverage`` list and ``timestamp`` float.
        """
        return await self._call("CSS.takeCoverageDelta")

    async def set_local_fonts_enabled(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enables/disables rendering of local CSS fonts (enabled by
        default).

        Args:
            enabled: Whether rendering of local fonts is enabled.
        """
        return await self._call(
            "CSS.setLocalFontsEnabled",
            {"enabled": enabled},
        )

    # -- Convenience methods below (not direct CDP commands) --

    async def get_inline_styles(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Alias for ``get_inline_styles_for_node``.

        Args:
            node_id: DOM node ID.

        Returns:
            Dict with ``inlineStyle`` and ``attributesStyle``.
        """
        return await self.get_inline_styles_for_node(node_id)

    async def get_stylesheet_text(
        self,
        style_sheet_id: str,
    ) -> dict[str, Any]:
        """Alias for ``get_style_sheet_text``.

        Args:
            style_sheet_id: Stylesheet ID.

        Returns:
            Dict with ``text`` string.
        """
        return await self.get_style_sheet_text(style_sheet_id)

    async def set_stylesheet_text(
        self,
        style_sheet_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Alias for ``set_style_sheet_text``.

        Args:
            style_sheet_id: Stylesheet ID.
            text: New text content.

        Returns:
            Dict with ``sourceMapURL`` string.
        """
        return await self.set_style_sheet_text(style_sheet_id, text)

    async def set_rule_style(
        self,
        style_sheet_id: str,
        style_text: str,
        range_: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set the style text of a CSS rule in a stylesheet.

        Convenience wrapper for ``set_style_texts`` with a single edit.

        Args:
            style_sheet_id: The stylesheet ID.
            style_text: The new style text (e.g. ``"color: green"``).
            range_: Optional SourceRange dict. If omitted, the edit will
                not include a range.

        Returns:
            Dict with ``styles`` list.
        """
        edit: dict[str, Any] = {
            "styleSheetId": style_sheet_id,
            "text": style_text,
        }
        if range_ is not None:
            edit["range"] = range_
        return await self.set_style_texts([edit])

    async def set_style_text(
        self,
        style_sheet_id: str,
        range_: dict[str, Any],
        style_text: str,
    ) -> dict[str, Any]:
        """Set the text of a CSS style in a stylesheet.

        Convenience wrapper for ``set_style_texts`` with a single edit
        that includes a range.

        Args:
            style_sheet_id: Stylesheet ID.
            range_: SourceRange dict with ``startLine``, ``startColumn``,
                ``endLine``, ``endColumn``.
            style_text: New CSS style text.

        Returns:
            Dict with ``styles`` list.
        """
        return await self.set_style_texts(
            [
                {
                    "styleSheetId": style_sheet_id,
                    "range": range_,
                    "text": style_text,
                }
            ]
        )
