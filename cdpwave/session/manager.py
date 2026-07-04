"""Session manager for CDP flatten sessions."""

from cdpwave.transport.connection import Connection


class SessionManager:
    """Manages CDP target creation and session attachment.

    Wraps Target domain commands for creating targets, attaching sessions,
    and closing targets via a single Connection.
    """

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def create_target(self, url: str = "about:blank") -> str:
        """Create a new browser target and return its target ID."""
        result = await self._connection.send_command(
            "Target.createTarget",
            {"url": url},
        )
        return str(result["targetId"])

    async def attach_to_target(self, target_id: str) -> str:
        """Attach to a target and return the session ID."""
        result = await self._connection.send_command(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": True},
        )
        return str(result["sessionId"])

    async def detach_session(self, session_id: str) -> None:
        """Detach a session from its target."""
        await self._connection.send_command(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> None:
        """Close a browser target by target ID."""
        await self._connection.send_command(
            "Target.closeTarget",
            {"targetId": target_id},
        )
