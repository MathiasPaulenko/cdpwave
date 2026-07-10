"""Session manager for CDP flatten sessions."""

from cdpwave.transport.connection import Connection


class SessionManager:
    """Manages CDP target creation and session attachment.

    Wraps Target domain commands for creating targets, attaching sessions,
    and closing targets via a single Connection.
    """

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def create_target(
        self,
        url: str = "about:blank",
        browser_context_id: str | None = None,
    ) -> str:
        """Create a new browser target and return its target ID.

        Args:
            url: The initial URL for the new target.
            browser_context_id: Optional browser context ID for isolation.
        """
        params: dict[str, object] = {"url": url}
        if browser_context_id is not None:
            params["browserContextId"] = browser_context_id
        result = await self._connection.send_command(
            "Target.createTarget",
            params,
        )
        target_id = result.get("targetId")
        if target_id is None:
            raise KeyError(
                "Target.createTarget response missing 'targetId' field"
            )
        return str(target_id)

    async def attach_to_target(self, target_id: str) -> str:
        """Attach to a target and return the session ID."""
        result = await self._connection.send_command(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": True},
        )
        session_id = result.get("sessionId")
        if session_id is None:
            raise KeyError(
                "Target.attachToTarget response missing 'sessionId' field"
            )
        return str(session_id)

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
