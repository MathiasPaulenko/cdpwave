"""Security domain: certificate error handling and security state."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SecurityDomain(BaseDomain):
    """Wrapper for the CDP Security domain.

    Provides certificate error override and handling for insecure
    connections during navigation.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Security domain.

        Activates Security domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Security.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Security domain.

        Deactivates Security domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Security.disable")

    async def handle_certificate_error(
        self,
        event_id: int,
        action: str,
    ) -> dict[str, Any]:
        """Handle a certificate error event.

        Args:
            event_id: The ID of the certificate error event.
            action: ``"continue"`` to proceed, ``"cancel"`` to abort.
        """
        return await self._call(
            "Security.handleCertificateError",
            {"eventId": event_id, "action": action},
        )

    async def set_override_certificate_errors(
        self,
        override: bool,
    ) -> dict[str, Any]:
        """Enable or disable certificate error override.

        When enabled, ``Security.certificateError`` events will be sent
        for certificate errors, allowing the client to handle them.

        Args:
            override: Whether to override certificate errors.
        """
        return await self._call(
            "Security.setOverrideCertificateErrors",
            {"override": override},
        )
