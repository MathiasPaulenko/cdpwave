"""Unit tests for the CacheStorage domain.

Covers all 5 CDP CacheStorage commands (deleteCache, deleteEntry,
requestCacheNames, requestCachedResponse, requestEntries) with FakeSender —
parameter verification, omitempty behavior, return values, CommandError
propagation, method parity, coroutine checks, and edge cases.
"""

import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.cache_storage import CacheStorageDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message
        self._calls: list[tuple[str, dict[str, Any] | None]] = []

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._calls.append((method, params))
        raise CommandError(self._code, self._message)

    @property
    def calls(self) -> list[tuple[str, dict[str, Any] | None]]:
        return self._calls

    @property
    def last_call(self) -> tuple[str, dict[str, Any] | None]:
        return self._calls[-1]


@pytest.mark.unit
class TestDeleteCache:
    async def test_delete_cache_params(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_cache("cache-123")
        assert fake.last_call == ("CacheStorage.deleteCache", {"cacheId": "cache-123"})

    async def test_delete_cache_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        result = await domain.delete_cache("c1")
        assert result == {}

    async def test_delete_cache_returns_response(self) -> None:
        fake = FakeSender({"deleted": True})
        domain = CacheStorageDomain(fake)
        result = await domain.delete_cache("c1")
        assert result == {"deleted": True}

    async def test_delete_cache_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_cache("c1")
        method, _ = fake.last_call
        assert method == "CacheStorage.deleteCache"

    async def test_delete_cache_single_call(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_cache("c1")
        assert len(fake.calls) == 1

    async def test_delete_cache_called_three_times(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        for _ in range(3):
            await domain.delete_cache("c1")
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call == ("CacheStorage.deleteCache", {"cacheId": "c1"})


@pytest.mark.unit
class TestDeleteEntry:
    async def test_delete_entry_params(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_entry("cache-1", "https://example.com/data")
        assert fake.last_call == (
            "CacheStorage.deleteEntry",
            {"cacheId": "cache-1", "request": "https://example.com/data"},
        )

    async def test_delete_entry_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        result = await domain.delete_entry("c1", "https://example.com")
        assert result == {}

    async def test_delete_entry_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = CacheStorageDomain(fake)
        result = await domain.delete_entry("c1", "https://example.com")
        assert result == {"ok": True}

    async def test_delete_entry_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_entry("c1", "https://example.com")
        method, _ = fake.last_call
        assert method == "CacheStorage.deleteEntry"

    async def test_delete_entry_empty_request_url(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_entry("c1", "")
        assert fake.last_call == (
            "CacheStorage.deleteEntry",
            {"cacheId": "c1", "request": ""},
        )


@pytest.mark.unit
class TestRequestCacheNames:
    async def test_with_security_origin(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        method, params = fake.last_call
        assert method == "CacheStorage.requestCacheNames"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_with_storage_key(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(storage_key="sk1")
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert "securityOrigin" not in params

    async def test_with_storage_bucket(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_cache_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_with_all_params(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_cache_names(
            security_origin="https://example.com",
            storage_key="sk1",
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_no_params_sends_empty_dict(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names()
        _, params = fake.last_call
        assert params == {}

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="")
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(storage_key="")
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_caches_list(self) -> None:
        fake = FakeSender({"caches": [{"cacheId": "c1", "cacheName": "v1"}]})
        domain = CacheStorageDomain(fake)
        result = await domain.request_cache_names(security_origin="https://example.com")
        assert "caches" in result
        assert isinstance(result["caches"], list)

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        method, _ = fake.last_call
        assert method == "CacheStorage.requestCacheNames"


@pytest.mark.unit
class TestRequestCachedResponse:
    async def test_params(self) -> None:
        fake = FakeSender({"body": "response body"})
        domain = CacheStorageDomain(fake)
        headers = [{"name": "Content-Type", "value": "text/html"}]
        await domain.request_cached_response("c1", "https://example.com", headers)
        assert fake.last_call == (
            "CacheStorage.requestCachedResponse",
            {
                "cacheId": "c1",
                "requestURL": "https://example.com",
                "requestHeaders": headers,
            },
        )

    async def test_returns_body(self) -> None:
        fake = FakeSender({"body": "cached content"})
        domain = CacheStorageDomain(fake)
        result = await domain.request_cached_response("c1", "https://example.com", [])
        assert result == {"body": "cached content"}

    async def test_empty_headers(self) -> None:
        fake = FakeSender({"body": ""})
        domain = CacheStorageDomain(fake)
        await domain.request_cached_response("c1", "https://example.com", [])
        _, params = fake.last_call
        assert params is not None
        assert params["requestHeaders"] == []

    async def test_multiple_headers(self) -> None:
        fake = FakeSender({"body": ""})
        domain = CacheStorageDomain(fake)
        headers = [
            {"name": "Content-Type", "value": "text/html"},
            {"name": "Cache-Control", "value": "max-age=3600"},
            {"name": "ETag", "value": "abc123"},
        ]
        await domain.request_cached_response("c1", "https://example.com", headers)
        _, params = fake.last_call
        assert params is not None
        assert len(params["requestHeaders"]) == 3

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"body": ""})
        domain = CacheStorageDomain(fake)
        await domain.request_cached_response("c1", "https://example.com", [])
        method, _ = fake.last_call
        assert method == "CacheStorage.requestCachedResponse"


@pytest.mark.unit
class TestRequestEntries:
    async def test_only_cache_id(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1")
        _, params = fake.last_call
        assert params == {"cacheId": "c1"}

    async def test_with_skip_count(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", skip_count=10)
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 10
        assert "pageSize" not in params

    async def test_with_page_size(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", page_size=50)
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == 50
        assert "skipCount" not in params

    async def test_with_path_filter(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", path_filter="/api/")
        _, params = fake.last_call
        assert params is not None
        assert params["pathFilter"] == "/api/"

    async def test_with_all_params(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", skip_count=5, page_size=50, path_filter="/api")
        _, params = fake.last_call
        assert params is not None
        assert params["cacheId"] == "c1"
        assert params["skipCount"] == 5
        assert params["pageSize"] == 50
        assert params["pathFilter"] == "/api"

    async def test_skip_count_zero_is_sent(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", skip_count=0)
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 0

    async def test_page_size_zero_is_sent(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", page_size=0)
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == 0

    async def test_omitempty_skip_count_none(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", skip_count=None)
        _, params = fake.last_call
        assert params is not None
        assert "skipCount" not in params

    async def test_omitempty_page_size_none(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", page_size=None)
        _, params = fake.last_call
        assert params is not None
        assert "pageSize" not in params

    async def test_omitempty_empty_path_filter(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1", path_filter="")
        _, params = fake.last_call
        assert params is not None
        assert "pathFilter" not in params

    async def test_returns_entries(self) -> None:
        fake = FakeSender({"cacheDataEntries": [{"url": "https://example.com"}], "returnCount": 1})
        domain = CacheStorageDomain(fake)
        result = await domain.request_entries("c1")
        assert "cacheDataEntries" in result
        assert "returnCount" in result

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("c1")
        method, _ = fake.last_call
        assert method == "CacheStorage.requestEntries"


@pytest.mark.unit
class TestCacheStorageMethodParity:
    async def test_all_five_methods_exist(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        assert hasattr(domain, "delete_cache")
        assert hasattr(domain, "delete_entry")
        assert hasattr(domain, "request_cache_names")
        assert hasattr(domain, "request_cached_response")
        assert hasattr(domain, "request_entries")

    async def test_no_extra_methods(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        public_methods = {
            m for m in dir(domain) if not m.startswith("_")
        }
        expected = {
            "delete_cache", "delete_entry",
            "request_cache_names", "request_cached_response",
            "request_entries",
        }
        assert public_methods == expected

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        for method_name in (
            "delete_cache", "delete_entry",
            "request_cache_names", "request_cached_response",
            "request_entries",
        ):
            method = getattr(domain, method_name)
            assert inspect.iscoroutinefunction(method)

    async def test_is_basedomain(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_method_order_alphabetical(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        methods = [m for m in dir(domain) if not m.startswith("_")]
        idx_delete_cache = methods.index("delete_cache")
        idx_delete_entry = methods.index("delete_entry")
        idx_req_cache_names = methods.index("request_cache_names")
        idx_req_cached_response = methods.index("request_cached_response")
        idx_req_entries = methods.index("request_entries")
        assert idx_delete_cache < idx_delete_entry
        assert idx_delete_entry < idx_req_cache_names
        assert idx_req_cache_names < idx_req_cached_response
        assert idx_req_cached_response < idx_req_entries


@pytest.mark.unit
class TestCacheStorageCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        fake.set_response({"cacheDataEntries": [], "returnCount": 0})
        await domain.request_entries("c1")
        fake.set_response({})
        await domain.delete_entry("c1", "https://example.com/data")
        await domain.delete_cache("c1")
        assert len(fake.calls) == 4
        assert fake.calls[0][0] == "CacheStorage.requestCacheNames"
        assert fake.calls[1][0] == "CacheStorage.requestEntries"
        assert fake.calls[2][0] == "CacheStorage.deleteEntry"
        assert fake.calls[3][0] == "CacheStorage.deleteCache"

    async def test_repeated_delete_cache(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        for _ in range(5):
            await domain.delete_cache("c1")
        assert len(fake.calls) == 5
        for call in fake.calls:
            assert call == ("CacheStorage.deleteCache", {"cacheId": "c1"})

    async def test_interleaved_calls(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        fake.set_response({"cacheDataEntries": [], "returnCount": 0})
        await domain.request_entries("c1")
        fake.set_response({})
        await domain.delete_entry("c1", "https://example.com")
        await domain.request_entries("c1")
        await domain.delete_cache("c1")
        assert len(fake.calls) == 5

    async def test_all_methods_use_cachestorage_prefix(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        fake.set_response({"cacheDataEntries": [], "returnCount": 0})
        await domain.request_entries("c1")
        fake.set_response({"body": ""})
        await domain.request_cached_response("c1", "https://example.com", [])
        fake.set_response({})
        await domain.delete_entry("c1", "https://example.com")
        await domain.delete_cache("c1")
        assert all(call[0].startswith("CacheStorage.") for call in fake.calls)


@pytest.mark.unit
class TestCacheStorageErrorPropagation:
    async def test_delete_cache_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Cache not found")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.delete_cache("nonexistent")
        assert exc_info.value.code == -32000
        assert "Cache not found" in exc_info.value.message
        assert len(sender.calls) == 1

    async def test_delete_entry_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32602, message="Invalid params")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.delete_entry("c1", "https://example.com")
        assert exc_info.value.code == -32602

    async def test_request_cache_names_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Security origin required")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_cache_names()
        assert exc_info.value.code == -32001

    async def test_request_cached_response_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Response not found")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_cached_response("c1", "https://example.com", [])
        assert exc_info.value.code == -32000

    async def test_request_entries_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Cache not found")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_entries("nonexistent")
        assert exc_info.value.code == -32000

    async def test_error_stops_execution(self) -> None:
        sender = ErrorSender(code=-32000, message="Failed")
        domain = CacheStorageDomain(sender)
        with pytest.raises(CommandError):
            await domain.delete_cache("c1")
        with pytest.raises(CommandError):
            await domain.delete_entry("c1", "https://example.com")
        assert len(sender.calls) == 2


@pytest.mark.unit
class TestCacheStorageEdgeCases:
    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        r1 = await domain.request_cache_names(security_origin="https://example.com")
        assert "caches" in r1
        fake.set_response({"caches": [{"cacheId": "c1"}]})
        r2 = await domain.request_cache_names(security_origin="https://example.com")
        assert r2["caches"] == [{"cacheId": "c1"}]

    async def test_large_response_dict(self) -> None:
        large = {f"key_{i}": f"value_{i}" for i in range(100)}
        fake = FakeSender(large)
        domain = CacheStorageDomain(fake)
        result = await domain.delete_cache("c1")
        assert result == large
        assert len(result) == 100

    async def test_method_signatures(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        sig_delete_cache = inspect.signature(domain.delete_cache)
        assert "cache_id" in sig_delete_cache.parameters
        assert sig_delete_cache.parameters["cache_id"].default is inspect.Parameter.empty

        sig_request_entries = inspect.signature(domain.request_entries)
        assert sig_request_entries.parameters["skip_count"].default is None
        assert sig_request_entries.parameters["page_size"].default is None
        assert sig_request_entries.parameters["path_filter"].default is None

        sig_request_cache_names = inspect.signature(domain.request_cache_names)
        assert sig_request_cache_names.parameters["security_origin"].default is None
        assert sig_request_cache_names.parameters["storage_key"].default is None
        assert sig_request_cache_names.parameters["storage_bucket"].default is None

    async def test_concurrent_calls_isolated(self) -> None:
        import asyncio
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await asyncio.gather(
            domain.delete_cache("c1"),
            domain.delete_entry("c1", "https://example.com"),
            domain.request_entries("c1"),
        )
        assert len(fake.calls) == 3
        methods = {call[0] for call in fake.calls}
        assert methods == {
            "CacheStorage.deleteCache",
            "CacheStorage.deleteEntry",
            "CacheStorage.requestEntries",
        }

    async def test_request_cached_response_empty_url(self) -> None:
        fake = FakeSender({"body": ""})
        domain = CacheStorageDomain(fake)
        await domain.request_cached_response("c1", "", [])
        _, params = fake.last_call
        assert params is not None
        assert params["requestURL"] == ""

    async def test_request_entries_empty_cache_id(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("")
        _, params = fake.last_call
        assert params == {"cacheId": ""}

    async def test_mixed_error_and_success(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        assert len(fake.calls) == 1
        error_sender = ErrorSender(code=-32000, message="Fail")
        domain_err = CacheStorageDomain(error_sender)
        with pytest.raises(CommandError):
            await domain_err.delete_cache("c1")
        assert len(error_sender.calls) == 1
