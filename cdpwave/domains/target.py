"""Target domain: session management and target lifecycle."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class TargetDomain(BaseDomain):
    """Wrapper for the CDP Target domain."""

    async def create_target(self, url: str) -> dict[str, Any]:
        """Create a new browser target.

        Args:
            url: The initial URL for the new target.

        Returns:
            Response dict containing ``targetId``.
        """
        return await self._call("Target.createTarget", {"url": url})

    async def attach_to_target(
        self,
        target_id: str,
        flatten: bool = True,
    ) -> dict[str, Any]:
        """Attach to a target and return a session ID.

        Args:
            target_id: The target ID to attach to.
            flatten: If True, use flatten mode (single WebSocket).

        Returns:
            Response dict containing ``sessionId``.
        """
        return await self._call(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": flatten},
        )

    async def detach_from_target(self, session_id: str) -> dict[str, Any]:
        """Detach from a target session.

        Args:
            session_id: The session ID to detach.
        """
        return await self._call(
            "Target.detachFromTarget",
            {"sessionId": session_id},
        )

    async def close_target(self, target_id: str) -> dict[str, Any]:
        """Close a browser target.

        Args:
            target_id: The target ID to close.
        """
        return await self._call("Target.closeTarget", {"targetId": target_id})

    async def get_targets(self) -> dict[str, Any]:
        """List all available targets."""
        return await self._call("Target.getTargets")

    async def set_auto_attach(
        self,
        auto_attach: bool,
        flatten: bool = True,
    ) -> dict[str, Any]:
        """Configure auto-attach to new targets.

        Args:
            auto_attach: If True, auto-attach to new targets.
            flatten: If True, use flatten mode for auto-attached sessions.
        """
        return await self._call(
            "Target.setAutoAttach",
            {"autoAttach": auto_attach, "flatten": flatten},
        )
