"""SmartCardEmulation domain: smart card emulation for testing.

Experimental domain that provides emulation of smart card readers and
cards for testing Web Smart Card API interactions, bypassing the need
for physical hardware.

Types defined by this domain:
  - ResultCode: PC/SC error code (string enum)
  - ShareMode: ``"shared"``, ``"exclusive"``, ``"direct"``
  - Disposition: ``"leave-card"``, ``"reset-card"``,
    ``"unpower-card"``, ``"eject-card"``
  - ConnectionState: ``"absent"``, ``"present"``, ``"swallowed"``,
    ``"powered"``, ``"negotiable"``, ``"specific"``
  - ReaderStateFlags, ProtocolSet, Protocol: ``"t0"``, ``"t1"``, ``"raw"``
  - ReaderStateIn, ReaderStateOut

Events:
  - ``establishContextRequested``
  - ``releaseContextRequested``
  - ``listReadersRequested``
  - ``getStatusChangeRequested``
  - ``cancelRequested``
  - ``connectRequested``
  - ``disconnectRequested``
  - ``transmitRequested``
  - ``controlRequested``
  - ``getAttribRequested``
  - ``setAttribRequested``
  - ``statusRequested``
  - ``beginTransactionRequested``
  - ``endTransactionRequested``

Commands:
  - ``enable``: enable the SmartCardEmulation domain
  - ``disable``: disable the SmartCardEmulation domain
  - ``reportEstablishContextResult``: report SCardEstablishContext result
  - ``reportReleaseContextResult``: report SCardReleaseContext result
  - ``reportListReadersResult``: report SCardListReaders result
  - ``reportGetStatusChangeResult``: report SCardGetStatusChange result
  - ``reportBeginTransactionResult``: report SCardBeginTransaction result
  - ``reportPlainResult``: report result for SCardCancel, SCardDisconnect,
    SCardSetAttrib, SCardEndTransaction
  - ``reportConnectResult``: report SCardConnect result
  - ``reportDataResult``: report result for SCardTransmit, SCardControl,
    SCardGetAttrib
  - ``reportStatusResult``: report SCardStatus result
  - ``reportError``: report an error result
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SmartCardEmulationDomain(BaseDomain):
    """Wrapper for the CDP SmartCardEmulation domain (experimental).

    Provides emulation of smart card readers and cards for testing
    Web Smart Card API interactions.

    Events emitted when the domain is enabled:
      - ``SmartCardEmulation.establishContextRequested``
      - ``SmartCardEmulation.releaseContextRequested``
      - ``SmartCardEmulation.listReadersRequested``
      - ``SmartCardEmulation.getStatusChangeRequested``
      - ``SmartCardEmulation.cancelRequested``
      - ``SmartCardEmulation.connectRequested``
      - ``SmartCardEmulation.disconnectRequested``
      - ``SmartCardEmulation.transmitRequested``
      - ``SmartCardEmulation.controlRequested``
      - ``SmartCardEmulation.getAttribRequested``
      - ``SmartCardEmulation.setAttribRequested``
      - ``SmartCardEmulation.statusRequested``
      - ``SmartCardEmulation.beginTransactionRequested``
      - ``SmartCardEmulation.endTransactionRequested``
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the SmartCardEmulation domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("SmartCardEmulation.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the SmartCardEmulation domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("SmartCardEmulation.disable")

    async def report_establish_context_result(
        self,
        request_id: str,
        context_id: int,
    ) -> dict[str, Any]:
        """Report the result of establishing a context.

        Args:
            request_id: Request ID from the establishContextRequested event.
            context_id: Context ID to use in subsequent calls.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str or ``context_id``
                is not an int (bool rejected).
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(context_id, int) or isinstance(context_id, bool):
            raise TypeError(
                f"context_id must be an int, got {type(context_id).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportEstablishContextResult",
            {"requestId": request_id, "contextId": context_id},
        )

    async def report_release_context_result(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Report the result of releasing a context.

        Args:
            request_id: Request ID from the releaseContextRequested event.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportReleaseContextResult",
            {"requestId": request_id},
        )

    async def report_list_readers_result(
        self,
        request_id: str,
        readers: list[str],
    ) -> dict[str, Any]:
        """Report the result of listing readers.

        Args:
            request_id: Request ID from the listReadersRequested event.
            readers: List of reader names.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str or ``readers`` is
                not a list of str.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(readers, list):
            raise TypeError(
                f"readers must be a list, got {type(readers).__name__}"
            )
        for i, r in enumerate(readers):
            if not isinstance(r, str):
                raise TypeError(
                    f"readers[{i}] must be a str, got {type(r).__name__}"
                )
        return await self._call(
            "SmartCardEmulation.reportListReadersResult",
            {"requestId": request_id, "readers": readers},
        )

    async def report_get_status_change_result(
        self,
        request_id: str,
        reader_states: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Report the result of getting status changes.

        Args:
            request_id: Request ID from the getStatusChangeRequested event.
            reader_states: List of ``ReaderStateOut`` dicts.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str or ``reader_states``
                is not a list of dict.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(reader_states, list):
            raise TypeError(
                f"reader_states must be a list, "
                f"got {type(reader_states).__name__}"
            )
        for i, rs in enumerate(reader_states):
            if not isinstance(rs, dict):
                raise TypeError(
                    f"reader_states[{i}] must be a dict, "
                    f"got {type(rs).__name__}"
                )
        return await self._call(
            "SmartCardEmulation.reportGetStatusChangeResult",
            {"requestId": request_id, "readerStates": reader_states},
        )

    async def report_begin_transaction_result(
        self,
        request_id: str,
        handle: int,
    ) -> dict[str, Any]:
        """Report the result of beginning a transaction.

        Args:
            request_id: Request ID from the beginTransactionRequested event.
            handle: Transaction handle.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str or ``handle`` is
                not an int (bool rejected).
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(handle, int) or isinstance(handle, bool):
            raise TypeError(
                f"handle must be an int, got {type(handle).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportBeginTransactionResult",
            {"requestId": request_id, "handle": handle},
        )

    async def report_plain_result(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Report a plain result (success with no additional data).

        Used for SCardCancel, SCardDisconnect, SCardSetAttrib,
        and SCardEndTransaction.

        Args:
            request_id: Request ID from the originating event.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportPlainResult",
            {"requestId": request_id},
        )

    async def report_connect_result(
        self,
        request_id: str,
        handle: int,
        active_protocol: str | None = None,
    ) -> dict[str, Any]:
        """Report the result of connecting to a card.

        Args:
            request_id: Request ID from the connectRequested event.
            handle: Card handle to use in subsequent calls.
            active_protocol: Active protocol (``"t0"``, ``"t1"``,
                ``"raw"``). Optional.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` is not a str, ``handle`` is
                not an int (bool rejected), or ``active_protocol`` is
                not a str when provided.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(handle, int) or isinstance(handle, bool):
            raise TypeError(
                f"handle must be an int, got {type(handle).__name__}"
            )
        params: dict[str, Any] = {"requestId": request_id, "handle": handle}
        if active_protocol is not None:
            if not isinstance(active_protocol, str):
                raise TypeError(
                    f"active_protocol must be a str, "
                    f"got {type(active_protocol).__name__}"
                )
            params["activeProtocol"] = active_protocol
        return await self._call(
            "SmartCardEmulation.reportConnectResult",
            params,
        )

    async def report_data_result(
        self,
        request_id: str,
        data: str,
    ) -> dict[str, Any]:
        """Report the result of a data transfer.

        Used for SCardTransmit, SCardControl, and SCardGetAttrib.

        Args:
            request_id: Request ID from the transmitRequested,
                controlRequested, or getAttribRequested event.
            data: Response data as base64-encoded binary.

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` or ``data`` is not a str.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(data, str):
            raise TypeError(
                f"data must be a str, got {type(data).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportDataResult",
            {"requestId": request_id, "data": data},
        )

    async def report_status_result(
        self,
        request_id: str,
        reader_name: str,
        state: str,
        atr: str,
        protocol: str | None = None,
    ) -> dict[str, Any]:
        """Report the status of a card.

        Args:
            request_id: Request ID from the statusRequested event.
            reader_name: Reader name.
            state: Connection state (``"absent"``, ``"present"``,
                ``"swallowed"``, ``"powered"``, ``"negotiable"``,
                ``"specific"``).
            atr: ATR (Answer To Reset) as base64-encoded binary.
            protocol: Optional protocol (``"t0"``, ``"t1"``, ``"raw"``).

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id``, ``reader_name``, ``state``,
                or ``atr`` is not a str, or ``protocol`` is not a str
                when provided.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(reader_name, str):
            raise TypeError(
                f"reader_name must be a str, "
                f"got {type(reader_name).__name__}"
            )
        if not isinstance(state, str):
            raise TypeError(
                f"state must be a str, got {type(state).__name__}"
            )
        if not isinstance(atr, str):
            raise TypeError(
                f"atr must be a str, got {type(atr).__name__}"
            )
        params: dict[str, Any] = {
            "requestId": request_id,
            "readerName": reader_name,
            "state": state,
            "atr": atr,
        }
        if protocol is not None:
            if not isinstance(protocol, str):
                raise TypeError(
                    f"protocol must be a str, got {type(protocol).__name__}"
                )
            params["protocol"] = protocol
        return await self._call(
            "SmartCardEmulation.reportStatusResult",
            params,
        )

    async def report_error(
        self,
        request_id: str,
        result_code: str,
    ) -> dict[str, Any]:
        """Report an error result for a request.

        Args:
            request_id: Request ID from the originating event.
            result_code: Error code from the ``ResultCode`` enum
                (e.g. ``"cancelled"``, ``"timeout"``, ``"internal-error"``).

        Returns:
            Response dict from the CDP.

        Raises:
            TypeError: If ``request_id`` or ``result_code`` is not a str.
        """
        if not isinstance(request_id, str):
            raise TypeError(
                f"request_id must be a str, "
                f"got {type(request_id).__name__}"
            )
        if not isinstance(result_code, str):
            raise TypeError(
                f"result_code must be a str, "
                f"got {type(result_code).__name__}"
            )
        return await self._call(
            "SmartCardEmulation.reportError",
            {"requestId": request_id, "resultCode": result_code},
        )
