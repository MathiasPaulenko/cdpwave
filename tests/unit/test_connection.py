import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest
import websockets

from cdpwave.exceptions import CommandError, CommandTimeoutError, ConnectionClosedError
from cdpwave.transport.connection import Connection

_WS_CONNECT = "cdpwave.transport.connection.websockets.connect"


class FakeWebSocket:
    def __init__(self, responses: list[str]) -> None:
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        for r in responses:
            self._queue.put_nowait(r)
        self._sent: list[str] = []
        self._closed = False

    async def send(self, message: str) -> None:
        self._sent.append(message)

    async def close(self) -> None:
        self._closed = True

    def __aiter__(self) -> "FakeWebSocket":
        return self

    async def __anext__(self) -> str:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=2.0)
        except TimeoutError:
            raise StopAsyncIteration from None

    @property
    def sent_messages(self) -> list[str]:
        return self._sent


class TestConnection:
    async def test_connect_starts_receive_loop(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()

        assert conn.is_closed is False
        assert conn._receive_task is not None
        await conn.close()

    async def test_send_command_success(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({"id": 1, "result": {"targetInfos": []}})
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn.send_command("Target.getTargets")

        assert result == {"targetInfos": []}
        sent = json.loads(fake_ws.sent_messages[0])
        assert sent["id"] == 1
        assert sent["method"] == "Target.getTargets"
        assert "params" not in sent
        await conn.close()

    async def test_send_command_with_params(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({"id": 1, "result": {"targetId": "ABC"}})
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn.send_command(
                "Target.createTarget", {"url": "https://example.com"}
            )

        assert result == {"targetId": "ABC"}
        sent = json.loads(fake_ws.sent_messages[0])
        assert sent["params"] == {"url": "https://example.com"}
        await conn.close()

    async def test_send_command_with_session_id(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({
            "id": 1,
            "result": {"value": {"type": "string", "value": "Example"}},
        })
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            await conn.send_command(
                "Runtime.evaluate",
                {"expression": "document.title"},
                session_id="SESSION-123",
            )

        sent = json.loads(fake_ws.sent_messages[0])
        assert sent["sessionId"] == "SESSION-123"
        assert sent["params"] == {"expression": "document.title"}
        await conn.close()

    async def test_send_command_error_response(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({
            "id": 1,
            "error": {"code": -32602, "message": "Invalid params"},
        })
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            with pytest.raises(CommandError) as exc_info:
                await conn.send_command("Page.navigate", {"url": "invalid"})

        assert exc_info.value.code == -32602
        assert exc_info.value.message == "Invalid params"
        await conn.close()

    async def test_send_command_on_closed_connection(self) -> None:
        conn = Connection("ws://localhost:9222")
        await conn.close()
        with pytest.raises(ConnectionClosedError):
            await conn.send_command("Target.getTargets")

    async def test_close_is_idempotent(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()

        await conn.close()
        await conn.close()
        assert conn.is_closed is True

    async def test_close_rejects_pending(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()

        cmd_id = conn._correlator.next_id()
        fut = conn._correlator.register(cmd_id)

        await conn.close()
        assert fut.done()
        assert isinstance(fut.exception(), ConnectionClosedError)

    async def test_receive_loop_handles_connection_closed(self) -> None:
        conn = Connection("ws://localhost:9222")

        class ClosedWS:
            async def close(self) -> None:
                pass

            def __aiter__(self) -> "ClosedWS":
                return self

            async def __anext__(self) -> str:
                raise websockets.ConnectionClosed(None, None)

        mock_ws = ClosedWS()

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = mock_ws
            await conn.connect()

        await asyncio.sleep(0.1)
        assert conn.is_closed is True

    async def test_send_command_timeout(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            with pytest.raises(CommandTimeoutError):
                await conn.send_command("Runtime.evaluate", timeout=0.05)

        await conn.close()

    async def test_events_logged_not_crashed(self) -> None:
        conn = Connection("ws://localhost:9222")
        event_msg = json.dumps({
            "method": "Page.loadEventFired",
            "params": {},
            "sessionId": "SESSION-1",
        })
        response = json.dumps({"id": 1, "result": {}})
        fake_ws = FakeWebSocket([event_msg, response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn.send_command("Page.enable")

        assert result == {}
        await conn.close()
