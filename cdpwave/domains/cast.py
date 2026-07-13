"""Cast domain: interact with Cast, Presentation API, and Remote Playback API.

Events:
    Cast.sinksUpdated: Fired whenever the list of available sinks changes.
        Params: ``sinks`` (array of Sink — each with ``name`` (string),
        ``id`` (string), optional ``session`` (string)).
    Cast.issueUpdated: Fired whenever the outstanding issue/error message
        changes. ``issueMessage`` is empty if there is no issue.
        Params: ``issueMessage`` (string).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CastDomain(BaseDomain):
    """Wrapper for the CDP Cast domain.

    A domain for interacting with Cast, Presentation API, and Remote
    Playback API functionalities.

    Note: This entire domain is **experimental**.

    Events:
        ``Cast.sinksUpdated`` — fired whenever the list of available
            sinks changes. A sink is a device or a software surface
            that you can cast to.
            Params: ``sinks`` (array of Sink — each with ``name``
            (string), ``id`` (string), optional ``session`` (string)).
        ``Cast.issueUpdated`` — fired whenever the outstanding
            issue/error message changes. ``issueMessage`` is empty
            if there is no issue.
            Params: ``issueMessage`` (string).

    Use ``session.on("Cast.sinksUpdated", handler)``
    to subscribe to these events.
    """

    async def enable(
        self,
        presentation_url: str | None = None,
    ) -> dict[str, Any]:
        """Start observing for sinks that can be used for tab mirroring.

        If ``presentation_url`` is set, also observes sinks compatible
        with that URL. When sinks are found, a ``sinksUpdated`` event
        is fired. Also starts observing for issue messages. When an
        issue is added or removed, an ``issueUpdated`` event is fired.

        Args:
            presentation_url: Optional presentation URL to filter sinks.
        """
        params: dict[str, Any] = {}
        if presentation_url is not None:
            if not isinstance(presentation_url, str):
                raise TypeError("presentation_url must be a string")
            params["presentationUrl"] = presentation_url
        return await self._call("Cast.enable", params)

    async def disable(self) -> dict[str, Any]:
        """Stop observing for sinks and issues."""
        return await self._call("Cast.disable")

    async def set_sink_to_use(self, sink_name: str) -> dict[str, Any]:
        """Set a sink to be used when the web page requests the browser to choose a sink.

        Args:
            sink_name: Name of the sink to use.
        """
        if not isinstance(sink_name, str):
            raise TypeError("sink_name must be a string")
        return await self._call(
            "Cast.setSinkToUse",
            {"sinkName": sink_name},
        )

    async def start_desktop_mirroring(self, sink_name: str) -> dict[str, Any]:
        """Start mirroring the desktop to the sink.

        Args:
            sink_name: Name of the sink to mirror to.
        """
        if not isinstance(sink_name, str):
            raise TypeError("sink_name must be a string")
        return await self._call(
            "Cast.startDesktopMirroring",
            {"sinkName": sink_name},
        )

    async def start_tab_mirroring(self, sink_name: str) -> dict[str, Any]:
        """Start mirroring the tab to the sink.

        Args:
            sink_name: Name of the sink to mirror to.
        """
        if not isinstance(sink_name, str):
            raise TypeError("sink_name must be a string")
        return await self._call(
            "Cast.startTabMirroring",
            {"sinkName": sink_name},
        )

    async def stop_casting(self, sink_name: str) -> dict[str, Any]:
        """Stop the active Cast session on the sink.

        Args:
            sink_name: Name of the sink to stop casting to.
        """
        if not isinstance(sink_name, str):
            raise TypeError("sink_name must be a string")
        return await self._call(
            "Cast.stopCasting",
            {"sinkName": sink_name},
        )
