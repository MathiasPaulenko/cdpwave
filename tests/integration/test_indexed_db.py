"""Integration tests for the IndexedDB domain (real browser).

Exercises all IndexedDB domain methods against a real Chrome browser,
including enable/disable, requestDatabaseNames, requestDatabase,
requestData, getMetadata, deleteDatabase, clearObjectStore,
deleteObjectStoreEntries, and full lifecycle flows.
"""

import asyncio
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


async def _wait_for_page(page: CDPSession) -> str:
    await page.page.enable()
    nav_result = await page.page.navigate("https://example.com")
    frame_id = nav_result.get("frameId", "")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True,
        )
        if result.get("result", {}).get("value"):
            break
    return frame_id


async def _create_idb(
    session: CDPSession,
    db_name: str = "test-idb-integration",
    store_name: str = "store1",
) -> dict[str, Any]:
    """Create an IndexedDB database with an object store and records via JS."""
    await session.runtime.enable()
    await session.runtime.evaluate(
        f"""
        new Promise((resolve, reject) => {{
            const req = indexedDB.open('{db_name}', 1);
            req.onupgradeneeded = (event) => {{
                const db = event.target.result;
                if (!db.objectStoreNames.contains('{store_name}')) {{
                    db.createObjectStore('{store_name}', {{keyPath: 'id'}});
                }}
            }};
            req.onsuccess = (event) => {{
                const db = event.target.result;
                const tx = db.transaction('{store_name}', 'readwrite');
                const store = tx.objectStore('{store_name}');
                store.put({{id: 1, name: 'Alice'}});
                store.put({{id: 2, name: 'Bob'}});
                store.put({{id: 3, name: 'Charlie'}});
                tx.oncomplete = () => {{ db.close(); resolve('done'); }};
                tx.onerror = () => reject(tx.error);
            }};
            req.onerror = () => reject(req.error);
        }})
        """,
        return_by_value=True,
        await_promise=True,
    )
    return {"db_name": db_name, "store_name": store_name}


