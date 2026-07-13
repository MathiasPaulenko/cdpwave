"""E2E tests for the IndexedDB domain (real browser flows).

Full end-to-end flows against a real Chrome browser, including
IndexedDB API interaction via JS, CDP IndexedDB domain verification,
raw command sending, and edge cases.
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
    db_name: str = "e2e-idb",
    store_name: str = "store1",
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create an IndexedDB database with an object store and records via JS."""
    if records is None:
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]
    records_js = ", ".join(
        f"{{id: {r['id']}, name: '{r['name']}'}}" for r in records
    )
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
                const records = [{records_js}];
                for (const r of records) {{
                    store.put(r);
                }}
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


@pytest.mark.e2e
class TestIndexedDBE2E:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.indexed_db.enable()
            assert isinstance(result, dict)
            await session.indexed_db.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            result = await session.indexed_db.disable()
            assert isinstance(result, dict)

    async def test_request_database_names_security_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="e2e-idb-names")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "databaseNames" in result
            assert isinstance(result["databaseNames"], list)
            assert "e2e-idb-names" in result["databaseNames"]
            await session.indexed_db.disable()

    async def test_request_database_names_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="e2e-idb-names-sk")
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
            info = await _create_idb(session, db_name="e2e-idb-req-db")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            assert "databaseWithObjectStores" in result
            db = result["databaseWithObjectStores"]
            assert db["name"] == info["db_name"]
            assert isinstance(db["objectStores"], list)
            store_names = [s["name"] for s in db["objectStores"]]
            assert info["store_name"] in store_names
            await session.indexed_db.disable()

    async def test_request_data(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-req-data")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert "objectStoreDataEntries" in result
            assert "hasMore" in result
            entries = result["objectStoreDataEntries"]
            assert len(entries) > 0
            await session.indexed_db.disable()

    async def test_request_data_with_skip_count(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-skip")
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
            info = await _create_idb(session, db_name="e2e-idb-page")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=2,
            )
            assert "objectStoreDataEntries" in result
            assert result["hasMore"] is True
            await session.indexed_db.disable()

    async def test_request_data_with_index_name_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-index-empty")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                index_name="",
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_request_data_with_key_range(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-keyrange")
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

    async def test_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-metadata")
            await session.indexed_db.enable()
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert "entriesCount" in result
            assert "keyGeneratorValue" in result
            assert result["entriesCount"] == 3
            await session.indexed_db.disable()

    async def test_clear_object_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-clear")
            await session.indexed_db.enable()
            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_delete_object_store_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-del-entries")
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

    async def test_delete_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-del-db")
            await session.indexed_db.enable()
            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name=info["db_name"],
            )
            names = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert info["db_name"] not in names.get("databaseNames", [])
            await session.indexed_db.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-lifecycle")
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
            assert len(data["objectStoreDataEntries"]) > 0

            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 3

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

    async def test_raw_send_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("IndexedDB.enable")
            await session.send("IndexedDB.disable")

    async def test_raw_send_request_database_names(self) -> None:
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

    async def test_raw_send_request_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-db")
            await session.send("IndexedDB.enable")
            result = await session.send(
                "IndexedDB.requestDatabase",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                },
            )
            assert "databaseWithObjectStores" in result
            await session.send("IndexedDB.disable")

    async def test_raw_send_request_data(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-data")
            await session.send("IndexedDB.enable")
            result = await session.send(
                "IndexedDB.requestData",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                    "indexName": "",
                    "skipCount": 0,
                    "pageSize": 10,
                },
            )
            assert "objectStoreDataEntries" in result
            await session.send("IndexedDB.disable")

    async def test_raw_send_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-meta")
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

    async def test_raw_send_delete_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-del")
            await session.send("IndexedDB.enable")
            await session.send(
                "IndexedDB.deleteDatabase",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                },
            )
            names = await session.send(
                "IndexedDB.requestDatabaseNames",
                {"securityOrigin": "https://example.com"},
            )
            assert info["db_name"] not in names.get("databaseNames", [])
            await session.send("IndexedDB.disable")

    async def test_raw_send_clear_object_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-clear")
            await session.send("IndexedDB.enable")
            await session.send(
                "IndexedDB.clearObjectStore",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            meta = await session.send(
                "IndexedDB.getMetadata",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            assert meta["entriesCount"] == 0
            await session.send("IndexedDB.disable")

    async def test_raw_send_delete_object_store_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-raw-del-entries")
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
            meta = await session.send(
                "IndexedDB.getMetadata",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            assert meta["entriesCount"] == 0
            await session.send("IndexedDB.disable")

    async def test_all_methods_return_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-return-dict")
            await session.indexed_db.enable()
            assert isinstance(await session.indexed_db.enable(), dict)
            assert isinstance(
                await session.indexed_db.request_database_names(
                    security_origin="https://example.com",
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.request_database(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.request_data(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.get_metadata(
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                    security_origin="https://example.com",
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.delete_object_store_entries(
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                    key_range={"lower": None, "upper": None},
                    security_origin="https://example.com",
                ),
                dict,
            )
            assert isinstance(
                await session.indexed_db.delete_database(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                ),
                dict,
            )
            assert isinstance(await session.indexed_db.disable(), dict)

    async def test_empty_db_request_database_names(self) -> None:
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

    async def test_nonexistent_database_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_database(
                    security_origin="https://example.com",
                    database_name="nonexistent-e2e-xyz",
                )
            await session.indexed_db.disable()

    async def test_nonexistent_db_request_data(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_data(
                    security_origin="https://example.com",
                    database_name="nonexistent-e2e-data",
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_nonexistent_db_get_metadata(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.get_metadata(
                    database_name="nonexistent-e2e-meta",
                    object_store_name="nonexistent-store",
                    security_origin="https://example.com",
                )
            await session.indexed_db.disable()

    async def test_nonexistent_db_delete_database(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.delete_database(
                    security_origin="https://example.com",
                    database_name="nonexistent-e2e-del",
                )
            await session.indexed_db.disable()

    async def test_nonexistent_db_clear_object_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name="nonexistent-e2e-clear",
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.indexed_db.enable()
                await session.indexed_db.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.disable()

    async def test_request_data_large_page_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-large-page")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=1000,
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_multiple_databases(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="e2e-idb-multi-1")
            await _create_idb(session, db_name="e2e-idb-multi-2")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            names = result.get("databaseNames", [])
            assert "e2e-idb-multi-1" in names
            assert "e2e-idb-multi-2" in names
            await session.indexed_db.disable()

    async def test_request_data_after_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-after-clear")
            await session.indexed_db.enable()
            await session.indexed_db.clear_object_store(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert len(result["objectStoreDataEntries"]) == 0
            await session.indexed_db.disable()

    async def test_request_data_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-idb-all-params")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                storage_key="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                index_name="",
                skip_count=0,
                page_size=10,
                key_range={"lower": None, "upper": None},
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()


@pytest.mark.e2e
class TestIndexedDBE2EEdge:
    async def test_request_data_page_size_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-ps0")
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
            info = await _create_idb(session, db_name="e2e-edge-skip-exceed")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=999,
            )
            assert len(result["objectStoreDataEntries"]) == 0
            await session.indexed_db.disable()

    async def test_get_metadata_after_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-meta-clear")
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

    async def test_clear_nonexistent_object_store(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-clear-ne")
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.clear_object_store(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name="nonexistent-store",
                )
            await session.indexed_db.disable()

    async def test_delete_entries_then_verify_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-del-verify")
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
            data = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert len(data["objectStoreDataEntries"]) == 0
            await session.indexed_db.disable()

    async def test_request_database_verify_object_store_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-store-fields")
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
            assert "autoIncrement" in store
            await session.indexed_db.disable()

    async def test_multiple_databases_create_list_delete(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="e2e-edge-multi-a")
            await _create_idb(session, db_name="e2e-edge-multi-b")
            await session.indexed_db.enable()
            names = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "e2e-edge-multi-a" in names["databaseNames"]
            assert "e2e-edge-multi-b" in names["databaseNames"]
            await session.indexed_db.delete_database(
                security_origin="https://example.com",
                database_name="e2e-edge-multi-a",
            )
            names_after = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "e2e-edge-multi-a" not in names_after["databaseNames"]
            assert "e2e-edge-multi-b" in names_after["databaseNames"]
            await session.indexed_db.disable()

    async def test_request_data_with_key_range(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-keyrange")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
            )
            assert "objectStoreDataEntries" in result
            assert len(result["objectStoreDataEntries"]) == 3
            await session.indexed_db.disable()

    async def test_enable_disable_re_enable(self) -> None:
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

    async def test_request_data_pagination(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-pagination")
            await session.indexed_db.enable()
            r1 = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=0,
                page_size=2,
            )
            assert len(r1["objectStoreDataEntries"]) == 2
            assert r1["hasMore"] is True
            r2 = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                skip_count=2,
                page_size=2,
            )
            assert len(r2["objectStoreDataEntries"]) == 1
            assert r2["hasMore"] is False
            await session.indexed_db.disable()

    async def test_request_data_has_more_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-hasmore")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                page_size=1,
            )
            assert result["hasMore"] is True
            await session.indexed_db.disable()

    async def test_all_methods_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-all-sk")
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            names = await session.indexed_db.request_database_names(storage_key=sk)
            assert info["db_name"] in names["databaseNames"]
            db = await session.indexed_db.request_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            assert "databaseWithObjectStores" in db
            data = await session.indexed_db.request_data(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert "objectStoreDataEntries" in data
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=sk,
            )
            assert meta["entriesCount"] == 3
            await session.indexed_db.clear_object_store(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta_after = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=sk,
            )
            assert meta_after["entriesCount"] == 0
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={"lower": None, "upper": None},
                storage_key=sk,
            )
            await session.indexed_db.delete_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            names_after = await session.indexed_db.request_database_names(
                storage_key=sk,
            )
            assert info["db_name"] not in names_after["databaseNames"]
            await session.indexed_db.disable()

    async def test_raw_send_all_commands(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-raw-all")
            await session.send("IndexedDB.enable")
            names = await session.send(
                "IndexedDB.requestDatabaseNames",
                {"securityOrigin": "https://example.com"},
            )
            assert "databaseNames" in names
            db = await session.send(
                "IndexedDB.requestDatabase",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                },
            )
            assert "databaseWithObjectStores" in db
            data = await session.send(
                "IndexedDB.requestData",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                    "indexName": "",
                    "skipCount": 0,
                    "pageSize": 10,
                },
            )
            assert "objectStoreDataEntries" in data
            meta = await session.send(
                "IndexedDB.getMetadata",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            assert "entriesCount" in meta
            await session.send(
                "IndexedDB.clearObjectStore",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                },
            )
            await session.send(
                "IndexedDB.deleteObjectStoreEntries",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                    "objectStoreName": info["store_name"],
                    "keyRange": {"lower": None, "upper": None},
                },
            )
            await session.send(
                "IndexedDB.deleteDatabase",
                {
                    "securityOrigin": "https://example.com",
                    "databaseName": info["db_name"],
                },
            )
            await session.send("IndexedDB.disable")

    async def test_nonexistent_db_delete_object_store_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.delete_object_store_entries(
                    database_name="nonexistent-e2e-dse",
                    object_store_name="nonexistent-store",
                    key_range={"lower": None, "upper": None},
                    security_origin="https://example.com",
                )
            await session.indexed_db.disable()

    async def test_full_lifecycle_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-lifecycle-sk")
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            names = await session.indexed_db.request_database_names(storage_key=sk)
            assert info["db_name"] in names["databaseNames"]
            db = await session.indexed_db.request_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            assert db["databaseWithObjectStores"]["name"] == info["db_name"]
            data = await session.indexed_db.request_data(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert len(data["objectStoreDataEntries"]) == 3
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=sk,
            )
            assert meta["entriesCount"] == 3
            await session.indexed_db.clear_object_store(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta_after = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                storage_key=sk,
            )
            assert meta_after["entriesCount"] == 0
            await session.indexed_db.delete_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            names_after = await session.indexed_db.request_database_names(
                storage_key=sk,
            )
            assert info["db_name"] not in names_after["databaseNames"]
            await session.indexed_db.disable()

    async def test_request_data_empty_key_range(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-empty-kr")
            await session.indexed_db.enable()
            result = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={},
            )
            assert "objectStoreDataEntries" in result
            await session.indexed_db.disable()

    async def test_delete_object_store_entries_empty_key_range(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-del-empty-kr")
            await session.indexed_db.enable()
            await session.indexed_db.delete_object_store_entries(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                key_range={},
                security_origin="https://example.com",
            )
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_get_metadata_float_key_generator(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-float-kg")
            await session.indexed_db.enable()
            result = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert "entriesCount" in result
            assert "keyGeneratorValue" in result
            assert isinstance(result["keyGeneratorValue"], (int, float))
            await session.indexed_db.disable()

    async def test_request_data_index_name_nonempty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(session, db_name="e2e-edge-idx-name")
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_data(
                    security_origin="https://example.com",
                    database_name=info["db_name"],
                    object_store_name=info["store_name"],
                    index_name="nonexistent-index",
                )
            await session.indexed_db.disable()

    async def test_request_database_names_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_database_names()
            await session.indexed_db.disable()

    async def test_request_database_no_origin_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.request_database(
                    database_name="some-db",
                )
            await session.indexed_db.disable()

    async def test_clear_object_store_no_origin_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            with pytest.raises(CommandError):
                await session.indexed_db.clear_object_store(
                    database_name="some-db",
                    object_store_name="some-store",
                )
            await session.indexed_db.disable()


@pytest.mark.e2e
class TestIndexedDBE2EBoundary:
    async def test_unicode_database_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(
                session, db_name="数据库-🔒-e2e", store_name="ストア",
            )
            await session.indexed_db.enable()
            names = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "数据库-🔒-e2e" in names["databaseNames"]
            db = await session.indexed_db.request_database(
                security_origin="https://example.com",
                database_name="数据库-🔒-e2e",
            )
            stores = db["databaseWithObjectStores"]["objectStores"]
            assert any(s["name"] == "ストア" for s in stores)
            data = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name="数据库-🔒-e2e",
                object_store_name="ストア",
            )
            assert len(data["objectStoreDataEntries"]) == 3
            await session.indexed_db.disable()

    async def test_concurrent_request_database_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await _create_idb(session, db_name="e2e-idb-concurrent-names")
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
                assert "e2e-idb-concurrent-names" in r["databaseNames"]
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
                session, db_name="e2e-idb-del-recreate",
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
            await _create_idb(session, db_name="e2e-idb-del-recreate")
            names_recreated = await session.indexed_db.request_database_names(
                security_origin="https://example.com",
            )
            assert "e2e-idb-del-recreate" in names_recreated["databaseNames"]
            data = await session.indexed_db.request_data(
                security_origin="https://example.com",
                database_name="e2e-idb-del-recreate",
                object_store_name="store1",
            )
            assert len(data["objectStoreDataEntries"]) == 3
            await session.indexed_db.disable()

    async def test_request_data_key_range_lower_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-kr-lower-only",
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
                session, db_name="e2e-idb-kr-upper-only",
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

    async def test_request_data_skip_all_records(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-skip-all",
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
                session, db_name="e2e-idb-clear-then-del",
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
                session, db_name="e2e-idb-large-ps-hasmore",
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

    async def test_pagination_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-sk-pagination",
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
                session, db_name="e2e-idb-concurrent-clear-meta",
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
            meta = await session.indexed_db.get_metadata(
                database_name=info["db_name"],
                object_store_name=info["store_name"],
                security_origin="https://example.com",
            )
            assert meta["entriesCount"] == 0
            await session.indexed_db.disable()

    async def test_delete_database_with_storage_key_verify(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-del-sk-verify",
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

    async def test_request_database_with_storage_key_verify_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-db-sk-fields",
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
            store = db_data["objectStores"][0]
            assert store["name"] == info["store_name"]
            assert "keyPath" in store
            assert "autoIncrement" in store
            assert "indexes" in store
            await session.indexed_db.disable()

    async def test_full_lifecycle_unicode_with_storage_key(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            info = await _create_idb(
                session, db_name="e2e-idb-lifecycle-sk", store_name="ストア",
            )
            await session.indexed_db.enable()
            sk_result = await session.storage.get_storage_key()
            sk = sk_result["storageKey"]
            names = await session.indexed_db.request_database_names(storage_key=sk)
            assert info["db_name"] in names["databaseNames"]
            db = await session.indexed_db.request_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            assert db["databaseWithObjectStores"]["name"] == info["db_name"]
            data = await session.indexed_db.request_data(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert len(data["objectStoreDataEntries"]) == 3
            meta = await session.indexed_db.get_metadata(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert meta["entriesCount"] == 3
            await session.indexed_db.clear_object_store(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            meta_after = await session.indexed_db.get_metadata(
                storage_key=sk,
                database_name=info["db_name"],
                object_store_name=info["store_name"],
            )
            assert meta_after["entriesCount"] == 0
            await session.indexed_db.delete_database(
                storage_key=sk,
                database_name=info["db_name"],
            )
            names_after = await session.indexed_db.request_database_names(
                storage_key=sk,
            )
            assert info["db_name"] not in names_after["databaseNames"]
            await session.indexed_db.disable()
