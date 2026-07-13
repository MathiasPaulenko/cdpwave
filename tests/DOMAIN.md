# cdpwave vs CDP — Comparación de dominios y métodos

Comparación contra `browser_protocol.json` + `js_protocol.json` (tip-of-tree, Sept 2025).

## Resumen

| Métrica | Valor |
|---|---|
| Dominios CDP | 52 |
| Dominios cdpwave | 60 (58 de CDP + `sensor` y `worker` extra) |
| Métodos CDP totales | 670 |
| Métodos implementados | 688 |
| Métodos faltantes | 36 |
| Métodos extra (convenience/aliases) | 53 |
| Cobertura de métodos | 94.6% |

## Cobertura por dominio

Ordenado por importancia para automatización de navegadores (cobertura tipo Playwright).

### Tier 1 — Críticos (core de automatización)

| Dominio | CDP | Impl | Faltan | Extra | Revisado |
|---|---:|---:|---:|---:|:---:|
| Page | 61 | 62 | 0 | 1 | ✅ |
| Runtime | 23 | 23 | 1 | 1 | ✅ |
| DOM | 53 | 54 | 1 | 2 | ✅ |
| Input | 13 | 14 | 0 | 1 | ✅ |
| Network | 41 | 34 | 2 | 2 | ✅ |
| Target | 18 | 19 | 0 | 1 | ✅ |
| Emulation | 47 | 57 | 0 | 10 | ✅ |

### Tier 2 — Importantes (features avanzadas)

| Dominio | CDP | Impl | Faltan | Extra | Revisado |
|---|---:|---:|---:|---:|:---:|
| Fetch | 9 | 11 | 0 | 2 | ✅ |
| Storage | 34 | 34 | 0 | 0 | ✅ |
| DOMStorage | 6 | 6 | 0 | 1 | ✅ |
| Browser | 20 | 21 | 0 | 1 | ✅ |
| Log | 5 | 5 | 0 | 0 | ✅ |
| Accessibility | 8 | 8 | 0 | 0 | ✅ |
| CSS | 38 | 38 | 0 | 5 | ✅ |
| Console | 3 | 3 | 0 | 0 | ✅ |

### Tier 3 — Útiles (escenarios específicos)

| Dominio | CDP | Impl | Faltan | Extra | Revisado |
|---|---:|---:|---:|---:|:---:|
| ServiceWorker | 12 | 11 | 4 | 3 |✅  |
| CacheStorage | 5 | 5 | 0 | 0 | ✅ |
| IndexedDB | 9 | 9 | 0 | 0 | ✅ |
| Performance | 4 | 4 | 0 | 0 | ✅ |
| Security | 6 | 6 | 0 | 0 | ✅ |
| WebAuthn | 13 | 13 | 0 | 0 | ✅ |
| Debugger | 33 | 25 | 10 | 2 | |
| DOMSnapshot | 4 | 4 | 0 | 0 | ✅ |
| Overlay | 31 | 28 | 3 | 0 | ✅ |
| PerformanceTimeline | 1 | 1 | 0 | 0 | ✅ |
| FileSystem | 1 | 1 | 0 | 0 | ✅ |

### Tier 4 — Niche (casos especializados)

| Dominio | CDP | Impl | Faltan | Extra | Revisado |
|---|---:|---:|---:|---:|:---:|
| Profiler | 9 | 9 | 0 | 0 | ✅ |
| HeapProfiler | 12 | 12 | 0 | 0 | ✅ |
| Memory | 11 | 11 | 0 | 0 | ✅ |
| Tracing | 6 | 6 | 0 | 0 | ✅ |
| LayerTree | 9 | 9 | 0 | 0 | ✅ |
| IO | 3 | 3 | 0 | 0 | ✅ |
| PWA | 7 | 7 | 0 | 0 | ✅ |
| Extensions | 8 | 8 | 0 | 0 | ✅ |
| SystemInfo | 3 | 4 | 0 | 1 | ✅ |
| Preload | 2 | 2 | 0 | 0 | ✅ |
| DeviceAccess | 4 | 4 | 0 | 0 | ✅ |
| Audits | 4 | 5 | 0 | 1 | ✅ |
| Animation | 10 | 12 | 0 | 2 | ✅ |
| FedCm | 7 | 7 | 0 | 0 | ✅ |
| Schema | 1 | 1 | 0 | 0 | ✅ |

### Tier 5 — Raramente necesario para automatización

| Dominio | CDP | Impl | Faltan | Extra | Revisado |
|---|---:|---:|---:|---:|:---:|
| HeadlessExperimental | 3 | 3 | 0 | 0 | ✅ |
| DOMDebugger | 10 | 10 | 0 | 0 | ✅ |
| EventBreakpoints | 3 | 4 | 0 | 1 | ✅ |
| Inspector | 2 | 2 | 0 | 0 | ✅ |
| Cast | 6 | 6 | 0 | 0 | ✅ |
| Tethering | 2 | 2 | 0 | 0 | ✅ |
| DeviceOrientation | 2 | 2 | 0 | 0 | |
| Media | 2 | 4 | 0 | 2 | |
| Autofill | 4 | 6 | 0 | 2 | ✅ |
| BackgroundService | 4 | 4 | 0 | 0 | ✅ |
| BluetoothEmulation | 15 | 15 | 0 | 0 | ✅ |
| SmartCardEmulation | 12 | 12 | 0 | 0 | ✅ |
| WebAudio | 3 | 3 | 0 | 0 | ✅ |
| WebMCP | 2 | 2 | 0 | 0 | ✅ |
| Ads | 1 | 1 | 0 | 0 | ✅ |
| CrashReportContext | 1 | 1 | 0 | 0 | ✅ |
| DigitalCredentials | 1 | 1 | 0 | 0 | ✅ |
| **TOTAL** | **670** | **681** | **30** | **53** |

## Métodos faltantes (29)

### Browser (0)

All 9 missing methods implemented. See detailed review below.

### Debugger (10)

- `continue_to_location`
- `disassemble_wasm_module`
- `get_wasm_bytecode`
- `next_wasm_disassembly_chunk`
- `pause_on_async_call`
- `restart_frame`
- `set_async_call_stack_depth`
- `set_blackbox_execution_contexts`
- `set_blackboxed_ranges`
- `set_instrumentation_breakpoint`

### ServiceWorker (4)

- `dispatch_periodic_sync_event`
- `set_force_update_on_page_load`
- `stop_all_workers`
- `update_registration`

### CSS (0)

- ~~`get_style_sheet_text`~~ — implementado como `get_style_sheet_text` (snake_case)
- ~~`set_style_sheet_text`~~ — implementado como `set_style_sheet_text` (snake_case)
- ~~`set_style_texts`~~ — implementado como `set_style_texts` (snake_case)

### Tethering (0)

- ~~`bind`~~ — implementado como `bind` (corregido en revisión)
- ~~`unbind`~~ — implementado como `unbind` (corregido en revisión)

### Tracing (0)

All 6 CDP methods implemented. See detailed review below.

### Network (2 — naming mismatches)

- `set_blocked_ur_ls` — cdpwave usa `set_blocked_urls`
- `set_extra_http_headers` — cdpwave usa `set_extra_request_headers`

### 1 faltante cada uno

- **CacheStorage**: `request_cached_response`
- ~~**Cast**: `start_desktop_mirroring`~~ — implementado como `start_desktop_mirroring` (corregido en revisión)
- **DOM**: `get_attributes` — cdpwave usa `get_attribute` con filtrado por nombre
- ~~**DeviceAccess**: `select_prompt`~~ — implementado como `select_prompt` (corregido en revisión)
- ~~**EventBreakpoints**: `disable`, `remove_instrumentation_breakpoint`~~ — implementados en revisión (`disable` ya existía, `clear_instrumentation_breakpoint` renombrado a `remove_instrumentation_breakpoint`)
- **Runtime**: `set_max_call_stack_size_to_capture`

## Métodos extra en cdpwave (55)

Convenience methods y aliases que no existen como comandos CDP separados:

- **Page**: `go_back`, `go_forward`, `stop` (combinan `get_navigation_history` + `navigate_to_history_entry`)
- **DOM**: `get_attribute` (filtra `DOM.getAttributes` por nombre), `set_text_content`
- **Emulation**: 6 métodos clear/reset convenience (`clear_auto_dark_mode_override`, `clear_emulated_media`, `clear_emulated_vision_deficiency`, `clear_default_background_color_override`, `clear_timezone_override`, `set_emulated_media_feature`)
- **Browser**: `get_bounds`/`set_bounds` (aliases de `get_window_bounds`/`set_window_bounds`), `get_command_line`, `get_cpu_profile`, `get_heap_profile`, `reset_histograms`, `_call` (interno)
- **CSS**: `get_inline_styles` (alias de `get_inline_styles_for_node`), `get_stylesheet_text`/`set_stylesheet_text` (aliases de `get_style_sheet_text`/`set_style_sheet_text`), `set_rule_style`, `set_style_text` (convenience wrappers para `set_style_texts`)
- **Network**: `set_blocked_urls` (alias de `set_blocked_ur_ls`), `set_extra_request_headers` (alias de `set_extra_http_headers`)
- **Input**: `type_text` (convenience para `insert_text`)
- **Runtime**: `collect_garbage`
- **Fetch**: `continue_request_with_auth`, `get_request_post_data`
- **ServiceWorker**: `get_messages`, `inspect_worker`, `update`
- **Animation**: `replay`, `seek_to`
- **Audits**: `check_contrast`
- **Autofill**: `trigger_fill` (alias de `trigger`), `trigger_fill_after_save`
- **CacheStorage**: `disable`, `enable`
- **DOMStorage**: `clear_dom_storage_items`
- **Debugger**: `get_properties`, `set_breakpoints_by_url`
- ~~**DeviceAccess**: `select_bluetooth_device`~~ — renombrado a `select_prompt` en revisión (coincide con Go source)
- **EventBreakpoints**: `clear_instrumentation_breakpoint` — alias deprecated de `remove_instrumentation_breakpoint`
- **LayerTree**: _(ninguno — `get_layers` removido en revisión, no existe en CDP spec ni Go source)_
- ~~**Media**: `get_player_properties`, `get_players`~~ — removidos en revisión (no existen en CDP spec ni Go source)
- ~~**Preload**: `get_preload_policy`, `set_preload_policy`~~ — removidos en revisión (no existen en Go source)
- **Storage**: _(ninguno — `set_storage_bucket_info` removido en revisión, no existe en CDP spec ni Go source)_
- **SystemInfo**: _(ninguno — `get_gpu_info` removido en revisión, no existe en Go source ni CDP spec)_
- **Tethering**: _(ninguno — `enable`/`disable` removidos en revisión, no existen en CDP spec ni Go source; eran métodos espurios)_
- **Tracing**: _(ninguno — `request_clock_sync_marker` removido en revisión, no existe en Go source ni CDP spec)_

## Dominios extra en cdpwave

- **`sensor`** — wrapper para `Sensor` (presente en CDP pero como parte de Emulation)
- **`worker`** — placeholder sin métodos

## Naming mismatches

| CDP (camelCase) | cdpwave (snake_case) | Issue |
|---|---|---|
| `setBlockedURLs` | `set_blocked_urls` | CDP usa `URLs` → `ur_ls` en snake estricto |
| `setExtraHTTPHeaders` | `set_extra_request_headers` | Renombrado en cdpwave |
| `forciblyPurgeJavaScriptMemory` | `forcibly_purge_javascript_memory` | `JavaScript` → `java_script` vs `javascript` |

Estos son funcionales pero el nombre no coincide exactamente con la conversión automática.

## Notas de revisión

### Network (revisado contra Go source cdproto)

- **33 comandos CDP** en Go source, **34 métodos** en cdpwave (1 extra: `set_user_agent_override`).
- **0 bugs** encontrados. Todos los parámetros requeridos, opcionales y bools no-omitempty coinciden con el Go source.
- `set_blocked_urls` soporta tanto `urls` (legacy) como `url_patterns` (`BlockPattern[]` actual) — correcto.
- `set_extra_request_headers` envía `Network.setExtraHTTPHeaders` — naming mismatch intencional.
- `set_user_agent_override` envía `Network.setUserAgentOverride` — existe en CDP spec pero no en Go source (probablemente deprecado).
- `enable` incluye `enableDurableMessages` (deprecated en favor de `configure_durable_messages`) — correctamente documentado.
- `get_request_post_data` existe en ambos dominios Network y Fetch (comandos CDP diferentes: `Network.getRequestPostData` vs `Fetch.getRequestPostData`).

### Target (revisado contra Go source cdproto)

- **18 comandos CDP** en Go source, **19 métodos** en cdpwave (1 extra: `send_message_to_target`, deprecated).
- **9 bugs encontrados y corregidos**:
  - `create_target`: `new_window`/`background` ahora siempre se envían (bools sin omitempty). Añadidos `left`, `top`, `window_state`, `enable_begin_frame_control`, `for_tab`, `hidden`, `focus`.
  - `get_targets`: añadido parámetro `filter`.
  - `set_auto_attach`: `wait_for_debugger_on_start` ahora siempre se envía (bool sin omitempty). Añadido `filter`.
  - `set_discover_targets`: añadido parámetro `filter`.
  - `expose_dev_tools_protocol`: añadido `inherit_permissions` (bool sin omitempty). `binding_name` ahora opcional (omitempty en Go).
  - `create_browser_context`: añadidos `proxy_server`, `proxy_bypass_list`, `origins_with_universal_network_access`.
  - `auto_attach_related`: removido parámetro espurio `auto_attach` (no existe en CDP). Añadido `filter`.
  - `get_dev_tools_target`: añadido parámetro requerido `target_id`.
  - `open_dev_tools`: añadidos `target_id` (requerido) y `panel_id` (opcional).
- `send_message_to_target` es deprecated en CDP pero se mantiene por compatibilidad.

### Emulation (revisado contra Go source cdproto)

- **47 comandos CDP** en Go source/CDP spec, **53 métodos** en cdpwave (6 extra: aliases de conveniencia — `clear_emulated_media`, `set_emulated_media_feature`, `clear_default_background_color_override`, `clear_auto_dark_mode_override`, `clear_emulated_vision_deficiency`, `clear_timezone_override`).
- **53 bugs encontrados y corregidos**.
- **163 tests unitarios** + **69 tests de integración** en navegador real (casos edge: omitempty/omitzero, screen management headless, sensores con metadata, pressure API, device posture, display features, virtual time, safe area insets, geolocation completa, UA metadata).
  - `set_device_metrics_override`: añadidos `scale`, `dont_set_visible_size` (bool siempre enviado), `scrollbar_type`, `screen_orientation_lock_emulation` (bool siempre enviado). Removidos parámetros espurios `display_feature` y `device_posture` (no existen en Go source `SetDeviceMetricsOverrideParams`; usar `set_display_features_override` y `set_device_posture_override` respectivamente). Removido parámetro espurio `user_agent` (no existe en Go source ni CDP spec).
  - `set_idle_override`: `is_screen_active` renombrado a `is_screen_unlocked` (coincide con Go source `IsScreenUnlocked`).
  - `set_data_saver_override`: `enabled` renombrado a `dataSaverEnabled` (coincide con Go source `DataSaverEnabled`).
  - `set_small_viewport_height_difference_override`: cambiado de `enabled: bool` a `difference: int` (coincide con Go source `Difference int64`).
  - `set_emulated_os_text_scale`: `fontScale` renombrado a `scale` (coincide con Go source `Scale float64`). Ahora `scale` es opcional con `omitempty,omitzero` (solo se envía si no es cero).
  - `set_pressure_state_override`: removido `own_contribution` (no existe en Go source `SetPressureStateOverrideParams`).
  - `set_device_posture_override`: ahora envía `{"posture": {"type": posture}}` (struct anidado, coincide con Go source `DevicePosture` con campo `Type`).
  - `set_display_features_override`: `displayFeatures` renombrado a `features` (coincide con Go source `Features`).
  - `add_screen`: firma completamente reescrita — `left`/`top` ahora requeridos, `device_scale_factor`/`touch`/`external` reemplazados por `device_pixel_ratio`/`is_internal` (bool siempre enviado). Añadidos `work_area_insets`, `rotation`, `color_depth`.
  - `update_screen`: mismos cambios de campos que `add_screen`.
  - `set_geolocation_override`: todos los parámetros ahora opcionales (omitempty en Go). Añadidos `altitude`, `altitude_accuracy`, `heading`, `speed`. Ya no se envía `accuracy` por defecto.
  - `set_emit_touch_events_for_mouse`: `configuration` ahora opcional (omitempty en Go). Ya no se envía `"mobile"` por defecto.
  - `set_virtual_time_policy`: `budget` cambiado de `int` a `float` (coincide con Go source `Budget float64`).
  - `set_auto_dark_mode_override`: `enabled` ahora siempre se envía (bool sin omitempty en Go). Cambiado de `bool | None` a `bool = False`.
  - `set_emulated_media`: `media` ahora solo se envía si no está vacío (omitempty en Go). `clear_emulated_media` ahora envía params vacíos en vez de `{"media": ""}`.
  - `get_overridden_sensor_information`: docstring corregido de `requestedFrequencyHz` a `requestedSamplingFrequency` (coincide con Go source `RequestedSamplingFrequency`).
  - `set_locale_override`: `locale` ahora solo se envía si no está vacío (omitempty en Go). Cambiado de requerido a opcional con default `""`.
  - `set_focus_emulation_enabled`: removida docstring de deprecación incorrecta (comando activo en Go source).
  - `set_emulated_vision_deficiency`: removida docstring de deprecación incorrecta (comando activo en Go source).
  - `set_disabled_sensors`: método espurio removido (no existe en CDP spec ni Go source).
  - `clear_sensor_override_readings`: método espurio removido (no existe en CDP spec ni Go source).
  - `set_javascript_disabled`: método espurio removido (no existe en CDP spec ni Go source; usar `set_script_execution_disabled`).
  - `set_sensor_override_enabled`: añadido parámetro opcional `metadata` faltante (presente en Go source `Metadata *SensorMetadata` con `omitempty` y CDP spec `SensorMetadata`).
  - `set_scroll_position`: método espurio removido (no existe en CDP spec ni Go source; `Emulation.setScrollPositionOverride` no es un comando CDP válido).
  - `set_device_metrics_override`: `scale`, `screen_width`, `screen_height`, `position_x`, `position_y` ahora se omiten cuando son cero (Go source usa `omitempty,omitzero`). Antes usaban `is not None` y se enviaban como `0`/`0.0`.
  - `set_virtual_time_policy`: `budget=0.0` y `max_virtual_time_task_starvation_count=0` ahora se omiten (Go source usa `omitempty,omitzero`).
  - `set_touch_emulation_enabled`: `max_touch_points=0` ahora se omite (Go source usa `omitempty,omitzero`).
  - `set_geolocation_override`: todos los params float ahora se omiten cuando son `0.0` (Go source usa `omitempty,omitzero`). Antes usaban `is not None`.
  - `set_user_agent_override`: `accept_language=""` y `platform=""` ahora se omiten (Go source usa `omitempty,omitzero`).
  - `set_emit_touch_events_for_mouse`: `configuration=""` ahora se omite (Go source usa `omitempty,omitzero`).
  - `set_idle_override`/`clear_idle_override`: removidas docstrings de deprecación incorrectas (comandos activos en Go source y CDP spec).
  - `add_screen`: `device_pixel_ratio=0`, `rotation=0`, `color_depth=0`, `label=""` ahora se omiten (Go source usa `omitempty,omitzero`).
  - `update_screen`: `left=0`, `top=0`, `width=0`, `height=0`, `device_pixel_ratio=0`, `rotation=0`, `color_depth=0`, `label=""` ahora se omiten (Go source usa `omitempty,omitzero`).
  - `set_default_background_color_override`: alpha cambiado de `int` (0-255) a `float` (0-1) (coincide con CDP spec RGBA `a: number 0-1`). Default cambiado de `255` a `1.0`.
  - `set_device_posture_override`: corregido campo interno del struct `DevicePosture` de `"posture"` a `"type"` (coincide con Go source `Type DevicePostureType json:"type"`).
  - `set_sensor_override_readings`/`set_sensor_override_enabled`: docstrings corregidos — `"linear-accelerometer"` → `"linear-acceleration"`, añadidos `"ambient-light"`, `"gravity"`, `"magnetometer"` (coincide con Go source `SensorType` values).
  - `set_pressure_source_override_enabled`/`set_pressure_state_override`: docstrings corregidos — removido `"gpu"` de pressure sources (Go source `PressureSource` solo tiene `"cpu"`).
  - `set_disabled_image_types`: docstring corregido — `"jpg"` → `"jxl"` (coincide con Go source `DisabledImageType` values: `avif`, `jxl`, `webp`).
  - `set_display_features_override`: docstring corregido — removido `maskThickness` (no existe en Go source `DisplayFeature` struct; solo `orientation`, `offset`, `maskLength`).
  - `set_safe_area_insets_override`: añadidos parámetros `top_max`, `left_max`, `bottom_max`, `right_max` (faltantes, existen en Go source `SafeAreaInsets` struct como `TopMax`, `LeftMax`, `BottomMax`, `RightMax`). Cambiados defaults de `0` a `None` con `omitempty,omitzero` — antes siempre enviaba los 4 campos básicos incluso si eran `0`, ahora solo se envían si el usuario los pasa explícitamente.
  - `set_virtual_time_policy`: `initial_virtual_time=0.0` ahora se omite (Go source usa `omitempty,omitzero`). Antes usaba `is not None` y se enviaba `0.0`.
  - `update_screen`: añadido docstring de return `Dict with screenInfo` (faltante, Go source tiene `UpdateScreenReturns { ScreenInfo *ScreenInfo }`).
  - `set_visible_size`: docstring corregido — "CSS pixels" → "DIP (Device Independent Pixels)" (coincide con CDP spec). Añadida nota de deprecación (deprecated en CDP spec, no en Go source).
  - `can_emulate`/`set_navigator_overrides`: añadidas notas de deprecación (deprecated en CDP spec, no en Go source).
  - `set_emulated_media`: docstring corregido — "Emulate CSS media features" → "Emulate CSS media type or media features" (coincide con CDP spec).
  - `set_emulated_media`: `features=[]` ahora se omite (Go source usa `omitempty,omitzero` para `Features []MediaFeature`). Antes usaba `is not None` y enviaba lista vacía.
  - `set_device_metrics_override`: `scrollbar_type=""` ahora se omite (Go source usa `omitempty,omitzero` para `ScrollbarType`). Antes usaba `is not None` y enviaba string vacío.
  - `add_screen`/`update_screen`/`set_primary_screen`/`get_screen_infos`: tests de integración corregidos — respuesta `ScreenInfo` usa campo `id` (no `screenId`) (coincide con Go source `ScreenInfo.ID ScreenID json:"id"`).
  - `set_sensor_override_readings`: docstring corregido — ejemplo `{"x": 0, "y": 0, "z": 0}` era incorrecto. `SensorReading` es un struct wrapper con campos `single`, `xyz`, `quaternion`. Ejemplos correctos: `{"xyz": {"x": 1.0, "y": 0.0, "z": 9.8}}` para accelerometer, `{"single": {"value": 100.0}}` para ambient-light, `{"quaternion": {"x": 0, "y": 0, "z": 0, "w": 1}}` para orientation.
  - `set_safe_area_insets_override`: cambiado `if top is not None:` a `if top:` para todos los campos `SafeAreaInsets` (Go source usa `omitempty,omitzero` para ints). Antes enviaba `top=0` explícitamente, ahora se omite (coincide con Go behavior: 0 = undefined).

### Fetch (revisado contra Go source cdproto)

- **9 comandos CDP** en Go source, **11 métodos** en cdpwave (2 extra: `get_request_post_data` también en Network, `take_response_bodyAsStream` alias).
- **3 bugs encontrados y corregidos**:
  - `continue_request`: `interceptResponse` ahora siempre se envía (bool sin omitempty en Go source).
  - `continue_response`: añadido parámetro `response_phrase` (faltante, existe en Go source `ResponsePhrase`).
  - `fulfill_request`: añadido parámetro `response_phrase` (faltante, existe en Go source `ResponsePhrase`).

### Storage (revisado contra Go source cdproto)

- **33 comandos CDP** en Go source, **34 métodos** en cdpwave (1 extra: `get_storage_key_for_frame`, deprecated en CDP spec pero no en Go source).
- **15 bugs encontrados y corregidos en primera revisión**:
  - `get_cookies`: `browser_context_id` ahora usa truthiness en vez de `is not None` (Go source usa `omitempty` para `BrowserContextID`).
  - `set_cookies`: `browser_context_id` ahora usa truthiness en vez de `is not None` (mismo motivo).
  - `clear_cookies`: `browser_context_id` ahora usa truthiness en vez de `is not None` (mismo motivo).
  - `get_usage_and_quota`: docstring corregido para incluir `usageBreakdown` en el return documentado (Go source `GetUsageAndQuotaReturns` incluye `UsageBreakdown []*UsageForType`).
  - `clear_trust_tokens`: `issuer_origin` cambiado de opcional a requerido (Go source `IssuerOrigin string` sin `omitempty`). Añadido `didDeleteTokens` al docstring de return (Go source `DidDeleteTokens bool`).
  - `set_storage_bucket_info`: método espurio removido (no existe en CDP spec ni Go source).
  - `get_storage_key_for_frame`: añadida nota de deprecación (deprecated en CDP spec, usar `get_storage_key` en su lugar).
  - `get_storage_key`: `frame_id` cambiado de requerido a opcional (Go source `FrameID cdp.FrameID json:"frameId,omitempty"`). Usa truthiness para omisión.
  - `override_quota_for_origin`: `quota_size` cambiado de `int` a `float` (Go source `QuotaSize float64`). Usa truthiness para omisión (Go source `omitempty,omitzero`).
  - `get_shared_storage_metadata`: docstring completado para incluir `remainingBudget` y `bytesUsed` en el return (Go source `GetSharedStorageMetadataReturns` tiene `Metadata *SharedStorageMetadata` con esos campos).
  - `reset_shared_storage_budget`: removido parámetro espurio `budget` (no existe en Go source `ResetSharedStorageBudgetParams`, solo tiene `owner`).
  - `delete_storage_bucket`: corregido para enviar estructura anidada `{"bucket": {"storageKey": ..., "name": ...}}` (coincide con Go source `DeleteStorageBucketParams.Bucket *StorageBucket`).
  - `run_bounce_tracking_mitigations`: añadido `deletedSites` al docstring de return (Go source `RunBounceTrackingMitigationsReturns` tiene `DeletedSites []string`).
  - `set_protected_audience_k_anonymity`: corregidos parámetros a `owner`, `name`, `hashes: list[str]` (coincide con Go source `SetProtectedAudienceKAnonymityParams` con `Owner string`, `Name string`, `Hashes []string`).
  - Class docstring: añadidos todos los eventos del dominio Storage (`cacheStorageContentUpdated`, `cacheStorageListUpdated`, `indexedDBContentUpdated`, `indexedDBListUpdated`, `interestGroupAccessed`, `interestGroupAuctionEventOccurred`, `interestGroupAuctionNetworkRequestCreated`, `sharedStorageAccessed`, `sharedStorageWorkletOperationExecutionFinished`, `storageBucketCreatedOrUpdated`, `storageBucketDeleted`).
- **Tests unitarios**: **58 tests** en total (`test_coverage_boost.py` + `test_tier3c_domains.py`) con FakeSender — cubriendo optionality de `browser_context_id`, `frame_id`, `quota_size`, estructura anidada de `delete_storage_bucket`, `hashes` en `set_protected_audience_k_anonymity`, deprecación de `get_storage_key_for_frame`, bools en `False` para todos los tracking methods, edge cases de strings vacíos, y verificación de return values (`didDeleteTokens`, `deletedSites`, `usageBreakdown`).
- **Tests de integración**: **29 tests** en `tests/integration/test_storage.py` con cobertura de navegador real para todos los comandos principales, incluyendo `clear_trust_tokens`, `get_interest_group_details`, `set_shared_storage_entry` con `ignore_if_present=True`, y assertions de tipo (`isinstance`) en return values.
- **Segunda revisión (robustez y cobertura edge)** — 4 issues adicionales encontrados y corregidos:
  - `clear_data_for_origin`/`clear_data_for_storage_key`: docstring corregido — removido `session_storage` de ejemplos (no existe en Go source `StorageType` enum; los valores válidos son `cookies`, `file_systems`, `indexeddb`, `local_storage`, `shader_cache`, `websql`, `service_workers`, `cache_storage`, `interest_groups`, `shared_storage`, `storage_buckets`, `all`, `other`).
  - `test_tier3c_domains.py`: `test_clear_trust_tokens_all` corregido — ahora llama con `issuer_origin` requerido. `test_set_storage_bucket_info` removido (método espurio eliminado en primera revisión).
  - `test_coverage_boost.py`: `test_run_bounce_tracking_mitigations` duplicado renombrado a `test_run_bounce_tracking_mitigations_return` (verifica return value `deletedSites`).
  - Añadidos 16 tests unitarios edge: `track/untrack_indexed_db_for_origin`, `track/untrack_cache_storage_for_origin`, bools `False` para 4 tracking methods, `set_shared_storage_entry` con `ignoreIfPresent=False` default, `get_storage_key()` omitido, `delete_storage_bucket()` omitido, return values para `clear_trust_tokens` y `get_usage_and_quota`.
