"""Edge-case tests for the CacheStorage domain — validation branches only.

Targets every TypeError raise in CacheStorageDomain to push
coverage from 75% to >=90%.
"""

import pytest

from cdpwave.domains.cache_storage import CacheStorageDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestCacheStorageEdgeValidation:
    async def test_delete_cache_cache_id_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cache_id must be a string"):
            await d.delete_cache(123)  # type: ignore[arg-type]

    async def test_delete_entry_cache_id_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cache_id must be a string"):
            await d.delete_entry(123, "request")  # type: ignore[arg-type]

    async def test_delete_entry_request_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request must be a string"):
            await d.delete_entry("cache", 123)  # type: ignore[arg-type]

    async def test_request_cache_names_security_origin_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.request_cache_names(security_origin=123)  # type: ignore[arg-type]

    async def test_request_cache_names_storage_key_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.request_cache_names(storage_key=123)  # type: ignore[arg-type]

    async def test_request_cache_names_storage_bucket_not_dict(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.request_cache_names(storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_request_cached_response_cache_id_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cache_id must be a string"):
            await d.request_cached_response(123, "url", [])  # type: ignore[arg-type]

    async def test_request_cached_response_request_url_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_url must be a string"):
            await d.request_cached_response("cache", 123, [])  # type: ignore[arg-type]

    async def test_request_cached_response_request_headers_not_list(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_headers must be a list"):
            await d.request_cached_response("cache", "url", "not-a-list")  # type: ignore[arg-type]

    async def test_request_entries_cache_id_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cache_id must be a string"):
            await d.request_entries(123)  # type: ignore[arg-type]

    async def test_request_entries_skip_count_not_int(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="skip_count must be an int or None"):
            await d.request_entries("cache", skip_count="x")  # type: ignore[arg-type]

    async def test_request_entries_skip_count_bool(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="skip_count must be an int or None"):
            await d.request_entries("cache", skip_count=True)  # type: ignore[arg-type]

    async def test_request_entries_page_size_not_int(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="page_size must be an int or None"):
            await d.request_entries("cache", page_size="x")  # type: ignore[arg-type]

    async def test_request_entries_page_size_bool(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="page_size must be an int or None"):
            await d.request_entries("cache", page_size=True)  # type: ignore[arg-type]

    async def test_request_entries_path_filter_not_str(self) -> None:
        d = CacheStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="path_filter must be a str or None"):
            await d.request_entries("cache", path_filter=123)  # type: ignore[arg-type]
