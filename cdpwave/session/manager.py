from cdpwave.transport.connection import Connection


class SessionManager:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def create_target(self, url: str = "about:blank") -> str:
        result = await self._connection.send_command(
            "Target.createTarget",
            {"url": url},
        )
        return str(result["targetId"])

    async def attach_to_target(self, target_id: str) -> str:
        result = await self._connection.send_command(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": True},
        )
        return str(result["sessionId"])

    async def detach_session(self, session_id: str) -> None:
        await self._connection.send_command(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> None:
        await self._connection.send_command(
            "Target.closeTarget",
            {"targetId": target_id},
        )