- **Tercera revisión (precisión de docstrings y coverage de integración)** — 3 issues adicionales:
  - Docstrings mejorados: "a shared storage" → "an origin's shared storage" en 5 métodos. Añadidos eventos emitidos a docstrings de `track_indexed_db_for_origin` (`indexedDBContentUpdated`), `set_interest_group_tracking` (`interestGroupAccessed`), `set_interest_group_auction_tracking` (`interestGroupAuctionEventOccurred`, `interestGroupAuctionNetworkRequestCreated`), `set_shared_storage_tracking` (`sharedStorageAccessed`).
  - Conteo Go source corregido: 33 comandos (no 34; `getStorageKeyForFrame` no está en Go source, solo en CDP spec como deprecated).
  - Integration tests ampliados: añadidos `test_clear_trust_tokens`, `test_get_interest_group_details`, `test_set_shared_storage_entry_default` (sin `ignore_if_present`). Assertions reforzadas con `isinstance` en `get_usage_and_quota`, `get_trust_tokens`, `get_storage_key`, `clear_trust_tokens`, `run_bounce_tracking_mitigations`, `get_related_website_sets`. Total: 29 integration tests.
- **Cuarta revisión (verificación Go source completa + E2E tests)** — 0 bugs nuevos, E2E tests añadidos:
  - Verificación línea por línea de los 33 comandos del Go source completada. Todos los parámetros, tipos, optionality (`omitempty`/`omitzero`), y return values coinciden exactamente. Sin bugs nuevos.
  - Creados **21 E2E tests** en `tests/e2e/test_storage_e2e.py` con flujos completos contra navegador real: roundtrip de cookies (set/get/clear/verify), quota override + reset con verificación de `overrideActive`, `clear_data_for_origin` con verificación de side effect, `get_storage_key` con y sin frame_id, tracking toggles para todos los tracking methods, `clear_trust_tokens` con verificación de `didDeleteTokens` bool, `run_bounce_tracking_mitigations` con verificación de `deletedSites` list, `get_related_website_sets` con verificación de `sets` list, `clear_data_for_storage_key` usando storage key real del target, track/untrack for storage key usando storage key real, `get_storage_key_for_frame` deprecated, y cookie persistence con múltiples cookies.
  - **Total: 58 unit tests + 29 integration tests + 21 E2E tests = 108 tests** para el dominio Storage.

### DOMStorage (revisado contra Go source cdproto)

- **6 comandos CDP** en Go source, **6 métodos** en cdpwave (1 extra: `clear_dom_storage_items` alias de `clear`).
- **12 bugs encontrados y corregidos**:
  - `enable`: método faltante añadido (Go source `CommandEnable = "DOMStorage.enable"`). Params `None` (coincide con Go source `cdp.Execute(ctx, CommandEnable, nil, nil)`).
  - `disable`: método faltante añadido (Go source `CommandDisable = "DOMStorage.disable"`). Params `None` (mismo motivo).
  - `clear`: método renombrado de `clear_dom_storage_items` a `clear` (coincide con Go source `CommandClear = "DOMStorage.clear"`). `clear_dom_storage_items` mantenido como alias.
  - Class docstring: removida afirmación incorrecta "does not require enable/disable calls — commands work directly". Ahora documenta correctamente que `enable`/`disable` controlan el envío de eventos.
  - Class docstring: añadidos los 4 eventos del dominio (`domStorageItemAdded`, `domStorageItemRemoved`, `domStorageItemsCleared`, `domStorageItemUpdated`) con sus parámetros (verificado contra Go source `events.go`: `domStorageItemAdded` tiene `key`+`newValue`, `domStorageItemRemoved` tiene `key`, `domStorageItemUpdated` tiene `key`+`oldValue`+`newValue`, `domStorageItemsCleared` solo `storageId`).
  - Docstrings de `storage_id` en todos los métodos: añadido campo `storageKey` (str, optional) que faltaba (Go source `StorageID` tiene `StorageKey SerializedStorageKey` con `omitempty,omitzero`). Documentado `isLocalStorage` como bool siempre enviado (Go source sin `omitempty`).
  - `get_dom_storage_items`: return docstring mejorado — ahora documenta `entries` como `list[list[str]]` de pares `[key, value]` (coincide con Go source `GetDOMStorageItemsReturns.Entries []Item` donde `Item []string`).
  - `enable`/`disable`: params corregidos de `{}` a `None` (coincide con convención de todos los demás dominios en cdpwave y Go source `nil` params).
  - Module docstring: "inspection" → "access" (Go source: "Query and modify DOM storage").
  - `enable` docstring: añadido "now" — "storage events will now be delivered" (Go source exacto).
  - `disable` docstring: añadido "to the client" — "prevents storage events from being sent to the client" (Go source exacto).
  - N802 ruff violation: `test_storage_id_isLocalStorage_false` renombrado a `test_storage_id_is_local_storage_false` (PEP 8 snake_case).
- **Tests unitarios**: **13 tests** en `test_coverage_boost.py` con FakeSender — cubriendo `enable`/`disable` (params `None`), `get_dom_storage_items` (con y sin `storageKey`, `isLocalStorage=False`), `set_dom_storage_item` (valor vacío), `remove_dom_storage_item`, `clear`, `clear_dom_storage_items` alias, return values de `entries`.
- **Tests de integración**: **14 tests** en `tests/integration/test_dom_storage.py` con navegador real — enable/disable, get vacío, set/get localStorage y sessionStorage, remove, clear, alias, aislamiento local/session, valor vacío, overwrite, **4 event tests** (domStorageItemAdded con `key`+`newValue`, domStorageItemRemoved con `key`, domStorageItemUpdated con `key`+`oldValue`+`newValue`, domStorageItemsCleared).
- **E2E tests**: **18 tests** en `tests/e2e/test_dom_storage_e2e.py` con flujos completos contra navegador real — set/get/remove/clear localStorage y sessionStorage con verificación de side effects via `Runtime.evaluate`, aislamiento local/session, overwrite, valor vacío, alias, múltiples items roundtrip, remove non-existent, clear already-empty, **4 event E2E tests** con verificación de side effects via `Runtime.evaluate` (event params verificados contra Go source `events.go`).
- **Total: 13 unit tests + 14 integration tests + 18 E2E tests = 45 tests** para el dominio DOMStorage.

### Browser (revisado contra Go source cdproto)

- **20 comandos CDP** en Go source, **21 métodos** en cdpwave (1 extra: `get_command_line` alias de `get_browser_command_line`). `grant_permissions` es un comando CDP deprecado mantenido por compatibilidad, no un método extra.
- **9 métodos faltantes añadidos**:
  - `set_permission`: Set permission settings for given embedding and embedded origins. Params: `permission` (PermissionDescriptor dict), `setting` (str), optional `origin`, `embedded_origin`, `browser_context_id`.
  - `cancel_download`: Cancel a download if in progress. Params: `guid` (str), optional `browser_context_id`.
  - `crash`: Crashes browser on the main thread. No params. Experimental/destructive.
  - `crash_gpu_process`: Crashes GPU process. No params. Experimental/destructive.
  - `set_contents_size`: Set size of browser contents. Params: `window_id` (int), optional `width`, `height`.
  - `set_dock_tile`: Set dock tile details. Params: optional `badge_label`, `image`.
  - `execute_browser_command`: Invoke custom browser commands. Params: `command_id` (str).
  - `add_privacy_sandbox_enrollment_override`: Allow site to use privacy sandbox features. Params: `url` (str).
  - `add_privacy_sandbox_coordinator_key_config`: Configure encryption keys for privacy sandbox API. Params: `api`, `coordinator_origin`, `key_config`, optional `browser_context_id`.
- **5 métodos espurios removidos** (no existen en Go source ni CDP spec):
  - `reset_histograms`: removido (no existe en Go source ni CDP spec).
  - `get_cpu_profile`: removido (no existe en Go source ni CDP spec).
  - `get_heap_profile`: removido (no existe en Go source ni CDP spec).
  - `get_bounds`: removido (no existe en Go source ni CDP spec, era alias sin `window_id` de `get_window_bounds`).
  - `set_bounds`: removido (no existe en Go source ni CDP spec, era alias sin `window_id` de `set_window_bounds`).
- **6 bugs encontrados y corregidos**:
  - `reset_permissions`: removido parámetro `origin` (Go source `ResetPermissionsParams` solo tiene `BrowserContextID`). Antes enviaba `{"origin": ...}` que no existe en CDP.
  - `set_download_behavior`: `events_enabled` cambiado de `bool | None = None` (condicional) a `bool = False` (siempre enviado). Go source `EventsEnabled bool` sin `omitempty` — siempre se envía, default `false`.
  - `get_histograms`: añadidos parámetros `query` (str, optional) y `delta` (bool, siempre enviado, default `false`). Go source `GetHistogramsParams` tiene `Query string` (omitempty) y `Delta bool` (sin omitempty). Antes no tenía parámetros.
  - `get_histogram`: `delta` cambiado de `bool | None = None` (condicional) a `bool = False` (siempre enviado). Go source `Delta bool` sin `omitempty`.
  - `get_window_for_target`: removido parámetro `window_id` (Go source `GetWindowForTargetParams` solo tiene `TargetID`). Antes aceptaba `window_id` que no existe en CDP.
  - `get_browser_command_line`/`get_command_line`: docstring corregido — return es `arguments` (list of command-line parameters), no `commandLine` (string). Go source `GetBrowserCommandLineReturns.Arguments []string`.
- **Eventos documentados en class docstring**:
  - `Browser.downloadWillBegin`: Params `frameId` (str), `guid` (str), `url` (str), `suggestedFilename` (str).
  - `Browser.downloadProgress`: Params `guid` (str), `totalBytes` (float), `receivedBytes` (float), `state` (str: `"inProgress"`, `"completed"`, `"canceled"`), `filePath` (str, optional).
- **Tests unitarios**: **30+ tests** en `test_browser_domain.py` y `test_coverage_gaps.py` con FakeSender — cubriendo todos los métodos nuevos, fixes de params, defaults de booleanos, y casos edge.
- **Tests de integración**: **8 tests** en `tests/integration/test_browser_domain.py` con navegador real — get_version, get_window_for_target, get/set_window_bounds, grant/reset_permissions, set_download_behavior, get_histograms, get_histogram, set_permission/reset.
- **E2E tests**: **12 tests** en `tests/e2e/test_browser_e2e.py` con flujos completos — get_version, get_window_for_target, get/set_window_bounds, set_download_behavior (con y sin events), get_histograms (con y sin query), get_histogram, set_permission/reset, grant_permissions deprecated, close.
- **Total: 30+ unit tests + 8 integration tests + 12 E2E tests = 50+ tests** para el dominio Browser.

### Log (revisado contra Go source cdproto)

- **5 comandos CDP** en Go source, **5 métodos** en cdpwave (0 extra, 0 faltantes).
- **0 bugs** encontrados. Todos los parámetros, tipos y optionality coinciden exactamente con el Go source.
- **Cambios de precisión (docstrings y orden)**:
  - Orden de métodos reordenado para coincidir con Go source: `clear` → `disable` → `enable` → `start_violations_report` → `stop_violations_report` (antes era `enable` → `disable` → `clear` → `start` → `stop`).
  - `clear` docstring: "Clear all accumulated log entries" → "Clears the log" (coincide con Go source `Clear clears the log`).
  - `disable` docstring: "Disable Log domain events" → "Disables log domain, prevents further log entries from being reported to the client" (coincide con Go source exacto).
  - `enable` docstring: "Enable Log domain events" → "Enables log domain, sends the entries collected so far to the client by means of the entryAdded notification" (coincide con Go source exacto).
  - `start_violations_report` docstring: "Start reporting violations" → "Start violation reporting" (coincide con Go source `StartViolationsReport start violation reporting`). Añadidos todos los 7 violation types (`longTask`, `longLayout`, `blockedEvent`, `blockedParser`, `discouragedAPIUse`, `handler`, `recurringHandler`) y tipo `threshold` (float) al docstring.
  - `stop_violations_report` docstring: "Stop reporting violations" → "Stop violation reporting" (coincide con Go source `StopViolationsReport stop violation reporting`). Removido texto extra "Stops the violation reporting that was started by start_violations_report".
  - Module docstring: "Log domain: browser log entries and violation reporting" → "Log domain: provides access to log entries" (coincide con Go source package doc `Provides access to log entries`).
  - Module docstring: añadidos todos los campos de LogEntry con tipos y optionality (verificado contra Go source `types.go`: `source` sin omitempty, `level` sin omitempty, `text` sin omitempty, `category` con `omitempty,omitzero`, `timestamp` sin omitempty, `url`/`lineNumber`/`stackTrace`/`networkRequestId`/`workerId`/`args` con `omitempty,omitzero`).
  - Class docstring: añadido evento `Log.entryAdded` con descripción y parámetros (verificado contra Go source `events.go`: `EventEntryAdded` tiene `Entry *Entry json:"entry"`).
- **Tipos verificados contra Go source `types.go`**:
  - `ViolationSetting`: `Name Violation` (str, sin omitempty) + `Threshold float64` (sin omitempty) — cdpwave envía `{"name": ..., "threshold": ...}` correctamente.
  - `Entry`: todos los campos documentados con tipos correctos (`Source`, `Level`, `Text`, `Category`, `Timestamp`, `URL`, `LineNumber`, `StackTrace`, `NetworkRequestID`, `WorkerID`, `Args`).
  - `Source` values: `xml`, `javascript`, `network`, `storage`, `appcache`, `rendering`, `security`, `deprecation`, `worker`, `violation`, `intervention`, `recommendation`, `other` (13 valores).
  - `Level` values: `verbose`, `info`, `warning`, `error` (4 valores).
  - `EntryCategory` values: `cors` (1 valor).
  - `Violation` values: `longTask`, `longLayout`, `blockedEvent`, `blockedParser`, `discouragedAPIUse`, `handler`, `recurringHandler` (7 valores).
- **Eventos del dominio Log** (verificado contra Go source `events.go`):
  - `Log.entryAdded`: Issued when new message was logged. Params: `entry` (LogEntry dict).
- **Tests unitarios**: **12 tests** en `test_new_domains.py` con FakeSender — cubriendo los 5 métodos, `start_violations_report` con config single/multiple (7 violation types)/empty list/float threshold, return values de los 4 métodos sin params, verificación de `params is None` para métodos sin parámetros.
- **Tests de integración**: **4 tests** en `tests/integration/test_log_console_target.py` con navegador real — enable/disable, entryAdded event, clear, start/stop violations report.
- **Total: 12 unit tests + 4 integration tests = 16 tests** para el dominio Log.

### Log — Segunda revisión (edge cases, E2E, bug audit)

- **0 bugs nuevos** encontrados. Verificación línea por línea completada nuevamente.
- **Tests unitarios ampliados**: **12 → 24 tests** en `test_new_domains.py` con FakeSender:
  - 7 tests individuales para cada violation type (`longTask`, `longLayout`, `blockedEvent`, `blockedParser`, `discouragedAPIUse`, `handler`, `recurringHandler`).
  - `threshold=0` (edge case — se envía correctamente como `0`).
  - `threshold=-1` (negative — se envía sin validación, correcto: Go source no valida).
  - `config` con extra keys (se preservan sin filtrar, correcto: Go source usa `json.Marshal` directo).
  - `test_all_methods_call_sequence` — verifica orden de llamadas y conteo.
  - `test_start_violations_report_returns_response` — verifica que el return value se propaga.
- **E2E tests creados**: **20 tests** en `tests/e2e/test_log_e2e.py` con navegador real:
  - `test_enable_disable` / `test_enable_returns_empty` / `test_disable_returns_empty` — enable/disable roundtrip + return values.
  - `test_clear` / `test_clear_without_enable` — clear con y sin enable previo.
  - `test_entry_added_deprecation` — captura evento `Log.entryAdded` via XMLHttpRequest deprecation.
  - `test_entry_added_has_correct_types` — verifica tipos de campos (`source: str`, `level: str`, `text: str`, `timestamp: int|float`).
  - `test_entry_added_source_values` — verifica `source` contra los 13 valores válidos del Go source.
  - `test_entry_added_level_values` — verifica `level` contra los 4 valores válidos (`verbose`, `info`, `warning`, `error`).
  - `test_start_violations_report_single` / `test_start_violations_report_all_types` — 1 y 7 violation types.
  - `test_start_violations_report_float_threshold` — threshold float.
  - `test_stop_violations_report_without_start` — stop sin start previo (no debe errorar).
  - `test_start_violations_report_returns_empty` / `test_stop_violations_report_returns_empty` — return values.
  - `test_full_lifecycle` — clear → enable → start → stop → clear → disable.
  - `test_repeated_enable_disable` — 3 ciclos enable/disable.
  - `test_violation_report_restart` — 2 ciclos start/stop.
  - `test_clear_after_entries` — clear después de generar entries.
  - `test_entry_added_optional_fields` — verifica tipos de campos opcionales (`url`, `lineNumber`, `stackTrace`, `networkRequestId`, `workerId`, `args`, `category`).
- **Total: 24 unit tests + 4 integration tests + 20 E2E tests = 48 tests** para el dominio Log.

### Accessibility (revisado contra Go source cdproto)

- **8 comandos CDP** en Go source, **8 métodos** en cdpwave (0 extra, 0 faltantes).
- **1 bug encontrado y corregido**:
  - Todos los parámetros con `omitempty,omitzero` en Go source usaban `is not None` (siempre enviados incluso con valores cero). Cambiados a truthiness checks (`if value:`) para coincidir con Go source behavior: `0` y `""` se omiten. Afecta a `depth` en `get_full_ax_tree`, `frame_id` en `get_child_ax_nodes`/`get_full_ax_tree`/`get_root_ax_node`, `node_id`/`backend_node_id`/`object_id` en `get_ax_node_and_ancestors`/`get_partial_ax_tree`/`query_ax_tree`, `accessible_name`/`role` en `query_ax_tree`.
- **Cambios de precisión (docstrings, orden y eventos)**:
  - Orden de métodos reordenado para coincidir con Go source (orden de aparición en archivo): `disable` → `enable` → `get_partial_ax_tree` → `get_full_ax_tree` → `get_root_ax_node` → `get_ax_node_and_ancestors` → `get_child_ax_nodes` → `query_ax_tree`.
  - `disable` docstring: "Disable the Accessibility domain" → "Disables the accessibility domain" (coincide con Go source `Disable disables the accessibility domain`).
  - `enable` docstring: "Enable the Accessibility domain" → "Enables the accessibility domain which causes AXNodeIds to remain consistent between method calls. This turns on accessibility for the page, which can impact performance until accessibility is disabled" (coincide con Go source exacto).
  - `get_partial_ax_tree` docstring: "Get a partial accessibility tree for a node" → "Fetches the accessibility node and partial accessibility tree for this DOM node, if it exists" (coincide con Go source exacto).
  - `get_full_ax_tree` docstring: "Get the full accessibility tree for the current page" → "Fetches the entire accessibility tree for the root Document" (coincide con Go source exacto).
  - `get_root_ax_node` docstring: "Get the root AX node of the accessibility tree" → "Fetches the root node. Requires enable() to have been called previously" (coincide con Go source exacto).
  - `get_child_ax_nodes` docstring: "Get child AX nodes of a given node" → "Fetches a particular accessibility node by AXNodeId. Requires enable() to have been called previously" (coincide con Go source exacto).
  - `get_ax_node_and_ancestors` docstring: "Fetch a node and all ancestors up to and including the root" → "Fetches a node and all ancestors up to and including the root. Requires enable() to have been called previously" (coincide con Go source exacto).
  - `query_ax_tree` docstring: "Query the AX tree for nodes matching a query" → "Query a DOM node's accessibility subtree for accessible name and role. This command computes the name and role for all nodes in the subtree, including those that are ignored for accessibility, and returns those that match the specified name and role. If no DOM node is specified, or the DOM node does not exist, the command returns an error. If neither accessibleName or role is specified, it returns all the accessibility nodes in the subtree" (coincide con Go source exacto).
  - Descripciones de parámetros actualizadas para coincidir con Go source exacto (e.g. "Identifier of the node to get the partial accessibility tree for" en vez de "DOM node ID to query from").
  - Module docstring: "Accessibility domain: AX tree inspection for accessibility testing" → "Accessibility domain: access to the accessibility tree" + documentación de eventos.
  - Class docstring: añadidos los 2 eventos del dominio Accessibility (`loadComplete`, `nodesUpdated`) con sus parámetros (verificado contra Go source `events.go`: `EventLoadComplete` tiene `root *Node`, `EventNodesUpdated` tiene `nodes []*Node`).
- **Tipos verificados contra Go source `types.go`**:
  - `NodeID` es `string` (Go source `type NodeID string`) — `get_child_ax_nodes` usa `id: str` correctamente (no `nodeId: int`).
  - `cdp.NodeID` es `int` (Go source) — `get_partial_ax_tree`/`get_ax_node_and_ancestors`/`query_ax_tree` usan `node_id: int` correctamente.
  - `cdp.BackendNodeID` es `int` (Go source) — `backend_node_id: int` correctamente.
  - `runtime.RemoteObjectID` es `string` (Go source) — `object_id: str` correctamente.
  - `cdp.FrameID` es `string` (Go source) — `frame_id: str` correctamente.
  - `fetchRelatives` es `bool` sin `omitempty` (Go source) — siempre se envía, default `True`. Correcto.
  - `depth` es `int64` con `omitempty,omitzero` (Go source) — opcional, se omite si es `0`. Correcto.
  - `id` en `getChildAXNodes` es `NodeID` (string) sin `omitempty` (Go source) — requerido. Correcto.
  - `accessibleName` y `role` en `queryAXTree` son `string` con `omitempty,omitzero` (Go source) — opcionales, se omiten si están vacíos. Correcto.
- **Eventos del dominio Accessibility** (verificado contra Go source `events.go`):
  - `Accessibility.loadComplete`: Mirrors the load complete event sent by the browser to assistive technology when the web page has finished loading. Params: `root` (AXNode) — new document root node.
  - `Accessibility.nodesUpdated`: Sent every time a previously requested node has changed in the tree. Params: `nodes` (list[AXNode]) — updated node data.
- **Tests unitarios**: **64 tests** en `tests/unit/domains/test_accessibility.py` con FakeSender — cubriendo los 8 métodos, parámetros opcionales, bools siempre enviados (`fetchRelatives`), edge cases de `omitempty,omitzero` (0 y "" omitidos, combinaciones de múltiples parámetros zero/empty, valores negativos enviados), tipos (`id` es string en `get_child_ax_nodes`), return values, secuencia de llamadas, y conteo de métodos. Cobertura: **100%** (55/55 statements).
- **Tests de integración**: **34 tests** en `tests/integration/test_accessibility_storage_tracing_animation.py` con navegador real — enable/disable, get_full_ax_tree (con/sin depth, depth=0, frameId), get_partial_ax_tree (con nodeId, backendNodeId, objectId, fetchRelatives true/false, fetchRelatives=false sin node), get_root_ax_node (con/sin enable, frameId), get_child_ax_nodes (con/sin enable, invalid id, frameId), get_ax_node_and_ancestors (con nodeId, backendNodeId, objectId), query_ax_tree (por role, por name, sin filtros, role inexistente, múltiples roles, sin node → error, backendNodeId, objectId), flujos completos (full AX inspection, DOM modification + query, ancestors chain, partial vs full consistency, screenshot + AX, depth limit), edge cases (invalid nodeId, enable twice, disable without enable).
- **E2E tests**: **35 tests** en `tests/e2e/test_accessibility_e2e.py` con flujos completos contra navegador real — enable/disable lifecycle (con return values), getFullAXTree (con/sin depth, depth=0, shallow vs deep), getPartialAXTree (con nodeId, backendNodeId, fetchRelatives true/false), getRootAXNode (con/sin enable → error), getChildAXNodes (con enable, returns list, invalid id → error), queryAXTree (por role, por name, sin filtros, role inexistente, role+name combinados), getAXNodeAndAncestors (con nodeId, con backendNodeId), enable twice, disable without enable, flujos completos (full AX inspection flow, DOM modification + AX query, ancestors chain, partial vs full consistency, screenshot + AX, múltiples roles, full lifecycle, repeated enable/disable 3 ciclos).
- **Total: 64 unit tests + 34 integration tests + 35 E2E tests = 133 tests** para el dominio Accessibility.
- **Cobertura de código**: **100%** (55/55 statements en `cdpwave/domains/accessibility.py`).
- **B017 corregido**: 2 tests de integración con `pytest.raises(Exception)` cambiados a `pytest.raises(CDPError)`.
- **Marker `e2e` registrado**: en `tests/conftest.py` y `pyproject.toml` (faltaba antes de esta revisión).

### CSS (revisado contra Go source cdproto)

- **38 comandos CDP** en Go source, **38 métodos directos** en cdpwave (0 faltantes, 5 extra convenience).
- **10 bugs encontrados y corregidos**:
  1. `force_starting_style`: enviaba `startingStyle: dict` en vez de `forced: bool` (Go source: `Forced bool` sin omitempty). Cambiado a parámetro requerido `forced: bool`.
  2. `get_longhand_properties`: tenía parámetro espurio `style_sheet_id` (no existe en Go source) y faltaba parámetro requerido `value` (Go source: `Value string` sin omitempty). Corregido a `shorthand_name: str` + `value: str`.
  3. `set_property_rule_property_name`: enviaba `name` en vez de `propertyName` (Go source: `PropertyName Value`). Corregido.
  4. `track_computed_style_updates_for_node`: tenía parámetro espurio `properties_to_track` (no existe en Go source) y `node_id` era requerido. Go source: `NodeID cdp.NodeID` con `omitempty`. Cambiado a `node_id: int | None = None` (omitir si no se pasa o es 0).
  5. `create_style_sheet`: faltaba parámetro `force: bool` (Go source: `Force bool` sin omitempty — siempre se envía). Añadido con default `False`.
  6. `add_rule`: `location` era opcional (`None`) pero en Go source es requerido (`Location *SourceRange` sin omitempty). Cambiado a requerido. Añadido parámetro opcional `node_for_property_syntax_validation` (Go source: `NodeForPropertySyntaxValidation cdp.NodeID` con omitempty).
  7. `resolve_values`: `node_id` era opcional pero en Go source es requerido (`NodeID cdp.NodeID` sin omitempty). Cambiado a requerido. Añadidos 3 parámetros opcionales con `omitzero`: `property_name`, `pseudo_type`, `pseudo_identifier` (Go source: `PropertyName`, `PseudoType`, `PseudoIdentifier` todos con `omitempty,omitzero`).
  8. `set_container_query_text`: **no existe en CDP** (Go source no tiene `SetContainerQueryText`). Eliminado. El método correcto es `set_container_query_condition_text` (Go source: `SetContainerQueryConditionText`).
  9. `get_layout_tree_and_styles`: **no existe en CDP** (Go source no tiene `GetLayoutTreeAndStyles`). Eliminado.
  10. `set_style_texts`: no existía como método directo. Añadido (Go source: `SetStyleTexts` con `Edits []*StyleDeclarationEdit` requerido + `NodeForPropertySyntaxValidation` opcional).
