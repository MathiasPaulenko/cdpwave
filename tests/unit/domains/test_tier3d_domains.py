"""Unit tests for ServiceWorker, SystemInfo, WebAuthn, and IO domains."""

import pytest

from cdpwave.domains.io import IODomain
from cdpwave.domains.service_worker import ServiceWorkerDomain
from cdpwave.domains.system_info import SystemInfoDomain
from cdpwave.domains.web_authn import WebAuthnDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestServiceWorkerDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.enable()
        assert fake.last_call == ("ServiceWorker.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.disable()
        assert fake.last_call == ("ServiceWorker.disable", None)

    async def test_start_worker(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.start_worker("https://example.com/sw")
        assert fake.last_call == (
            "ServiceWorker.startWorker",
            {"scopeURL": "https://example.com/sw"},
        )

    async def test_stop_worker(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.stop_worker("123")
        assert fake.last_call == (
            "ServiceWorker.stopWorker",
            {"versionId": "123"},
        )

    async def test_unregister(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.unregister("https://example.com/sw")
        assert fake.last_call == (
            "ServiceWorker.unregister",
            {"scopeURL": "https://example.com/sw"},
        )

    async def test_deliver_push_message(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.deliver_push_message(
            "https://example.com", "reg1", "data123"
        )
        method, params = fake.last_call
        assert method == "ServiceWorker.deliverPushMessage"
        assert params is not None
        assert params["origin"] == "https://example.com"
        assert params["registrationId"] == "reg1"
        assert params["data"] == "data123"

    async def test_dispatch_sync_event(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.dispatch_sync_event(
            "https://example.com", "reg1", "sync-tag", False
        )
        method, params = fake.last_call
        assert method == "ServiceWorker.dispatchSyncEvent"
        assert params is not None
        assert params["origin"] == "https://example.com"
        assert params["registrationId"] == "reg1"
        assert params["tag"] == "sync-tag"
        assert params["lastChance"] is False

    async def test_dispatch_sync_event_last_chance(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.dispatch_sync_event(
            "https://example.com", "reg1", "sync-tag", True
        )
        method, params = fake.last_call
        assert params is not None
        assert params["lastChance"] is True

    async def test_skip_waiting(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.skip_waiting("https://example.com/sw")
        assert fake.last_call == (
            "ServiceWorker.skipWaiting",
            {"scopeURL": "https://example.com/sw"},
        )

    async def test_inspect_worker(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.inspect_worker("123")
        assert fake.last_call == (
            "ServiceWorker.inspectWorker",
            {"versionId": "123"},
        )

    async def test_update(self) -> None:
        fake = FakeSender({})
        domain = ServiceWorkerDomain(fake)
        await domain.update("https://example.com/sw")
        assert fake.last_call == (
            "ServiceWorker.updateRegistration",
            {"scopeURL": "https://example.com/sw"},
        )

    async def test_get_messages(self) -> None:
        fake = FakeSender({"messages": []})
        domain = ServiceWorkerDomain(fake)
        await domain.get_messages()
        assert fake.last_call == ("ServiceWorker.getMessages", None)


@pytest.mark.unit
class TestSystemInfoDomain:
    async def test_get_info(self) -> None:
        fake = FakeSender({"gpu": {}, "modelName": "Test"})
        domain = SystemInfoDomain(fake)
        result = await domain.get_info()
        assert fake.last_call == ("SystemInfo.getInfo", None)
        assert "modelName" in result

    async def test_get_process_info(self) -> None:
        fake = FakeSender({"processInfo": []})
        domain = SystemInfoDomain(fake)
        await domain.get_process_info()
        assert fake.last_call == ("SystemInfo.getProcessInfo", None)

    async def test_get_feature_state(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        await domain.get_feature_state("Vulkan")
        assert fake.last_call == (
            "SystemInfo.getFeatureState",
            {"featureState": "Vulkan"},
        )

    async def test_get_info_return_value(self) -> None:
        fake = FakeSender({
            "gpu": {"devices": []},
            "modelName": "TestModel",
            "modelVersion": "1.0",
            "commandLine": "--test",
        })
        domain = SystemInfoDomain(fake)
        result = await domain.get_info()
        assert result["modelName"] == "TestModel"
        assert result["modelVersion"] == "1.0"
        assert "commandLine" in result

    async def test_get_process_info_return_value(self) -> None:
        fake = FakeSender({"processInfo": [{"type": "browser", "id": 1}]})
        domain = SystemInfoDomain(fake)
        result = await domain.get_process_info()
        assert isinstance(result["processInfo"], list)

    async def test_get_feature_state_return_value(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        result = await domain.get_feature_state("Vulkan")
        assert result["featureEnabled"] is True

    async def test_get_feature_state_disabled(self) -> None:
        fake = FakeSender({"featureEnabled": False})
        domain = SystemInfoDomain(fake)
        result = await domain.get_feature_state("SomeFeature")
        assert result["featureEnabled"] is False

    # --- TypeError edge cases ---

    async def test_type_error_get_feature_state_int(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        with pytest.raises(TypeError, match="feature_state must be a str"):
            await domain.get_feature_state(42)

    async def test_type_error_get_feature_state_bytes(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        with pytest.raises(TypeError, match="feature_state must be a str"):
            await domain.get_feature_state(b"Vulkan")

    async def test_type_error_get_feature_state_bool(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        with pytest.raises(TypeError, match="feature_state must be a str"):
            await domain.get_feature_state(True)

    async def test_type_error_get_feature_state_none(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        with pytest.raises(TypeError, match="feature_state must be a str"):
            await domain.get_feature_state(None)  # type: ignore[arg-type]

    async def test_type_error_get_feature_state_list(self) -> None:
        fake = FakeSender({"featureEnabled": True})
        domain = SystemInfoDomain(fake)
        with pytest.raises(TypeError, match="feature_state must be a str"):
            await domain.get_feature_state(["Vulkan"])  # type: ignore[arg-type]


@pytest.mark.unit
class TestWebAuthnDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        assert fake.last_call == ("WebAuthn.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.disable()
        assert fake.last_call == ("WebAuthn.disable", None)

    async def test_add_virtual_authenticator(self) -> None:
        fake = FakeSender({"authenticatorId": "auth1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "usb")
        method, params = fake.last_call
        assert method == "WebAuthn.addVirtualAuthenticator"
        assert params is not None
        assert params["options"]["protocol"] == "ctap2"

    async def test_remove_virtual_authenticator(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_virtual_authenticator("auth1")
        assert fake.last_call == (
            "WebAuthn.removeVirtualAuthenticator",
            {"authenticatorId": "auth1"},
        )

    async def test_add_credential(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth1", {
            "credentialId": "cred1",
            "isResidentCredential": False,
            "privateKey": "key1",
        })
        method, params = fake.last_call
        assert method == "WebAuthn.addCredential"
        assert params is not None
        assert params["authenticatorId"] == "auth1"
        assert params["credential"]["credentialId"] == "cred1"

    async def test_get_credentials(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.get_credentials("auth1")
        assert fake.last_call == (
            "WebAuthn.getCredentials",
            {"authenticatorId": "auth1"},
        )

    async def test_get_credential(self) -> None:
        fake = FakeSender({"credential": {}})
        domain = WebAuthnDomain(fake)
        await domain.get_credential("auth1", "cred1")
        assert fake.last_call == (
            "WebAuthn.getCredential",
            {"authenticatorId": "auth1", "credentialId": "cred1"},
        )

    async def test_remove_credential(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_credential("auth1", "cred1")
        assert fake.last_call == (
            "WebAuthn.removeCredential",
            {"authenticatorId": "auth1", "credentialId": "cred1"},
        )

    async def test_clear_credentials(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.clear_credentials("auth1")
        assert fake.last_call == (
            "WebAuthn.clearCredentials",
            {"authenticatorId": "auth1"},
        )

    async def test_set_user_verified(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth1", True)
        method, params = fake.last_call
        assert method == "WebAuthn.setUserVerified"
        assert params is not None
        assert params["authenticatorId"] == "auth1"
        assert params["isUserVerified"] is True

    async def test_set_automatic_presence_simulation(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_automatic_presence_simulation("auth1", True)
        method, params = fake.last_call
        assert method == "WebAuthn.setAutomaticPresenceSimulation"
        assert params is not None
        assert params["authenticatorId"] == "auth1"
        assert params["enabled"] is True


@pytest.mark.unit
class TestIODomain:
    async def test_read(self) -> None:
        fake = FakeSender({"data": "abc", "eof": True, "base64Encoded": False})
        domain = IODomain(fake)
        await domain.read("handle1")
        assert fake.last_call == ("IO.read", {"handle": "handle1"})

    async def test_read_with_offset_size(self) -> None:
        fake = FakeSender({"data": "abc", "eof": False})
        domain = IODomain(fake)
        await domain.read("handle1", offset=10, size=1024)
        method, params = fake.last_call
        assert method == "IO.read"
        assert params is not None
        assert params["handle"] == "handle1"
        assert params["offset"] == 10
        assert params["size"] == 1024

    async def test_close(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain.close("handle1")
        assert fake.last_call == ("IO.close", {"handle": "handle1"})

    async def test_resolve_blob(self) -> None:
        fake = FakeSender({"uuid": "blob-uuid-123"})
        domain = IODomain(fake)
        await domain.resolve_blob("obj1")
        assert fake.last_call == ("IO.resolveBlob", {"objectId": "obj1"})
