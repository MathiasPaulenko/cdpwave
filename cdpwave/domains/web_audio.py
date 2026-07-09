"""WebAudio domain: inspection of Web Audio API graphs for testing.

Provides methods to observe and inspect Web Audio API contexts,
nodes, and connections for audio testing and debugging.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class WebAudioDomain(BaseDomain):
    """Wrapper for the CDP WebAudio domain.

    Provides methods to enable Web Audio domain events, query
    audio context real-time data, and inspect Web Audio graphs
    (contexts, nodes, params, and connections).
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the WebAudio domain.

        Activates WebAudio domain events such as ``contextCreated``,
        ``contextChanged``, ``nodeCreated``, and ``nodeConnected``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAudio.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the WebAudio domain.

        Deactivates WebAudio domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAudio.disable")

    async def get_realtime_data(
        self,
        context_id: str,
    ) -> dict[str, Any]:
        """Fetch real-time audio data for a context.

        Args:
            context_id: The Web Audio context ID to query.

        Returns:
            Dict with real-time audio data (``currentValue``,
            ``currentTime``, ``currentTick``).
        """
        return await self._call(
            "WebAudio.getRealtimeData",
            {"contextId": context_id},
        )