- **Métodos extra (convenience, 5)**: `get_inline_styles` (alias de `get_inline_styles_for_node`), `get_stylesheet_text`/`set_stylesheet_text` (aliases de `get_style_sheet_text`/`set_style_sheet_text`), `set_rule_style` (wrapper de `set_style_texts` con un solo edit), `set_style_text` (wrapper de `set_style_texts` con un solo edit + range). Todos documentados como convenience en una sección separada del archivo.
- **Cambios de precisión (docstrings, orden y eventos)**:
  - Orden de métodos reordenado para coincidir con Go source (orden alfabético de aparición en `css.go`): `addRule` → `collectClassNames` → `createStyleSheet` → `disable` → `enable` → `forcePseudoState` → `forceStartingStyle` → `getBackgroundColors` → `getComputedStyleForNode` → `resolveValues` → `getLonghandProperties` → `getInlineStylesForNode` → `getAnimatedStylesForNode` → `getMatchedStylesForNode` → `getEnvironmentVariables` → `getMediaQueries` → `getPlatformFontsForNode` → `getStyleSheetText` → `getLayersForNode` → `getLocationForSelector` → `trackComputedStyleUpdatesForNode` → `trackComputedStyleUpdates` → `takeComputedStyleUpdates` → `setEffectivePropertyValueForNode` → `setPropertyRulePropertyName` → `setKeyframeKey` → `setMediaText` → `setContainerQueryConditionText` → `setSupportsText` → `setNavigationText` → `setScopeText` → `setRuleSelector` → `setStyleSheetText` → `setStyleTexts` → `startRuleUsageTracking` → `stopRuleUsageTracking` → `takeCoverageDelta` → `setLocalFontsEnabled`.
  - Todos los docstrings actualizados para coincidir exactamente con las descripciones del Go source.
  - Parámetros renombrados a snake_case consistentemente: `range_start` → `range_` (evita conflicto con builtin `range`), `pseudo_state` → `forced_pseudo_classes`, `shorthand_name` mantiene nombre.
  - Module docstring: añadida descripción completa del dominio + documentación de los 6 eventos del dominio CSS.
  - Class docstring: añadidos los 6 eventos con sus parámetros y tipos.
- **Tipos verificados contra Go source `types.go`**:
  - `StyleSheetID` es `string` (Go source `type StyleSheetID string`) — todos los métodos usan `style_sheet_id: str` correctamente.
  - `cdp.NodeID` es `int` (Go source) — todos los métodos usan `node_id: int` correctamente.
  - `SourceRange` es un struct con `StartLine`, `StartColumn`, `EndLine`, `EndColumn` (todos `int64`) — pasado como `dict[str, Any]` con keys `startLine`, `startColumn`, `endLine`, `endColumn`.
  - `CSSRange` es un struct con `StartLine`, `StartColumn`, `EndLine`, `EndColumn` — mismo formato que SourceRange.
  - `StyleDeclarationEdit` tiene `StyleSheetID`, `Range *SourceRange` (omitempty), `Text string` — pasado como dict.
  - `ComputedStyleProperty` tiene `Name string`, `Value string` — pasado como dict.
  - `Forced bool` en `forceStartingStyle` — sin omitempty, siempre se envía.
  - `Force bool` en `createStyleSheet` — sin omitempty, siempre se envía.
  - `Enabled bool` en `setLocalFontsEnabled` — sin omitempty, siempre se envía.
- **Eventos del dominio CSS** (verificado contra Go source `events.go`):
  - `CSS.fontsUpdated`: fires whenever a web font is updated. Params: `font` (FontFace, optional).
  - `CSS.mediaQueryResultChanged`: fires whenever a MediaQuery result changes. No params.
  - `CSS.styleSheetAdded`: fired whenever an active document stylesheet is added. Params: `header` (StyleSheetHeader).
  - `CSS.styleSheetChanged`: fired whenever a stylesheet is changed as a result of the client operation. Params: `styleSheetId` (str).
  - `CSS.styleSheetRemoved`: fired whenever an active document stylesheet is removed. Params: `styleSheetId` (str).
  - `CSS.computedStyleUpdated`: [no description]. Params: `nodeId` (int).
- **Tests unitarios**: **160+ tests** en `tests/unit/domains/test_css.py` con FakeSender — cubriendo los 38 métodos directos + 5 convenience, parámetros requeridos vs opcionales, `omitzero` (string vacío omitido), booleanos siempre enviados (`force`, `forced`, `enabled`), `node_id=0` omitido en `track_computed_style_updates_for_node`, return values, edge cases, secuencia de llamadas.
- **Tests de integración**: **16 tests** en `tests/integration/test_cachestorage_css_domdebugger_eventbreakpoints.py` con navegador real — enable/disable, get_media_queries, get_inline_styles_for_node, get_computed_style_for_node, get_matched_styles_for_node, create_style_sheet + set/get_text, collect_class_names, get_platform_fonts_for_node, get_background_colors, force_pseudo_state, start/stop_rule_usage_tracking + take_coverage_delta, track/take_computed_style_updates, set_local_fonts_enabled, get_environment_variables, get_longhand_properties, full lifecycle.
- **E2E tests**: **5 tests** en `tests/e2e/test_css_e2e.py` con flujos completos — full CSS lifecycle, enable/disable cycle, CSS without enable raises CommandError, create and modify stylesheet, track_computed_style_for_node.
- **Tests actualizados en otros archivos**: `test_expanded_methods.py` (add_rule ahora requiere location, create_style_sheet ahora envía force), `test_tier3i_domains.py` (removido test de get_layout_tree_and_styles que ya no existe).
- **Total: 160+ unit tests + 16 integration tests + 5 E2E tests = 181+ tests** para el dominio CSS.

### Console (revisado contra CDP spec oficial — dominio deprecado)

- **3 comandos CDP** en CDP spec oficial, **3 métodos** en cdpwave (0 extra, 0 faltantes).
- **Nota**: El dominio Console fue removido de chromedp/cdproto (directorio `console/` no existe en el repo). La revisión se realizó contra la especificación CDP oficial en https://chromedevtools.github.io/devtools-protocol/tot/Console/.
- **0 bugs** encontrados. Todos los métodos son parameterless (`params=None`), coinciden con la spec.
- **Cambios de precisión (docstrings, orden y eventos)**:
  - Orden de métodos reordenado para coincidir con CDP spec (orden alfabético): `clear_messages` → `disable` → `enable` (antes era `enable` → `disable` → `clear_messages`).
  - `clear_messages` docstring: "Clear all accumulated console messages" → "Does nothing" (coincide con CDP spec exacto — el comando `Console.clearMessages` no tiene descripción en la spec oficial, solo "Does nothing").
  - `disable` docstring: "Disable Console domain events" → "Disables console domain, prevents further console messages from being reported to the client" (coincide con CDP spec exacto).
  - `enable` docstring: "Enable Console domain events" → "Enables console domain, sends the messages collected so far to the client by means of the messageAdded notification" (coincide con CDP spec exacto).
  - `enable` docstring: removida nota de deprecación del docstring del método (la deprecación ya está documentada en module docstring y class docstring; el docstring del método debe coincidir con la spec).
  - `disable` docstring: removida nota de deprecación del docstring del método (mismo motivo).
  - Module docstring: "Console domain: deprecated console message clearing" → "Console domain: deprecated console domain for console messages" + documentación de eventos y tipos.
  - Module docstring: añadidos todos los campos de ConsoleMessage con tipos y optionality (verificado contra CDP spec: `source` sin omitempty, `level` sin omitempty, `text` sin omitempty, `url`/`line`/`column` opcionales).
  - Class docstring: añadido evento `Console.messageAdded` con descripción y parámetros (verificado contra CDP spec: `message` es ConsoleMessage).
- **Tipos verificados contra CDP spec oficial**:
  - `ConsoleMessage`: struct con `source` (str enum), `level` (str enum), `text` (str), `url` (str, optional), `line` (int, optional, 1-based), `column` (int, optional, 1-based).
  - `MessageSource` values: `xml`, `javascript`, `network`, `console-api`, `storage`, `appcache`, `rendering`, `security`, `other`, `deprecation`, `worker` (11 valores).
  - `MessageLevel` values: `log`, `warning`, `error`, `debug`, `info` (5 valores).
- **Eventos del dominio Console** (verificado contra CDP spec oficial):
  - `Console.messageAdded`: Issued when new console message is added. Params: `message` (ConsoleMessage dict) — console message that has been added.
- **Tests unitarios**: **34 tests** en `tests/unit/domains/test_console.py` con FakeSender — cubriendo los 3 métodos (no params, return values, single call, params es `None` no `{}`, exact CDP method name, llamada repetida 3x), orden alfabético de métodos, existencia de los 3 métodos, ausencia de métodos extra, verificación de que todos los métodos son coroutines (`inspect.iscoroutinefunction`), secuencias de llamadas (full lifecycle, repeated enable/disable, clear without enable, disable without enable, interleaved calls, solo clear/enable/disable repetido 5x), propagación de `CommandError` (cada método levanta `CommandError` con code y message correctos, error detiene ejecución).
- **Tests de integración**: **24 tests** en `tests/integration/test_log_console_target.py` con navegador real — enable/disable (con return values), clear_messages (con y sin enable previo), disable without enable, repeated enable/disable (3 ciclos), full lifecycle (enable → evaluate → clear → disable), messageAdded event (verificación de campos `source`/`level`/`text`), source values contra 11 valores válidos, level values contra 5 valores válidos, messageAdded para los 5 niveles (`log`/`warning`/`error`/`info`/`debug`), múltiples mensajes (3 mensajes con verificación de texts), no eventos después de disable, enable twice, disable twice, clear after messages, campos opcionales (`url`/`line`/`column`) con type checking, text content exacto, console con runtime.enable.
- **E2E tests**: **33 tests** en `tests/e2e/test_console_e2e.py` con flujos completos contra navegador real — enable/disable (con return values), clear_messages (con y sin enable), disable without enable, repeated enable/disable (3 ciclos), full lifecycle, messageAdded para los 5 niveles (`log`/`warning`/`error`/`info`/`debug`) con verificación de `text` y `level` exactos, verificación de `source` contra 11 valores válidos y `source == "console-api"` para `console.log`, verificación de `text` como str, campos opcionales (`url`/`line`/`column`) con type checking, clear after messages, enable twice, disable twice, all methods call sequence, no events after disable, múltiples mensajes (3 mensajes), múltiples niveles en secuencia (5 niveles con verificación), clear then no new messages, console con runtime.enable, all required fields (`source`/`level`/`text`), deprecation source (XMLHttpRequest), error does not raise, clear does not raise without messages, re-enable after disable, raw `session.send` para los 3 comandos.
- **Tests actualizados en otros archivos**: `test_new_domains.py` (removidos 3 tests redundantes de `TestConsoleDomain` y import de `ConsoleDomain` — movidos a archivo dedicado `test_console.py`).
- **Segunda revisión (bug audit)**: 0 bugs encontrados en implementación. Helper `_wait_for_console_message` actualizado para incluir `runtime.enable()` (mejora confiabilidad de eventos). Helper `_wait_for_multiple_console_messages` añadido para tests de múltiples mensajes. `ErrorSender` añadido en tests unitarios para propagación de `CommandError`.
- **Tercera revisión (edge cases)**: 0 bugs encontrados. Añadidos tests edge case:
  - **Unit (+10 tests)**: `isinstance(BaseDomain)`, return exact response object, `set_response` between calls, mixed error/success senders, method signatures (no required params), large response dict (100 keys), `None` response from sender, error sender records call before raising, all methods use `Console.` prefix, concurrent calls via `asyncio.gather`.
  - **Integration (+15 tests)**: special chars (ñ, emoji, tabs, newlines), empty string, long text (5000 chars), multiple args, uncaught exception, `console.assert(false)`, `console.count`, `console.dir`, `console.trace`, `console.table`, rapid fire (20 messages), `console.group`/`groupEnd`, `console.time`/`timeEnd`, `console.clear()` browser-side.
  - **E2E (+18 tests)**: unicode/emoji text, empty string, long text (10000 chars), multiple args, uncaught exception, `console.assert(false)`, `console.count`, `console.dir`, `console.trace`, `console.table`, rapid fire (20 messages), `console.group`/`groupEnd`, `console.time`/`timeEnd`, `console.clear()` browser-side, message after navigation, enable→disable→enable→message, all methods return dict, line/column positive.
- **Total: 37 unit tests + 39 integration tests + 51 E2E tests = 127 tests** para el dominio Console.

---

## CacheStorage

- **Archivo**: `cdpwave/domains/cache_storage.py`
- **Spec CDP**: https://chromedevtools.github.io/devtools-protocol/tot/CacheStorage/
- **Métodos CDP (5)**: `deleteCache`, `deleteEntry`, `requestCacheNames`, `requestCachedResponse`, `requestEntries`.
- **Métodos implementados (5)**: `delete_cache`, `delete_entry`, `request_cache_names`, `request_cached_response`, `request_entries`.
- **Paridad**: 5/5 métodos CDP implementados. 0 faltantes. 0 extra.

### Bugs encontrados y corregidos

- **Bug #1 — Método faltante `requestCachedResponse`**: La spec CDP define `CacheStorage.requestCachedResponse` para recuperar el body de una respuesta cacheada. No estaba implementado. **Corregido**: añadido `request_cached_response(cache_id, request_url, request_headers)`.
- **Bug #2 — Métodos extra `enable`/`disable`**: `CacheStorage.enable` y `CacheStorage.disable` no existen en la spec CDP. Llamarlos contra un navegador real causa `CommandError`. **Corregido**: eliminados ambos métodos.
- **Bug #3 — `request_entries` siempre enviaba `skipCount` y `pageSize`**: Los defaults `skip_count=0` y `page_size=100` siempre se enviaban al browser. La spec usa `omitempty` — los valores zero deben omitirse. **Corregido**: cambiados defaults a `None`, solo se envían si son truthy.
- **Bug #4 — `request_cache_names` violaba `omitempty` para strings**: `security_origin` y `storage_key` usaban `if ... is not None:`, que envía strings vacíos `""`. La spec CDP usa `omitempty` en Go, que omite strings vacíos. **Corregido**: cambiados a truthy check (`if security_origin:`).
- **Bug #5 — `request_entries` violaba `omitempty` para `path_filter`**: Usaba `if path_filter is not None:` que envía `pathFilter: ""`. **Corregido**: cambiado a truthy check (`if path_filter:`).
- **Bug #6 — `request_cached_response` enviaba `responseHeaders` en vez de `requestHeaders`**: El struct Go confirma `RequestHeaders []*CacheStorageHeader json:"requestHeaders"`. La spec CDP dice "headers of the request", no "headers of the response". **Corregido**: cambiado el parámetro CDP de `responseHeaders` a `requestHeaders`.
- **Bug #7 — El parámetro Python se llamaba `response_headers` pero debería ser `request_headers`**: El nombre snake_case debe reflejar el parámetro CDP real. **Corregido**: renombrado a `request_headers`.
- **Bug #8 — Docstring incorrecta del return de `request_cached_response`**: Decía "Dict with `body`" pero el return real es `{"response": {"body": ...}}` según `CacheStorageRequestCachedResponseResult`. **Corregido**: docstring actualizada.
- **Bug #9 — `skip_count` y `page_size` usaban truthy check pero Go usa `*int` con `omitempty`**: Go usa `*int` (puntero) con `omitempty`, que omite solo cuando es `nil`, no cuando apunta a `0`. `skip_count=0` debería enviarse (como Go `&0`), no omitirse. **Corregido**: cambiados a `is not None` check. Solo `None` se omite.
- **Bug #10 — Eventos `cacheAdded` y `cacheContentListLoaded` no existen en la spec CDP**: La spec de CacheStorage no tiene sección de Events. Las docstrings los documentaban incorrectamente. **Corregido**: eliminados de las docstrings del módulo y clase.
- **Bug #11 — Docstrings con `(omitempty)`**: `skip_count` y `page_size` tenían "(omitempty)" en sus docstrings, un detalle de implementación de Go. **Corregido**: eliminado "(omitempty)", actualizado a "Number of records to skip/fetch" según CDP spec.
- **Bug #12 — Docstrings no coincidían con la spec CDP**: `delete_entry` decía "Deletes a specific entry from a cache" (CDP: "Deletes a cache entry"), `request_entries` decía "Requests data entries from a cache" (CDP: "Requests data from cache"), `path_filter` decía "Optional path filter string" (CDP: "If present, only return the entries containing this substring in the path"). **Corregido**: docstrings alineadas con la spec CDP exacta.
- **Bug #13 — `request_cache_names` no documentaba la restricción de params**: La spec CDP dice "At least and at most one of securityOrigin, storageKey, storageBucket must be specified." **Corregido**: añadida la restricción a la docstring.

### Eventos

El dominio CacheStorage no tiene eventos en la spec CDP.

### Tests unitarios

- **59 tests** en `tests/unit/domains/test_cache_storage.py` con FakeSender — cubriendo los 5 métodos:
  - `delete_cache`: params, return values, exact CDP method name, single call, repeated 3x.
  - `delete_entry`: params, return values, empty request URL, exact CDP method name.
  - `request_cache_names`: security_origin, storage_key, storage_bucket, all params, no params (empty dict), omitempty empty security_origin, omitempty empty storage_key, return caches list, omitempty for optionals.
  - `request_cached_response`: params, return body, empty headers, multiple headers, exact CDP method name.
  - `request_entries`: only cache_id, skip_count, page_size, path_filter, all params, skip_count=0 is sent, page_size=0 is sent, omitempty skip_count=None, omitempty page_size=None, omitempty empty path_filter, return entries, exact CDP method name.
  - Method parity: 5 methods exist, no extra methods, all coroutines, `isinstance(BaseDomain)`, alphabetical order.
  - Call sequence: full lifecycle, repeated delete_cache 5x, interleaved calls, all methods use `CacheStorage.` prefix.
  - Error propagation: `CommandError` for each method, error stops execution.
  - Edge cases: `set_response` between calls, large response dict (100 keys), method signatures, concurrent calls via `asyncio.gather`, empty URL, empty cache_id, mixed error/success.

### Tests de integración

- **20 tests** en `tests/integration/test_cache_storage.py` con navegador real — request_cache_names (security_origin, no params, storage_key), request_entries (empty cache, skip_count, page_size, path_filter, all optional params, omitempty skip_count=0, large page_size), full lifecycle (create + delete), request_cached_response, delete nonexistent cache/entry/entries (CommandError), raw send, return dict verification, multiple caches create and list, delete entry and verify, request entries nonexistent cache.

### E2E tests

- **28 tests** en `tests/e2e/test_cache_storage_e2e.py` con flujos completos contra navegador real — request_cache_names (security_origin, no params, storage_key), create cache via JS Cache API and list via CDP, request_entries after create, verify URL in entries, request_cached_response body, delete entry and verify removed, delete cache and verify removed, full lifecycle (create → entries → cached response → delete entry → delete cache), path_filter, skip_count + page_size, raw send for all 5 commands, all methods return dict, multiple caches, empty cache_id (CommandError), nonexistent cache (CommandError), nonexistent cached response (CommandError), special chars URL, unicode body, omitempty no optional params, large skip count, page_size=1, delete entry then delete cache, repeated request_cache_names, invalid origin (CommandError).

### Tests actualizados en otros archivos

- `test_coverage_gaps.py`: removidos `test_enable` y `test_disable` de `TestCacheStorageCoverage` (métodos eliminados).
- `test_tier3i_domains.py`: tests existentes siguen funcionando (params explícitos siguen válidos).
- `test_param_casuistics.py`: test existente sigue funcionando.

### Quality checks

- `ruff check`: ✅
- `mypy --strict`: ✅
- `pytest -m unit`: 59/59 passed

### Total: 59 unit tests + 20 integration tests + 28 E2E tests = 107 tests para el dominio CacheStorage.

---

## IndexedDB

- **Archivo**: `cdpwave/domains/indexed_db.py`
- **Spec CDP**: https://chromedevtools.github.io/devtools-protocol/tot/IndexedDB/
- **Go source**: `go-rod/rod/lib/proto/indexed_db.go`
- **Métodos CDP (9)**: `clearObjectStore`, `deleteDatabase`, `deleteObjectStoreEntries`, `disable`, `enable`, `getMetadata`, `requestData`, `requestDatabase`, `requestDatabaseNames`.
- **Métodos implementados (9)**: `clear_object_store`, `delete_database`, `delete_object_store_entries`, `disable`, `enable`, `get_metadata`, `request_data`, `request_database`, `request_database_names`.
- **Paridad**: 9/9 métodos CDP implementados. 0 faltantes. 0 extra.

### Bugs encontrados y corregidos

- **Bug #1 — `security_origin` y `storage_key` violaban `omitempty` para strings**: Todos los métodos que aceptan `security_origin` y `storage_key` usaban `if ... is not None:`, que envía strings vacíos `""`. El Go source usa `omitempty` para strings (`SecurityOrigin string json:"securityOrigin,omitempty"`), que omite strings vacíos. **Corregido**: cambiados a truthy check (`if security_origin:`) en los 7 métodos afectados (`clear_object_store`, `delete_database`, `delete_object_store_entries`, `get_metadata`, `request_data`, `request_database`, `request_database_names`).
- **Bug #2 — `request_data` `index_name` era opcional (`None`) pero Go siempre lo envía**: El parámetro `index_name` tenía default `None` y solo se enviaba si no era `None`. El Go source usa `IndexName string json:"indexName"` (sin `omitempty`), lo que significa que siempre se envía, incluso como string vacío. **Corregido**: cambiado default a `str = ""` y se envía siempre en el dict de params.
- **Bug #3 — `request_data` `skip_count` y `page_size` siempre se enviaban (correcto)**: Go usa `SkipCount int json:"skipCount"` y `PageSize int json:"pageSize"` (sin `omitempty`), confirmando que siempre se envían. **Verificado**: comportamiento correcto, no se cambió.
- **Bug #4 — `delete_object_store_entries` `key_range` siempre se envía (correcto)**: Go usa `KeyRange *IndexedDBKeyRange json:"keyRange"` (sin `omitempty`), confirmando que siempre se envía. **Verificado**: comportamiento correcto, no se cambió.
- **Bug #5 — Docstrings no coincidían con la spec CDP**: Las docstrings de todos los métodos usaban descripciones genéricas en vez de las descripciones exactas de la spec CDP. **Corregido**: alineadas con la spec CDP exacta:
  - `clear_object_store`: "Clears all entries from an object store."
  - `delete_database`: "Deletes a database."
  - `delete_object_store_entries`: "Delete a range of entries from an object store"
  - `disable`: "Disables events from backend."
  - `enable`: "Enables events from backend."
  - `get_metadata`: "Gets metadata of an object store."
  - `request_data`: "Requests data from object store or index."
  - `request_database`: "Requests database with given name in given frame."
  - `request_database_names`: "Requests database names for given security origin."
- **Bug #6 — Restricción de params no documentada**: La spec CDP dice "At least and at most one of securityOrigin, storageKey, or storageBucket must be specified" para todos los métodos con esos params. **Corregido**: añadida la restricción a las docstrings de los 7 métodos afectados.
- **Bug #7 — `index_name` docstring no coincidía con CDP**: Decía "Optional index to query (instead of store)" pero la spec dice "Index name, empty string for object store data requests." **Corregido**: docstring actualizada.
- **Bug #8 — Return values no documentados correctamente**: `get_metadata` no documentaba `entriesCount` y `keyGeneratorValue` con descripciones de la spec. `request_data` no documentaba `objectStoreDataEntries` y `hasMore`. `request_database` no documentaba `databaseWithObjectStores`. `request_database_names` no documentaba `databaseNames`. **Corregido**: return docstrings actualizadas con descripciones exactas de la spec CDP y Go source.
- **Bug #9 — Orden de métodos no alfabético**: Los métodos estaban en orden `enable, disable, request_database_names, request_database, request_data, delete_database, clear_object_store, delete_object_store_entries, get_metadata`. **Corregido**: reordenados alfabéticamente para coincidir con el Go source: `clear_object_store, delete_database, delete_object_store_entries, disable, enable, get_metadata, request_data, request_database, request_database_names`.
- **Bug #10 — Module docstring no mencionaba ausencia de eventos**: La spec CDP de IndexedDB no tiene sección de Events. **Corregido**: añadido "The IndexedDB domain has no events in the CDP spec." al module y class docstrings.

### Eventos

El dominio IndexedDB no tiene eventos en la spec CDP.

### Tests unitarios

- **140 tests** en `tests/unit/domains/test_indexed_db.py` con FakeSender — cubriendo los 9 métodos:
  - `clear_object_store`: params con security_origin, storage_key, storage_bucket, all params, omitempty empty security_origin, omitempty empty storage_key, returns empty, returns response, exact CDP method name, single call, repeated 5x, no origin/key/bucket.
  - `delete_database`: params con security_origin, storage_key, storage_bucket, omitempty empty security_origin, omitempty empty storage_key, returns empty, returns response, exact CDP method name, repeated 5x, no origin/key/bucket.
  - `delete_object_store_entries`: params con security_origin, storage_key, storage_bucket, key_range always sent, omitempty empty security_origin, omitempty empty storage_key, returns empty, exact CDP method name, empty key_range, no origin/key/bucket.
  - `disable`: params none, returns empty, returns response, exact CDP method name, single call, sends None not empty dict.
  - `enable`: params none, returns empty, returns response, exact CDP method name, single call, sends None not empty dict.
  - `get_metadata`: params con security_origin, storage_key, storage_bucket, omitempty empty security_origin, omitempty empty storage_key, returns entriesCount and keyGeneratorValue, exact CDP method name, zero values, float keyGeneratorValue, no origin/key/bucket.
  - `request_data`: params con security_origin, storage_key, storage_bucket, index_name always sent default empty, index_name with value, skip_count always sent default zero, page_size always sent default ten, skip_count with value, page_size with value, page_size=0, negative skip_count, negative page_size, large skip_count, large page_size, key_range omitted when None, key_range sent when provided, empty key_range dict, complex key_range, omitempty empty security_origin, omitempty empty storage_key, all params, returns entries and hasMore, exact CDP method name, empty entries hasMore false, skip+page combined, exact response, no origin/key/bucket.
  - `request_database`: params con security_origin, storage_key, storage_bucket, omitempty empty security_origin, omitempty empty storage_key, returns databaseWithObjectStores, exact CDP method name, complex nested response, no origin/key/bucket.
  - `request_database_names`: params con security_origin, storage_key, storage_bucket, no params sends empty dict, omitempty empty security_origin, omitempty empty storage_key, returns databaseNames list, exact CDP method name, empty list, single element.
  - Method parity: 9 methods exist, no extra methods, all coroutines, `isinstance(BaseDomain)`, alphabetical order.
  - Call sequence: full lifecycle (9 calls), repeated enable/disable 3x, interleaved calls, all methods use `IndexedDB.` prefix.
  - Error propagation: `CommandError` for each of the 9 methods, error stops execution, error sender records call before raising, error code preserved, error message preserved.
  - Edge cases round 1: `set_response` between calls, large response dict (100 keys), method signatures (defaults verified), concurrent calls via `asyncio.gather`, mixed error/success, None response from sender, empty database_name sent, empty object_store_name sent, request_data empty strings sent.
  - Edge cases round 2: page_size=0, skip_count=0 explicit, negative skip_count/page_size, large skip_count/page_size, empty key_range dict, complex key_range, empty storage_bucket dict, storage_bucket with name, no origin/key/bucket for all 7 methods, repeated clear/delete 5x, zero values get_metadata, empty entries hasMore false, complex nested request_database, empty/single databaseNames, empty key_range delete_entries, all methods with storage_key only, all methods with storage_bucket only, skip+page combined, concurrent same method, concurrent all different methods, error code/message preserved, exact response, float keyGeneratorValue, params not mutated between calls, no params is dict not None, enable/disable sends None.

### Tests de integración

- **52 tests** en `tests/integration/test_indexed_db.py` con navegador real — enable/disable, enable returns empty, disable returns empty, request_database_names (security_origin, storage_key), request_database, request_data, request_data with skip_count, request_data with page_size, request_data with index_name, get_metadata, clear_object_store, delete_object_store_entries, delete_database, full lifecycle, empty db request_database_names, nonexistent database name (CommandError), nonexistent db request_data (CommandError), nonexistent db get_metadata (CommandError), nonexistent db delete_database (CommandError), nonexistent db clear_object_store (CommandError), raw send all commands, return dict verification for all methods, repeated enable/disable, request_data large page_size. Edge: page_size=0, skip_count exceeds records, get_metadata after clear, clear nonexistent store (CommandError), delete entries partial, request_database object store details, multiple databases create and list, request_data with key_range, request_data after delete entries, enable/disable/re-enable, request_database_names after delete, all methods with storage_key (request_data, get_metadata, request_database, clear_object_store, delete_database, delete_object_store_entries), request_data pagination, request_data hasMore true with small page, raw send get_metadata, raw send delete_object_store_entries.

