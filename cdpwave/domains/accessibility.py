"""Accessibility domain: access to the accessibility tree.

Provides commands, types, and events for the Accessibility domain.

Events:
    Accessibility.loadComplete: Mirrors the load complete event sent by the
        browser to assistive technology when the web page has finished
        loading. Params: ``root`` (AXNode) — new document root node.
    Accessibility.nodesUpdated: Sent every time a previously requested node
        has changed in the tree. Params: ``nodes`` (list[AXNode]) — updated
        node data.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AccessibilityDomain(BaseDomain):
    """Wrapper for the CDP Accessibility domain.

    Provides access to the accessibility tree for inspecting
    semantic structure, roles, names, and states of DOM elements.

    Events:
        ``Accessibility.loadComplete`` — mirrors the load complete event
            sent by the browser to assistive technology when the web page
            has finished loading. Params: ``root`` (AXNode).
        ``Accessibility.nodesUpdated`` — sent every time a previously
            requested node has changed in the tree. Params: ``nodes``
            (list[AXNode]).
    """

    async def disable(self) -> dict[str, Any]:
        """Disables the accessibility domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Accessibility.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables the accessibility domain which causes AXNodeIds to remain
        consistent between method calls. This turns on accessibility for the
        page, which can impact performance until accessibility is disabled.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Accessibility.enable")

    async def get_partial_ax_tree(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        fetch_relatives: bool = True,
    ) -> dict[str, Any]:
        """Fetches the accessibility node and partial accessibility tree for
        this DOM node, if it exists.

        Args:
            node_id: Identifier of the node to get the partial accessibility
                tree for.
            backend_node_id: Identifier of the backend node to get the
                partial accessibility tree for.
            object_id: JavaScript object id of the node wrapper to get the
                partial accessibility tree for.
            fetch_relatives: Whether to fetch this node's ancestors, siblings
                and children. Defaults to true.

        Returns:
            Dict with ``nodes`` — the AXNode for this DOM node, if it
            exists, plus its ancestors, siblings and children, if requested.
        """
        params: dict[str, Any] = {"fetchRelatives": fetch_relatives}
        if node_id:
            params["nodeId"] = node_id
        if backend_node_id:
            params["backendNodeId"] = backend_node_id
        if object_id:
            params["objectId"] = object_id
        return await self._call("Accessibility.getPartialAXTree", params)

    async def get_full_ax_tree(
        self,
        depth: int | None = None,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Fetches the entire accessibility tree for the root Document.

        Args:
            depth: The maximum depth at which descendants of the root node
                should be retrieved. If omitted, the full tree is returned.
            frame_id: The frame for whose document the AX tree should be
                retrieved. If omitted, the root frame is used.

        Returns:
            Dict with ``nodes`` list of AX node objects.
        """
        params: dict[str, Any] = {}
        if depth:
            params["depth"] = depth
        if frame_id:
            params["frameId"] = frame_id
        return await self._call("Accessibility.getFullAXTree", params)

    async def get_root_ax_node(
        self,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Fetches the root node. Requires ``enable()`` to have been called
        previously.

        Args:
            frame_id: The frame in whose document the node resides. If
                omitted, the root frame is used.

        Returns:
            Dict with the root ``node`` object.
        """
        params: dict[str, Any] = {}
        if frame_id:
            params["frameId"] = frame_id
        return await self._call("Accessibility.getRootAXNode", params)

    async def get_ax_node_and_ancestors(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
    ) -> dict[str, Any]:
        """Fetches a node and all ancestors up to and including the root.
        Requires ``enable()`` to have been called previously.

        Args:
            node_id: Identifier of the node to get.
            backend_node_id: Identifier of the backend node to get.
            object_id: JavaScript object id of the node wrapper to get.

        Returns:
            Dict with ``nodes`` list of AX node objects from the node
            up to the root.
        """
        params: dict[str, Any] = {}
        if node_id:
            params["nodeId"] = node_id
        if backend_node_id:
            params["backendNodeId"] = backend_node_id
        if object_id:
            params["objectId"] = object_id
        return await self._call(
            "Accessibility.getAXNodeAndAncestors", params
        )

    async def get_child_ax_nodes(
        self,
        node_id: str,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Fetches a particular accessibility node by AXNodeId.
        Requires ``enable()`` to have been called previously.

        Args:
            node_id: AX node ID (string) to get children for.
            frame_id: The frame in whose document the node resides.
                If omitted, the root frame is used.

        Returns:
            Dict with ``nodes`` list of child AX node objects.
        """
        params: dict[str, Any] = {"id": node_id}
        if frame_id:
            params["frameId"] = frame_id
        return await self._call("Accessibility.getChildAXNodes", params)

    async def query_ax_tree(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        accessible_name: str | None = None,
        role: str | None = None,
    ) -> dict[str, Any]:
        """Query a DOM node's accessibility subtree for accessible name and
        role. This command computes the name and role for all nodes in the
        subtree, including those that are ignored for accessibility, and
        returns those that match the specified name and role. If no DOM node
        is specified, or the DOM node does not exist, the command returns an
        error. If neither accessibleName or role is specified, it returns all
        the accessibility nodes in the subtree.

        Args:
            node_id: Identifier of the node for the root to query.
            backend_node_id: Identifier of the backend node for the root to
                query.
            object_id: JavaScript object id of the node wrapper for the root
                to query.
            accessible_name: Find nodes with this computed name.
            role: Find nodes with this computed role.

        Returns:
            Dict with ``nodes`` — a list of AXNode matching the specified
            attributes, including nodes that are ignored for accessibility.
        """
        params: dict[str, Any] = {}
        if node_id:
            params["nodeId"] = node_id
        if backend_node_id:
            params["backendNodeId"] = backend_node_id
        if object_id:
            params["objectId"] = object_id
        if accessible_name:
            params["accessibleName"] = accessible_name
        if role:
            params["role"] = role
        return await self._call("Accessibility.queryAXTree", params)
