from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cdpwave.browser.discovery import TargetInfo
from cdpwave.client import BrowserContext, CDPClient, CDPSession
from cdpwave.exceptions import DiscoveryError, SessionClosedError

_LAUNCH = "cdpwave.client.BrowserLauncher"
_CONNECT = "cdpwave.client.Connection"
_DISCOVERY = "cdpwave.client.TargetDiscovery"


class TestCDPSession:
    async def test_send_escape_hatch(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        conn.send_command.return_value = {"value": 42}
        session = CDPSession(conn, "S-1", "T-1")
        result = await session.send("Emulation.setDeviceMetricsOverride", {"width": 800})
        assert result == {"value": 42}
        conn.send_command.assert_called_with(
            "Emulation.setDeviceMetricsOverride",
            {"width": 800},
            session_id="S-1",
        )

    async def test_send_escape_hatch_no_params(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        conn.send_command.return_value = {}
        session = CDPSession(conn, "S-1", "T-1")
        await session.send("Page.enable")
        conn.send_command.assert_called_with(
            "Page.enable", None, session_id="S-1"
        )

    async def test_domain_properties(self) -> None:
        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        assert session.page is not None
        assert session.runtime is not None
        assert session.target is not None
        assert session.network is not None
        assert session.dom is not None
        assert session.log is not None
        assert session.console is not None

    async def test_close_detaches(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        session = CDPSession(conn, "S-1", "T-1")
        await session.close()
        conn.send_command.assert_called_with(
            "Target.detachFromTarget",
            {"sessionId": "S-1"},
        )
        assert session.is_closed is True

    async def test_close_detaches_before_marking_closed(self) -> None:
        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")

        call_order: list[str] = []

        async def _track_send_command(method: str, params: dict | None = None) -> dict:
            if not session.is_closed:
                call_order.append(f"send:{method}")
            else:
                call_order.append(f"send_after_closed:{method}")
            return {}

        conn.send_command.side_effect = _track_send_command

        original_closed = session.is_closed
        assert original_closed is False

        await session.close()

        assert call_order[0] == "send:Target.detachFromTarget"
        assert session.is_closed is True

    async def test_close_is_idempotent(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        session = CDPSession(conn, "S-1", "T-1")
        await session.close()
        await session.close()
        assert conn.send_command.call_count == 1

    async def test_context_manager_closes_on_exit(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        async with CDPSession(conn, "S-1", "T-1") as session:
            assert session.is_closed is False
        assert session.is_closed is True

    async def test_session_id_and_target_id(self) -> None:
        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        assert session.session_id == "S-1"
        assert session.target_id == "T-1"


class TestCDPClient:
    async def test_launch_creates_client(self) -> None:
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
            client = await CDPClient.launch(headless=True)

        mock_launcher.launch.assert_awaited_once()
        mock_conn_cls.assert_called_with(
            "ws://localhost:9222/devtools/browser/abc",
            max_retries=0,
            backoff_base=1.0,
            backoff_max=30.0,
        )
        mock_conn.connect.assert_awaited_once()
        assert client.is_closed is False

    async def test_launch_with_pipe(self) -> None:
        mock_launcher = AsyncMock()
        mock_launcher.launch.return_value = MagicMock(
            web_socket_debugger_url="",
            port=0,
            pipe=True,
        )
        mock_launcher.process = MagicMock()
        mock_pipe_conn = AsyncMock()
        mock_pipe_conn.is_closed = False

        with (
            patch(_LAUNCH, return_value=mock_launcher),
            patch("cdpwave.client.PipeConnection", return_value=mock_pipe_conn) as mock_pipe_cls,
        ):
            client = await CDPClient.launch(headless=True, pipe=True)

        mock_launcher.launch.assert_awaited_once()
        mock_pipe_cls.assert_called_once_with(
            read_fd=mock_launcher.pipe_fds[0],
            write_fd=mock_launcher.pipe_fds[1],
            process=mock_launcher.process,
        )
        mock_pipe_conn.connect.assert_awaited_once()
        assert client.is_closed is False

    async def test_connect_to_existing_browser(self) -> None:
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
            client = await CDPClient.connect(host="localhost", port=9222)

        mock_discovery.get_version.assert_awaited_once()
        mock_conn_cls.assert_called_with(
            "ws://localhost:9222/devtools/browser/xyz",
            max_retries=0,
            backoff_base=1.0,
            backoff_max=30.0,
        )
        mock_conn.connect.assert_awaited_once()
        assert client.is_closed is False

    async def test_new_page_returns_session(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"targetId": "T-1"},
            {"sessionId": "S-1"},
        ]
        client = CDPClient(conn)
        session = await client.new_page("https://example.com")
        assert isinstance(session, CDPSession)
        assert session.target_id == "T-1"
        assert session.session_id == "S-1"

    async def test_new_page_default_url(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"targetId": "T-1"},
            {"sessionId": "S-1"},
        ]
        client = CDPClient(conn)
        session = await client.new_page()
        assert session.target_id == "T-1"
        first_call = conn.send_command.call_args_list[0]
        assert first_call.args[1] == {"url": "about:blank"}

    async def test_get_pages(self) -> None:
        conn = AsyncMock()
        discovery = AsyncMock()
        page_target = TargetInfo(
            target_id="T-1",
            type="page",
            title="Test",
            url="https://example.com",
            web_socket_debugger_url="ws://localhost:9222/devtools/page/T-1",
        )
        worker_target = TargetInfo(
            target_id="T-2",
            type="worker",
            title="Worker",
            url="",
            web_socket_debugger_url=None,
        )
        discovery.list_targets.return_value = [page_target, worker_target]
        client = CDPClient(conn, discovery=discovery)
        pages = await client.get_pages()
        assert len(pages) == 1
        assert pages[0].type == "page"

    async def test_get_pages_no_discovery_raises(self) -> None:
        conn = AsyncMock()
        client = CDPClient(conn, discovery=None)
        with pytest.raises(DiscoveryError):
            await client.get_pages()

    async def test_connect_to_page(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        client = CDPClient(conn)
        session = await client.connect_to_page("T-1")
        assert session.target_id == "T-1"
        assert session.session_id == "S-1"

    async def test_close_closes_connection_and_launcher(self) -> None:
        conn = AsyncMock()
        launcher = AsyncMock()
        client = CDPClient(conn, launcher=launcher)
        await client.close()
        conn.close.assert_awaited_once()
        launcher.close.assert_awaited_once()

    async def test_close_without_launcher(self) -> None:
        conn = AsyncMock()
        client = CDPClient(conn, launcher=None)
        await client.close()
        conn.close.assert_awaited_once()

    async def test_context_manager_closes_on_exit(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        launcher = AsyncMock()
        async with CDPClient(conn, launcher=launcher) as client:
            assert client.is_closed is False
        conn.close.assert_awaited_once()
        launcher.close.assert_awaited_once()

    async def test_session_dispatcher_inherits_strict_events(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        client = CDPClient(conn, strict_events=True)
        session = await client.connect_to_page("T-1")
        assert session._dispatcher._strict is True

    async def test_session_dispatcher_inherits_on_event_error(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        on_error = MagicMock()
        client = CDPClient(conn, on_event_error=on_error)
        session = await client.connect_to_page("T-1")
        assert session._dispatcher._on_event_error is on_error

    async def test_session_without_client_has_default_dispatcher(self) -> None:
        conn = AsyncMock()
        session = CDPSession(conn, "S-1", "T-1")
        assert session._dispatcher._strict is False
        assert session._dispatcher._on_event_error is None

    async def test_invalidate_sessions_clears_all(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        client = CDPClient(conn)
        session = await client.connect_to_page("T-1")
        assert len(client._sessions) == 1
        assert session.is_closed is False

        await client._invalidate_sessions()

        assert len(client._sessions) == 0
        assert len(client._session_dispatchers) == 0
        assert session.is_closed is True

    async def test_invalidate_sessions_with_no_sessions(self) -> None:
        conn = AsyncMock()
        client = CDPClient(conn)
        assert len(client._sessions) == 0

        await client._invalidate_sessions()

        assert len(client._sessions) == 0
        assert len(client._session_dispatchers) == 0

    async def test_invalidate_sessions_clears_multiple(self) -> None:
        conn = AsyncMock()
        conn.send_command.side_effect = [
            {"sessionId": "S-1"},
            {"sessionId": "S-2"},
            {"sessionId": "S-3"},
        ]
        client = CDPClient(conn)
        s1 = await client.connect_to_page("T-1")
        s2 = await client.connect_to_page("T-2")
        s3 = await client.connect_to_page("T-3")
        assert len(client._sessions) == 3

        await client._invalidate_sessions()

        assert len(client._sessions) == 0
        assert len(client._session_dispatchers) == 0
        assert s1.is_closed is True
        assert s2.is_closed is True
        assert s3.is_closed is True

    async def test_invalidate_sessions_is_idempotent(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        client = CDPClient(conn)
        await client.connect_to_page("T-1")

        await client._invalidate_sessions()
        await client._invalidate_sessions()

        assert len(client._sessions) == 0

    async def test_invalidate_sessions_clears_dispatcher_handlers(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        client = CDPClient(conn)
        session = await client.connect_to_page("T-1")
        handler = MagicMock()
        session.on("Page.loadEventFired", handler)
        assert len(session._dispatcher._handlers) > 0

        await client._invalidate_sessions()

        assert len(session._dispatcher._handlers) == 0


class TestAutoAttachRouting:
    """Regression tests for Target.* event routing through _event_callback.

    The top-level ``sessionId`` of a CDP message is the parent session
    that issued ``setAutoAttach``; ``params["sessionId"]`` is the child.
    """

    async def test_attached_to_target_creates_sub_session(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        parent = CDPSession(conn, "P-1", "T-1", client=client)
        client._sessions["P-1"] = parent

        await client._event_callback(
            "Target.attachedToTarget",
            {
                "sessionId": "CHILD-1",
                "targetInfo": {"targetId": "T-CHILD", "type": "iframe"},
            },
            "P-1",
        )

        assert "CHILD-1" in parent._sub_sessions
        assert "CHILD-1" in client._sessions
        assert client._sessions["CHILD-1"]._target_id == "T-CHILD"

    async def test_attached_to_target_dispatched_to_handlers(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        parent = CDPSession(conn, "P-1", "T-1", client=client)
        client._sessions["P-1"] = parent
        captured: list[dict] = []

        async def _handler(params: dict) -> None:
            captured.append(params)

        parent.on("Target.attachedToTarget", _handler)

        params = {
            "sessionId": "CHILD-1",
            "targetInfo": {"targetId": "T-CHILD", "type": "worker"},
        }
        await client._event_callback("Target.attachedToTarget", params, "P-1")

        assert captured == [params]

    async def test_attached_to_target_browser_level_dispatches(self) -> None:
        """Events with no top-level sessionId go to client.on() handlers."""
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        captured: list[dict] = []

        async def _handler(params: dict) -> None:
            captured.append(params)

        client.on("Target.attachedToTarget", _handler)

        params = {
            "sessionId": "CHILD-1",
            "targetInfo": {"targetId": "T-CHILD", "type": "worker"},
        }
        await client._event_callback("Target.attachedToTarget", params, None)

        assert captured == [params]

    async def test_detached_from_target_cleans_sub_session(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        parent = CDPSession(conn, "P-1", "T-1", client=client)
        client._sessions["P-1"] = parent
        parent._handle_attached_to_target({
            "sessionId": "CHILD-1",
            "targetInfo": {"targetId": "T-CHILD", "type": "worker"},
        })
        child = parent._sub_sessions["CHILD-1"]

        await client._event_callback(
            "Target.detachedFromTarget",
            {"sessionId": "CHILD-1"},
            "P-1",
        )

        assert "CHILD-1" not in parent._sub_sessions
        assert child.is_closed
        assert "CHILD-1" not in client._sessions
        assert "CHILD-1" not in client._session_dispatchers


class TestBrowserContextGuards:
    async def test_new_page_on_closed_context_raises(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        context = BrowserContext(client, "ctx-1")
        context._closed = True

        with pytest.raises(SessionClosedError):
            await context.new_page()


class TestLaunchCleanup:
    async def test_launch_connection_failure_closes_launcher(self) -> None:
        """If the WebSocket handshake fails after the browser starts,
        the browser process must be cleaned up."""
        mock_launcher = AsyncMock()
        mock_launcher.launch.return_value = MagicMock(
            web_socket_debugger_url="ws://127.0.0.1:1234/devtools/browser/x",
            port=1234,
            pipe=False,
        )
        mock_conn = AsyncMock()
        mock_conn.connect.side_effect = OSError("connection refused")

        with (
            patch(_LAUNCH, return_value=mock_launcher),
            patch(_CONNECT, return_value=mock_conn),
            patch(_DISCOVERY),
            pytest.raises(OSError, match="connection refused"),
        ):
            await CDPClient.launch(headless=True)

        mock_launcher.close.assert_awaited_once()

    async def test_connect_failure_closes_connection(self) -> None:
        mock_conn = AsyncMock()
        mock_conn.connect.side_effect = OSError("connection refused")

        with (
            patch(_CONNECT, return_value=mock_conn),
            patch(_DISCOVERY),
            pytest.raises(OSError, match="connection refused"),
        ):
            await CDPClient.connect(ws_url="ws://127.0.0.1:1234/x")

        mock_conn.close.assert_awaited_once()


class TestClientSystemInfo:
    def test_client_exposes_browser_level_system_info(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        client._system_info = MagicMock()
        assert client.system_info is client._system_info

    async def test_client_system_info_sends_browser_target(self) -> None:
        conn = AsyncMock()
        conn.is_closed = False
        conn.send_command.return_value = {"gpu": {}}
        client = CDPClient(conn)

        result = await client.system_info.get_info()

        conn.send_command.assert_awaited_once_with("SystemInfo.getInfo", None)
        assert result == {"gpu": {}}
