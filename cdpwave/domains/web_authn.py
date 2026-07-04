"""WebAuthn domain: virtual authenticator and credential management."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class WebAuthnDomain(BaseDomain):
    """Wrapper for the CDP WebAuthn domain.

    Provides virtual authenticator management for testing WebAuthn
    flows without physical hardware. Add credentials, verify users,
    and simulate authenticator presence.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the WebAuthn domain.

        Activates WebAuthn domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAuthn.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the WebAuthn domain.

        Deactivates WebAuthn domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAuthn.disable")

    async def add_virtual_authenticator(
        self,
        options: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a virtual authenticator.

        Args:
            options: Authenticator options dict with ``protocol``,
                ``transport``, ``hasResidentKey``, ``hasUserVerification``,
                and optional ``automaticPresenceSimulation``.

        Returns:
            Dict with ``authenticatorId``.
        """
        return await self._call(
            "WebAuthn.addVirtualAuthenticator",
            {"options": options},
        )

    async def remove_virtual_authenticator(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Remove a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator to remove.
        """
        return await self._call(
            "WebAuthn.removeVirtualAuthenticator",
            {"authenticatorId": authenticator_id},
        )

    async def add_credential(
        self,
        authenticator_id: str,
        credential: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a credential to a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.
            credential: Credential dict with ``credentialId``,
                ``isResidentCredential``, ``rpId``, ``privateKey``,
                and optional ``userHandle`` and ``signCount``.
        """
        return await self._call(
            "WebAuthn.addCredential",
            {"authenticatorId": authenticator_id, "credential": credential},
        )

    async def get_credential(
        self,
        authenticator_id: str,
        credential_id: str,
    ) -> dict[str, Any]:
        """Get a specific credential from a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.
            credential_id: Base64-encoded credential ID.

        Returns:
            Dict with the ``credential`` object.
        """
        return await self._call(
            "WebAuthn.getCredential",
            {"authenticatorId": authenticator_id, "credentialId": credential_id},
        )

    async def get_credentials(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Get all credentials from a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.

        Returns:
            Dict with ``credentials`` list.
        """
        return await self._call(
            "WebAuthn.getCredentials",
            {"authenticatorId": authenticator_id},
        )

    async def remove_credential(
        self,
        authenticator_id: str,
        credential_id: str,
    ) -> dict[str, Any]:
        """Remove a credential from a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.
            credential_id: Base64-encoded credential ID.
        """
        return await self._call(
            "WebAuthn.removeCredential",
            {"authenticatorId": authenticator_id, "credentialId": credential_id},
        )

    async def clear_credentials(
        self,
        authenticator_id: str,
    ) -> dict[str, Any]:
        """Clear all credentials from a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.
        """
        return await self._call(
            "WebAuthn.clearCredentials",
            {"authenticatorId": authenticator_id},
        )

    async def set_user_verified(
        self,
        authenticator_id: str,
        is_user_verified: bool,
    ) -> dict[str, Any]:
        """Set the user verified flag on a virtual authenticator.

        Args:
            authenticator_id: ID of the authenticator.
            is_user_verified: Whether user verification is active.
        """
        return await self._call(
            "WebAuthn.setUserVerified",
            {
                "authenticatorId": authenticator_id,
                "isUserVerified": is_user_verified,
            },
        )

    async def set_automatic_presence_simulation(
        self,
        authenticator_id: str,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable automatic presence simulation.

        Args:
            authenticator_id: ID of the authenticator.
            enabled: Whether to simulate authenticator presence.
        """
        return await self._call(
            "WebAuthn.setAutomaticPresenceSimulation",
            {"authenticatorId": authenticator_id, "enabled": enabled},
        )
