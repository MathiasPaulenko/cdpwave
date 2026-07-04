"""Accessibility domain: AX tree inspection for accessibility testing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AccessibilityDomain(BaseDomain):
    """Wrapper for the CDP Accessibility domain.

    Provides access to the accessibility tree for inspecting
    semantic structure, roles, names, and states of DOM elements.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Accessibility domain.

        Activates Accessibility domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Accessibility.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Accessibility domain.

        Deactivates Accessibility domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Accessibility.disable")

    async def get_partial_ax_tree(
        self,
        node_id: int | None = None,
        backend_node_id: int | None = None,
        object_id: str | None = None,
        fetch_relatives: bool = True,
    ) -> dict[str, Any]:
        """Get a partial accessibility tree for a node.

        Args:
            node_id: DOM node ID to query from.
            backend_node_id: Backend DOM node ID.
            object_id: Remote object ID.
            fetch_relatives: Whether to fetch relatives of the node.

        Returns:
            Dict with ``nodes`` list of AX node objects.
        """
        params: dict[str, Any] = {"fetchRelatives": fetch_relatives}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        return await self._call("Accessibility.getPartialAXTree", params)

    async def get_full_ax_tree(self) -> dict[str, Any]:
        """Get the full accessibility tree for the current page.

        Returns:
            Dict with ``nodes`` list of AX node objects.
        """
        return await self._call("Accessibility.getFullAXTree")

    async def get_root_ax_node(
        self,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the root AX node of the accessibility tree.

        Args:
            frame_id: Optional frame ID to get the root for.

        Returns:
            Dict with the root ``node`` object.
        """
        params: dict[str, Any] = {}
        if frame_id is not None:
            params["frameId"] = frame_id
        return await self._call("Accessibility.getRootAXNode", params)

    async def get_child_ax_nodes(
        self,
        node_id: str,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Get child AX nodes of a given node.

        Args:
            node_id: AX node ID to get children for.
            frame_id: Optional frame ID.

        Returns:
            Dict with ``nodes`` list of child AX node objects.
        """
        params: dict[str, Any] = {"id": node_id}
        if frame_id is not None:
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
        """Query the AX tree for nodes matching a query.

        Args:
            node_id: DOM node ID to query from.
            backend_node_id: Backend DOM node ID.
            object_id: Remote object ID.
            accessible_name: Filter by accessible name.
            role: Filter by AX role (e.g. ``"button"``, ``"link"``).

        Returns:
            Dict with ``nodes`` list of matching AX nodes.
        """
        params: dict[str, Any] = {}
        if node_id is not None:
            params["nodeId"] = node_id
        if backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        if object_id is not None:
            params["objectId"] = object_id
        if accessible_name is not None:
            params["accessibleName"] = accessible_name
        if role is not None:
            params["role"] = role
        return await self._call("Accessibility.queryAXTree", params)
