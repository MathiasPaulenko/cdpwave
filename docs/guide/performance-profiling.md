# Performance & Profiling

cdpwave provides full coverage of the `Performance`, `Profiler`,
`HeapProfiler`, and `Tracing` domains for measuring and analyzing
runtime performance.

## When to use which domain

| Domain | What it measures | Output | Overhead |
|---|---|---|---|
| `Performance` | Runtime metrics (JS heap, nodes, events) | Key-value pairs | Low |
| `Profiler` | CPU time per function | Call tree with samples | Medium |
| `HeapProfiler` | Memory allocation and retention | Heap snapshot / sampling profile | High |
| `Tracing` | Browser-level events (rendering, paint, network) | Trace JSON | Variable |

Use `Performance` for quick health checks. Use `Profiler` for CPU
bottlenecks. Use `HeapProfiler` for memory leaks. Use `Tracing` for
full browser-level analysis (rendering, paint, compositor).

## Performance metrics

### Get runtime metrics

```python
await session.performance.enable()
metrics = await session.performance.get_metrics()
for metric in metrics["metrics"]:
    print(f"{metric['name']}: {metric['value']}")
```

Common metrics:

| Metric | Description |
|---|---|
| `Timestamp` | When metrics were collected |
| `Documents` | Number of documents in the page |
| `Frames` | Number of frames |
| `JSEventListeners` | Number of JS event listeners |
| `JSHeapTotalSize` | Total JS heap size (bytes) |
| `JSHeapUsedSize` | Used JS heap size (bytes) |
| `Nodes` | Number of DOM nodes |

!!! tip "Memory leak detection"
    Compare `JSHeapUsedSize` before and after an interaction. If it
    keeps growing across repeated operations, you likely have a
    memory leak.

### Listen to timeline events

`Performance.metrics` events fire periodically with updated metrics:

```python
async def on_metrics(event: dict) -> None:
    print(f"Metrics at {event['timestamp']}: {event['metrics']}")

session.on("Performance.metrics", on_metrics)
```

### Web vitals (LCP, FID, CLS)

The `PerformanceTimeline` domain emits events for Core Web Vitals.
These are event-only — no commands to call, just subscribe:

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

| Vital | Event | What it measures |
|---|---|---|
| LCP | `largestContentfulPaint` | Time to largest visible element |
| FID | `firstInput` | Delay of first user interaction |
| CLS | `layoutShift` | Cumulative layout shift score |

## CPU profiling

CPU profiling samples the call stack at regular intervals, producing
a profile that shows which functions consumed the most time.

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

!!! note "Single active profile"
    Only one CPU profile can be active at a time. Call `stop()`
    before starting a new one.

### Profile structure

The returned profile contains:

- **`nodes`** — call tree nodes with `id`, `functionName`,
  `scriptId`, `url`, `lineNumber`, `children`.
- **`samples`** — list of node IDs, one per sample.
- **`timeDeltas`** — time (microseconds) between consecutive samples.

### Precise code coverage

Track exactly which functions and lines executed:

```python
await session.profiler.start_precise_coverage(
    call_count=True,    # Track call counts per function
    detailed=True,      # Track per-block coverage
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

!!! tip "Precise vs best-effort"
    Precise coverage (`start_precise_coverage`) instruments every
    function call — accurate but slower. Best-effort coverage
    (`start_coverage`) is lighter but may miss infrequently
    executed code.

### Best effort coverage

```python
await session.profiler.start_coverage()
# ... run code ...
result = await session.profiler.take_coverage()
await session.profiler.stop_coverage()
```

### Console profile finished

Listen for profiles started from `console.profile()` in JavaScript:

```python
async def on_profile(event: dict) -> None:
    print(f"Profile finished: {event['profile']['title']}")

session.on("Profiler.consoleProfileFinished", on_profile)
```

## Heap profiling

Heap profiling captures the state of JavaScript objects in memory.
Use it to find memory leaks, identify large object retentions, and
analyze allocation patterns.

### Heap snapshot

A heap snapshot is a complete dump of all JS objects. It's delivered
in chunks via events:

```python
await session.heap_profiler.enable()

