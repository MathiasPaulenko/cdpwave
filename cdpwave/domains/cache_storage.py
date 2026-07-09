"""CacheStorage domain: inspect and manipulate Cache API caches."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CacheStorageDomain(BaseDomain):
    """Wrapper for the CDP CacheStorage domain.

    Provides inspection and manipulation of Cache API caches
    (Service Worker Cache Storage), including listing caches,
    retrieving entries, and deleting caches or individual entries.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable CacheStorage domain."""
        return await self._call("CacheStorage.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable CacheStorage domain."""
        return await self._call("CacheStorage.disable")

    async def delete_cache(
        self,
        cache_id: str,
    ) -> dict[str, Any]:
        """Delete a cache.

        Args:
            cache_id: ID of the cache to delete.
        """
        return await self._call(
            "CacheStorage.deleteCache",
            {"cacheId": cache_id},
        )

    async def delete_entry(
        self,
        cache_id: str,
        request: str,
    ) -> dict[str, Any]:
        """Delete a specific entry from a cache.

        Args:
            cache_id: ID of the cache containing the entry.
            request: URL of the request to delete.
        """
        return await self._call(
            "CacheStorage.deleteEntry",
            {"cacheId": cache_id, "request": request},
        )

    async def request_cache_names(
        self,
        security_origin: str | None = None,
        storage_key: str | None = None,
        storage_bucket: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """List all caches for a security origin or storage key.

        Args:
            security_origin: Security origin to query.
            storage_key: Storage key to query.
            storage_bucket: Optional storage bucket info.

        Returns:
            Dict with ``caches`` list.
        """
        params: dict[str, Any] = {}
        if security_origin is not None:
            params["securityOrigin"] = security_origin
        if storage_key is not None:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("CacheStorage.requestCacheNames", params)

    async def request_entries(
        self,
        cache_id: str,
        skip_count: int = 0,
        page_size: int = 100,
        path_filter: str | None = None,
    ) -> dict[str, Any]:
        """Request entries from a cache.

        Args:
            cache_id: ID of the cache to query.
            skip_count: Number of entries to skip.
            page_size: Maximum entries to return.
            path_filter: Optional path filter string.

        Returns:
            Dict with ``cacheDataEntries`` and ``returnCount``.
        """
        params: dict[str, Any] = {
            "cacheId": cache_id,
            "skipCount": skip_count,
            "pageSize": page_size,
        }
        if path_filter is not None:
            params["pathFilter"] = path_filter
        return await self._call("CacheStorage.requestEntries", params)
