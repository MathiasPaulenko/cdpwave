"""Security domain: tracking security state changes.

Events:

    ``Security.certificateError`` (deprecated) — there is a certificate
    error.  Parameters: ``eventId`` (int), ``errorType`` (str),
    ``requestURL`` (str).

    ``Security.securityStateChanged`` (deprecated) — the security state
    of the page changed.  No longer being sent.  Parameters:
    ``securityState`` (SecurityState), ``schemeIsCryptographic`` (bool),
    ``explanations`` (list[SecurityStateExplanation]),
    ``mixedContentStatus`` (InsecureContentStatus), ``summary`` (str,
    optional).

    ``Security.visibleSecurityStateChanged`` (experimental) — the
    security state of the page changed.  Parameters:
    ``visibleSecurityState`` (VisibleSecurityState).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_CERTIFICATE_ERROR_ACTIONS = ("continue", "cancel")


class SecurityDomain(BaseDomain):
    """Wrapper for the CDP Security domain.

    Tracks security state changes and allows handling certificate
    errors during navigation.

    Event ``Security.certificateError`` (deprecated):
        - ``eventId``: int — the ID of the event
        - ``errorType``: str — the type of the error
        - ``requestURL``: str — the url that was requested

    Event ``Security.securityStateChanged`` (deprecated, no longer sent):
        - ``securityState``: SecurityState — security state
        - ``schemeIsCryptographic``: bool — loaded over HTTPS
        - ``explanations``: list[SecurityStateExplanation]
        - ``mixedContentStatus``: InsecureContentStatus
        - ``summary``: str (optional)

    Event ``Security.visibleSecurityStateChanged`` (experimental):
        - ``visibleSecurityState``: VisibleSecurityState — security
          state information about the page
    """

    async def disable(self) -> dict[str, Any]:
        """Disables tracking security state changes.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Security.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables tracking security state changes.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Security.enable")

    async def get_visible_security_state(self) -> dict[str, Any]:
        """Get the visible security state of the page.

        Experimental.

        Returns:
            Dict with ``visibleSecurityState`` containing security state
            details (e.g. ``securityState``, ``certificateSecurityState``,
            ``safetyTipInfo``, ``securityStateIssueIds``).
        """
        return await self._call("Security.getVisibleSecurityState")

    async def handle_certificate_error(
        self,
        event_id: int,
        action: str,
    ) -> dict[str, Any]:
        """Handles a certificate error that fired a certificateError event.

        Deprecated.

        Args:
            event_id: The ID of the event.
            action: The action to take on the certificate error.
                Allowed values: ``"continue"`` and ``"cancel"``.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``event_id`` is not an int or ``action`` is
                not a string.
            ValueError: If ``action`` is not ``"continue"`` or
                ``"cancel"``.
        """
        if isinstance(event_id, bool) or not isinstance(event_id, int):
            raise TypeError("event_id must be an integer")
        if not isinstance(action, str):
            raise TypeError("action must be a string")
        if action not in _CERTIFICATE_ERROR_ACTIONS:
            raise ValueError(
                "action must be 'continue' or 'cancel'"
            )
        return await self._call(
            "Security.handleCertificateError",
            {"eventId": event_id, "action": action},
        )

    async def set_ignore_certificate_errors(
        self,
        ignore: bool,
    ) -> dict[str, Any]:
        """Enable/disable whether all certificate errors should be ignored.

        Args:
            ignore: If true, all certificate errors will be ignored.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``ignore`` is not a bool.
        """
        if not isinstance(ignore, bool):
            raise TypeError("ignore must be a bool")
        return await self._call(
            "Security.setIgnoreCertificateErrors",
            {"ignore": ignore},
        )

    async def set_override_certificate_errors(
        self,
        override: bool,
    ) -> dict[str, Any]:
        """Enable/disable overriding certificate errors.

        Deprecated. If enabled, all certificate error events need to be
        handled by the DevTools client and should be answered with
        ``handle_certificate_error`` commands.

        Args:
            override: If true, certificate errors will be overridden.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``override`` is not a bool.
        """
        if not isinstance(override, bool):
            raise TypeError("override must be a bool")
        return await self._call(
            "Security.setOverrideCertificateErrors",
            {"override": override},
        )
