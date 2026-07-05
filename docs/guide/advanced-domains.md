# Advanced Domains

cdpwave covers all 48 CDP domains. This guide covers the remaining domains
not covered in other guides: Accessibility, CSS, Overlay, Security, Audits,
WebAuthn, Animation, LayerTree, ServiceWorker, Media, and more.

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
