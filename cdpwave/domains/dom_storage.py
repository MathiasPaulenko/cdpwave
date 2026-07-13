"""DOMStorage domain: localStorage and sessionStorage access."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DOMStorageDomain(BaseDomain):
    """Wrapper for the CDP DOMStorage domain.

    Provides access to Web Storage (localStorage and sessionStorage)
    per security origin.

    Events:
        - ``DOMStorage.domStorageItemAdded`` — fired when item added.
          Params: ``storageId`` (StorageId), ``key`` (str), ``newValue`` (str).
        - ``DOMStorage.domStorageItemRemoved`` — fired when item removed.
          Params: ``storageId`` (StorageId), ``key`` (str).
        - ``DOMStorage.domStorageItemsCleared`` — fired when all items cleared.
          Params: ``storageId`` (StorageId).
        - ``DOMStorage.domStorageItemUpdated`` — fired when item value updated.
          Params: ``storageId`` (StorageId), ``key`` (str),
          ``oldValue`` (str), ``newValue`` (str).

    Call ``enable`` to receive storage events; ``disable`` to stop them.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable storage tracking, storage events will now be delivered to the client."""
        return await self._call("DOMStorage.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable storage tracking, prevents storage events from being sent to the client."""
        return await self._call("DOMStorage.disable")

    async def get_dom_storage_items(
        self,
        storage_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Get DOM storage items.

        Args:
            storage_id: Dict with ``securityOrigin`` (str, optional),
                ``storageKey`` (str, optional), and ``isLocalStorage``
                (bool, always sent).

        Returns:
            Dict with ``entries`` key: list of ``[key, value]`` pairs
            (each pair is a ``list[str]`` of length 2).
        """
        if not isinstance(storage_id, dict):
            raise TypeError("storage_id must be a dict")
        if "isLocalStorage" not in storage_id:
            raise ValueError("storage_id must contain 'isLocalStorage'")
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
            storage_id: Dict with ``securityOrigin`` (str, optional),
                ``storageKey`` (str, optional), and ``isLocalStorage``
                (bool, always sent).
            key: Item key.
            value: Item value.
        """
        if not isinstance(storage_id, dict):
            raise TypeError("storage_id must be a dict")
        if "isLocalStorage" not in storage_id:
            raise ValueError("storage_id must contain 'isLocalStorage'")
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(value, str):
            raise TypeError("value must be a string")
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
            storage_id: Dict with ``securityOrigin`` (str, optional),
                ``storageKey`` (str, optional), and ``isLocalStorage``
                (bool, always sent).
            key: Item key to remove.
        """
        if not isinstance(storage_id, dict):
            raise TypeError("storage_id must be a dict")
        if "isLocalStorage" not in storage_id:
            raise ValueError("storage_id must contain 'isLocalStorage'")
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        return await self._call(
            "DOMStorage.removeDOMStorageItem",
            {"storageId": storage_id, "key": key},
        )

    async def clear(
        self,
        storage_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Clear all DOM storage items for the given storage.

        Args:
            storage_id: Dict with ``securityOrigin`` (str, optional),
                ``storageKey`` (str, optional), and ``isLocalStorage``
                (bool, always sent).
        """
        if not isinstance(storage_id, dict):
            raise TypeError("storage_id must be a dict")
        if "isLocalStorage" not in storage_id:
            raise ValueError("storage_id must contain 'isLocalStorage'")
        return await self._call(
            "DOMStorage.clear",
            {"storageId": storage_id},
        )

    async def clear_dom_storage_items(
        self,
        storage_id: dict[str, Any],
    ) -> dict[str, Any]:
        """Alias for :meth:`clear`."""
        return await self.clear(storage_id)
