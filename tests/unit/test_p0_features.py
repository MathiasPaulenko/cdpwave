"""Unit tests for P0 features: reconnection, auto-attach, browser contexts."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cdpwave.client import BrowserContext, CDPClient, CDPSession
from cdpwave.exceptions import ProtocolError
from cdpwave.transport.connection import Connection

_LAUNCH = "cdpwave.client.BrowserLauncher"
_CONNECT = "cdpwave.client.Connection"
_DISCOVERY = "cdpwave.client.TargetDiscovery"


class TestReconnection:
    async def test_connection_accepts_reconnect_params(self) -> None:
        conn = Connection(
            "ws://localhost:9222",
            max_retries=5,
            backoff_base=0.5,
            backoff_max=10.0,
        )
        assert conn._max_retries == 5
        assert conn._backoff_base == 0.5
        assert conn._backoff_max == 10.0

    async def test_connection_defaults_no_reconnect(self) -> None:
        conn = Connection("ws://localhost:9222")
        assert conn._max_retries == 0

    async def test_launch_passes_reconnect_params(self) -> None:
        mock_launcher = AsyncMock()
        mock_launcher.launch.return_value = MagicMock(
            web_socket_debugger_url="ws://localhost:9222/devtools/browser/abc",
            port=9222,
            pipe=False,
        )
        mock_conn = AsyncMock()
        mock_conn.is_closed = False
        mock_discovery = MagicMock()

        with (
            patch(_LAUNCH, return_value=mock_launcher),
            patch(_CONNECT, return_value=mock_conn) as mock_conn_cls,
            patch(_DISCOVERY, return_value=mock_discovery),
        ):
            await CDPClient.launch(
                headless=True,
                max_retries=3,
                backoff_base=2.0,
                backoff_max=60.0,
            )

        mock_conn_cls.assert_called_with(
            "ws://localhost:9222/devtools/browser/abc",
            max_retries=3,
            backoff_base=2.0,
            backoff_max=60.0,
        )

    async def test_connect_passes_reconnect_params(self) -> None:
        mock_discovery = AsyncMock()
        mock_version = MagicMock()
        mock_version.web_socket_debugger_url = "ws://localhost:9222/devtools/browser/xyz"
        mock_discovery.get_version.return_value = mock_version
        mock_conn = AsyncMock()
        mock_conn.is_closed = False

        with (
            patch(_DISCOVERY, return_value=mock_discovery),
            patch(_CONNECT, return_value=mock_conn) as mock_conn_cls,
        ):
            await CDPClient.connect(
                host="localhost",
                port=9222,
                max_retries=5,
            )

        mock_conn_cls.assert_called_with(
            "ws://localhost:9222/devtools/browser/xyz",
            max_retries=5,
            backoff_base=1.0,
            backoff_max=30.0,
        )


class TestAutoAttach:
    async def test_new_page_with_auto_attach(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"targetId": "T-1"},
            {"sessionId": "S-1"},
            {},
        ]
        client = CDPClient(conn)
        session = await client.new_page("https://example.com", auto_attach=True)
        assert session._auto_attach_enabled is True
        assert session.session_id == "S-1"

    async def test_new_page_without_auto_attach(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"targetId": "T-1"},
            {"sessionId": "S-1"},
        ]
        client = CDPClient(conn)
        session = await client.new_page("https://example.com")
        assert session._auto_attach_enabled is False

    async def test_sub_sessions_empty_by_default(self) -> None:
        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        assert session.sub_sessions == []

    async def test_handle_attached_to_target_creates_sub_session(self) -> None:
        conn = AsyncMock()
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        session._handle_attached_to_target({
            "sessionId": "SUB-1",
            "targetInfo": {"targetId": "SUB-T-1", "type": "iframe"},
        })
        assert len(session.sub_sessions) == 1
        assert session.sub_sessions[0].session_id == "SUB-1"

    async def test_handle_detached_from_target_removes_sub_session(self) -> None:
        conn = AsyncMock()
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        session._handle_attached_to_target({
            "sessionId": "SUB-1",
            "targetInfo": {"targetId": "SUB-T-1", "type": "iframe"},
        })
        assert len(session.sub_sessions) == 1
        session._handle_detached_from_target({"sessionId": "SUB-1"})
        assert len(session.sub_sessions) == 0

    async def test_close_cleans_up_sub_sessions(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        session._handle_attached_to_target({
            "sessionId": "SUB-1",
            "targetInfo": {"targetId": "SUB-T-1", "type": "iframe"},
        })
        await session.close()
        assert len(session.sub_sessions) == 0
        assert "SUB-1" not in client._sessions


class TestBrowserContext:
    async def test_new_context_returns_browser_context(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"browserContextId": "CTX-1"}
        client = CDPClient(conn)
        context = await client.new_context()
        assert isinstance(context, BrowserContext)
        assert context.context_id == "CTX-1"
        assert context.is_closed is False

    async def test_new_context_missing_id_raises(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        client = CDPClient(conn)
        with pytest.raises(ProtocolError):
            await client.new_context()

    async def test_context_new_page(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"browserContextId": "CTX-1"},
            {"targetId": "T-CTX-1"},
            {"sessionId": "S-CTX-1"},
        ]
        client = CDPClient(conn)
        context = await client.new_context()
        session = await context.new_page("https://example.com")
        assert isinstance(session, CDPSession)
        assert session.target_id == "T-CTX-1"
        assert session.session_id == "S-CTX-1"

    async def test_context_close_disposes(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"browserContextId": "CTX-1"}
        client = CDPClient(conn)
        context = await client.new_context()
        await context.close()
        assert context.is_closed is True
        assert conn.send_command.call_count >= 2

    async def test_context_close_is_idempotent(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"browserContextId": "CTX-1"}
        client = CDPClient(conn)
        context = await client.new_context()
        await context.close()
        call_count = conn.send_command.call_count
        await context.close()
        assert conn.send_command.call_count == call_count

    async def test_context_context_manager(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"browserContextId": "CTX-1"}
        client = CDPClient(conn)
        async with await client.new_context() as context:
            assert context.is_closed is False
        assert context.is_closed is True
