"""DOMStorage domain: localStorage and sessionStorage inspection."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMStorageDomain(BaseDomain):
    """Wrapper for the CDP DOMStorage domain.

    Provides access to Web Storage (localStorage and sessionStorage)
    per security origin. The DOMStorage domain does not require
    ``enable``/``disable`` calls — commands work directly.
    """

    async def get_dom_storage_items(
        self,
        storage_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Get DOM storage items.

        Args:
            storage_id: Dict with ``securityOrigin`` and ``isLocalStorage``.

        Returns:
            Dict with ``entries`` list of ``[key, value]`` pairs.
        """
        return await self._call(
            "DOMStorage.getDOMStorageItems",
            {"storageId": storage_id},
        )

    async def set_dom_storage_item(
        self,
        storage_id: dict[str, Any],
        key: str,
        value: str,
    ) -> dict[str, Any]:
        """Set a DOM storage item.

        Args:
            storage_id: Dict with ``securityOrigin`` and ``isLocalStorage``.
            key: Item key.
            value: Item value.
        """
        return await self._call(
            "DOMStorage.setDOMStorageItem",
            {"storageId": storage_id, "key": key, "value": value},
        )

    async def remove_dom_storage_item(
        self,
        storage_id: dict[str, Any],
        key: str,
    ) -> dict[str, Any]:
        """Remove a DOM storage item.

        Args:
            storage_id: Dict with ``securityOrigin`` and ``isLocalStorage``.
            key: Item key to remove.
        """
        return await self._call(
            "DOMStorage.removeDOMStorageItem",
            {"storageId": storage_id, "key": key},
        )

    async def clear_dom_storage_items(
        self,
        storage_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Clear all DOM storage items.

        Args:
            storage_id: Dict with ``securityOrigin`` and ``isLocalStorage``.
        """
        return await self._call(
            "DOMStorage.clear",
            {"storageId": storage_id},
        )
