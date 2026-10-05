"""Unit tests for PipeConnection NUL-delimited framing.

Chrome's ``--remote-debugging-pipe`` protocol sends JSON messages
terminated by a NUL byte on fd 4 (browser → client).
"""

import asyncio
from typing import Any

import pytest

from cdpwave.exceptions import CommandError, ConnectionClosedError
from cdpwave.transport.pipe_connection import PipeConnection


def _conn() -> PipeConnection:
    return PipeConnection(read_fd=0, write_fd=1)


class TestNulFraming:
    async def test_single_message_resolves_command(self) -> None:
        conn = _conn()
        future = conn._correlator.register(1)

        conn._on_data(b'{"id": 1, "result": {"ok": true}}\x00')

        assert await future == {"ok": True}

    async def test_multiple_messages_in_one_chunk(self) -> None:
        conn = _conn()
        f1 = conn._correlator.register(1)
        f2 = conn._correlator.register(2)

        conn._on_data(
            b'{"id": 1, "result": {"a": 1}}\x00'
            b'{"id": 2, "result": {"b": 2}}\x00'
        )

        assert await f1 == {"a": 1}
        assert await f2 == {"b": 2}

    async def test_partial_message_waits_for_delimiter(self) -> None:
        conn = _conn()
        future = conn._correlator.register(1)

        conn._on_data(b'{"id": 1, "result"')
        assert not future.done()

        conn._on_data(b': {"ok": true}}\x00')
        assert await future == {"ok": True}

    async def test_error_response_rejects_future(self) -> None:
        conn = _conn()
        future = conn._correlator.register(1)

        conn._on_data(b'{"id": 1, "error": {"code": -32601, "message": "nope"}}\x00')

        with pytest.raises(CommandError) as exc:
            await future
        assert exc.value.code == -32601

    async def test_malformed_message_skipped(self) -> None:
        conn = _conn()
        future = conn._correlator.register(1)

        conn._on_data(b'not json\x00')
        assert not future.done()

        conn._on_data(b'{"id": 1, "result": {"ok": true}}\x00')
        assert await future == {"ok": True}

    async def test_event_dispatched_to_callback(self) -> None:
        events: list[tuple[str, dict[str, Any], str | None]] = []

        async def _cb(method: str, params: dict[str, Any], session: str | None) -> None:
            events.append((method, params, session))

        conn = PipeConnection(read_fd=0, write_fd=1, event_callback=_cb)
        conn._on_data(
            b'{"method": "Page.loadEventFired", "params": {"t": 1},'
            b' "sessionId": "S-1"}\x00'
        )
        await asyncio.sleep(0.01)

        assert events == [("Page.loadEventFired", {"t": 1}, "S-1")]

    async def test_connection_lost_rejects_pending(self) -> None:
        conn = _conn()
        future = conn._correlator.register(1)

        conn._on_connection_lost()

        with pytest.raises(ConnectionClosedError):
            await future
        assert conn.is_closed

    async def test_send_command_rejects_when_closed(self) -> None:
        conn = _conn()
        conn._closed = True

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    async def test_send_command_rejects_without_transport(self) -> None:
        conn = _conn()

        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Page.enable")

    def test_url_is_pipe(self) -> None:
        assert _conn().url == "pipe://"
