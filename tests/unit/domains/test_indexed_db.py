"""Unit tests for the IndexedDB domain.

Covers all 9 CDP IndexedDB commands (clearObjectStore, deleteDatabase,
deleteObjectStoreEntries, disable, enable, getMetadata, requestData,
requestDatabase, requestDatabaseNames) with FakeSender —
parameter verification, omitempty behavior, return values, CommandError
propagation, method parity, coroutine checks, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
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


# ---------------------------------------------------------------------------
# clear_object_store
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestClearObjectStore:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.clearObjectStore"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            storage_key="sk1",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"
        assert "securityOrigin" not in params

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.clear_object_store(
            storage_bucket=bucket,
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_params_all_origin_key_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.clear_object_store(
            security_origin="https://example.com",
            storage_key="sk1",
            database_name="db1",
            object_store_name="store1",
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            storage_key="",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        result = await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = IndexedDBDomain(fake)
        result = await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.clearObjectStore"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert len(fake.calls) == 1


# ---------------------------------------------------------------------------
# delete_database
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDeleteDatabase:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteDatabase"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["databaseName"] == "db1"
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            storage_key="sk1",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.delete_database(
            storage_bucket=bucket,
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            storage_key="",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        result = await domain.delete_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"deleted": True})
        domain = IndexedDBDomain(fake)
        result = await domain.delete_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        assert result == {"deleted": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.deleteDatabase"


# ---------------------------------------------------------------------------
# delete_object_store_entries
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDeleteObjectStoreEntries:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        key_range = {"lower": 0, "upper": 100}
        await domain.delete_object_store_entries(
            database_name="db1",
            object_store_name="store1",
            key_range=key_range,
            security_origin="https://example.com",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteObjectStoreEntries"
        assert params is not None
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert params["keyRange"] == key_range
        assert params["securityOrigin"] == "https://example.com"

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        key_range = {"lower": 0, "upper": 100}
        await domain.delete_object_store_entries(
            "db1", "store1", key_range,
            storage_key="sk1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        key_range = {"lower": 0, "upper": 100}
        await domain.delete_object_store_entries(
            "db1", "store1", key_range,
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_key_range_omitted_when_all_none(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        key_range = {"lower": None, "upper": None}
        await domain.delete_object_store_entries(
            "db1", "store1", key_range,
            security_origin="https://example.com",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == {"lowerOpen": False, "upperOpen": False}

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0},
            security_origin="",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0},
            storage_key="",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        result = await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0},
            security_origin="https://example.com",
        )
        assert result == {}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0},
            security_origin="https://example.com",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.deleteObjectStoreEntries"


# ---------------------------------------------------------------------------
# disable / enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        assert fake.last_call == ("IndexedDB.disable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = IndexedDBDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "IndexedDB.disable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1


@pytest.mark.unit
class TestEnable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        assert fake.last_call == ("IndexedDB.enable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = IndexedDBDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "IndexedDB.enable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1


# ---------------------------------------------------------------------------
# get_metadata
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetMetadata:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({"entriesCount": 5, "keyGeneratorValue": 10})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            database_name="db1",
            object_store_name="store1",
            security_origin="https://example.com",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.getMetadata"
        assert params is not None
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert params["securityOrigin"] == "https://example.com"

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({"entriesCount": 5, "keyGeneratorValue": 10})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            "db1", "store1",
            storage_key="sk1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({"entriesCount": 5, "keyGeneratorValue": 10})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.get_metadata(
            "db1", "store1",
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            "db1", "store1",
            security_origin="",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            "db1", "store1",
            storage_key="",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_entries_count_and_key_generator_value(self) -> None:
        fake = FakeSender({"entriesCount": 42, "keyGeneratorValue": 7.5})
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "store1",
            security_origin="https://example.com",
        )
        assert result["entriesCount"] == 42
        assert result["keyGeneratorValue"] == 7.5

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            "db1", "store1",
            security_origin="https://example.com",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.getMetadata"


# ---------------------------------------------------------------------------
# request_data
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRequestData:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestData"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            storage_key="sk1",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_data(
            storage_bucket=bucket,
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_index_name_always_sent_default_empty(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "indexName" not in params

    async def test_index_name_with_value(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            index_name="idx1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["indexName"] == "idx1"

    async def test_skip_count_always_sent_default_zero(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "skipCount" in params
        assert params["skipCount"] == 0

    async def test_page_size_always_sent_default_ten(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "pageSize" in params
        assert params["pageSize"] == 10

    async def test_skip_count_with_value(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            skip_count=50,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 50

    async def test_page_size_with_value(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            page_size=100,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == 100

    async def test_key_range_omitted_when_none(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "keyRange" not in params

    async def test_key_range_sent_when_provided(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        key_range = {"lower": 0, "upper": 100}
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            key_range=key_range,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == key_range

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            storage_key="",
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_all_params(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        key_range = {"lower": 0, "upper": 100}
        await domain.request_data(
            security_origin="https://example.com",
            storage_key="sk1",
            database_name="db1",
            object_store_name="store1",
            index_name="idx1",
            skip_count=5,
            page_size=50,
            key_range=key_range,
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert params["indexName"] == "idx1"
        assert params["skipCount"] == 5
        assert params["pageSize"] == 50
        assert params["keyRange"] == key_range
        assert params["storageBucket"] == bucket

    async def test_returns_entries_and_has_more(self) -> None:
        fake = FakeSender({
            "objectStoreDataEntries": [{"key": "k1"}],
            "hasMore": True,
        })
        domain = IndexedDBDomain(fake)
        result = await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert "objectStoreDataEntries" in result
        assert "hasMore" in result
        assert result["hasMore"] is True

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.requestData"


# ---------------------------------------------------------------------------
# request_database
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRequestDatabase:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabase"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["databaseName"] == "db1"
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            storage_key="sk1",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_database(
            storage_bucket=bucket,
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            storage_key="",
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_database_with_object_stores(self) -> None:
        fake = FakeSender({
            "databaseWithObjectStores": {
                "name": "db1",
                "version": 1,
                "objectStores": [],
            },
        })
        domain = IndexedDBDomain(fake)
        result = await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        assert "databaseWithObjectStores" in result

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        method, _ = fake.last_call
        assert method == "IndexedDB.requestDatabase"


# ---------------------------------------------------------------------------
# request_database_names
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRequestDatabaseNames:
    async def test_params_with_security_origin(self) -> None:
        fake = FakeSender({"databaseNames": ["db1", "db2"]})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabaseNames"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_params_with_storage_key(self) -> None:
        fake = FakeSender({"databaseNames": ["db1"]})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(storage_key="sk1")
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "sk1"

    async def test_params_with_storage_bucket(self) -> None:
        fake = FakeSender({"databaseNames": ["db1"]})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_database_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_no_params_sends_empty_dict(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names()
        _, params = fake.last_call
        assert params == {}

    async def test_omitempty_empty_security_origin(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="")
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params

    async def test_omitempty_empty_storage_key(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(storage_key="")
        _, params = fake.last_call
        assert params is not None
        assert "storageKey" not in params

    async def test_returns_database_names_list(self) -> None:
        fake = FakeSender({"databaseNames": ["db1", "db2", "db3"]})
        domain = IndexedDBDomain(fake)
        result = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert "databaseNames" in result
        assert isinstance(result["databaseNames"], list)
        assert len(result["databaseNames"]) == 3

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        method, _ = fake.last_call
        assert method == "IndexedDB.requestDatabaseNames"


# ---------------------------------------------------------------------------
# Method parity
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBMethodParity:
    async def test_all_nine_methods_exist(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        assert hasattr(domain, "clear_object_store")
        assert hasattr(domain, "delete_database")
        assert hasattr(domain, "delete_object_store_entries")
        assert hasattr(domain, "disable")
        assert hasattr(domain, "enable")
        assert hasattr(domain, "get_metadata")
        assert hasattr(domain, "request_data")
        assert hasattr(domain, "request_database")
        assert hasattr(domain, "request_database_names")

    async def test_no_extra_methods(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        public_methods = {
            m for m in dir(domain) if not m.startswith("_")
        }
        expected = {
            "clear_object_store",
            "delete_database",
            "delete_object_store_entries",
            "disable",
            "enable",
            "get_metadata",
            "request_data",
            "request_database",
            "request_database_names",
        }
        assert public_methods == expected

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for method_name in (
            "clear_object_store",
            "delete_database",
            "delete_object_store_entries",
            "disable",
            "enable",
            "get_metadata",
            "request_data",
            "request_database",
            "request_database_names",
        ):
            method = getattr(domain, method_name)
            assert inspect.iscoroutinefunction(method)

    async def test_is_basedomain(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_method_order_alphabetical(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        methods = [m for m in dir(domain) if not m.startswith("_")]
        idx_clear = methods.index("clear_object_store")
        idx_delete_db = methods.index("delete_database")
        idx_delete_entries = methods.index("delete_object_store_entries")
        idx_disable = methods.index("disable")
        idx_enable = methods.index("enable")
        idx_metadata = methods.index("get_metadata")
        idx_req_data = methods.index("request_data")
        idx_req_db = methods.index("request_database")
        idx_req_names = methods.index("request_database_names")
        assert idx_clear < idx_delete_db
        assert idx_delete_db < idx_delete_entries
        assert idx_delete_entries < idx_disable
        assert idx_disable < idx_enable
        assert idx_enable < idx_metadata
        assert idx_metadata < idx_req_data
        assert idx_req_data < idx_req_db
        assert idx_req_db < idx_req_names


# ---------------------------------------------------------------------------
# Call sequences
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({"databaseNames": ["db1"]})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        await domain.request_database_names(security_origin="https://example.com")
        fake.set_response({"databaseWithObjectStores": {}})
        await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        fake.set_response({"objectStoreDataEntries": [], "hasMore": False})
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        fake.set_response({"entriesCount": 5, "keyGeneratorValue": 10})
        await domain.get_metadata(
            "db1", "store1",
            security_origin="https://example.com",
        )
        fake.set_response({})
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        await domain.delete_object_store_entries(
            "db1", "store1", {"lower": 0},
            security_origin="https://example.com",
        )
        await domain.delete_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        await domain.disable()
        assert len(fake.calls) == 9
        assert fake.calls[0][0] == "IndexedDB.enable"
        assert fake.calls[1][0] == "IndexedDB.requestDatabaseNames"
        assert fake.calls[2][0] == "IndexedDB.requestDatabase"
        assert fake.calls[3][0] == "IndexedDB.requestData"
        assert fake.calls[4][0] == "IndexedDB.getMetadata"
        assert fake.calls[5][0] == "IndexedDB.clearObjectStore"
        assert fake.calls[6][0] == "IndexedDB.deleteObjectStoreEntries"
        assert fake.calls[7][0] == "IndexedDB.deleteDatabase"
        assert fake.calls[8][0] == "IndexedDB.disable"

    async def test_repeated_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for _ in range(3):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 6
        for i, call in enumerate(fake.calls):
            if i % 2 == 0:
                assert call[0] == "IndexedDB.enable"
            else:
                assert call[0] == "IndexedDB.disable"

    async def test_interleaved_calls(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        fake.set_response({"databaseWithObjectStores": {}})
        await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        fake.set_response({"databaseNames": []})
        await domain.request_database_names(security_origin="https://example.com")
        assert len(fake.calls) == 3

    async def test_all_methods_use_indexeddb_prefix(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        await domain.request_database_names(security_origin="https://example.com")
        fake.set_response({"databaseWithObjectStores": {}})
        await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        fake.set_response({"objectStoreDataEntries": [], "hasMore": False})
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        fake.set_response({})
        await domain.disable()
        assert all(call[0].startswith("IndexedDB.") for call in fake.calls)


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBErrorPropagation:
    async def test_clear_object_store_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Object store not found")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.clear_object_store(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="store1",
            )
        assert exc_info.value.code == -32000
        assert "Object store not found" in exc_info.value.message
        assert len(sender.calls) == 1

    async def test_delete_database_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32602, message="Invalid params")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.delete_database(
                security_origin="https://example.com",
                database_name="nonexistent",
            )
        assert exc_info.value.code == -32602

    async def test_delete_object_store_entries_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Database not found")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.delete_object_store_entries(
                "db1", "store1", {"lower": 0},
                security_origin="https://example.com",
            )
        assert exc_info.value.code == -32000

    async def test_disable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Already disabled")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -32001

    async def test_enable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Already enabled")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == -32001

    async def test_get_metadata_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Store not found")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.get_metadata(
                "db1", "store1",
                security_origin="https://example.com",
            )
        assert exc_info.value.code == -32000

    async def test_request_data_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Database not found")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_data(
                security_origin="https://example.com",
                database_name="nonexistent",
                object_store_name="store1",
            )
        assert exc_info.value.code == -32000

    async def test_request_database_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Database not found")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_database(
                security_origin="https://example.com",
                database_name="nonexistent",
            )
        assert exc_info.value.code == -32000

    async def test_request_database_names_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Security origin required")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_database_names()
        assert exc_info.value.code == -32001

    async def test_error_stops_execution(self) -> None:
        sender = ErrorSender(code=-32000, message="Failed")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 2


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBEdgeCases:
    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        r1 = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert r1["databaseNames"] == []
        fake.set_response({"databaseNames": ["db1", "db2"]})
        r2 = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert r2["databaseNames"] == ["db1", "db2"]

    async def test_large_response_dict(self) -> None:
        large = {f"key_{i}": f"value_{i}" for i in range(100)}
        fake = FakeSender(large)
        domain = IndexedDBDomain(fake)
        result = await domain.enable()
        assert result == large
        assert len(result) == 100

    async def test_method_signatures(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)

        sig_enable = inspect.signature(domain.enable)
        assert len(sig_enable.parameters) == 0

        sig_disable = inspect.signature(domain.disable)
        assert len(sig_disable.parameters) == 0

        sig_clear = inspect.signature(domain.clear_object_store)
        assert sig_clear.parameters["security_origin"].default is None
        assert sig_clear.parameters["storage_key"].default is None
        assert sig_clear.parameters["database_name"].default == ""
        assert sig_clear.parameters["object_store_name"].default == ""
        assert sig_clear.parameters["storage_bucket"].default is None

        sig_delete_entries = inspect.signature(domain.delete_object_store_entries)
        assert sig_delete_entries.parameters["database_name"].default is inspect.Parameter.empty
        assert sig_delete_entries.parameters["object_store_name"].default is inspect.Parameter.empty
        assert sig_delete_entries.parameters["key_range"].default is inspect.Parameter.empty
        assert sig_delete_entries.parameters["security_origin"].default is None

        sig_req_data = inspect.signature(domain.request_data)
        assert sig_req_data.parameters["index_name"].default == ""
        assert sig_req_data.parameters["skip_count"].default == 0
        assert sig_req_data.parameters["page_size"].default == 10
        assert sig_req_data.parameters["key_range"].default is None

        sig_get_metadata = inspect.signature(domain.get_metadata)
        assert sig_get_metadata.parameters["database_name"].default is inspect.Parameter.empty
        assert sig_get_metadata.parameters["object_store_name"].default is inspect.Parameter.empty

    async def test_concurrent_calls_isolated(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.request_database_names(security_origin="https://example.com"),
        )
        assert len(fake.calls) == 3
        methods = {call[0] for call in fake.calls}
        assert methods == {
            "IndexedDB.enable",
            "IndexedDB.disable",
            "IndexedDB.requestDatabaseNames",
        }

    async def test_mixed_error_and_success(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        assert len(fake.calls) == 1
        error_sender = ErrorSender(code=-32000, message="Fail")
        domain_err = IndexedDBDomain(error_sender)
        with pytest.raises(CommandError):
            await domain_err.delete_database(
                security_origin="https://example.com",
                database_name="db1",
            )
        assert len(error_sender.calls) == 1

    async def test_none_response_from_sender(self) -> None:
        fake = FakeSender()
        domain = IndexedDBDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_error_sender_records_call_before_raising(self) -> None:
        sender = ErrorSender(code=-32000, message="Error")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        assert len(sender.calls) == 1
        assert sender.calls[0][0] == "IndexedDB.enable"

    async def test_empty_database_name_sent(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="https://example.com",
            database_name="",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == ""

    async def test_empty_object_store_name_sent(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["objectStoreName"] == ""

    async def test_request_data_empty_strings_sent(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="",
            object_store_name="",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == ""
        assert params["objectStoreName"] == ""
        assert "indexName" not in params
        assert params["skipCount"] == 0
        assert params["pageSize"] == 10


# ---------------------------------------------------------------------------
# Additional edge cases — second review
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBEdgeCasesRound2:
    async def test_request_data_page_size_zero(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            page_size=0,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == 0

    async def test_request_data_skip_count_zero_explicit(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            skip_count=0,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 0

    async def test_request_data_negative_skip_count(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            skip_count=-1,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == -1

    async def test_request_data_negative_page_size(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            page_size=-1,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == -1

    async def test_request_data_large_skip_count(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            skip_count=999999,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 999999

    async def test_request_data_large_page_size(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            page_size=999999,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == 999999

    async def test_request_data_empty_key_range_dict(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            key_range={},
        )
        _, params = fake.last_call
        assert params is not None
        assert "keyRange" not in params

    async def test_request_data_complex_key_range(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        key_range = {
            "lower": 0,
            "upper": 100,
            "lowerOpen": True,
            "upperOpen": False,
        }
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            key_range=key_range,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == key_range

    async def test_storage_bucket_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            storage_bucket={},
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "storageBucket" in params
        assert params["storageBucket"] == {}

    async def test_storage_bucket_with_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": "custom-bucket"}
        await domain.delete_database(
            storage_bucket=bucket,
            database_name="db1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_clear_object_store_no_origin_key_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"

    async def test_delete_database_no_origin_key_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(database_name="db1")
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert params["databaseName"] == "db1"

    async def test_get_metadata_no_origin_key_bucket(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata("db1", "store1")
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params

    async def test_request_database_no_origin_key_bucket(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": {}})
        domain = IndexedDBDomain(fake)
        await domain.request_database(database_name="db1")
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert params["databaseName"] == "db1"

    async def test_request_data_no_origin_key_bucket(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            database_name="db1",
            object_store_name="store1",
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert "keyRange" not in params
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert "indexName" not in params
        assert params["skipCount"] == 0
        assert params["pageSize"] == 10

    async def test_delete_object_store_entries_no_origin_key_bucket(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries("db1", "store1", {"lower": 0})
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "store1"
        assert params["keyRange"] == {"lower": 0}

    async def test_clear_object_store_repeated_5x(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for _ in range(5):
            await domain.clear_object_store(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="store1",
            )
        assert len(fake.calls) == 5
        assert all(c[0] == "IndexedDB.clearObjectStore" for c in fake.calls)

    async def test_delete_database_repeated_5x(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for _ in range(5):
            await domain.delete_database(
                security_origin="https://example.com",
                database_name="db1",
            )
        assert len(fake.calls) == 5

    async def test_get_metadata_zero_values(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "store1",
            security_origin="https://example.com",
        )
        assert result["entriesCount"] == 0
        assert result["keyGeneratorValue"] == 0

    async def test_request_data_empty_entries_hasmore_false(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        result = await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert result["objectStoreDataEntries"] == []
        assert result["hasMore"] is False

    async def test_request_database_complex_nested(self) -> None:
        nested = {
            "databaseWithObjectStores": {
                "name": "db1",
                "version": 2,
                "objectStores": [
                    {
                        "name": "store1",
                        "keyPath": {"type": "string", "string": "id"},
                        "autoIncrement": False,
                        "indexes": [
                            {
                                "name": "idx1",
                                "keyPath": {"type": "string", "string": "name"},
                                "unique": False,
                                "multiEntry": False,
                            },
                        ],
                    },
                ],
            },
        }
        fake = FakeSender(nested)
        domain = IndexedDBDomain(fake)
        result = await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        db = result["databaseWithObjectStores"]
        assert db["name"] == "db1"
        assert db["version"] == 2
        assert len(db["objectStores"]) == 1
        assert db["objectStores"][0]["name"] == "store1"
        assert len(db["objectStores"][0]["indexes"]) == 1

    async def test_request_database_names_empty_list(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        result = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert result["databaseNames"] == []

    async def test_request_database_names_single_element(self) -> None:
        fake = FakeSender({"databaseNames": ["only-db"]})
        domain = IndexedDBDomain(fake)
        result = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert result["databaseNames"] == ["only-db"]

    async def test_delete_object_store_entries_empty_key_range(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            "db1", "store1", {},
            security_origin="https://example.com",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == {"lowerOpen": False, "upperOpen": False}

    async def test_all_methods_with_storage_key_only(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            storage_key="sk1", database_name="db1", object_store_name="s1",
        )
        await domain.delete_database(storage_key="sk1", database_name="db1")
        await domain.delete_object_store_entries(
            "db1", "s1", {"lower": 0}, storage_key="sk1",
        )
        fake.set_response({"entriesCount": 0, "keyGeneratorValue": 0})
        await domain.get_metadata("db1", "s1", storage_key="sk1")
        fake.set_response({"objectStoreDataEntries": [], "hasMore": False})
        await domain.request_data(
            storage_key="sk1", database_name="db1", object_store_name="s1",
        )
        fake.set_response({"databaseWithObjectStores": {}})
        await domain.request_database(storage_key="sk1", database_name="db1")
        fake.set_response({"databaseNames": []})
        await domain.request_database_names(storage_key="sk1")
        for _, params in fake.calls:
            assert params is not None
            assert params.get("storageKey") == "sk1"
            assert "securityOrigin" not in params

    async def test_all_methods_with_storage_bucket_only(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": "bucket1"}
        await domain.clear_object_store(
            storage_bucket=bucket, database_name="db1", object_store_name="s1",
        )
        await domain.delete_database(storage_bucket=bucket, database_name="db1")
        await domain.delete_object_store_entries(
            "db1", "s1", {"lower": 0}, storage_bucket=bucket,
        )
        fake.set_response({"entriesCount": 0, "keyGeneratorValue": 0})
        await domain.get_metadata("db1", "s1", storage_bucket=bucket)
        fake.set_response({"objectStoreDataEntries": [], "hasMore": False})
        await domain.request_data(
            storage_bucket=bucket, database_name="db1", object_store_name="s1",
        )
        fake.set_response({"databaseWithObjectStores": {}})
        await domain.request_database(storage_bucket=bucket, database_name="db1")
        fake.set_response({"databaseNames": []})
        await domain.request_database_names(storage_bucket=bucket)
        for _, params in fake.calls:
            assert params is not None
            assert params.get("storageBucket") == bucket
            assert "securityOrigin" not in params

    async def test_request_data_skip_and_page_combined(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": True})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
            skip_count=10,
            page_size=5,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == 10
        assert params["pageSize"] == 5

    async def test_concurrent_same_method(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await asyncio.gather(
            domain.request_database_names(security_origin="https://example.com"),
            domain.request_database_names(security_origin="https://example.com"),
            domain.request_database_names(security_origin="https://example.com"),
        )
        assert len(fake.calls) == 3
        assert all(c[0] == "IndexedDB.requestDatabaseNames" for c in fake.calls)

    async def test_concurrent_all_different_methods(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.clear_object_store(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="s1",
            ),
            domain.delete_database(
                security_origin="https://example.com",
                database_name="db1",
            ),
        )
        assert len(fake.calls) == 4

    async def test_error_code_preserved(self) -> None:
        sender = ErrorSender(code=-999, message="Custom error")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.request_database_names()
        assert exc_info.value.code == -999

    async def test_error_message_preserved(self) -> None:
        sender = ErrorSender(code=-1, message="Very specific error message")
        domain = IndexedDBDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert "Very specific error message" in exc_info.value.message

    async def test_request_data_returns_exact_response(self) -> None:
        response = {
            "objectStoreDataEntries": [
                {
                    "key": {"type": "number", "number": 1},
                    "value": {"type": "object", "object": {"name": "Alice"}},
                },
                {
                    "key": {"type": "number", "number": 2},
                    "value": {"type": "object", "object": {"name": "Bob"}},
                },
            ],
            "hasMore": False,
        }
        fake = FakeSender(response)
        domain = IndexedDBDomain(fake)
        result = await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="store1",
        )
        assert result == response
        assert len(result["objectStoreDataEntries"]) == 2

    async def test_get_metadata_float_key_generator(self) -> None:
        fake = FakeSender({"entriesCount": 100, "keyGeneratorValue": 5.5})
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "store1",
            security_origin="https://example.com",
        )
        assert result["entriesCount"] == 100
        assert result["keyGeneratorValue"] == 5.5

    async def test_params_not_mutated_between_calls(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
        )
        _, params1 = fake.last_call
        await domain.clear_object_store(
            security_origin="https://other.com",
            database_name="db2",
            object_store_name="s2",
        )
        _, params2 = fake.last_call
        assert params1 is not None
        assert params2 is not None
        assert params1["securityOrigin"] == "https://example.com"
        assert params1["databaseName"] == "db1"
        assert params2["securityOrigin"] == "https://other.com"
        assert params2["databaseName"] == "db2"

    async def test_request_database_names_no_params_is_dict_not_none(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names()
        _, params = fake.last_call
        assert params is not None
        assert isinstance(params, dict)
        assert params == {}

    async def test_disable_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "IndexedDB.disable"
        assert params is None

    async def test_enable_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "IndexedDB.enable"
        assert params is None


# ---------------------------------------------------------------------------
# Boundary / limit tests — third review
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIndexedDBBoundary:
    async def test_security_origin_whitespace_only_sent(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="   ")
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "   "

    async def test_storage_key_whitespace_only_sent(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(storage_key="   ")
        _, params = fake.last_call
        assert params is not None
        assert params["storageKey"] == "   "

    async def test_all_three_origin_key_bucket_set(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": "b1"}
        await domain.request_database_names(
            security_origin="https://example.com",
            storage_key="sk1",
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["storageKey"] == "sk1"
        assert params["storageBucket"] == bucket

    async def test_all_three_clear_object_store(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": "b1"}
        await domain.clear_object_store(
            security_origin="https://example.com",
            storage_key="sk1",
            database_name="db1",
            object_store_name="s1",
            storage_bucket=bucket,
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" in params
        assert "storageKey" in params
        assert "storageBucket" in params

    async def test_unicode_database_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="https://example.com",
            database_name="数据库-🔒-café",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == "数据库-🔒-café"

    async def test_unicode_object_store_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="オブジェクト店舗-🏷️",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["objectStoreName"] == "オブジェクト店舗-🏷️"

    async def test_special_chars_database_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        name = 'db";DROP TABLE--\n\t\\'
        await domain.delete_database(
            security_origin="https://example.com",
            database_name=name,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == name

    async def test_newline_in_database_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db\nwith\nnewlines",
            object_store_name="s1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == "db\nwith\nnewlines"

    async def test_very_long_database_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        long_name = "a" * 10000
        await domain.delete_database(
            security_origin="https://example.com",
            database_name=long_name,
        )
        _, params = fake.last_call
        assert params is not None
        assert len(params["databaseName"]) == 10000

    async def test_very_long_object_store_name(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        long_name = "x" * 10000
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name=long_name,
        )
        _, params = fake.last_call
        assert params is not None
        assert len(params["objectStoreName"]) == 10000

    async def test_skip_count_max_int(self) -> None:
        import sys

        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            skip_count=sys.maxsize,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["skipCount"] == sys.maxsize

    async def test_page_size_max_int(self) -> None:
        import sys

        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            page_size=sys.maxsize,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["pageSize"] == sys.maxsize

    async def test_page_size_true_bool(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        with pytest.raises(TypeError, match="page_size must be an int"):
            await domain.request_data(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="s1",
                page_size=True,
            )

    async def test_page_size_false_bool(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        with pytest.raises(TypeError, match="page_size must be an int"):
            await domain.request_data(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="s1",
                page_size=False,
            )

    async def test_skip_count_true_bool(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        with pytest.raises(TypeError, match="skip_count must be an int"):
            await domain.request_data(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="s1",
                skip_count=True,
            )

    async def test_key_range_nested_complex(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        key_range = {
            "lower": {"type": "number", "number": 42},
            "upper": {"type": "string", "string": "zzz"},
            "lowerOpen": True,
            "upperOpen": False,
        }
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=key_range,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == key_range

    async def test_key_range_deeply_nested(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        key_range = {
            "lower": {
                "type": "array",
                "array": [
                    {"type": "number", "number": 1},
                    {"type": "number", "number": 2},
                ],
            },
            "upper": None,
            "lowerOpen": False,
            "upperOpen": False,
        }
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=key_range,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == {
            "lower": key_range["lower"],
            "lowerOpen": False,
            "upperOpen": False,
        }

    async def test_storage_bucket_extra_keys(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": "b1", "extra": "ignored"}
        await domain.request_database_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == bucket

    async def test_100_concurrent_calls(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await asyncio.gather(
            *[
                domain.request_database_names(
                    security_origin="https://example.com",
                )
                for _ in range(100)
            ]
        )
        assert len(fake.calls) == 100
        assert all(c[0] == "IndexedDB.requestDatabaseNames" for c in fake.calls)

    async def test_100_concurrent_mixed_methods(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        tasks = []
        for _ in range(50):
            tasks.append(domain.enable())
            tasks.append(domain.disable())
        await asyncio.gather(*tasks)
        assert len(fake.calls) == 100

    async def test_explicit_none_all_optionals(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(
            security_origin=None,
            storage_key=None,
            storage_bucket=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert params == {}

    async def test_explicit_none_all_optionals_clear(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin=None,
            storage_key=None,
            database_name="db1",
            object_store_name="s1",
            storage_bucket=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert "securityOrigin" not in params
        assert "storageKey" not in params
        assert "storageBucket" not in params
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "s1"

    async def test_explicit_none_key_range(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert "keyRange" not in params

    async def test_all_keyword_args(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            storage_key=None,
            database_name="db1",
            object_store_name="s1",
            index_name="idx1",
            skip_count=5,
            page_size=20,
            key_range={"lower": 0},
            storage_bucket=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "s1"
        assert params["indexName"] == "idx1"
        assert params["skipCount"] == 5
        assert params["pageSize"] == 20
        assert params["keyRange"] == {"lower": 0}

    async def test_get_metadata_all_keyword(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        await domain.get_metadata(
            database_name="db1",
            object_store_name="s1",
            security_origin="https://example.com",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "s1"
        assert params["securityOrigin"] == "https://example.com"

    async def test_delete_object_store_entries_all_keyword(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_object_store_entries(
            database_name="db1",
            object_store_name="s1",
            key_range={"lower": None, "upper": None},
            security_origin="https://example.com",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["databaseName"] == "db1"
        assert params["objectStoreName"] == "s1"
        assert params["keyRange"] == {"lowerOpen": False, "upperOpen": False}
        assert params["securityOrigin"] == "https://example.com"

    async def test_security_origin_with_port(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(
            security_origin="https://example.com:8080",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "https://example.com:8080"

    async def test_security_origin_localhost(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(
            security_origin="http://localhost:3000",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "http://localhost:3000"

    async def test_security_origin_file_protocol(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(
            security_origin="file:///C:/path",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["securityOrigin"] == "file:///C:/path"

    async def test_index_name_with_special_chars(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            index_name="idx@#$%^&*()",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["indexName"] == "idx@#$%^&*()"

    async def test_index_name_unicode(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            index_name="索引-🔑",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["indexName"] == "索引-🔑"

    async def test_index_name_very_long(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        long_name = "i" * 10000
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            index_name=long_name,
        )
        _, params = fake.last_call
        assert params is not None
        assert len(params["indexName"]) == 10000

    async def test_key_range_with_only_lower(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        kr = {"lower": 5}
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=kr,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == kr

    async def test_key_range_with_only_upper(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        kr = {"upper": 10}
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=kr,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == kr

    async def test_key_range_with_only_lower_open(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        kr = {"lowerOpen": True}
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=kr,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["keyRange"] == kr

    async def test_storage_bucket_only_storage_key(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1"}
        await domain.request_database_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == {"storageKey": "sk1"}

    async def test_storage_bucket_only_name(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        bucket = {"name": "my-bucket"}
        await domain.request_database_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == {"name": "my-bucket"}

    async def test_storage_bucket_empty_name(self) -> None:
        fake = FakeSender({"databaseNames": []})
        domain = IndexedDBDomain(fake)
        bucket = {"storageKey": "sk1", "name": ""}
        await domain.request_database_names(storage_bucket=bucket)
        _, params = fake.last_call
        assert params is not None
        assert params["storageBucket"] == {"storageKey": "sk1", "name": ""}

    async def test_request_data_has_more_true(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": True})
        domain = IndexedDBDomain(fake)
        result = await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
        )
        assert result["hasMore"] is True

    async def test_get_metadata_negative_entries_count(self) -> None:
        fake = FakeSender({"entriesCount": -1, "keyGeneratorValue": 0})
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "s1",
            security_origin="https://example.com",
        )
        assert result["entriesCount"] == -1

    async def test_get_metadata_negative_key_generator(self) -> None:
        fake = FakeSender({"entriesCount": 0, "keyGeneratorValue": -1})
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "s1",
            security_origin="https://example.com",
        )
        assert result["keyGeneratorValue"] == -1

    async def test_get_metadata_large_values(self) -> None:
        import sys

        fake = FakeSender(
            {"entriesCount": sys.maxsize, "keyGeneratorValue": sys.maxsize},
        )
        domain = IndexedDBDomain(fake)
        result = await domain.get_metadata(
            "db1", "s1",
            security_origin="https://example.com",
        )
        assert result["entriesCount"] == sys.maxsize
        assert result["keyGeneratorValue"] == sys.maxsize

    async def test_request_database_names_many_databases(self) -> None:
        names = [f"db-{i}" for i in range(1000)]
        fake = FakeSender({"databaseNames": names})
        domain = IndexedDBDomain(fake)
        result = await domain.request_database_names(
            security_origin="https://example.com",
        )
        assert len(result["databaseNames"]) == 1000
        assert result["databaseNames"][0] == "db-0"
        assert result["databaseNames"][-1] == "db-999"

    async def test_request_data_many_entries(self) -> None:
        entries = [
            {
                "key": {"type": "number", "number": i},
                "value": {"type": "string", "string": f"val-{i}"},
            }
            for i in range(1000)
        ]
        fake = FakeSender({"objectStoreDataEntries": entries, "hasMore": False})
        domain = IndexedDBDomain(fake)
        result = await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
        )
        assert len(result["objectStoreDataEntries"]) == 1000

    async def test_request_database_many_object_stores(self) -> None:
        stores = [
            {
                "name": f"store-{i}",
                "keyPath": {"type": "string", "string": "id"},
                "autoIncrement": False,
                "indexes": [],
            }
            for i in range(100)
        ]
        fake = FakeSender(
            {"databaseWithObjectStores": {"name": "db1", "version": 1, "objectStores": stores}},
        )
        domain = IndexedDBDomain(fake)
        result = await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        assert len(result["databaseWithObjectStores"]["objectStores"]) == 100

    async def test_request_database_many_indexes(self) -> None:
        indexes = [
            {
                "name": f"idx-{i}",
                "keyPath": {"type": "string", "string": "field"},
                "unique": False,
                "multiEntry": False,
            }
            for i in range(100)
        ]
        fake = FakeSender(
            {
                "databaseWithObjectStores": {
                    "name": "db1",
                    "version": 1,
                    "objectStores": [
                        {
                            "name": "s1",
                            "keyPath": {"type": "string", "string": "id"},
                            "autoIncrement": False,
                            "indexes": indexes,
                        },
                    ],
                },
            },
        )
        domain = IndexedDBDomain(fake)
        result = await domain.request_database(
            security_origin="https://example.com",
            database_name="db1",
        )
        store = result["databaseWithObjectStores"]["objectStores"][0]
        assert len(store["indexes"]) == 100

    async def test_enable_disable_100x_alternating(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for i in range(100):
            if i % 2 == 0:
                await domain.enable()
            else:
                await domain.disable()
        assert len(fake.calls) == 100
        enable_count = sum(1 for c in fake.calls if c[0] == "IndexedDB.enable")
        disable_count = sum(1 for c in fake.calls if c[0] == "IndexedDB.disable")
        assert enable_count == 50
        assert disable_count == 50

    async def test_clear_object_store_100x_same_params(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        for _ in range(100):
            await domain.clear_object_store(
                security_origin="https://example.com",
                database_name="db1",
                object_store_name="s1",
            )
        assert len(fake.calls) == 100
        for _, params in fake.calls:
            assert params is not None
            assert params["databaseName"] == "db1"
            assert params["objectStoreName"] == "s1"

    async def test_error_after_successful_calls(self) -> None:
        class HybridSender:
            def __init__(self) -> None:
                self.calls = 0
                self._calls_list: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self._calls_list.append((method, params))
                self.calls += 1
                if self.calls <= 2:
                    return {}
                raise CommandError(code=-1, message="fail on 3rd")

            @property
            def last_call(self) -> tuple[str, dict[str, Any] | None]:
                return self._calls_list[-1]

        sender = HybridSender()
        domain = IndexedDBDomain(sender)
        await domain.enable()
        await domain.disable()
        with pytest.raises(CommandError):
            await domain.enable()
        assert sender.calls == 3

    async def test_request_data_empty_string_index_name(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            index_name="",
        )
        _, params = fake.last_call
        assert params is not None
        assert "indexName" not in params

    async def test_request_data_none_vs_empty_key_range(self) -> None:
        fake1 = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain1 = IndexedDBDomain(fake1)
        await domain1.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range=None,
        )
        _, params1 = fake1.last_call
        assert params1 is not None
        assert "keyRange" not in params1

        fake2 = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain2 = IndexedDBDomain(fake2)
        await domain2.request_data(
            security_origin="https://example.com",
            database_name="db1",
            object_store_name="s1",
            key_range={},
        )
        _, params2 = fake2.last_call
        assert params2 is not None
        assert "keyRange" not in params2

    async def test_storage_bucket_none_vs_empty_dict(self) -> None:
        fake1 = FakeSender({"databaseNames": []})
        domain1 = IndexedDBDomain(fake1)
        await domain1.request_database_names(storage_bucket=None)
        _, params1 = fake1.last_call
        assert params1 is not None
        assert "storageBucket" not in params1

        fake2 = FakeSender({"databaseNames": []})
        domain2 = IndexedDBDomain(fake2)
        await domain2.request_database_names(storage_bucket={})
        _, params2 = fake2.last_call
        assert params2 is not None
        assert "storageBucket" in params2
        assert params2["storageBucket"] == {}

    async def test_security_origin_empty_vs_none(self) -> None:
        fake1 = FakeSender({"databaseNames": []})
        domain1 = IndexedDBDomain(fake1)
        await domain1.request_database_names(security_origin="")
        _, params1 = fake1.last_call
        assert params1 is not None
        assert "securityOrigin" not in params1

        fake2 = FakeSender({"databaseNames": []})
        domain2 = IndexedDBDomain(fake2)
        await domain2.request_database_names(security_origin=None)
        _, params2 = fake2.last_call
        assert params2 is not None
        assert "securityOrigin" not in params2

    async def test_storage_key_empty_vs_none(self) -> None:
        fake1 = FakeSender({"databaseNames": []})
        domain1 = IndexedDBDomain(fake1)
        await domain1.request_database_names(storage_key="")
        _, params1 = fake1.last_call
        assert params1 is not None
        assert "storageKey" not in params1

        fake2 = FakeSender({"databaseNames": []})
        domain2 = IndexedDBDomain(fake2)
        await domain2.request_database_names(storage_key=None)
        _, params2 = fake2.last_call
        assert params2 is not None
        assert "storageKey" not in params2
