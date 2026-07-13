from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cdpwave.browser.discovery import TargetInfo
from cdpwave.client import CDPClient, CDPSession

_LAUNCH = "cdpwave.client.BrowserLauncher"
_CONNECT = "cdpwave.client.Connection"
_DISCOVERY = "cdpwave.client.TargetDiscovery"


class TestCDPSession:
    async def test_send_escape_hatch(self) -> None:
        conn = AsyncMock()
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
        with pytest.raises(RuntimeError):
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