### E2E tests

- **60 tests** en `tests/e2e/test_indexed_db_e2e.py` con flujos completos contra navegador real — enable/disable, enable returns dict, disable returns dict, request_database_names (security_origin, storage_key), request_database (verify name and object stores), request_data (verify entries), request_data with skip_count, request_data with page_size (verify hasMore), request_data with index_name empty, request_data with key_range, get_metadata (verify entriesCount=3), clear_object_store (verify entriesCount=0), delete_object_store_entries (verify entriesCount=0), delete_database (verify removed from names), full lifecycle (create → names → database → data → metadata → clear → delete), raw send for all 9 commands, all methods return dict, empty db, nonexistent database (CommandError), nonexistent db request_data (CommandError), nonexistent db get_metadata (CommandError), nonexistent db delete_database (CommandError), nonexistent db clear_object_store (CommandError), repeated enable/disable 3x, enable twice, disable without enable, request_data large page_size, multiple databases, request_data after clear (verify empty), request_data all params. Edge: page_size=0, skip_count exceeds records, get_metadata after clear, clear nonexistent store (CommandError), delete entries then verify empty, request_database object store fields, multiple databases create/list/delete, request_data with key_range (verify 3 entries), enable/disable/re-enable, request_data pagination (verify hasMore true then false), request_data hasMore true, all methods with storage_key (full lifecycle), raw send all 9 commands, nonexistent db delete_object_store_entries (CommandError), full lifecycle with storage_key, request_data empty key_range, delete entries empty key_range, get_metadata float keyGeneratorValue, request_data nonexistent index_name (CommandError), request_database_names no params (CommandError), request_database no origin/key (CommandError), clear_object_store no origin/key (CommandError).

### Tests actualizados en otros archivos

- `test_tier3g_domains.py`: tests existentes siguen funcionando (params explícitos no vacíos siguen válidos con truthy check).
- `test_coverage_gaps.py`: tests existentes siguen funcionando (usan `security_origin`, `storage_key`, `storage_bucket` con valores no vacíos).
- `test_coverage_boost.py`: tests existentes siguen funcionando.
- `test_expanded_methods.py`: tests existentes siguen funcionando (`delete_object_store_entries` y `get_metadata` con params posicionales).
- `test_param_casuistics.py`: tests existentes siguen funcionando (`request_data` con `index_name="idx1"` y `key_range`).
- `test_preload_indexeddb_media_deviceaccess.py`: tests existentes siguen funcionando.

### Quality checks

- `ruff check`: ✅
- `mypy --strict`: ✅
- `pytest -m unit`: 194/194 passed

### Total: 194 unit tests + 67 integration tests + 75 E2E tests = 336 tests para el dominio IndexedDB.

---

## Performance

- **Archivo**: `cdpwave/domains/performance.py`
- **Spec CDP**: https://chromedevtools.github.io/devtools-protocol/tot/Performance/
- **Go source**: `go-rod/rod/lib/proto/performance.go`
- **Métodos CDP (4)**: `disable`, `enable`, `getMetrics`, `setTimeDomain`.
- **Métodos implementados (4)**: `disable`, `enable`, `get_metrics`, `set_time_domain`.
- **Paridad**: 4/4 métodos CDP implementados. 0 faltantes. 0 extra.

### Bugs encontrados y corregidos

- **Bug #1 — `enable` faltaba parámetro opcional `time_domain`**: Go source `PerformanceEnable` tiene `TimeDomain PerformanceEnableTimeDomain json:"timeDomain,omitempty"`. CDP spec muestra parámetro opcional `timeDomain` con valores `"timeTicks"` y `"threadTicks"`. cdpwave's `enable()` no aceptaba parámetros. **Corregido**: añadido `time_domain: str | None = None` con truthiness check (coincide con `omitempty` en Go).
- **Bug #2 — `set_time_domain` docstring con valor de enum incorrecto**: Decía `"wallTime"` pero los valores correctos son `"timeTicks"` y `"threadTicks"` (verificado contra Go source `PerformanceSetTimeDomainTimeDomain` y CDP spec). **Corregido**.
- **Bug #3 — `set_time_domain` docstring sin nota de deprecación**: Go source marca el comando como `(deprecated) (experimental)`. **Corregido**: añadida nota "Deprecated and experimental".
- **Bug #4 — `set_time_domain` docstring sin notas de uso importantes**: Go source dice "Must be called before enabling metrics collection. Calling this method while metrics collection is enabled returns an error." **Corregido**: añadidas ambas notas.
- **Bug #5 — `set_time_domain` docstring sin sección `Returns`**: Los demás métodos tienen `Returns: Response dict from the CDP.`. **Corregido**.
- **Bug #6 — `enable` docstring no coincidía con spec**: "Enable collecting performance metrics" → "Enable collecting and reporting metrics" (coincide con Go source y CDP spec exacto). **Corregido**.
- **Bug #7 — `disable` docstring no coincidía con spec**: "Disable collecting performance metrics" → "Disable collecting and reporting metrics" (coincide con Go source y CDP spec exacto). **Corregido**.
- **Bug #8 — `get_metrics` docstring no coincidía con spec**: "Retrieve current runtime performance metrics" → "Retrieve current values of run-time metrics" (coincide con Go source y CDP spec exacto). **Corregido**.
- **Bug #9 — Orden de métodos no alfabético**: Orden era `enable, disable, get_metrics, set_time_domain`. **Corregido**: reordenado a `disable, enable, get_metrics, set_time_domain` (alfabético, coincide con Go source).
- **Bug #10 — Module docstring no mencionaba evento `Performance.metrics`**: **Corregido**: añadida documentación del evento con parámetros (`metrics` list[Metric], `title` str).
- **Bug #11 — Class docstring no documentaba parámetros del evento**: **Corregido**: añadidos parámetros del evento `Performance.metrics` (`metrics`: list[Metric] con `name`: str, `value`: float; `title`: str).
- **Bug #12 — `set_time_domain` sin validación de tipo en runtime**: El método aceptaba cualquier tipo (None, int, list, dict, bool, float, bytes) y lo enviaba al CDP como JSON inválido. Go source usa `TimeDomain PerformanceSetTimeDomainTimeDomain` (tipo enum string). **Corregido**: añadido `isinstance(time_domain, str)` check que eleva `TypeError` antes de enviar al CDP. Performance es el primer dominio en usar `isinstance` + `TypeError` para validación de tipos; otros dominios (`runtime.py`, `page.py`, `dom.py`, `fetch.py`) usan `ValueError` para validación de valores (rangos, enums, exclusión mutua).
- **Bug #13 — `enable` sin validación de tipo para `time_domain` opcional**: El método usaba `if time_domain:` (truthiness check) sin validar el tipo. Si se pasaba un valor truthy no-string (ej. `enable(time_domain=123)`), enviaba `{"timeDomain": 123}` al CDP como JSON inválido. Go source usa `TimeDomain PerformanceEnableTimeDomain` (tipo enum string). **Corregido**: añadido `isinstance(time_domain, str)` check cuando `time_domain is not None`, antes del truthiness check para `omitempty`. Preserva el comportamiento `omitempty` (string vacío no se envía) mientras captura tipos incorrectos.
- **Bug #14 — `enable` y `set_time_domain` sin validación de valores enum**: CDP spec y Go source definen valores permitidos `"timeTicks"` y `"threadTicks"`. cdpwave no validaba, enviando strings inválidos al CDP. `page.py` valida enums con `ValueError` en 10+ métodos (transition_type, referrer_policy, format, state, behavior, mode, configuration). **Corregido**: añadido `ValueError` check en ambos métodos para rechazar valores fuera del enum antes de enviar al CDP. TypeError (tipo incorrecto) toma precedencia sobre ValueError (valor inválido).
- **Bug #15 — docstring de `enable` inexacto para `ValueError`**: Decía `ValueError: If time_domain is not "timeTicks" or "threadTicks"` pero `enable(time_domain="")` no eleva `ValueError` (es `omitempty`, string vacío = no enviar). **Corregido**: docstring ahora dice `ValueError: If time_domain is a non-empty string that is not "timeTicks" or "threadTicks"`.

### Tipos verificados contra Go source

- `PerformanceMetric`: `Name string json:"name"` (sin omitempty) + `Value float64 json:"value"` (sin omitempty) — cdpwave retorna dicts con `name` y `value` correctamente.
- `PerformanceEnableTimeDomain` enum: `"timeTicks"`, `"threadTicks"` — cdpwave documenta ambos valores correctamente.
- `PerformanceSetTimeDomainTimeDomain` enum: `"timeTicks"`, `"threadTicks"` — cdpwave documenta ambos valores correctamente.
- `PerformanceEnable.TimeDomain`: `omitempty` — cdpwave valida `isinstance(time_domain, str)` cuando no es `None`, luego usa truthiness check (`if time_domain:`) para `omitempty`. Envía `None` cuando no se especifica o es string vacío.
- `PerformanceSetTimeDomain.TimeDomain`: sin `omitempty` — cdpwave valida `isinstance(time_domain, str)` + enum value, siempre envía `{"timeDomain": time_domain}` para valores válidos. String vacío eleva `ValueError`.
- `PerformanceGetMetricsResult`: `Metrics []*PerformanceMetric json:"metrics"` — cdpwave retorna dict con `metrics` list. Correcto.

### Eventos del dominio Performance

- `Performance.metrics`: Current values of the metrics. Params: `metrics` (list[Metric] — each with `name`: str, `value`: float), `title` (str — timestamp title).

### Tests unitarios

- **142 tests** en `tests/unit/domains/test_performance.py` con FakeSender — cubriendo los 4 métodos:
  - `disable`: params `None`, returns empty/response, exact CDP method name, single call, sends `None` not empty dict.
  - `enable`: params `None` without `time_domain`, params with `"timeTicks"`/`"threadTicks"`, `omitempty` empty string, `omitempty` `None`, returns empty/response, exact CDP method name, single call, sends `None` without param.
  - `get_metrics`: params `None`, returns metrics list with `name`/`value`, returns empty metrics, returns response, float value, large metrics list (100 items), exact CDP method name, single call, sends `None`.
  - `set_time_domain`: params with `"timeTicks"`/`"threadTicks"`, empty string (no omitempty — always sent), unicode string, special chars, long string (10000 chars), returns empty/response, exact CDP method name, single call.
  - Method parity: 4 methods exist, no extra methods, all coroutines, `isinstance(BaseDomain)`, alphabetical order, `enable` accepts optional `time_domain`, `set_time_domain` requires `time_domain`.
  - Error propagation: `CommandError` for each of the 4 methods, error sender records call before raising, error stops execution.
  - Concurrency: 100 concurrent `get_metrics`, concurrent mixed methods (4 methods), 50 concurrent `enable`.
  - Repetition: enable/disable 10x, repeated enable 10x, repeated set_time_domain 10x, repeated get_metrics 10x.
  - Call sequences: full lifecycle (4 calls), all methods use `Performance.` prefix, interleaved calls (7 calls).
  - Edge cases: `set_response` between calls, large response dict (100 keys), `None` response from sender, mixed error/success, enable with then without `time_domain`, `set_time_domain` preserves exact value, exact response object, params not mutated between calls.
  - Edge cases extended: `set_time_domain` TypeError for None/int/list/dict/bool/float/bytes (7 tests), `enable` TypeError for int/float/list/dict/bool/False/bytes/zero-int (8 tests), TypeError prevents sender call (both methods), `enable(None)` and `enable("")` do not raise, ValueError for invalid enum values in `enable` (8 tests: whitespace, newline, tab, unicode, long, "0", "False", "None", "wallTime") and `set_time_domain` (5 tests: "wallTime", "", "abc", " ", "\n"), TypeError takes precedence over ValueError (2 tests), new dict created each call (enable + set_time_domain), camelCase key verification, get_metrics with negative/zero/large/None values, empty name, extra keys in response/metric, extra keys in disable/enable/set_time_domain responses, custom sender compatibility.
  - Concurrency extended: 100 concurrent `set_time_domain`, 100 concurrent `disable`, 100 concurrent `enable` with param, concurrent all 4 methods, 50 enable + 50 disable.
  - Error propagation extended: positive/zero error codes, empty/long/unicode error messages, code+message preservation, error with `enable(time_domain=...)`, TypeError not swallowed by CommandError.
  - Method parity extended: exactly 4 public async methods, no sync methods, signature checks (params, kind, annotation, return), all methods have docstrings, class/module docstrings mention `Performance.metrics` event.

### Tests de integración

- **49 tests** en `tests/integration/test_performance.py` con navegador real — enable/disable (con return values), get_metrics después de enable (verificar `metrics` list con `name` y `value`), get_metrics incluye `JSHeapUsedSize` y `Nodes`, set_time_domain con `"timeTicks"` y `"threadTicks"`, set_time_domain antes de enable, set_time_domain después de enable (CommandError), get_metrics sin enable, enable repetido 10x, disable sin enable, raw send para los 4 comandos, all methods return dict, enable con `time_domain` `"timeTicks"`/`"threadTicks"`, concurrencia enable + get_metrics, repeated enable/disable 3x, enable twice, disable twice, set_time_domain valor inválido (ValueError), get_metrics después de navegación, TypeError para set_time_domain (None/int) y enable (int/list/bool), enable(None) no eleva error, enable valor inválido (ValueError), set_time_domain string vacío (ValueError).

### E2E tests

- **54 tests** en `tests/e2e/test_performance_e2e.py` con flujos completos contra navegador real — ciclo completo (enable → get_metrics → set_time_domain → get_metrics → disable), navegar a página con JS pesado → get_metrics → verificar métricas no vacías con `JSHeapUsedSize`, set_time_domain antes y después de enable (después → CommandError), get_metrics múltiples veces (verificar valores cambian), raw send para los 4 comandos, set_time_domain valor inválido (ValueError), todos los métodos retornan dict, enable con `time_domain` `"timeTicks"`/`"threadTicks"`, repeated enable/disable 3x, enable twice, disable without enable, get_metrics without enable, metrics have `name` and `value` with type checking, metrics include `JSHeapUsedSize` and `Nodes`, concurrent enable + get_metrics, full lifecycle with navigation (enable → get_metrics → heavy JS → get_metrics → disable), set_time_domain `"threadTicks"` before enable, get_metrics after disable, TypeError para set_time_domain (None/int/list) y enable (int/list/bool), enable(None) no eleva error, enable valor inválido (ValueError), set_time_domain string vacío (ValueError), heap grows after heavy JS, JSHeapUsedSize positive, Nodes positive, repeated enable 5x, repeated disable 5x, enable then set_time_domain errors.

### Quality checks

- `ruff check`: ✅
- `mypy --strict`: ✅ (sin errores en archivos de Performance)
- `pytest -m unit`: 142/142 passed

### Total: 142 unit tests + 49 integration tests + 54 E2E tests = 245 tests para el dominio Performance.

---

## Security

- **Archivo**: `cdpwave/domains/security.py`
- **Spec CDP**: https://chromedevtools.github.io/devtools-protocol/tot/Security/
- **Go source**: `go-rod/rod/lib/proto/security.go`
- **Métodos CDP (6)**: `disable`, `enable`, `setIgnoreCertificateErrors`, `handleCertificateError`, `setOverrideCertificateErrors`, `getVisibleSecurityState`.
- **Métodos implementados (6)**: `disable`, `enable`, `set_ignore_certificate_errors`, `handle_certificate_error`, `set_override_certificate_errors`, `get_visible_security_state`.
- **Paridad**: 6/6 métodos CDP implementados. 0 faltantes. 0 extra.

### Bugs encontrados y corregidos

- **Bug #1 — `set_ignore_certificate_errors` era un alias incorrecto**: El método era `set_ignore_certificate_errors = set_override_certificate_errors`, lo que enviaba `Security.setOverrideCertificateErrors` con parámetro `override` en vez de `Security.setIgnoreCertificateErrors` con parámetro `ignore`. Go source confirma que son comandos CDP distintos con parámetros distintos. **Corregido**: reemplazado el alias por un método propio que envía `Security.setIgnoreCertificateErrors` con `{"ignore": ignore}`.
- **Bug #2 — `handle_certificate_error` sin validación de tipo para `event_id`**: Aceptaba cualquier tipo (str, float, bool, None, list, dict) y lo enviaba al CDP como JSON inválido. Go source usa `EventID int json:"eventId"` (tipo int). **Corregido**: añadido `isinstance(event_id, int)` check (con exclusión de `bool` pues `bool` es subtipo de `int` en Python) que eleva `TypeError` antes de enviar al CDP.
- **Bug #3 — `handle_certificate_error` sin validación de tipo para `action`**: Aceptaba cualquier tipo (int, None, bool, list, dict, float, bytes). Go source usa `Action SecurityCertificateErrorAction` (tipo enum string). **Corregido**: añadido `isinstance(action, str)` check que eleva `TypeError`.
- **Bug #4 — `handle_certificate_error` sin validación de enum para `action`**: Aceptaba cualquier string, incluyendo valores fuera del enum. Go source define `SecurityCertificateErrorActionContinue = "continue"` y `SecurityCertificateErrorActionCancel = "cancel"`. **Corregido**: añadido `ValueError` check que rechaza strings fuera del enum. TypeError (tipo incorrecto) toma precedencia sobre ValueError (valor inválido).
- **Bug #5 — `set_override_certificate_errors` sin validación de tipo para `override`**: Aceptaba cualquier tipo (int, str, None, float, list, dict). Go source usa `Override bool json:"override"` (tipo bool). **Corregido**: añadido `isinstance(override, bool)` check que eleva `TypeError`.
- **Bug #6 — `set_ignore_certificate_errors` sin validación de tipo para `ignore`**: (Nuevo método) Go source usa `Ignore bool json:"ignore"` (tipo bool). **Corregido**: añadido `isinstance(ignore, bool)` check que eleva `TypeError`.
- **Bug #7 — Docstrings no coincidían con CDP spec**: `enable` decía "Activates Security domain events and reporting" → "Enables tracking security state changes" (Go source). `disable` decía "Deactivates Security domain events and reporting" → "Disables tracking security state changes" (Go source). `handle_certificate_error` no mencionaba deprecación. `set_override_certificate_errors` no mencionaba deprecación ni relación con `handleCertificateError`. `get_visible_security_state` no mencionaba que es experimental. **Corregido**: todas las docstrings alineadas con Go source y CDP spec.
- **Bug #8 — Module docstring no mencionaba eventos**: La spec CDP define 3 eventos para Security: `Security.certificateError` (deprecated), `Security.securityStateChanged` (deprecated, no longer sent), `Security.visibleSecurityStateChanged` (experimental). **Corregido**: añadida documentación de los 3 eventos con parámetros en el module docstring.
- **Bug #9 — Class docstring no documentaba eventos**: **Corregido**: añadidos los 3 eventos con parámetros y tipos en el class docstring.
- **Bug #10 — Orden de métodos no alfabético**: Orden era `enable, disable, handle_certificate_error, set_override_certificate_errors, get_visible_security_state`. **Corregido**: reordenado a `disable, enable, set_ignore_certificate_errors, handle_certificate_error, set_override_certificate_errors, get_visible_security_state` (alfabético, coincide con Go source).
- **Bug #11 — `client.py` docstring del property `security` inexacta**: Decía "certificate error handling" → "tracking security state changes" (coincide con Go source). **Corregido**.

### Tipos verificados contra Go source

- `SecurityCertificateErrorAction` enum: `"continue"`, `"cancel"` — cdpwave valida estos valores con `ValueError`.
- `SecuritySetIgnoreCertificateErrors.Ignore`: `bool json:"ignore"` (sin omitempty) — cdpwave valida `isinstance(ignore, bool)` y siempre envía `{"ignore": ignore}`.
- `SecurityHandleCertificateError.EventID`: `int json:"eventId"` (sin omitempty) — cdpwave valida `isinstance(event_id, int)` (excluyendo `bool`) y siempre envía `{"eventId": event_id}`.
- `SecurityHandleCertificateError.Action`: `SecurityCertificateErrorAction json:"action"` (sin omitempty) — cdpwave valida `isinstance(action, str)` + enum value, siempre envía `{"action": action}`.
- `SecuritySetOverrideCertificateErrors.Override`: `bool json:"override"` (sin omitempty) — cdpwave valida `isinstance(override, bool)` y siempre envía `{"override": override}`.
- `SecurityDisable`, `SecurityEnable`: sin parámetros — cdpwave envía `None` (no dict vacío).
- `SecurityGetVisibleSecurityStateResult`: `VisibleSecurityState *SecurityVisibleSecurityState json:"visibleSecurityState"` — cdpwave retorna dict con `visibleSecurityState`.
- `SecurityVisibleSecurityState`: `SecurityState` (enum), `CertificateSecurityState` (optional), `SafetyTipInfo` (optional), `SecurityStateIssueIDs []string` — cdpwave documenta todos los campos en la docstring.

### Eventos del dominio Security

- `Security.certificateError` (deprecated): There is a certificate error. Params: `eventId` (int), `errorType` (str), `requestURL` (str).
- `Security.securityStateChanged` (deprecated, no longer sent): The security state of the page changed. Params: `securityState` (SecurityState), `schemeIsCryptographic` (bool), `explanations` (list[SecurityStateExplanation]), `mixedContentStatus` (InsecureContentStatus), `summary` (str, optional).
- `Security.visibleSecurityStateChanged` (experimental): The security state of the page changed. Params: `visibleSecurityState` (VisibleSecurityState).

### Tests unitarios

- **224 tests** en `tests/unit/domains/test_security.py` con FakeSender — cubriendo los 6 métodos:
  - `disable`: params `None`, returns empty/response, exact CDP method name, single call, sends `None` not empty dict.
  - `enable`: params `None`, returns empty/response, exact CDP method name, single call, sends `None` not empty dict.
  - `set_ignore_certificate_errors`: params `True`/`False`, returns empty/response, exact CDP method name, single call, only key in params, camelCase key, new dict each call.
  - `handle_certificate_error`: params `continue`/`cancel`, event_id 0/negative/large, returns empty/response, exact CDP method name, single call, only keys in params, camelCase keys, new dict each call.
  - `set_override_certificate_errors`: params `True`/`False`, returns empty/response, exact CDP method name, single call, only key in params, camelCase key, new dict each call.
  - `get_visible_security_state`: params `None`, returns visibleSecurityState (full/minimal/empty/extra keys), exact CDP method name, single call, sends `None`, safety tip info, all security state enums (6 values).
  - Type validation `set_ignore_certificate_errors`: TypeError for int/zero-int/str/None/float/list/dict (7 tests) + bytes/bytearray/tuple/set/frozenset/complex/range (7 exotic tests), no sender call on error.
  - Type validation `handle_certificate_error` event_id: TypeError for None/str/float/bool/False/list/dict (7 tests) + bytes/bytearray/tuple/set/frozenset/complex/range (7 exotic tests), no sender call on error.
  - Type validation `handle_certificate_error` action: TypeError for int/None/bool/list/dict/float/bytes (7 tests) + bytearray/tuple/set/frozenset/complex/range (6 exotic tests), no sender call on error.
  - Enum validation `handle_certificate_error` action: ValueError for empty string/uppercase continue/uppercase cancel/random string/whitespace/continue with spaces/long string/unicode (8 tests) + newline/tab/null-byte/single-letter/Title-Case/ALL-CAPS (8 boundary tests), no sender call on error. TypeError takes precedence over ValueError (2 tests).
  - Type validation `set_override_certificate_errors`: TypeError for int/zero-int/str/None/float/list/dict (7 tests) + bytes/bytearray/tuple/set/frozenset/complex/range (7 exotic tests), no sender call on error.
  - Validation order: event_id checked before action type, event_id before action enum, action type before enum, bool event_id rejected (6 tests).
  - Value identity: bool identity preserved (True/False), int identity preserved, negative int, maxsize int, str identity (8 tests).
  - Response content: certificateSecurityState with full fields, safetyTipInfo lookalike/badReputation, empty/many issue IDs, no certificate/safetyTip state, exact response object (9 tests).
  - Concurrent validation: valid+invalid mixed, handle_cert mixed validity, all valid different params (3 tests).
  - Method parity: 6 methods exist, no extra methods, all coroutines, `isinstance(BaseDomain)`, alphabetical order, no alias attribute, `set_ignore_certificate_errors` is distinct method from `set_override_certificate_errors`.
  - Method signatures: all 6 methods with correct params, annotations, return types, docstrings. Class and module docstrings mention events. `handle_certificate_error` and `set_override_certificate_errors` docstrings mention deprecated. `get_visible_security_state` docstring mentions experimental.
  - Error propagation: `CommandError` for each of the 6 methods, error sender records call before raising, error stops execution, positive/zero error codes, empty/long/unicode error messages, code+message preservation.
  - Concurrency: 100 concurrent for each method, concurrent mixed 6 methods, 50 enable + 50 disable, concurrent with params all verified.
  - Repetition: enable/disable 10x, repeated enable 10x, repeated set_ignore 10x, repeated handle_certificate_error 10x, repeated get_visible_security_state 10x.
  - Call sequences: full lifecycle (6 calls), all methods use `Security.` prefix, interleaved calls (8 calls).
  - Edge cases: `set_response` between calls, large response dict (100 keys), None response from sender, mixed error/success, exact response object, params not mutated between calls, custom sender compatibility, extra keys in all 6 method responses, safety tip info, all security state enums, TypeError not swallowed, ValueError not swallowed.

### Tests de integración

- **60+ tests** en `tests/integration/test_security.py` con navegador real Edge headless — enable/disable (con return values), set_ignore_certificate_errors `True`/`False`/toggle, set_override_certificate_errors `True`/`False`/toggle, handle_certificate_error `continue`/`cancel`, get_visible_security_state (verificar `visibleSecurityState`, `securityState` enum válido, `securityStateIssueIds`), eventos `visibleSecurityStateChanged` (verificar params y no events after disable), raw send para los 6 comandos, all methods return dict, full lifecycle, lifecycle with navigation, **sin enable previo** (4 tests), **about:blank** state, **HTTP page** state, **HTTPS certificate state** fields, **state changes between navigations**, **combined operations** (ignore+override, override+handle, large/negative event_id, multiple enable/disable cycles), **raw send extended** (handleCertificateError, setOverrideCertificateErrors).

### E2E tests

- **80+ tests** en `tests/e2e/test_security_e2e.py` con flujos completos contra navegador real Edge headless — enable/disable (con return values y ciclos), set_ignore_certificate_errors `True`/`False`/toggle, set_override_certificate_errors `True`/`False`/toggle, handle_certificate_error `continue`/`cancel` (con suppress para errores esperados), validación TypeError/ValueError en cliente, get_visible_security_state (verificar `visibleSecurityState`, `securityState` enum, `certificateSecurityState` en HTTPS), eventos `visibleSecurityStateChanged` (verificar params y no events after disable), raw send para los 6 comandos, all methods return dict, full lifecycle, lifecycle with navigation, lifecycle multiple navigations, distinct methods verification, **HTTP page security state**, **about:blank state**, **HTTP→HTTPS state change**, **HTTPS→HTTP state change**, **multiple navigations state always valid**, **event details** (securityState + securityStateIssueIds on HTTPS/HTTP/about:blank), **combined flows** (enable+ignore+override+get+disable, repeated lifecycle 3x with navigation, true/false/true sequences, continue+cancel), **validation extended** (None/float/list event_id, None/list action, None/float/int override, None/int ignore, empty action ValueError), **distinct methods extended** (ignore≠override, both in sequence).

### Tests actualizados en otros archivos

- `test_debugger_overlay_security_audits.py`: tests existentes siguen funcionando (enable/disable y set_override_certificate_errors sin cambios en la API).

### Quality checks

- `ruff check`: ✅
- `mypy --strict`: ✅ (sin errores en `cdpwave/domains/security.py`)
- `pytest -m unit`: 224/224 passed

### Total: 224 unit tests + 60+ integration tests + 80+ E2E tests = 364+ tests para el dominio Security.


### DOMSnapshot (revisado contra Go source cdproto)

