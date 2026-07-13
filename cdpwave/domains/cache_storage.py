"""CacheStorage domain: inspect and manipulate Cache API caches.

Provides inspection and manipulation of Cache API caches
(Service Worker Cache Storage), including listing caches,
retrieving entries, deleting caches or individual entries,
and retrieving cached responses.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CacheStorageDomain(BaseDomain):
    """Wrapper for the CDP CacheStorage domain.

    Provides inspection and manipulation of Cache API caches
    (Service Worker Cache Storage), including listing caches,
    retrieving entries, and deleting caches or individual entries.
    """

    async def delete_cache(
        self,
        cache_id: str,
    ) -> dict[str, Any]:
        """Deletes a cache.

        Args:
            cache_id: ID of the cache to delete.

        Returns:
            Response dict from the CDP.
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
        """Deletes a cache entry.

        Args:
            cache_id: ID of the cache where the entry will be deleted.
            request: URL spec of the request.

        Returns:
            Response dict from the CDP.
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
        """Requests cache names.

        At least and at most one of security_origin, storage_key, or
        storage_bucket must be specified.

        Args:
            security_origin: Security origin.
            storage_key: Storage key.
            storage_bucket: Storage bucket. If not specified, uses the
                default bucket.

        Returns:
            Dict with ``caches`` list.
        """
        params: dict[str, Any] = {}
        if security_origin:
            params["securityOrigin"] = security_origin
        if storage_key:
            params["storageKey"] = storage_key
        if storage_bucket is not None:
            params["storageBucket"] = storage_bucket
        return await self._call("CacheStorage.requestCacheNames", params)

    async def request_cached_response(
        self,
        cache_id: str,
        request_url: str,
        request_headers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Fetches cache entry.

        Args:
            cache_id: ID of the cache that contains the entry.
            request_url: URL spec of the request.
            request_headers: Headers of the request.

        Returns:
            Dict with ``response`` containing ``body`` (base64-encoded str).
        """
        return await self._call(
            "CacheStorage.requestCachedResponse",
            {
                "cacheId": cache_id,
                "requestURL": request_url,
                "requestHeaders": request_headers,
            },
        )

    async def request_entries(
        self,
        cache_id: str,
        skip_count: int | None = None,
        page_size: int | None = None,
        path_filter: str | None = None,
    ) -> dict[str, Any]:
        """Requests data from cache.

        Args:
            cache_id: ID of cache to get entries from.
            skip_count: Number of records to skip.
            page_size: Number of records to fetch.
            path_filter: If present, only return the entries containing
                this substring in the path.

        Returns:
            Dict with ``cacheDataEntries`` and ``returnCount``.
        """
        params: dict[str, Any] = {"cacheId": cache_id}
        if skip_count is not None:
            params["skipCount"] = skip_count
        if page_size is not None:
            params["pageSize"] = page_size
        if path_filter:
            params["pathFilter"] = path_filter
        return await self._call("CacheStorage.requestEntries", params)
