"""Storage domain: cookies, IndexedDB, cache storage, and storage quotas."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class StorageDomain(BaseDomain):
    """Wrapper for the CDP Storage domain.

    Provides access to browser storage: cookies per origin, IndexedDB,
    cache storage, and storage quota tracking.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable Storage domain."""
        return await self._call("DOMStorage.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Storage domain."""
        return await self._call("DOMStorage.disable")

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

    async def get_cookies(
        self,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Get all cookies for the browser context.

        Args:
            browser_context_id: Optional browser context ID.

        Returns:
            Dict with ``cookies`` list of cookie objects.
        """
        params: dict[str, Any] = {}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Storage.getCookies", params)

    async def set_cookies(
        self,
        cookies: list[dict[str, Any]],
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Set cookies for the browser context.

        Args:
            cookies: List of cookie dicts with ``name``, ``value``,
                ``domain``, ``path``, etc.
            browser_context_id: Optional browser context ID.
        """
        params: dict[str, Any] = {"cookies": cookies}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Storage.setCookies", params)

    async def clear_cookies(
        self,
        browser_context_id: str | None = None,
    ) -> dict[str, Any]:
        """Clear all cookies for the browser context.

        Args:
            browser_context_id: Optional browser context ID.
        """
        params: dict[str, Any] = {}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        return await self._call("Storage.clearCookies", params)

    async def get_usage_and_quota(
        self,
        origin: str,
    ) -> dict[str, Any]:
        """Get storage usage and quota for an origin.

        Args:
            origin: Security origin (e.g. ``"https://example.com"``).

        Returns:
            Dict with ``usage``, ``quota``, and ``overrideActive``.
        """
        return await self._call(
            "Storage.getUsageAndQuota",
            {"origin": origin},
        )

    async def clear_data_for_origin(
        self,
        origin: str,
        storage_types: str,
    ) -> dict[str, Any]:
        """Clear storage data for an origin.

        Args:
            origin: Security origin.
            storage_types: Comma-separated storage types (e.g.
                ``"cookies,local_storage,session_storage,indexeddb"``,
                or ``"all"``).
        """
        return await self._call(
            "Storage.clearDataForOrigin",
            {"origin": origin, "storageTypes": storage_types},
        )

    async def get_trust_tokens(self) -> dict[str, Any]:
        """Get all trust tokens stored.

        Returns:
            Dict with ``tokens`` list.
        """
        return await self._call("Storage.getTrustTokens")

    async def clear_trust_tokens(
        self,
        issuer_origin: str | None = None,
    ) -> dict[str, Any]:
        """Clear trust tokens for an issuer.

        Args:
            issuer_origin: Optional issuer origin. If omitted, clears all.
        """
        params: dict[str, Any] = {}
        if issuer_origin is not None:
            params["issuerOrigin"] = issuer_origin
        return await self._call("Storage.clearTrustTokens", params)

    async def set_storage_bucket_info(
        self,
        bucket: dict[str, Any],
    ) -> dict[str, Any]:
        """Set storage bucket info (quota, expiration, etc.).

        Args:
            bucket: Bucket info dict with ``storageKey``, ``name``,
                and ``quota``.
        """
        return await self._call(
            "Storage.setStorageBucketInfo",
            {"bucket": bucket},
        )

    async def track_indexed_db_for_origin(self, origin: str) -> dict[str, Any]:
        """Start tracking IndexedDB storage for an origin.

        Emits ``Storage.indexedDBListUpdated`` events when the database
        list changes.

        Args:
            origin: Origin to track.
        """
        return await self._call(
            "Storage.trackIndexedDBForOrigin",
            {"origin": origin},
        )

    async def untrack_indexed_db_for_origin(self, origin: str) -> dict[str, Any]:
        """Stop tracking IndexedDB storage for an origin.

        Args:
            origin: Origin to stop tracking.
        """
        return await self._call(
            "Storage.untrackIndexedDBForOrigin",
            {"origin": origin},
        )

    async def track_cache_storage_for_origin(self, origin: str) -> dict[str, Any]:
        """Start tracking Cache Storage for an origin.

        Emits ``Storage.cacheStorageListUpdated`` events when the cache
        list changes.

        Args:
            origin: Origin to track.
        """
        return await self._call(
            "Storage.trackCacheStorageForOrigin",
            {"origin": origin},
        )

    async def untrack_cache_storage_for_origin(self, origin: str) -> dict[str, Any]:
        """Stop tracking Cache Storage for an origin.

        Args:
            origin: Origin to stop tracking.
        """
        return await self._call(
            "Storage.untrackCacheStorageForOrigin",
            {"origin": origin},
        )

    async def get_storage_key_for_frame(self, frame_id: str) -> dict[str, Any]:
        """Get the storage key for a frame.

        Args:
            frame_id: Frame ID to get the storage key for.

        Returns:
            Dict with ``storageKey``.
        """
        return await self._call(
            "Storage.getStorageKeyForFrame",
            {"frameId": frame_id},
        )
