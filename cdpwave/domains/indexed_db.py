"""IndexedDB domain: inspect and manipulate IndexedDB databases.

Provides access to IndexedDB databases for inspection and manipulation,
including listing databases, object stores, and records, as well as
deleting databases and clearing object stores.

The IndexedDB domain has no events in the CDP spec.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class IndexedDBDomain(BaseDomain):
    """Wrapper for the CDP IndexedDB domain.

    Provides access to IndexedDB databases for inspection and manipulation.
    The IndexedDB domain has no events in the CDP spec.
    """

    async def clear_object_store(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        object_store_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Clears all entries from an object store.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Database name.
            object_store_name: Object store name.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
        }
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.clearObjectStore", params)

    async def delete_database(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Deletes a database.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Database name.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {"databaseName": database_name}
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.deleteDatabase", params)

    async def delete_object_store_entries(
        self,
        database_name: str,
        object_store_name: str,
        key_range: dict[str, Any],
        security_origin: str | None = None,
        storage_key: str | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Delete a range of entries from an object store.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            database_name: Database name.
            object_store_name: Object store name.
            key_range: Range of entry keys to delete.
            security_origin: Security origin.
            storage_key: Storage key.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
            "keyRange": key_range,
        }
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.deleteObjectStoreEntries", params)

    async def disable(self) -> dict[str, Any]:
        """Disables events from backend.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("IndexedDB.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables events from backend.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("IndexedDB.enable")

    async def get_metadata(
        self,
        database_name: str,
        object_store_name: str,
        security_origin: str | None = None,
        storage_key: str | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Gets metadata of an object store.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            database_name: Database name.
            object_store_name: Object store name.
            security_origin: Security origin.
            storage_key: Storage key.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Dict with ``entriesCount`` (the entries count) and
            ``keyGeneratorValue`` (the current value of key generator,
            to become the next inserted key into the object store.
            Valid if objectStore.autoIncrement is true).
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
        }
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.getMetadata", params)

    async def request_data(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        object_store_name: str = "",
        index_name: str = "",
        skip_count: int = 0,
        page_size: int = 10,
        key_range: dict[str, Any] | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Requests data from object store or index.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Database name.
            object_store_name: Object store name.
            index_name: Index name, empty string for object store data
                requests.
            skip_count: Number of records to skip.
            page_size: Number of records to fetch.
            key_range: Key range.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Dict with ``objectStoreDataEntries`` (array of object store
            data entries) and ``hasMore`` (if true, there are more
            entries to fetch in the given range).
        """
        params: dict[str, Any] = {
            "databaseName": database_name,
            "objectStoreName": object_store_name,
            "indexName": index_name,
            "skipCount": skip_count,
            "pageSize": page_size,
        }
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if key_range is not None:
            params["keyRange"] = key_range
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestData", params)

    async def request_database(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        database_name: str = "",
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Requests database with given name in given frame.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            database_name: Database name.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Dict with ``databaseWithObjectStores`` (database with an
            array of object stores).
        """
        params: dict[str, Any] = {"databaseName": database_name}
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestDatabase", params)

    async def request_database_names(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Requests database names for given security origin.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Dict with ``databaseNames`` (database names for origin).
        """
        params: dict[str, Any] = {}
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("IndexedDB.requestDatabaseNames", params)
