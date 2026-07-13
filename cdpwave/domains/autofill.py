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

    async def trigger(
        self,
        field_id: int,
        frame_id: str | None = None,
        card: dict[str, Any] | None = None,
        address: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger autofill on a form identified by the fieldId.

        If the field and related form cannot be autofilled, returns an error.
        ``card`` and ``address`` are mutually exclusive.

        Args:
            field_id: The backend node ID that serves as an anchor for autofill.
            frame_id: Identifies the frame that the field belongs to.
            card: Credit card information to fill out the form.
                Not saved. Mutually exclusive with ``address``.
            address: Address to fill out the form.
                Not saved. Mutually exclusive with ``card``.
        """
        if isinstance(field_id, bool) or not isinstance(field_id, int):
            raise TypeError("field_id must be an int")
        if frame_id is not None and not isinstance(frame_id, str):
            raise TypeError("frame_id must be a str or None")
        if card is not None and not isinstance(card, dict):
            raise TypeError("card must be a dict or None")
        if address is not None and not isinstance(address, dict):
            raise TypeError("address must be a dict or None")
        params: dict[str, Any] = {"fieldId": field_id}
        if frame_id is not None:
            params["frameId"] = frame_id
        if card is not None:
            params["card"] = card
        if address is not None:
            params["address"] = address
        return await self._call("Autofill.trigger", params)

    async def trigger_fill(
        self,
        field_id: int,
        frame_id: str | None = None,
        card: dict[str, Any] | None = None,
        address: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger autofill on a form field.

        Alias for :meth:`trigger`.
        """
        return await self.trigger(field_id, frame_id, card, address)

    async def trigger_fill_after_save(
        self,
        field_id: int,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Trigger autofill using saved data after a user save action.

        Convenience method that calls :meth:`trigger` without card/address
        to use previously saved autofill data.
        """
        return await self.trigger(field_id, frame_id)

    async def set_addresses(
        self,
        addresses: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set autofill addresses for testing.

        Populates the autofill address list with the provided entries,
        replacing any existing addresses.

        Args:
            addresses: List of ``Address`` dicts, each containing a
                ``fields`` key with a list of ``{"name": ..., "value": ...}``
                entries (e.g. ``{"name": "NAME_FULL", "value": "Jon"}``).
        """
        if not isinstance(addresses, list):
            raise TypeError("addresses must be a list")
        for i, addr in enumerate(addresses):
            if not isinstance(addr, dict):
                raise TypeError(f"addresses[{i}] must be a dict")
        return await self._call(
            "Autofill.setAddresses",
            {"addresses": addresses},
        )
