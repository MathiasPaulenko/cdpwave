"""WebAuthn domain: virtual authenticator and credential management.

Events:

    ``WebAuthn.credentialAdded`` (experimental) — triggered when a
    credential is added to an authenticator.  Parameters:
    ``authenticatorId`` (str), ``credential`` (Credential).

    ``WebAuthn.credentialAsserted`` (experimental) — triggered when a
    credential is used in a webauthn assertion.  Parameters:
    ``authenticatorId`` (str), ``credential`` (Credential).

    ``WebAuthn.credentialDeleted`` (experimental) — triggered when a
    credential is deleted, e.g. through
    ``PublicKeyCredential.signalUnknownCredential()``.  Parameters:
    ``authenticatorId`` (str), ``credentialId`` (str).

    ``WebAuthn.credentialUpdated`` (experimental) — triggered when a
    credential is updated, e.g. through
    ``PublicKeyCredential.signalCurrentUserDetails()``.  Parameters:
    ``authenticatorId`` (str), ``credential`` (Credential).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_AUTHENTICATOR_PROTOCOLS = ("u2f", "ctap2")
_AUTHENTICATOR_TRANSPORTS = ("usb", "nfc", "ble", "cable", "hybrid", "internal")
_CTAP2_VERSIONS = ("ctap2_0", "ctap2_1", "ctap2_2")


class WebAuthnDomain(BaseDomain):
    """Wrapper for the CDP WebAuthn domain.

    Provides virtual authenticator management for testing WebAuthn
    flows without physical hardware.  Add credentials, verify users,
    and simulate authenticator presence.

    Event ``WebAuthn.credentialAdded`` (experimental):
        - ``authenticatorId``: str — the authenticator ID
        - ``credential``: Credential — the credential that was added

    Event ``WebAuthn.credentialAsserted`` (experimental):
        - ``authenticatorId``: str — the authenticator ID
        - ``credential``: Credential — the credential that was asserted

    Event ``WebAuthn.credentialDeleted`` (experimental):
        - ``authenticatorId``: str — the authenticator ID
        - ``credentialId``: str — the ID of the deleted credential

    Event ``WebAuthn.credentialUpdated`` (experimental):
        - ``authenticatorId``: str — the authenticator ID
        - ``credential``: Credential — the updated credential
    """

    async def add_credential(
        self,
        authenticator_id: str,
        credential: dict[str, Any],
    ) -> dict[str, Any]:
        """Adds the credential to the specified authenticator.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            credential: Credential dict with ``credentialId`` (str),
                ``isResidentCredential`` (bool), ``privateKey`` (str),
                ``signCount`` (int), ``backupEligibility`` (bool),
                ``backupState`` (bool), and optional ``rpId`` (str),
                ``userHandle`` (str), ``largeBlob`` (str),
                ``userName`` (str), ``userDisplayName`` (str).

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string or
                ``credential`` is not a dict.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(credential, dict):
            raise TypeError("credential must be a dict")
        return await self._call(
            "WebAuthn.addCredential",
            {"authenticatorId": authenticator_id, "credential": credential},
        )

    async def add_virtual_authenticator(
        self,
        protocol: str,
        transport: str,
        has_resident_key: bool = False,
        has_user_verification: bool = False,
        has_large_blob: bool = False,
        has_cred_blob: bool = False,
        has_min_pin_length: bool = False,
        has_prf: bool = False,
        has_hmac_secret: bool = False,
        has_hmac_secret_mc: bool = False,
        automatic_presence_simulation: bool = False,
        is_user_verified: bool = False,
        default_backup_eligibility: bool = False,
        default_backup_state: bool = False,
        ctap2_version: str | None = None,
    ) -> dict[str, Any]:
        """Creates and adds a virtual authenticator.

        Experimental.

        Args:
            protocol: Authenticator protocol. Allowed values:
                ``"u2f"`` and ``"ctap2"``.
            transport: Authenticator transport. Allowed values:
                ``"usb"``, ``"nfc"``, ``"ble"``, ``"cable"``,
                ``"hybrid"``, and ``"internal"``.
            has_resident_key: Whether the authenticator supports
                resident keys. Defaults to false.
            has_user_verification: Whether the authenticator supports
                user verification. Defaults to false.
            has_large_blob: Whether the authenticator supports the
                largeBlob extension. Defaults to false.
            has_cred_blob: Whether the authenticator supports the
                credBlob extension. Defaults to false.
            has_min_pin_length: Whether the authenticator supports the
                minPinLength extension. Defaults to false.
            has_prf: Whether the authenticator supports the prf
                extension. Defaults to false.
            has_hmac_secret: Whether the authenticator supports the
                hmac-secret extension. Defaults to false.
            has_hmac_secret_mc: Whether the authenticator supports the
                hmac-secret-mc extension. Defaults to false.
            automatic_presence_simulation: Whether tests of user
                presence will succeed immediately. Defaults to false.
            is_user_verified: Whether user verification succeeds.
                Defaults to false.
            default_backup_eligibility: Default backup eligibility
                flag for credentials. Defaults to false.
            default_backup_state: Default backup state flag for
                credentials. Defaults to false.
            ctap2_version: CTAP2 version. Allowed values:
                ``"ctap2_0"``, ``"ctap2_1"``, and ``"ctap2_2"``.
                Ignored if ``protocol`` is ``"u2f"``. Only sent if
                not ``None``.

        Returns:
            Dict with ``authenticatorId``.

        Raises:
            TypeError: If ``protocol`` or ``transport`` is not a
                string, or any bool parameter is not a bool.
            ValueError: If ``protocol`` is not ``"u2f"`` or
                ``"ctap2"``, ``transport`` is not a valid transport,
                or ``ctap2_version`` is not a valid CTAP2 version.
        """
        if not isinstance(protocol, str):
            raise TypeError("protocol must be a string")
        if not isinstance(transport, str):
            raise TypeError("transport must be a string")
        if protocol not in _AUTHENTICATOR_PROTOCOLS:
            raise ValueError("protocol must be 'u2f' or 'ctap2'")
        if transport not in _AUTHENTICATOR_TRANSPORTS:
            raise ValueError(
                "transport must be 'usb', 'nfc', 'ble', 'cable', "
                "'hybrid', or 'internal'"
            )
        if not isinstance(has_resident_key, bool):
            raise TypeError("has_resident_key must be a bool")
        if not isinstance(has_user_verification, bool):
            raise TypeError("has_user_verification must be a bool")
        if not isinstance(has_large_blob, bool):
            raise TypeError("has_large_blob must be a bool")
        if not isinstance(has_cred_blob, bool):
            raise TypeError("has_cred_blob must be a bool")
        if not isinstance(has_min_pin_length, bool):
            raise TypeError("has_min_pin_length must be a bool")
        if not isinstance(has_prf, bool):
            raise TypeError("has_prf must be a bool")
        if not isinstance(has_hmac_secret, bool):
            raise TypeError("has_hmac_secret must be a bool")
        if not isinstance(has_hmac_secret_mc, bool):
            raise TypeError("has_hmac_secret_mc must be a bool")
        if not isinstance(automatic_presence_simulation, bool):
            raise TypeError("automatic_presence_simulation must be a bool")
        if not isinstance(is_user_verified, bool):
            raise TypeError("is_user_verified must be a bool")
        if not isinstance(default_backup_eligibility, bool):
            raise TypeError("default_backup_eligibility must be a bool")
        if not isinstance(default_backup_state, bool):
            raise TypeError("default_backup_state must be a bool")
        if ctap2_version is not None:
            if not isinstance(ctap2_version, str):
                raise TypeError("ctap2_version must be a string or None")
            if ctap2_version not in _CTAP2_VERSIONS:
                raise ValueError(
                    "ctap2_version must be 'ctap2_0', 'ctap2_1', or 'ctap2_2'"
                )
        params: dict[str, Any] = {
            "options": {
                "protocol": protocol,
                "transport": transport,
                "hasResidentKey": has_resident_key,
                "hasUserVerification": has_user_verification,
                "hasLargeBlob": has_large_blob,
                "hasCredBlob": has_cred_blob,
                "hasMinPinLength": has_min_pin_length,
                "hasPrf": has_prf,
                "hasHmacSecret": has_hmac_secret,
                "hasHmacSecretMc": has_hmac_secret_mc,
                "automaticPresenceSimulation": automatic_presence_simulation,
                "isUserVerified": is_user_verified,
                "defaultBackupEligibility": default_backup_eligibility,
                "defaultBackupState": default_backup_state,
            }
        }
        if ctap2_version is not None:
            params["options"]["ctap2Version"] = ctap2_version
        return await self._call(
            "WebAuthn.addVirtualAuthenticator",
            params,
        )

    async def clear_credentials(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Clears all the credentials from the specified authenticator.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        return await self._call(
            "WebAuthn.clearCredentials",
            {"authenticatorId": authenticator_id},
        )

    async def disable(self) -> dict[str, Any]:
        """Disable the WebAuthn domain.

        Deactivates WebAuthn domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAuthn.disable")

    async def enable(self, enable_ui: bool | None = None) -> dict[str, Any]:
        """Enable the WebAuthn domain and start intercepting credential
        storage and retrieval with a virtual authenticator.

        Args:
            enable_ui: Whether to enable the WebAuthn user interface.
                Enabling the UI is recommended for debugging and demo
                purposes. Disabling the UI is recommended for automated
                testing. Only sent if not ``None``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``enable_ui`` is not a bool or ``None``.
        """
        params: dict[str, Any] | None = None
        if enable_ui is not None:
            if not isinstance(enable_ui, bool):
                raise TypeError("enable_ui must be a bool or None")
            params = {"enableUI": enable_ui}
        return await self._call("WebAuthn.enable", params)

    async def get_credential(
        self,
        authenticator_id: str,
        credential_id: str,
    ) -> dict[str, Any]:
        """Returns a single credential stored in the given virtual
        authenticator that matches the credential ID.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            credential_id: Base64-encoded credential ID.

        Returns:
            Dict with ``credential`` object.

        Raises:
            TypeError: If ``authenticator_id`` or ``credential_id``
                is not a string.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(credential_id, str):
            raise TypeError("credential_id must be a string")
        return await self._call(
            "WebAuthn.getCredential",
            {"authenticatorId": authenticator_id, "credentialId": credential_id},
        )

    async def get_credentials(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Returns all the credentials stored in the given virtual
        authenticator.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.

        Returns:
            Dict with ``credentials`` list.

        Raises:
            TypeError: If ``authenticator_id`` is not a string.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        return await self._call(
            "WebAuthn.getCredentials",
            {"authenticatorId": authenticator_id},
        )

    async def remove_credential(
        self,
        authenticator_id: str,
        credential_id: str,
    ) -> dict[str, Any]:
        """Removes a credential from the authenticator.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            credential_id: Base64-encoded credential ID.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` or ``credential_id``
                is not a string.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(credential_id, str):
            raise TypeError("credential_id must be a string")
        return await self._call(
            "WebAuthn.removeCredential",
            {"authenticatorId": authenticator_id, "credentialId": credential_id},
        )

    async def remove_virtual_authenticator(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Removes the given authenticator.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator to remove.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        return await self._call(
            "WebAuthn.removeVirtualAuthenticator",
            {"authenticatorId": authenticator_id},
        )

    async def set_automatic_presence_simulation(
        self,
        authenticator_id: str,
        enabled: bool,
    ) -> dict[str, Any]:
        """Sets whether tests of user presence will succeed immediately
        (if true) or fail to resolve (if false) for an authenticator.
        The default is true.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            enabled: Whether to simulate authenticator presence.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string or
                ``enabled`` is not a bool.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a bool")
        return await self._call(
            "WebAuthn.setAutomaticPresenceSimulation",
            {"authenticatorId": authenticator_id, "enabled": enabled},
        )

    async def set_credential_properties(
        self,
        authenticator_id: str,
        credential_id: str,
        backup_eligibility: bool | None = None,
        backup_state: bool | None = None,
    ) -> dict[str, Any]:
        """Allows setting credential properties.

        See https://w3c.github.io/webauthn/#sctn-automation-set-credential-properties.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            credential_id: Base64-encoded credential ID.
            backup_eligibility: Whether the credential is backup
                eligible. Only sent if not ``None``.
            backup_state: Whether the credential is in backup state.
                Only sent if not ``None``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` or ``credential_id``
                is not a string, or ``backup_eligibility`` or
                ``backup_state`` is not a bool or ``None``.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(credential_id, str):
            raise TypeError("credential_id must be a string")
        params: dict[str, Any] = {
            "authenticatorId": authenticator_id,
            "credentialId": credential_id,
        }
        if backup_eligibility is not None:
            if not isinstance(backup_eligibility, bool):
                raise TypeError("backup_eligibility must be a bool or None")
            params["backupEligibility"] = backup_eligibility
        if backup_state is not None:
            if not isinstance(backup_state, bool):
                raise TypeError("backup_state must be a bool or None")
            params["backupState"] = backup_state
        return await self._call(
            "WebAuthn.setCredentialProperties",
            params,
        )

    async def set_response_override_bits(
        self,
        authenticator_id: str,
        is_bogus_signature: bool | None = None,
        is_bad_uv: bool | None = None,
        is_bad_up: bool | None = None,
    ) -> dict[str, Any]:
        """Resets parameters isBogusSignature, isBadUV, isBadUP to false
        if they are not present.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            is_bogus_signature: If set, overrides the signature in the
                authenticator response to be zero. Only sent if not
                ``None``.
            is_bad_uv: If set, overrides the UV bit in the flags in
                the authenticator response to be zero. Only sent if
                not ``None``.
            is_bad_up: If set, overrides the UP bit in the flags in
                the authenticator response to be zero. Only sent if
                not ``None``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string, or
                ``is_bogus_signature``, ``is_bad_uv``, or
                ``is_bad_up`` is not a bool or ``None``.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        params: dict[str, Any] = {"authenticatorId": authenticator_id}
        if is_bogus_signature is not None:
            if not isinstance(is_bogus_signature, bool):
                raise TypeError("is_bogus_signature must be a bool or None")
            params["isBogusSignature"] = is_bogus_signature
        if is_bad_uv is not None:
            if not isinstance(is_bad_uv, bool):
                raise TypeError("is_bad_uv must be a bool or None")
            params["isBadUV"] = is_bad_uv
        if is_bad_up is not None:
            if not isinstance(is_bad_up, bool):
                raise TypeError("is_bad_up must be a bool or None")
            params["isBadUP"] = is_bad_up
        return await self._call(
            "WebAuthn.setResponseOverrideBits",
            params,
        )

    async def set_user_verified(
        self,
        authenticator_id: str,
        is_user_verified: bool,
    ) -> dict[str, Any]:
        """Sets whether User Verification succeeds or fails for an
        authenticator. The default is true.

        Experimental.

        Args:
            authenticator_id: ID of the authenticator.
            is_user_verified: Whether user verification is active.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``authenticator_id`` is not a string or
                ``is_user_verified`` is not a bool.
        """
        if not isinstance(authenticator_id, str):
            raise TypeError("authenticator_id must be a string")
        if not isinstance(is_user_verified, bool):
            raise TypeError("is_user_verified must be a bool")
        return await self._call(
            "WebAuthn.setUserVerified",
            {
                "authenticatorId": authenticator_id,
                "isUserVerified": is_user_verified,
            },
        )
