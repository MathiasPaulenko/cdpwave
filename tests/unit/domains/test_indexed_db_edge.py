"""Edge-case tests for the IndexedDB domain — validation branches only.

Targets every TypeError raise in IndexedDBDomain to push
coverage from 76% to >=90%.
"""

import pytest

from cdpwave.domains.indexed_db import IndexedDBDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestIndexedDBEdgeValidation:
    async def test_clear_object_store_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.clear_object_store(security_origin="http://x", database_name=123)  # type: ignore[arg-type]

    async def test_clear_object_store_object_store_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="object_store_name must be a string"):
            await d.clear_object_store(security_origin="http://x", object_store_name=123)  # type: ignore[arg-type]

    async def test_clear_object_store_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.clear_object_store(security_origin=123)  # type: ignore[arg-type]

    async def test_clear_object_store_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.clear_object_store(storage_key=123)  # type: ignore[arg-type]

    async def test_clear_object_store_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.clear_object_store(storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_delete_database_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.delete_database(security_origin="http://x", database_name=123)  # type: ignore[arg-type]

    async def test_delete_database_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.delete_database(security_origin=123)  # type: ignore[arg-type]

    async def test_delete_database_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.delete_database(storage_key=123)  # type: ignore[arg-type]

    async def test_delete_database_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.delete_database(storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_delete_object_store_entries_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.delete_object_store_entries(123, "store", {})  # type: ignore[arg-type]

    async def test_delete_object_store_entries_object_store_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="object_store_name must be a string"):
            await d.delete_object_store_entries("db", 123, {})  # type: ignore[arg-type]

    async def test_delete_object_store_entries_key_range_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key_range must be a dict"):
            await d.delete_object_store_entries("db", "store", "not-a-dict")  # type: ignore[arg-type]

    async def test_delete_object_store_entries_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.delete_object_store_entries("db", "store", {}, security_origin=123)  # type: ignore[arg-type]

    async def test_delete_object_store_entries_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.delete_object_store_entries("db", "store", {}, storage_key=123)  # type: ignore[arg-type]

    async def test_delete_object_store_entries_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.delete_object_store_entries("db", "store", {}, storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_get_metadata_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.get_metadata(123, "store", security_origin="http://x")  # type: ignore[arg-type]

    async def test_get_metadata_object_store_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="object_store_name must be a string"):
            await d.get_metadata("db", 123, security_origin="http://x")  # type: ignore[arg-type]

    async def test_get_metadata_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.get_metadata("db", "store", security_origin=123)  # type: ignore[arg-type]

    async def test_get_metadata_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.get_metadata("db", "store", storage_key=123)  # type: ignore[arg-type]

    async def test_get_metadata_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.get_metadata("db", "store", storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_request_data_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.request_data(security_origin="http://x", database_name=123)  # type: ignore[arg-type]

    async def test_request_data_object_store_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="object_store_name must be a string"):
            await d.request_data(security_origin="http://x", object_store_name=123)  # type: ignore[arg-type]

    async def test_request_data_index_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="index_name must be a string"):
            await d.request_data(security_origin="http://x", index_name=123)  # type: ignore[arg-type]

    async def test_request_data_skip_count_not_int(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="skip_count must be an int"):
            await d.request_data(security_origin="http://x", skip_count="x")  # type: ignore[arg-type]

    async def test_request_data_skip_count_bool(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="skip_count must be an int"):
            await d.request_data(security_origin="http://x", skip_count=True)  # type: ignore[arg-type]

    async def test_request_data_page_size_not_int(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="page_size must be an int"):
            await d.request_data(security_origin="http://x", page_size="x")  # type: ignore[arg-type]

    async def test_request_data_page_size_bool(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="page_size must be an int"):
            await d.request_data(security_origin="http://x", page_size=True)  # type: ignore[arg-type]

    async def test_request_data_key_range_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key_range must be a dict or None"):
            await d.request_data(security_origin="http://x", key_range="not-a-dict")  # type: ignore[arg-type]

    async def test_request_data_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.request_data(security_origin=123)  # type: ignore[arg-type]

    async def test_request_data_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.request_data(storage_key=123)  # type: ignore[arg-type]

    async def test_request_data_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.request_data(storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_request_database_database_name_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="database_name must be a string"):
            await d.request_database(security_origin="http://x", database_name=123)  # type: ignore[arg-type]

    async def test_request_database_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.request_database(security_origin=123)  # type: ignore[arg-type]

    async def test_request_database_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.request_database(storage_key=123)  # type: ignore[arg-type]

    async def test_request_database_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.request_database(storage_bucket="not-a-dict")  # type: ignore[arg-type]

    async def test_request_database_names_security_origin_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="security_origin must be a str or None"):
            await d.request_database_names(security_origin=123)  # type: ignore[arg-type]

    async def test_request_database_names_storage_key_not_str(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_key must be a str or None"):
            await d.request_database_names(storage_key=123)  # type: ignore[arg-type]

    async def test_request_database_names_storage_bucket_not_dict(self) -> None:
        d = IndexedDBDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_bucket must be a dict or None"):
            await d.request_database_names(storage_bucket="not-a-dict")  # type: ignore[arg-type]
