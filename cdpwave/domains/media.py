"""Media domain: media player inspection and events.

Experimental domain. This domain allows detailed inspection of media elements.

Types:
    - PlayerId: string, unique within the agent context.
    - Timestamp: number.
    - PlayerMessage: object with ``level`` (error/warning/info/debug) and
      ``message`` (string).
    - PlayerProperty: object with ``name`` (string) and ``value`` (string).
    - PlayerEvent: object with ``timestamp`` (Timestamp) and ``value`` (string).
    - PlayerErrorSourceLocation: object with ``file`` (string) and
      ``line`` (integer).
    - PlayerError: object with ``errorType`` (string), ``code`` (integer),
      ``stack`` (array of PlayerErrorSourceLocation), ``cause`` (array of
      PlayerError), and ``data`` (object).
    - Player: object with ``playerId`` (PlayerId) and optional
      ``domNodeId`` (DOM.BackendNodeId).

Events:
    - playerPropertiesChanged: playerId, properties (array of PlayerProperty).
    - playerEventsAdded: playerId, events (array of PlayerEvent).
    - playerMessagesLogged: playerId, messages (array of PlayerMessage).
    - playerErrorsRaised: playerId, errors (array of PlayerError).
    - playerCreated: player (Player).

Commands:
    - enable: enable the Media domain.
    - disable: disable the Media domain.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class MediaDomain(BaseDomain):
    """Wrapper for the CDP Media domain.

    Experimental domain that provides access to media player events
    for inspecting media playback state, including audio/video players.

    Events: playerPropertiesChanged, playerEventsAdded, playerMessagesLogged,
    playerErrorsRaised, playerCreated.

    Commands: enable, disable.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Media domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Media.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Media domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Media.disable")
