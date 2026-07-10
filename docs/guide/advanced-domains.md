# Advanced Domains

cdpwave covers all 60 CDP domains. This guide covers the remaining domains
not covered in other guides: Accessibility, CSS, Overlay, Security, Audits,
WebAuthn, Animation, LayerTree, ServiceWorker, Media, DOMSnapshot,
DOMStorage, Autofill, BluetoothEmulation, FedCM, WebAudio, and more.

## Accessibility

The `Accessibility` domain exposes the browser's accessibility tree —
the same tree used by screen readers and other assistive technologies.
Each node has a role (button, link, textbox), name, and state (focused,
checked, disabled).

!!! tip "When to use"
    Use the accessibility tree to verify ARIA implementations, test
    screen reader compatibility, and audit pages for WCAG compliance.

```python
await session.accessibility.enable()

# Get the full AX tree
result = await session.accessibility.get_full_ax_tree()
for node in result["nodes"]:
    print(f"Role: {node['role']['value']}, Name: {node.get('name', {}).get('value', '')}")
```

Get AX tree for a specific node (useful for checking a single
component):

```python
result = await session.accessibility.get_partial_ax_tree(
    node_id=1,
    fetch_relatives=True,
)
```

Get the root AX node:

```python
result = await session.accessibility.get_root_ax_node()
```

## CSS

The `CSS` domain provides access to the browser's CSS engine. You can
inspect computed styles, inline styles, matched rules, and manipulate
stylesheets programmatically.

!!! note "Requires DOM node IDs"
    CSS methods operate on DOM node IDs. Use `session.dom` methods
    (e.g., `query_selector`) to obtain node IDs first.

### Enable CSS domain

```python
await session.css.enable()
```

### Get computed styles

Computed styles are the final resolved values after applying all
CSS rules and inheritance:

```python
styles = await session.css.get_computed_style_for_node(node_id=1)
for prop in styles["computedStyle"]:
    print(f"{prop['name']}: {prop['value']}")
```

### Get inline styles

Inline styles are those set via the `style` attribute:

```python
result = await session.css.get_inline_styles_for_node(node_id=1)
print(result["inlineStyle"])
```

### Get matched styles

See which CSS rules match a node, including their source
stylesheets and specificity:

```python
result = await session.css.get_matched_styles_for_node(node_id=1)
for rule in result["matchedCSSRules"]:
    print(rule["rule"]["selectorList"]["text"])
```

### Get and set stylesheet text

```python
result = await session.css.get_style_sheet_text(style_sheet_id="ss1")
print(result["text"])

await session.css.set_style_sheet_text(
    stylesheet_id="ss1",
    text=".my-class { color: red; }",
)
```

### Add a CSS rule

```python
result = await session.css.add_rule(
    style_sheet_id="ss1",
    rule_text=".highlight { background: yellow; }",
)
```

### Create a new stylesheet

Inject a new stylesheet into a frame:

```python
result = await session.css.create_style_sheet(frame_id="frame1")
sheet_id = result["styleSheetId"]
```

### Force pseudo state

Simulate `:hover`, `:focus`, `:active` etc. without user
interaction — useful for testing pseudo-state styles:

```python
await session.css.force_pseudo_state(
    node_id=1,
    pseudo_state=["hover"],
)
```

### Get media queries

List all media queries in the page:

```python
result = await session.css.get_media_queries()
for media in result["medias"]:
    print(f"Media: {media['text']}")
```

### Get background colors

```python
result = await session.css.get_background_colors(node_id=1)
print(result["backgroundColors"])
```

---

## Overlay

The `Overlay` domain controls DevTools' visual overlays — highlighting,
FPS counters, paint rects, and debug borders. These are the same visual
aids shown in DevTools' Elements panel.

!!! note "Visual only"
    Overlay methods only affect what's drawn on screen. They don't
    modify the DOM or change page behavior. Useful for debugging
    and visual testing.

### Enable overlay

```python
await session.overlay.enable()
```

### Highlight a node

Draw a highlight box around a DOM node with configurable colors
and info:

