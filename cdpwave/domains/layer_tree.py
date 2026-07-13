"""LayerTree domain: compositing layer inspection.

This domain is **experimental** in the Chrome DevTools Protocol.

Types:

    ``LayerId`` — str. Unique Layer identifier.

    ``SnapshotId`` — str. Unique snapshot identifier.

    ``PaintProfile`` — list[float]. Array of timings, one per paint
    step.

    ``PictureTile`` — dict. Serialized fragment of layer picture
    along with its offset within the layer.  Fields: ``x`` (float),
    ``y`` (float), ``picture`` (str — base64-encoded snapshot data).

    ``ScrollRect`` — dict. Rectangle where scrolling happens on the
    main thread.  Fields: ``rect`` (DOM.Rect), ``type`` (str —
    ScrollRectType enum).

    ``ScrollRectType`` — str. Reason for rectangle to force scrolling
    on the main thread.  Values: ``"RepaintsOnScroll"``,
    ``"TouchEventHandler"``, ``"WheelEventHandler"``.

    ``StickyPositionConstraint`` — dict. Sticky position constraints.
    Fields: ``stickyBoxRect`` (DOM.Rect), ``containingBlockRect``
    (DOM.Rect), ``nearestLayerShiftingStickyBox`` (str, optional),
    ``nearestLayerShiftingContainingBlock`` (str, optional).

    ``Layer`` — dict. Information about a compositing layer.  Fields:
    ``layerId`` (str), ``parentLayerId`` (str, optional),
    ``backendNodeId`` (int, optional), ``offsetX`` (float),
    ``offsetY`` (float), ``width`` (float), ``height`` (float),
    ``transform`` (list[float], optional), ``anchorX`` (float,
    optional), ``anchorY`` (float, optional), ``anchorZ`` (float,
    optional), ``paintCount`` (int), ``drawsContent`` (bool),
    ``invisible`` (bool), ``scrollRects`` (list[ScrollRect],
    optional), ``stickyPositionConstraint``
    (StickyPositionConstraint, optional).

Events:
    LayerTree.layerPainted: [no description].
        Parameters:
            layerId (str — LayerId): The id of the painted layer.
            clip (dict — DOM.Rect): Clip rectangle.

    LayerTree.layerTreeDidChange: [no description].
        Parameters:
            layers (list[Layer], optional — omitempty,omitzero):
                Layer tree, absent if not in the compositing mode.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class LayerTreeDomain(BaseDomain):
    """Wrapper for the CDP LayerTree domain.

    Provides access to the compositing layer tree for inspecting
    how the browser composites layers for rendering.

    This domain is **experimental** in the Chrome DevTools Protocol.

    Events:
        LayerTree.layerPainted: A layer was painted.
        LayerTree.layerTreeDidChange: The layer tree changed.
    """

    async def compositing_reasons(
        self,
        layer_id: str,
    ) -> dict[str, Any]:
        """Provides the reasons why the given layer was composited.

        Args:
            layer_id: The id of the layer for which we want to get
                the reasons it was composited.

        Returns:
            Dict with ``compositingReasons`` (list[str] — reasons)
            and ``compositingReasonIds`` (list[str] — reason IDs).

        Raises:
            TypeError: If ``layer_id`` is not a str.
        """
        if not isinstance(layer_id, str):
            raise TypeError(
                f"layer_id must be a str, "
                f"got {type(layer_id).__name__}"
            )
        return await self._call(
            "LayerTree.compositingReasons",
            {"layerId": layer_id},
        )

    async def disable(self) -> dict[str, Any]:
        """Disables compositing tree inspection.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("LayerTree.disable")

    async def enable(self) -> dict[str, Any]:
        """Enables compositing tree inspection.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("LayerTree.enable")

    async def load_snapshot(
        self,
        tiles: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Returns the snapshot identifier.

        Args:
            tiles: An array of tiles composing the snapshot.

        Returns:
            Dict with ``snapshotId`` (str — the id of the snapshot).

        Raises:
            TypeError: If ``tiles`` is not a list or any element is
                not a dict.
        """
        if not isinstance(tiles, list):
            raise TypeError(
                f"tiles must be a list, "
                f"got {type(tiles).__name__}"
            )
        for i, tile in enumerate(tiles):
            if not isinstance(tile, dict):
                raise TypeError(
                    f"tiles[{i}] must be a dict, "
                    f"got {type(tile).__name__}"
                )
        return await self._call(
            "LayerTree.loadSnapshot",
            {"tiles": tiles},
        )

    async def make_snapshot(
        self,
        layer_id: str,
    ) -> dict[str, Any]:
        """Returns the layer snapshot identifier.

        Args:
            layer_id: The id of the layer.

        Returns:
            Dict with ``snapshotId`` (str — the id of the layer
            snapshot).

        Raises:
            TypeError: If ``layer_id`` is not a str.
        """
        if not isinstance(layer_id, str):
            raise TypeError(
                f"layer_id must be a str, "
                f"got {type(layer_id).__name__}"
            )
        return await self._call(
            "LayerTree.makeSnapshot",
            {"layerId": layer_id},
        )

    async def profile_snapshot(
        self,
        snapshot_id: str,
        min_repeat_count: int | None = None,
        min_duration: float | None = None,
        clip_rect: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Profile a layer snapshot.

        Args:
            snapshot_id: The id of the layer snapshot.
            min_repeat_count: The maximum number of times to replay
                the snapshot (1, if not specified).  Omitted when
                None or 0 (omitempty,omitzero in Go source).
            min_duration: The minimum duration (in seconds) to
                replay the snapshot.  Omitted when None or 0.0
                (omitempty,omitzero in Go source).
            clip_rect: The clip rectangle to apply when replaying
                the snapshot.  Omitted when None
                (omitempty,omitzero in Go source — pointer omitted
                when nil, sent when non-nil including empty dict).

        Returns:
            Dict with ``timings`` (list[PaintProfile] — the array
            of paint profiles, one per run).

        Raises:
            TypeError: If ``snapshot_id`` is not a str,
                ``min_repeat_count`` is not an int (bool rejected),
                ``min_duration`` is not a float (bool rejected), or
                ``clip_rect`` is not a dict.
        """
        if not isinstance(snapshot_id, str):
            raise TypeError(
                f"snapshot_id must be a str, "
                f"got {type(snapshot_id).__name__}"
            )
        if min_repeat_count is not None and (
            isinstance(min_repeat_count, bool)
            or not isinstance(min_repeat_count, int)
        ):
            raise TypeError(
                f"min_repeat_count must be an int, "
                f"got {type(min_repeat_count).__name__}"
            )
        if min_duration is not None and (
            isinstance(min_duration, bool)
            or not isinstance(min_duration, (int, float))
        ):
            raise TypeError(
                f"min_duration must be a float, "
                f"got {type(min_duration).__name__}"
            )
        if clip_rect is not None and not isinstance(clip_rect, dict):
            raise TypeError(
                f"clip_rect must be a dict, "
                f"got {type(clip_rect).__name__}"
            )
        params: dict[str, Any] = {"snapshotId": snapshot_id}
        if min_repeat_count:
            params["minRepeatCount"] = min_repeat_count
        if min_duration:
            params["minDuration"] = min_duration
        if clip_rect is not None:
            params["clipRect"] = clip_rect
        return await self._call("LayerTree.profileSnapshot", params)

    async def release_snapshot(
        self,
        snapshot_id: str,
    ) -> dict[str, Any]:
        """Releases layer snapshot captured by the back-end.

        Args:
            snapshot_id: The id of the layer snapshot.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``snapshot_id`` is not a str.
        """
        if not isinstance(snapshot_id, str):
            raise TypeError(
                f"snapshot_id must be a str, "
                f"got {type(snapshot_id).__name__}"
            )
        return await self._call(
            "LayerTree.releaseSnapshot",
            {"snapshotId": snapshot_id},
        )

    async def replay_snapshot(
        self,
        snapshot_id: str,
        from_step: int | None = None,
        to_step: int | None = None,
        scale: float | None = None,
    ) -> dict[str, Any]:
        """Replays the layer snapshot and returns the resulting bitmap.

        Args:
            snapshot_id: The id of the layer snapshot.
            from_step: The first step to replay from (replay from
                the very start if not specified).  Omitted when None
                or 0 (omitempty,omitzero in Go source).
            to_step: The last step to replay to (replay till the end
                if not specified).  Omitted when None or 0
                (omitempty,omitzero in Go source).
            scale: The scale to apply while replaying (defaults to
                1).  Omitted when None or 0.0 (omitempty,omitzero in
                Go source).

        Returns:
            Dict with ``dataURL`` (str — a data: URL for resulting
            image).

        Raises:
            TypeError: If ``snapshot_id`` is not a str,
                ``from_step``/``to_step`` are not int (bool
                rejected), or ``scale`` is not a float (bool
                rejected).
        """
        if not isinstance(snapshot_id, str):
            raise TypeError(
                f"snapshot_id must be a str, "
                f"got {type(snapshot_id).__name__}"
            )
        if from_step is not None and (
            isinstance(from_step, bool)
            or not isinstance(from_step, int)
        ):
            raise TypeError(
                f"from_step must be an int, "
                f"got {type(from_step).__name__}"
            )
        if to_step is not None and (
            isinstance(to_step, bool)
            or not isinstance(to_step, int)
        ):
            raise TypeError(
                f"to_step must be an int, "
                f"got {type(to_step).__name__}"
            )
        if scale is not None and (
            isinstance(scale, bool)
            or not isinstance(scale, (int, float))
        ):
            raise TypeError(
                f"scale must be a float, "
                f"got {type(scale).__name__}"
            )
        params: dict[str, Any] = {"snapshotId": snapshot_id}
        if from_step:
            params["fromStep"] = from_step
        if to_step:
            params["toStep"] = to_step
        if scale:
            params["scale"] = scale
        return await self._call("LayerTree.replaySnapshot", params)

    async def snapshot_command_log(
        self,
        snapshot_id: str,
    ) -> dict[str, Any]:
        """Replays the layer snapshot and returns canvas log.

        Args:
            snapshot_id: The id of the layer snapshot.

        Returns:
            Dict with ``commandLog`` (list — the array of canvas
            function calls).

        Raises:
            TypeError: If ``snapshot_id`` is not a str.
        """
        if not isinstance(snapshot_id, str):
            raise TypeError(
                f"snapshot_id must be a str, "
                f"got {type(snapshot_id).__name__}"
            )
        return await self._call(
            "LayerTree.snapshotCommandLog",
            {"snapshotId": snapshot_id},
        )
