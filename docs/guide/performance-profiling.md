# Performance & Profiling

cdpwave provides full coverage of the `Performance`, `Profiler`,
`HeapProfiler`, and `Tracing` domains for measuring and analyzing
runtime performance.

## Performance metrics

### Get runtime metrics

```python
await session.performance.enable()
metrics = await session.performance.get_metrics()
for metric in metrics["metrics"]:
    print(f"{metric['name']}: {metric['value']}")
```

Common metrics include `Timestamp`, `Documents`, `Frames`, `JSEventListeners`,
`JSHeapTotalSize`, `JSHeapUsedSize`, `Nodes`.

### Listen to timeline events

```python
async def on_metrics(event: dict) -> None:
    print(f"Metrics at {event['timestamp']}: {event['metrics']}")

session.on("Performance.metrics", on_metrics)
```

### Performance timeline (LCP, FID, CLS)

The `PerformanceTimeline` domain emits events for web vitals:

```python
async def on_lcp(event: dict) -> None:
    print(f"LCP: {event['frameId']} renderTime={event['renderTime']}")

async def on_fid(event: dict) -> None:
    print(f"FID: {event['frameId']} processingTime={event['processingTime']}")

async def on_cls(event: dict) -> None:
    print(f"CLS: {event['frameId']} score={event['score']}")

session.on("PerformanceTimeline.largestContentfulPaint", on_lcp)
session.on("PerformanceTimeline.firstInput", on_fid)
session.on("PerformanceTimeline.layoutShift", on_cls)
```

---

## CPU profiling

### Start and stop profiling

```python
await session.profiler.enable()

await session.profiler.start()
# ... run your workload ...
result = await session.profiler.stop()

# result["profile"] contains the CPU profile
# with nodes, samples, and timeDeltas
print(f"Profile samples: {len(result['profile']['samples'])}")
```

### Precise code coverage

```python
await session.profiler.start_precise_coverage(
    call_count=True,
    detailed=True,
)

# ... run code ...

coverage = await session.profiler.take_precise_coverage()

for script in coverage["result"]:
    url = script["url"]
    for function in script["functions"]:
        for range_ in function["ranges"]:
            print(f"{url}: {range_['startOffset']}-{range_['endOffset']} count={range_['count']}")

await session.profiler.stop_precise_coverage()
```

### Best effort coverage

```python
await session.profiler.start_coverage()
# ... run code ...
result = await session.profiler.take_coverage()
await session.profiler.stop_coverage()
```

### Console profile finished

Listen for profiles started from `console.profile()`:

```python
async def on_profile(event: dict) -> None:
    print(f"Profile finished: {event['profile']['title']}")

session.on("Profiler.consoleProfileFinished", on_profile)
```

---

## Heap profiling

### Heap snapshot

```python
await session.heap_profiler.enable()

# Take a heap snapshot
await session.heap_profiler.take_heap_snapshot()

# Listen for snapshot data
async def on_snapshot(event: dict) -> None:
    print(f"Heap snapshot: {len(event['chunk'])} bytes")

session.on("HeapProfiler.addHeapSnapshotChunk", on_snapshot)
```

### Track heap objects

```python
await session.heap_profiler.start_tracking_heap_objects()

# ... interact with the page ...

# Stop and get the snapshot
await session.heap_profiler.stop_tracking_heap_objects()

# Listen for heap stats updates
async def on_heap_stats(event: dict) -> None:
    for sample in event["statsSamples"]:
        print(f"Heap size: {sample['size']}")

session.on("HeapProfiler.heapStatsUpdate", on_heap_stats)
```

### Allocation sampling

```python
await session.heap_profiler.start_sampling()

# ... interact with the page ...

result = await session.heap_profiler.stop_sampling()
# result["profile"] contains the sampling heap profile
```

### Garbage collection

Force a garbage collection:

```python
await session.heap_profiler.collect_garbage()
```

### Object tracking

```python
await session.heap_profiler.start_tracking_heap_objects(track_allocations=True)

async def on_object_added(event: dict) -> None:
    print(f"Object allocated: {event['snapshot']['className']}")

session.on("HeapProfiler.heapObjectAdded", on_object_added)
```

---

## Tracing

### Start tracing

```python
await session.tracing.start(
    categories=[
        "-*",
        "devtools.timeline",
        "v8.execute",
        "disabled-by-default-devtools.timeline",
    ],
    options="record-as-much-as-possible",
)
```

### Stop tracing

```python
async def on_data_collected(event: dict) -> None:
    # event["value"] contains trace data as a string
    # (typically a sequence of JSON objects, one per line)
    with open("trace.json", "w") as f:
        f.write(event["value"])

session.on("Tracing.dataCollected", on_data_collected)

await session.tracing.end()
```

### Get available categories

```python
categories = await session.tracing.get_categories()
for category in categories["categories"]:
    print(category)
```

### Record clock sync marker

```python
await session.tracing.record_clock_sync_marker(sync_id="sync1")
```
