"""IndexedDB domain: inspect and manipulate IndexedDB databases."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class IndexedDBDomain(BaseDomain):
    """Wrapper for the CDP IndexedDB domain.

    Provides inspection and manipulation of IndexedDB databases,
    including listing databases, object stores, and records,
    as well as deleting databases and clearing object stores.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the IndexedDB domain."""
        return await self._call("IndexedDB.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the IndexedDB domain."""
        return await self._call("IndexedDB.disable")

    async def request_database_names(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Request database names for a security origin or storage key.

        Args:
            security_origin: Security origin to query.
            storage_key: Storage key to query.
            storage_bucket: Optional storage bucket info.

        Returns:
            Dict with ``databaseNames`` list.
        """
        params: dict[str, Any] = {}
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestDatabaseNames", params)

    async def request_database(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Request database structure with object stores.

        Args:
            security_origin: Security origin to query.
            storage_key: Storage key to query.
            database_name: Name of the database to inspect.
            storage_bucket: Optional storage bucket info.

        Returns:
            Dict with ``databaseWithObjectStores`` list.
        """
        params: dict[str, Any] = {"databaseName": database_name}
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestDatabase", params)

    async def request_data(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        object_store_name: str = "",
        index_name: str | None = None,
        skip_count: int = 0,
        page_size: int = 10,
        key_range: dict[str, Any] | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Request data from an object store or index.

        Args:
            security_origin: Security origin to query.
            storage_key: Storage key to query.
            database_name: Database name.
            object_store_name: Object store name.
            index_name: Optional index to query (instead of store).
            skip_count: Number of records to skip.
            page_size: Maximum records to return.
            key_range: Optional key range filter.
            storage_bucket: Optional storage bucket info.

        Returns:
            Dict with ``objectStoreDataEntries`` and ``hasMore``.
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
            "skipCount": skip_count,
            "pageSize": page_size,
        }
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if index_name is not None:
            params["indexName"] = index_name
        if key_range is not None:
            params["keyRange"] = key_range
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestData", params)

    async def delete_database(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Delete an IndexedDB database.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Name of the database to delete.
            storage_bucket: Optional storage bucket info.
        """
        params: dict[str, Any] = {"databaseName": database_name}
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.deleteDatabase", params)

    async def clear_object_store(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        object_store_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Clear all records from an object store.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Database name.
            object_store_name: Object store to clear.
            storage_bucket: Optional storage bucket info.
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
        }
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.clearObjectStore", params)
