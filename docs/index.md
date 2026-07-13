# cdpwave

Chrome DevTools Protocol for Python — direct, typed, async.

cdpwave talks to Chrome over a raw WebSocket. No Node.js, no ChromeDriver, no browser downloads. Just pure Python with full type hints and async-first design.

## Why cdpwave?

- **Full CDP coverage** — all 60 CDP domains implemented with 685 typed methods
- **Direct WebSocket** — single connection to Chrome's DevTools Protocol, no intermediate layers
- **Fully typed** — `mypy --strict` across the entire codebase, IDE autocomplete everywhere
- **Async-first** — built on `asyncio`, no threading, no blocking calls
- **Browser detection** — finds Chrome, Edge, Brave, or Chromium already on your system
- **Flatten sessions** — one WebSocket for all tabs via `Target.attachToTarget` + `sessionId`
- **Escape hatch** — `session.send("Any.CDPMethod", params)` for any uncovered command
- **HTTP discovery** — typed access to `/json/version` and `/json/list` endpoints
- **Integration tested** — 322 integration tests against a real Chromium browser covering all domains
- **MIT licensed** — permissive, compatible with any use

## Install

```bash
pip install cdpwave
```

## Quick start

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])  # "Example Domain"
        await session.close()

asyncio.run(main())
```

## CDP domain coverage

cdpwave implements all 60 domains of the Chrome DevTools Protocol with typed
Python wrappers. Every domain is accessible as a property on `CDPSession`
(or `CDPClient` for browser-level domains).

### Core domains

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Page** | `session.page` | 64 | Navigation, screenshots, PDF, CSP bypass, scripts, frame tree |
| **Runtime** | `session.runtime` | 23 | JS evaluation, remote objects, bindings, compile/run scripts |
| **Network** | `session.network` | 41 | Monitoring, cookies, cache, blocking, network emulation |
| **DOM** | `session.dom` | 56 | Inspection, manipulation, search, box model, node location |
| **Target** | `session.target` | 19 | Session management, browser contexts, target discovery |
| **Log** | `session.log` | 5 | Console log entries, violation reporting |
| **Console** | `session.console` | 3 | Console API (deprecated, use Runtime instead) |

### Emulation & input

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Emulation** | `session.emulation` | 57 | Device metrics, CPU throttling, sensors, dark mode, JS disable |
| **Input** | `session.input` | 14 | Keyboard, mouse, touch, drag, pinch, scroll, tap gestures |
| **Sensor** | `session.sensor` | 4 | Accelerometer, gyroscope, magnetometer overrides |
| **DeviceOrientation** | `session.device_orientation` | 2 | Device orientation override |
| **DeviceAccess** | `session.device_access` | 4 | Bluetooth/USB device selection prompts |

### Network & fetch

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Fetch** | `session.fetch` | 11 | Request interception, mocking, auth, response body streaming |
| **CacheStorage** | `session.cache_storage` | 6 | Cache API inspection and deletion |
| **IndexedDB** | `session.indexed_db` | 9 | IndexedDB database and object store inspection |
| **Storage** | `session.storage` | 35 | Cookies, quotas, trust tokens, storage tracking, shared storage |

### Debugging & profiling

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Debugger** | `session.debugger` | 25 | Breakpoints, stepping, blackboxing, variable inspection |
| **Profiler** | `session.profiler` | 9 | CPU profiling, precise code coverage |
| **HeapProfiler** | `session.heap_profiler` | 10 | Heap snapshots, allocation sampling, GC, object tracking |
| **DOMDebugger** | `session.dom_debugger` | 10 | DOM breakpoints, event listener breakpoints, XHR breakpoints |
| **EventBreakpoints** | `session.event_breakpoints` | 4 | Instrumentation breakpoints for native operations and events |

### Performance & tracing

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Performance** | `session.performance` | 4 | Runtime metrics, timeline events |
| **PerformanceTimeline** | `session.performance_timeline` | 1 | Timeline events (LCP, FID, CLS) |
| **Tracing** | `session.tracing` | 6 | Chrome tracing, category discovery, clock sync, memory dumps |

### Rendering & CSS

| Domain | Property | Methods | Description |
|---|---|---|---|
| **CSS** | `session.css` | 42 | Styles, stylesheets, rules, pseudo states, media queries |
| **Overlay** | `session.overlay` | 31 | Paint rects, debug borders, FPS, highlighting, inspect mode |
| **Animation** | `session.animation` | 9 | Playback rate, pausing, seeking, replaying animations |
| **LayerTree** | `session.layer_tree` | 9 | Compositing layers, snapshots, compositing reasons |

### Security & audits

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Security** | `session.security` | 5 | Certificate error handling, insecure connection overrides |
| **Audits** | `session.audits` | 4 | Contrast checking, encoded response inspection |
| **Accessibility** | `session.accessibility` | 7 | AX tree inspection, roles, names, states |

### Browser & system

| Domain | Property | Methods | Description |
|---|---|---|---|
| **Browser** | `client.browser` | 17 | Version, window bounds, permissions, download behavior |
| **SystemInfo** | `client.system_info` | 4 | GPU info, process info, feature state |
| **Memory** | `session.memory` | 11 | DOM counters, leak detection, pressure notifications |
| **IO** | `session.io` | 3 | Stream reading, blob resolution |
| **Schema** | `session.schema` | 1 | Domain discovery |

### Workers & services

| Domain | Property | Methods | Description |
|---|---|---|---|
| **ServiceWorker** | `session.service_worker` | 11 | Push messages, sync events, worker lifecycle |
| **Worker** | `session.worker` | 0 | Event-only: worker errors and messages |
| **Extensions** | `session.extensions` | 8 | Load unpacked, storage items |
| **PWA** | `session.pwa` | 7 | Install, uninstall, app state |
| **Preload** | `session.preload` | 2 | Speculative loading, prefetch, prerender events |

### Mobile & cast

| Domain | Property | Methods | Description |
|---|---|---|---|
| **WebAuthn** | `session.web_authn` | 11 | Virtual authenticators, credentials, presence simulation |
| **Cast** | `session.cast` | 6 | Tab/desktop mirroring, sink selection |
| **Tethering** | `session.tethering` | 2 | Browser port binding |

### Experimental & other

| Domain | Property | Methods | Description |
|---|---|---|---|
| **HeadlessExperimental** | `session.headless_experimental` | 3 | Headless window bounds (deprecated) |
| **Media** | `session.media` | 4 | Media player properties and events |
| **BackgroundService** | `session.background_service` | 4 | Background service event recording |
| **Inspector** | `session.inspector` | 2 | Inspector domain notifications and lifecycle events |
| **Ads** | `session.ads` | 1 | Ad metrics inspection |
| **Autofill** | `session.autofill` | 5 | Autofill address injection |
| **BluetoothEmulation** | `session.bluetooth_emulation` | 15 | Virtual Bluetooth adapters and devices |
| **CrashReportContext** | `session.crash_report_context` | 1 | Crash report context entries |
| **DigitalCredentials** | `session.digital_credentials` | 1 | Digital credentials wallet behavior |
| **DOMSnapshot** | `session.dom_snapshot` | 4 | Full DOM snapshot with computed styles |
| **DOMStorage** | `session.dom_storage` | 4 | Local/session storage inspection |
| **FedCM** | `session.fed_cm` | 7 | Federated Credential Management |
| **FileSystem** | `session.file_system` | 1 | File system access API |
| **SmartCardEmulation** | `session.smart_card_emulation` | 12 | Smart card emulation for testing |
| **WebAudio** | `session.web_audio` | 3 | Web Audio context inspection |
| **WebMCP** | `session.web_mcp` | 4 | Model Context Protocol integration |

## Next steps

- [Quickstart](quickstart.md) — 10-minute tutorial
- [Guide](guide/installation.md) — in-depth coverage of each feature
- [Cookbook](cookbook/connect-existing.md) — recipes for common scenarios
- [API Reference](api/client.md) — auto-generated docs for every class
- [Migration](migration/pyppeteer.md) — coming from pyppeteer or pychrome
