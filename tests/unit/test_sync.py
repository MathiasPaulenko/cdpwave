"""Unit tests for sync API wrapper."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

from cdpwave.sync import SyncCDPClient, SyncCDPSession, _run, _SyncDomainWrapper, _SyncRunner


class TestRun:
    def test_run_no_running_loop(self) -> None:
        async def _coro() -> int:
            return 42

        assert _run(_coro()) == 42

    def test_run_with_running_loop(self) -> None:
        """When a loop is running, _run uses a thread pool."""
        async def _inner() -> int:
            return 99

        async def _outer() -> None:
            result = _run(_inner())
            assert result == 99

        asyncio.run(_outer())


class TestSyncRunner:
    def test_run_no_running_loop(self) -> None:
        runner = _SyncRunner()

        async def _coro() -> int:
            return 42

        assert runner.run(_coro()) == 42
        runner.shutdown()

    def test_run_with_running_loop_creates_pool(self) -> None:
        runner = _SyncRunner()

        async def _inner() -> int:
            return 99

        async def _outer() -> None:
            result = runner.run(_inner())
            assert result == 99

        asyncio.run(_outer())
        assert runner._pool is not None
        runner.shutdown()

    def test_pool_reused_across_calls(self) -> None:
        runner = _SyncRunner()

        async def _coro(val: int) -> int:
            return val

        async def _outer() -> None:
            assert runner.run(_coro(1)) == 1
            pool_after_first = runner._pool
            assert pool_after_first is not None
            assert runner.run(_coro(2)) == 2
            assert runner._pool is pool_after_first

        asyncio.run(_outer())
        runner.shutdown()

    def test_shutdown_clears_pool(self) -> None:
        runner = _SyncRunner()

        async def _coro() -> int:
            return 1

        async def _outer() -> None:
            runner.run(_coro())

        asyncio.run(_outer())
        assert runner._pool is not None
        runner.shutdown()
        assert runner._pool is None

    def test_shutdown_idempotent(self) -> None:
        runner = _SyncRunner()
        runner.shutdown()
        runner.shutdown()
        assert runner._pool is None

    def test_shutdown_without_pool(self) -> None:
        runner = _SyncRunner()
        runner.shutdown()
        assert runner._pool is None


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

    def test_properties_passthrough(self) -> None:
        mock_session = MagicMock()
        mock_session.page = "page_domain"
        mock_session.runtime = "runtime_domain"
        sync_session = SyncCDPSession(mock_session)
        assert sync_session.page == "page_domain"
        assert sync_session.runtime == "runtime_domain"

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

    def test_connect_to_page(self) -> None:
        mock_session = MagicMock()
        mock_session.target_id = "T1"
        mock_client = MagicMock()
        mock_client.connect_to_page = AsyncMock(return_value=mock_session)
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.connect_to_page("T1")
        assert isinstance(result, SyncCDPSession)
        assert result.target_id == "T1"

    def test_get_pages(self) -> None:
        mock_client = MagicMock()
        mock_client.get_pages = AsyncMock(return_value=[])
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.get_pages()
        assert result == []

    def test_send(self) -> None:
        mock_client = MagicMock()
        mock_client.send = AsyncMock(return_value={"ok": True})
        sync_client = SyncCDPClient(mock_client)
        result = sync_client.send("Browser.getVersion")
        assert result == {"ok": True}


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
