"""Overlay domain: visual highlighting and inspect mode for debugging.

This domain is **experimental** in the Chrome DevTools Protocol.

Provides various functionality related to drawing atop the inspected page.

Events:
    Overlay.inspectNodeRequested: Fired when the user selects node by
        clicking on it in inspect mode.
        Parameters:
            nodeId (int): The node id of the inspected node.

    Overlay.nodeHighlightRequested: Fired when user selects a node by
        hovering over it in inspect mode.
        Parameters:
            nodeId (int): The node id of the inspected node.

    Overlay.inspectModeCanceled: Fired when inspect mode is canceled.
        No parameters.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_COLOR_FORMATS = frozenset({"rgb", "hsl", "hwb", "hex"})
_VALID_INSPECT_MODES = frozenset({
    "searchForNode",
    "searchForUAShadowDOM",
    "captureAreaScreenshot",
    "none",
})


class OverlayDomain(BaseDomain):
    """Wrapper for the CDP Overlay domain.

    Provides visual overlays for debugging: paint rectangles, debug
    borders, FPS counter, scroll bottleneck rects, and node highlighting.

    This domain is **experimental** in the Chrome DevTools Protocol.

    Events:
        Overlay.inspectNodeRequested: Fired when the user selects node
            by clicking on it in inspect mode.
        Overlay.nodeHighlightRequested: Fired when user selects a node
            by hovering over it in inspect mode.
        Overlay.inspectModeCanceled: Fired when inspect mode is canceled.
    """

    async def disable(self) -> dict[str, Any]:
        """Disables domain notifications.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables domain notifications.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.enable")

    async def get_grid_highlight_objects_for_test(
        self,
        node_ids: list[int],
    ) -> dict[str, Any]:
        """For Persistent Grid testing.

        Args:
            node_ids: Ids of the node to get highlight object for.

        Returns:
            Dict with ``highlights`` (Grid Highlight data for the
            node ids provided).
        """
        if not isinstance(node_ids, list):
            raise TypeError("node_ids must be a list")
        return await self._call(
            "Overlay.getGridHighlightObjectsForTest",
            {"nodeIds": node_ids},
        )

    async def get_highlight_object_for_test(
        self,
        node_id: int,
        include_distance: bool = False,
        include_style: bool = False,
        color_format: str | None = None,
        show_accessibility_info: bool = True,
    ) -> dict[str, Any]:
        """For testing.

        Args:
            node_id: Id of the node to get highlight object for.
            include_distance: Whether to include distance info
                (default: false).
            include_style: Whether to include style info (default: false).
            color_format: The color format to get config with
                (default: hex). One of ``"rgb"``, ``"hsl"``, ``"hwb"``,
                ``"hex"``.
            show_accessibility_info: Whether to show accessibility info
                (default: true).

        Returns:
            Dict with ``highlight`` (Highlight data for the node).
        """
        if not isinstance(node_id, int):
            raise TypeError("node_id must be an int")
        if not isinstance(include_distance, bool):
            raise TypeError("include_distance must be a bool")
        if not isinstance(include_style, bool):
            raise TypeError("include_style must be a bool")
        if not isinstance(show_accessibility_info, bool):
            raise TypeError("show_accessibility_info must be a bool")
        params: dict[str, Any] = {
            "nodeId": node_id,
            "includeDistance": include_distance,
            "includeStyle": include_style,
            "showAccessibilityInfo": show_accessibility_info,
        }
        if color_format is not None:
            if not isinstance(color_format, str):
                raise TypeError("color_format must be a str or None")
            if color_format and color_format not in _VALID_COLOR_FORMATS:
                raise ValueError(
                    "color_format must be 'rgb', 'hsl', 'hwb', or 'hex'"
                )
            if color_format:
                params["colorFormat"] = color_format
        return await self._call("Overlay.getHighlightObjectForTest", params)

    async def get_source_order_highlight_object_for_test(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """For Source Order Viewer testing.

        Args:
            node_id: Id of the node to highlight.

        Returns:
            Dict with ``highlight`` (Source order highlight data for
            the node id provided).
        """
        if not isinstance(node_id, int):
            raise TypeError("node_id must be an int")
        return await self._call(
            "Overlay.getSourceOrderHighlightObjectForTest",
            {"nodeId": node_id},
        )

    async def hide_highlight(self) -> dict[str, Any]:
        """Hides any highlight.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.hideHighlight")

    async def highlight_node(
        self,
        highlight_config: dict[str, Any],
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        selector: str | None = None,
    ) -> dict[str, Any]:
        """Highlights DOM node with given id or with the given JavaScript
        object wrapper. Either nodeId or objectId must be specified.

        Args:
            highlight_config: A descriptor for the highlight appearance.
            node_id: Identifier of the node to highlight.
            backend_node_id: Identifier of the backend node to highlight.
            object_id: JavaScript object id of the node to be highlighted.
            selector: Selectors to highlight relevant nodes.
        """
        if not isinstance(highlight_config, dict):
            raise TypeError("highlight_config must be a dict")
        params: dict[str, Any] = {"highlightConfig": highlight_config}
        if node_id is not None:
            if not isinstance(node_id, int):
                raise TypeError("node_id must be an int or None")
            params["nodeId"] = node_id
        if backend_node_id is not None:
            if not isinstance(backend_node_id, int):
                raise TypeError("backend_node_id must be an int or None")
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            if not isinstance(object_id, str):
                raise TypeError("object_id must be a str or None")
            if object_id:
                params["objectId"] = object_id
        if selector is not None:
            if not isinstance(selector, str):
                raise TypeError("selector must be a str or None")
            if selector:
                params["selector"] = selector
        return await self._call("Overlay.highlightNode", params)

    async def highlight_quad(
        self,
        quad: list[float],
        color: dict[str, Any] | None = None,
        outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlights given quad. Coordinates are absolute with respect to
        the main frame viewport.

        Args:
            quad: Quad to highlight (list of 8 numbers: x1, y1, x2, y2,
                x3, y3, x4, y4).
            color: The highlight fill color (default: transparent).
                RGBA dict with ``r``, ``g``, ``b``, ``a``.
            outline_color: The highlight outline color (default:
                transparent). RGBA dict.
        """
        if not isinstance(quad, list):
            raise TypeError("quad must be a list")
        params: dict[str, Any] = {"quad": quad}
        if color is not None:
            if not isinstance(color, dict):
                raise TypeError("color must be a dict or None")
            params["color"] = color
        if outline_color is not None:
            if not isinstance(outline_color, dict):
                raise TypeError("outline_color must be a dict or None")
            params["outlineColor"] = outline_color
        return await self._call("Overlay.highlightQuad", params)

    async def highlight_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: dict[str, Any] | None = None,
        outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlights given rectangle. Coordinates are absolute with respect
        to the main frame viewport.

        Note: This method does not handle device pixel ratio (DPR)
        correctly. The coordinates currently have to be adjusted by
        the client if DPR is not 1 (see crbug.com/437807128).

        Args:
            x: X coordinate.
            y: Y coordinate.
            width: Rectangle width.
            height: Rectangle height.
            color: The highlight fill color (default: transparent).
                RGBA dict with ``r``, ``g``, ``b``, ``a``.
            outline_color: The highlight outline color (default:
                transparent). RGBA dict.
        """
        if not isinstance(x, int):
            raise TypeError("x must be an int")
        if not isinstance(y, int):
            raise TypeError("y must be an int")
        if not isinstance(width, int):
            raise TypeError("width must be an int")
        if not isinstance(height, int):
            raise TypeError("height must be an int")
        params: dict[str, Any] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        if color is not None:
            if not isinstance(color, dict):
                raise TypeError("color must be a dict or None")
            params["color"] = color
        if outline_color is not None:
            if not isinstance(outline_color, dict):
                raise TypeError("outline_color must be a dict or None")
            params["outlineColor"] = outline_color
        return await self._call("Overlay.highlightRect", params)

    async def highlight_source_order(
        self,
        source_order_config: dict[str, Any],
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Highlights the source order of the children of the DOM node with
        given id or with the given JavaScript object wrapper. Either nodeId
        or objectId must be specified.

        Args:
            source_order_config: A descriptor for the appearance of the
                overlay drawing.
            node_id: Identifier of the node to highlight.
            backend_node_id: Identifier of the backend node to highlight.
            object_id: JavaScript object id of the node to be highlighted.
        """
        if not isinstance(source_order_config, dict):
            raise TypeError("source_order_config must be a dict")
        params: dict[str, Any] = {"sourceOrderConfig": source_order_config}
        if node_id is not None:
            if not isinstance(node_id, int):
                raise TypeError("node_id must be an int or None")
            params["nodeId"] = node_id
        if backend_node_id is not None:
            if not isinstance(backend_node_id, int):
                raise TypeError("backend_node_id must be an int or None")
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            if not isinstance(object_id, str):
                raise TypeError("object_id must be a str or None")
            if object_id:
                params["objectId"] = object_id
        return await self._call("Overlay.highlightSourceOrder", params)

    async def set_inspect_mode(
        self,
        mode: str,
        highlight_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Enters the 'inspect' mode. In this mode, elements that user is
        hovering over are highlighted. Backend then generates
        'inspectNodeRequested' event upon element selection.

        Args:
            mode: Set an inspection mode. One of ``"searchForNode"``,
                ``"searchForUAShadowDOM"``, ``"captureAreaScreenshot"``,
                ``"none"``.
            highlight_config: A descriptor for the highlight appearance
                of hovered-over nodes. May be omitted if enabled == false.
        """
        if not isinstance(mode, str):
            raise TypeError("mode must be a str")
        if mode not in _VALID_INSPECT_MODES:
            raise ValueError(
                "mode must be 'searchForNode', 'searchForUAShadowDOM', "
                "'captureAreaScreenshot', or 'none'"
            )
        params: dict[str, Any] = {"mode": mode}
        if highlight_config is not None:
            if not isinstance(highlight_config, dict):
                raise TypeError("highlight_config must be a dict or None")
            params["highlightConfig"] = highlight_config
        return await self._call("Overlay.setInspectMode", params)

    async def set_paused_in_debugger_message(
        self,
        message: str | None = None,
    ) -> dict[str, Any]:
        """Sets paused-in-debugger message.

        Args:
            message: The message to display, also triggers resume and
                step over controls.
        """
        params: dict[str, Any] = {}
        if message is not None:
            if not isinstance(message, str):
                raise TypeError("message must be a str or None")
            if message:
                params["message"] = message
        return await self._call(
            "Overlay.setPausedInDebuggerMessage", params or None,
        )

    async def set_show_ad_highlights(self, show: bool) -> dict[str, Any]:
        """Highlights owner element of all frames detected to be ads.

        Args:
            show: True for showing ad highlights.
        """
        if not isinstance(show, bool):
            raise TypeError("show must be a bool")
        return await self._call(
            "Overlay.setShowAdHighlights",
            {"show": show},
        )

    async def set_show_container_query_overlays(
        self,
        container_query_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Show container query overlays.

        Args:
            container_query_highlight_configs: An array of node
                identifiers and descriptors for the highlight appearance.
        """
        if not isinstance(container_query_highlight_configs, list):
            raise TypeError("container_query_highlight_configs must be a list")
        return await self._call(
            "Overlay.setShowContainerQueryOverlays",
            {"containerQueryHighlightConfigs": container_query_highlight_configs},
        )

    async def set_show_debug_borders(self, show: bool) -> dict[str, Any]:
        """Requests that backend shows debug borders on layers.

        Args:
            show: True for showing debug borders.
        """
        if not isinstance(show, bool):
            raise TypeError("show must be a bool")
        return await self._call(
            "Overlay.setShowDebugBorders",
            {"show": show},
        )

    async def set_show_display_cutout(
        self,
        display_cutout_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a display cutout overlay.

        Args:
            display_cutout_config: Display cutout data, null means hide
                display cutout.
        """
        params: dict[str, Any] = {}
        if display_cutout_config is not None:
            if not isinstance(display_cutout_config, dict):
                raise TypeError("display_cutout_config must be a dict or None")
            params["displayCutoutConfig"] = display_cutout_config
        return await self._call("Overlay.setShowDisplayCutout", params or None)

    async def set_show_flex_overlays(
        self,
        flex_node_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Show flex overlays.

        Args:
            flex_node_highlight_configs: An array of node identifiers
                and descriptors for the highlight appearance.
        """
        if not isinstance(flex_node_highlight_configs, list):
            raise TypeError("flex_node_highlight_configs must be a list")
        return await self._call(
            "Overlay.setShowFlexOverlays",
            {"flexNodeHighlightConfigs": flex_node_highlight_configs},
        )

    async def set_show_fps_counter(self, show: bool) -> dict[str, Any]:
        """Requests that backend shows the FPS counter.

        Args:
            show: True for showing the FPS counter.
        """
        if not isinstance(show, bool):
            raise TypeError("show must be a bool")
        return await self._call(
            "Overlay.setShowFPSCounter",
            {"show": show},
        )

    async def set_show_grid_overlays(
        self,
        grid_node_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Highlight multiple elements with the CSS Grid overlay.

        Args:
            grid_node_highlight_configs: An array of node identifiers
                and descriptors for the highlight appearance.
        """
        if not isinstance(grid_node_highlight_configs, list):
            raise TypeError("grid_node_highlight_configs must be a list")
        return await self._call(
            "Overlay.setShowGridOverlays",
            {"gridNodeHighlightConfigs": grid_node_highlight_configs},
        )

    async def set_show_hinge(
        self,
        hinge_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a dual screen device hinge.

        Args:
            hinge_config: Hinge data, null means hideHinge. A
                HingeConfig dict with ``rect`` (required) and optional
                ``contentColor``/``outlineColor``.
        """
        params: dict[str, Any] = {}
        if hinge_config is not None:
            if not isinstance(hinge_config, dict):
                raise TypeError("hinge_config must be a dict or None")
            params["hingeConfig"] = hinge_config
        return await self._call("Overlay.setShowHinge", params or None)

    async def set_show_inspected_element_anchor(
        self,
        inspected_element_anchor_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Show inspected element anchor.

        Args:
            inspected_element_anchor_config: Node identifier for which
                to show an anchor for. An
                InspectedElementAnchorConfig dict with ``nodeId``
                (optional) and ``backendNodeId`` (optional).
        """
        if not isinstance(inspected_element_anchor_config, dict):
            raise TypeError("inspected_element_anchor_config must be a dict")
        return await self._call(
            "Overlay.setShowInspectedElementAnchor",
            {"inspectedElementAnchorConfig": inspected_element_anchor_config},
        )

    async def set_show_isolated_elements(
        self,
        isolated_element_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Show elements in isolation mode with overlays.

        Args:
            isolated_element_highlight_configs: An array of node
                identifiers and descriptors for the highlight appearance.
        """
        if not isinstance(isolated_element_highlight_configs, list):
            raise TypeError("isolated_element_highlight_configs must be a list")
        return await self._call(
            "Overlay.setShowIsolatedElements",
            {"isolatedElementHighlightConfigs": isolated_element_highlight_configs},
        )

    async def set_show_layout_shift_regions(self, result: bool) -> dict[str, Any]:
        """Requests that backend shows layout shift regions.

        Args:
            result: True for showing layout shift regions.
        """
        if not isinstance(result, bool):
            raise TypeError("result must be a bool")
        return await self._call(
            "Overlay.setShowLayoutShiftRegions",
            {"result": result},
        )

    async def set_show_paint_rects(self, result: bool) -> dict[str, Any]:
        """Requests that backend shows paint rectangles.

        Args:
            result: True for showing paint rectangles.
        """
        if not isinstance(result, bool):
            raise TypeError("result must be a bool")
        return await self._call(
            "Overlay.setShowPaintRects",
            {"result": result},
        )

    async def set_show_scroll_bottleneck_rects(
        self,
        show: bool,
    ) -> dict[str, Any]:
        """Requests that backend shows scroll bottleneck rects.

        Args:
            show: True for showing scroll bottleneck rects.
        """
        if not isinstance(show, bool):
            raise TypeError("show must be a bool")
        return await self._call(
            "Overlay.setShowScrollBottleneckRects",
            {"show": show},
        )

    async def set_show_scroll_snap_overlays(
        self,
        scroll_snap_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Show scroll snap overlays.

        Args:
            scroll_snap_highlight_configs: An array of node identifiers
                and descriptors for the highlight appearance.
        """
        if not isinstance(scroll_snap_highlight_configs, list):
            raise TypeError("scroll_snap_highlight_configs must be a list")
        return await self._call(
            "Overlay.setShowScrollSnapOverlays",
            {"scrollSnapHighlightConfigs": scroll_snap_highlight_configs},
        )

    async def set_show_viewport_size_on_resize(self, show: bool) -> dict[str, Any]:
        """Paints viewport size upon main frame resize.

        Args:
            show: Whether to paint size or not.
        """
        if not isinstance(show, bool):
            raise TypeError("show must be a bool")
        return await self._call(
            "Overlay.setShowViewportSizeOnResize",
            {"show": show},
        )

    async def set_show_window_controls_overlay(
        self,
        window_controls_overlay_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Show Window Controls Overlay for PWA.

        Args:
            window_controls_overlay_config: Window Controls Overlay
                data, null means hide Window Controls Overlay. A
                WindowControlsOverlayConfig dict with ``showCSS``
                (bool), ``selectedPlatform`` (str), and ``themeColor``
                (str).
        """
        params: dict[str, Any] = {}
        if window_controls_overlay_config is not None:
            if not isinstance(window_controls_overlay_config, dict):
                raise TypeError(
                    "window_controls_overlay_config must be a dict or None"
                )
            params["windowControlsOverlayConfig"] = window_controls_overlay_config
        return await self._call(
            "Overlay.setShowWindowControlsOverlay", params or None,
        )
