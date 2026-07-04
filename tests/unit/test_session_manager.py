from unittest.mock import AsyncMock

from cdpwave.session.manager import SessionManager


class TestSessionManager:
    async def test_create_target(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"targetId": "T-1"}
        manager = SessionManager(conn)
        target_id = await manager.create_target("https://example.com")
        assert target_id == "T-1"
        conn.send_command.assert_called_with(
            "Target.createTarget",
            {"url": "https://example.com"},
        )

    async def test_create_target_default_url(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"targetId": "T-1"}
        manager = SessionManager(conn)
        await manager.create_target()
        conn.send_command.assert_called_with(
            "Target.createTarget",
            {"url": "about:blank"},
        )

    async def test_attach_to_target_sends_flatten_true(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {"sessionId": "S-1"}
        manager = SessionManager(conn)
        session_id = await manager.attach_to_target("T-1")
        assert session_id == "S-1"
        conn.send_command.assert_called_with(
            "Target.attachToTarget",
            {"targetId": "T-1", "flatten": True},
        )

    async def test_detach_session(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        manager = SessionManager(conn)
        await manager.detach_session("S-1")
        conn.send_command.assert_called_with(
            "Target.detachFromTarget",
            {"sessionId": "S-1"},
        )

    async def test_close_target(self) -> None:
        conn = AsyncMock()
        conn.send_command.return_value = {}
        manager = SessionManager(conn)
        await manager.close_target("T-1")
        conn.send_command.assert_called_with(
            "Target.closeTarget",
            {"targetId": "T-1"},
        )
