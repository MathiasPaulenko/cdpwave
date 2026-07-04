"""Cast domain: discover sinks and start/stop tab mirroring."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class CastDomain(BaseDomain):
    """Wrapper for the CDP Cast domain.

    Provides discovery of available cast sinks (Chromecast devices)
    and control of tab mirroring sessions.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Cast domain and start sink discovery."""
        return await self._call("Cast.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Cast domain and stop sink discovery."""
        return await self._call("Cast.disable")

    async def set_sink_to_use(self, sink_name: str) -> dict[str, Any]:
        """Select a sink to use for casting.

        Args:
            sink_name: Name of the sink to use.
        """
        return await self._call(
            "Cast.setSinkToUse",
            {"sinkName": sink_name},
        )

    async def start_tab_mirroring(self, sink_name: str) -> dict[str, Any]:
        """Start mirroring the current tab to a sink.

        Args:
            sink_name: Name of the sink to mirror to.
        """
        return await self._call(
            "Cast.startTabMirroring",
            {"sinkName": sink_name},
        )

    async def stop_casting(self, sink_name: str) -> dict[str, Any]:
        """Stop casting to a sink.

        Args:
            sink_name: Name of the sink to stop casting to.
        """
        return await self._call(
            "Cast.stopCasting",
            {"sinkName": sink_name},
        )
