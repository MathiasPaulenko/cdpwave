from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMDomain(BaseDomain):
    async def enable(self) -> dict[str, Any]:
        return await self._call("DOM.enable")

    async def disable(self) -> dict[str, Any]:
        return await self._call("DOM.disable")

    async def get_document(
        self,
        depth: int = -1,
        pierce: bool = False,
    ) -> dict[str, Any]:
        return await self._call(
            "DOM.getDocument",
            {"depth": depth, "pierce": pierce},
        )

    async def get_outer_html(self, node_id: int) -> dict[str, Any]:
        return await self._call(
            "DOM.getOuterHTML",
            {"nodeId": node_id},
        )

    async def get_inner_html(self, node_id: int) -> dict[str, Any]:
        return await self._call(
            "DOM.getInnerHTML",
            {"nodeId": node_id},
        )

    async def query_selector(
        self,
        node_id: int,
        selector: str,
    ) -> dict[str, Any]:
        return await self._call(
            "DOM.querySelector",
            {"nodeId": node_id, "selector": selector},
        )

    async def query_selector_all(
        self,
        node_id: int,
        selector: str,
    ) -> dict[str, Any]:
        return await self._call(
            "DOM.querySelectorAll",
            {"nodeId": node_id, "selector": selector},
        )

    async def remove_node(self, node_id: int) -> dict[str, Any]:
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
        return await self._call(
            "DOM.setAttributeValue",
            {"nodeId": node_id, "name": name, "value": value},
        )

    async def get_attribute(
        self,
        node_id: int,
        name: str,
    ) -> dict[str, Any]:
        return await self._call(
            "DOM.getAttributes",
            {"nodeId": node_id},
        )

    async def focus(self, node_id: int) -> dict[str, Any]:
        return await self._call(
            "DOM.focus",
            {"nodeId": node_id},
        )

    async def scroll_into_view_if_needed(self, node_id: int) -> dict[str, Any]:
        return await self._call(
            "DOM.scrollIntoViewIfNeeded",
            {"nodeId": node_id},
        )