@pytest.mark.integration
class TestIndexedDBIntegration:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_enable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.indexed_db.enable()
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_disable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            result = await session.indexed_db.disable()
            assert isinstance(result, dict)

    async def test_request_database_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "databaseNames" in result
            assert isinstance(result["databaseNames"], list)
            await session.indexed_db.disable()

    async def test_request_database_names_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session)
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            result = await session.indexed_db.request_database_names(
                storage_key=storage_key,
            )
            assert "databaseNames" in result
            await session.indexed_db.disable()

    async def test_request_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-req-db")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            assert "databaseWithObjectStores" in result
            db = result["databaseWithObjectStores"]
            assert db["name"] == info["db_name"]
            assert isinstance(db["objectStores"], list)
            await session.indexed_db.disable()

    async def test_request_data(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert "objectStoreDataEntries" in result
            assert "hasMore" in result
            await session.indexed_db.disable()

    async def test_request_data_with_skip_count(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=1,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_request_data_with_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=2,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_request_data_with_index_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                index_name="",
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert "entriesCount" in result
            assert "keyGeneratorValue" in result
            await session.indexed_db.disable()

    async def test_clear_object_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-clear")
            await session.indexed_db.enable()
            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert result["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_delete_object_store_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-delete-entries")
            await session.indexed_db.enable()
            key_range = {"lower": None, "upper": None}
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range=key_range,
                security_origin="https://example.com",
            )
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert result["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_delete_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-delete-db")
            await session.indexed_db.enable()
            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] not in result.get("databaseNames", [])
            await session.indexed_db.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-lifecycle")
            await session.indexed_db.enable()

            names = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] in names.get("databaseNames", [])

            db = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            assert "databaseWithObjectStores" in db

            data = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert "objectStoreDataEntries" in data

            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] > 0

            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta_after = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta_after["entriesCount"] == 0

            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            names_after = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] not in names_after.get("databaseNames", [])

            await session.indexed_db.disable()

    async def test_request_database_names_empty_db(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "databaseNames" in result
            assert isinstance(result["databaseNames"], list)
            await session.indexed_db.disable()

    async def test_request_database_nonexistent_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_database(
                    security_origin="https://example.com",
                    database_name="nonexistent-db-xyz",
                )
            await session.indexed_db.disable()

    async def test_request_data_nonexistent_db(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_data(
                    security_origin="https://example.com",
                    database_name="nonexistent-db-xyz",
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_get_metadata_nonexistent_db(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.get_metadata(
                    database_name="nonexistent-db-xyz",
                    object_store_name="nonexistent-store",
                    security_origin="https://example.com",
                )
            await session.indexed_db.disable()

    async def test_delete_database_nonexistent(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.delete_database(
                    security_origin="https://example.com",
                    database_name="nonexistent-db-xyz",
                )
            await session.indexed_db.disable()

    async def test_clear_object_store_nonexistent_db(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name="nonexistent-db-xyz",
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_raw_send_all_commands(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send("IndexedDB.enable")
            result = await session.send(
                "IndexedDB.requestDatabaseNames",
                {"securityOrigin": "https://example.com"},
            )
            assert "databaseNames" in result
            await session.send("IndexedDB.disable")

    async def test_request_database_names_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_request_database_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="test-idb-dict")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_request_data_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_get_metadata_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.indexed_db.enable()
                await session.indexed_db.disable()

    async def test_request_data_large_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=1000,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()


@pytest.mark.integration
class TestIndexedDBIntegrationEdge:
    async def test_request_data_page_size_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-ps0")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=0,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_request_data_skip_count_exceeds_records(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-skip-exceed")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=999,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_get_metadata_after_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-meta-clear")
            await session.indexed_db.enable()
            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert result["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_clear_object_store_nonexistent_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-clear-ne")
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_delete_object_store_entries_partial(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-del-partial")
            await session.indexed_db.enable()
            key_range = {"lower": None, "upper": None}
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range=key_range,
                security_origin="https://example.com",
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_request_database_returns_object_store_details(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-store-details")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            db = result["databaseWithObjectStores"]
            assert db["name"] == info["db_name"]
            stores = db["objectStores"]
            assert len(stores) >= 1
            store = next(s for s in stores if s["name"] == info["store_name"])
            assert "keyPath" in store
            await session.indexed_db.disable()

    async def test_multiple_databases_create_and_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="edge-idb-multi-a")
            await _create_idb(session, db_name="edge-idb-multi-b")
            await _create_idb(session, db_name="edge-idb-multi-c")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            names = result.get("databaseNames", [])
            assert "edge-idb-multi-a" in names
            assert "edge-idb-multi-b" in names
            assert "edge-idb-multi-c" in names
            await session.indexed_db.disable()

    async def test_request_data_with_key_range_specific(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-keyrange-spec")
            await session.indexed_db.enable()
            key_range = {"lower": None, "upper": None}
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range=key_range,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_request_data_after_delete_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-after-del")
            await session.indexed_db.enable()
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
                security_origin="https://example.com",
            )
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert len(result["objectStoreDataEntries"]) == 0
            await session.indexed_db.disable()

    async def test_enable_disable_then_re_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.disable()
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "databaseNames" in result
            await session.indexed_db.disable()

    async def test_request_database_names_after_delete(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-names-after-del")
            await session.indexed_db.enable()
            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] not in result.get("databaseNames", [])
            await session.indexed_db.disable()

    async def test_request_data_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-data-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            result = await session.indexed_db.request_data(
                storage_key=storage_key,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_get_metadata_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-meta-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=storage_key,
            )
            assert "entriesCount" in result
            await session.indexed_db.disable()

    async def test_request_database_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-db-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            result = await session.indexed_db.request_database(
                storage_key=storage_key,
                database_name=info["db_name"],
            )
            assert "databaseWithObjectStores" in result
            await session.indexed_db.disable()

    async def test_clear_object_store_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-clear-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            await session.indexed_db.clear_object_store(
                storage_key=storage_key,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=storage_key,
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_delete_database_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-del-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            await session.indexed_db.delete_database(
                storage_key=storage_key,
                database_name=info["db_name"],
            )
            names = await session.indexed_db.request_database_names(
                storage_key=storage_key,
            )
            assert info["db_name"] not in names.get("databaseNames", [])
            await session.indexed_db.disable()

    async def test_delete_object_store_entries_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-del-entries-sk")
            await session.indexed_db.enable()
            storage_key_result = await session.storage.get_storage_key()
            storage_key = storage_key_result["storageKey"]
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
                storage_key=storage_key,
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=storage_key,
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_request_data_pagination(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-pagination")
            await session.indexed_db.enable()
            r1 = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=0,
                page_size=2,
            )
            assert len(r1["objectStoreDataEntries"]) <= 2
            r2 = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=2,
                page_size=2,
            )
            assert "objectStoreDataEntries" in r2
            await session.indexed_db.disable()

    async def test_request_data_has_more_true_with_small_page(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-hasmore")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=1,
            )
            assert result["hasMore"] is True
            await session.indexed_db.disable()

    async def test_raw_send_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-raw-meta")
            await session.send("IndexedDB.enable")
            result = await session.send(
                "IndexedDB.getMetadata",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            assert "entriesCount" in result
            await session.send("IndexedDB.disable")

    async def test_raw_send_delete_object_store_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="edge-idb-raw-del-entries")
            await session.send("IndexedDB.enable")
            await session.send(
                "IndexedDB.deleteObjectStoreEntries",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                    "keyRange": {"lower": None, "upper": None},
                },
            )
            result = await session.send(
                "IndexedDB.getMetadata",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            assert result["entriesCount"] == 0
            await session.send("IndexedDB.disable")


@pytest.mark.integration
class TestIndexedDBIntegrationBoundary:
    async def test_unicode_database_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(
                session, db_name="数据库-🔒", store_name="ストア",
            )
            await session.indexed_db.enable()
            names = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "数据库-🔒" in names["databaseNames"]
            db = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name="数据库-🔒",
            )
            stores = db["databaseWithObjectStores"]["objectStores"]
            assert any(s["name"] == "ストア" for s in stores)
            await session.indexed_db.disable()

    async def test_concurrent_request_database_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="edge-idb-concurrent-names")
            await session.indexed_db.enable()
            results = await asyncio.gather(
                session.indexed_db.request_database_names(
                    security_origin="https://example.com",
                ),
                session.indexed_db.request_database_names(
                    security_origin="https://example.com",
                ),
                session.indexed_db.request_database_names(
                    security_origin="https://example.com",
                ),
            )
            for r in results:
                assert "databaseNames" in r
            await session.indexed_db.disable()

    async def test_repeated_enable_10x(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(10):
                await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_delete_and_recreate_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-del-recreate",
            )
            await session.indexed_db.enable()
            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            names_after = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] not in names_after["databaseNames"]
            await _create_idb(session, db_name="edge-idb-del-recreate")
            names_recreated = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "edge-idb-del-recreate" in names_recreated["databaseNames"]
            await session.indexed_db.disable()

    async def test_get_metadata_after_delete_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-meta-after-del",
            )
            await session.indexed_db.enable()
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
                security_origin="https://example.com",
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_request_database_names_empty_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_database_names(
                    security_origin="",
                )
            await session.indexed_db.disable()

    async def test_request_data_large_page_size_hasmore_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-large-ps-hasmore",
            )
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=10000,
            )
            assert result["hasMore"] is False
            assert len(result["objectStoreDataEntries"]) == 3
            await session.indexed_db.disable()

    async def test_request_data_skip_all_records(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-skip-all",
            )
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=3,
            )
            assert len(result["objectStoreDataEntries"]) == 0
            assert result["hasMore"] is False
            await session.indexed_db.disable()

    async def test_clear_then_delete_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-clear-then-del",
            )
            await session.indexed_db.enable()
            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
                security_origin="https://example.com",
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_request_database_with_storage_key_and_verify(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-db-sk-verify",
            )
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            db = await session.indexed_db.request_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            db_data = db["databaseWithObjectStores"]
            assert db_data["name"] == info["db_name"]
            assert len(db_data["objectStores"]) >= 1
            store = db_data["objectStores"][0]
            assert store["name"] == info["store_name"]
            assert "keyPath" in store
            await session.indexed_db.disable()

    async def test_request_data_with_storage_key_pagination(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-sk-pagination",
            )
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            r1 = await session.indexed_db.request_data(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=0,
                page_size=2,
            )
            assert len(r1["objectStoreDataEntries"]) == 2
            assert r1["hasMore"] is True
            r2 = await session.indexed_db.request_data(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=2,
                page_size=2,
            )
            assert len(r2["objectStoreDataEntries"]) == 1
            assert r2["hasMore"] is False
            await session.indexed_db.disable()

    async def test_concurrent_clear_and_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-concurrent-clear-meta",
            )
            await session.indexed_db.enable()
            await asyncio.gather(
                session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                ),
                session.indexed_db.get_metadata(
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                    security_origin="https://example.com",
                ),
            )
            await session.indexed_db.disable()

    async def test_request_data_key_range_lower_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-kr-lower-only",
            )
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": 2},
            )
            entries = result["objectStoreDataEntries"]
            assert len(entries) == 2
            await session.indexed_db.disable()

    async def test_request_data_key_range_upper_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-kr-upper-only",
            )
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"upper": 2},
            )
            entries = result["objectStoreDataEntries"]
            assert len(entries) >= 1
            await session.indexed_db.disable()

    async def test_delete_database_names_after_delete_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="edge-idb-del-sk-verify",
            )
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            await session.indexed_db.delete_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            names = await session.indexed_db.request_database_names(
                storage_key=sk,
            )
            assert info["db_name"] not in names["databaseNames"]
            await session.indexed_db.disable()
