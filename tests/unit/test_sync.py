"""Unit tests for sync API wrapper."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from cdpwave.sync import SyncCDPClient, SyncCDPSession, _SyncDomainWrapper, _SyncRunner


class TestSyncRunner:
    def test_run_executes_coroutine(self) -> None:
        runner = _SyncRunner()

        async def _coro() -> int:
            return 42

        try:
            assert runner.run(_coro()) == 42
        finally:
            runner.shutdown()

    def test_run_with_running_loop(self) -> None:
        """Sync calls from inside a running loop run on the runner's loop."""
        runner = _SyncRunner()

        async def _inner() -> int:
            return 99

        async def _outer() -> None:
            assert runner.run(_inner()) == 99

        try:
            asyncio.run(_outer())
        finally:
            runner.shutdown()

    def test_shared_loop_across_calls(self) -> None:
        """All calls share a single persistent event loop."""
        runner = _SyncRunner()

        async def _get_loop() -> asyncio.AbstractEventLoop:
            return asyncio.get_running_loop()

        try:
            loop1 = runner.run(_get_loop())
            loop2 = runner.run(_get_loop())
            assert loop1 is loop2
        finally:
            runner.shutdown()

    def test_state_persists_across_calls(self) -> None:
        """Objects created on the loop stay usable across calls."""
        runner = _SyncRunner()

        async def _make() -> asyncio.Event:
            return asyncio.Event()

        async def _set_and_get(ev: asyncio.Event) -> bool:
            ev.set()
            return ev.is_set()

        try:
            ev = runner.run(_make())
            assert runner.run(_set_and_get(ev)) is True
        finally:
            runner.shutdown()

    def test_run_after_shutdown_raises(self) -> None:
        runner = _SyncRunner()
        runner.shutdown()

        async def _coro() -> int:
            return 1

        with pytest.raises(RuntimeError):
            runner.run(_coro())

    def test_shutdown_idempotent(self) -> None:
        runner = _SyncRunner()
        runner.shutdown()
        runner.shutdown()

    def test_run_from_loop_thread_raises(self) -> None:
        """Calling run() from inside the runner's loop deadlocks — guarded."""
        runner = _SyncRunner()

        async def _nested() -> None:
            async def _inner() -> int:
                return 1

            runner.run(_inner())

        try:
            with pytest.raises(RuntimeError, match="sync API"):
                runner.run(_nested())
        finally:
            runner.shutdown()


