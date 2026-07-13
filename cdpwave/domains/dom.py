"""DOM domain: document inspection and element manipulation."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_WHITESPACE = frozenset({"none", "all"})
_VALID_RELATIONS = frozenset({
    "PopoverTarget",
    "InterestTarget",
    "CommandFor",
    "controlledby",
})
_VALID_PHYSICAL_AXES = frozenset({"Horizontal", "Vertical", "Both"})
_VALID_LOGICAL_AXES = frozenset({"Inline", "Block", "Both"})


class DOMDomain(BaseDomain):
    """Wrapper for the CDP DOM domain."""

    async def enable(
        self,
        include_whitespace: str | None = None,
    ) -> dict[str, Any]:
        """Enable DOM domain events.

        Activates reporting of DOM document updates, attribute changes,
        and node modifications. Must be called before using most
        other DOM methods.

        Args:
            include_whitespace: Whether to include whitespaces in
                the children array of returned Nodes. One of
                ``"none"`` or ``"all"``.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {}
        if include_whitespace is not None:
            if not isinstance(include_whitespace, str):
                raise TypeError("include_whitespace must be a str or None")
            if include_whitespace not in _VALID_WHITESPACE:
                raise ValueError(
                    "include_whitespace must be 'none' or 'all'"
                )
            params["includeWhitespace"] = include_whitespace
        return await self._call("DOM.enable", params)

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
            Typed as ``DOMGetDocumentResult`` for autocompletion.
        """
        if depth < -1:
            raise ValueError("depth must be >= -1")
        params: dict[str, Any] = {"depth": depth}
        if pierce:
            params["pierce"] = pierce
        return await self._call(
            "DOM.getDocument",
            params,
        )

    async def get_outer_html(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        include_shadow_dom: bool = False,
    ) -> dict[str, Any]:
        """Get the outer HTML of a node.

        Args:
            node_id: Identifier of the node.
            backend_node_id: Identifier of the backend node.
            object_id: JavaScript object id of the node wrapper.
            include_shadow_dom: Include all shadow roots.

        Returns:
            Response dict containing ``outerHTML``.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        if include_shadow_dom:
            params["includeShadowDOM"] = True
        return await self._call("DOM.getOuterHTML", params)

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
        name: str | None = None,
    ) -> dict[str, Any]:
        """Get attributes of a node.

        If ``name`` is provided, returns the value of that specific
        attribute. Otherwise returns all attributes.

        Args:
            node_id: The node ID to inspect.
            name: Optional attribute name to retrieve.

        Returns:
            Response dict containing ``attributes`` (flat list of
            name/value pairs) or ``value`` (single attribute value
            when ``name`` is provided).
        """
        result = await self._call(
            "DOM.getAttributes",
            {"nodeId": node_id},
        )
        if name is not None:
            attrs = result.get("attributes", [])
            for i in range(0, len(attrs) - 1, 2):
                if attrs[i] == name:
                    return {"value": attrs[i + 1]}
            return {"value": None}
        return result

    async def focus(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Focus a node.

        Args:
            node_id: Identifier of the node.
            backend_node_id: Identifier of the backend node.
            object_id: JavaScript object id of the node wrapper.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("DOM.focus", params)

    async def scroll_into_view_if_needed(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        rect: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Scroll a node into view if needed.

        Args:
            node_id: Identifier of the node.
            backend_node_id: Identifier of the backend node.
            object_id: JavaScript object id of the node wrapper.
            rect: The rect to be scrolled into view, relative to
                the node's border box, in CSS pixels. When omitted,
                center of the node will be used.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        if rect is not None:
            params["rect"] = rect
        return await self._call("DOM.scrollIntoViewIfNeeded", params)

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
        if depth < -1:
            raise ValueError("depth must be >= -1")
        params: dict[str, Any] = {"depth": depth}
        if pierce:
            params["pierce"] = pierce
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
        ignore_pointer_events_none: bool = False,
    ) -> dict[str, Any]:
        """Get the node at a given screen location.

        Args:
            x: X coordinate relative to the document.
            y: Y coordinate relative to the document.
            include_user_agent_shadow_dom: Include UA shadow DOM.
            ignore_pointer_events_none: Whether to ignore
                pointer-events: none on elements and hit test them.

        Returns:
            Dict with ``backendNodeId``, ``frameId``, and optional
            ``nodeId`` (only when DOM domain is enabled).
        """
        params: dict[str, Any] = {"x": x, "y": y}
        if include_user_agent_shadow_dom:
            params["includeUserAgentShadowDOM"] = True
        if ignore_pointer_events_none:
            params["ignorePointerEventsNone"] = True
        return await self._call("DOM.getNodeForLocation", params)

    async def resolve_node(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_group: str | None = None,
        execution_context_id: int | None = None,
    ) -> dict[str, Any]:
        """Resolve a DOM node to a remote object.

        Args:
            node_id: Node ID to resolve.
            backend_node_id: Backend node ID to resolve.
            object_group: Optional symbolic group name for releasing
                multiple objects.
            execution_context_id: Execution context in which to
                resolve the node.

        Returns:
            Dict with ``object`` remote object descriptor.

        Raises:
            ValueError: If neither ``node_id`` nor ``backend_node_id``
                is provided.
        """
        if node_id is None and backend_node_id is None:
            raise ValueError(
                "Either node_id or backend_node_id must be provided"
            )
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_group is not None:
            params["objectGroup"] = object_group
        if execution_context_id is not None:
            params["executionContextId"] = execution_context_id
        return await self._call("DOM.resolveNode", params)

    async def request_node(
        self,
        object_id: str,
    ) -> dict[str, Any]:
        """Request a node by JavaScript object reference.

        Args:
            object_id: JavaScript object id to convert into node.

        Returns:
            Dict with ``nodeId`` of the requested node.
        """
        return await self._call(
            "DOM.requestNode",
            {"objectId": object_id},
        )

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
        if depth < -1:
            raise ValueError("depth must be >= -1")
        params: dict[str, Any] = {"nodeId": node_id, "depth": depth}
        if pierce:
            params["pierce"] = pierce
        return await self._call(
            "DOM.requestChildNodes",
            params,
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

    async def get_flattened_document(
        self,
        depth: int = -1,
        pierce: bool = False,
    ) -> dict[str, Any]:
        """Get the flattened DOM document tree.

        Deprecated: Use ``get_document`` instead.

        Args:
            depth: Maximum depth to traverse (-1 for full).
            pierce: Whether to pierce iframes and shadow DOM.

        Returns:
            Response dict containing ``root`` node.
        """
        if depth < -1:
            raise ValueError("depth must be >= -1")
        params: dict[str, Any] = {"depth": depth}
        if pierce:
            params["pierce"] = pierce
        return await self._call(
            "DOM.getFlattenedDocument",
            params,
        )

    async def collect_class_names_from_subtree(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Collect class names from all descendants of a node.

        Args:
            node_id: Node ID to collect class names from.

        Returns:
            Dict with ``classNames`` list.
        """
        return await self._call(
            "DOM.collectClassNamesFromSubtree",
            {"nodeId": node_id},
        )

    async def get_content_quads(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Get content quads for a node.

        Args:
            node_id: Identifier of the node.
            backend_node_id: Identifier of the backend node.
            object_id: JavaScript object id of the node wrapper.

        Returns:
            Dict with ``quads`` list.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("DOM.getContentQuads", params)

    async def set_file_input_files(
        self,
        files: list[str],
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Set files for a file input element.

        Args:
            files: List of file paths to set.
            node_id: Identifier of the node.
            backend_node_id: Identifier of the backend node.
            object_id: JavaScript object id of the node wrapper.
        """
        params: dict[str, Any] = {"files": files}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("DOM.setFileInputFiles", params)

    async def set_outer_html(
        self,
        node_id: int,
        outer_html: str,
    ) -> dict[str, Any]:
        """Set the outer HTML of a node.

        Args:
            node_id: Node ID to modify.
            outer_html: New outer HTML content.
        """
        return await self._call(
            "DOM.setOuterHTML",
            {"nodeId": node_id, "outerHTML": outer_html},
        )

    async def set_text_content(
        self,
        node_id: int,
        text: str,
    ) -> dict[str, Any]:
        """Set the text content of a node.

        Uses ``DOM.setNodeValue`` to set the value. Only works for
        text nodes and processing instructions.

        Args:
            node_id: Node ID to modify.
            text: New text content.
        """
        return await self._call(
            "DOM.setNodeValue",
            {"nodeId": node_id, "value": text},
        )

    async def undo(self) -> dict[str, Any]:
        """Undo the last DOM modification."""
        return await self._call("DOM.undo")

    async def redo(self) -> dict[str, Any]:
        """Redo the last undone DOM modification."""
        return await self._call("DOM.redo")

    async def mark_undoable_state(self) -> dict[str, Any]:
        """Mark an undoable state in the DOM modification history."""
        return await self._call("DOM.markUndoableState")

    async def hide_highlight(self) -> dict[str, Any]:
        """Hide any highlighted node."""
        return await self._call("Overlay.hideHighlight")

    async def highlight_node(
        self,
        highlight_config: dict[str, Any],
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        selector: str | None = None,
    ) -> dict[str, Any]:
        """Highlight a node in the browser.

        Redirects to ``Overlay.highlightNode``.

        Args:
            highlight_config: Dict with show options (``showInfo``,
                ``contentColor``, ``borderColor``, etc.).
            node_id: Optional DOM node ID.
            backend_node_id: Optional backend DOM node ID.
            object_id: Optional remote object ID.
            selector: Optional CSS selector.
        """
        params: dict[str, Any] = {"highlightConfig": highlight_config}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        if selector is not None:
            params["selector"] = selector
        return await self._call("Overlay.highlightNode", params)

    async def highlight_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: dict[str, Any] | None = None,
        outline_color: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Highlight a rectangular area in the browser.

        Redirects to ``Overlay.highlightRect``.

        Args:
            x: X coordinate.
            y: Y coordinate.
            width: Width of the rectangle.
            height: Height of the rectangle.
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

    async def push_node_by_path_to_frontend(
        self,
        path: str,
    ) -> dict[str, Any]:
        """Push a node by path to the frontend.

        Args:
            path: Node path (e.g. ``"0,1,2,3"``).

        Returns:
            Dict with ``nodeId``.
        """
        return await self._call(
            "DOM.pushNodeByPathToFrontend",
            {"path": path},
        )

    async def push_nodes_by_backend_ids_to_frontend(
        self,
        backend_node_ids: list[int],
    ) -> dict[str, Any]:
        """Push nodes by backend IDs to the frontend.

        Args:
            backend_node_ids: List of backend node IDs.

        Returns:
            Dict with ``nodeIds`` list.
        """
        return await self._call(
            "DOM.pushNodesByBackendIdsToFrontend",
            {"backendNodeIds": backend_node_ids},
        )

    async def get_nodes_for_subtree_by_style(
        self,
        node_id: int,
        computed_styles: list[dict[str, str]],
        pierce: bool = False,
    ) -> dict[str, Any]:
        """Find nodes in a subtree that match computed styles.

        Args:
            node_id: Root node ID to search from.
            computed_styles: List of CSS computed style properties
                to filter nodes by (includes nodes if any of
                properties matches). Each entry is a dict with
                ``name`` and ``value`` keys.
            pierce: Whether to pierce shadow DOM.

        Returns:
            Dict with ``nodeIds`` list.
        """
        params: dict[str, Any] = {
            "nodeId": node_id,
            "computedStyles": computed_styles,
        }
        if pierce:
            params["pierce"] = pierce
        return await self._call(
            "DOM.getNodesForSubtreeByStyle",
            params,
        )

    async def get_relayout_boundary(self, node_id: int) -> dict[str, Any]:
        """Get the relayout boundary for a node.

        Args:
            node_id: Node ID to query.

        Returns:
            Dict with ``nodeId`` of the relayout boundary node.
        """
        return await self._call(
            "DOM.getRelayoutBoundary",
            {"nodeId": node_id},
        )

    async def get_top_layer_elements(self) -> dict[str, Any]:
        """Get elements in the top layer.

        Returns:
            Dict with ``nodeIds`` list.
        """
        return await self._call("DOM.getTopLayerElements")

    async def get_element_by_relation(
        self,
        node_id: int,
        relation: str,
    ) -> dict[str, Any]:
        """Get an element by relation.

        Args:
            node_id: Id of the node from which to query the relation.
            relation: Type of relation to get. One of
                ``"PopoverTarget"``, ``"InterestTarget"``,
                ``"CommandFor"``, ``"controlledby"``.

        Returns:
            Dict with ``nodeId`` of the matching element.
        """
        if not isinstance(node_id, int):
            raise TypeError("node_id must be an int")
        if not isinstance(relation, str):
            raise TypeError("relation must be a str")
        if relation not in _VALID_RELATIONS:
            raise ValueError(
                "relation must be 'PopoverTarget', 'InterestTarget', "
                "'CommandFor', or 'controlledby'"
            )
        return await self._call(
            "DOM.getElementByRelation",
            {"nodeId": node_id, "relation": relation},
        )

    async def set_node_stack_traces_enabled(
        self,
        enable: bool,
    ) -> dict[str, Any]:
        """Enable or disable node stack traces.

        Args:
            enable: Whether to capture stack traces for DOM nodes.
        """
        return await self._call(
            "DOM.setNodeStackTracesEnabled",
            {"enable": enable},
        )

    async def get_node_stack_traces(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get stack traces for a node.

        Args:
            node_id: Node ID to query.

        Returns:
            Dict with optional ``creation`` stack trace.
        """
        return await self._call(
            "DOM.getNodeStackTraces",
            {"nodeId": node_id},
        )

    async def get_file_info(self, object_id: str) -> dict[str, Any]:
        """Get file info for a File wrapper.

        Args:
            object_id: JavaScript object id of the File wrapper.

        Returns:
            Dict with ``path``.
        """
        return await self._call("DOM.getFileInfo", {"objectId": object_id})

    async def get_detached_dom_nodes(self) -> dict[str, Any]:
        """Get detached DOM nodes.

        Returns:
            Dict with ``detachedNodes`` list.
        """
        return await self._call("DOM.getDetachedDomNodes")

    async def set_inspected_node(self, node_id: int) -> dict[str, Any]:
        """Set the inspected node for console $0 reference.

        Args:
            node_id: Node ID to set as inspected.
        """
        return await self._call(
            "DOM.setInspectedNode",
            {"nodeId": node_id},
        )

    async def set_node_name(
        self,
        node_id: int,
        name: str,
    ) -> dict[str, Any]:
        """Set the tag name of a node.

        Args:
            node_id: Node ID to rename.
            name: New tag name.

        Returns:
            Dict with ``nodeId`` of the new node.
        """
        return await self._call(
            "DOM.setNodeName",
            {"nodeId": node_id, "name": name},
        )

    async def get_frame_owner(self, frame_id: str) -> dict[str, Any]:
        """Get the owner node of a frame.

        Args:
            frame_id: Frame ID to find the owner for.

        Returns:
            Dict with ``backendNodeId`` and optional ``nodeId``.
        """
        return await self._call(
            "DOM.getFrameOwner",
            {"frameId": frame_id},
        )

    async def get_container_for_node(
        self,
        node_id: int,
        container_name: str | None = None,
        physical_axes: str | None = None,
        logical_axes: str | None = None,
        queries_scroll_state: bool = False,
        queries_anchored: bool = False,
    ) -> dict[str, Any]:
        """Get the query container of a given node.

        Args:
            node_id: Node ID to find the container for.
            container_name: Optional container name to match.
            physical_axes: Physical axes to match. One of
                ``"Horizontal"``, ``"Vertical"``, ``"Both"``.
            logical_axes: Logical axes to match. One of
                ``"Inline"``, ``"Block"``, ``"Both"``.
            queries_scroll_state: Whether to query scroll-state.
            queries_anchored: Whether to query anchored elements.

        Returns:
            Dict with ``nodeId`` of the container.
        """
        params: dict[str, Any] = {"nodeId": node_id}
        if container_name is not None:
            params["containerName"] = container_name
        if physical_axes is not None:
            if not isinstance(physical_axes, str):
                raise TypeError("physical_axes must be a str or None")
            if physical_axes not in _VALID_PHYSICAL_AXES:
                raise ValueError(
                    "physical_axes must be 'Horizontal', 'Vertical', or 'Both'"
                )
            params["physicalAxes"] = physical_axes
        if logical_axes is not None:
            if not isinstance(logical_axes, str):
                raise TypeError("logical_axes must be a str or None")
            if logical_axes not in _VALID_LOGICAL_AXES:
                raise ValueError(
                    "logical_axes must be 'Inline', 'Block', or 'Both'"
                )
            params["logicalAxes"] = logical_axes
        if queries_scroll_state:
            params["queriesScrollState"] = True
        if queries_anchored:
            params["queriesAnchored"] = True
        return await self._call("DOM.getContainerForNode", params)

    async def get_querying_descendants_for_container(
        self,
        node_id: int,
    ) -> dict[str, Any]:
        """Get querying descendants for a container node.

        Args:
            node_id: Container node ID.

        Returns:
            Dict with ``nodeIds`` list.
        """
        return await self._call(
            "DOM.getQueryingDescendantsForContainer",
            {"nodeId": node_id},
        )

    async def get_anchor_element(
        self,
        node_id: int,
        anchor_specifier: str | None = None,
    ) -> dict[str, Any]:
        """Get the anchor element for a positioned element.

        Args:
            node_id: Id of the positioned element from which to find
                the anchor.
            anchor_specifier: Optional anchor specifier, as defined in
                the CSS Anchor Positioning spec. If not provided, the
                implicit anchor element is returned.

        Returns:
            Dict with ``nodeId`` of the anchor element.
        """
        params: dict[str, Any] = {"nodeId": node_id}
        if anchor_specifier is not None:
            params["anchorSpecifier"] = anchor_specifier
        return await self._call("DOM.getAnchorElement", params)

    async def force_show_popover(
        self,
        node_id: int,
        enable: bool,
        invoker_node_id: int | None = None,
    ) -> dict[str, Any]:
        """Force show or hide a popover element.

        When enabled, force-opens the popover and keeps it open until
        disabled.

        Args:
            node_id: Node ID of the popover HTMLElement.
            enable: If true, opens the popover and keeps it open.
                If false, closes the popover if previously force-opened.
            invoker_node_id: Optional backend node ID of the invoking
                element, used to establish the implicit anchor.

        Returns:
            Dict with ``nodeIds`` of popovers closed to respect
            stacking order.
        """
        params: dict[str, Any] = {"nodeId": node_id, "enable": enable}
        if invoker_node_id is not None:
            params["invokerNodeId"] = invoker_node_id
        return await self._call("DOM.forceShowPopover", params)