# Listen for snapshot chunks
chunks: list[str] = []

async def on_snapshot(event: dict) -> None:
    chunks.append(event["chunk"])

session.on("HeapProfiler.addHeapSnapshotChunk", on_snapshot)

# Take the snapshot
await session.heap_profiler.take_heap_snapshot()

# Reconstruct the full snapshot
full_snapshot = "".join(chunks)
print(f"Snapshot size: {len(full_snapshot)} bytes")
```

!!! note "Snapshot format"
    The snapshot is a JSON string. You can load it into Chrome
    DevTools' Memory tab for visual analysis.

### Track heap objects

Track object allocation and growth over time:

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

Sample memory allocations at regular intervals — lighter than full
snapshots:

```python
await session.heap_profiler.start_sampling()

# ... interact with the page ...

result = await session.heap_profiler.stop_sampling()
# result["profile"] contains the sampling heap profile
```

### Garbage collection

Force a garbage collection to test cleanup logic:

```python
await session.heap_profiler.collect_garbage()
```

!!! tip "Leak detection workflow"
    1. Take a heap snapshot or start tracking.
    2. Perform the operation you suspect leaks.
    3. Force GC with `collect_garbage()`.
    4. Take another snapshot.
    5. Compare — surviving objects are potential leaks.

### Object tracking

Track individual object allocations in real time:

```python
await session.heap_profiler.start_tracking_heap_objects(track_allocations=True)

async def on_object_added(event: dict) -> None:
    print(f"Object allocated: {event['snapshot']['className']}")

session.on("HeapProfiler.heapObjectAdded", on_object_added)
```

## Tracing

The `Tracing` domain captures browser-level events: rendering, paint,
compositor, network, V8 execution, and more. It produces a trace
file compatible with `chrome://tracing` and Perfetto.

### Start tracing

```python
await session.tracing.start(
    categories=[
        "-*",                                    # Disable all default categories
        "devtools.timeline",                     # Timeline events
        "v8.execute",                            # V8 execution
        "disabled-by-default-devtools.timeline", # Detailed timeline
    ],
    options="record-as-much-as-possible",
)
```

!!! tip "Category selection"
    Start with `"-*"` to disable all defaults, then add only the
    categories you need. Tracing with too many categories produces
    huge files and slows the browser.

### Stop tracing and collect data

```python
trace_data: list[str] = []

async def on_data_collected(event: dict) -> None:
    # event["value"] contains trace data as a string
    # (typically a sequence of JSON objects, one per line)
    trace_data.append(event["value"])

session.on("Tracing.dataCollected", on_data_collected)

await session.tracing.end()

# Save the trace
with open("trace.json", "w") as f:
    f.write("".join(trace_data))
```

The trace file can be loaded in `chrome://tracing` or
[Perfetto UI](https://ui.perfetto.dev/).

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

Used to synchronize trace events across different clocks (e.g.,
browser and renderer processes).

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()
        await session.performance.enable()
        await session.profiler.enable()

        # Capture initial metrics
        before = await session.performance.get_metrics()
        before_heap = next(
            (m["value"] for m in before["metrics"] if m["name"] == "JSHeapUsedSize"),
            0,
        )

        # Start CPU profile
        await session.profiler.start()

        # Navigate and interact
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        # Run some JS
        await session.runtime.evaluate(
            "Array.from({length: 10000}, (_, i) => i * 2)",
            return_by_value=True,
        )

        # Stop CPU profile
        profile = await session.profiler.stop()
        print(f"CPU profile samples: {len(profile['profile']['samples'])}")

        # Capture final metrics
        after = await session.performance.get_metrics()
        after_heap = next(
            (m["value"] for m in after["metrics"] if m["name"] == "JSHeapUsedSize"),
            0,
        )
        print(f"Heap delta: {(after_heap - before_heap) / 1024:.1f} KB")

        await session.close()

asyncio.run(main())
```
