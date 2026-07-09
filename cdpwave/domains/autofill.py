"""Autofill domain: autofill form fields for testing.

Provides control over browser autofill to fill form fields
programmatically, useful for automated form testing.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AutofillDomain(BaseDomain):
    """Wrapper for the CDP Autofill domain.

    Provides methods to trigger autofill on form fields and to set
    autofill addresses for testing form auto-completion.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Autofill domain.

        Activates Autofill domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Autofill.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Autofill domain.

        Deactivates Autofill domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Autofill.disable")

    async def trigger_fill(
        self,
        field_id: int,
        frame_id: str | None = None,
        card: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger autofill on a form field.

        Fills the form field identified by ``field_id`` with the
        provided credit card or address data.

        Args:
            field_id: The DOM node ID of the field to autofill.
            frame_id: Optional frame ID containing the field.
            card: Optional credit card data dict with fields like
                ``number``, ``name``, ``expiryMonth``, ``expiryYear``,
                ``cvc``.
        """
        params: dict[str, Any] = {"fieldId": field_id}
        if frame_id is not None:
            params["frameId"] = frame_id
        if card is not None:
            params["card"] = card
        return await self._call("Autofill.triggerFill", params)

    async def trigger_fill_after_save(
        self,
        field_id: int,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Trigger autofill using saved data after a user save action.

        Args:
            field_id: The DOM node ID of the field to autofill.
            frame_id: Optional frame ID containing the field.
        """
        params: dict[str, Any] = {"fieldId": field_id}
        if frame_id is not None:
            params["frameId"] = frame_id
        return await self._call("Autofill.triggerFillAfterSave", params)

    async def set_addresses(
        self,
        addresses: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set autofill addresses for testing.

        Populates the autofill address list with the provided entries,
        replacing any existing addresses.

        Args:
            addresses: List of address dicts with fields like
                ``street``, ``city``, ``state``, ``postalCode``,
                ``country``, ``name``, ``organization``, etc.
        """
        return await self._call(
            "Autofill.setAddresses",
            {"addresses": addresses},
        )
