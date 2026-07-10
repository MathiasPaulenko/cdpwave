"""SmartCardEmulation domain: Smart card emulation for testing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SmartCardEmulationDomain(BaseDomain):
    """Wrapper for the CDP SmartCardEmulation domain.

    Provides emulation of smart card readers and cards for testing
    Web Smart Card API interactions.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the SmartCard emulation domain."""
        return await self._call("SmartCardEmulation.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the SmartCard emulation domain."""
        return await self._call("SmartCardEmulation.disable")

    async def report_establish_context_result(
        self,
        context_id: str,
        result: int,
    ) -> dict[str, Any]:
        """Report the result of establishing a context.

        Args:
            context_id: Context ID.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportEstablishContextResult",
            {"contextId": context_id, "result": result},
        )

    async def report_release_context_result(
        self,
        context_id: str,
        result: int,
    ) -> dict[str, Any]:
        """Report the result of releasing a context.

        Args:
            context_id: Context ID.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportReleaseContextResult",
            {"contextId": context_id, "result": result},
        )

    async def report_list_readers_result(
        self,
        context_id: str,
        readers: list[dict[str, Any]],
        result: int,
    ) -> dict[str, Any]:
        """Report the result of listing readers.

        Args:
            context_id: Context ID.
            readers: List of reader dicts.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportListReadersResult",
            {
                "contextId": context_id,
                "readers": readers,
                "result": result,
            },
        )

    async def report_get_status_change_result(
        self,
        context_id: str,
        reader_states: list[dict[str, Any]],
        result: int,
    ) -> dict[str, Any]:
        """Report the result of getting status changes.

        Args:
            context_id: Context ID.
            reader_states: List of reader state dicts.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportGetStatusChangeResult",
            {
                "contextId": context_id,
                "readerStates": reader_states,
                "result": result,
            },
        )

    async def report_connect_result(
        self,
        context_id: str,
        reader: str,
        card_handle: str,
        active_protocol: int,
        result: int,
    ) -> dict[str, Any]:
        """Report the result of connecting to a card.

        Args:
            context_id: Context ID.
            reader: Reader name.
            card_handle: Card handle.
            active_protocol: Active protocol.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportConnectResult",
            {
                "contextId": context_id,
                "reader": reader,
                "cardHandle": card_handle,
                "activeProtocol": active_protocol,
                "result": result,
            },
        )

    async def report_status_result(
        self,
        context_id: str,
        reader: str,
        card_state: int,
        active_protocol: int,
        result: int,
    ) -> dict[str, Any]:
        """Report the status of a card.

        Args:
            context_id: Context ID.
            reader: Reader name.
            card_state: Card state.
            active_protocol: Active protocol.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportStatusResult",
            {
                "contextId": context_id,
                "reader": reader,
                "cardState": card_state,
                "activeProtocol": active_protocol,
                "result": result,
            },
        )

    async def report_data_result(
        self,
        card_handle: str,
        response: str,
        result: int,
    ) -> dict[str, Any]:
        """Report the result of a data transfer.

        Args:
            card_handle: Card handle.
            response: Response data (hex-encoded).
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportDataResult",
            {
                "cardHandle": card_handle,
                "response": response,
                "result": result,
            },
        )

    async def report_begin_transaction_result(
        self,
        card_handle: str,
        result: int,
    ) -> dict[str, Any]:
        """Report the result of beginning a transaction.

        Args:
            card_handle: Card handle.
            result: Result code.
        """
        return await self._call(
            "SmartCardEmulation.reportBeginTransactionResult",
            {"cardHandle": card_handle, "result": result},
        )

    async def report_error(
        self,
        context_id: str | None = None,
        error: int | None = None,
    ) -> dict[str, Any]:
        """Report a smart card error.

        Args:
            context_id: Optional context ID.
            error: Optional error code.
        """
        params: dict[str, Any] = {}
        if context_id is not None:
            params["contextId"] = context_id
        if error is not None:
            params["error"] = error
        return await self._call("SmartCardEmulation.reportError", params)

    async def report_plain_result(
        self,
        result: int,
        context_id: str | None = None,
    ) -> dict[str, Any]:
        """Report a plain result.

        Args:
            result: Result code.
            context_id: Optional context ID.
        """
        params: dict[str, Any] = {"result": result}
        if context_id is not None:
            params["contextId"] = context_id
        return await self._call("SmartCardEmulation.reportPlainResult", params)
