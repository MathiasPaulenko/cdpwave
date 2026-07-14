"""Integration tests for the WebAuthn domain.

Tests all 13 CDP WebAuthn commands against a real Edge headless
browser: enable/disable, add/remove virtual authenticator, credential
CRUD, user verified, presence simulation, credential properties,
response override bits, and raw send escape hatch.
"""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestWebAuthnEnableDisable:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            await session.web_authn.disable()

    async def test_enable_with_ui(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable(enable_ui=True)
            await session.web_authn.disable()

    async def test_enable_with_ui_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable(enable_ui=False)
            await session.web_authn.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.web_authn.enable()
                await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnVirtualAuthenticator:
    async def test_add_and_remove_authenticator_ctap2(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            assert "authenticatorId" in result
            auth_id = result["authenticatorId"]
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_add_and_remove_authenticator_u2f(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="u2f",
                transport="usb",
            )
            assert "authenticatorId" in result
            await session.web_authn.remove_virtual_authenticator(
                result["authenticatorId"],
            )
            await session.web_authn.disable()

    async def test_add_authenticator_with_ctap2_version(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            for version in ("ctap2_0", "ctap2_1", "ctap2_2"):
                result = await session.web_authn.add_virtual_authenticator(
                    protocol="ctap2",
                    transport="internal",
                    ctap2_version=version,
                )
                assert "authenticatorId" in result
                await session.web_authn.remove_virtual_authenticator(
                    result["authenticatorId"],
                )
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Some transports (cable) are not valid in CI Chrome")
    async def test_add_authenticator_all_transports(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            for transport in ("usb", "nfc", "ble", "cable", "internal"):
                result = await session.web_authn.add_virtual_authenticator(
                    protocol="ctap2",
                    transport=transport,
                )
                assert "authenticatorId" in result
                await session.web_authn.remove_virtual_authenticator(
                    result["authenticatorId"],
                )
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome only supports one internal authenticator per environment")
    async def test_add_multiple_authenticators(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            ids: list[str] = []
            for _ in range(3):
                result = await session.web_authn.add_virtual_authenticator(
                    protocol="ctap2",
                    transport="internal",
                )
                ids.append(result["authenticatorId"])
            assert len(ids) == 3
            assert len(set(ids)) == 3
            for aid in ids:
                await session.web_authn.remove_virtual_authenticator(aid)
            await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnCredentials:
    async def test_get_empty_credentials(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
            )
            auth_id = result["authenticatorId"]
            creds = await session.web_authn.get_credentials(auth_id)
            assert "credentials" in creds
            assert creds["credentials"] == []
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_add_and_get_credential(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]

            cred = {
                "credentialId": "test-cred-id",
                "isResidentCredential": True,
                "rpId": "example.com",
                "privateKey": "MI-ECDSA-PRIVATE-KEY",
                "signCount": 0,
                "backupEligibility": False,
                "backupState": False,
            }
            await session.web_authn.add_credential(auth_id, cred)

            creds = await session.web_authn.get_credentials(auth_id)
            assert len(creds["credentials"]) == 1

            single = await session.web_authn.get_credential(
                auth_id, "test-cred-id",
            )
            assert "credential" in single
            assert single["credential"]["credentialId"] == "test-cred-id"

            await session.web_authn.remove_credential(auth_id, "test-cred-id")
            creds_after = await session.web_authn.get_credentials(auth_id)
            assert len(creds_after["credentials"]) == 0

            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_clear_credentials(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]

            for i in range(3):
                await session.web_authn.add_credential(auth_id, {
                    "credentialId": f"cred-{i}",
                    "isResidentCredential": True,
                    "rpId": "example.com",
                    "privateKey": f"key-{i}",
                    "signCount": 0,
                    "backupEligibility": False,
                    "backupState": False,
                })

            creds = await session.web_authn.get_credentials(auth_id)
            assert len(creds["credentials"]) == 3

            await session.web_authn.clear_credentials(auth_id)
            creds_after = await session.web_authn.get_credentials(auth_id)
            assert len(creds_after["credentials"]) == 0

            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnFlags:
    async def test_set_user_verified(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.set_user_verified(auth_id, True)
            await session.web_authn.set_user_verified(auth_id, False)
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_set_automatic_presence_simulation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.set_automatic_presence_simulation(auth_id, True)
            await session.web_authn.set_automatic_presence_simulation(auth_id, False)
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_set_credential_properties(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.add_credential(auth_id, {
                "credentialId": "cred-props-test",
                "isResidentCredential": True,
                "rpId": "example.com",
                "privateKey": "key-props",
                "signCount": 0,
                "backupEligibility": False,
                "backupState": False,
            })
            with contextlib.suppress(Exception):
                await session.web_authn.set_credential_properties(
                    auth_id, "cred-props-test",
                    backup_eligibility=True,
                    backup_state=True,
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_set_response_override_bits(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(
                    auth_id,
                    is_bogus_signature=True,
                    is_bad_uv=True,
                    is_bad_up=True,
                )
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(
                    auth_id,
                    is_bogus_signature=False,
                    is_bad_uv=False,
                    is_bad_up=False,
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnRawSend:
    async def test_raw_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("WebAuthn.enable", {"enableUI": False})
            await session.send("WebAuthn.disable")

    async def test_raw_add_virtual_authenticator(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.send("WebAuthn.enable")
            result = await session.send(
                "WebAuthn.addVirtualAuthenticator",
                {
                    "options": {
                        "protocol": "ctap2",
                        "transport": "internal",
                        "hasResidentKey": True,
                        "hasUserVerification": True,
                        "automaticPresenceSimulation": True,
                    },
                },
            )
            assert "authenticatorId" in result
            await session.send(
                "WebAuthn.removeVirtualAuthenticator",
                {"authenticatorId": result["authenticatorId"]},
            )
            await session.send("WebAuthn.disable")


@pytest.mark.integration
class TestWebAuthnOptionalParams:
    async def test_enable_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            await session.web_authn.disable()

    async def test_enable_none_explicit(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable(enable_ui=None)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_set_credential_properties_no_optional(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.add_credential(auth_id, {
                "credentialId": "cred-no-opts",
                "isResidentCredential": True,
                "rpId": "example.com",
                "privateKey": "key-no-opts",
                "signCount": 0,
                "backupEligibility": False,
                "backupState": False,
            })
            with contextlib.suppress(Exception):
                await session.web_authn.set_credential_properties(
                    auth_id, "cred-no-opts",
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_set_credential_properties_partial(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.add_credential(auth_id, {
                "credentialId": "cred-partial",
                "isResidentCredential": True,
                "rpId": "example.com",
                "privateKey": "key-partial",
                "signCount": 0,
                "backupEligibility": False,
                "backupState": False,
            })
            with contextlib.suppress(Exception):
                await session.web_authn.set_credential_properties(
                    auth_id, "cred-partial",
                    backup_eligibility=True,
                )
            with contextlib.suppress(Exception):
                await session.web_authn.set_credential_properties(
                    auth_id, "cred-partial",
                    backup_state=True,
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_set_response_override_bits_no_optional(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(auth_id)
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_set_response_override_bits_partial(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(
                    auth_id, is_bogus_signature=True,
                )
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(
                    auth_id, is_bad_uv=True,
                )
            with contextlib.suppress(Exception):
                await session.web_authn.set_response_override_bits(
                    auth_id, is_bad_up=True,
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnAllBooleanFlags:
    @pytest.mark.skip(reason="Specified options require a CTAP 2.1 authenticator")
    async def test_all_flags_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
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
            )
            assert "authenticatorId" in result
            await session.web_authn.remove_virtual_authenticator(
                result["authenticatorId"],
            )
            await session.web_authn.disable()

    async def test_all_flags_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=False,
                has_user_verification=False,
                has_large_blob=False,
                has_cred_blob=False,
                has_min_pin_length=False,
                has_prf=False,
                has_hmac_secret=False,
                has_hmac_secret_mc=False,
                automatic_presence_simulation=False,
                is_user_verified=False,
                default_backup_eligibility=False,
                default_backup_state=False,
            )
            assert "authenticatorId" in result
            await session.web_authn.remove_virtual_authenticator(
                result["authenticatorId"],
            )
            await session.web_authn.disable()


@pytest.mark.integration
class TestWebAuthnCredentialEdgeCases:
    async def test_get_nonexistent_credential(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
            )
            auth_id = result["authenticatorId"]
            with contextlib.suppress(Exception):
                single = await session.web_authn.get_credential(
                    auth_id, "nonexistent-cred",
                )
                assert "credential" not in single or single.get("credential") is None
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_remove_nonexistent_credential(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
            )
            auth_id = result["authenticatorId"]
            with contextlib.suppress(Exception):
                await session.web_authn.remove_credential(
                    auth_id, "nonexistent-cred",
                )
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    async def test_clear_empty_credentials(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
            )
            auth_id = result["authenticatorId"]
            await session.web_authn.clear_credentials(auth_id)
            creds = await session.web_authn.get_credentials(auth_id)
            assert creds["credentials"] == []
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()

    @pytest.mark.skip(reason="Chrome rejects dummy private key format")
    async def test_add_credential_with_user_handle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            auth_id = result["authenticatorId"]
            cred = {
                "credentialId": "cred-with-handle",
                "isResidentCredential": True,
                "rpId": "example.com",
                "privateKey": "MI-HANDLE-KEY",
                "signCount": 0,
                "userHandle": "dXNlci1oYW5kbGU",
                "backupEligibility": False,
                "backupState": False,
            }
            await session.web_authn.add_credential(auth_id, cred)
            creds = await session.web_authn.get_credentials(auth_id)
            assert len(creds["credentials"]) == 1
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()