- **4 comandos CDP** en Go source, **4 métodos** en cdpwave (0 extra, 0 faltantes).
- **3 bugs encontrados y corregidos**:
  1. `capture_snapshot`: `computed_styles` era opcional (`list[str] | None = None`) pero el CDP spec lo marca como requerido. Cambiado a parámetro requerido (`list[str]`).
  2. `capture_snapshot`: los 4 bools (`include_paint_order`, `include_dom_rects`, `include_blended_background_colors`, `include_text_color_opacities`) eran `bool | None = None` (condicional, se omitían si `None`). Go source `CaptureSnapshotParams` no tiene `omitempty` en ninguno — siempre se serializan. Cambiados a `bool = False` (siempre enviados).
  3. Module y class docstrings no mencionaban "Experimental" — todo el dominio DOMSnapshot es experimental en CDP. Añadida la etiqueta.
- **Verificación contra Go source** (`domsnapshot/domsnapshot.go` y `types.go`):
  - `CaptureSnapshotParams`: `ComputedStyles` (sin omitempty, requerido), `IncludePaintOrder`/`IncludeDOMRects`/`IncludeBlendedBackgroundColors`/`IncludeTextColorOpacities` (bool sin omitempty, siempre enviados).
  - `getSnapshot` no existe en Go source (completamente removido/deprecated). Se mantiene por compatibilidad con CDP spec TypeScript.
  - `GetSnapshotRequest` (TypeScript spec): bools son `?` (opcionales) — `bool | None = None` es correcto.
  - No hay eventos en DOMSnapshot (verificado en TypeScript spec y Go source).
- **Docstrings**: module y class mencionan "Experimental". `capture_snapshot` marca `include_blended_background_colors` e `include_text_color_opacities` como "Experimental". `get_snapshot` marcado como "Deprecated".
- **Métodos en orden alfabético**: `capture_snapshot`, `disable`, `enable`, `get_snapshot`.
- **Tests unitarios**: **82 tests** en `tests/unit/domains/test_dom_snapshot.py` con FakeSender — parameter verification, type validation (TypeError para str/int/dict/tuple/None en computed_styles, str/int en bools), bool sending semantics (always-sent para capture_snapshot, conditional para get_snapshot), camelCase keys, return values, CommandError propagation, method parity, coroutine checks, concurrency, repetition, docstring checks (Experimental/Deprecated), edge cases (empty list, large list, int 0/1 rejected as bool, dict/tuple rejected as list, bool overrides default).
- **Tests de integración**: **30+ tests** en `tests/integration/test_dom_snapshot.py` con navegador real Edge headless — enable/disable (con return values), capture_snapshot con defaults/styles/paint_order/dom_rects/all_params/empty/about_blank/repeated/bool_false/response_types, get_snapshot (deprecated, con suppress), type validation (7 tests para capture_snapshot, 6 tests para get_snapshot).
- **E2E tests**: **45+ tests** en `tests/e2e/test_dom_snapshot_e2e.py` con flujos completos — lifecycle (enable/disable, repeated cycles, return values), capture_snapshot (after navigate, paint_order, dom_rects, all_params, empty_styles, repeated, about_blank, bool_false, deep_response_structure, strings_are_strings), get_snapshot (deprecated, all_params, bool_false, empty_whitelist), type validation (12 tests), full flow (enable→navigate→capture→disable, capture_without_enable, multiple captures, all bools true/false, get_snapshot lifecycle).
- **Quality checks**: `ruff check` ✅, `pytest -m unit` 82/82 passed.
- **Total: 82 unit tests + 30+ integration tests + 45+ E2E tests = 157+ tests** para el dominio DOMSnapshot.

## Overlay

**Revisión completa contra Go source `chromedp/cdproto/overlay/overlay.go` y `types.go`.**

### Bugs encontrados y corregidos

1. **`highlight_frame`** — método presente en cdpwave pero **no existe en el Go source ni en el CDP spec**. Eliminado.
2. **`set_show_hit_test_borders`** — método presente en cdpwave pero **no existe en el Go source ni en el CDP spec**. Eliminado.
3. **`set_show_window_controls`** → renombrado a **`set_show_window_controls_overlay`** para coincidir con el comando CDP `Overlay.setShowWindowControlsOverlay`. El parámetro `windowControls` fue corregido a `windowControlsOverlayConfig`. El parámetro cambió de required a optional (con `params or None`).
4. **`highlight_node`** — `highlight_config` era `Optional` en Python pero es **required** en Go. Corregido a required.
5. **`highlight_rect`** — `x`, `y`, `width`, `height` eran `float` pero Go usa `int`. Corregido a `int`.
6. **`get_highlight_object_for_test`** — `include_distance` e `include_style` eran `Optional[bool]` pero Go tiene `bool` con default `false`. `show_accessibility_info` era `Optional[bool]` pero Go tiene `bool` con default `true`. Corregidos a `bool = False` y `bool = True` respectivamente.
7. **`set_show_web_vitals`** — `layered` era `Optional[bool]` pero Go tiene `bool` con default `false`. Corregido a `bool = False`.
8. **`set_show_hinge`** — parámetro renombrado de `hinge` a `hinge_config` para coincidir con el key CDP `hingeConfig`.
9. **`set_paused_in_debugger_message`** — no usaba el patrón `params or None`. Corregido: cuando `message` es `None`, envía `None` en lugar de `{}`.
10. **`set_show_display_cutout`** — no usaba el patrón `params or None`. Corregido: cuando `display_cutout_config` es `None`, envía `None`.
11. **`set_show_window_controls_overlay`** — no usaba el patrón `params or None`. Corregido: cuando `window_controls_overlay_config` es `None`, envía `None`.
12. **Falta de validación `isinstance`** — ningún método tenía validación de tipos. Agregado `isinstance` con `TypeError` descriptivo para todos los parámetros en todos los métodos.
13. **Métodos no en orden alfabético** — reordenados alfabéticamente.
14. **Docstrings** — agregadas marcas **Experimental** en docstring del módulo y clase. Agregados eventos (`inspectNodeRequested`, `nodeHighlightRequested`, `inspectModeCanceled`).
15. **Métodos faltantes agregados**: `get_grid_highlight_objects_for_test`, `get_highlight_object_for_test`, `get_source_order_highlight_object_for_test`, `highlight_source_order`, `set_show_ad_highlights`, `set_show_container_query_overlays`, `set_show_display_cutout`, `set_show_flex_overlays`, `set_show_grid_overlays`, `set_show_inspected_element_anchor`, `set_show_layout_shift_regions`, `set_show_scroll_snap_overlays`.

### Segunda revisión — bugs adicionales encontrados y corregidos

16. **`set_show_web_vitals`** — método mantenido en primera revisión pero **no existe en Go source** y está marcado **Deprecated** en CDP spec ("Deprecated, no longer has any effect"). Eliminado.
17. **`set_paused_in_debugger_message`** — string vacío `""` se enviaba como `{"message": ""}` pero Go usa `omitempty,omitzero` que omite strings vacíos. Corregido: `""` ahora se omite y envía `None`.
18. **`get_highlight_object_for_test`** — `color_format=""` se enviaba como `{"colorFormat": ""}` pero Go usa `omitempty,omitzero`. Corregido: string vacío ahora se omite.
19. **`highlight_rect`** — docstring no mencionaba el issue de DPR (device pixel ratio) documentado en Go source. Agregado note sobre crbug.com/437807128.

### Tercera revisión — bugs adicionales encontrados y corregidos

20. **`highlight_node`** — `selector=""` se enviaba como `{"selector": ""}` pero Go usa `omitempty,omitzero`. Corregido: string vacío ahora se omite.
21. **`highlight_node`** — `object_id=""` se enviaba como `{"objectId": ""}` pero Go usa `omitempty,omitzero`. Corregido: string vacío ahora se omite.
22. **`highlight_source_order`** — `object_id=""` se enviaba como `{"objectId": ""}` pero Go usa `omitempty,omitzero`. Corregido: string vacío ahora se omite.
23. **Class docstring** — mencionaba "Web Vitals" pero `set_show_web_vitals` fue eliminado. Corregido.

### Resumen: 28 métodos implementados, 3 removidos (deprecated), 0 faltantes, 0 extra

### Tests unitarios

- **118 tests** en `tests/unit/domains/test_overlay.py` con FakeSender — parameter verification para los 28 métodos, type validation (TypeError para str/int/dict/list/None en todos los params), bool sending semantics (True/False), camelCase keys, return values, CommandError propagation, method parity (28 methods, 4 removed methods verified absent, renamed method exists, inherits BaseDomain, all coroutines), concurrent calls, empty string omitempty edge cases.
- Tests actualizados en `test_tier3b_domains.py`, `test_coverage_gaps.py`, `test_expanded_methods.py`.

### Tests de integración

- **40+ tests** en `tests/integration/test_debugger_overlay_security_audits.py` — todos los métodos con navegador real, edge cases (enable twice, disable without enable, type error on bad param, full lifecycle).

### E2E tests

- **60+ tests** en `tests/e2e/test_overlay_e2e.py` con flujos completos contra navegador real Edge headless — lifecycle, show toggles, highlights, inspect mode, overlays, test methods, debugger message, type validation (5 tests), full flow, raw send.

### Quality checks

- `ruff check` ✅
- `pytest -m unit` 118/118 passed (test_overlay.py) + 67/67 passed (test_tier3b_domains.py)
- **Total: 118 unit tests + 40+ integration tests + 60+ E2E tests = 218+ tests** para el dominio Overlay.

### PerformanceTimeline (revisado contra Go source cdproto)

- **1 comando CDP** en Go source, **1 método** en cdpwave (0 extra, 0 faltantes).
- **Dominio experimental** (marcado en CDP doc).
- **7 bugs encontrados y corregidos en primera revisión**:
  - `enable`: tipo de `event_types` cambiado de `list[dict[str, Any]]` a `list[str]` (Go source `EventTypes []string`, CDP doc `array of string`). Antes aceptaba dicts con `name`/`eventCategory` que no existen en CDP.
  - `enable`: docstring corregido — removida descripción incorrecta "List of event type filters, each with `name` and optional `eventCategory`". Ahora describe correctamente como lista de strings de tipos de evento (e.g. `"largest-contentful-paint"`, `"layout-shift"`).
  - `enable`: añadido `isinstance` type validation para `event_types` (list) y cada elemento (str) con `TypeError` descriptivo.
  - `enable`: añadido docstring de return "Empty dict (no return value from CDP)" (Go source `Do` retorna solo `err`, sin return value).
  - `enable`: añadido nota "Previously buffered events are reported before the method returns" (Go source docstring exacto).
  - Class docstring: corregido nombre de evento `timelineEvent` → `timelineEventAdded` (Go source `events.go` y CDP doc confirman `PerformanceTimeline.timelineEventAdded`).
  - Class docstring: añadida marca **Experimental** y documentación del evento `timelineEventAdded`.
- **2 bugs encontrados y corregidos en segunda revisión**:
  - Class docstring: corregida estructura del evento `timelineEventAdded` — el evento tiene un único parámetro `event` (dict) que contiene un `TimelineEvent`, no parámetros directos (`frameId`, `type`, etc.). Coincide con Go source `EventTimelineEventAdded struct { Event *TimelineEvent json:"event" }`.
  - `enable` docstring: añadida nota faltante "Note that not all types exposed to the web platform are currently supported" (Go source comment exacto).
- **Tests unitarios**: **13 tests** en total (`test_tier3j_domains.py` + `test_p2_features.py`) con FakeSender — cubriendo command name, JSON key camelCase, múltiples event types, empty list (disable recording), type validation (not list, not str element, dict element).
- **Tests de integración**: **2 tests** en `test_heapprofiler_layertree_performancetimeline.py` con navegador real — domain accessible, enable con event types + disable con empty list.
- **Total: 13 unit tests + 2 integration tests = 15 tests** para el dominio PerformanceTimeline.

### FileSystem (revisado contra Go source cdproto)

- **1 comando CDP** en Go source, **1 método** en cdpwave (0 extra, 0 faltantes).
- **Dominio experimental** (marcado en CDP doc).
- **5 bugs encontrados y corregidos**:
  - `get_directory`: faltaba parámetro requerido `bucket_file_system_locator` (Go source `GetDirectoryParams.BucketFileSystemLocator`). Ahora acepta `storage_key` (str, required), `path_components` (list[str], required), `bucket_name` (str, optional con omitempty — string vacío se omite, coincide con Go source `BucketName string json:"bucketName,omitempty,omitzero"`). Antes no tomaba parámetros y enviaba `None`.
  - `get_directory`: docstring corregido — return es `directory` únicamente (Go source `GetDirectoryReturns.Directory`), no `directory` + `token` (token no existe en Go source ni CDP spec).
  - `get_directory`: añadida validación `isinstance` con `TypeError` descriptivo para `storage_key` (str), `path_components` (list[str], cada elemento str), `bucket_name` (str).
  - Class docstring: añadida marca **Experimental**.
  - Module docstring: añadidos tipos `BucketFileSystemLocator`, `Directory`, `File` con sus campos y tipos (verificado contra Go source `types.go`).
- **Tests unitarios**: **7 tests** en `test_p2_features.py` con FakeSender — cubriendo command name, JSON key `bucketFileSystemLocator` con `storageKey`/`pathComponents`, `bucketName` presente cuando se pasa, `bucketName` omitido cuando es string vacío (omitempty), type validation (storage_key no str, path_components no list, elemento no str, bucket_name no str).
- **Tests de integración**: **1 test** en `test_missing_domains.py` con navegador real — `get_directory` con `storage_key` y `path_components` (skip si no disponible).
- **Total: 7 unit tests + 1 integration test = 8 tests** para el dominio FileSystem.

### Profiler (revisado contra Go source cdproto)

- **9 comandos CDP** en Go source, **9 métodos** en cdpwave (0 extra, 0 faltantes).
- **0 métodos deprecados** (ninguno marcado como Deprecated en Go source ni CDP spec).
- **5 bugs encontrados y corregidos**:
  - Métodos reordenados alfabéticamente para coincidir con Go source: `disable` → `enable` → `get_best_effort_coverage` → `set_sampling_interval` → `start` → `start_precise_coverage` → `stop` → `stop_precise_coverage` → `take_precise_coverage` (antes era `enable` → `disable` → `start` → `stop` → `start_precise_coverage` → `stop_precise_coverage` → `take_precise_coverage` → `get_best_effort_coverage` → `set_sampling_interval`).
  - `start`: docstring corregido — return es "Empty dict (no return value from CDP)" (Go source `StartParams.Do` retorna solo `err`, sin return value). Antes decía "Dict containing the profiling `timestamp`" — incorrecto, `Profiler.start` no retorna timestamp.
  - `stop_precise_coverage`: docstring corregido — return es "Empty dict (no return value from CDP)" (Go source `StopPreciseCoverageParams.Do` retorna solo `err`). Antes decía "Dict with the `timestamp` of coverage stop" — incorrecto.
  - `take_precise_coverage`: docstring corregido — return ahora documenta `timestamp` además de `result` (Go source `TakePreciseCoverageReturns` tiene `Result []*ScriptCoverage` y `Timestamp float64`). Antes solo documentaba `result`.
  - `set_sampling_interval`: añadida validación `isinstance` con `TypeError` descriptivo para `interval` (int). Añadido docstring "Must be called before CPU profiles recording started" (Go source exacto).
  - `start_precise_coverage`: añadida validación `isinstance` con `TypeError` descriptivo para `call_count` (bool), `detailed` (bool), `allow_triggered_updates` (bool). Docstrings ampliados con descripciones exactas de Go source.
  - `get_best_effort_coverage`: docstring añadido "The coverage data may be incomplete due to garbage collection" (Go source exacto).
  - `stop_precise_coverage`: docstring añadido "Disabling releases unnecessary execution count records and allows executing optimized code" (Go source exacto).
  - Class docstring: añadidos eventos `Profiler.consoleProfileFinished` (Params: `id`, `location`, `profile`, `title` optional) y `Profiler.preciseCoverageDeltaUpdate` (Params: `result`, `timestamp`).
  - Module docstring: añadidos eventos con sus parámetros.
  - `enable`/`disable`: docstrings corregidos — return "Empty dict (no return value from CDP)" (Go source no retorna valores).
- **Bools sin omitempty**: `start_precise_coverage` envía `callCount`, `detailed`, `allowTriggeredUpdates` siempre (Go source `bool` sin `omitempty`). Correcto en implementación anterior, mantenido.
- **Tests unitarios**: **14 tests** en `test_tier3_domains.py` con FakeSender — cubriendo todos los 9 métodos, bool defaults (`False`), bool con `True`, type validation (`interval` no int, `call_count`/`detailed`/`allow_triggered_updates` no bool), return values (`start` retorna `{}`, `take_precise_coverage` retorna `result` + `timestamp`), orden alfabético verificado.
- **Tests de integración**: **5 tests** en `test_performance_profiler.py` con navegador real — enable/disable, start/stop profile con verificación de `profile.nodes`, precise coverage con `call_count` + `detailed`, best effort coverage, set_sampling_interval.
- **Total: 14 unit tests + 5 integration tests = 19 tests** para el dominio Profiler.

### Segunda revisión — bugs adicionales encontrados y corregidos

#### Profiler

6. **`set_sampling_interval` bool-as-int bug**: `isinstance(True, int)` retorna `True` en Python porque `bool` es subclase de `int`. Esto permitía `set_sampling_interval(True)` que enviaría `{"interval": true}` (JSON boolean) en lugar de un entero. Corregido: añadido `isinstance(interval, bool)` check que rechaza bools explícitamente.

#### FileSystem

Sin bugs adicionales en segunda revisión. La implementación de `get_directory` con `bucket_file_system_locator`, `storage_key`, `path_components`, `bucket_name` (omitempty) y validación de tipos es correcta.

### Tests adicionales — segunda revisión

#### FileSystem — unit tests edge (7 → 16 tests)

- `test_get_directory_empty_path_components`: lista vacía se envía correctamente.
- `test_get_directory_empty_storage_key`: string vacío se envía como `storageKey: ""`.
- `test_get_directory_multiple_path_components`: múltiples componentes de path.
- `test_get_directory_return_value`: verificación del dict retornado con `directory`.
- `test_get_directory_only_bucket_locator_key`: params solo contiene `bucketFileSystemLocator`.
- `test_get_directory_locator_keys`: keys del locator con bucket_name = `{storageKey, pathComponents, bucketName}`.
- `test_get_directory_locator_keys_without_bucket`: keys sin bucket_name = `{storageKey, pathComponents}`.
- `test_get_directory_bool_as_storage_key`: `True` como storage_key rechazado (bool no es str).
- `test_get_directory_none_as_path_components`: `None` como path_components rechazado.

#### Profiler — unit tests edge (14 → 29 tests)

- `test_set_sampling_interval_bool_true_rejected`: `True` rechazado por bool-as-int guard.
- `test_set_sampling_interval_bool_false_rejected`: `False` rechazado por bool-as-int guard.
- `test_set_sampling_interval_zero`: interval=0 se envía correctamente.
- `test_set_sampling_interval_negative`: interval=-100 se envía correctamente.
- `test_set_sampling_interval_large`: interval=2^31-1 (int64 max) se envía correctamente.
- `test_enable_returns_empty_dict`: enable retorna `{}`.
- `test_disable_returns_empty_dict`: disable retorna `{}`.
- `test_start_returns_empty_dict`: start retorna `{}`.
- `test_stop_precise_coverage_returns_empty_dict`: stop_precise_coverage retorna `{}`.
- `test_stop_profile_structure`: verificación completa de estructura de `profile` (nodes, startTime, endTime, samples, timeDeltas).
- `test_start_precise_coverage_returns_timestamp`: verificación de `timestamp` en return.
- `test_take_precise_coverage_returns_timestamp`: verificación de `timestamp` + `result` con scriptId.
- `test_get_best_effort_coverage_returns_result`: verificación de `result` con url.
- `test_all_methods_are_coroutines`: los 9 métodos son coroutines.
- `test_method_count`: exactamente 9 métodos públicos.
- `test_inherits_base_domain`: hereda de BaseDomain.

#### Profiler — integration tests edge (5 → 18 tests)

- `test_enable_twice`: enable doble no falla.
- `test_disable_without_enable`: disable sin enable no falla.
- `test_stop_without_start_raises`: stop sin start lanza CommandError.
- `test_start_precise_coverage_default_flags`: flags por defecto retorna timestamp.
- `test_start_precise_coverage_allow_triggered_updates`: allow_triggered_updates=True.
- `test_take_precise_coverage_returns_timestamp`: timestamp presente y es numérico.
- `test_precise_coverage_with_detailed`: estructura completa de coverage con `functionName`, `ranges`, `isBlockCoverage`.
- `test_set_sampling_interval_type_error`: TypeError con str y bool en navegador real.
- `test_start_precise_coverage_type_error`: TypeError con str e int en navegador real.
- `test_full_profile_lifecycle`: ciclo completo con set_sampling_interval + start + JS + stop + verificación startTime ≤ endTime.
- `test_coverage_reset_on_take`: double take_precise_coverage (counters reset).
- `test_best_effort_coverage_structure`: estructura de result con list.

#### E2E tests (nuevos)

- **`test_profiler_filesystem_e2e.py`** con **30 tests E2E** contra navegador real Edge headless:
  - **TestProfilerE2E** (20 tests): full profile lifecycle, precise coverage full flow, best effort coverage, coverage reset on double take, enable/disable cycle, stop without start raises, set_sampling_interval before start, 5 type validation tests (str/bool/int/allow_triggered), raw send, all methods coroutines, method count, inherits BaseDomain, domain accessible, allow_triggered_updates flow.
  - **TestFileSystemE2E** (10 tests): domain accessible, get_directory with params, get_directory with bucket_name, 4 type validation tests (storage_key, path_components, element, bucket_name), inherits BaseDomain, all methods coroutines, method count, raw send.

### Resumen final actualizado

- **FileSystem**: 16 unit tests + 1 integration test + 10 E2E tests = **27 tests**.
- **Profiler**: 29 unit tests + 18 integration tests + 20 E2E tests = **67 tests**.
- **Total combinado**: 45 unit tests + 19 integration tests + 30 E2E tests = **94 tests**.
- `ruff check` ✅ en todos los archivos modificados.
- `pytest -m unit` ✅ — 2534 passed (2 fallos preexistentes CSS/WebAuthn no relacionados).

### Tercera revisión — bugs adicionales encontrados y corregidos

#### Profiler

7. **Falta evento `Profiler.consoleProfileStarted`**: Go source define `EventConsoleProfileStarted` con `id` (str), `location` (Location), `title` (str, optional con `omitempty,omitzero`). No estaba documentado en module docstring ni class docstring. Corregido: añadido a ambos.

8. **Falta campo `occasion` en `Profiler.preciseCoverageDeltaUpdate`**: Go source define `Occasion string json:"occasion"` — "Identifier for distinguishing coverage events." Nuestra documentación solo listaba `result` y `timestamp`, omitiendo `occasion`. Corregido: añadido `occasion` (str) a module y class docstring. También añadida marca **Experimental** al evento (CDP doc lo marca como Experimental).

#### FileSystem

Sin bugs adicionales en tercera revisión. Verificado contra Go source `types.go`:
- `Directory.NestedDirectories` es `[]string` (no `[]Directory`) — correcto en nuestra documentación.
- `File.LastModified` es `*cdp.TimeSinceEpoch` (float) — correcto.
- `BucketFileSystemLocator.StorageKey` es `storage.SerializedStorageKey` (string) — correcto.

### Tests adicionales — tercera revisión

#### Profiler — unit tests event documentation (29 → 36 tests)

- `test_module_docstring_documents_console_profile_finished`: verifica que module docstring documenta `consoleProfileFinished` con `id`, `location`, `profile`, `title`.
- `test_module_docstring_documents_console_profile_started`: verifica que module docstring documenta `consoleProfileStarted` y menciona `console.profile()`.
- `test_module_docstring_documents_precise_coverage_delta_update`: verifica que module docstring documenta `preciseCoverageDeltaUpdate` con `occasion`, `timestamp`, `result`.
- `test_class_docstring_documents_all_three_events`: verifica que class docstring documenta los 3 eventos.
- `test_class_docstring_precise_coverage_delta_update_has_occasion`: verifica que class docstring incluye `occasion`.
- `test_class_docstring_precise_coverage_delta_update_marked_experimental`: verifica que el segmento del evento tiene marca **Experimental**.

### Resumen final actualizado (tercera revisión)

- **FileSystem**: 16 unit tests + 1 integration test + 10 E2E tests = **27 tests**.
- **Profiler**: 36 unit tests + 18 integration tests + 20 E2E tests = **74 tests**.
- **Total combinado**: 52 unit tests + 19 integration tests + 30 E2E tests = **101 tests**.
- `ruff check` ✅ en todos los archivos modificados.
- `pytest -m unit` ✅ — 36/36 Profiler tests passed.

### HeapProfiler (revisado contra Go source cdproto)

- **12 comandos CDP** en Go source, **12 métodos** en cdpwave (0 extra, 0 faltantes).
- **0 métodos deprecados** (ninguno marcado como Deprecated en Go source ni CDP spec).
- **Dominio experimental** (marcado en CDP doc).
- **9 bugs encontrados y corregidos**:
  1. **2 métodos faltantes añadidos**: `add_inspected_heap_object` (Go: `AddInspectedHeapObject`) y `get_sampling_profile` (Go: `GetSamplingProfile`). Antes: 10 métodos. Ahora: 12 métodos.
  2. **`start_sampling` tipo incorrecto**: `sampling_interval` era `int | None`, debe ser `float | None` (Go: `float64`). Además faltaban 3 parámetros: `stack_depth` (float, omitempty), `include_objects_collected_by_major_gc` (bool, sin omitempty), `include_objects_collected_by_minor_gc` (bool, sin omitempty). Antes solo tenía `sampling_interval`.
  3. **`start_sampling` bools sin omitempty**: `includeObjectsCollectedByMajorGC` y `includeObjectsCollectedByMinorGC` siempre se envían (Go source `bool` sin `omitempty`). Implementado correctamente: siempre presentes en params dict.
  4. **`start_sampling` omitempty para floats**: `samplingInterval` y `stackDepth` se omiten cuando son 0 o None (Go source `omitempty,omitzero`). Implementado con `if sampling_interval:` y `if stack_depth:`.
  5. **`get_object_by_heap_object_id` JSON key incorrecto**: usaba `heapObjectId` como key JSON, debe ser `objectId` (Go source `json:"objectId"`). Corregido.
  6. **`stop_tracking_heap_objects` parámetros faltantes**: solo tenía `report_progress`, faltaban `capture_numeric_value` (bool, sin omitempty) y `expose_internals` (bool, sin omitempty). Go source: `CaptureNumericValue bool` y `ExposeInternals bool` ambos sin `omitempty`. Corregido: los 3 bools siempre se envían.
  7. **Falta validación de tipos**: añadida validación `isinstance` con `TypeError` descriptivo para todos los parámetros en todos los métodos: `add_inspected_heap_object` (str), `get_heap_object_id` (str), `get_object_by_heap_object_id` (str, str|None), `start_sampling` (float|None con bool-as-int guard, bool, bool), `start_tracking_heap_objects` (bool), `stop_tracking_heap_objects` (bool, bool, bool), `take_heap_snapshot` (bool, bool, bool).
  8. **Bool-as-int guard para floats**: `sampling_interval` y `stack_depth` rechazan `bool` explícitamente (`isinstance(x, bool)` check) ya que `bool` es subclase de `int` en Python y podría pasar validaciones numéricas.
  9. **Métodos desordenados**: reordenados alfabéticamente para coincidir con Go source: `add_inspected_heap_object` → `collect_garbage` → `disable` → `enable` → `get_heap_object_id` → `get_object_by_heap_object_id` → `get_sampling_profile` → `start_sampling` → `start_tracking_heap_objects` → `stop_sampling` → `stop_tracking_heap_objects` → `take_heap_snapshot`.
- **Eventos documentados** (5 eventos desde Go source `events.go`):
  - `HeapProfiler.addHeapSnapshotChunk`: `chunk` (str).
  - `HeapProfiler.heapStatsUpdate`: `statsUpdate` (list[int] — array de triplets).
  - `HeapProfiler.lastSeenObjectId`: `lastSeenObjectId` (int), `timestamp` (float).
  - `HeapProfiler.reportHeapSnapshotProgress`: `done` (int), `total` (int), `finished` (bool).
  - `HeapProfiler.resetProfiles`: sin parámetros.
