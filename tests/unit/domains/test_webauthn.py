"""Unit tests for the WebAuthn domain.

Covers all 13 CDP WebAuthn commands (enable, disable,
addVirtualAuthenticator, removeVirtualAuthenticator, addCredential,
getCredential, getCredentials, removeCredential, clearCredentials,
setUserVerified, setAutomaticPresenceSimulation,
setCredentialProperties, setResponseOverrideBits) with FakeSender —
parameter verification, type/enum validation, return values,
CommandError propagation, method parity, coroutine checks,
concurrency, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.web_authn import WebAuthnDomain
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
# add_credential
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddCredential:
    async def test_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        cred = {"credentialId": "cred1", "isResidentCredential": True}
        await domain.add_credential("auth-1", cred)
        method, params = fake.last_call
        assert method == "WebAuthn.addCredential"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["credential"] == cred

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.add_credential("auth-1", {})
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = WebAuthnDomain(fake)
        result = await domain.add_credential("auth-1", {})
        assert result == {"ok": True}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth-1", {})
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth-1", {})
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "credential"}

    async def test_camel_case_keys(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth-1", {})
        _, params = fake.last_call
        assert params is not None
        assert "authenticatorId" in params
        assert "credential" in params

    async def test_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth-1", {})
        first = fake.calls[0][1]
        await domain.add_credential("auth-1", {})
        second = fake.calls[1][1]
        assert first is not None
        assert second is not None
        assert first is not second


# ---------------------------------------------------------------------------
# add_virtual_authenticator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddVirtualAuthenticator:
    async def test_params_minimal(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "internal")
        method, params = fake.last_call
        assert method == "WebAuthn.addVirtualAuthenticator"
        assert params is not None
        assert "options" in params
        opts = params["options"]
        assert opts["protocol"] == "ctap2"
        assert opts["transport"] == "internal"
        assert opts["hasResidentKey"] is False
        assert opts["hasUserVerification"] is False
        assert "ctap2Version" not in opts

    async def test_params_full(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator(
            "ctap2",
            "usb",
            has_resident_key=True,
            has_user_verification=True,
            has_large_blob=True,
            has_cred_blob=True,
            has_min_pin_length=True,
            has_prf=True,
            has_hmac_secret=True,
            has_hmac_secret_mc=True,
            automatic_presence_simulation=True,
            is_user_verified=True,
            default_backup_eligibility=True,
            default_backup_state=True,
            ctap2_version="ctap2_1",
        )
        _, params = fake.last_call
        assert params is not None
        opts = params["options"]
        assert opts["protocol"] == "ctap2"
        assert opts["transport"] == "usb"
        assert opts["hasResidentKey"] is True
        assert opts["hasUserVerification"] is True
        assert opts["hasLargeBlob"] is True
        assert opts["hasCredBlob"] is True
        assert opts["hasMinPinLength"] is True
        assert opts["hasPrf"] is True
        assert opts["hasHmacSecret"] is True
        assert opts["hasHmacSecretMc"] is True
        assert opts["automaticPresenceSimulation"] is True
        assert opts["isUserVerified"] is True
        assert opts["defaultBackupEligibility"] is True
        assert opts["defaultBackupState"] is True
        assert opts["ctap2Version"] == "ctap2_1"

    async def test_ctap2_version_none_not_sent(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("u2f", "usb")
        _, params = fake.last_call
        assert params is not None
        assert "ctap2Version" not in params["options"]

    async def test_returns_authenticator_id(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        result = await domain.add_virtual_authenticator("ctap2", "internal")
        assert result == {"authenticatorId": "auth-1"}

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.add_virtual_authenticator("ctap2", "internal")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "internal")
        assert len(fake.calls) == 1

    async def test_only_options_key(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "internal")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["options"]

    async def test_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "internal")
        first = fake.calls[0][1]
        await domain.add_virtual_authenticator("ctap2", "internal")
        second = fake.calls[1][1]
        assert first is not None
        assert second is not None
        assert first is not second


# ---------------------------------------------------------------------------
# clear_credentials
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestClearCredentials:
    async def test_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.clear_credentials("auth-1")
        method, params = fake.last_call
        assert method == "WebAuthn.clearCredentials"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.clear_credentials("auth-1")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.clear_credentials("auth-1")
        assert len(fake.calls) == 1

    async def test_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.clear_credentials("auth-1")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["authenticatorId"]


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.disable()
        assert fake.last_call == ("WebAuthn.disable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = WebAuthnDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_params_default_none(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "WebAuthn.enable"
        assert params is None

    async def test_params_enable_ui_true(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable(enable_ui=True)
        _, params = fake.last_call
        assert params is not None
        assert params["enableUI"] is True

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = WebAuthnDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1

    async def test_only_key_when_specified(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable(enable_ui=True)
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["enableUI"]


# ---------------------------------------------------------------------------
# get_credential
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetCredential:
    async def test_params(self) -> None:
        fake = FakeSender({"credential": {}})
        domain = WebAuthnDomain(fake)
        await domain.get_credential("auth-1", "cred-1")
        method, params = fake.last_call
        assert method == "WebAuthn.getCredential"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["credentialId"] == "cred-1"

    async def test_returns_credential(self) -> None:
        fake = FakeSender({"credential": {"credentialId": "cred-1"}})
        domain = WebAuthnDomain(fake)
        result = await domain.get_credential("auth-1", "cred-1")
        assert "credential" in result
        assert result["credential"]["credentialId"] == "cred-1"

    async def test_single_call(self) -> None:
        fake = FakeSender({"credential": {}})
        domain = WebAuthnDomain(fake)
        await domain.get_credential("auth-1", "cred-1")
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({"credential": {}})
        domain = WebAuthnDomain(fake)
        await domain.get_credential("auth-1", "cred-1")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "credentialId"}


# ---------------------------------------------------------------------------
# get_credentials
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetCredentials:
    async def test_params(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.get_credentials("auth-1")
        method, params = fake.last_call
        assert method == "WebAuthn.getCredentials"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"

    async def test_returns_credentials(self) -> None:
        fake = FakeSender({"credentials": [{"credentialId": "c1"}]})
        domain = WebAuthnDomain(fake)
        result = await domain.get_credentials("auth-1")
        assert "credentials" in result
        assert len(result["credentials"]) == 1

    async def test_returns_empty_list(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        result = await domain.get_credentials("auth-1")
        assert result["credentials"] == []

    async def test_single_call(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.get_credentials("auth-1")
        assert len(fake.calls) == 1

    async def test_only_key_in_params(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.get_credentials("auth-1")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["authenticatorId"]


# ---------------------------------------------------------------------------
# remove_credential
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRemoveCredential:
    async def test_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_credential("auth-1", "cred-1")
        method, params = fake.last_call
        assert method == "WebAuthn.removeCredential"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["credentialId"] == "cred-1"

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.remove_credential("auth-1", "cred-1")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_credential("auth-1", "cred-1")
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_credential("auth-1", "cred-1")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "credentialId"}


# ---------------------------------------------------------------------------
# remove_virtual_authenticator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRemoveVirtualAuthenticator:
    async def test_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_virtual_authenticator("auth-1")
        method, params = fake.last_call
        assert method == "WebAuthn.removeVirtualAuthenticator"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.remove_virtual_authenticator("auth-1")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_virtual_authenticator("auth-1")
        assert len(fake.calls) == 1

    async def test_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_virtual_authenticator("auth-1")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["authenticatorId"]


# ---------------------------------------------------------------------------
# set_automatic_presence_simulation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetAutomaticPresenceSimulation:
    async def test_params_true(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_automatic_presence_simulation("auth-1", True)
        method, params = fake.last_call
        assert method == "WebAuthn.setAutomaticPresenceSimulation"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["enabled"] is True

    async def test_params_false(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_automatic_presence_simulation("auth-1", False)
        _, params = fake.last_call
        assert params is not None
        assert params["enabled"] is False

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.set_automatic_presence_simulation("auth-1", True)
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_automatic_presence_simulation("auth-1", True)
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_automatic_presence_simulation("auth-1", True)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "enabled"}


# ---------------------------------------------------------------------------
# set_credential_properties
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetCredentialProperties:
    async def test_params_default(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties("auth-1", "cred-1")
        method, params = fake.last_call
        assert method == "WebAuthn.setCredentialProperties"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["credentialId"] == "cred-1"
        assert "backupEligibility" not in params
        assert "backupState" not in params

    async def test_params_full(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties(
            "auth-1", "cred-1", backup_eligibility=True, backup_state=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["backupEligibility"] is True
        assert params["backupState"] is True

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.set_credential_properties("auth-1", "cred-1")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties("auth-1", "cred-1")
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties("auth-1", "cred-1")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "credentialId"}


# ---------------------------------------------------------------------------
# set_response_override_bits
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetResponseOverrideBits:
    async def test_params_default(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits("auth-1")
        method, params = fake.last_call
        assert method == "WebAuthn.setResponseOverrideBits"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert "isBogusSignature" not in params
        assert "isBadUV" not in params
        assert "isBadUP" not in params

    async def test_params_full(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1", is_bogus_signature=True, is_bad_uv=True, is_bad_up=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["isBogusSignature"] is True
        assert params["isBadUV"] is True
        assert params["isBadUP"] is True

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.set_response_override_bits("auth-1")
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits("auth-1")
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits("auth-1")
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["authenticatorId"]


# ---------------------------------------------------------------------------
# set_user_verified
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetUserVerified:
    async def test_params_true(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth-1", True)
        method, params = fake.last_call
        assert method == "WebAuthn.setUserVerified"
        assert params is not None
        assert params["authenticatorId"] == "auth-1"
        assert params["isUserVerified"] is True

    async def test_params_false(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth-1", False)
        _, params = fake.last_call
        assert params is not None
        assert params["isUserVerified"] is False

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        result = await domain.set_user_verified("auth-1", True)
        assert result == {}

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth-1", True)
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth-1", True)
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"authenticatorId", "isUserVerified"}


# ---------------------------------------------------------------------------
# Type validation — authenticator_id (shared across methods)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAuthenticatorIdTypeValidation:
    async def test_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.remove_virtual_authenticator(123)
        assert len(fake.calls) == 0

    async def test_none_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.clear_credentials(None)
        assert len(fake.calls) == 0

    async def test_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.get_credentials(True)
        assert len(fake.calls) == 0

    async def test_list_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.set_user_verified([], True)
        assert len(fake.calls) == 0

    async def test_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.set_automatic_presence_simulation({}, True)
        assert len(fake.calls) == 0

    async def test_float_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.remove_virtual_authenticator(1.5)
        assert len(fake.calls) == 0

    async def test_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.clear_credentials(b"auth-1")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — credential_id
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCredentialIdTypeValidation:
    async def test_int_raises(self) -> None:
        fake = FakeSender({"credential": {}})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential_id must be a string"):
            await domain.get_credential("auth-1", 123)
        assert len(fake.calls) == 0

    async def test_none_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential_id must be a string"):
            await domain.remove_credential("auth-1", None)
        assert len(fake.calls) == 0

    async def test_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential_id must be a string"):
            await domain.set_credential_properties("auth-1", True)
        assert len(fake.calls) == 0

    async def test_list_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential_id must be a string"):
            await domain.remove_credential("auth-1", ["cred-1"])
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — bool params
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestBoolTypeValidation:
    async def test_set_user_verified_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_user_verified must be a bool"):
            await domain.set_user_verified("auth-1", 1)
        assert len(fake.calls) == 0

    async def test_set_user_verified_str_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_user_verified must be a bool"):
            await domain.set_user_verified("auth-1", "true")
        assert len(fake.calls) == 0

    async def test_set_user_verified_none_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_user_verified must be a bool"):
            await domain.set_user_verified("auth-1", None)
        assert len(fake.calls) == 0

    async def test_set_presence_sim_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="enabled must be a bool"):
            await domain.set_automatic_presence_simulation("auth-1", 1)
        assert len(fake.calls) == 0

    async def test_enable_ui_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="enable_ui must be a bool or None"):
            await domain.enable(enable_ui=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_enable_ui_str_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="enable_ui must be a bool or None"):
            await domain.enable(enable_ui="true")  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_backup_eligibility_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="backup_eligibility must be a bool or None"):
            await domain.set_credential_properties("auth-1", "cred-1", backup_eligibility=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_backup_state_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="backup_state must be a bool or None"):
            await domain.set_credential_properties("auth-1", "cred-1", backup_state=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_is_bogus_signature_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_bogus_signature must be a bool or None"):
            await domain.set_response_override_bits("auth-1", is_bogus_signature=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_is_bad_uv_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_bad_uv must be a bool or None"):
            await domain.set_response_override_bits("auth-1", is_bad_uv=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_is_bad_up_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_bad_up must be a bool or None"):
            await domain.set_response_override_bits("auth-1", is_bad_up=1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — add_credential credential param
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddCredentialCredentialTypeValidation:
    async def test_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential must be a dict"):
            await domain.add_credential("auth-1", 123)
        assert len(fake.calls) == 0

    async def test_str_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential must be a dict"):
            await domain.add_credential("auth-1", "cred")
        assert len(fake.calls) == 0

    async def test_list_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential must be a dict"):
            await domain.add_credential("auth-1", [])
        assert len(fake.calls) == 0

    async def test_none_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential must be a dict"):
            await domain.add_credential("auth-1", None)  # type: ignore[arg-type]
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — add_virtual_authenticator bool params
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddVirtualAuthenticatorBoolValidation:
    async def test_has_resident_key_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_resident_key must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_resident_key=1)
        assert len(fake.calls) == 0

    async def test_has_user_verification_str_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_user_verification must be a bool"):
            await domain.add_virtual_authenticator(
                "ctap2", "internal", has_user_verification="true",
            )
        assert len(fake.calls) == 0

    async def test_automatic_presence_simulation_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="automatic_presence_simulation must be a bool"):
            await domain.add_virtual_authenticator(
                "ctap2", "internal", automatic_presence_simulation=1,
            )
        assert len(fake.calls) == 0

    async def test_is_user_verified_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="is_user_verified must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", is_user_verified=1)
        assert len(fake.calls) == 0

    async def test_default_backup_eligibility_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="default_backup_eligibility must be a bool"):
            await domain.add_virtual_authenticator(
                "ctap2", "internal", default_backup_eligibility=1,
            )
        assert len(fake.calls) == 0

    async def test_default_backup_state_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="default_backup_state must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", default_backup_state=1)
        assert len(fake.calls) == 0

    async def test_has_large_blob_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_large_blob must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_large_blob=1)
        assert len(fake.calls) == 0

    async def test_has_cred_blob_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_cred_blob must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_cred_blob=1)
        assert len(fake.calls) == 0

    async def test_has_min_pin_length_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_min_pin_length must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_min_pin_length=1)
        assert len(fake.calls) == 0

    async def test_has_prf_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_prf must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_prf=1)
        assert len(fake.calls) == 0

    async def test_has_hmac_secret_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_hmac_secret must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_hmac_secret=1)
        assert len(fake.calls) == 0

    async def test_has_hmac_secret_mc_int_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="has_hmac_secret_mc must be a bool"):
            await domain.add_virtual_authenticator("ctap2", "internal", has_hmac_secret_mc=1)
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Enum validation — protocol
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProtocolEnumValidation:
    async def test_u2f_valid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("u2f", "usb")
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["protocol"] == "u2f"

    async def test_ctap2_valid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "usb")
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["protocol"] == "ctap2"

    async def test_empty_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="protocol must be 'u2f' or 'ctap2'"):
            await domain.add_virtual_authenticator("", "usb")
        assert len(fake.calls) == 0

    async def test_uppercase_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="protocol must be 'u2f' or 'ctap2'"):
            await domain.add_virtual_authenticator("U2F", "usb")
        assert len(fake.calls) == 0

    async def test_random_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="protocol must be 'u2f' or 'ctap2'"):
            await domain.add_virtual_authenticator("ctap1", "usb")
        assert len(fake.calls) == 0

    async def test_int_raises_type_error_before_value_error(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a string"):
            await domain.add_virtual_authenticator(123, "usb")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Enum validation — transport
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTransportEnumValidation:
    async def test_all_valid_transports(self) -> None:
        for t in ("usb", "nfc", "ble", "cable", "internal"):
            fake = FakeSender({})
            domain = WebAuthnDomain(fake)
            await domain.add_virtual_authenticator("ctap2", t)
            _, params = fake.last_call
            assert params is not None
            assert params["options"]["transport"] == t

    async def test_empty_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="transport must be"):
            await domain.add_virtual_authenticator("ctap2", "")
        assert len(fake.calls) == 0

    async def test_uppercase_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="transport must be"):
            await domain.add_virtual_authenticator("ctap2", "USB")
        assert len(fake.calls) == 0

    async def test_random_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="transport must be"):
            await domain.add_virtual_authenticator("ctap2", "wifi")
        assert len(fake.calls) == 0

    async def test_int_raises_type_error_before_value_error(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="transport must be a string"):
            await domain.add_virtual_authenticator("ctap2", 123)
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Enum validation — ctap2_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCtap2VersionEnumValidation:
    async def test_ctap2_0_valid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="ctap2_0")
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["ctap2Version"] == "ctap2_0"

    async def test_ctap2_1_valid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="ctap2_1")
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["ctap2Version"] == "ctap2_1"

    async def test_ctap2_2_valid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="ctap2_2")
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["ctap2Version"] == "ctap2_2"

    async def test_empty_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="ctap2_version must be"):
            await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="")
        assert len(fake.calls) == 0

    async def test_uppercase_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="ctap2_version must be"):
            await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="CTAP2_0")
        assert len(fake.calls) == 0

    async def test_random_string_raises(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="ctap2_version must be"):
            await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version="ctap3_0")
        assert len(fake.calls) == 0

    async def test_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="ctap2_version must be a string or None"):
            await domain.add_virtual_authenticator("ctap2", "usb", ctap2_version=123)
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Method parity
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    _EXPECTED = {
        "add_credential",
        "add_virtual_authenticator",
        "clear_credentials",
        "disable",
        "enable",
        "get_credential",
        "get_credentials",
        "remove_credential",
        "remove_virtual_authenticator",
        "set_automatic_presence_simulation",
        "set_credential_properties",
        "set_response_override_bits",
        "set_user_verified",
    }

    def test_thirteen_methods_exist(self) -> None:
        methods = {
            attr for attr in dir(WebAuthnDomain)
            if not attr.startswith("_") and callable(getattr(WebAuthnDomain, attr))
        }
        domain_methods = methods - set(dir(BaseDomain))
        assert domain_methods == self._EXPECTED

    def test_no_extra_methods(self) -> None:
        actual = {
            attr for attr in dir(WebAuthnDomain)
            if not attr.startswith("_")
            and callable(getattr(WebAuthnDomain, attr))
        }
        domain_methods = actual - set(dir(BaseDomain))
        assert domain_methods == self._EXPECTED

    def test_all_coroutines(self) -> None:
        for name in self._EXPECTED:
            method = getattr(WebAuthnDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_isinstance_base_domain(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        assert isinstance(domain, BaseDomain)

    def test_alphabetical_order(self) -> None:
        methods = [
            name for name, value in WebAuthnDomain.__dict__.items()
            if not name.startswith("_")
            and inspect.iscoroutinefunction(value)
        ]
        assert methods == sorted(methods), f"Methods not in alphabetical order: {methods}"


# ---------------------------------------------------------------------------
# Method signatures
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodSignatures:
    def test_disable_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.disable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_enable_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.enable)
        params = list(sig.parameters.keys())
        assert params == ["self", "enable_ui"]
        assert sig.parameters["enable_ui"].annotation == bool | None
        assert sig.parameters["enable_ui"].default is None
        assert sig.return_annotation == dict[str, Any]

    def test_add_credential_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.add_credential)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id", "credential"]
        assert sig.parameters["authenticator_id"].annotation is str
        assert sig.return_annotation == dict[str, Any]

    def test_add_virtual_authenticator_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.add_virtual_authenticator)
        params = list(sig.parameters.keys())
        assert params[0] == "self"
        assert params[1] == "protocol"
        assert params[2] == "transport"
        assert sig.parameters["protocol"].annotation is str
        assert sig.parameters["transport"].annotation is str
        assert sig.parameters["ctap2_version"].annotation == str | None
        assert sig.return_annotation == dict[str, Any]

    def test_clear_credentials_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.clear_credentials)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id"]
        assert sig.parameters["authenticator_id"].annotation is str
        assert sig.return_annotation == dict[str, Any]

    def test_get_credential_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.get_credential)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id", "credential_id"]
        assert sig.return_annotation == dict[str, Any]

    def test_get_credentials_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.get_credentials)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id"]
        assert sig.return_annotation == dict[str, Any]

    def test_remove_credential_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.remove_credential)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id", "credential_id"]
        assert sig.return_annotation == dict[str, Any]

    def test_remove_virtual_authenticator_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.remove_virtual_authenticator)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id"]
        assert sig.return_annotation == dict[str, Any]

    def test_set_automatic_presence_simulation_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.set_automatic_presence_simulation)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id", "enabled"]
        assert sig.parameters["enabled"].annotation is bool
        assert sig.return_annotation == dict[str, Any]

    def test_set_credential_properties_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.set_credential_properties)
        params = list(sig.parameters.keys())
        assert params == [
            "self", "authenticator_id", "credential_id",
            "backup_eligibility", "backup_state",
        ]
        assert sig.parameters["backup_eligibility"].annotation == bool | None
        assert sig.parameters["backup_state"].annotation == bool | None
        assert sig.parameters["backup_eligibility"].default is None
        assert sig.parameters["backup_state"].default is None
        assert sig.return_annotation == dict[str, Any]

    def test_set_response_override_bits_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.set_response_override_bits)
        params = list(sig.parameters.keys())
        assert params == [
            "self", "authenticator_id",
            "is_bogus_signature", "is_bad_uv", "is_bad_up",
        ]
        assert sig.parameters["is_bogus_signature"].annotation == bool | None
        assert sig.parameters["is_bad_uv"].annotation == bool | None
        assert sig.parameters["is_bad_up"].annotation == bool | None
        assert sig.parameters["is_bogus_signature"].default is None
        assert sig.parameters["is_bad_uv"].default is None
        assert sig.parameters["is_bad_up"].default is None
        assert sig.return_annotation == dict[str, Any]

    def test_set_user_verified_signature(self) -> None:
        sig = inspect.signature(WebAuthnDomain.set_user_verified)
        params = list(sig.parameters.keys())
        assert params == ["self", "authenticator_id", "is_user_verified"]
        assert sig.parameters["is_user_verified"].annotation is bool
        assert sig.return_annotation == dict[str, Any]

    def test_all_methods_have_docstrings(self) -> None:
        for name in (
            "add_credential", "add_virtual_authenticator", "clear_credentials",
            "disable", "enable", "get_credential", "get_credentials",
            "remove_credential", "remove_virtual_authenticator",
            "set_automatic_presence_simulation", "set_credential_properties",
            "set_response_override_bits", "set_user_verified",
        ):
            method = getattr(WebAuthnDomain, name)
            assert method.__doc__ is not None, f"{name} missing docstring"
            assert len(method.__doc__) > 10, f"{name} docstring too short"

    def test_class_has_docstring(self) -> None:
        assert WebAuthnDomain.__doc__ is not None
        assert "WebAuthn" in WebAuthnDomain.__doc__

    def test_module_has_docstring(self) -> None:
        import cdpwave.domains.web_authn as mod
        assert mod.__doc__ is not None
        assert "WebAuthn" in mod.__doc__

    def test_module_docstring_mentions_events(self) -> None:
        import cdpwave.domains.web_authn as mod
        doc = mod.__doc__ or ""
        assert "credentialAdded" in doc
        assert "credentialAsserted" in doc
        assert "credentialDeleted" in doc
        assert "credentialUpdated" in doc

    def test_class_docstring_mentions_events(self) -> None:
        doc = WebAuthnDomain.__doc__ or ""
        assert "credentialAdded" in doc
        assert "credentialAsserted" in doc
        assert "credentialDeleted" in doc
        assert "credentialUpdated" in doc


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagation:
    async def test_disable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Disable failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -32000
        assert "Disable failed" in exc_info.value.message

    async def test_enable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Enable failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == -32001

    async def test_add_virtual_authenticator_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32002, message="Add auth failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.add_virtual_authenticator("ctap2", "internal")
        assert exc_info.value.code == -32002

    async def test_add_credential_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32003, message="Add cred failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.add_credential("auth-1", {})

    async def test_get_credentials_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32004, message="Get creds failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.get_credentials("auth-1")

    async def test_set_user_verified_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32005, message="Set UV failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.set_user_verified("auth-1", True)

    async def test_set_credential_properties_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32006, message="Set cred props failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.set_credential_properties("auth-1", "cred-1")

    async def test_set_response_override_bits_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32007, message="Set override bits failed")
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.set_response_override_bits("auth-1")

    async def test_error_sender_records_call_before_raising(self) -> None:
        sender = ErrorSender()
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 1
        assert sender.calls[0][0] == "WebAuthn.disable"

    async def test_error_stops_execution(self) -> None:
        sender = ErrorSender()
        domain = WebAuthnDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 2


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_100_concurrent_disable(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(*[domain.disable() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_100_concurrent_enable(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(*[domain.enable() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_100_concurrent_add_virtual_authenticator(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(
            *[domain.add_virtual_authenticator("ctap2", "internal") for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_100_concurrent_set_user_verified(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(
            *[domain.set_user_verified("auth-1", True) for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_concurrent_mixed_methods(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.enable(),
            domain.add_virtual_authenticator("ctap2", "internal"),
            domain.add_credential("auth-1", {}),
            domain.get_credentials("auth-1"),
            domain.set_user_verified("auth-1", True),
            domain.set_automatic_presence_simulation("auth-1", True),
            domain.clear_credentials("auth-1"),
            domain.remove_virtual_authenticator("auth-1"),
            domain.remove_credential("auth-1", "cred-1"),
            domain.get_credential("auth-1", "cred-1"),
            domain.set_credential_properties("auth-1", "cred-1"),
            domain.set_response_override_bits("auth-1"),
        )
        assert len(fake.calls) == 13

    async def test_concurrent_50_enable_50_disable(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(
            *[domain.enable() for _ in range(50)],
            *[domain.disable() for _ in range(50)],
        )
        assert len(fake.calls) == 100


# ---------------------------------------------------------------------------
# Repetition
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRepetition:
    async def test_enable_disable_10x(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        for _ in range(10):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 20
        for i in range(10):
            assert fake.calls[i * 2][0] == "WebAuthn.enable"
            assert fake.calls[i * 2 + 1][0] == "WebAuthn.disable"

    async def test_repeated_enable_10x(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        for _ in range(10):
            await domain.enable()
        assert len(fake.calls) == 10

    async def test_repeated_add_virtual_authenticator_10x(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        for _ in range(10):
            await domain.add_virtual_authenticator("ctap2", "internal")
        assert len(fake.calls) == 10

    async def test_repeated_set_user_verified_10x(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        for _ in range(10):
            await domain.set_user_verified("auth-1", True)
        assert len(fake.calls) == 10


# ---------------------------------------------------------------------------
# Call sequences
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1", "credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        await domain.add_virtual_authenticator("ctap2", "internal")
        await domain.add_credential("auth-1", {})
        await domain.get_credentials("auth-1")
        await domain.get_credential("auth-1", "cred-1")
        await domain.set_user_verified("auth-1", True)
        await domain.set_automatic_presence_simulation("auth-1", True)
        await domain.set_credential_properties("auth-1", "cred-1")
        await domain.set_response_override_bits("auth-1")
        await domain.remove_credential("auth-1", "cred-1")
        await domain.clear_credentials("auth-1")
        await domain.remove_virtual_authenticator("auth-1")
        await domain.disable()
        assert len(fake.calls) == 13
        assert fake.calls[0][0] == "WebAuthn.enable"
        assert fake.calls[1][0] == "WebAuthn.addVirtualAuthenticator"
        assert fake.calls[2][0] == "WebAuthn.addCredential"
        assert fake.calls[3][0] == "WebAuthn.getCredentials"
        assert fake.calls[4][0] == "WebAuthn.getCredential"
        assert fake.calls[5][0] == "WebAuthn.setUserVerified"
        assert fake.calls[6][0] == "WebAuthn.setAutomaticPresenceSimulation"
        assert fake.calls[7][0] == "WebAuthn.setCredentialProperties"
        assert fake.calls[8][0] == "WebAuthn.setResponseOverrideBits"
        assert fake.calls[9][0] == "WebAuthn.removeCredential"
        assert fake.calls[10][0] == "WebAuthn.clearCredentials"
        assert fake.calls[11][0] == "WebAuthn.removeVirtualAuthenticator"
        assert fake.calls[12][0] == "WebAuthn.disable"

    async def test_all_methods_use_webauthn_prefix(self) -> None:
        fake = FakeSender({"credentials": []})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.add_virtual_authenticator("ctap2", "internal")
        await domain.add_credential("auth-1", {})
        await domain.get_credential("auth-1", "cred-1")
        await domain.get_credentials("auth-1")
        await domain.remove_credential("auth-1", "cred-1")
        await domain.remove_virtual_authenticator("auth-1")
        await domain.clear_credentials("auth-1")
        await domain.set_user_verified("auth-1", True)
        await domain.set_automatic_presence_simulation("auth-1", True)
        await domain.set_credential_properties("auth-1", "cred-1")
        await domain.set_response_override_bits("auth-1")
        for method, _ in fake.calls:
            assert method.startswith("WebAuthn.")


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        r1 = await domain.enable()
        assert r1 == {}
        fake.set_response({"ok": True})
        r2 = await domain.enable()
        assert r2 == {"ok": True}

    async def test_large_response_dict(self) -> None:
        large = {f"key{i}": i for i in range(100)}
        fake = FakeSender(large)
        domain = WebAuthnDomain(fake)
        result = await domain.get_credentials("auth-1")
        assert result == large

    async def test_exact_response_object(self) -> None:
        response = {"authenticatorId": "auth-1"}
        fake = FakeSender(response)
        domain = WebAuthnDomain(fake)
        result = await domain.add_virtual_authenticator("ctap2", "internal")
        assert result is response

    async def test_params_not_mutated_between_calls(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_user_verified("auth-1", True)
        await domain.set_user_verified("auth-2", False)
        assert fake.calls[0][1] == {"authenticatorId": "auth-1", "isUserVerified": True}
        assert fake.calls[1][1] == {"authenticatorId": "auth-2", "isUserVerified": False}

    async def test_empty_string_authenticator_id(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.clear_credentials("")
        _, params = fake.last_call
        assert params is not None
        assert params["authenticatorId"] == ""

    async def test_empty_string_credential_id(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.remove_credential("auth-1", "")
        _, params = fake.last_call
        assert params is not None
        assert params["credentialId"] == ""

    async def test_empty_credential_dict(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.add_credential("auth-1", {})
        _, params = fake.last_call
        assert params is not None
        assert params["credential"] == {}


# ---------------------------------------------------------------------------
# Validation order
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValidationOrder:
    async def test_authenticator_id_checked_before_bool(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.set_user_verified(123, "bad")
        assert len(fake.calls) == 0

    async def test_protocol_type_before_transport_type(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a string"):
            await domain.add_virtual_authenticator(123, 456)
        assert len(fake.calls) == 0

    async def test_transport_type_before_protocol_value(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="transport must be a string"):
            await domain.add_virtual_authenticator("bad", 456)
        assert len(fake.calls) == 0

    async def test_authenticator_id_before_credential_id(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.get_credential(123, 456)
        assert len(fake.calls) == 0

    async def test_authenticator_id_before_credential_type(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.add_credential(123, "bad")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Concurrent validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrentValidation:
    async def test_concurrent_valid_and_invalid(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)

        async def valid_call() -> dict[str, Any]:
            return await domain.set_user_verified("auth-1", True)

        async def invalid_call() -> dict[str, Any]:
            return await domain.set_user_verified("auth-1", "bad")

        results = await asyncio.gather(
            valid_call(),
            invalid_call(),
            valid_call(),
            return_exceptions=True,
        )
        assert isinstance(results[0], dict)
        assert isinstance(results[1], TypeError)
        assert isinstance(results[2], dict)
        assert len(fake.calls) == 2

    async def test_concurrent_all_valid_different_params(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await asyncio.gather(
            domain.set_user_verified("auth-1", True),
            domain.set_user_verified("auth-2", False),
            domain.set_automatic_presence_simulation("auth-1", True),
            domain.set_automatic_presence_simulation("auth-2", False),
        )
        assert len(fake.calls) == 4
        for _, params in fake.calls:
            assert params is not None


# ---------------------------------------------------------------------------
# Optional param omission (bug regression tests)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOptionalParamOmission:
    """Verify that optional params are only sent when explicitly set."""

    async def test_enable_false_sends_param(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable(enable_ui=False)
        _, params = fake.last_call
        assert params is not None
        assert params["enableUI"] is False

    async def test_enable_none_omits_param(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable(enable_ui=None)
        _, params = fake.last_call
        assert params is None

    async def test_enable_explicit_none_same_as_default(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.enable()
        default_params = fake.last_call[1]
        await domain.enable(enable_ui=None)
        explicit_params = fake.last_call[1]
        assert default_params == explicit_params

    async def test_set_credential_properties_only_eligibility(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties(
            "auth-1", "cred-1", backup_eligibility=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["backupEligibility"] is True
        assert "backupState" not in params

    async def test_set_credential_properties_only_state(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties(
            "auth-1", "cred-1", backup_state=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["backupState"] is False
        assert "backupEligibility" not in params

    async def test_set_credential_properties_none_omits_both(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties(
            "auth-1", "cred-1",
            backup_eligibility=None, backup_state=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert "backupEligibility" not in params
        assert "backupState" not in params

    async def test_set_credential_properties_false_sends(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_credential_properties(
            "auth-1", "cred-1",
            backup_eligibility=False, backup_state=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["backupEligibility"] is False
        assert params["backupState"] is False

    async def test_set_response_override_bits_only_bogus(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1", is_bogus_signature=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["isBogusSignature"] is True
        assert "isBadUV" not in params
        assert "isBadUP" not in params

    async def test_set_response_override_bits_only_uv(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1", is_bad_uv=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["isBadUV"] is True
        assert "isBogusSignature" not in params
        assert "isBadUP" not in params

    async def test_set_response_override_bits_only_up(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1", is_bad_up=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["isBadUP"] is True
        assert "isBogusSignature" not in params
        assert "isBadUV" not in params

    async def test_set_response_override_bits_none_omits_all(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1",
            is_bogus_signature=None,
            is_bad_uv=None,
            is_bad_up=None,
        )
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["authenticatorId"]

    async def test_set_response_override_bits_false_sends(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1",
            is_bogus_signature=False,
            is_bad_uv=False,
            is_bad_up=False,
        )
        _, params = fake.last_call
        assert params is not None
        assert params["isBogusSignature"] is False
        assert params["isBadUV"] is False
        assert params["isBadUP"] is False

    async def test_set_response_override_bits_partial_keys(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        await domain.set_response_override_bits(
            "auth-1", is_bogus_signature=True, is_bad_up=True,
        )
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {
            "authenticatorId", "isBogusSignature", "isBadUP",
        }


# ---------------------------------------------------------------------------
# Validation order with optional params
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOptionalParamValidationOrder:
    """Verify validation order is correct with optional params."""

    async def test_enable_ui_type_validation(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="enable_ui must be a bool or None"):
            await domain.enable(enable_ui=123)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_set_cred_props_auth_id_before_backup(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.set_credential_properties(
                123, "cred-1", backup_eligibility=1,  # type: ignore[arg-type]
            )
        assert len(fake.calls) == 0

    async def test_set_cred_props_cred_id_before_backup(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="credential_id must be a string"):
            await domain.set_credential_properties(
                "auth-1", 123, backup_eligibility=1,  # type: ignore[arg-type]
            )
        assert len(fake.calls) == 0

    async def test_set_override_bits_auth_id_before_bools(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(TypeError, match="authenticator_id must be a string"):
            await domain.set_response_override_bits(
                123, is_bogus_signature=1,  # type: ignore[arg-type]
            )
        assert len(fake.calls) == 0

    async def test_set_cred_props_eligibility_before_state(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(
            TypeError, match="backup_eligibility must be a bool or None"
        ):
            await domain.set_credential_properties(
                "auth-1", "cred-1",
                backup_eligibility=1,  # type: ignore[arg-type]
                backup_state=1,  # type: ignore[arg-type]
            )
        assert len(fake.calls) == 0

    async def test_set_override_bits_bogus_before_uv(self) -> None:
        fake = FakeSender({})
        domain = WebAuthnDomain(fake)
        with pytest.raises(
            TypeError, match="is_bogus_signature must be a bool or None"
        ):
            await domain.set_response_override_bits(
                "auth-1",
                is_bogus_signature=1,  # type: ignore[arg-type]
                is_bad_uv=1,  # type: ignore[arg-type]
            )
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# ctap2_version with u2f protocol
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCtap2VersionWithU2f:
    """Verify ctap2_version handling when protocol is u2f."""

    async def test_ctap2_version_sent_even_with_u2f(self) -> None:
        """The implementation sends ctap2_version if not None regardless
        of protocol. This documents the current behavior."""
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator(
            "u2f", "usb", ctap2_version="ctap2_1",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["options"]["ctap2Version"] == "ctap2_1"

    async def test_ctap2_version_none_with_u2f_not_sent(self) -> None:
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        await domain.add_virtual_authenticator("u2f", "usb")
        _, params = fake.last_call
        assert params is not None
        assert "ctap2Version" not in params["options"]

    async def test_ctap2_version_invalid_with_u2f_raises(self) -> None:
        """Even with u2f, an invalid ctap2_version should raise."""
        fake = FakeSender({"authenticatorId": "auth-1"})
        domain = WebAuthnDomain(fake)
        with pytest.raises(ValueError, match="ctap2_version must be"):
            await domain.add_virtual_authenticator(
                "u2f", "usb", ctap2_version="ctap3_0",
            )
        assert len(fake.calls) == 0