```python
await session.overlay.highlight_node(
    highlight_config={
        "showInfo": True,
        "showStyles": True,
        "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
    },
    node_id=1,
)
```

### Highlight a frame

```python
await session.overlay.highlight_frame(
    frame_id="frame1",
    highlight_config={"showInfo": True},
)
```

### Clear highlight

```python
await session.overlay.clear_highlight()
```

### Set inspect mode

Enter node inspection mode — the browser highlights elements on
hover, like DevTools' inspect tool:

```python
await session.overlay.set_inspect_mode(
    mode="searchForNode",
    highlight_config={"showInfo": True},
)
```

### Visual debugging aids

```python
# Show FPS counter
await session.overlay.set_show_fps_counter(show=True)

# Show paint rects (areas being repainted)
await session.overlay.set_show_paint_rects(show=True)

# Show debug borders around elements
await session.overlay.set_show_debug_borders(show=True)
```

### Paused in debugger message

Display a custom message when the debugger is paused:

```python
await session.overlay.set_paused_in_debugger_message(message="Paused in Python debugger")
```

## Security

The `Security` domain handles SSL/TLS certificate errors and security
state. Use it to bypass certificate errors during testing or to monitor
security state changes.

### Handle certificate errors

```python
async def on_cert_error(event: dict) -> None:
    # Override to continue despite the error
    await session.security.handle_certificate_error(
        event_id=event["eventId"],
        action="continue",
    )

session.on("Security.certificateError", on_cert_error)
await session.security.enable()
```

Certificate error actions:

- **`"continue"`** — proceed despite the error.
- **`"cancel"`** — cancel the navigation.

### Override security settings

Automatically override all certificate errors:

```python
await session.security.set_override_certificate_errors(override=True)
```

!!! warning "Security implications"
    Overriding certificate errors bypasses TLS verification. Only
    use this in testing environments with self-signed certificates.

## Audits

The `Audits` domain provides accessibility and performance audits.

### Check contrast

Check color contrast for accessibility compliance:

```python
result = await session.audits.check_contrast(
    node_id=1,
    contrast_algorithm="AA",
)
for issue in result["issues"]:
    print(f"Contrast ratio: {issue['contrastRatio']}")
```

Contrast algorithms: `"AA"` (4.5:1 for normal text) or `"AAA"`
(7:1 for normal text).

### Get encoded response

Retrieve a response body in a compressed format:

```python
result = await session.audits.get_encoded_response(
    request_id="req1",
    encoding="webp",
)
```

---

## WebAuthn

The `WebAuthn` domain simulates WebAuthn authenticators for testing
Web Authentication API flows without physical hardware. You can create
virtual authenticators that respond to `navigator.credentials.create()`
and `navigator.credentials.get()` calls.

### Enable and create a virtual authenticator

```python
await session.web_authn.enable()

result = await session.web_authn.add_virtual_authenticator(
    options={
        "protocol": "ctap2",
        "transport": "internal",
        "hasResidentKey": True,
        "hasUserVerification": True,
        "isUserVerified": True,
    },
)
authenticator_id = result["authenticatorId"]
```

### Add a credential

```python
await session.web_authn.add_credential(
    authenticator_id=authenticator_id,
    credential={
        "credentialId": "cred1",
        "isResidentCredential": True,
        "rpId": "example.com",
        "privateKey": "private-key-base64",
        "userHandle": "user1",
    },
)
```

### Get credentials

```python
result = await session.web_authn.get_credentials(
    authenticator_id=authenticator_id,
)
for cred in result["credentials"]:
    print(f"Credential: {cred['credentialId']}")
```

### Set user verified

```python
await session.web_authn.set_user_verified(
    authenticator_id=authenticator_id,
    is_user_verified=True,
)
```

### Remove a credential

```python
await session.web_authn.remove_credential(
    authenticator_id=authenticator_id,
    credential_id="cred1",
)
```

### Remove authenticator

```python
await session.web_authn.remove_virtual_authenticator(
    authenticator_id=authenticator_id,
)
```

## Animation