- **Tipos documentados** en module docstring (4 tipos desde Go source `types.go`):
  - `HeapSnapshotObjectID` — str.
  - `SamplingHeapProfileNode` — callFrame (dict), selfSize (float), id (int), children (list).
  - `SamplingHeapProfileSample` — size (float), nodeId (int), ordinal (float).
  - `SamplingHeapProfile` — head (SamplingHeapProfileNode), samples (list[SamplingHeapProfileSample]).
- **Tests unitarios**: **102 tests** en `test_tier3j_domains.py` con FakeSender — cubriendo todos los 12 métodos, command names, JSON keys, params opcionales vs requeridos, bool defaults (`False`), bool con `True`, bool-as-int guard (sampling_interval, stack_depth), type validation (str, float, bool), zero values omitted (sampling_interval=0, stack_depth=0, ambos zero), return values (get_heap_object_id, get_object_by_heap_object_id, get_sampling_profile, stop_sampling, + 8 void methods), int accepted for float params, small/large float values, explicit None for object_group, individual bool combinations (capture_numeric_value only, expose_internals only), params key count verification (all 12 methods), method order alfabético, method count (12), inherits BaseDomain, all methods coroutines, 12 docstring verification tests.
- **Tests de integración**: **24 tests** en `test_heapprofiler_layertree_performancetimeline.py` con navegador real — enable/disable, collect_garbage, start/stop_sampling con verificación de `profile`, start_sampling con all params, get_sampling_profile mid-sampling, take_heap_snapshot (default + capture_numeric_value + expose_internals), get_heap_object_id roundtrip, get_object_by_heap_object_id roundtrip, add_inspected_heap_object, start/stop_tracking_heap_objects, start_tracking with False, double enable/disable, negative interval, float stack_depth, large interval, 6 type validation tests.
- **Tests E2E**: **48 tests** en `test_heap_profiler_e2e.py` con navegador real Edge headless — domain accessible, enable/disable cycle, collect_garbage, full sampling lifecycle, get_sampling_profile mid-sampling, sampling with include_objects_collected_by_major_gc, sampling with include_objects_collected_by_minor_gc, take_heap_snapshot (3 variantes + expose_internals), heap_object_id roundtrip, get_object_by_heap_object_id with group + empty group omitted, add_inspected_heap_object real, start/stop_tracking_heap_objects, stop_tracking with all params, start_tracking with False, stop_sampling without start raises, double enable/disable, negative interval, float stack_depth, large interval, 12 type validation tests, raw send, inherits BaseDomain, all methods coroutines, method count, method order, 8 docstring verification tests (events, types, Experimental mark, $x mention, major/minor GC detail, lastSeenObjectId extra detail).
- **Total: 102 unit tests + 24 integration tests + 48 E2E tests = 174 tests** para el dominio HeapProfiler.
- `ruff check` ✅ en todos los archivos modificados.
- `pytest -m unit` ✅ — 114/114 tests passed (HeapProfiler + LayerTree + PerformanceTimeline combinados).

### Segunda revisión HeapProfiler — bugs adicionales encontrados y corregidos

10. **`get_object_by_heap_object_id` empty string `object_group` no se omite**: Go tiene `json:"objectGroup,omitempty,omitzero"`. String vacío es zero value para `string` en Go y se omite. Python usaba `if object_group is not None:` que incluye `""`. Corregido: `if object_group:` para omitir tanto `None` como `""`.

11. **Falta marca "Experimental"**: CDP doc marca HeapProfiler como Experimental. No estaba en class docstring. Corregido: añadida marca `**Experimental**` en class docstring.

12. **`start_sampling` docstrings incompletos para bool params**: `include_objects_collected_by_major_gc` y `include_objects_collected_by_minor_gc` solo decían "Include objects discarded by major/minor GC". Go source tiene descripciones detalladas sobre el comportamiento por defecto y qué información adicional incluye cada flag. Corregido: docstrings expandidos con descripciones completas del Go source.

13. **`add_inspected_heap_object` docstring incompleto**: Faltaba "See Command Line API for more details $x functions" (Go source exacto). Corregido: añadido.

14. **Descripciones de tipos en module docstring sin campos**: Los tipos `SamplingHeapProfileNode` y `SamplingHeapProfileSample` no incluían descripciones de campos del Go source (e.g., "Function location", "Allocations size in bytes excluding children", "Time-ordered sample ordinal number"). Corregido: añadidas descripciones de campos desde Go source `types.go`.

15. **Evento `lastSeenObjectId` descripción incompleta**: Go source dice "If the were changes in the heap since last event then one or more heapStatsUpdate events will be sent before a new lastSeenObjectId event." Nuestra documentación no mencionaba esto. Corregido: añadido detalle sobre heapStatsUpdate events enviados antes de lastSeenObjectId.

### Tercera revisión HeapProfiler — sin bugs nuevos, cobertura expandida

Revisión línea por línea contra Go source completo (`heapprofiler.go`, `types.go`, `events.go`). Verificados:
- 12 command names exactos vs Go constants ✅
- Todos los JSON keys vs Go `json:"..."` tags ✅
- `omitempty` vs `omitempty,omitzero` semantics ✅
- Bool params sin `omitempty` siempre enviados ✅
- Float params con `omitzero` omitidos en zero value ✅
- String params con `omitempty,omitzero` omitidos en `None` y `""` ✅
- Type validation completa (str, float, bool) ✅
- Bool-as-int guard para float params ✅
- Method order alfabético vs Go source ✅
- Events documentation completa (5 eventos) ✅
- Types documentation completa (4 tipos con campos) ✅
- Experimental mark en class docstring ✅
- Docstrings detallados vs Go source comments ✅
- Return values documentados correctamente ✅

**Sin bugs nuevos encontrados.** Implementación correcta tras 3 pasadas.

**+26 unit tests añadidos** (76 → 102):
- 8 return value tests para void methods (enable, disable, collect_garbage, add_inspected_heap_object, start_sampling, start_tracking_heap_objects, stop_tracking_heap_objects, take_heap_snapshot)
- 1 test ambos zero params omitidos simultáneamente
- 1 test int aceptado para float params
- 2 tests small/large float values (0.001, 1e15)
- 1 test explicit None para object_group
- 4 tests individual bool combinations (capture_numeric_value only, expose_internals only para take_heap_snapshot y stop_tracking_heap_objects)
- 8 tests params key count verification (todos los métodos con params)

### Memory (revisado contra Go source cdproto)

- **Archivo**: `cdpwave/domains/memory.py`
- **Spec CDP**: https://chromedevtools.github.io/devtools-protocol/tot/Memory/
- **Go source**: `chromedp/cdproto/master/memory/memory.go` y `types.go`
- **Métodos CDP (11)**: `getDOMCounters`, `getDOMCountersForLeakDetection`, `prepareForLeakDetection`, `forciblyPurgeJavaScriptMemory`, `setPressureNotificationsSuppressed`, `simulatePressureNotification`, `startSampling`, `stopSampling`, `getAllTimeSamplingProfile`, `getBrowserSamplingProfile`, `getSamplingProfile`.
- **Métodos implementados (11)**: `get_dom_counters`, `get_dom_counters_for_leak_detection`, `prepare_for_leak_detection`, `forcibly_purge_javascript_memory`, `set_pressure_notifications_suppressed`, `simulate_pressure_notification`, `start_sampling`, `stop_sampling`, `get_all_time_sampling_profile`, `get_browser_sampling_profile`, `get_sampling_profile`.
- **Paridad**: 11/11 métodos CDP implementados. 0 faltantes. 0 extra. 1 naming mismatch (`JavaScript` → `javascript` en vez de `java_script`).
- **Dominio experimental** (marcado en CDP doc y Go source).

### Bugs encontrados y corregidos

- **Bug #1 — `force_garbage_collection` método espurio**: No existe en Go source ni CDP spec. Eliminado.
- **Bug #2 — `start_sampling` parámetros incorrectos**: Tenía `sampling_interval: int = 0` y `suppress_randomness: bool = False` pero enviaba ambos siempre. Go source: `SamplingInterval float64 json:"samplingInterval,omitempty,omitzero"` (se omite si es 0) y `SuppressRandomness bool json:"suppressRandomness"` (sin omitempty, siempre se envía). Corregido: `sampling_interval` solo se envía si es truthy (`if sampling_interval:`), `suppress_randomness` siempre se envía.
- **Bug #3 — `start_sampling` sin validación de tipos**: Añadido `isinstance(sampling_interval, int)` con bool-as-int guard (`isinstance(x, bool)` check) y `isinstance(suppress_randomness, bool)` con `TypeError` descriptivo.
- **Bug #4 — `set_pressure_notifications_suppressed` sin validación de tipo**: Añadido `isinstance(suppressed, bool)` con `TypeError` descriptivo.
- **Bug #5 — `simulate_pressure_notification` sin validación de tipo ni enum**: Añadido `isinstance(level, str)` con `TypeError` y validación de enum (`"moderate"`, `"critical"`) con `ValueError` usando `frozenset` inmutable.
- **Bug #6 — Docstrings no coincidían con Go source**: Todas las docstrings actualizadas para coincidir exactamente con las descripciones del Go source:
  - `get_dom_counters_for_leak_detection`: añadido "renderer" → "after preparing renderer for leak detection"
  - `set_pressure_notifications_suppressed`: añadido "in all processes"
  - `simulate_pressure_notification`: añadido "in all processes"
  - `get_all_time_sampling_profile`: añadido "process" → "renderer process startup"
  - `get_browser_sampling_profile`: añadido "process" → "browser process startup"
  - `get_sampling_profile`: añadido "call" → "last startSampling call"
- **Bug #7 — Module docstring sin tipos**: Añadidos 5 tipos del Go source `types.go`: `PressureLevel` (enum), `SamplingProfileNode`, `SamplingProfile`, `Module`, `DOMCounter` con todos sus campos y tipos.
- **Bug #8 — Class docstring sin marca Experimental**: Añadida marca `**Experimental**` y "No events".
- **Bug #9 — Orden de métodos no alfabético**: Reordenados para coincidir con Go source: `get_dom_counters` → `get_dom_counters_for_leak_detection` → `prepare_for_leak_detection` → `forcibly_purge_javascript_memory` → `set_pressure_notifications_suppressed` → `simulate_pressure_notification` → `start_sampling` → `stop_sampling` → `get_all_time_sampling_profile` → `get_browser_sampling_profile` → `get_sampling_profile`.
- **Bug #10 — `client.py` docstring del property `memory` inexacta**: Decía "GC control" → actualizada a "DOM counters, sampling, and pressure control".

### Tipos verificados contra Go source `types.go`

- `PressureLevel`: enum string — `"moderate"`, `"critical"`. cdpwave valida con `frozenset({"moderate", "critical"})`.
- `SamplingProfileNode`: `Size float64`, `Total float64`, `Stack []string` — cdpwave documenta como dict con `size` (float), `total` (float), `stack` (list[str]).
- `SamplingProfile`: `Samples []*SamplingProfileNode`, `Modules []*Module` — cdpwave documenta como dict con `samples` (list[SamplingProfileNode]), `modules` (list[Module]).
- `Module`: `Name string`, `UUID string`, `BaseAddress string`, `Size float64` — cdpwave documenta todos los campos con tipos correctos.
- `DOMCounter`: `Name string`, `Count int64` — cdpwave documenta como dict con `name` (str), `count` (int). Nota sobre volatilidad de nombres incluida.

### Eventos

El dominio Memory no tiene eventos en la spec CDP ni en Go source.

### Naming mismatch

| CDP (camelCase) | cdpwave (snake_case) | Issue |
|---|---|---|
| `forciblyPurgeJavaScriptMemory` | `forcibly_purge_javascript_memory` | `JavaScript` → `javascript` vs `java_script` |

### Tests unitarios

- **35+ tests** en `tests/unit/domains/test_tier3e_domains.py` con FakeSender — cubriendo los 11 métodos:
  - Method count (11), method order (alfabético), `isinstance(BaseDomain)`, all coroutines.
  - `get_dom_counters`: params `None`, return values, exact CDP method name.
  - `get_dom_counters_for_leak_detection`: params `None`, return `counters` list.
  - `prepare_for_leak_detection`: params `None`, return empty.
  - `forcibly_purge_javascript_memory`: params `None`, return empty.
  - `set_pressure_notifications_suppressed`: `True`/`False`, TypeError for int/str/None/float/list/dict, bool always sent.
  - `simulate_pressure_notification`: `"moderate"`/`"critical"`, TypeError for int/None/bool/list/dict, ValueError for invalid enum (`"low"`, `""`, `"high"`), TypeError takes precedence over ValueError.
  - `start_sampling`: `sampling_interval` omitted when 0 (omitempty), `suppress_randomness` always sent, bool-as-int guard for `sampling_interval`, TypeError for non-bool `suppress_randomness`, combinations of params.
  - `stop_sampling`: params `None`, return empty.
  - `get_all_time_sampling_profile`: params `None`, return `profile`.
  - `get_browser_sampling_profile`: params `None`, return `profile`.
  - `get_sampling_profile`: params `None`, return `profile`.
  - Docstring accuracy tests: "all processes", "renderer process", "browser process", "last startSampling call", "OomIntervention", "V8", "workers", "Experimental".

### Tests de integración

- **11+ tests** en `tests/integration/test_memory_schema_deviceorientation_sensor.py` con navegador real — todos los 11 métodos con verificación de return values, `get_dom_counters` con documentos/nodes/jsEventListeners, `start_sampling` + `get_sampling_profile` lifecycle, `simulate_pressure_notification` con enum válido, `set_pressure_notifications_suppressed` True/False, raw send.

### E2E tests

- **30+ tests** en `tests/e2e/test_memory_e2e.py` con flujos completos contra navegador real Edge headless:
  - Full flow: `get_dom_counters` → `prepare_for_leak_detection` → `get_dom_counters_for_leak_detection` → `forcibly_purge_javascript_memory`.
  - Sampling lifecycle: `start_sampling` → `get_sampling_profile` → `stop_sampling` → `get_all_time_sampling_profile` → `get_browser_sampling_profile`.
  - DOM counters: verify `documents`, `nodes`, `jsEventListeners` are ints.
  - Leak detection: `prepare_for_leak_detection` + `get_dom_counters_for_leak_detection` with `counters` list.
  - Pressure notifications: `set_pressure_notifications_suppressed` True/False, `simulate_pressure_notification` moderate/critical.
  - Type validation: TypeError for `suppressed` (int), `level` (int), `sampling_interval` (bool/str), `suppress_randomness` (int). ValueError for `level` ("low").
  - Raw send: all 11 commands via `session.send`.
  - Docstring accuracy: "all processes", "renderer process", "browser process", "last startSampling call", "OomIntervention", "V8", "jsEventListeners", "Experimental", method count (11), method order.

### Quality checks

- `ruff check`: ✅
- `mypy --strict`: ✅
- `pytest -m unit`: 3166/3166 passed (all domains, 0 failures)

### Total: 35+ unit tests + 11+ integration tests + 30+ E2E tests = 76+ tests para el dominio Memory.

### Tracing (revisado contra Go source cdproto)

- **6 comandos CDP** en Go source, **6 métodos** en cdpwave (0 extra, 0 faltantes).
- **12 bugs encontrados y corregidos**:
  - `request_clock_sync_marker`: método espurio removido (no existe en Go source ni CDP spec).
  - `get_track_event_descriptor`: método faltante añadido (Go source `CommandGetTrackEventDescriptor = "Tracing.getTrackEventDescriptor"`). Sin params, return `descriptor` (str base64-encoded).
  - `request_memory_dump`: método faltante añadido (Go source `CommandRequestMemoryDump = "Tracing.requestMemoryDump"`). Params: `deterministic` (bool, siempre enviado, default False), `level_of_detail` (str, omitempty — solo se envía si no es None/vacío). Return: `dumpGuid` (str), `success` (bool).
  - `start`: params completamente incorrectos — removidos `categories`, `options`, `trace_type` (no existen en Go source). Añadidos `trace_config`, `perfetto_config`, `tracing_backend`, `screenshot_max_size`, `screenshot_max_count`. Cambiados `transfer_mode`, `stream_format`, `stream_compression`, `buffer_usage_reporting_interval` a omitempty (Go source usa `omitempty,omitzero` — solo se envían si son truthy). Todos los params ahora son opcionales con default `None`.
  - `record_clock_sync_marker`: añadida validación de tipo `isinstance(sync_id, str)` con `TypeError`.
  - Añadida validación de enums con `ValueError` para `transfer_mode` ("ReportEvents"/"ReturnAsStream"), `stream_format` ("json"/"proto"), `stream_compression` ("none"/"gzip"), `level_of_detail` ("background"/"light"/"detailed"), `tracing_backend` ("auto"/"chrome"/"system").
  - Añadida validación de tipos con `TypeError` para todos los params de `start` y `request_memory_dump`.
  - Bool-as-int guard para `screenshot_max_size` y `screenshot_max_count` (isinstance bool check antes de int).
  - Bool-as-int guard para `buffer_usage_reporting_interval` (isinstance bool check antes de int/float).
  - Module docstring: añadidos todos los tipos del Go source (`RecordMode`, `StreamFormat`, `StreamCompression`, `MemoryDumpLevelOfDetail`, `Backend`, `TransferMode`, `TraceConfig`, `MemoryDumpConfig`) con todos sus campos y valores enum.
  - Module docstring: añadidos los 3 eventos (`bufferUsage`, `dataCollected`, `tracingComplete`) con sus parámetros.
  - Class docstring: añadida marca **Experimental** y eventos.
  - Métodos reordenados alfabético para coincidir con Go source: `end` → `get_categories` → `get_track_event_descriptor` → `record_clock_sync_marker` → `request_memory_dump` → `start`.
- **Tests unitarios**: **80+ tests** en `tests/unit/domains/test_tracing_domain.py` con FakeSender — cubriendo los 6 métodos, params verification, return values, exact CDP method names, type validation (TypeError) para todos los params, enum validation (ValueError) para transfer_mode/stream_format/stream_compression/level_of_detail/tracing_backend, omitempty semantics (params omitidos cuando son zero/empty/None), bool siempre enviado (deterministic en request_memory_dump), method count (6), method order, isinstance(BaseDomain), all coroutines, docstring accuracy tests, no request_clock_sync_marker test.
- **Tests de integración**: **13 tests** en `tests/integration/test_accessibility_storage_tracing_animation.py` con navegador real — get_categories, start/end lifecycle, record_clock_sync_marker, request_memory_dump (default + deterministic), get_track_event_descriptor (con suppress), raw send para todos los 6 comandos.
- **E2E tests**: **50+ tests** en `tests/e2e/test_tracing_e2e.py` con flujos completos contra navegador real Edge headless — full tracing lifecycle (start → end → tracingComplete event), get_categories return verification, start with stream_format/stream_compression/buffer_usage_interval/tracing_backend, request_memory_dump with deterministic True/False and level_of_detail, record_clock_sync_marker, get_track_event_descriptor, start no params, end without start, raw send for all 6 commands, type validation tests (TypeError/ValueError), docstring accuracy tests, method count, method order, inherits BaseDomain, no request_clock_sync_marker.
- **Total: 80+ unit tests + 13 integration tests + 50+ E2E tests = 143+ tests** para el dominio Tracing.

### IO (revisado contra Go source cdproto)

- **3 comandos CDP** en Go source, **3 métodos** en cdpwave (0 extra, 0 faltantes).
- **0 bugs** encontrados. Verificación línea por línea completada en 3 pasadas.
- **Métodos verificados**:
  - `close`: `handle` (StreamHandle, str, sin omitempty — siempre enviado). Command: `IO.close`.
  - `read`: `handle` (StreamHandle, str, sin omitempty), `offset` (int64, `omitempty,omitzero` — omitido cuando 0 o None, negativos enviados), `size` (int64, `omitempty,omitzero` — mismo). Command: `IO.read`. Return: `base64Encoded` (bool, siempre), `data` (str, `omitempty,omitzero`), `eof` (bool, siempre).
  - `resolve_blob`: `objectId` (runtime.RemoteObjectID, str, sin omitempty). Command: `IO.resolveBlob`. Return: `uuid` (str, `omitempty,omitzero`).
- **Tipos verificados contra Go source `types.go`**: `StreamHandle` = string (puede ser `blob:<uuid>`).
- **Validación de tipos**: bool rechazado para int (`isinstance(offset, bool)` antes de `isinstance(offset, int)`). Exotic types rechazados: bytes, set, tuple, dict, list, float, None.
- **Tests unitarios**: **278 tests** en `tests/unit/domains/test_io_pwa_domains.py` con FakeSender — cubriendo básicos, omitempty (None/0/""/negativos), type validation exhaustiva (int/bool/list/dict/None/float/bytes/set/tuple), multi-call isolation, raw send, return values (completos/minimales/vacíos), edge cases (large values, max int64, special chars, unicode, empty strings), combos omitempty, meta tests (herencia, orden alfabético, docstrings, sección Raises).
- **Tests de integración**: tests en `tests/integration/test_io_pwa.py` con navegador real — read after close, close already closed, resolve blob invalid object ID, negative offset, raw send with None, chunk count, base64 encoded field, type errors.
- **E2E tests**: tests en `tests/e2e/test_io_pwa_e2e.py` con flujos completos contra navegador real — mismos escenarios que integración.
- **Total: 278 unit tests + integration tests + E2E tests** para el dominio IO (compartidos con PWA en el mismo archivo).

### PWA (revisado contra Go source cdproto)

- **7 comandos CDP** en Go source, **7 métodos** en cdpwave (0 extra, 0 faltantes).
- **0 bugs** encontrados. Verificación línea por línea completada en 3 pasadas.
- **Métodos verificados**:
  - `change_app_user_settings`: `manifestId` (str, siempre), `linkCapturing` (bool, **sin** omitempty — siempre enviado, default False), `displayMode` (DisplayMode, `omitempty,omitzero` — omitido cuando None o ""). Command: `PWA.changeAppUserSettings`.
  - `get_os_app_state`: `manifestId` (str, siempre). Command: `PWA.getOsAppState`. Return: `badgeCount` (int64, `omitempty,omitzero`), `fileHandlers` ([]FileHandler, `omitempty,omitzero`).
  - `install`: `manifestId` (str, siempre), `installUrlOrBundleUrl` (str, `omitempty,omitzero`). Command: `PWA.install`.
  - `launch`: `manifestId` (str, siempre), `url` (str, `omitempty,omitzero`). Command: `PWA.launch`. Return: `targetId` (target.ID, `omitempty,omitzero`).
  - `launch_files_in_app`: `manifestId` (str, siempre), `files` ([]string, **sin** omitempty — siempre enviado, incluso []). Command: `PWA.launchFilesInApp`. Return: `targetIds` ([]target.ID, `omitempty,omitzero`).
  - `open_current_page_in_app`: `manifestId` (str, siempre). Command: `PWA.openCurrentPageInApp`.
  - `uninstall`: `manifestId` (str, siempre). Command: `PWA.uninstall`.
- **Tipos verificados contra Go source `types.go`**: `DisplayMode` = string enum (`"standalone"`, `"browser"`), `FileHandlerAccept` (`mediaType` str, `fileExtensions` []str), `FileHandler` (`action` str, `accepts` []FileHandlerAccept, `displayName` str).
- **Validación de tipos**: bool rechazado para int, validación exhaustiva para str/list/dict/None/float/bytes/set/tuple. `files` valida tipo list + cada elemento con índice en error.
- **Tests unitarios**: **278 tests** en `tests/unit/domains/test_io_pwa_domains.py` (compartidos con IO) — cubriendo básicos, omitempty, type validation, multi-call isolation, raw send, return values, special manifest IDs (unicode, IWA URLs, special chars), combos, meta tests.
- **Tests de integración**: tests en `tests/integration/test_io_pwa.py` — install/uninstall roundtrip, change app user settings, launch files in app empty list, isolated app manifest, type errors.
- **E2E tests**: tests en `tests/e2e/test_io_pwa_e2e.py` — mismos escenarios con navegador real.
- **Quality checks**: ruff ✅, mypy --strict ✅ (0 issues in 5 files), pytest 278/278 passed.
- **Total: 278 unit tests + integration tests + E2E tests** para el dominio PWA (compartidos con IO en el mismo archivo).

### Extensions (revisado contra Go source cdproto)

- **Archivo**: `cdpwave/domains/extensions.py`
- **Go source**: `chromedp/cdproto/main/extensions/extensions.go` y `types.go`
- **Métodos CDP (8)**: `triggerAction`, `loadUnpacked`, `getExtensions`, `uninstall`, `getStorageItems`, `removeStorageItems`, `clearStorageItems`, `setStorageItems`.
- **Métodos implementados (8)**: `trigger_action`, `load_unpacked`, `get_extensions`, `uninstall`, `get_storage_items`, `remove_storage_items`, `clear_storage_items`, `set_storage_items`.
- **Paridad**: 8/8 métodos CDP implementados. 0 faltantes. 0 extra.
- **Dominio experimental** (marcado en CDP doc y Go source).

### Bugs encontrados y corregidos

- **BUG 17 — `storage_area` con default inconsistente**: `storage_area` tenía default `"local"` en algunos métodos pero era requerido en otros. Go source requiere `storageArea` como parámetro requerido en `GetStorageItems`, `RemoveStorageItems`, `ClearStorageItems`, `SetStorageItems`. **Corregido**: removido default de `storage_area` en `get_storage_items`, `remove_storage_items`, y `clear_storage_items` — ahora es requerido, coincide con Go.
- **BUG 18 — 4 métodos sin `Returns:` en docstring**: `trigger_action`, `uninstall`, `clear_storage_items`, `set_storage_items` no tenían sección `Returns:`. Go source confirma que retornan solo `err` (void). **Corregido**: añadido `Returns: Empty dict (no return value from CDP).` a los 4 métodos.
- **BUG 19 — Module docstring incompleto**: Faltaban secciones `Types:` y `Events:` presentes en otros dominios (IO, PWA). **Corregido**: añadidas secciones `Types:` (`StorageArea` enum con 4 valores, `ExtensionInfo` struct con 5 campos) y `Events:` (el dominio Extensions no tiene eventos en Go source ni CDP spec).
- **BUG 21 — `remove_storage_items` sin `Returns:`**: Único método void sin sección `Returns:`. **Corregido**: añadido `Returns: Empty dict (no return value from CDP).`.
- **BUG 22 — Orden inconsistente de valores `StorageArea`**: Module docstring usaba `"session", "local", "sync", "managed"` (orden de Go const) pero method docstrings usaban `"local", "session", "sync", "managed"`. **Corregido**: alineadas method docstrings al orden de Go source (`"session"`, `"local"`, `"sync"`, `"managed"`).
- **BUG 23 — Missing `TypeError` unit tests**: `remove_storage_items` sin tests para `storage_area` (int) y `keys` con elemento no-string (`[42]`). `set_storage_items` sin tests para `id` (int) y `storage_area` (int). **Corregido**: añadidos 4 tests unitarios.

### Tipos verificados contra Go source `types.go`

- `StorageArea`: enum string — `"session"`, `"local"`, `"sync"`, `"managed"` (4 valores, orden verificado contra Go const block).
- `ExtensionInfo`: struct con `id` (str, sin omitempty), `name` (str, sin omitempty), `version` (str, sin omitempty), `path` (str, sin omitempty), `enabled` (bool, sin omitempty).

### Métodos verificados contra Go source `extensions.go`

- `trigger_action`: `id` (str, sin omitempty), `targetId` (str, sin omitempty). Command: `Extensions.triggerAction`. Void return.
- `load_unpacked`: `path` (str, sin omitempty), `enableInIncognito` (bool, sin omitempty — siempre enviado, default `false`). Command: `Extensions.loadUnpacked`. Return: `id` (str, `omitempty,omitzero`).
- `get_extensions`: sin params. Command: `Extensions.getExtensions`. Return: `extensions` (list[ExtensionInfo], `omitempty,omitzero`).
- `uninstall`: `id` (str, sin omitempty). Command: `Extensions.uninstall`. Void return.
- `get_storage_items`: `id` (str, sin omitempty), `storageArea` (StorageArea, sin omitempty), `keys` ([]string, `omitempty,omitzero` — omitido cuando `None`). Command: `Extensions.getStorageItems`. Return: `data` (jsontext.Value, `omitempty,omitzero`).
- `remove_storage_items`: `id` (str, sin omitempty), `storageArea` (StorageArea, sin omitempty), `keys` ([]string, sin omitempty — siempre enviado). Command: `Extensions.removeStorageItems`. Void return.
- `clear_storage_items`: `id` (str, sin omitempty), `storageArea` (StorageArea, sin omitempty). Command: `Extensions.clearStorageItems`. Void return.
- `set_storage_items`: `id` (str, sin omitempty), `storageArea` (StorageArea, sin omitempty), `values` (jsontext.Value, sin omitempty). Command: `Extensions.setStorageItems`. Void return.

