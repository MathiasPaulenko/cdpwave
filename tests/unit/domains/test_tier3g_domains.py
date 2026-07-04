"""Unit tests for Preload, IndexedDB, Media, and DeviceAccess domains."""

import pytest

from cdpwave.domains.device_access import DeviceAccessDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
from cdpwave.domains.media import MediaDomain
from cdpwave.domains.preload import PreloadDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestPreloadDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Preload.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Preload.disable", None)

    async def test_get_preload_policy(self) -> None:
        fake = FakeSender({"preloadPolicy": "always"})
        domain = PreloadDomain(fake)
        await domain.get_preload_policy()
        assert fake.last_call == ("Preload.getPreloadPolicy", None)

    async def test_set_preload_policy(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.set_preload_policy("no-preload")
        assert fake.last_call == (
            "Preload.setPreloadPolicy",
            {"preloadPolicy": "no-preload"},
        )


@pytest.mark.unit
class TestIndexedDBDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        assert fake.last_call == ("IndexedDB.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        assert fake.last_call == ("IndexedDB.disable", None)

    async def test_request_database_names(self) -> None:
        fake = FakeSender({"databaseNames": ["db1", "db2"]})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabaseNames"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"

    async def test_request_database(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="https://example.com", database_name="testdb"
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabase"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["securityOrigin"] == "https://example.com"

    async def test_request_data(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="testdb",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestData"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["objectStoreName"] == "store1"
        assert params["skipCount"] == 0
        assert params["pageSize"] == 10

    async def test_delete_database(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="https://example.com", database_name="testdb"
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteDatabase"
        assert params is not None
        assert params["databaseName"] == "testdb"

    async def test_clear_object_store(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="testdb",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.clearObjectStore"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["objectStoreName"] == "store1"


@pytest.mark.unit
class TestMediaDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Media.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Media.disable", None)

    async def test_get_player_properties(self) -> None:
        fake = FakeSender({"properties": [{"name": "currentTime", "value": "0"}]})
        domain = MediaDomain(fake)
        await domain.get_player_properties("player1")
        assert fake.last_call == (
            "Media.getPlayerProperties",
            {"playerId": "player1"},
        )

    async def test_get_players(self) -> None:
        fake = FakeSender({"players": []})
        domain = MediaDomain(fake)
        await domain.get_players()
        assert fake.last_call == ("Media.getPlayers", None)


@pytest.mark.unit
class TestDeviceAccessDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.enable()
        assert fake.last_call == ("DeviceAccess.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.disable()
        assert fake.last_call == ("DeviceAccess.disable", None)

    async def test_select_bluetooth_device(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.select_bluetooth_device(
            "req1", {"id": "dev1", "name": "Test Device"}
        )
        method, params = fake.last_call
        assert method == "DeviceAccess.selectBluetoothDevice"
        assert params is not None
        assert params["requestId"] == "req1"
        assert params["device"]["id"] == "dev1"

    async def test_cancel_prompt(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.cancel_prompt("req1")
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"requestId": "req1"},
        )
