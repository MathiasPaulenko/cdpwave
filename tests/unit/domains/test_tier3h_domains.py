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

    async def test_load_unpacked_with_file_access(self) -> None:
        fake = FakeSender({"id": "ext123"})
        domain = ExtensionsDomain(fake)
        await domain.load_unpacked("/path/to/extension", allow_file_access=True)
        method, params = fake.last_call
        assert params is not None
        assert params["allowFileAccess"] is True

    async def test_get_storage_items(self) -> None:
        fake = FakeSender({"items": {"key": "value"}})
        domain = ExtensionsDomain(fake)
        await domain.get_storage_items("ext123", "local")
        assert fake.last_call == (
            "Extensions.getStorageItems",
            {"id": "ext123", "storageType": "local"},
        )

    async def test_remove_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.remove_storage_items("ext123", "sync", ["key1", "key2"])
        method, params = fake.last_call
        assert method == "Extensions.removeStorageItems"
        assert params is not None
        assert params["keys"] == ["key1", "key2"]

    async def test_clear_storage_items(self) -> None:
        fake = FakeSender({})
        domain = ExtensionsDomain(fake)
        await domain.clear_storage_items("ext123", "local")
        assert fake.last_call == (
            "Extensions.clearStorageItems",
            {"id": "ext123", "storageType": "local"},
        )


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