### Validación de tipos

- `isinstance` con `TypeError` descriptivo añadido a los 8 métodos:
  - `trigger_action`: `id` (str), `target_id` (str).
  - `load_unpacked`: `path` (str), `enable_in_incognito` (bool).
  - `get_extensions`: sin params (sin validación).
  - `uninstall`: `id` (str).
  - `get_storage_items`: `id` (str), `storage_area` (str), `keys` (list[str], cada elemento str).
  - `remove_storage_items`: `id` (str), `storage_area` (str), `keys` (list[str], cada elemento str).
  - `clear_storage_items`: `id` (str), `storage_area` (str).
  - `set_storage_items`: `id` (str), `storage_area` (str), `values` (dict).

### Eventos

El dominio Extensions no tiene eventos en Go source ni CDP spec.

### Tests unitarios

- **80 tests** en `tests/unit/domains/test_tier3h_domains.py` con FakeSender — cubriendo los 8 métodos: básicos, params verification, return values, type validation (TypeError para str/int/list/dict/None en todos los params), `keys` omitempty (None omitido, [] enviado), `enable_in_incognito` bool siempre enviado, `storage_area` requerido (sin default), meta tests (method count, alphabetical order, docstrings, Raises section presence basado en params).

### Tests de integración

- **Tests** en `tests/integration/test_extensions_pwa_worker_inspector.py` con navegador real — get_extensions, uninstall, trigger_action, set_storage_items, remove_storage_items, clear_storage_items, load_unpacked, TypeError validation, uso de `contextlib.suppress(Exception)` para comandos que fallan sin extensión real instalada.

### E2E tests

- **Tests** en `tests/e2e/test_extensions_systeminfo_e2e.py` con flujos completos contra navegador real — domain accessible from session, functional tests (get_extensions, load_unpacked with suppress, trigger_action with suppress, storage operations with suppress), type validation in real browser context, raw send commands, meta tests (method count, alphabetical order, docstring presence, Raises section basado en params).

### Total: 80 unit tests + integration tests + E2E tests para el dominio Extensions.

---

### SystemInfo (revisado contra Go source cdproto)

- **Archivo**: `cdpwave/domains/system_info.py`
- **Go source**: `chromedp/cdproto/main/systeminfo/systeminfo.go` y `types.go`
- **Métodos CDP (3)**: `getInfo`, `getFeatureState`, `getProcessInfo`.
- **Métodos implementados (4)**: `get_info`, `get_feature_state`, `get_process_info` + 1 extra (removido `get_gpu_info` — no existe en Go source ni CDP spec).
- **Paridad**: 3/3 métodos CDP implementados. 0 faltantes. 0 extra (después de remover `get_gpu_info`).
- **Nota**: `getInfo` y `getProcessInfo` son comandos de browser target (no page target). Se llaman via `client.send("SystemInfo.getInfo")`, no via `session.system_info.get_info()`.

### Bugs encontrados y corregidos

- **BUG 20 — Module docstring incompleto**: Faltaban secciones `Types:` y `Events:`. **Corregido**: añadidas secciones `Types:` (`GPUDevice` con 8 campos, `Size` con 2 campos, `GPUInfo` con 6 campos, `ProcessInfo` con 3 campos, `VideoDecodeAcceleratorCapability`, `VideoEncodeAcceleratorCapability`, `SubsamplingFormat` enum, `ImageType` enum) y `Events:` (el dominio SystemInfo no tiene eventos en Go source ni CDP spec).
- **`get_gpu_info` removido**: Método espurio que no existe en Go source ni CDP spec. Removido en revisión anterior.

### Tipos verificados contra Go source `types.go`

- `GPUDevice`: `vendorId` (float64), `deviceId` (float64), `subSysId` (float64, omitempty), `revision` (float64, omitempty), `vendorString` (str), `deviceString` (str), `driverVendor` (str), `driverVersion` (str).
- `Size`: `width` (int64), `height` (int64).
- `GPUInfo`: `devices` ([]GPUDevice), `auxAttributes` (jsontext.Value, omitempty), `featureStatus` (jsontext.Value, omitempty), `driverBugWorkarounds` ([]string), `videoDecoding` ([]VideoDecodeAcceleratorCapability), `videoEncoding` ([]VideoEncodeAcceleratorCapability).
- `ProcessInfo`: `type` (str), `id` (int64), `cpuTime` (float64).
- `SubsamplingFormat`: enum — `"yuv420"`, `"yuv422"`, `"yuv444"`.
- `ImageType`: enum — `"jpeg"`, `"webp"`, `"unknown"`.

### Métodos verificados contra Go source `systeminfo.go`

- `get_info`: sin params. Command: `SystemInfo.getInfo`. Return: `gpu` (GPUInfo, omitempty), `modelName` (str, omitempty), `modelVersion` (str, omitempty), `commandLine` (str, omitempty). **Browser target only**.
- `get_feature_state`: `featureState` (str, sin omitempty — requerido). Command: `SystemInfo.getFeatureState`. Return: `featureEnabled` (bool, sin omitempty). **Page target**.
- `get_process_info`: sin params. Command: `SystemInfo.getProcessInfo`. Return: `processInfo` ([]ProcessInfo, omitempty). **Browser target only**.

### Validación de tipos

- `isinstance` con `TypeError` descriptivo añadido a `get_feature_state`: `feature_state` (str). `get_info` y `get_process_info` no tienen params (sin validación necesaria).

### Eventos

El dominio SystemInfo no tiene eventos en Go source ni CDP spec.

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3d_domains.py` con FakeSender — cubriendo los 3 métodos (+1 extra removido): básicos, return values (`gpu`, `modelName`, `modelVersion`, `commandLine` en get_info; `featureEnabled` en get_feature_state; `processInfo` en get_process_info), type validation (TypeError para `feature_state` int/None/bool/list/dict), meta tests (method count, alphabetical order, docstrings, Raises section basado en params).

### Tests de integración

- **Tests** en `tests/integration/test_service_worker_systeminfo_webauthn_io.py` con navegador real — `getInfo` y `getProcessInfo` via `client.send()` (browser target only), `getFeatureState` via `session.system_info` (page target), `test_domain_accessible_from_session`, TypeError validation para `get_feature_state`.

### E2E tests

- **Tests** en `tests/e2e/test_extensions_systeminfo_e2e.py` con flujos completos contra navegador real — `getInfo` y `getProcessInfo` via `client.send()` (browser target only), `getFeatureState` via `session.system_info` (page target), type validation, raw send, meta tests (method count, alphabetical order, docstring presence, Raises section basado en params).

### Total: unit tests + integration tests + E2E tests para el dominio SystemInfo.

---

### Preload (revisado contra Go source cdproto)

- **Archivo**: `cdpwave/domains/preload.py`
- **Go source**: `chromedp/cdproto/main/preload/preload.go`, `types.go`, `events.go`
- **Métodos CDP (2)**: `enable`, `disable`.
- **Métodos implementados (2)**: `enable`, `disable`.
- **Paridad**: 2/2 métodos CDP implementados. 0 faltantes. 0 extra (después de remover métodos espurios).

### Bugs encontrados y corregidos

- **BUG 1 — Métodos espurios**: `get_preload_policy` y `set_preload_policy` no existen en Go source (solo `enable` y `disable`). **Corregido**: ambos métodos removidos.
- **BUG 2 — Docstrings incorrectos**: `enable`/`disable` decían "Activates/Deactivates Preload domain events and reporting" pero Go source dice `[no description]`. **Corregido**: docstrings actualizados a `[no description]`.
- **BUG 3 — Module docstring incompleto**: Faltaban secciones `Types:` y `Events:`. **Corregido**: añadidas secciones `Types:` (RuleSetID, RuleSet, RuleSetErrorType, SpeculationAction, SpeculationTargetHint, IngAttemptKey, IngAttemptSource, PipelineID, PrerenderFinalStatus, IngStatus, PrefetchStatus, PrerenderMismatchedHeaders) y `Events:` (ruleSetUpdated, ruleSetRemoved, preloadEnabledStateUpdated, prefetchStatusUpdated, prerenderStatusUpdated, preloadingAttemptSourcesUpdated).
- **BUG 4 — Falta marca Experimental**: Class docstring no marcaba el dominio como experimental. **Corregido**: añadida marca **Experimental domain.**.
- **BUG 5 — Class docstring sin eventos**: Class docstring no documentaba eventos. **Corregido**: añadidos los 6 eventos con sus parámetros.
- **BUG 6 — Return values incorrectos**: Docstrings decían "Response dict from the CDP" en vez de "Empty dict (no return value from CDP)". **Corregido**: ambos métodos documentan `Empty dict`.
- **BUG 7 — Orden de métodos**: `enable` antes de `disable`. **Corregido**: reordenado alfabéticamente (`disable`, `enable`).

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3g_domains.py` con FakeSender — cubriendo ambos métodos: básicos, return values (empty dict), meta tests (method count=2, alphabetical order, inherits BaseDomain, all coroutines), docstring tests ([no description], Empty dict, Types section, Events section, Experimental mark, all events documented). **Edge case tests**: no params sent (None), multiple calls recorded, enable-disable-enable cycle, no spurious methods exist, signature tests (0 params), docstring no old text (Activates/Deactivates/Must be called), module docstring description.

### Tests de integración

- **Tests** en `tests/integration/test_preload_indexeddb_media_deviceaccess.py` con navegador real — enable/disable, domain accessible from session, raw send. **Edge case tests**: enable-disable-enable cycle, double enable, double disable, enable returns dict type.

### E2E tests

- **Tests** en `tests/e2e/test_preload_device_access_e2e.py` con flujos completos contra navegador real — enable/disable, return dict verification, domain accessible from session, raw send, meta tests (method count, alphabetical order, coroutines, Experimental mark, Types/Events sections). **Edge case tests**: enable-disable-enable cycle, double enable/disable, no spurious methods, no params for enable/disable, signature tests, docstring content (no old text, description), inherits BaseDomain.

### Total: 28 unit tests + 7 integration tests + 22 E2E tests = 57 tests para el dominio Preload.

---

### DeviceAccess (revisado contra Go source cdproto)

- **Archivo**: `cdpwave/domains/device_access.py`
- **Go source**: `chromedp/cdproto/main/deviceaccess/deviceaccess.go`, `types.go`, `events.go`
- **Métodos CDP (4)**: `enable`, `disable`, `selectPrompt`, `cancelPrompt`.
- **Métodos implementados (4)**: `enable`, `disable`, `select_prompt`, `cancel_prompt`.
- **Paridad**: 4/4 métodos CDP implementados. 0 faltantes. 0 extra (después de renombrar `select_bluetooth_device`).

### Bugs encontrados y corregidos

- **BUG 1 — Método renombrado**: `select_bluetooth_device` no existe en Go source. Go source tiene `SelectPrompt` (command `DeviceAccess.selectPrompt`). **Corregido**: renombrado a `select_prompt`.
- **BUG 2 — Parámetros incorrectos en select_prompt**: `select_bluetooth_device` tomaba `request_id: str` y `device: dict[str, Any]` con JSON keys `requestId` y `device`. Go source `SelectPromptParams` tiene `ID RequestID json:"id"` y `DeviceID DeviceID json:"deviceId"`. **Corregido**: parámetros cambiados a `id: str` y `device_id: str` con JSON keys `id` y `deviceId`.
- **BUG 3 — Parámetro incorrecto en cancel_prompt**: `cancel_prompt` tomaba `request_id: str` con JSON key `requestId`. Go source `CancelPromptParams` tiene `ID RequestID json:"id"`. **Corregido**: parámetro cambiado a `id: str` con JSON key `id`.
- **BUG 4 — Docstrings incorrectos**: `enable`/`disable` decían "Activates/Deactivates DeviceAccess domain events and reporting" pero Go source dice "enable/disable events in this domain". **Corregido**: docstrings actualizados.
- **BUG 5 — Module docstring incompleto**: Faltaban secciones `Types:` y `Events:`. **Corregido**: añadidas secciones `Types:` (RequestID, DeviceID, PromptDevice) y `Events:` (deviceRequestPrompted).
- **BUG 6 — Falta marca Experimental**: Class docstring no marcaba el dominio como experimental. **Corregido**: añadida marca **Experimental domain.**.
- **BUG 7 — Class docstring sin eventos**: Class docstring no documentaba eventos. **Corregido**: añadido evento `deviceRequestPrompted` con sus parámetros.
- **BUG 8 — Falta type validation**: `select_prompt` y `cancel_prompt` no validaban tipos de parámetros. **Corregido**: añadido `isinstance` con `TypeError` descriptivo para `id` (str) y `device_id` (str).
- **BUG 9 — Return values incorrectos**: Docstrings no documentaban return values. **Corregido**: todos los métodos documentan `Empty dict (no return value from CDP)`.
- **BUG 10 — Falta Raises section**: `select_prompt` y `cancel_prompt` no tenían sección `Raises:`. **Corregido**: añadida sección `Raises:` con `TypeError`.
- **BUG 11 — Orden de métodos**: `enable` antes de `disable` antes de `select_bluetooth_device` antes de `cancel_prompt`. **Corregido**: reordenado alfabéticamente (`cancel_prompt`, `disable`, `enable`, `select_prompt`).

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3g_domains.py` con FakeSender — cubriendo los 4 métodos: básicos, params verification (JSON keys `id` y `deviceId`), return values (empty dict), type validation (TypeError para `id` int en cancel_prompt y select_prompt, `device_id` int en select_prompt), empty strings, meta tests (method count=4, alphabetical order, inherits BaseDomain, all coroutines), docstring tests (Enable/Disable events, Empty dict, Raises section, Types section, Events section, Experimental mark, event documented). **Edge case tests**: None/bool/list/dict/bytes type validation para `cancel_prompt` y `select_prompt`, both-params-wrong (id first), unicode strings, long strings (1000 chars), special chars, multiple calls recorded, enable-disable-enable cycle, no spurious methods (select_bluetooth_device), signature tests (id, device_id), docstring content (no old text, mentions deviceRequestPrompted, param descriptions), no params for enable/disable, module docstring PromptDevice fields.

### Tests de integración

- **Tests** en `tests/integration/test_preload_indexeddb_media_deviceaccess.py` con navegador real — enable/disable, domain accessible from session, type validation (cancel_prompt y select_prompt), raw send. **Edge case tests**: None/bool type validation para cancel_prompt y select_prompt, both-params-wrong, enable-disable-enable cycle, double enable/disable, enable returns dict type, valid select_prompt/cancel_prompt with suppress, raw send select_prompt/cancel_prompt.

### E2E tests

- **Tests** en `tests/e2e/test_preload_device_access_e2e.py` con flujos completos contra navegador real — enable/disable, return dict verification, domain accessible from session, type validation in real browser, raw send, meta tests (method count, alphabetical order, coroutines, Experimental mark, Types/Events sections). **Edge case tests**: None/bool/list/dict type validation, both-params-wrong, enable-disable-enable cycle, double enable/disable, valid select_prompt/cancel_prompt with suppress, raw send select_prompt/cancel_prompt, no spurious methods, signature tests, docstring content (no old text, mentions deviceRequestPrompted, description), inherits BaseDomain.

### Total: 56 unit tests + 18 integration tests + 38 E2E tests = 112 tests para el dominio DeviceAccess.

---

### HeadlessExperimental (revisado contra PDL oficial + Go source cdproto)

- **Archivo**: `cdpwave/domains/headless_experimental.py`
- **PDL oficial**: `ChromeDevTools/devtools-protocol/pdl/domains/HeadlessExperimental.pdl`
- **Métodos CDP (3)**: `beginFrame`, `enable`, `disable`.
- **Métodos implementados (3)**: `begin_frame`, `enable`, `disable`.
- **Paridad**: 3/3 métodos CDP implementados. 0 faltantes. 0 extra.
- **Domain marked experimental** ✅ (PDL: `experimental domain HeadlessExperimental`).
- **`enable`/`disable` marked deprecated** ✅ (PDL: `deprecated command`).

### Bugs encontrados y corregidos

- **BUG 1 — Método espurio `set_window_bounds`**: No existe en el PDL oficial ni en Go source. **Corregido**: reemplazado por `begin_frame` (el único comando con parámetros del dominio).
- **BUG 2 — Docstrings genéricos**: `enable`/`disable` decían "Activates/Deactivates HeadlessExperimental domain events and reporting". **Corregido**: añadida marca `.. deprecated::` coincidiendo con PDL.
- **BUG 3 — Falta type validation**: `begin_frame` no validaba tipos de parámetros. **Corregido**: añadido `isinstance` + `TypeError` para `frame_time_ticks` (int|float, con bool rejection), `interval` (int|float, con bool rejection), `no_display_updates` (bool), `screenshot` (dict).
- **BUG 4 — Bool subclass bug**: `isinstance(True, int)` devuelve `True` en Python, por lo que `bool` pasaba como número válido. **Corregido**: patrón `isinstance(x, bool) or not isinstance(x, (int, float))` para `frame_time_ticks` e `interval`.

### Métodos verificados contra PDL

- `begin_frame`: 4 params opcionales — `frameTimeTicks` (number), `interval` (number), `noDisplayUpdates` (boolean), `screenshot` (ScreenshotParams dict). Returns `hasDamage` (bool) + `screenshotData` (optional binary). ✅
- `enable`: sin params. Deprecated. ✅
- `disable`: sin params. Deprecated. ✅

### ScreenshotParams documentado

- `format`: enum `jpeg`, `png`, `webp` (opcional, default png)
- `quality`: int 0-100 (jpeg/webp only)
- `optimizeForSpeed`: bool (opcional, default false)

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3f_domains.py` (3 básicos) + `tests/unit/domains/test_headless_experimental_edge.py` (12 edge) + `tests/unit/domains/test_headless_experimental_validation.py` (11 type validation) = **26 tests** con FakeSender — cubriendo begin_frame con todos los params, defaults, edge cases (zero interval, float ticks, screenshot format/quality/optimizeForSpeed), type validation (TypeError para str/bool/list/int en cada param), bool rejection para numeric params, meta tests.

### Tests de integración

- **Tests** en `tests/integration/test_headless_dom_debugger.py` — 11 tests con navegador real: enable/disable roundtrip, begin_frame sin params, con interval, con frame_time_ticks, con no_display_updates, con screenshot png/jpeg, all params, zero interval, repeated frames, enable→begin_frame→disable.

### E2E tests

- **Tests** en `tests/e2e/test_headless_dom_debugger_e2e.py` — 4 type validation E2E tests con navegador real: TypeError se levanta antes de cualquier llamada CDP para frame_time_ticks str, interval str, no_display_updates str, screenshot str.

### Total: 26 unit tests + 11 integration tests + 4 E2E tests = 41 tests para el dominio HeadlessExperimental.

---

### DOMDebugger (revisado contra PDL oficial + Go source cdproto)

- **Archivo**: `cdpwave/domains/dom_debugger.py`
- **PDL oficial**: `ChromeDevTools/devtools-protocol/pdl/domains/DOMDebugger.pdl`
- **Métodos CDP (10)**: `setDOMBreakpoint`, `removeDOMBreakpoint`, `setEventListenerBreakpoint`, `removeEventListenerBreakpoint`, `setXHRBreakpoint`, `removeXHRBreakpoint`, `getEventListeners`, `setInstrumentationBreakpoint`, `removeInstrumentationBreakpoint`, `setBreakOnCSPViolation`.
- **Métodos implementados (10)**: `set_dom_breakpoint`, `remove_dom_breakpoint`, `set_event_listener_breakpoint`, `remove_event_listener_breakpoint`, `set_xhr_breakpoint`, `remove_xhr_breakpoint`, `get_event_listeners`, `set_instrumentation_breakpoint`, `remove_instrumentation_breakpoint`, `set_break_on_csp_violation`.
- **Paridad**: 10/10 métodos CDP implementados. 0 faltantes. 0 extra.

### Bugs encontrados y corregidos

- **BUG 1 — Falta type validation**: Ningún método validaba tipos de parámetros. **Corregido**: añadido `isinstance` + `TypeError` en todos los 10 métodos para todos los parámetros.
- **BUG 2 — Falta enum validation**: `set_dom_breakpoint`/`remove_dom_breakpoint` no validaban `DOMBreakpointType`. `set_break_on_csp_violation` no validaba `CSPViolationType`. **Corregido**: añadido `ValueError` con set de valores válidos.
  - `DOMBreakpointType`: `subtree-modified`, `attribute-modified`, `node-removed`
  - `CSPViolationType`: `trustedtype-sink-violation`, `trustedtype-policy-violation`
- **BUG 3 — Bool subclass bug**: `isinstance(True, int)` devuelve `True` en Python, por lo que `bool` pasaba como int válido en `node_id` y `depth`. **Corregido**: patrón `isinstance(x, bool) or not isinstance(x, int)` para `node_id` (set/remove_dom_breakpoint) y `depth` (get_event_listeners).
- **BUG 4 — Docstrings incompletos**: `target_name` no marcado como experimental. `set_instrumentation_breakpoint`/`remove_instrumentation_breakpoint` no marcados como deprecated ni con redirect. `set_break_on_csp_violation` no marcado como experimental. `get_event_listeners` depth default y -1 no documentados. **Corregido**: todos los docstrings actualizados.
- **BUG 5 — CSP violation type incorrecto**: Docstring usaba `trustedtype-source-violation` (no existe). **Corregido**: cambiado a `trustedtype-policy-violation`.

### Métodos verificados contra PDL

- `set_dom_breakpoint`: `nodeId` (int, requerido), `type` (DOMBreakpointType enum, requerido). ✅
- `remove_dom_breakpoint`: `nodeId` (int, requerido), `type` (DOMBreakpointType enum, requerido). ✅
- `set_event_listener_breakpoint`: `eventName` (str, requerido), `targetName` (str, experimental opcional). ✅
- `remove_event_listener_breakpoint`: `eventName` (str, requerido), `targetName` (str, experimental opcional). ✅
- `set_xhr_breakpoint`: `url` (str, requerido). ✅
- `remove_xhr_breakpoint`: `url` (str, requerido). ✅
- `get_event_listeners`: `objectId` (str, requerido), `depth` (int, opcional, default 1, -1 for entire subtree), `pierce` (bool, opcional). Returns `listeners` list. ✅
- `set_instrumentation_breakpoint`: `eventName` (str, requerido). Experimental + deprecated, redirect to `EventBreakpoints.setInstrumentationBreakpoint`. ✅
- `remove_instrumentation_breakpoint`: `eventName` (str, requerido). Experimental + deprecated, redirect to `EventBreakpoints.removeInstrumentationBreakpoint`. ✅
- `set_break_on_csp_violation`: `violationTypes` (CSPViolationType[] list, requerido). Experimental. ✅

### Enums validados

- `DOMBreakpointType`: `subtree-modified`, `attribute-modified`, `node-removed`
- `CSPViolationType`: `trustedtype-sink-violation`, `trustedtype-policy-violation`

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3i_domains.py` (7 básicos) + `tests/unit/domains/test_dom_debugger_edge.py` (18 edge) + `tests/unit/domains/test_dom_debugger_validation.py` (29 type validation) = **54 tests** con FakeSender — cubriendo todos los métodos, todos los breakpoint types, target_name opcional, empty url, depth 0/-1, pierce true/false, return values, type validation (TypeError para str/int/bool/list en cada param de cada método), enum validation (ValueError para invalid DOMBreakpointType y CSPViolationType), bool rejection para node_id y depth, meta tests.

### Tests de integración

- **Tests** en `tests/integration/test_headless_dom_debugger.py` — 18 tests con navegador real: set/remove dom breakpoint (3 types), event listener breakpoint (con/sin target), xhr breakpoint (con/empty url), get_event_listeners (con depth, pierce, ambos), instrumentation breakpoint, CSP violation (both/single types), all types roundtrip, multiple xhr breakpoints, set same breakpoint twice, full lifecycle.

### E2E tests

- **Tests** en `tests/e2e/test_headless_dom_debugger_e2e.py` — 46 tests con navegador real: DOM breakpoints (set/remove/3 types/mutation), event listener breakpoints (set/remove/multiple/window target), XHR breakpoints (set/remove/empty/multiple/duplicate), get_event_listeners (document/depth 0/-1/pierce true/false/body node/listener fields/after adding listener), instrumentation breakpoints (setInterval/setTimeout), CSP violation (both/sink/policy/empty), full lifecycle, **13 type validation E2E tests** (TypeError/ValueError se levanta antes de cualquier llamada CDP en navegador real para todos los métodos y params).

### Total: 54 unit tests + 18 integration tests + 46 E2E tests = 118 tests para el dominio DOMDebugger.

---

### EventBreakpoints (revisado contra PDL oficial + Go source cdproto)

- **Archivo**: `cdpwave/domains/event_breakpoints.py`
- **PDL oficial**: `ChromeDevTools/devtools-protocol/pdl/domains/EventBreakpoints.pdl`
- **Métodos CDP (3)**: `setInstrumentationBreakpoint`, `removeInstrumentationBreakpoint`, `disable`.
- **Métodos implementados (4)**: `set_instrumentation_breakpoint`, `remove_instrumentation_breakpoint`, `disable`, `clear_instrumentation_breakpoint` (alias deprecated).
- **Paridad**: 3/3 métodos CDP implementados. 0 faltantes. 1 extra (`clear_instrumentation_breakpoint` — alias deprecated de `remove_instrumentation_breakpoint`).
- **Domain marked experimental** ✅ (PDL: `experimental domain EventBreakpoints`).

### Bugs encontrados y corregidos

- **BUG 1 — Método mal nombrado `clear_instrumentation_breakpoint`**: Enviaba `EventBreakpoints.removeInstrumentationBreakpoint` pero se llamaba `clear_instrumentation_breakpoint` (no coincide con CDP). **Corregido**: renombrado a `remove_instrumentation_breakpoint`. `clear_instrumentation_breakpoint` mantenido como alias deprecated que delega a `remove_instrumentation_breakpoint`.
- **BUG 2 — Falta type validation**: Ningún método validaba tipos de parámetros. **Corregido**: añadido `isinstance` + `TypeError` en `set_instrumentation_breakpoint` y `remove_instrumentation_breakpoint` para `event_name` (str).
- **BUG 3 — Domain no marcado experimental**: PDL marca `experimental domain EventBreakpoints`. **Corregido**: añadida nota `Note: This entire domain is **experimental**.` en class docstring.
- **BUG 4 — Docstring de `clear_instrumentation_breakpoint` incorrecto**: Decía "Clear an instrumentation breakpoint" (vago). **Corregido**: ahora documenta que es alias deprecated de `remove_instrumentation_breakpoint`.
- **BUG 5 — Docstrings no coincidían con PDL/Go source**: `set_instrumentation_breakpoint` decía "Set an instrumentation breakpoint" (PDL: "Sets breakpoint on particular native event"). `remove_instrumentation_breakpoint` decía "Remove an instrumentation breakpoint" (PDL: "Removes breakpoint on particular native event"). `disable` decía "Disable all breakpoints" (PDL: "Removes all breakpoints"). Parámetro `event_name` decía "Instrumentation event name" (PDL: "Instrumentation name to stop on"). **Corregido**: docstrings ahora coinciden exactamente con PDL/Go source.
- **BUG 6 — Class docstring incompleta**: Decía "Provides instrumentation breakpoints for pausing JavaScript execution at specific events" (PDL: "permits setting JavaScript breakpoints on operations and events occurring in native code invoked from JavaScript. Once breakpoint is hit, it is reported through Debugger domain"). **Corregido**: ahora incluye mención de que los breakpoints se reportan via Debugger domain.
- **BUG 7 — Docs de debugging incorrectos**: Ejemplo usaba `"DOMContentLoaded"` (evento DOM, no instrumentation event). Etiqueta "Disable:" sobre `remove_instrumentation_breakpoint` (debería ser "Remove:"). Faltaba ejemplo de `disable()`. Descripción decía "native DOM events" (debería ser "native operations and events"). **Corregido**: ejemplo usa `"scriptFirstStatement"`, etiqueta correcta, añadido ejemplo de `disable()`, descripción actualizada.
- **BUG 8 — Descripciones en index.md imprecisas**: EventBreakpoints decía "native events" (debería ser "native operations and events"). Inspector decía "lifecycle events and detached" (debería ser "domain notifications and lifecycle events"). **Corregido**.
- **BUG 9 — Módulo docstring inconsistente con otros dominios**: Decía "EventBreakpoints has no events in the CDP specification." mientras que otros dominios sin eventos (`io.py`, `pwa.py`, `extensions.py`) usan el formato estándar `None.`. **Corregido**: cambiado a `None.` para consistencia.

### Métodos verificados contra PDL

- `set_instrumentation_breakpoint`: `eventName` (str, requerido). ✅
- `remove_instrumentation_breakpoint`: `eventName` (str, requerido). ✅
- `disable`: sin params. ✅

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3i_domains.py` (4 básicos: set/remove/clear_alias/disable) + `tests/unit/domains/test_event_breakpoints_validation.py` (13 type validation) + `tests/unit/domains/test_event_breakpoints_edge.py` (27 edge cases) = **44 tests** con FakeSender — cubriendo set/remove/disable, alias deprecated, type validation (TypeError para int/bool/list/None/dict/bytes/float en event_name de set, remove y clear alias), casos válidos (str pasa, empty str aceptado, unicode, long name, str subclass), return value passthrough, multiple calls tracked, set same breakpoint twice, remove without set, disable without breakpoints, full lifecycle, verificación de que no se envía llamada CDP en TypeError, verificación de que no existe método `enable`, verificación de que no hay métodos extra, verificación de orden de métodos coincide con PDL.

