# Advanced Domains

cdpwave covers all 48 CDP domains. This guide covers the remaining domains
not covered in other guides: Accessibility, CSS, Overlay, Security, Audits,
WebAuthn, Animation, LayerTree, ServiceWorker, Media, and more.

## Accessibility

Inspect the accessibility tree:

```python
await session.accessibility.enable()

# Get the full AX tree
result = await session.accessibility.get_full_ax_tree()
for node in result["nodes"]:
    print(f"Role: {node['role']['value']}, Name: {node.get('name', {}).get('value', '')}")
```

Get AX tree for a specific node:

```python
result = await session.accessibility.get_partial_ax_tree(
    node_id=1,
    fetch_relatives=True,
)
```

Get root AX node:

```python
result = await session.accessibility.get_root_ax_node()
```

---

## CSS

### Enable CSS domain

```python
await session.css.enable()
```

### Get styles for a node

```python
styles = await session.css.get_computed_style_for_node(node_id=1)
for prop in styles["computedStyle"]:
    print(f"{prop['name']}: {prop['value']}")
```

### Get inline styles

```python
result = await session.css.get_inline_styles_for_node(node_id=1)
print(result["inlineStyle"])
```

### Get matched styles

```python
result = await session.css.get_matched_styles_for_node(node_id=1)
for rule in result["matchedCSSRules"]:
    print(rule["rule"]["selectorList"]["text"])
```

### Get stylesheet text

```python
result = await session.css.get_style_sheet_text(style_sheet_id="ss1")
print(result["text"])
```

### Set stylesheet text

```python
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

```python
result = await session.css.create_style_sheet(frame_id="frame1")
sheet_id = result["styleSheetId"]
```

### Force pseudo state

```python
await session.css.force_pseudo_state(
    node_id=1,
    pseudo_state=["hover"],
)
```

### Get media queries

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

### Enable overlay

```python
await session.overlay.enable()
```

### Highlight a node

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

```python
await session.overlay.set_inspect_mode(
    mode="searchForNode",
    highlight_config={"showInfo": True},
)
```

### Show FPS counter

```python
await session.overlay.set_show_fps_counter(show=True)
```

### Show paint rects

```python
await session.overlay.set_show_paint_rects(show=True)
```

### Show debug borders

```python
await session.overlay.set_show_debug_borders(show=True)
```

### Paused in debugger message

```python
await session.overlay.set_paused_in_debugger_message(message="Paused in Python debugger")
```

---

## Security

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

### Override security settings

```python
await session.security.set_override_certificate_errors(override=True)
```

---

## Audits

### Check contrast

```python
result = await session.audits.check_contrast(
    node_id=1,
    contrast_algorithm="AA",
)
for issue in result["issues"]:
    print(f"Contrast ratio: {issue['contrastRatio']}")
```

### Get encoded response

```python
result = await session.audits.get_encoded_response(
    request_id="req1",
    encoding="webp",
)
```

---

## WebAuthn

### Enable WebAuthn

```python
await session.web_authn.enable()
```

### Add a virtual authenticator

```python
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

---

## Animation

### Enable animation domain

```python
await session.animation.enable()
```

### Set playback rate

```python
await session.animation.set_playback_rate(playback_rate=2.0)  # 2x speed
```

### Pause animations

```python
await session.animation.pause_all()
```

### Resume animations

```python
await session.animation.resume_all()
```

### Seek animations

```python
await session.animation.seek_animations(
    animations=["anim1", "anim2"],
    current_time=500,
)
```

### Release animations

```python
await session.animation.release_animations(animations=["anim1"])
```

---

## LayerTree

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

---

## ServiceWorker

### Enable service worker domain

```python
await session.service_worker.enable()
```

### Deliver push message

```python
await session.service_worker.deliver_push_message(
    origin="https://example.com",
    registration_id="reg1",
    data="push payload",
)
```

### Dispatch sync event

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

---

## Media

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

---

## SystemInfo

### Get GPU info

```python
result = await client.system_info.get_info()
gpu = result["gpu"]
print(f"GPU: {gpu['devices'][0]['vendorString']} {gpu['devices'][0]['deviceString']}")
```

### Get process info

```python
result = await client.system_info.get_process_info()
for process in result["processInfo"]:
    print(f"PID {process['id']}: {process['type']} CPU={process['cpuTime']}")
```

---

## Browser

### Get browser version

```python
result = await client.browser.get_version()
print(f"Browser: {result['product']}")
print(f"Protocol: {result['protocolVersion']}")
print(f"User agent: {result['userAgent']}")
```

### Set window bounds

```python
await client.browser.set_window_bounds(
    window_id=1,
    bounds={"left": 0, "top": 0, "width": 1280, "height": 720},
)
```

### Grant permissions

```python
await client.browser.grant_permissions(
    permissions=["geolocation", "notifications"],
    origin="https://example.com",
)
```

### Set download behavior

```python
await client.browser.set_download_behavior(
    behavior="allow",
    download_path="/tmp/downloads",
)
```
