"""DOM domain: document inspection and element manipulation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMDomain(BaseDomain):
    """Wrapper for the CDP DOM domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable DOM domain events.

        Activates reporting of DOM document updates, attribute changes,
        and node modifications. Must be called before using most
        other DOM methods.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("DOM.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable DOM domain events.

        Stops reporting of DOM document updates and node modifications.

        Returns:
            Response dict from the CDP.
        """
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
    ) -> dict[str, Any]:
        """Get attributes of a node.

        Args:
            node_id: The node ID to inspect.

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

    async def remove_attribute(
        self,
        node_id: int,
        name: str,
    ) -> dict[str, Any]:
        """Remove an attribute from a node.

        Args:
            node_id: The node ID to modify.
            name: Attribute name to remove.
        """
        return await self._call(
            "DOM.removeAttribute",
            {"nodeId": node_id, "name": name},
        )

    async def describe_node(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        depth: int = -1,
        pierce: bool = False,
    ) -> dict[str, Any]:
        """Describe a DOM node.

        Args:
            node_id: Node ID to describe.
            backend_node_id: Backend node ID.
            object_id: Remote object ID.
            depth: Maximum depth to traverse (-1 for full).
            pierce: Whether to pierce iframes and shadow DOM.

        Returns:
            Dict with ``node`` descriptor.
        """
        params: dict[str, Any] = {"depth": depth, "pierce": pierce}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("DOM.describeNode", params)

    async def get_box_model(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the box model of a node.

        Returns content, padding, border, and margin quads.

        Args:
            node_id: Node ID to query.
            backend_node_id: Backend node ID.
            object_id: Remote object ID.

        Returns:
            Dict with ``model`` containing ``content``, ``padding``,
            ``border``, ``margin``, ``width``, ``height``.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("DOM.getBoxModel", params)

    async def get_node_for_location(
        self,
        x: int,
        y: int,
        include_user_agent_shadow_dom: bool = False,
    ) -> dict[str, Any]:
        """Get the node at a given screen location.

        Args:
            x: X coordinate relative to the document.
            y: Y coordinate relative to the document.
            include_user_agent_shadow_dom: Include UA shadow DOM.

        Returns:
            Dict with ``nodeId``, ``backendNodeId``, ``frameId``.
        """
        params: dict[str, Any] = {"x": x, "y": y}
        if include_user_agent_shadow_dom:
            params["includeUserAgentShadowDOM"] = True
        return await self._call("DOM.getNodeForLocation", params)

    async def resolve_node(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_group: str | None = None,
    ) -> dict[str, Any]:
        """Resolve a DOM node to a remote object.

        Args:
            node_id: Node ID to resolve.
            backend_node_id: Backend node ID.
            object_group: Optional object group.

        Returns:
            Dict with ``object`` remote object descriptor.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_group is not None:
            params["objectGroup"] = object_group
        return await self._call("DOM.resolveNode", params)

    async def request_node(self, node_id: int) -> dict[str, Any]:
        """Request a node by ID.

        Args:
            node_id: Node ID to request.

        Returns:
            Dict with ``node`` descriptor.
        """
        return await self._call("DOM.requestNode", {"nodeId": node_id})

    async def set_attributes_as_text(
        self,
        node_id: int,
        text: str,
        name: str | None = None,
    ) -> dict[str, Any]:
        """Set multiple attributes on a node from text.

        Parses the text as HTML attributes and applies them to the node.

        Args:
            node_id: Node ID to modify.
            text: Attribute text (e.g. ``"class='foo' id='bar'"``).
            name: Optional attribute name to replace.
        """
        params: dict[str, Any] = {"nodeId": node_id, "text": text}
        if name is not None:
            params["name"] = name
        return await self._call("DOM.setAttributesAsText", params)

    async def copy_to(
        self,
        node_id: int,
        target_node_id: int,
        insert_before_node_id: int | None = None,
    ) -> dict[str, Any]:
        """Copy a node to another location in the DOM.

        Args:
            node_id: Node ID to copy.
            target_node_id: Parent node ID to copy into.
            insert_before_node_id: Node ID to insert before.
        """
        params: dict[str, Any] = {
            "nodeId": node_id,
            "targetNodeId": target_node_id,
        }
        if insert_before_node_id is not None:
            params["insertBeforeNodeId"] = insert_before_node_id
        return await self._call("DOM.copyTo", params)

    async def move_to(
        self,
        node_id: int,
        target_node_id: int,
        insert_before_node_id: int | None = None,
    ) -> dict[str, Any]:
        """Move a node to another location in the DOM.

        Args:
            node_id: Node ID to move.
            target_node_id: Parent node ID to move into.
            insert_before_node_id: Node ID to insert before.

        Returns:
            Dict with ``nodeId`` of the moved node.
        """
        params: dict[str, Any] = {
            "nodeId": node_id,
            "targetNodeId": target_node_id,
        }
        if insert_before_node_id is not None:
            params["insertBeforeNodeId"] = insert_before_node_id
        return await self._call("DOM.moveTo", params)

    async def request_child_nodes(
        self,
        node_id: int,
        depth: int = -1,
        pierce: bool = False,
    ) -> dict[str, Any]:
        """Request child nodes of a node.

        Args:
            node_id: Node ID to request children for.
            depth: Maximum depth to traverse (-1 for full).
            pierce: Whether to pierce iframes and shadow DOM.
        """
        return await self._call(
            "DOM.requestChildNodes",
            {"nodeId": node_id, "depth": depth, "pierce": pierce},
        )

    async def perform_search(
        self,
        query: str,
        include_user_agent_shadow_dom: bool = False,
    ) -> dict[str, Any]:
        """Search the DOM for a query.

        Supports XPath and CSS selectors.

        Args:
            query: Search query (XPath or CSS selector).
            include_user_agent_shadow_dom: Include UA shadow DOM.

        Returns:
            Dict with ``searchId``, ``resultCount``.
        """
        params: dict[str, Any] = {"query": query}
        if include_user_agent_shadow_dom:
            params["includeUserAgentShadowDOM"] = True
        return await self._call("DOM.performSearch", params)

    async def get_search_results(
        self,
        search_id: str,
        from_index: int,
        to_index: int,
    ) -> dict[str, Any]:
        """Get search results from a previous search.

        Args:
            search_id: Search ID from ``perform_search``.
            from_index: Start index.
            to_index: End index.

        Returns:
            Dict with ``nodeIds`` list.
        """
        return await self._call(
            "DOM.getSearchResults",
            {
                "searchId": search_id,
                "fromIndex": from_index,
                "toIndex": to_index,
            },
        )

    async def discard_search_results(self, search_id: str) -> dict[str, Any]:
        """Discard search results.

        Args:
            search_id: Search ID from ``perform_search``.
        """
        return await self._call(
            "DOM.discardSearchResults",
            {"searchId": search_id},
        )

    async def set_node_value(
        self,
        node_id: int,
        value: str,
    ) -> dict[str, Any]:
        """Set the value of a node (for input/textarea/select).

        Args:
            node_id: Node ID to modify.
            value: New value.
        """
        return await self._call(
            "DOM.setNodeValue",
            {"nodeId": node_id, "value": value},
        )
