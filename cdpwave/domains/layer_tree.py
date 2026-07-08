"""LayerTree domain: compositing layer inspection."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class LayerTreeDomain(BaseDomain):
    """Wrapper for the CDP LayerTree domain.

    Provides access to the compositing layer tree for inspecting
    how the browser composites layers for rendering.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the LayerTree domain.

        Activates LayerTree domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("LayerTree.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the LayerTree domain.

        Deactivates LayerTree domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("LayerTree.disable")

    async def get_layers(
        self,
        root_id: int | None = None,
    ) -> dict[str, Any]:
        """Get the layer tree.

        Args:
            root_id: Optional root layer ID to query from.

        Returns:
            Dict with ``layers`` list and optional ``paintProfiles``.
        """
        params: dict[str, Any] = {}
        if root_id is not None:
            params["rootId"] = root_id
        return await self._call("LayerTree.getLayers", params)

    async def compositing_reasons(
        self,
        layer_id: str,
    ) -> dict[str, Any]:
        """Get compositing reasons for a layer.

        Args:
            layer_id: Layer ID to query.

        Returns:
            Dict with ``compositingReasons`` list and
            ``compositingReasonIds`` list.
        """
        return await self._call(
            "LayerTree.compositingReasons",
            {"layerId": layer_id},
        )

    async def load_snapshot(
        self,
        tiles: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Load a snapshot of the layer tree.

        Args:
            tiles: List of tile dicts to load.

        Returns:
            Dict with ``snapshotId``.
        """
        return await self._call(
            "LayerTree.loadSnapshot",
            {"tiles": tiles},
        )

    async def release_snapshot(
        self,
        snapshot_id: str,
    ) -> dict[str, Any]:
        """Release a loaded snapshot.

        Args:
            snapshot_id: Snapshot ID to release.
        """
        return await self._call(
            "LayerTree.releaseSnapshot",
            {"snapshotId": snapshot_id},
        )

    async def profile_snapshot(
        self,
        snapshot_id: str,
        min_interval_ms: int = 0,
        clip_rect: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Profile a snapshot.

        Args:
            snapshot_id: Snapshot ID to profile.
            min_interval_ms: Minimum interval between samples in ms.
            clip_rect: Optional clip rect to limit profiling area.

        Returns:
            Dict with ``timings`` list.
        """
        params: dict[str, Any] = {
            "snapshotId": snapshot_id,
            "minIntervalMS": min_interval_ms,
        }
        if clip_rect is not None:
            params["clipRect"] = clip_rect
        return await self._call("LayerTree.profileSnapshot", params)