class TestSyncCDPSession:
    def test_send_delegates(self) -> None:
        mock_session = MagicMock()
        mock_session.send = AsyncMock(return_value={"ok": True})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.send("Page.navigate", {"url": "https://example.com"})
        assert result == {"ok": True}
        mock_session.send.assert_called_once_with(
            "Page.navigate", {"url": "https://example.com"},
        )
        sync_session._runner.shutdown()

    def test_close_delegates(self) -> None:
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        sync_session = SyncCDPSession(mock_session)
        sync_session.close()
        mock_session.close.assert_called_once()

    def test_wait_for_selector_delegates(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_selector = AsyncMock(return_value=42)
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.wait_for_selector(".btn", timeout=1.0)
        assert result == 42
        sync_session._runner.shutdown()

    def test_wait_for_event_delegates(self) -> None:
        mock_session = MagicMock()
        mock_session.wait_for_event = AsyncMock(return_value={"type": "x"})
        sync_session = SyncCDPSession(mock_session)
        result = sync_session.wait_for_event("Page.loadEventFired", timeout=1.0)
        assert result == {"type": "x"}
        mock_session.wait_for_event.assert_called_once_with(
            "Page.loadEventFired", timeout=1.0
        )
        sync_session._runner.shutdown()

    def test_domain_attribute_wrapped(self) -> None:
        mock_domain = MagicMock()
        mock_domain._send = MagicMock()
        mock_session = MagicMock()
        mock_session.page = mock_domain
        sync_session = SyncCDPSession(mock_session)
        assert isinstance(sync_session.page, _SyncDomainWrapper)
        sync_session._runner.shutdown()

    def test_non_domain_attribute_passthrough(self) -> None:
        mock_session = MagicMock()
        mock_session.page = "page_domain"
        sync_session = SyncCDPSession(mock_session)
        assert sync_session.page == "page_domain"
        sync_session._runner.shutdown()

    def test_on_off_delegate(self) -> None:
        mock_session = MagicMock()
        handler = MagicMock()
        sync_session = SyncCDPSession(mock_session)
        sync_session.on("Page.loadEventFired", handler)
        mock_session.on.assert_called_once_with("Page.loadEventFired", handler)
        sync_session.off("Page.loadEventFired", handler)
        mock_session.off.assert_called_once_with("Page.loadEventFired", handler)
        sync_session._runner.shutdown()

    def test_context_manager(self) -> None:
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        with SyncCDPSession(mock_session):
            pass
        mock_session.close.assert_called_once()


class TestSyncCDPClient:
    def test_context_manager(self) -> None:
        mock_client = MagicMock()
        mock_client.close = AsyncMock()
        with SyncCDPClient(mock_client):
            pass
        mock_client.close.assert_called_once()

    def test_new_page(self) -> None:
        mock_session = MagicMock()
        mock_session.session_id = "S1"
        mock_client = MagicMock()
        mock_client.new_page = AsyncMock(return_value=mock_session)
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.new_page("https://example.com")
        assert isinstance(result, SyncCDPSession)
        assert result.session_id == "S1"
        assert result._runner is sync_client._runner
        sync_client._runner.shutdown()

    def test_connect_to_page(self) -> None:
        mock_session = MagicMock()
        mock_session.target_id = "T1"
        mock_client = MagicMock()
        mock_client.connect_to_page = AsyncMock(return_value=mock_session)
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.connect_to_page("T1")
        assert isinstance(result, SyncCDPSession)
        assert result.target_id == "T1"
        sync_client._runner.shutdown()

    def test_get_pages(self) -> None:
        mock_client = MagicMock()
        mock_client.get_pages = AsyncMock(return_value=[])
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.get_pages()
        assert result == []
        sync_client._runner.shutdown()

    def test_send(self) -> None:
        mock_client = MagicMock()
        mock_client.send = AsyncMock(return_value={"ok": True})
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.send("Browser.getVersion")
        assert result == {"ok": True}
        sync_client._runner.shutdown()

    def test_browser_domain_wrapped(self) -> None:
        mock_domain = MagicMock()
        mock_domain._send = MagicMock()
        mock_client = MagicMock()
        mock_client.browser = mock_domain
        sync_client = SyncCDPClient(mock_client)
        assert isinstance(sync_client.browser, _SyncDomainWrapper)
        sync_client._runner.shutdown()


class TestSyncDomainWrapper:
    def test_async_method_runs_sync(self) -> None:
        domain = MagicMock()
        domain._send = MagicMock()
        domain.click_dialog_button = AsyncMock(return_value={"ok": True})
        runner = _SyncRunner()
        wrapper = _SyncDomainWrapper(domain, runner)

        result = wrapper.click_dialog_button("dialog-1", "ConfirmIdpLoginContinue")

        assert result == {"ok": True}
        domain.click_dialog_button.assert_called_once_with(
            "dialog-1", "ConfirmIdpLoginContinue",
        )
        runner.shutdown()

    def test_non_async_attribute_passthrough(self) -> None:
        domain = MagicMock()
        domain._send = MagicMock()
        domain.some_property = "value"
        runner = _SyncRunner()
        wrapper = _SyncDomainWrapper(domain, runner)

        assert wrapper.some_property == "value"
        runner.shutdown()

    def test_sync_method_passthrough(self) -> None:
        domain = MagicMock()
        domain._send = MagicMock()

        def sync_method(x: int) -> int:
            return x * 2

        domain.calculate = sync_method
        runner = _SyncRunner()
        wrapper = _SyncDomainWrapper(domain, runner)

        assert wrapper.calculate(21) == 42
        runner.shutdown()

    def test_getattr_wraps_domain_via_session(self) -> None:
        mock_domain = MagicMock()
        mock_domain._send = MagicMock()
        mock_domain.click_dialog_button = AsyncMock(return_value={"done": True})
        mock_session = MagicMock()
        mock_session.fed_cm = mock_domain
        sync_session = SyncCDPSession(mock_session)

        wrapper = sync_session.fed_cm
        assert isinstance(wrapper, _SyncDomainWrapper)
        result = wrapper.click_dialog_button("d1", "ErrorGotIt")
        assert result == {"done": True}
        sync_session._runner.shutdown()

    def test_non_domain_attribute_passthrough_via_session(self) -> None:
        mock_session = MagicMock()
        mock_session.is_closed = False
        sync_session = SyncCDPSession(mock_session)

        assert sync_session.is_closed is False
        sync_session._runner.shutdown()


class TestSyncRealConnection:
    def test_sync_session_over_real_websocket(self) -> None:
        """Regression: the sync API must share one persistent loop across
        calls — the old per-call asyncio.run() left the WS receive task on
        a closed loop, so the second command always failed."""
        import json

        runner = _SyncRunner()

        async def _setup() -> tuple[object, object]:
            from websockets.asyncio.server import serve

            async def _handler(ws: object) -> None:
                async for raw in ws:
                    msg = json.loads(raw)
                    await ws.send(json.dumps({
                        "id": msg["id"],
                        "result": {"echoed": msg.get("method")},
                    }))

            server = await serve(_handler, "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]

            from cdpwave.transport.connection import Connection

            conn = Connection(f"ws://127.0.0.1:{port}")
            await conn.connect()
            return conn, server

        async def _teardown(server: object) -> None:
            server.close()
            await server.wait_closed()

        conn = None
        server = None
        try:
            conn, server = runner.run(_setup())
            from cdpwave.client import CDPSession

            session = CDPSession(conn, "S-1", "T-1")
            sync_session = SyncCDPSession(session, runner)

            r1 = sync_session.send("Page.enable")
            r2 = sync_session.send("Runtime.evaluate", {"expression": "1"})
            r3 = sync_session.page.navigate("https://example.com")

            assert r1 == {"echoed": "Page.enable"}
            assert r2 == {"echoed": "Runtime.evaluate"}
            assert r3 == {"echoed": "Page.navigate"}
            runner.run(conn.close())
            runner.run(_teardown(server))
        finally:
            runner.shutdown()
