"""Extensions domain: load unpacked extensions and manage extension storage."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ExtensionsDomain(BaseDomain):
    """Wrapper for the CDP Extensions domain.

    Provides loading of unpacked extensions and management of
    extension storage items for testing extension behavior.
    """

    async def load_unpacked(
        self,
        path: str,
        allow_file_access: bool | None = None,
    ) -> dict[str, Any]:
        """Load an unpacked extension from a directory path.

        Args:
            path: Absolute path to the extension directory.
            allow_file_access: Whether to allow file access.

        Returns:
            Dict with ``id`` of the loaded extension.
        """
        params: dict[str, Any] = {"path": path}
        if allow_file_access is not None:
            params["allowFileAccess"] = allow_file_access
        return await self._call("Extensions.loadUnpacked", params)

    async def get_storage_items(
        self,
        id: str,
        storage_type: str = "local",
    ) -> dict[str, Any]:
        """Get extension storage items.

        Args:
            id: Extension ID.
            storage_type: Storage type (``"local"``, ``"session"``,
                ``"sync"``, ``"managed"``).

        Returns:
            Dict with ``items`` mapping.
        """
        return await self._call(
            "Extensions.getStorageItems",
            {"id": id, "storageType": storage_type},
        )

    async def remove_storage_items(
        self,
        id: str,
        storage_type: str = "local",
        keys: list[str] | None = None,
    ) -> dict[str, Any]:
        """Remove items from extension storage.

        Args:
            id: Extension ID.
            storage_type: Storage type.
            keys: List of keys to remove.
        """
        params: dict[str, Any] = {"id": id, "storageType": storage_type}
        if keys is not None:
            params["keys"] = keys
        return await self._call("Extensions.removeStorageItems", params)

    async def clear_storage_items(
        self,
        id: str,
        storage_type: str = "local",
    ) -> dict[str, Any]:
        """Clear all items from extension storage.

        Args:
            id: Extension ID.
            storage_type: Storage type.
        """
        return await self._call(
            "Extensions.clearStorageItems",
            {"id": id, "storageType": storage_type},
        )
