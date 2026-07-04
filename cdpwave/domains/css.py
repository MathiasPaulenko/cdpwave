"""CSS domain: inspect and manipulate CSS styles and stylesheets."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CSSDomain(BaseDomain):
    """Wrapper for the CDP CSS domain.

    Provides inspection and manipulation of CSS styles, stylesheets,
    computed styles, and the CSS layout tree.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the CSS domain."""
        return await self._call("CSS.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the CSS domain."""
        return await self._call("CSS.disable")

    async def get_inline_styles(
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
