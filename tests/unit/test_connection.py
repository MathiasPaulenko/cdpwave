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

    async def test_reconnect_calls_on_reconnect_callback(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn._reconnect()

        assert result is True
        callback.assert_awaited_once()
        await conn.close()

    async def test_reconnect_no_callback_when_all_fail(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=2,
            backoff_base=0.01,
            on_reconnect=callback,
        )

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.side_effect = OSError("connection refused")
            result = await conn._reconnect()

        assert result is False
        callback.assert_not_awaited()

    async def test_reconnect_no_callback_when_not_set(self) -> None:
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn._reconnect()

        assert result is True
        await conn.close()

    async def test_reconnect_first_fails_second_succeeds(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=3,
            backoff_base=0.01,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.side_effect = [
                OSError("first attempt failed"),
                fake_ws,
            ]
            result = await conn._reconnect()

        assert result is True
        callback.assert_awaited_once()
        await conn.close()

    async def test_reconnect_callback_exception_caught_by_retry(self) -> None:
        callback = AsyncMock(side_effect=ValueError("callback boom"))
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn._reconnect()

        assert result is False
        callback.assert_awaited_once()
        await conn.close()

    async def test_reconnect_max_retries_zero_returns_false(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=0,
            on_reconnect=callback,
        )

        result = await conn._reconnect()

        assert result is False
        callback.assert_not_awaited()

    async def test_reconnect_with_zero_backoff(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.0,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn._reconnect()

        assert result is True
        callback.assert_awaited_once()
        await conn.close()

    async def test_reconnect_concurrent_serialized_by_lock(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.05,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            results = await asyncio.gather(
                conn._reconnect(),
                conn._reconnect(),
            )

        assert results == [True, True]
        assert callback.await_count == 2
        await conn.close()

    async def test_reconnect_restores_receive_loop(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
            on_reconnect=callback,
        )
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            original_task = conn._receive_task
            result = await conn._reconnect()

        assert result is True
        assert conn._receive_task is not None
        assert conn._receive_task is not original_task
        await conn.close()

    async def test_receive_loop_triggers_reconnect_on_close(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
            on_reconnect=callback,
        )

        class ClosingWS:
            async def close(self) -> None:
                pass

            def __aiter__(self) -> "ClosingWS":
                return self

            async def __anext__(self) -> str:
                raise websockets.ConnectionClosed(None, None)

        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.side_effect = [ClosingWS(), fake_ws]
            await conn.connect()
            await asyncio.sleep(0.2)

        assert conn.is_closed is False
        callback.assert_awaited_once()
        await conn.close()

    async def test_receive_loop_reconnect_exhausted_marks_closed(self) -> None:
        callback = AsyncMock()
        conn = Connection(
            "ws://localhost:9222",
            max_retries=1,
            backoff_base=0.01,
            on_reconnect=callback,
        )

        class ClosingWS:
            async def close(self) -> None:
                pass

            def __aiter__(self) -> "ClosingWS":
                return self

            async def __anext__(self) -> str:
                raise websockets.ConnectionClosed(None, None)

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.side_effect = [ClosingWS(), OSError("refused")]
            await conn.connect()
            await asyncio.sleep(0.2)

        assert conn.is_closed is True
        callback.assert_not_awaited()
