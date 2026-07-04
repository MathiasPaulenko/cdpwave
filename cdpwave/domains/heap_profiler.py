"""HeapProfiler domain: heap snapshot and allocation profiling."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class HeapProfilerDomain(BaseDomain):
    """Wrapper for the CDP HeapProfiler domain.

    Provides heap snapshot collection, allocation sampling, and
    garbage collection triggering for memory profiling.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the HeapProfiler domain.

        Activates heap profiling events, including heap snapshot chunks
        and allocation tracking updates.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeapProfiler.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the HeapProfiler domain.

        Stops heap profiling events and releases internal profiling
        state.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeapProfiler.disable")

    async def start_sampling(
        self,
        sampling_interval: int | None = None,
    ) -> dict[str, Any]:
        """Start sampling heap allocations.

        Args:
            sampling_interval: Sampling interval in bytes.
        """
        params: dict[str, Any] = {}
        if sampling_interval is not None:
            params["samplingInterval"] = sampling_interval
        return await self._call("HeapProfiler.startSampling", params)

    async def stop_sampling(self) -> dict[str, Any]:
        """Stop sampling heap allocations and return the profile.

        Returns:
            Dict with ``profile`` containing sampled heap profile data.
        """
        return await self._call("HeapProfiler.stopSampling")

    async def take_heap_snapshot(
        self,
        report_progress: bool = False,
        capture_numeric_value: bool = False,
        expose_internals: bool = False,
    ) -> dict[str, Any]:
        """Take a heap snapshot.

        Args:
            report_progress: Whether to report progress events.
            capture_numeric_value: Whether to capture numeric values.
            expose_internals: Whether to expose internals.
        """
        params: dict[str, Any] = {
            "reportProgress": report_progress,
            "captureNumericValue": capture_numeric_value,
            "exposeInternals": expose_internals,
        }
        return await self._call("HeapProfiler.takeHeapSnapshot", params)

    async def collect_garbage(self) -> dict[str, Any]:
        """Force garbage collection.

        Triggers a full garbage collection cycle in the V8 heap,
        reclaiming unreachable objects. Useful for memory analysis
        and testing cleanup behavior.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeapProfiler.collectGarbage")

    async def get_heap_object_id(
        self,
        object_id: str,
    ) -> dict[str, Any]:
        """Get the heap object ID for a remote object.

        Args:
            object_id: Remote object ID from Runtime.

        Returns:
            Dict with ``heapSnapshotObjectId``.
        """
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
            object_group: Optional object group for the result.

        Returns:
            Dict with ``result`` remote object.
        """
        params: dict[str, Any] = {"heapObjectId": heap_object_id}
        if object_group is not None:
            params["objectGroup"] = object_group
        return await self._call(
            "HeapProfiler.getObjectByHeapObjectId",
            params,
        )

    async def start_tracking_heap_objects(
        self,
        track_allocations: bool = False,
    ) -> dict[str, Any]:
        """Start tracking heap object allocation.

        Args:
            track_allocations: Whether to track allocations.
        """
        return await self._call(
            "HeapProfiler.startTrackingHeapObjects",
            {"trackAllocations": track_allocations},
        )

    async def stop_tracking_heap_objects(
        self,
        report_progress: bool = False,
    ) -> dict[str, Any]:
        """Stop tracking heap object allocation.

        Args:
            report_progress: Whether to report progress events.
        """
        return await self._call(
            "HeapProfiler.stopTrackingHeapObjects",
            {"reportProgress": report_progress},
        )
