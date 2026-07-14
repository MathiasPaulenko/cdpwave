from unittest.mock import AsyncMock, MagicMock

import pytest

from cdpwave.exceptions import ConnectionClosedError
from cdpwave.transport.connection import Connection


def _make_connection(max_retries: int = 0) -> Connection:
    return Connection(
        url="ws://localhost:9222",
        max_retries=max_retries,
    )


class TestSendCommandRaceCondition:
    async def test_ws_none_after_reconnect_block_raises(self) -> None:
        conn = _make_connection(max_retries=3)
        conn._closed = False
        conn._ws = None

        async def _lock_aenter() -> None:
            conn._ws = AsyncMock()

        async def _lock_aexit(*args: object) -> None:
            conn._ws = None

        conn._reconnect_lock = MagicMock()
        conn._reconnect_lock.__aenter__ = AsyncMock(side_effect=_lock_aenter)
        conn._reconnect_lock.__aexit__ = AsyncMock(side_effect=_lock_aexit)

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    async def test_closed_set_after_reconnect_block_raises(self) -> None:
        conn = _make_connection(max_retries=3)
        conn._closed = False
        conn._ws = None

        async def _lock_aenter() -> None:
            conn._ws = AsyncMock()
            conn._closed = False

        async def _lock_aexit(*args: object) -> None:
            conn._closed = True

        conn._reconnect_lock = MagicMock()
        conn._reconnect_lock.__aenter__ = AsyncMock(side_effect=_lock_aenter)
        conn._reconnect_lock.__aexit__ = AsyncMock(side_effect=_lock_aexit)

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    async def test_closed_true_raises_before_send(self) -> None:
        conn = _make_connection(max_retries=0)
        conn._closed = True
        conn._ws = AsyncMock()

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    async def test_ws_none_no_retries_raises(self) -> None:
        conn = _make_connection(max_retries=0)
        conn._closed = False
        conn._ws = None

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    async def test_ws_none_with_retries_still_none_in_lock_raises(self) -> None:
        conn = _make_connection(max_retries=3)
        conn._closed = False
        conn._ws = None

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")
