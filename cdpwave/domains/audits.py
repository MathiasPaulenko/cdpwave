"""Audits domain: Lighthouse-style audits and accessibility checks."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AuditsDomain(BaseDomain):
    """Wrapper for the CDP Audits domain.

    Provides access to Lighthouse-style audits, contrast checking,
    and encoded response inspection.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Audits domain.

        Activates Audits domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Audits.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Audits domain.

        Deactivates Audits domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Audits.disable")

    async def check_contrast(self) -> dict[str, Any]:
        """Check contrast issues on the current page.

        Returns:
            Dict with contrast issue results.
        """
        return await self._call("Audits.checkContrast")

    async def get_encoded_response(
        self,
        request_id: str,
        encoding: str,
        quality: float | None = None,
        size_only: bool | None = None,
    ) -> dict[str, Any]:
        """Get the encoded response body for a request.

        Only applies to images.

        Args:
            request_id: Request ID from Network domain.
            encoding: ``"webp"``, ``"jpeg"``, or ``"png"``.
            quality: Optional quality (0.0-1.0, defaults to 1).
            size_only: Whether to return only the size without the body.

        Returns:
            Dict with ``body`` (base64), ``originalSize``, and
            ``encodedSize``.
        """
        params: dict[str, Any] = {
            "requestId": request_id,
            "encoding": encoding,
        }
        if quality is not None:
            params["quality"] = quality
        if size_only is not None:
            params["sizeOnly"] = size_only
        return await self._call("Audits.getEncodedResponse", params)

    async def check_forms_issues(self) -> dict[str, Any]:
        """Run the form issues check for the target page.

        Found issues are reported via ``Audits.issueAdded`` events.

        Returns:
            Dict with ``issues`` list of GenericIssueDetails.
        """
        return await self._call("Audits.checkFormsIssues")
