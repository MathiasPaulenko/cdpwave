"""HeapProfiler domain: heap snapshot and allocation profiling.

Types:

    ``HeapSnapshotObjectID`` — str. Heap snapshot object id.

    ``SamplingHeapProfileNode`` — dict. Sampling heap profile node.
    Holds callsite information, allocation statistics and child
    nodes.  Fields: ``callFrame`` (dict — runtime.CallFrame,
    function location), ``selfSize`` (float — allocations size in
    bytes excluding children), ``id`` (int — node id, unique across
    all profiles collected between startSampling and stopSampling),
    ``children`` (list[SamplingHeapProfileNode] — child nodes).

    ``SamplingHeapProfileSample`` — dict. A single sample from a
    sampling profile.  Fields: ``size`` (float — allocation size in
    bytes attributed to the sample), ``nodeId`` (int — id of the
    corresponding profile tree node), ``ordinal`` (float —
    time-ordered sample ordinal number, unique across all profiles
    retrieved between startSampling and stopSampling).

    ``SamplingHeapProfile`` — dict. Sampling profile.  Fields:
    ``head`` (SamplingHeapProfileNode), ``samples``
    (list[SamplingHeapProfileSample]).

Events:

    ``HeapProfiler.addHeapSnapshotChunk`` — sent when a chunk of heap
    snapshot is available.  Parameters: ``chunk`` (str).

    ``HeapProfiler.heapStatsUpdate`` — sent if heap objects tracking
    has been started then backend may send update for one or more
    fragments.  Parameters: ``statsUpdate`` (list[int] — an array of
    triplets; each triplet describes a fragment: first integer is the
    fragment index, second is total count of objects, third is total
    size).

    ``HeapProfiler.lastSeenObjectId`` — sent if heap objects tracking
    has been started then backend regularly sends a current value for
    last seen object id and corresponding timestamp.  If there were
    changes in the heap since last event then one or more
    ``heapStatsUpdate`` events will be sent before a new
    ``lastSeenObjectId`` event.  Parameters: ``lastSeenObjectId``
    (int), ``timestamp`` (float).

    ``HeapProfiler.reportHeapSnapshotProgress`` — sent while heap
    snapshot is being taken.  Parameters: ``done`` (int), ``total``
    (int), ``finished`` (bool).

    ``HeapProfiler.resetProfiles`` — sent when all heap profiles have
    been reset.  No parameters.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class HeapProfilerDomain(BaseDomain):
    """Wrapper for the CDP HeapProfiler domain.

    Provides heap snapshot collection, allocation sampling, and
    garbage collection triggering for memory profiling.

    **Experimental** — marked as Experimental in the CDP spec.

    Events:

    - ``HeapProfiler.addHeapSnapshotChunk``: Params ``chunk`` (str).
    - ``HeapProfiler.heapStatsUpdate``: Params ``statsUpdate``
      (list[int] — array of triplets: fragment index, object count,
      total size).
    - ``HeapProfiler.lastSeenObjectId``: Params ``lastSeenObjectId``
      (int), ``timestamp`` (float).
    - ``HeapProfiler.reportHeapSnapshotProgress``: Params ``done``
      (int), ``total`` (int), ``finished`` (bool).
    - ``HeapProfiler.resetProfiles``: No params.

    Subscribe via ``session.on("HeapProfiler.addHeapSnapshotChunk", handler)``.
    """

    async def add_inspected_heap_object(
        self,
        heap_object_id: str,
    ) -> dict[str, Any]:
        """Enable console to refer to the node with given id via $x.

        See Command Line API for more details on $x functions.

        Args:
            heap_object_id: Heap snapshot object id to be accessible
                by means of $x command line API.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``heap_object_id`` is not a str.
        """
        if not isinstance(heap_object_id, str):
            raise TypeError(
                f"heap_object_id must be a str, "
                f"got {type(heap_object_id).__name__}"
            )
        return await self._call(
            "HeapProfiler.addInspectedHeapObject",
            {"heapObjectId": heap_object_id},
        )

    async def collect_garbage(self) -> dict[str, Any]:
        """Force garbage collection.

        Triggers a full garbage collection cycle in the V8 heap.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("HeapProfiler.collectGarbage")

    async def disable(self) -> dict[str, Any]:
        """Disable the HeapProfiler domain.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("HeapProfiler.disable")

    async def enable(self) -> dict[str, Any]:
        """Enable the HeapProfiler domain.

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("HeapProfiler.enable")

    async def get_heap_object_id(
        self,
        object_id: str,
    ) -> dict[str, Any]:
        """Get the heap object ID for a remote object.

        Args:
            object_id: Remote object ID from Runtime.

        Returns:
            Dict with ``heapSnapshotObjectId`` (str) — the heap
            snapshot object id corresponding to the passed remote
            object id.

        Raises:
            TypeError: If ``object_id`` is not a str.
        """
        if not isinstance(object_id, str):
            raise TypeError(
                f"object_id must be a str, got {type(object_id).__name__}"
            )
        return await self._call(
            "HeapProfiler.getHeapObjectId",
            {"objectId": object_id},
        )

    async def get_object_by_heap_object_id(
        self,
        heap_object_id: str,
        object_group: str | None = None,
    ) -> dict[str, Any]:
        """Get a remote object by heap object ID.

        Args:
            heap_object_id: Heap snapshot object ID.
            object_group: Optional symbolic group name that can be
                used to release multiple objects.

        Returns:
            Dict with ``result`` (dict — runtime.RemoteObject)
            — the evaluation result.

        Raises:
            TypeError: If ``heap_object_id`` is not a str or
                ``object_group`` is not a str.
        """
        if not isinstance(heap_object_id, str):
            raise TypeError(
                f"heap_object_id must be a str, "
                f"got {type(heap_object_id).__name__}"
            )
        if object_group is not None and not isinstance(object_group, str):
            raise TypeError(
                f"object_group must be a str, "
                f"got {type(object_group).__name__}"
            )
        params: dict[str, Any] = {"objectId": heap_object_id}
        if object_group:
            params["objectGroup"] = object_group
        return await self._call(
            "HeapProfiler.getObjectByHeapObjectId",
            params,
        )

    async def get_sampling_profile(self) -> dict[str, Any]:
        """Get the sampling heap profile being collected.

        Returns:
            Dict with ``profile`` (dict — SamplingHeapProfile) —
            the sampling profile being collected. The profile has
            ``head`` (SamplingHeapProfileNode) and ``samples``
            (list[SamplingHeapProfileSample]).
        """
        return await self._call("HeapProfiler.getSamplingProfile")

    async def start_sampling(
        self,
        sampling_interval: float | None = None,
        stack_depth: float | None = None,
        include_objects_collected_by_major_gc: bool = False,
        include_objects_collected_by_minor_gc: bool = False,
    ) -> dict[str, Any]:
        """Start sampling heap allocations.

        Args:
            sampling_interval: Average sample interval in bytes.
                Poisson distribution is used for the intervals.
                Default is 32768 bytes.
            stack_depth: Maximum stack depth. Default is 128.
            include_objects_collected_by_major_gc: By default, the
                sampling heap profiler reports only objects which are
                still alive when the profile is returned via
                getSamplingProfile or stopSampling. This flag
                instructs it to also include information about objects
                discarded by major GC, showing which functions cause
                large temporary memory usage or long GC pauses.
            include_objects_collected_by_minor_gc: By default, the
                sampling heap profiler reports only objects which are
                still alive when the profile is returned via
                getSamplingProfile or stopSampling. This flag
                instructs it to also include information about objects
                discarded by minor GC, useful when tuning a
                latency-sensitive application for minimal GC activity.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``sampling_interval`` or ``stack_depth`` is
                not a number, or if bool params are not bools.
        """
        if sampling_interval is not None and (
            isinstance(sampling_interval, bool)
            or not isinstance(sampling_interval, (int, float))
        ):
            raise TypeError(
                f"sampling_interval must be a number, "
                f"got {type(sampling_interval).__name__}"
            )
        if stack_depth is not None and (
            isinstance(stack_depth, bool)
            or not isinstance(stack_depth, (int, float))
        ):
            raise TypeError(
                f"stack_depth must be a number, "
                f"got {type(stack_depth).__name__}"
            )
        if not isinstance(include_objects_collected_by_major_gc, bool):
            raise TypeError(
                f"include_objects_collected_by_major_gc must be a bool, "
                f"got {type(include_objects_collected_by_major_gc).__name__}"
            )
        if not isinstance(include_objects_collected_by_minor_gc, bool):
            raise TypeError(
                f"include_objects_collected_by_minor_gc must be a bool, "
                f"got {type(include_objects_collected_by_minor_gc).__name__}"
            )
        params: dict[str, Any] = {
            "includeObjectsCollectedByMajorGC": include_objects_collected_by_major_gc,
            "includeObjectsCollectedByMinorGC": include_objects_collected_by_minor_gc,
        }
        if sampling_interval:
            params["samplingInterval"] = sampling_interval
        if stack_depth:
            params["stackDepth"] = stack_depth
        return await self._call("HeapProfiler.startSampling", params)

    async def start_tracking_heap_objects(
        self,
        track_allocations: bool = False,
    ) -> dict[str, Any]:
        """Start tracking heap object allocation.

        Args:
            track_allocations: Whether to track allocations.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``track_allocations`` is not a bool.
        """
        if not isinstance(track_allocations, bool):
            raise TypeError(
                f"track_allocations must be a bool, "
                f"got {type(track_allocations).__name__}"
            )
        return await self._call(
            "HeapProfiler.startTrackingHeapObjects",
            {"trackAllocations": track_allocations},
        )

    async def stop_sampling(self) -> dict[str, Any]:
        """Stop sampling heap allocations and return the profile.

        Returns:
            Dict with ``profile`` (dict — SamplingHeapProfile) —
            the recorded sampling heap profile. The profile has
            ``head`` (SamplingHeapProfileNode) and ``samples``
            (list[SamplingHeapProfileSample]).
        """
        return await self._call("HeapProfiler.stopSampling")

    async def stop_tracking_heap_objects(
        self,
        report_progress: bool = False,
        capture_numeric_value: bool = False,
        expose_internals: bool = False,
    ) -> dict[str, Any]:
        """Stop tracking heap object allocation.

        Args:
            report_progress: If true, ``reportHeapSnapshotProgress``
                events will be generated while snapshot is being
                taken when the tracking is stopped.
            capture_numeric_value: If true, numerical values are
                included in the snapshot.
            expose_internals: If true, exposes internals of the
                snapshot.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If any argument is not a bool.
        """
        if not isinstance(report_progress, bool):
            raise TypeError(
                f"report_progress must be a bool, "
                f"got {type(report_progress).__name__}"
            )
        if not isinstance(capture_numeric_value, bool):
            raise TypeError(
                f"capture_numeric_value must be a bool, "
                f"got {type(capture_numeric_value).__name__}"
            )
        if not isinstance(expose_internals, bool):
            raise TypeError(
                f"expose_internals must be a bool, "
                f"got {type(expose_internals).__name__}"
            )
        params: dict[str, Any] = {
            "reportProgress": report_progress,
            "captureNumericValue": capture_numeric_value,
            "exposeInternals": expose_internals,
        }
        return await self._call(
            "HeapProfiler.stopTrackingHeapObjects",
            params,
        )

    async def take_heap_snapshot(
        self,
        report_progress: bool = False,
        capture_numeric_value: bool = False,
        expose_internals: bool = False,
    ) -> dict[str, Any]:
        """Take a heap snapshot.

        Args:
            report_progress: If true, ``reportHeapSnapshotProgress``
                events will be generated while snapshot is being
                taken.
            capture_numeric_value: If true, numerical values are
                included in the snapshot.
            expose_internals: If true, exposes internals of the
                snapshot.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If any argument is not a bool.
        """
        if not isinstance(report_progress, bool):
            raise TypeError(
                f"report_progress must be a bool, "
                f"got {type(report_progress).__name__}"
            )
        if not isinstance(capture_numeric_value, bool):
            raise TypeError(
                f"capture_numeric_value must be a bool, "
                f"got {type(capture_numeric_value).__name__}"
            )
        if not isinstance(expose_internals, bool):
            raise TypeError(
                f"expose_internals must be a bool, "
                f"got {type(expose_internals).__name__}"
            )
        params: dict[str, Any] = {
            "reportProgress": report_progress,
            "captureNumericValue": capture_numeric_value,
            "exposeInternals": expose_internals,
        }
        return await self._call("HeapProfiler.takeHeapSnapshot", params)