The `Animation` domain controls CSS animations and Web Animations API.
You can pause, play, seek, and modify animations — useful for testing
animation states and capturing specific frames.

### Enable animation domain

```python
await session.animation.enable()
```

### Set playback rate

```python
await session.animation.set_playback_rate(playback_rate=2.0)  # 2x speed
```

### Pause and resume all animations

```python
await session.animation.pause_all()
await session.animation.resume_all()
```

### Seek animations

Jump to a specific point in an animation timeline:

```python
await session.animation.seek_animations(
    animations=["anim1", "anim2"],
    current_time=500,  # 500ms into the animation
)
```

### Release animations

```python
await session.animation.release_animations(animations=["anim1"])
```

## LayerTree

The `LayerTree` domain exposes the browser's compositor layer tree.
Layers are the intermediate rendering units between the DOM and the
screen. The browser composites layers together to produce the final
image.

!!! tip "When to use"
    Use LayerTree to debug rendering performance issues, understand
    compositing layers, and identify layers that cause unnecessary
    repaints.

### Enable layer tree

```python
await session.layer_tree.enable()
```

### Get compositing layers

```python
result = await session.layer_tree.get_layers()
for layer in result["layers"]:
    print(f"Layer: {layer['layerId']} bounds={layer['bounds']}")
```

### Compositing reasons

Understand why a node was promoted to its own compositing layer:

```python
result = await session.layer_tree.compositing_reasons(layer_id="layer1")
for reason in result["compositingReasons"]:
    print(f"Reason: {reason}")
```

### Capture layer snapshot

```python
result = await session.layer_tree.capture_snapshot()
print(f"Snapshot tiles: {len(result['timings'])}")
```

## ServiceWorker

The `ServiceWorker` domain controls service worker lifecycle and
events. Service workers are background scripts that intercept network
requests, manage caches, and handle push notifications.

### Enable service worker domain

```python
await session.service_worker.enable()
```

### Deliver push message

Simulate a push notification to a service worker:

```python
await session.service_worker.deliver_push_message(
    origin="https://example.com",
    registration_id="reg1",
    data="push payload",
)
```

### Dispatch sync event

Trigger a Background Sync event:

```python
await session.service_worker.dispatch_sync_event(
    origin="https://example.com",
    registration_id="reg1",
    tag="sync-tag",
    last_chance=False,
)
```

### Stop service worker

```python
await session.service_worker.stop_worker(version_id="ver1")
```

### Unregister service worker

```python
await session.service_worker.unregister(
    scope="https://example.com/",
)
```

## Media

The `Media` domain monitors media player events — playback state,
buffering, errors, and metadata. It's read-only: you observe media
player behavior but cannot control playback directly.

### Enable media domain

```python
await session.media.enable()
```

### Listen to player events

```python
async def on_player_created(event: dict) -> None:
    print(f"Media player created: {event['playerId']}")

async def on_player_event(event: dict) -> None:
    print(f"Player {event['playerId']}: {event['event']['eventName']}")

session.on("Media.playerCreated", on_player_created)
session.on("Media.playerEvent", on_player_event)
```

## SystemInfo

The `SystemInfo` domain provides hardware and process information.
It's accessed via `client.system_info` (browser-level, not per-session).

### Get GPU info

```python
result = await client.system_info.get_info()
gpu = result["gpu"]
print(f"GPU: {gpu['devices'][0]['vendorString']} {gpu['devices'][0]['deviceString']}")
```

### Get process info

List all browser processes and their CPU usage:

```python
result = await client.system_info.get_process_info()
for process in result["processInfo"]:
    print(f"PID {process['id']}: {process['type']} CPU={process['cpuTime']}")
```

## Browser

The `Browser` domain controls browser-level operations: version info,
window management, permissions, and downloads. It's accessed via
`client.browser` (browser-level, not per-session).

### Get browser version

```python
result = await client.browser.get_version()
print(f"Browser: {result['product']}")
print(f"Protocol: {result['protocolVersion']}")
print(f"User agent: {result['userAgent']}")
```

### Set window bounds

