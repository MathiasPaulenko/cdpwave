"""WebAudio domain: inspection of Web Audio API graphs for testing.

Experimental domain that provides methods to enable Web Audio domain
events and query audio context real-time data.

Types defined by this domain:
  - GraphObjectId: unique ID for a graph object (string)
  - ContextType: ``"realtime"`` or ``"offline"``
  - ContextState: ``"suspended"``, ``"running"``, ``"closed"``,
    ``"interrupted"``
  - NodeType: enum of AudioNode types (string)
  - ChannelCountMode: ``"clamped-max"``, ``"explicit"``, ``"max"``
  - ChannelInterpretation: ``"discrete"``, ``"speakers"``
  - ParamType: enum of AudioParam types (string)
  - AutomationRate: ``"a-rate"`` or ``"k-rate"``
  - ContextRealtimeData: real-time context metrics (currentTime,
    renderCapacity, callbackIntervalMean, callbackIntervalVariance)
  - BaseAudioContext, AudioListener, AudioNode, AudioParam

Events:
  - ``contextCreated``: a new BaseAudioContext has been created
  - ``contextWillBeDestroyed``: an existing BaseAudioContext will be
    destroyed
  - ``contextChanged``: existing BaseAudioContext has changed some
    properties
  - ``audioListenerCreated``: construction of an AudioListener has finished
  - ``audioListenerWillBeDestroyed``: an AudioListener will be destroyed
  - ``audioNodeCreated``: a new AudioNode has been created
  - ``audioNodeWillBeDestroyed``: an existing AudioNode has been destroyed
  - ``audioParamCreated``: a new AudioParam has been created
  - ``audioParamWillBeDestroyed``: an existing AudioParam has been destroyed
  - ``nodesConnected``: two AudioNodes are connected
  - ``nodesDisconnected``: AudioNodes are disconnected
  - ``nodeParamConnected``: an AudioNode is connected to an AudioParam
  - ``nodeParamDisconnected``: an AudioNode is disconnected from an AudioParam

Commands:
  - ``enable``: enable the WebAudio domain
  - ``disable``: disable the WebAudio domain
  - ``getRealtimeData``: fetch real-time data from a registered context
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class WebAudioDomain(BaseDomain):
    """Wrapper for the CDP WebAudio domain (experimental).

    Provides methods to enable Web Audio domain events and query
    audio context real-time data.

    Events emitted when the domain is enabled:
      - ``WebAudio.contextCreated`` (BaseAudioContext)
      - ``WebAudio.contextWillBeDestroyed`` (GraphObjectId)
      - ``WebAudio.contextChanged`` (BaseAudioContext)
      - ``WebAudio.audioListenerCreated`` (AudioListener)
      - ``WebAudio.audioListenerWillBeDestroyed`` (GraphObjectId)
      - ``WebAudio.audioNodeCreated`` (AudioNode)
      - ``WebAudio.audioNodeWillBeDestroyed`` (GraphObjectId)
      - ``WebAudio.audioParamCreated`` (AudioParam)
      - ``WebAudio.audioParamWillBeDestroyed`` (GraphObjectId)
      - ``WebAudio.nodesConnected`` (GraphObjectId)
      - ``WebAudio.nodesDisconnected`` (GraphObjectId)
      - ``WebAudio.nodeParamConnected`` (GraphObjectId)
      - ``WebAudio.nodeParamDisconnected`` (GraphObjectId)
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the WebAudio domain.

        Enables WebAudio domain events: ``contextCreated``,
        ``contextWillBeDestroyed``, ``contextChanged``,
        ``audioListenerCreated``, ``audioListenerWillBeDestroyed``,
        ``audioNodeCreated``, ``audioNodeWillBeDestroyed``,
        ``audioParamCreated``, ``audioParamWillBeDestroyed``,
        ``nodesConnected``, ``nodesDisconnected``,
        ``nodeParamConnected``, and ``nodeParamDisconnected``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("WebAudio.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the WebAudio domain.

        Disables WebAudio domain events and reporting.

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
            context_id: The Web Audio context ID (GraphObjectId) to query.

        Returns:
            Dict with real-time audio data (``currentTime``,
            ``renderCapacity``, ``callbackIntervalMean``,
            ``callbackIntervalVariance``).

        Raises:
            TypeError: If ``context_id`` is not a str (bool rejected).
        """
        if not isinstance(context_id, str):
            raise TypeError(
                f"context_id must be a str, "
                f"got {type(context_id).__name__}"
            )
        return await self._call(
            "WebAudio.getRealtimeData",
            {"contextId": context_id},
        )
