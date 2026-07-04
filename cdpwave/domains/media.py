"""Media domain: media player inspection and events."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class MediaDomain(BaseDomain):
    """Wrapper for the CDP Media domain.

    Provides access to media player properties and events for
    inspecting media playback state, including audio/video players,
    properties like currentTime, volume, readyState, etc.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Media domain."""
        return await self._call("Media.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Media domain."""
        return await self._call("Media.disable")

    async def get_player_properties(
        self,
        player_id: str,
    ) -> dict[str, Any]:
        """Get properties of a media player.

        Args:
            player_id: Media player ID.

        Returns:
            Dict with ``properties`` list of name/value pairs.
        """
        return await self._call(
            "Media.getPlayerProperties",
            {"playerId": player_id},
        )

    async def get_players(self) -> dict[str, Any]:
        """Get all media players on the current page.

        Returns:
            Dict with ``players`` list of player IDs.
        """
        return await self._call("Media.getPlayers")