Resize and reposition browser windows:

```python
await client.browser.set_window_bounds(
    window_id=1,
    bounds={"left": 0, "top": 0, "width": 1280, "height": 720},
)
```

### Grant permissions

Programmatically grant browser permissions without user prompts:

```python
await client.browser.grant_permissions(
    permissions=["geolocation", "notifications"],
    origin="https://example.com",
)
```

Available permissions include: `geolocation`, `notifications`,
`camera`, `microphone`, `midi`, `clipboard-read`, `clipboard-write`.

### Set download behavior

Control where and whether downloads are saved:

```python
await client.browser.set_download_behavior(
    behavior="allow",
    download_path="/tmp/downloads",
)
```

Use `behavior="deny"` to block all downloads, or
`behavior="allowAndName"` to let the browser auto-name files.

---

## DOMSnapshot

The `DOMSnapshot` domain captures a full DOM snapshot including computed
styles, text content, and layout information in a single call. It's more
efficient than walking the DOM tree with `DOM.getDocument` when you need
style data.

```python
await session.dom_snapshot.enable()

result = await session.dom_snapshot.capture_snapshot(
    computed_styles=["color", "display", "background-color"],
)
for doc in result["documents"]:
    print(f"Document: {len(doc['nodes'])} nodes")

await session.dom_snapshot.disable()
```

!!! tip "Performance"
    `DOMSnapshot.captureSnapshot` is significantly faster than calling
    `DOM.getDocument` + `CSS.getComputedStyleForNode` for each node.

### Capture with experimental options

Include blended background colors and text color opacities:

```python
result = await session.dom_snapshot.capture_snapshot(
    computed_styles=["color"],
    include_blended_background_colors=True,
    include_text_color_opacities=True,
)
```

## DOMStorage

The `DOMStorage` domain provides access to `localStorage` and
`sessionStorage` for any origin. Storage is accessed via a
`storage_id` containing the security origin and whether it's
local or session storage.

```python
storage_id = {
    "securityOrigin": "https://example.com",
    "isLocalStorage": True,
}

# Set an item
await session.dom_storage.set_dom_storage_item(storage_id, "key1", "value1")

# Get all items
result = await session.dom_storage.get_dom_storage_items(storage_id)
for item in result["entries"]:
    print(f"{item['key']}: {item['value']}")

# Remove an item
await session.dom_storage.remove_dom_storage_item(storage_id, "key1")

# Clear all storage
await session.dom_storage.clear_dom_storage_items(storage_id)
```

## Autofill

The `Autofill` domain allows you to simulate browser autofill
behavior — injecting address data into forms as if the user had
selected a saved address.

```python
await session.autofill.enable()

await session.autofill.set_addresses([
    {
        "name": "Test User",
        "streetAddress": "123 Main St",
        "city": "Test City",
        "state": "CA",
        "postalCode": "12345",
        "country": "US",
    },
])

await session.autofill.disable()
```

!!! warning "Experimental domain"
    `Autofill` is experimental and may not be available in all Chrome
    versions. Catch `CommandError` with code `-32601` to handle
    unavailable domains gracefully.

## BluetoothEmulation

The `BluetoothEmulation` domain simulates Bluetooth adapters and
devices for testing Web Bluetooth API interactions without physical
hardware.

```python
await session.bluetooth_emulation.enable()

# Set a simulated central state
await session.bluetooth_emulation.set_simulated_central_state("powered-on")

# Simulate a preconnected peripheral device
await session.bluetooth_emulation.simulate_preconnected_peripheral(
    address="00:11:22:33:44:55",
    name="Test Device",
    known_service_uuids=["0000180f-0000-1000-8000-00805f9b34fb"],
)

# Simulate an advertisement
await session.bluetooth_emulation.simulate_advertisement(
    advertisement={"type": "broadcast", "serviceUuids": []},
)

await session.bluetooth_emulation.disable()
```

!!! warning "Experimental domain"
    `BluetoothEmulation` is experimental and may not be available in
    all Chrome versions.

## FedCM

