import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cdpwave.browser.launcher import BrowserLauncher
from cdpwave.client import CDPClient, CDPSession
from cdpwave.exceptions import (
    CommandTimeoutError,
    ConnectionClosedError,
    LaunchTimeoutError,
    SessionClosedError,
)
from cdpwave.transport.connection import Connection

_WS_CONNECT = "cdpwave.transport.connection.websockets.connect"


class FakeWebSocket:
    def __init__(self, responses: list[str] | None = None) -> None:
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        for r in responses or []:
            self._queue.put_nowait(r)
        self._closed = False

    async def send(self, message: str) -> None:
        pass

    async def close(self) -> None:
        self._closed = True

    def __aiter__(self) -> "FakeWebSocket":
        return self

    async def __anext__(self) -> str:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=0.5)
        except TimeoutError:
            raise StopAsyncIteration from None


class TestConnectionTimeouts:
    async def test_send_command_with_timeout_raises_command_timeout(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            with pytest.raises(CommandTimeoutError):
                await conn.send_command("Runtime.evaluate", timeout=0.05)

        await conn.close()

    async def test_send_command_timeout_none_uses_default(self) -> None:
        conn = Connection("ws://localhost:9222", default_timeout=0.05)
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            with pytest.raises(CommandTimeoutError):
                await conn.send_command("Runtime.evaluate")

        await conn.close()

    async def test_send_command_timeout_zero_no_timeout(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({"id": 1, "result": {"value": 42}})
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn.send_command("Runtime.evaluate", timeout=0)

        assert result == {"value": 42}
        await conn.close()

    async def test_send_command_negative_timeout_no_timeout(self) -> None:
        conn = Connection("ws://localhost:9222")
        response = json.dumps({"id": 1, "result": {}})
        fake_ws = FakeWebSocket([response])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()
            result = await conn.send_command("Page.enable", timeout=-1)

        assert result == {}
        await conn.close()

    async def test_url_property(self) -> None:
        conn = Connection("ws://localhost:9222/devtools/browser/abc")
        assert conn.url == "ws://localhost:9222/devtools/browser/abc"


class TestConnectionClose:
    async def test_close_idempotent(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()

        await conn.close()
        await conn.close()
        assert conn.is_closed is True

    async def test_close_cancels_receive_task(self) -> None:
        conn = Connection("ws://localhost:9222")
        fake_ws = FakeWebSocket([])

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = fake_ws
            await conn.connect()

        assert conn._receive_task is not None
        await conn.close()
        assert conn._receive_task.cancelled() or conn._receive_task.done()

    async def test_receive_loop_connection_closed_ok_rejects_all(self) -> None:
        import websockets

        conn = Connection("ws://localhost:9222")

        class ClosedOKWS:
            async def send(self, message: str) -> None:
                pass

            async def close(self) -> None:
                pass

            def __aiter__(self) -> "ClosedOKWS":
                return self

            async def __anext__(self) -> str:
                raise websockets.ConnectionClosedOK(None, None)

        mock_ws = ClosedOKWS()

        with patch(_WS_CONNECT, new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = mock_ws
            await conn.connect()

        await asyncio.sleep(0.1)
        assert conn.is_closed is True


class TestCDPSessionClose:
    async def test_send_after_close_raises_session_closed(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)

        await session.close()
        with pytest.raises(SessionClosedError):
            await session.send("Page.enable")

    async def test_close_idempotent(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)

        await session.close()
        await session.close()
        assert session.is_closed is True

    async def test_close_with_detach_failure_does_not_propagate(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = ConnectionClosedError("detach failed")
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)

        await session.close()
        assert session.is_closed is True

    async def test_aexit_calls_close_on_exception(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)

        with pytest.raises(ValueError):
            async with session:
                raise ValueError("body error")

        assert session.is_closed is True


class TestCDPClientClose:
    async def test_close_idempotent(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)

        await client.close()
        await client.close()
        assert client.is_closed is True

    async def test_close_with_session_detach_failure_does_not_propagate(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = ConnectionClosedError("detach failed")
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session

        await client.close()
        assert client.is_closed is True

    async def test_close_with_launcher_failure_does_not_propagate(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        launcher = AsyncMock()
        launcher.close.side_effect = Exception("launcher error")
        client = CDPClient(conn, launcher=launcher)

        await client.close()
        assert client.is_closed is True

    async def test_aexit_calls_close_on_exception(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)

        with pytest.raises(ValueError):
            async with client:
                raise ValueError("body error")

        assert client.is_closed is True

    async def test_is_connected_property(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        assert client.is_connected is True

        conn.is_closed = True
        assert client.is_connected is False

    async def test_close_clears_sessions_and_dispatchers(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session

        await client.close()
        assert "S-1" not in client._session_dispatchers
        assert len(client._sessions) == 0
        assert session.is_closed is True


class TestTargetDetachedFromTarget:
    async def test_known_session_marked_closed(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        client._sessions["S-1"] = session

        await client._event_callback(
            "Target.detachedFromTarget",
            {"sessionId": "S-1"},
            None,
        )

        assert session.is_closed is True
        assert "S-1" not in client._session_dispatchers
        assert "S-1" not in client._sessions

    async def test_unknown_session_logs_warning_no_crash(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)

        await client._event_callback(
            "Target.detachedFromTarget",
            {"sessionId": "UNKNOWN"},
            None,
        )


class TestLauncherRobustness:
    async def test_launch_timeout_raises_launch_timeout_error(self) -> None:
        launcher = BrowserLauncher(browser_path="fake-browser")

        with (
            patch(
                "cdpwave.browser.launcher.asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
            ) as mock_exec,
            patch(
                "cdpwave.browser.launcher._fetch_version",
                side_effect=Exception("not ready"),
            ),
        ):
            mock_proc = MagicMock()
            mock_proc.returncode = None
            mock_exec.return_value = mock_proc

            with pytest.raises(LaunchTimeoutError):
                await launcher.launch(timeout=0.3)

    async def test_close_terminate_then_kill(self) -> None:
        launcher = BrowserLauncher(browser_path="fake-browser")
        launcher._temp_dir = None

        mock_proc = AsyncMock()
        mock_proc.returncode = None
        mock_proc.terminate = MagicMock()
        mock_proc.kill = MagicMock()

        wait_call_count = 0

        async def mock_wait() -> int:
            nonlocal wait_call_count
            wait_call_count += 1
            if wait_call_count == 1:
                raise TimeoutError()
            return 0

        mock_proc.wait = mock_wait
        launcher._process = mock_proc

        await launcher.close()
        mock_proc.terminate.assert_called_once()
        mock_proc.kill.assert_called_once()
        assert launcher._process is None

    async def test_close_cleanup_temp_dir(self) -> None:
        import tempfile

        launcher = BrowserLauncher(browser_path="fake-browser")
        temp_dir = tempfile.mkdtemp(prefix="cdpwave-test-")
        launcher._temp_dir = temp_dir

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        launcher._process = mock_proc

        await launcher.close()
        import os
        assert not os.path.exists(temp_dir)  # noqa: ASYNC240
        assert launcher._temp_dir is None

    async def test_close_idempotent(self) -> None:
        launcher = BrowserLauncher(browser_path="fake-browser")

        await launcher.close()
        await launcher.close()
        assert launcher._process is None
        assert launcher._info is None
