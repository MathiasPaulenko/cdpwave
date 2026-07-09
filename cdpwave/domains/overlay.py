"""Overlay domain: visual highlighting and inspect mode for debugging."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class OverlayDomain(BaseDomain):
    """Wrapper for the CDP Overlay domain.

    Provides visual overlays for debugging: paint rectangles, debug
    borders, FPS counter, scroll bottleneck rects, Web Vitals, and
    node highlighting.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Overlay domain.

        Activates visual debugging overlays such as paint rectangles,
        debug borders, FPS counter, and node highlighting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Overlay domain.

        Removes all visual debugging overlays and stops reporting
        overlay-related events.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.disable")

    async def set_show_paint_rects(self, show: bool) -> dict[str, Any]:
        """Toggle paint rectangles overlay.

        Args:
            show: Whether to show paint rectangles.
        """
        return await self._call(
            "Overlay.setShowPaintRects",
            {"show": show},
        )

    async def set_show_debug_borders(self, show: bool) -> dict[str, Any]:
        """Toggle debug borders overlay.

        Args:
            show: Whether to show debug borders.
        """
        return await self._call(
            "Overlay.setShowDebugBorders",
            {"show": show},
        )

    async def set_show_fps_counter(self, show: bool) -> dict[str, Any]:
        """Toggle FPS counter overlay.

        Args:
            show: Whether to show the FPS counter.
        """
        return await self._call(
            "Overlay.setShowFPSCounter",
            {"show": show},
        )

    async def set_show_scroll_bottleneck_rects(
        self,
        show: bool,
    ) -> dict[str, Any]:
        """Toggle scroll bottleneck rectangles overlay.

        Args:
            show: Whether to show scroll bottleneck rectangles.
        """
        return await self._call(
            "Overlay.setShowScrollBottleneckRects",
            {"show": show},
        )

    async def set_show_web_vitals(
        self,
        show: bool,
        layered: bool | None = None,
    ) -> dict[str, Any]:
        """Toggle Web Vitals overlay.

        Args:
            show: Whether to show Web Vitals.
            layered: Whether to show layered Web Vitals.
        """
        params: dict[str, Any] = {"show": show}
        if layered is not None:
            params["layered"] = layered
        return await self._call("Overlay.setShowWebVitals", params)

    async def set_show_hinge(
        self,
        hinge: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set a hinge rect for foldable device simulation.

        Args:
            hinge: Optional hinge rect dict with ``x``, ``y``, ``width``,
                ``height``, and optional ``contentColor``/``outlineColor``.
                Pass ``None`` to remove the hinge.
        """
        params: dict[str, Any] = {}
        if hinge is not None:
            params["hingeConfig"] = hinge
        return await self._call("Overlay.setShowHinge", params)

    async def highlight_node(
        self,
        highlight_config: dict[str, Any] | None = None,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        selector: str | None = None,
    ) -> dict[str, Any]:
        """Highlight a DOM node with a visual overlay.

        Args:
            highlight_config: Dict with show options (``showInfo``,
                ``showStyles``, ``contentColor``, etc.). Optional.
            node_id: Optional DOM node ID.
            backend_node_id: Optional backend DOM node ID.
            object_id: Optional remote object ID.
            selector: Optional CSS selector.
        """
        params: dict[str, Any] = {}
        if highlight_config is not None:
            params["highlightConfig"] = highlight_config
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        if selector is not None:
            params["selector"] = selector
        return await self._call("Overlay.highlightNode", params)

    async def hide_highlight(self) -> dict[str, Any]:
        """Hide any active node highlight overlay.

        Removes the highlighting set by ``highlight_node`` or
        ``highlight_frame``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Overlay.hideHighlight")

    async def set_inspect_mode(
        self,
        mode: str,
        highlight_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set the inspect mode for element selection.

        Args:
            mode: ``"searchForNode"``, ``"searchForUAShadowDOM"``,
                ``"captureAreaScreenshot"``, or ``"showDistances"``.
            highlight_config: Optional highlight config for the inspect mode.
        """
        params: dict[str, Any] = {"mode": mode}
        if highlight_config is not None:
            params["highlightConfig"] = highlight_config
        return await self._call("Overlay.setInspectMode", params)

    async def set_paused_in_debugger_message(
        self,
        message: str | None = None,
    ) -> dict[str, Any]:
        """Show a paused-in-debugger message overlay.

        Args:
            message: Message to display (None to clear).
        """
        params: dict[str, Any] = {}
        if message is not None:
            params["message"] = message
        return await self._call("Overlay.setPausedInDebuggerMessage", params)

    async def set_show_viewport_size_on_resize(self, show: bool) -> dict[str, Any]:
        """Show viewport size on resize.

        Args:
            show: Whether to show the viewport size.
        """
        return await self._call(
            "Overlay.setShowViewportSizeOnResize",
            {"show": show},
        )

    async def set_show_window_controls(
        self,
        window_controls: dict[str, Any],
    ) -> dict[str, Any]:
        """Show window controls overlay.

        Args:
            window_controls: Window controls config dict.
        """
        return await self._call(
            "Overlay.setShowWindowControlsOverlay",
            {"windowControls": window_controls},
        )

    async def set_show_isolated_elements(
        self,
        isolated_element_highlight_configs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Highlight isolated elements.

        Args:
            isolated_element_highlight_configs: List of highlight configs.
        """
        return await self._call(
            "Overlay.setShowIsolatedElements",
            {"isolatedElementHighlightConfigs": isolated_element_highlight_configs},
        )

    async def highlight_quad(
        self,
        quad: list[float],
        color: dict[str, Any] | None = None,
        outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlight a quad (polygon) with a visual overlay.

        Args:
            quad: List of 8 numbers representing the quad vertices
                (x1, y1, x2, y2, x3, y3, x4, y4) in page coordinates.
            color: Optional fill color as RGBA dict
                (``{"r": 255, "g": 0, "b": 0, "a": 0.5}``).
            outline_color: Optional outline color as RGBA dict.
        """
        params: dict[str, Any] = {"quad": quad}
        if color is not None:
            params["color"] = color
        if outline_color is not None:
            params["outlineColor"] = outline_color
        return await self._call("Overlay.highlightQuad", params)

    async def highlight_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: dict[str, Any] | None = None,
        outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlight a rectangle with a visual overlay.

        Args:
            x: X coordinate of the rect in page coordinates.
            y: Y coordinate of the rect in page coordinates.
            width: Width of the rect.
            height: Height of the rect.
            color: Optional fill color as RGBA dict.
            outline_color: Optional outline color as RGBA dict.
        """
        params: dict[str, Any] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        if color is not None:
            params["color"] = color
        if outline_color is not None:
            params["outlineColor"] = outline_color
        return await self._call("Overlay.highlightRect", params)

    async def highlight_frame(
        self,
        frame_id: str,
        content_color: dict[str, Any] | None = None,
        content_outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlight a frame with a visual overlay.

        Args:
            frame_id: The frame ID to highlight.
            content_color: Optional content fill color as RGBA dict.
            content_outline_color: Optional content outline color as RGBA dict.
        """
        params: dict[str, Any] = {"frameId": frame_id}
        if content_color is not None:
            params["contentColor"] = content_color
        if content_outline_color is not None:
            params["contentOutlineColor"] = content_outline_color
        return await self._call("Overlay.highlightFrame", params)