The `FedCM` domain controls the Federated Credential Management API,
allowing you to test identity provider flows without real network
requests.

```python
await session.fed_cm.enable()

# Reset any pending FedCM dialog
await session.fed_cm.reset_cooldown()

# Select an account in a FedCM dialog (requires dialog ID from event)
# await session.fed_cm.select_account(dialog_id="dialog-1", account_index=0)

# Click the dialog's continue button (requires dialog ID from event)
# await session.fed_cm.click_dialog_button(dialog_id="dialog-1", button="ConfirmIdpLoginContinue")

# Dismiss a dialog
# await session.fed_cm.dismiss_dialog(dialog_id="dialog-1", trigger_cooldown=True)

await session.fed_cm.disable()
```

!!! note "Dialog ID required"
    Most FedCm methods require a `dialog_id` obtained from the
    `FedCm.dialogShown` event. Register an event handler to capture
    the dialog ID before calling `select_account` or
    `click_dialog_button`.

## WebAudio

The `WebAudio` domain inspects Web Audio API contexts — AudioContexts,
realtime audio data, and context lifecycle events.

```python
await session.web_audio.enable()

# Create an AudioContext in the page
result = await session.runtime.evaluate(
    "new AudioContext().id", return_by_value=True,
)
ctx_id = result["result"]["value"]

if ctx_id:
    realtime = await session.web_audio.get_realtime_data(ctx_id)
    print(f"Context load: {realtime.get('contextLoadTime')}")

await session.web_audio.disable()
```

## Ads

The `Ads` domain provides ad metrics inspection capabilities.

```python
result = await session.ads.get_ad_metrics()
print(result)
```

!!! note "Simple domain"
    The `Ads` domain has a single method (`get_ad_metrics`) that
    retrieves ad-related metrics for the current page.

## CrashReportContext

The `CrashReportContext` domain provides access to crash report
context entries for the browser process.

```python
result = await session.crash_report_context.get_entries()
for entry in result.get("entries", []):
    print(entry)
```

## DigitalCredentials

The `DigitalCredentials` domain simulates digital credentials API
behavior for testing without real credential providers.

```python
await session.digital_credentials.set_virtual_wallet_behavior(
    behavior="spare",
)
```

## FileSystem

The `FileSystem` domain provides access to the File System Access API.

```python
result = await session.file_system.get_directory()
```

!!! warning "Permissions required"
    `FileSystem.getDirectory` requires the page to have been granted
    file system access permissions. Calls without permission will
    raise `CommandError`.

## SmartCardEmulation

The `SmartCardEmulation` domain simulates smart card operations for
testing Web Smart Card API interactions. It provides methods to report
results for various smart card operations.

```python
await session.smart_card_emulation.enable()

# Report the result of establishing a context
await session.smart_card_emulation.report_establish_context_result(
    context_id="ctx-1",
    result=0,
)

# Report the result of listing readers
await session.smart_card_emulation.report_list_readers_result(
    context_id="ctx-1",
    readers=[{"name": "Reader 1", "state": 0}],
)

# Report the result of connecting to a card
await session.smart_card_emulation.report_connect_result(
    context_id="ctx-1",
    reader="Reader 1",
    card_handle="card-1",
    active_protocol=1,
    result=0,
)

# Report an error
await session.smart_card_emulation.report_error(
    context_id="ctx-1",
    error=1,
)

await session.smart_card_emulation.disable()
```

!!! warning "Experimental domain"
    `SmartCardEmulation` is experimental and may not be available in
    all Chrome versions.

## WebMCP

The `WebMCP` domain integrates the Model Context Protocol with the
browser, enabling AI-driven page interactions.

```python
await session.web_mcp.enable()

# Invoke a tool registered by the page
result = await session.web_mcp.invoke_tool(
    tool_name="search",
    arguments={"query": "hello"},
)

# Cancel an ongoing invocation
await session.web_mcp.cancel_invocation(invocation_id="inv-1")

await session.web_mcp.disable()
```

!!! warning "Experimental domain"
    `WebMCP` is experimental and may not be available in all Chrome
    versions.