### Tests de integración

- **Tests** en `tests/integration/test_extensions_pwa_worker_inspector.py` — 11 tests con navegador real: domain accessible, set+remove instrumentation breakpoint, disable, clear alias, set multiple breakpoints (3 events), remove without set, set same breakpoint twice, full lifecycle (set×2, remove, disable, remove), disable without any breakpoints, type error raised before CDP call (set/remove/clear alias con int).

### E2E tests

- **Tests** en `tests/e2e/test_event_breakpoints_inspector_e2e.py` — 22 tests con navegador real: set/remove breakpoint lifecycle, disable, clear alias, set→disable→remove lifecycle, set multiple breakpoints (3 events), remove without set, set same breakpoint twice, full lifecycle, disable without any breakpoints, type_error_no_cdp_call (TypeError no bloquea sesión), **11 type validation E2E tests** (TypeError se levanta antes de cualquier llamada CDP para int/bool/list/dict/bytes/None en set, int/bool en remove, int/bool en clear alias).

### Total: 44 unit tests + 11 integration tests + 22 E2E tests = 77 tests para el dominio EventBreakpoints.

---

### Inspector (revisado contra PDL oficial + Go source cdproto)

- **Archivo**: `cdpwave/domains/inspector.py`
- **PDL oficial**: `ChromeDevTools/devtools-protocol/pdl/domains/Inspector.pdl`
- **Métodos CDP (2)**: `disable`, `enable`.
- **Métodos implementados (2)**: `disable`, `enable`.
- **Paridad**: 2/2 métodos CDP implementados. 0 faltantes. 0 extra.
- **Domain marked experimental** ✅ (PDL: `experimental domain Inspector`).

### Bugs encontrados y corregidos

- **BUG 1 — Domain no marcado experimental**: PDL marca `experimental domain Inspector`. **Corregido**: añadida nota `Note: This entire domain is **experimental**.` en class docstring.
- **BUG 2 — Eventos incompletos en docstring**: Solo documentaba `Inspector.detached` y `Inspector.targetCrashed`. **Corregido**: añadidos `Inspector.targetReloadedAfterCrash` (fired when debugging target has reloaded after crash) y `Inspector.workerScriptLoaded` (experimental, fired on worker targets when main worker script and any imported scripts have been evaluated). Añadido param `reason` (string) al evento `detached`.
- **BUG 3 — Orden de métodos no coincidía con PDL**: PDL lista `disable` antes que `enable`. **Corregido**: reordenado para coincidir con PDL y Go source.
- **BUG 4 — Docstrings genéricos**: `enable`/`disable` decían "Enable/Disable the Inspector domain". **Corregido**: cambiado a "Enable/Disable inspector domain notifications" (coincide con Go source exacto).
- **BUG 5 — Test edge con `dir()` no verificaba orden real**: `test_order_matches_pdl_disable_before_enable` usaba `dir()` que ordena alfabéticamente, no por orden de definición. El test pasaba siempre sin importar el orden real. **Corregido**: ahora usa `__dict__` que preserva orden de inserción.
- **BUG 6 — Docstrings de evento `detached` incompletos**: Módulo y class docstrings omitían "Contains detach reason" (PDL: "Fired when remote debugging connection is about to be terminated. Contains detach reason."). Param `reason` solo decía "(string)" sin descripción (PDL: "The reason why connection has been terminated"). **Corregido**: añadido "Contains detach reason" y descripción completa del param.
- **BUG 7 — Property docstring en client.py incorrecta**: `inspector` property decía "inspector lifecycle events" (PDL: "inspector domain notifications"). **Corregido** a "inspector domain notifications".
- **BUG 8 — Módulo docstring summary impreciso**: Decía "inspector lifecycle events and commands" (PDL no menciona "lifecycle"). **Corregido** a "inspector domain notifications and lifecycle events".

### Métodos verificados contra PDL

- `disable`: sin params. Disables inspector domain notifications. ✅
- `enable`: sin params. Enables inspector domain notifications. ✅

### Eventos documentados (verificados contra PDL)

- `Inspector.detached`: Params `reason` (string). ✅
- `Inspector.targetCrashed`: Sin params. ✅
- `Inspector.targetReloadedAfterCrash`: Sin params. ✅
- `Inspector.workerScriptLoaded`: Experimental. Sin params. ✅

### Tests unitarios

- **Tests** en `tests/unit/domains/test_tier3h_domains.py` (3: domain exists, disable, enable) + `tests/unit/domains/test_inspector_validation.py` (3: disable sends no params, enable sends no params, disable→enable sequence) + `tests/unit/domains/test_inspector_edge.py` (12 edge cases) = **18 tests** con FakeSender — cubriendo disable/enable, return value passthrough, multiple enable/disable cycles (5×), enable when already enabled, disable when already disabled, order matches PDL (disable before enable), no extra methods exist, enable→disable→enable sequence.

### Tests de integración

- **Tests** en `tests/integration/test_extensions_pwa_worker_inspector.py` — 7 tests con navegador real: domain accessible, enable/disable roundtrip, disable without enable, enable twice, multiple cycles (3×), enable only.

### E2E tests

- **Tests** en `tests/e2e/test_event_breakpoints_inspector_e2e.py` — 7 tests con navegador real: enable/disable, disable without enable, enable→disable→enable→disable cycle, enable twice, multiple cycles (5×), enable only, disable only.

### Total: 18 unit tests + 7 integration tests + 7 E2E tests = 32 tests para el dominio Inspector.

### Cast (revisado contra PDL oficial + Go source cdproto)

- **6 comandos CDP** en PDL y Go source, **6 métodos** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `Cast.pdl` (ChromeDevTools/devtools-protocol) + `cast.go` (chromedp/cdproto).
- **Dominio experimental** — flag añadido a class docstring.
- **5 bugs encontrados y corregidos**:
  - `enable`: añadido parámetro opcional `presentation_url` (PDL: `optional string presentationUrl`, Go source: `PresentationURL string json:"presentationUrl,omitempty,omitzero"`). Antes no aceptaba parámetros.
  - `start_desktop_mirroring`: método faltante añadido (PDL: `Cast.startDesktopMirroring`, Go source: `StartDesktopMirroring`). Params: `sinkName` (string, requerido).
  - Type validation añadida a `set_sink_to_use`, `start_desktop_mirroring`, `start_tab_mirroring`, `stop_casting` — `isinstance(sink_name, str)` check. `enable` valida `presentation_url` cuando no es `None`.
  - Module docstring y class docstring actualizados con eventos del PDL: `Cast.sinksUpdated` (params: `sinks` — array of Sink con `name`, `id`, optional `session`), `Cast.issueUpdated` (params: `issueMessage` — string).
  - Orden de métodos corregido para coincidir con PDL: `enable` → `disable` → `set_sink_to_use` → `start_desktop_mirroring` → `start_tab_mirroring` → `stop_casting`.
- **Eventos documentados**: `Cast.sinksUpdated`, `Cast.issueUpdated` (en module docstring y class docstring).
- **Tests unitarios**: **8 tests** básicos en `test_tier3f_domains.py` + **45 tests** edge en `test_cast_edge.py` — cubriendo type validation (int, bool, bytes, dict, list, None para sink_name; int, bool, bytes, dict, list para presentation_url), return value passthrough (6 métodos), multiple calls tracked, full lifecycle, enable with/without presentation_url, empty string, unicode, str subclass, type error no CDP call, no extra methods, order matches PDL.
- **Tests de integración**: **4 tests** en `tests/integration/test_headless_tethering_backgroundservice_cast.py` — enable/disable, enable with presentation_url, full lifecycle (enable→set_sink→start_desktop→start_tab→stop→disable), disable without enable.
- **E2E tests**: **17 tests** en `tests/e2e/test_cast_tethering_e2e.py` — type validation E2E (8 tests: int/bool/bytes/None para set_sink_to_use, int para start_desktop_mirroring/start_tab_mirroring/stop_casting, int para enable presentation_url, type error no CDP call), lifecycle E2E (5 tests: enable/disable, enable with presentation_url, disable without enable, enable twice, full lifecycle).
- **Total: 53 unit tests + 4 integration tests + 13 E2E tests = 70 tests** para el dominio Cast.

### Tethering (revisado contra PDL oficial + Go source cdproto)

- **2 comandos CDP** en PDL y Go source, **2 métodos** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `Tethering.pdl` (ChromeDevTools/devtools-protocol) + `tethering.go` (chromedp/cdproto).
- **Dominio experimental** — flag añadido a class docstring.
- **6 bugs encontrados y corregidos**:
  - `enable`: método espurio removido (no existe en PDL ni Go source). Enviaba `Tethering.enable` que no es un comando CDP válido.
  - `disable`: método espurio removido (no existe en PDL ni Go source). Enviaba `Tethering.disable` que no es un comando CDP válido.
  - `bind`: método faltante añadido (PDL: `Tethering.bind`, Go source: `Bind(port int64)`). Params: `port` (integer, requerido). Type validation: `isinstance(port, int) and not isinstance(port, bool)`.
  - `unbind`: método faltante añadido (PDL: `Tethering.unbind`, Go source: `Unbind(port int64)`). Params: `port` (integer, requerido). Type validation: `isinstance(port, int) and not isinstance(port, bool)`.
  - Module docstring y class docstring actualizados con evento del PDL: `Tethering.accepted` (params: `port` — integer, `connectionId` — string).
  - Descripción del dominio corregida: "port binding for incoming connections" → "browser port binding" (coincide con PDL: "The Tethering domain defines methods and events for browser port binding").
- **Eventos documentados**: `Tethering.accepted` (en module docstring y class docstring).
- **Tests unitarios**: **2 tests** básicos en `test_tier3f_domains.py` + **33 tests** edge en `test_tethering_edge.py` — cubriendo type validation (float, string, bool, None, list, dict para bind y unbind), return value passthrough (2 métodos), multiple calls tracked, full lifecycle, bind same port twice, unbind without bind, port zero, negative port, large port, int subclass, type error no CDP call, no extra methods, order matches PDL, no enable/disable methods exist.
- **Tests de integración**: **4 tests** en `tests/integration/test_headless_tethering_backgroundservice_cast.py` — bind/unbind, bind/unbind multiple ports, unbind without bind, bind same port twice.
- **E2E tests**: **12 tests** en `tests/e2e/test_cast_tethering_e2e.py` — type validation E2E (7 tests: float/string/bool/None para bind, float/string/bool para unbind, type error no CDP call), lifecycle E2E (4 tests: bind/unbind, unbind without bind, bind/unbind multiple ports, bind same port twice).
- **Total: 35 unit tests + 4 integration tests + 11 E2E tests = 50 tests** para el dominio Tethering.

### SmartCardEmulation (revisado contra PDL oficial + Go source cdproto)

- **12 comandos CDP** en PDL y Go source, **12 métodos** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `SmartCardEmulation.pdl` (ChromeDevTools/devtools-protocol) + `smart_card_emulation.go` (chromedp/cdproto).
- **Dominio experimental** — flag documentado en module y class docstring.
- **Orden de métodos corregido** para coincidir con PDL: `enable` → `disable` → `reportEstablishContextResult` → `reportReleaseContextResult` → `reportListReadersResult` → `reportGetStatusChangeResult` → `reportBeginTransactionResult` → `reportPlainResult` → `reportConnectResult` → `reportDataResult` → `reportStatusResult` → `reportError`.
- **5 bugs encontrados y corregidos**:
  - `report_get_status_change_result`: añadida validación de tipo de elementos de `reader_states` (cada elemento debe ser `dict`). Antes solo validaba que fuera `list` sin validar elementos.
  - Module docstring expandido con tipos del dominio en orden PDL (ResultCode, ShareMode, Disposition, ConnectionState, ReaderStateFlags, ProtocolSet, Protocol con valores enum `"t0"`/`"t1"`/`"raw"`, ReaderStateIn, ReaderStateOut), 14 eventos, y 12 comandos.
  - Class docstring expandido con lista completa de 14 eventos emitidos y flag experimental.
  - `Returns:` añadido a todos los docstrings de métodos (12/12).
  - Module docstring: `Protocol` ahora lista valores enum (`"t0"`, `"t1"`, `"raw"`) en lugar de solo el nombre del tipo.
- **Type validation estricta**: `request_id` (str), `context_id` (int, bool rechazado), `handle` (int, bool rechazado), `readers` (list[str] con validación de elementos), `reader_states` (list[dict] con validación de elementos), `active_protocol` (str, opcional), `data` (str), `reader_name` (str), `state` (str), `atr` (str), `protocol` (str, opcional), `result_code` (str).
- **Serialización**: params=None para enable/disable, camelCase keys exactas del PDL para todos los métodos, opcionales omitidos cuando son None.
- **Tests unitarios**: edge tests en `test_smart_card_emulation_edge.py` — method order, count, no spurious, inheritance, coroutines, signatures, type validation parametrizada, validation order, subclass acceptance, edge values, return passthrough, lifecycle, repeated cycles, concurrency, error propagation, docstring tests (module, class, returns, raises, args, no Activates/Deactivates).
- **Tests de integración**: en `tests/integration/test_missing_domains.py` — enable/disable con return dict, ciclo enable/disable, type errors para report_error, report_establish_context_result bool, report_list_readers_result elemento, report_get_status_change_result elemento.
- **E2E tests**: en `tests/e2e/test_smart_card_emulation_web_audio_e2e.py` — lifecycle, ciclo, type errors para múltiples métodos, bool rejection, element validation, no spurious methods.

### WebAudio (revisado contra PDL oficial + Go source cdproto)

- **3 comandos CDP** en PDL y Go source, **3 métodos** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `WebAudio.pdl` (ChromeDevTools/devtools-protocol) + `web_audio.go` (chromedp/cdproto).
- **Dominio experimental** — flag documentado en module y class docstring.
- **6 bugs encontrados y corregidos**:
  - `get_realtime_data`: añadida type validation para `context_id` (str, bool rechazado). Antes no tenía ninguna validación.
  - `enable`: docstring corregido de "Activates" a "Enables". Docstring ahora lista los 13 eventos del PDL.
  - `disable`: docstring corregido de "Deactivates" a "Disables".
  - `get_realtime_data`: docstring de Returns corregido — removidos campos inexistentes (`currentValue`, `currentTick`), añadidos campos correctos del PDL (`currentTime`, `renderCapacity`, `callbackIntervalMean`, `callbackIntervalVariance`).
  - Module docstring expandido con 13 tipos del dominio (GraphObjectId, ContextType, ContextState, ContextRealtimeData, BaseAudioContext, AudioListener, AudioNode, AudioParam, NodeType, ParamType, AutomationRate, ChannelCountMode, ChannelInterpretation), 13 eventos, 3 comandos.
  - Class docstring expandido con 13 eventos emitidos y flag experimental.
- **Type validation**: `context_id` (str, bool rechazado) con TypeError incluyendo nombre del parámetro y tipo real.
- **Serialización**: params=None para enable/disable, `contextId` key para get_realtime_data.
- **Tests unitarios**: edge tests en `test_web_audio_edge.py` — method order, count, no spurious, inheritance, coroutines, signatures, type validation parametrizada (10 tipos), return passthrough, lifecycle, repeated cycles, concurrency, error propagation, docstring tests (module, class, returns, args, raises, no Activates/Deactivates, no wrong fields, correct fields).
- **Tests de integración**: en `tests/integration/test_missing_domains.py` — enable/disable con return dict, ciclo, get_realtime_data con contexto real, type errors, bool rejection.
- **E2E tests**: en `tests/e2e/test_smart_card_emulation_web_audio_e2e.py` — lifecycle, ciclo, type errors, bool rejection, None rejection, empty string, get_realtime_data con contexto real, no spurious methods.

### WebMCP (revisado contra PDL oficial + Go source cdproto)

- **2 comandos CDP** en PDL (`enable`, `disable`), **2 métodos** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `WebMCP.pdl` (ChromeDevTools/devtools-protocol, v0.0.1612613).
- **Dominio experimental** — flag documentado en module y class docstring.
- **Depends on**: Runtime, Page, DOM — documentado en module docstring.
- **3 tipos del PDL**: `Annotation` (object), `InvocationStatus` (enum: "Success", "Canceled", "Error"), `Tool` (object) — listados en module docstring en orden PDL.
- **4 eventos del PDL**: `toolsAdded`, `toolsRemoved`, `toolInvoked`, `toolResponded` — listados en module y class docstring con params.
- **7 bugs encontrados y corregidos**:
  - `invoke_tool`: método espurio removido (no existe en el PDL — `WebMCP.invokeTool` no es un comando CDP).
  - `cancel_invocation`: método espurio removido (no existe en el PDL — `WebMCP.cancelInvocation` no es un comando CDP).
  - Module docstring: añadidos tipos (Annotation, InvocationStatus, Tool), comandos (enable, disable), eventos (toolsAdded, toolsRemoved, toolInvoked, toolResponded), flag experimental, dependencias (Runtime, Page, DOM).
  - Class docstring: añadidos 4 eventos con params, flag experimental. `enable` docstring mejorado con descripción de trigger de `toolsAdded`. `disable` y `enable` ahora tienen sección `Returns:`.
  - Module docstring: corregido "tool invocation" → "monitoring tool registration and invocation" — después de remover los métodos espurios `invoke_tool` y `cancel_invocation`, la descripción del módulo ya no coincide con la funcionalidad real (solo enable/disable, no invocación).
  - `client.py` property docstring: corregido "Web MCP tool invocation" → "Web MCP monitoring" — el docstring de la propiedad `web_mcp` en `CDPSession` quedó stale después de remover los métodos espurios.
  - `test_p2_features.py`: tests stale para `invoke_tool` y `cancel_invocation` (métodos espurios ya removidos) — eliminados 8 tests que referenciaban métodos inexistentes, añadido `test_disable` que faltaba.
- **Serialización**: `enable` y `disable` usan `params=None` (sin parámetros en PDL).
- **Tests unitarios**: edge tests en `test_web_mcp_edge.py` (50 tests) — method order/count, no spurious methods (explicit invoke_tool/cancel_invocation/invokeTool/cancelInvocation), BaseDomain inheritance, coroutines, signatures, serialization (params=None), return passthrough (empty dict, with data), lifecycle (enable/disable, repeated cycles, disable without enable, enable twice, alternating, multi-call tracking), concurrency, error propagation (CommandError), docstring tests (module describe, module experimental, module dependencies, module events in PDL order, module commands in PDL order, module types in PDL order, module monitoring, class describe, class events, class experimental, class subscription hint, enable Returns, enable toolsAdded trigger, disable Returns, no Activates/Deactivates).
- **Tests de integración**: en `tests/integration/test_webmcp_crashreport_digitalcredentials.py` — enable/disable con CommandError suppress, ciclo enable/disable, disable without enable, enable returns dict, alternating enable/disable, disable returns dict, no spurious methods.
- **E2E tests**: en `tests/e2e/test_webmcp_crashreport_digitalcredentials_e2e.py` — lifecycle enable/disable, ciclo, disable without enable, enable returns dict, alternating enable/disable, no spurious methods (invoke_tool, cancel_invocation, invokeTool, cancelInvocation), CommandError cuando experimental no disponible.

### CrashReportContext (revisado contra PDL oficial + Go source cdproto)

- **1 comando CDP** en PDL (`getEntries`), **1 método** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `CrashReportContext.pdl` (ChromeDevTools/devtools-protocol, v0.0.1612613).
- **Dominio experimental** — flag documentado en module y class docstring.
- **Depends on**: Page — documentado en module docstring.
- **1 tipo del PDL**: `CrashReportContextEntry` (object) — listado en module docstring.
- **0 eventos** — documentado en module docstring.
- **3 bugs encontrados y corregidos**:
  - Module docstring: añadidos tipo (CrashReportContextEntry), comando (getEntries), eventos (none), flag experimental, dependencia (Page).
  - Class docstring: añadido flag experimental. Descripción mejorada de "Provides access" a "Exposes the current state of the CrashReportContext API".
  - `get_entries`: return docstring mejorado — ahora documenta `entries` como lista de `CrashReportContextEntry` con campos `key` (string), `value` (string), `frameId` (Page.FrameId).
- **Serialización**: `get_entries` usa `params=None` (sin parámetros en PDL).
- **Tests unitarios**: edge tests en `test_crash_report_context_edge.py` (37 tests) — method order/count, no spurious methods (explicit enable/disable/clear/set_entries), BaseDomain inheritance, coroutines, signatures, serialization (params=None), return passthrough (empty entries, entries with data, three entries, unicode values, empty response, extra fields), lifecycle (repeated calls), concurrency, error propagation (CommandError, RuntimeError), docstring tests (module describe, module experimental, module dependencies, module types, module commands, module no-events, class describe, class experimental, Returns, entries described, key/value/frameId fields, no deprecated wording).
- **Tests de integración**: en `tests/integration/test_webmcp_crashreport_digitalcredentials.py` — get_entries con return dict, get_entries repeated, get_entries entries list structure (key/value/frameId), no spurious methods.
- **E2E tests**: en `tests/e2e/test_webmcp_crashreport_digitalcredentials_e2e.py` — get_entries, get_entries repeated, get_entries returns dict type, no spurious methods (enable/disable/set_entries), CommandError cuando experimental no disponible.

### DigitalCredentials (revisado contra PDL oficial + Go source cdproto)

- **1 comando CDP** en PDL (`setVirtualWalletBehavior`), **1 método** en cdpwave (0 extra, 0 faltantes).
- **Verificado contra**: `DigitalCredentials.pdl` (ChromeDevTools/devtools-protocol, v0.0.1612613).
- **Dominio experimental** — flag documentado en module y class docstring.
- **1 tipo del PDL**: `VirtualWalletAction` (enum: "respond", "decline", "wait", "clear") — listado en module docstring.
- **0 eventos** — documentado en module docstring.
- **11 bugs encontrados y corregidos**:
  - `set_virtual_wallet_behavior`: parámetro `behavior` renombrado a `action` (coincide con PDL `VirtualWalletAction action`). Antes enviaba `{"behavior": ...}` que no existe en CDP.
  - `set_virtual_wallet_behavior`: añadido parámetro `protocol` (str, optional) — existe en PDL como `optional string protocol`.
  - `set_virtual_wallet_behavior`: añadido parámetro `response` (dict, optional) — existe en PDL como `optional object response`.
  - `set_virtual_wallet_behavior`: añadido parámetro `frame_id` (str, optional) — existe en PDL como `optional Page.FrameId frameId`.
  - `set_virtual_wallet_behavior`: añadida type validation estricta para `action` (str), `protocol` (str), `response` (dict), `frame_id` (str) — rechaza bool, int, float, bytes, list, dict según corresponda. Antes no tenía ninguna validación.
  - Module docstring: añadidos tipo (VirtualWalletAction), comando (setVirtualWalletBehavior), eventos (none), flag experimental.
  - Class docstring: añadido flag experimental. `set_virtual_wallet_behavior` docstring ahora tiene Args (con enum values: respond, decline, wait, clear), Returns, Raises.
  - `set_virtual_wallet_behavior` docstring: removido "Required when action is respond, forbidden otherwise" de `protocol` y `response` — el PDL solo los marca como `optional` sin condiciones, y el código no enforcea ninguna restricción condicional. La documentación era misleading.
  - `set_virtual_wallet_behavior`: añadida enum value validation para `action` con `ValueError` — valida que `action` sea uno de `"respond"`, `"decline"`, `"wait"`, `"clear"` (VirtualWalletAction enum del PDL). Sigue el patrón de Memory, Tracing y WebAuthn. Antes solo validaba `isinstance(action, str)` sin verificar el valor.
  - `test_p2_features.py`: test stale usaba API pre-fix `set_virtual_wallet_behavior("default")` con `{"behavior": "default"}` — actualizado a `set_virtual_wallet_behavior("decline")` con `{"action": "decline"}`.
  - `test_missing_domains.py`: test stale usaba `set_virtual_wallet_behavior("default")` — `"default"` no es valor enum válido (lanza `ValueError` después de bug #9). Actualizado a `"decline"`.
- **Serialización**: `action` siempre enviado. `protocol`, `response`, `frameId` omitidos cuando son None. Key usa camelCase `frameId` (no `frame_id`).
- **Tests unitarios**: edge tests en `test_digital_credentials_edge.py` (107 tests) — method order/count, no spurious methods (explicit enable/disable/get/set_behavior), BaseDomain inheritance, coroutines, signatures (params, order, defaults), serialization (action only, with protocol, with response, with frame_id, all params, optionals omitted, camelCase, protocol+response without frame_id, response+frame_id without protocol, protocol+frame_id without response, params dict not None), return passthrough, type validation parametrizada (action: int/bool/float/bytes/dict/list/None/tuple/set; protocol: int/bool/float/bytes/list/dict/tuple/set/None accepted; response: int/str/bool/list/float/bytes/tuple/set/None accepted; frame_id: int/bool/float/bytes/dict/list/tuple/set/None accepted; dict subclass accepted), validation order (action before protocol before response before frame_id, cross-skip action→frame_id, protocol→frame_id, action→response), subclass acceptance (str subclass for action/protocol/frame_id, dict subclass for response), edge values (empty string, unicode, None optionals, empty response dict, nested response dict, response with list/int/bool values, long strings 1000 chars), all 4 enum values parametrized, concurrency (with all params), error propagation (CommandError, TypeError), repeated calls tracked, docstring tests (module describe, module experimental, module no-events, module types, module commands, class describe, class experimental, class virtual wallet, method Args, method Returns, method Raises, method enum values, method protocol requirement, method response requirement, method frame_id, no Activates/Deactivates).
- **Tests de integración**: en `tests/integration/test_webmcp_crashreport_digitalcredentials.py` — set_virtual_wallet_behavior decline/respond con protocol/response/frame_id, all 4 enum values parametrized, all params combined, type errors (action int/bool/float/bytes/dict/list, protocol int/bool/float/bytes/list, response int/bool/list, frame_id int/bool/float/bytes/dict/list), no CDP call on TypeError, repeated calls, no spurious methods.
- **E2E tests**: en `tests/e2e/test_webmcp_crashreport_digitalcredentials_e2e.py` — lifecycle (decline, respond con protocol, respond con response, con frame_id, repeated calls, all 4 enum values parametrized, all params combined, unicode action, empty string action), type validation (action int/bool/float/bytes/dict/list, protocol int/bool/float/bytes, response int/bool/list, frame_id int/bool/float/bytes/dict/list, no CDP call on TypeError), no spurious methods (enable/disable/get/set_behavior), CommandError cuando experimental no disponible.

### Total bugs corregidos en esta revisión: 21

| Dominio | Bugs | Métodos PDL | Métodos impl | Extra | Faltante |
|---|---:|---:|---:|---:|---:|
| WebMCP | 7 | 2 | 2 | 0 | 0 |
| CrashReportContext | 3 | 1 | 1 | 0 | 0 |
| DigitalCredentials | 11 | 1 | 1 | 0 | 0 |
| **Total** | **21** | **4** | **4** | **0** | **0** |
