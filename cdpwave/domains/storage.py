"""Storage domain: cookies, IndexedDB, cache storage, and storage quotas."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class StorageDomain(BaseDomain):
    """Wrapper for the CDP Storage domain.

    Provides access to browser storage: cookies per origin, IndexedDB,
    cache storage, and storage quota tracking.

    For DOMStorage (localStorage/sessionStorage), use
    ``DOMStorageDomain`` via ``session.dom_storage``.
    """

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

    async def get_storage_key(self, frame_id: str) -> dict[str, Any]:
        """Get the storage key for a frame.

        Args:
            frame_id: Frame ID to get the storage key for.

        Returns:
            Dict with ``storageKey``.
        """
        return await self._call(
            "Storage.getStorageKey",
            {"frameId": frame_id},
        )

    async def clear_data_for_storage_key(
        self,
        storage_key: str,
        storage_types: str,
    ) -> dict[str, Any]:
        """Clear storage data for a storage key.

        Args:
            storage_key: Storage key to clear data for.
            storage_types: Comma-separated storage types (e.g.
                ``"cookies,local_storage,session_storage,indexeddb"``,
                or ``"all"``).
        """
        return await self._call(
            "Storage.clearDataForStorageKey",
            {"storageKey": storage_key, "storageTypes": storage_types},
        )

    async def override_quota_for_origin(
        self,
        origin: str,
        quota_size: int | None = None,
    ) -> dict[str, Any]:
        """Override storage quota for an origin.

        Args:
            origin: Security origin to override quota for.
            quota_size: Quota size in bytes. If None, removes the override.
        """
        params: dict[str, Any] = {"origin": origin}
        if quota_size is not None:
            params["quotaSize"] = quota_size
        return await self._call("Storage.overrideQuotaForOrigin", params)

    async def track_indexed_db_for_storage_key(self, storage_key: str) -> dict[str, Any]:
        """Start tracking IndexedDB for a storage key.

        Args:
            storage_key: Storage key to track.
        """
        return await self._call(
            "Storage.trackIndexedDBForStorageKey",
            {"storageKey": storage_key},
        )

    async def untrack_indexed_db_for_storage_key(self, storage_key: str) -> dict[str, Any]:
        """Stop tracking IndexedDB for a storage key.

        Args:
            storage_key: Storage key to stop tracking.
        """
        return await self._call(
            "Storage.untrackIndexedDBForStorageKey",
            {"storageKey": storage_key},
        )

    async def track_cache_storage_for_storage_key(self, storage_key: str) -> dict[str, Any]:
        """Start tracking Cache Storage for a storage key.

        Args:
            storage_key: Storage key to track.
        """
        return await self._call(
            "Storage.trackCacheStorageForStorageKey",
            {"storageKey": storage_key},
        )

    async def untrack_cache_storage_for_storage_key(self, storage_key: str) -> dict[str, Any]:
        """Stop tracking Cache Storage for a storage key.

        Args:
            storage_key: Storage key to stop tracking.
        """
        return await self._call(
            "Storage.untrackCacheStorageForStorageKey",
            {"storageKey": storage_key},
        )

    async def get_interest_group_details(
        self,
        owner_origin: str,
        name: str,
    ) -> dict[str, Any]:
        """Get details for an interest group.

        Args:
            owner_origin: Owner origin of the interest group.
            name: Name of the interest group.

        Returns:
            Dict with ``details`` containing interest group info.
        """
        return await self._call(
            "Storage.getInterestGroupDetails",
            {"ownerOrigin": owner_origin, "name": name},
        )

    async def set_interest_group_tracking(self, enable: bool) -> dict[str, Any]:
        """Enable or disable interest group tracking.

        Args:
            enable: Whether to track interest groups.
        """
        return await self._call(
            "Storage.setInterestGroupTracking",
            {"enable": enable},
        )

    async def set_interest_group_auction_tracking(self, enable: bool) -> dict[str, Any]:
        """Enable or disable interest group auction tracking.

        Args:
            enable: Whether to track interest group auctions.
        """
        return await self._call(
            "Storage.setInterestGroupAuctionTracking",
            {"enable": enable},
        )

    async def get_shared_storage_metadata(
        self,
        owner_origin: str,
    ) -> dict[str, Any]:
        """Get metadata for a shared storage.

        Args:
            owner_origin: Owner origin of the shared storage.

        Returns:
            Dict with ``metadata`` containing ``creationTime`` and ``length``.
        """
        return await self._call(
            "Storage.getSharedStorageMetadata",
            {"ownerOrigin": owner_origin},
        )

    async def get_shared_storage_entries(
        self,
        owner_origin: str,
    ) -> dict[str, Any]:
        """Get entries from a shared storage.

        Args:
            owner_origin: Owner origin of the shared storage.

        Returns:
            Dict with ``entries`` list of ``{key, value}`` dicts.
        """
        return await self._call(
            "Storage.getSharedStorageEntries",
            {"ownerOrigin": owner_origin},
        )

    async def set_shared_storage_entry(
        self,
        owner_origin: str,
        key: str,
        value: str,
        ignore_if_present: bool = False,
    ) -> dict[str, Any]:
        """Set an entry in a shared storage.

        Args:
            owner_origin: Owner origin of the shared storage.
            key: Entry key.
            value: Entry value.
            ignore_if_present: If True, do not overwrite existing entries.
        """
        return await self._call(
            "Storage.setSharedStorageEntry",
            {
                "ownerOrigin": owner_origin,
                "key": key,
                "value": value,
                "ignoreIfPresent": ignore_if_present,
            },
        )

    async def delete_shared_storage_entry(
        self,
        owner_origin: str,
        key: str,
    ) -> dict[str, Any]:
        """Delete an entry from a shared storage.

        Args:
            owner_origin: Owner origin of the shared storage.
            key: Entry key to delete.
        """
        return await self._call(
            "Storage.deleteSharedStorageEntry",
            {"ownerOrigin": owner_origin, "key": key},
        )

    async def clear_shared_storage_entries(self, owner_origin: str) -> dict[str, Any]:
        """Clear all entries in a shared storage.

        Args:
            owner_origin: Owner origin of the shared storage.
        """
        return await self._call(
            "Storage.clearSharedStorageEntries",
            {"ownerOrigin": owner_origin},
        )

    async def reset_shared_storage_budget(
        self,
        owner_origin: str,
        budget: float | None = None,
    ) -> dict[str, Any]:
        """Reset the shared storage budget for an origin.

        Args:
            owner_origin: Owner origin of the shared storage.
            budget: Optional budget to set. If None, resets to default.
        """
        params: dict[str, Any] = {"ownerOrigin": owner_origin}
        if budget is not None:
            params["budget"] = budget
        return await self._call("Storage.resetSharedStorageBudget", params)

    async def set_shared_storage_tracking(self, enable: bool) -> dict[str, Any]:
        """Enable or disable shared storage tracking.

        Args:
            enable: Whether to track shared storage operations.
        """
        return await self._call(
            "Storage.setSharedStorageTracking",
            {"enable": enable},
        )

    async def set_storage_bucket_tracking(
        self,
        storage_key: str,
        enable: bool,
    ) -> dict[str, Any]:
        """Enable or disable storage bucket tracking.

        Args:
            storage_key: Storage key to track.
            enable: Whether to track storage bucket updates.
        """
        return await self._call(
            "Storage.setStorageBucketTracking",
            {"storageKey": storage_key, "enable": enable},
        )

    async def delete_storage_bucket(
        self,
        storage_key: str,
        bucket_name: str,
    ) -> dict[str, Any]:
        """Delete a storage bucket.

        Args:
            storage_key: Storage key of the bucket.
            bucket_name: Name of the bucket to delete.
        """
        return await self._call(
            "Storage.deleteStorageBucket",
            {"storageKey": storage_key, "bucketName": bucket_name},
        )

    async def run_bounce_tracking_mitigations(self) -> dict[str, Any]:
        """Run bounce tracking mitigations.

        Removes trackers that have been identified as bounce trackers.
        """
        return await self._call("Storage.runBounceTrackingMitigations")

    async def get_related_website_sets(self) -> dict[str, Any]:
        """Get related website sets.

        Returns:
            Dict with ``sets`` list of related website set dicts.
        """
        return await self._call("Storage.getRelatedWebsiteSets")

    async def set_protected_audience_k_anonymity(
        self,
        owner_origin: str,
        name: str,
        k_anonymity: bool,
    ) -> dict[str, Any]:
        """Set k-anonymity for a protected audience interest group.

        Args:
            owner_origin: Owner origin of the interest group.
            name: Name of the interest group.
            k_anonymity: Whether k-anonymity is satisfied.
        """
        return await self._call(
            "Storage.setProtectedAudienceKAnonymity",
            {
                "ownerOrigin": owner_origin,
                "name": name,
                "kAnonymity": k_anonymity,
            },
        )
