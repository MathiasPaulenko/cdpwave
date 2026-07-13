"""Unit tests for Extensions, PWA, Worker, and Inspector domains."""

import pytest

from cdpwave.domains.extensions import ExtensionsDomain
from cdpwave.domains.inspector import InspectorDomain
from cdpwave.domains.pwa import PWADomain
from cdpwave.domains.worker import WorkerDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestExtensionsDomain:
    async def test_load_unpacked(self) -> None:
        fake = FakeSender({"id": "ext123"})
        domain = ExtensionsDomain(fake)
        await domain.load_unpacked("/path/to/extension")
        method, params = fake.last_call
        assert method == "Extensions.loadUnpacked"
        assert params is not None
        assert params["path"] == "/path/to/extension"
        assert params["enableInIncognito"] is False

    async def test_load_unpacked_with_enable_in_incognito(self) -> None:
        fake = FakeSender({"id": "ext123"})
        domain = ExtensionsDomain(fake)
        await domain.load_unpacked("/path/to/extension", enable_in_incognito=True)
        method, params = fake.last_call
        assert params is not None
        assert params["enableInIncognito"] is True

    async def test_get_storage_items(self) -> None:
        fake = FakeSender({"data": {"key": "value"}})
        domain = ExtensionsDomain(fake)
        await domain.get_storage_items("ext123", "local")
        assert fake.last_call == (
            "Extensions.getStorageItems",
            {"id": "ext123", "storageArea": "local"},
        )

    async def test_get_storage_items_with_keys(self) -> None:
        fake = FakeSender({"data": {"key": "value"}})
        domain = ExtensionsDomain(fake)
        await domain.get_storage_items("ext123", "local", keys=["key1"])
        method, params = fake.last_call
        assert method == "Extensions.getStorageItems"
        assert params is not None
        assert params["keys"] == ["key1"]

    async def test_remove_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.remove_storage_items("ext123", "sync", ["key1", "key2"])
        method, params = fake.last_call
        assert method == "Extensions.removeStorageItems"
        assert params is not None
        assert params["keys"] == ["key1", "key2"]
        assert params["storageArea"] == "sync"

    async def test_clear_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.clear_storage_items("ext123", "local")
        assert fake.last_call == (
            "Extensions.clearStorageItems",
            {"id": "ext123", "storageArea": "local"},
        )

    async def test_trigger_action(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.trigger_action("ext123", "tab456")
        assert fake.last_call == (
            "Extensions.triggerAction",
            {"id": "ext123", "targetId": "tab456"},
        )

    async def test_get_extensions(self) -> None:
        fake = FakeSender({"extensions": []})
        domain = ExtensionsDomain(fake)
        await domain.get_extensions()
        assert fake.last_call == ("Extensions.getExtensions", None)

    async def test_uninstall(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.uninstall("ext123")
        assert fake.last_call == (
            "Extensions.uninstall",
            {"id": "ext123"},
        )

    async def test_set_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.set_storage_items("ext123", "local", {"key": "val"})
        assert fake.last_call == (
            "Extensions.setStorageItems",
            {"id": "ext123", "storageArea": "local", "values": {"key": "val"}},
        )

    async def test_remove_storage_items_default_keys(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.remove_storage_items("ext123", "local")
        method, params = fake.last_call
        assert method == "Extensions.removeStorageItems"
        assert params is not None
        assert params["keys"] == []

    async def test_get_storage_items_omitempty_keys(self) -> None:
        fake = FakeSender({"data": {}})
        domain = ExtensionsDomain(fake)
        await domain.get_storage_items("ext123", "local")
        method, params = fake.last_call
        assert method == "Extensions.getStorageItems"
        assert params is not None
        assert "keys" not in params

    async def test_load_unpacked_return_value(self) -> None:
        fake = FakeSender({"id": "ext-abc"})
        domain = ExtensionsDomain(fake)
        result = await domain.load_unpacked("/path")
        assert result["id"] == "ext-abc"

    async def test_get_extensions_return_value(self) -> None:
        fake = FakeSender({"extensions": [{"id": "e1", "name": "Ext1"}]})
        domain = ExtensionsDomain(fake)
        result = await domain.get_extensions()
        assert isinstance(result["extensions"], list)

    async def test_get_storage_items_return_data(self) -> None:
        fake = FakeSender({"data": {"k": "v"}})
        domain = ExtensionsDomain(fake)
        result = await domain.get_storage_items("ext1", "local")
        assert "data" in result

    # --- TypeError edge cases ---

    async def test_type_error_load_unpacked_path_int(self) -> None:
        fake = FakeSender({"id": "ext"})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="path must be a str"):
            await domain.load_unpacked(42)

    async def test_type_error_load_unpacked_enable_in_incognito_int(self) -> None:
        fake = FakeSender({"id": "ext"})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="enable_in_incognito must be a bool"):
            await domain.load_unpacked("/path", enable_in_incognito=1)

    async def test_type_error_trigger_action_id_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.trigger_action(42, "tab1")

    async def test_type_error_trigger_action_target_id_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="target_id must be a str"):
            await domain.trigger_action("ext1", 42)

    async def test_type_error_uninstall_id_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.uninstall(42)

    async def test_type_error_uninstall_id_bytes(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.uninstall(b"ext1")

    async def test_type_error_get_storage_items_id_int(self) -> None:
        fake = FakeSender({"data": {}})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.get_storage_items(42, "local")

    async def test_type_error_get_storage_items_storage_area_int(self) -> None:
        fake = FakeSender({"data": {}})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="storage_area must be a str"):
            await domain.get_storage_items("ext1", 42)

    async def test_type_error_get_storage_items_keys_str(self) -> None:
        fake = FakeSender({"data": {}})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="keys must be a list"):
            await domain.get_storage_items("ext1", "local", keys="key1")

    async def test_type_error_get_storage_items_keys_element_int(self) -> None:
        fake = FakeSender({"data": {}})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match=r"keys\[0\] must be a str"):
            await domain.get_storage_items("ext1", "local", keys=[42])

    async def test_type_error_remove_storage_items_id_bool(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.remove_storage_items(True, "local", ["k"])

    async def test_type_error_remove_storage_keys_not_list(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="keys must be a list"):
            await domain.remove_storage_items("ext1", "local", keys="key1")

    async def test_type_error_clear_storage_items_id_set(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.clear_storage_items({"ext1"}, "local")

    async def test_type_error_clear_storage_items_area_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="storage_area must be a str"):
            await domain.clear_storage_items("ext1", 42)

    async def test_type_error_remove_storage_items_storage_area_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="storage_area must be a str"):
            await domain.remove_storage_items("ext1", 42, ["k"])

    async def test_type_error_remove_storage_items_keys_element_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match=r"keys\[0\] must be a str"):
            await domain.remove_storage_items("ext1", "local", keys=[42])

    async def test_type_error_set_storage_items_id_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.set_storage_items(42, "local", {"k": "v"})

    async def test_type_error_set_storage_items_storage_area_int(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="storage_area must be a str"):
            await domain.set_storage_items("ext1", 42, {"k": "v"})

    async def test_type_error_set_storage_items_values_list(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="values must be a dict"):
            await domain.set_storage_items("ext1", "local", ["not", "dict"])

    async def test_type_error_set_storage_items_values_str(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        with pytest.raises(TypeError, match="values must be a dict"):
            await domain.set_storage_items("ext1", "local", "not a dict")


@pytest.mark.unit
class TestPWADomain:
    async def test_install(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest123")
        assert fake.last_call == (
            "PWA.install",
            {"manifestId": "manifest123"},
        )

    async def test_install_with_url(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest123", "https://example.com/app")
        method, params = fake.last_call
        assert method == "PWA.install"
        assert params is not None
        assert params["installUrlOrBundleUrl"] == "https://example.com/app"

    async def test_uninstall(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.uninstall("manifest123")
        assert fake.last_call == (
            "PWA.uninstall",
            {"manifestId": "manifest123"},
        )

    async def test_get_os_app_state(self) -> None:
        fake = FakeSender({"isAppInstalled": True})
        domain = PWADomain(fake)
        await domain.get_os_app_state("manifest123")
        assert fake.last_call == (
            "PWA.getOsAppState",
            {"manifestId": "manifest123"},
        )


@pytest.mark.unit
class TestWorkerDomain:
    def test_worker_domain_exists(self) -> None:
        fake = FakeSender({})
        domain = WorkerDomain(fake)
        assert domain is not None


@pytest.mark.unit
class TestInspectorDomain:
    def test_inspector_domain_exists(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        assert domain is not None

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.disable()
        assert fake.last_call == (
            "Inspector.disable",
            None,
        )

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = InspectorDomain(fake)
        await domain.enable()
        assert fake.last_call == (
            "Inspector.enable",
            None,
        )
