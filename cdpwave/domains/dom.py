"""DOM domain: document inspection and element manipulation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMDomain(BaseDomain):
    """Wrapper for the CDP DOM domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable DOM domain events."""
        return await self._call("DOM.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable DOM domain events."""
        return await self._call("DOM.disable")

    async def get_document(
        self,
        depth: int = -1,
        pierce: bool = False,
    ) -> dict[str, Any]:
        """Get the DOM document tree.

        Args:
            depth: Maximum depth to traverse (-1 for full).
            pierce: Whether to pierce iframes and shadow DOM.

        Returns:
            Response dict containing ``root`` node.
        """
        return await self._call(
            "DOM.getDocument",
            {"depth": depth, "pierce": pierce},
        )

    async def get_outer_html(self, node_id: int) -> dict[str, Any]:
        """Get the outer HTML of a node.

        Args:
            node_id: The node ID to inspect.

        Returns:
            Response dict containing ``outerHTML``.
        """
        return await self._call(
            "DOM.getOuterHTML",
            {"nodeId": node_id},
        )

    async def get_inner_html(self, node_id: int) -> dict[str, Any]:
        """Get the inner HTML of a node.

        Args:
            node_id: The node ID to inspect.

        Returns:
            Response dict containing ``innerHTML``.
        """
        return await self._call(
            "DOM.getInnerHTML",
            {"nodeId": node_id},
        )

    async def query_selector(
        self,
        node_id: int,
        selector: str,
    ) -> dict[str, Any]:
        """Find the first element matching a CSS selector.

        Args:
            node_id: The root node ID to search from.
            selector: CSS selector string.

        Returns:
            Response dict containing ``nodeId`` (0 if not found).
        """
        return await self._call(
            "DOM.querySelector",
            {"nodeId": node_id, "selector": selector},
        )

    async def query_selector_all(
        self,
        node_id: int,
        selector: str,
    ) -> dict[str, Any]:
        """Find all elements matching a CSS selector.

        Args:
            node_id: The root node ID to search from.
            selector: CSS selector string.

        Returns:
            Response dict containing ``nodeIds`` list.
        """
        return await self._call(
            "DOM.querySelectorAll",
            {"nodeId": node_id, "selector": selector},
        )

    async def remove_node(self, node_id: int) -> dict[str, Any]:
        """Remove a node from the DOM.

        Args:
            node_id: The node ID to remove.
        """
        return await self._call(
            "DOM.removeNode",
            {"nodeId": node_id},
        )

    async def set_attribute_value(
        self,
        node_id: int,
        name: str,
        value: str,
    ) -> dict[str, Any]:
        """Set an attribute on a node.

        Args:
            node_id: The node ID to modify.
            name: Attribute name.
            value: Attribute value.
        """
        return await self._call(
            "DOM.setAttributeValue",
            {"nodeId": node_id, "name": name, "value": value},
        )

    async def get_attribute(
        self,
        node_id: int,
        name: str,
    ) -> dict[str, Any]:
        """Get attributes of a node.

        Args:
            node_id: The node ID to inspect.
            name: Unused; CDP returns all attributes.

        Returns:
            Response dict containing ``attributes``.
        """
        return await self._call(
            "DOM.getAttributes",
            {"nodeId": node_id},
        )

    async def focus(self, node_id: int) -> dict[str, Any]:
        """Focus a node.

        Args:
            node_id: The node ID to focus.
        """
        return await self._call(
            "DOM.focus",
            {"nodeId": node_id},
        )

    async def scroll_into_view_if_needed(self, node_id: int) -> dict[str, Any]:
        """Scroll a node into view if needed.

        Args:
            node_id: The node ID to scroll into view.
        """
        return await self._call(
            "DOM.scrollIntoViewIfNeeded",
            {"nodeId": node_id},
        )
