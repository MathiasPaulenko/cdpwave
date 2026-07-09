# FIX-ROADMAP

This document tracks bugs found during testing of the cdpwave library.

## Bug Format

Each bug entry includes:

- **Bug ID**: Unique identifier (e.g., BUG-001)
- **Domain**: Affected CDP domain
- **Severity**: Critical/High/Medium/Low
- **Description**: Brief description of the bug
- **Steps to Reproduce**: How to reproduce the bug
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Status**: Open/In Progress/Fixed
- **Fix Details**: Description of the fix (when fixed)

---

## BUG-007: `Emulation.set_emulated_media` usada incorrectamente en TC-MAN-029

- **Bug ID**: BUG-007
- **Domain**: Emulation
- **Severity**: Medium
- **Description**: TC-MAN-029 llama `set_emulated_media("prefers-color-scheme", "dark")` pero la firma es `set_emulated_media(media="", features=None)`. Para emular `prefers-color-scheme: dark` se debe usar `set_emulated_media(features=[{"name": "prefers-color-scheme", "value": "dark"}])`.
- **Steps to Reproduce**: `await session.emulation.set_emulated_media("prefers-color-scheme", "dark")`
- **Expected Behavior**: Activar dark mode.
- **Actual Behavior**: Pasa "prefers-color-scheme" como `media` (tipo de medio) y "dark" como `features` (lista) — TypeError.
- **Status**: Open
- **Fix Details**: Corregir el test. Considerar añadir convenience method `set_emulated_media_feature(name, value)`.

---

## BUG-010: `Runtime.compile_script` no acepta `return_by_value`

- **Bug ID**: BUG-010
- **Domain**: Runtime
- **Severity**: Low
- **Description**: TC-MAN-033 llama `compile_script("1 + 2 + 3", return_by_value=True)` pero `compile_script` no tiene ese parámetro. Además falta `persist_script=True` para que `run_script` funcione.
- **Steps to Reproduce**: `await session.runtime.compile_script("1+2+3", return_by_value=True)`
- **Expected Behavior**: Compilar script y poder ejecutarlo después.
- **Actual Behavior**: TypeError — `return_by_value` no es un parámetro válido.
- **Status**: Open
- **Fix Details**: Corregir el test: `compile_script("1+2+3", persist_script=True)` y luego `run_script(scriptId, return_by_value=True)`.

---

## BUG-013: `Input.dispatch_mouse_event` — orden de parámetros en TC-MAN-003

- **Bug ID**: BUG-013
- **Domain**: Input
- **Severity**: Low
- **Description**: TC-MAN-003 llama `dispatch_mouse_event("mousePressed", "left", x, y)` pero la firma es `dispatch_mouse_event(type, x, y, button="none", ...)`. `"left"` se pasa como `x`.
- **Steps to Reproduce**: `await session.input.dispatch_mouse_event("mousePressed", "left", 100, 200)`
- **Expected Behavior**: Click con botón izquierdo en (100, 200).
- **Actual Behavior**: Pasa "left" como coordenada x — TypeError o comportamiento incorrecto.
- **Status**: Open
- **Fix Details**: Corregir el test a `dispatch_mouse_event("mousePressed", 100, 200, button="left")`.

---

## BUG-014: `Page.print_to_pdf` retorna `str` en modo base64, no `dict`

- **Bug ID**: BUG-014
- **Domain**: Page
- **Severity**: Medium
- **Description**: TC-MAN-004 asume que `print_to_pdf` retorna un dict con clave `data`, pero retorna directamente un `str` cuando `return_as_stream=False`. Esto es inconsistente con `capture_screenshot` que retorna dict.
- **Steps to Reproduce**: `pdf = await session.page.print_to_pdf(); pdf["data"]`
- **Expected Behavior**: Retornar dict con `{"data": "base64..."}`.
- **Actual Behavior**: Retorna `str` directamente — `pdf["data"]` falla con TypeError.
- **Status**: Open
- **Fix Details**: Hacer que `print_to_pdf` retorne siempre dict para consistencia, o documentar claramente.

---

## BUG-016: `Emulation.set_idle_override` envía parámetros inválidos a CDP

- **Bug ID**: BUG-016
- **Domain**: Emulation
- **Severity**: High
- **Description**: TC-MAN-047 ejecuta `set_idle_override(is_user_active=False, is_screen_active=False)` y Chrome retorna `[-32602] Invalid parameters`. El comando CDP `Emulation.setIdleOverride` fue **deprecado/removido** en versiones modernas de Chrome.
- **Steps to Reproduce**: `await session.emulation.set_idle_override(is_user_active=False, is_screen_active=False)`
- **Expected Behavior**: Override del idle state del navegador.
- **Actual Behavior**: `CommandError: [-32602] Invalid parameters`.
- **Status**: Open
- **Fix Details**: El comando `Emulation.setIdleOverride` fue removido en Chrome 120+. La librería debería documentar esto o usar el comando alternativo `Emulation.setEmulatedIdleState` (que es el reemplazo).

---

## BUG-018: `Fetch.enable` con patrón broad bloquea `Page.navigate` indefinidamente

- **Bug ID**: BUG-018
- **Domain**: Fetch
- **Severity**: High
- **Description**: TC-MAN-005 y TC-MAN-043: cuando `Fetch.enable` intercepta requests con patrón `*://*/*` o `*://example.com/*`, el `Page.navigate` hace timeout porque la request queda pausada esperando `continue_request`/`fulfill_request`, pero el evento `Fetch.requestPaused` llega **después** de que navigate ya hizo timeout.
- **Steps to Reproduce**:
  ```python
  await session.fetch.enable(patterns=[{"urlPattern": "*://*/*"}])
  await session.page.navigate("https://example.com")  # timeout
  ```
- **Expected Behavior**: Navigate debería completarse (o al menos no bloquear) cuando Fetch está interceptando.
- **Actual Behavior**: `CommandTimeoutError: Command timeout: Page.navigate` después de 30s.
- **Status**: Open
- **Fix Details**: El problema es de ordering: navigate se envía antes de que el handler de `requestPaused` esté listo. Solución: usar `wait_for_event("Fetch.requestPaused")` antes de navegar, o navegar con timeout corto y manejar el request paused después. La librería debería documentar este patrón o proporcionar un helper.

---

## BUG-019: `Runtime.evaluate` con bucle infinito corrompe la sesión entera

- **Bug ID**: BUG-019
- **Domain**: Runtime
- **Severity**: High
- **Description**: TC-MAN-015: `Runtime.evaluate("while(true){}")` hace timeout (esperado), pero después de el timeout, **todos los comandos posteriores a la sesión también hacen timeout**. La sesión queda en estado corrupto porque Chrome sigue ejecutando el script infinito y no puede procesar nuevos comandos.
- **Steps to Reproduce**:
  ```python
  await asyncio.wait_for(session.runtime.evaluate("while(true){}"), timeout=2.0)
  # TimeoutError raised (expected)
  await session.runtime.evaluate("1+1")  # Also times out!
  ```
- **Expected Behavior**: Después del timeout, la sesión debería seguir funcional.
- **Actual Behavior**: Todos los comandos posteriores hacen timeout. La sesión queda inservible.
- **Status**: Open
- **Fix Details**: No hay fix sencillo en la librería — Chrome no puede interrumpir JS en ejecución. Soluciones: (1) documentar que un bucle infinito corrompe la sesión, (2) añadir `Runtime.terminateExecution` (si existe en CDP), (3) crear una sesión nueva automáticamente.

---

## BUG-020: `Page.get_navigation_history` — redirecciones crean entries extra

- **Bug ID**: BUG-020
- **Domain**: Page
- **Severity**: Low
- **Description**: TC-MAN-012: al navegar a `https://www.google.com`, Google redirige de HTTP a HTTPS, creando un entry extra en el historial. El test asume `currentIndex == 1` pero obtiene `2`.
- **Steps to Reproduce**: Navegar a `https://example.com` luego a `https://www.google.com`, comprobar `get_navigation_history()["currentIndex"]`.
- **Expected Behavior**: `currentIndex == 1` (dos navegaciones).
- **Actual Behavior**: `currentIndex == 2` (tres entries por la redirección de Google).
- **Status**: Open
- **Fix Details**: Bug en el test, no en la librería. Usar un sitio sin redirecciones (ej. `https://example.org`).

---

## BUG-021: Eventos de sesión cerrada se reciben sin dispatcher

- **Bug ID**: BUG-021
- **Domain**: Client
- **Severity**: Low
- **Description**: Al cerrar una sesión y crear una nueva, los eventos de la sesión cerrada (ej. `Page.domContentEventFired`, `Page.loadEventFired`) se siguen recibiendo pero no encuentran dispatcher, generando warnings: `Event Page.domContentEventFired for unknown session`.
- **Steps to Reproduce**: Cerrar una sesión mientras una navegación está en progreso, luego crear una nueva sesión.
- **Expected Behavior**: Los eventos de la sesión cerrada deberían ser ignorados silenciosamente.
- **Actual Behavior**: Se loguea warning por cada evento de la sesión cerrada.
- **Status**: Open
- **Fix Details**: El warning ya se maneja en `client.py:584` con `logger.warning()`. Podría cambiarse a `logger.debug()` para reducir ruido, o verificar si la sesión fue cerrada intencionalmente antes de loguear.

---

## BUG-022: `tc_021` no acepta argumento `client` — error en runner

- **Bug ID**: BUG-022
- **Domain**: Test
- **Severity**: Low
- **Description**: TC-MAN-021 está definida como `async def tc_021()` (sin argumentos) pero el runner le pasa `client`. Esto causa `TypeError: tc_021() takes 0 positional arguments but 1 was given`.
- **Steps to Reproduce**: Ejecutar el runner de tests.
- **Expected Behavior**: El test se skip sin error.
- **Actual Behavior**: `TypeError` no capturado.
- **Status**: Open
- **Fix Details**: Cambiar firma a `async def tc_021(client: CDPClient) -> None`.

---

## BUG-031: `CacheStorageDomain` no tiene método `enable`

- **Bug ID**: BUG-031
- **Domain**: CacheStorage
- **Severity**: Medium
- **Description**: `CacheStorageDomain` no tiene método `enable()` ni `disable()`. El comando CDP `CacheStorage.enable` no existe — el dominio no requiere enable/disable. Además los tests TC-CS-002 a TC-CS-007 fallan con traceback porque intentan usar `s.cache_storage` que no está inicializado correctamente (falta `await s.dom.enable()` antes).
- **Steps to Reproduce**: `await session.cache_storage.enable()`
- **Expected Behavior**: El dominio funciona sin enable/disable.
- **Actual Behavior**: `AttributeError: 'CacheStorageDomain' object has no attribute 'enable'`
- **Status**: Open
- **Fix Details**: Corregir los tests para no llamar `enable()`. Los comandos `requestCacheNames`, `requestEntries`, etc. funcionan directamente.

---

## BUG-032: `OverlayDomain` requiere `DOM.enable()` antes de usarse

- **Bug ID**: BUG-032
- **Domain**: Overlay
- **Severity**: Medium
- **Description**: `Overlay.enable` falla con `[-32000] DOM should be enabled first` si no se ha llamado `DOM.enable()` antes. Los tests TC-OVERLAY-001 a TC-OVERLAY-015 fallan con traceback porque no habilitan DOM primero.
- **Steps to Reproduce**: `await session.overlay.enable()` sin `await session.dom.enable()` antes.
- **Expected Behavior**: Overlay funciona independientemente.
- **Actual Behavior**: `CommandError: [-32000] DOM should be enabled first`
- **Status**: Open
- **Fix Details**: Corregir tests para llamar `dom.enable()` antes de `overlay.enable()`.

---

## BUG-033: `CSSDomain.enable` requiere `DOM.enable()` antes

- **Bug ID**: BUG-033
- **Domain**: CSS
- **Severity**: Low
- **Description**: `CSS.enable` falla con `[-32000] DOM agent needs to be enabled first.` si DOM no está habilitado.
- **Steps to Reproduce**: `await session.css.enable()` sin `await session.dom.enable()` antes.
- **Expected Behavior**: CSS funciona independientemente o documenta la dependencia.
- **Actual Behavior**: `CommandError: [-32000] DOM agent needs to be enabled first.`
- **Status**: Open
- **Fix Details**: Documentar que DOM debe estar habilitado antes de CSS, o auto-habilitar DOM internamente.

---

## BUG-034: `StorageDomain` — comandos DOM Storage no disponibles

- **Bug ID**: BUG-034
- **Domain**: Storage
- **Severity**: Medium
- **Description**: Los comandos `Storage.enable`, `Storage.getDOMStorageItems`, `Storage.setDOMStorageItem`, `Storage.removeDOMStorageItem`, `Storage.clearDOMStorageItems` no existen en Chrome moderno (retornan `[-32601] wasn't found`). El dominio Storage no requiere enable/disable.
- **Steps to Reproduce**: `await session.storage.enable()`
- **Expected Behavior**: Comandos disponibles.
- **Actual Behavior**: `CommandError: [-32601] 'Storage.enable' wasn't found`
- **Status**: Open
- **Fix Details**: Los comandos de DOM Storage fueron movidos a `DOMStorage` domain en Chrome moderno. Implementar `DOMStorageDomain` o usar `session.send("DOMStorage.*")`.

---

## BUG-036: Múltiples dominios CDP removidos en Chrome moderno (24 métodos)

- **Bug ID**: BUG-036
- **Domain**: Multiple
- **Severity**: Low
- **Description**: Los siguientes comandos CDP ya no existen en Chrome moderno (retornan `[-32601] wasn't found`):
  - `Target.initiateTargetShutdown`
  - `DOM.getInnerHTML`
  - `Emulation.clearDefaultBackgroundColorOverride`
  - `Emulation.setDisabledSensors`
  - `Emulation.setScrollPosition`
  - `Emulation.setFocusEmulationEnabled`
  - `Emulation.setEmulatedVisionDeficiency` / `clearEmulatedVisionDeficiency`
  - `Emulation.clearAutoDarkModeOverride`
  - `Overlay.setShowDevTools`
  - `Debugger.setBreakpointActive`
  - `Log.getViolationsReport`
  - `Profiler.startTypeProfile` / `stopTypeProfile`
  - `HeapProfiler.addHeapSnapshotChunk` / `getLastSeenObjectId`
  - `Security.getVisibleSecurityState`
  - `Accessibility.getAXNode` / `getImageData`
  - `Animation.pause` / `resume`
  - `IndexedDB.deleteObjectStore`
  - `ServiceWorker.update` / `inspectWorker` / `getWorkers` / `getMessages`
  - `Cast.stopTabMirroring`
  - `DOMDebugger.getDOMBreakpoints`
  - `Extensions.checkForAllowedExtensions`
  - `HeadlessExperimental.beginFrame` / `disable`
  - `Inspector.detach` / `reload`
  - `LayerTree.getTree` / `setShowPaints`
  - `Media.setPlayerMessageHandler` / `setPlayerBreakpoint` / `clearPlayerEvents`
  - `Preload.setPrefetchLogging`
  - `PWA.install` / `uninstall` / `launch`
  - `Sensor.enable` / `setSensorOverride` / `clearSensorOverride`
  - `Tethering.bind` / `unbind`
  - `Tracing.requestClockSyncMarker`
  - `Worker.enable` / `disable`
- **Steps to Reproduce**: Ejecutar cualquier comando listado arriba.
- **Expected Behavior**: Comando disponible.
- **Actual Behavior**: `CommandError: [-32601] 'X.method' wasn't found`
- **Status**: Open
- **Fix Details**: Documentar estos comandos como no disponibles en Chrome moderno. Considerar lanzar un error descriptivo en lugar de enviar al browser.

---

## BUG-037: `SystemInfo` solo funciona en browser target

- **Bug ID**: BUG-037
- **Domain**: SystemInfo
- **Severity**: Low
- **Description**: Los comandos `SystemInfo.getInfo`, `getProcessInfo`, `getGPUInfo`, `getDisplayInfo` solo funcionan en el browser target, no en page targets.
- **Steps to Reproduce**: `await session.system_info.get_info()` desde una sesión de página.
- **Expected Behavior**: Funcionar desde cualquier sesión o documentar la limitación.
- **Actual Behavior**: `CommandError: [-32000] SystemInfo.getInfo is only supported on the browser target`
- **Status**: Open
- **Fix Details**: Usar `client.browser.send("SystemInfo.getInfo")` o documentar que debe usarse desde browser target.

---

## BUG-040: `Emulation.set_script_execution_disabled` — parámetros inválidos

- **Bug ID**: BUG-040
- **Domain**: Emulation
- **Severity**: Medium
- **Description**: `Emulation.setScriptExecutionDisabled` retorna `[-32602] Invalid parameters` cuando se le pasa `True`. El comando CDP espera un valor booleano pero la librería podría estar enviándolo incorrectamente.
- **Steps to Reproduce**: `await session.emulation.set_script_execution_disabled(True)`
- **Expected Behavior**: Deshabilitar ejecución de JavaScript.
- **Actual Behavior**: `CommandError: [-32602] Invalid parameters`
- **Status**: Open
- **Fix Details**: Verificar que el parámetro se envía como booleano nativo en el JSON.

---

## BUG-041: `Emulation.set_device_metrics_override` con `display_feature` — parámetros inválidos

- **Bug ID**: BUG-041
- **Domain**: Emulation
- **Severity**: Low
- **Description**: `set_device_metrics_override` con `display_feature` retorna `[-32602] Invalid parameters`. El formato del `display_feature` puede no ser correcto.
- **Steps to Reproduce**: `await session.emulation.set_device_metrics_override(width=400, height=800, device_scale_factor=1, mobile=True, display_feature={"orientation":"vertical", "offset":0, "maskLength":200, "maskThickness":2})`
- **Expected Behavior**: Configurar display feature.
- **Actual Behavior**: `CommandError: [-32602] Invalid parameters`
- **Status**: Open
- **Fix Details**: Verificar el formato esperado de `display_feature` en el protocolo CDP.

---

## BUG-042: Tests de Fetch interception fallan por timing de eventos

- **Bug ID**: BUG-042
- **Domain**: Fetch
- **Severity**: High
- **Description**: TC-FETCH-002 a TC-FETCH-004, TC-INT-008, TC-MAN-005, TC-MAN-025 fallan con traceback porque los tests intentan usar `fail_request`/`fulfill_request`/`continue_request` con `request_id` antes de que el evento `Fetch.requestPaused` haya llegado. El patrón de esperar el evento antes de actuar no está implementado en los tests.
- **Steps to Reproduce**: Ejecutar cualquier test de Fetch interception.
- **Expected Behavior**: El test espera el evento `requestPaused` y luego actúa.
- **Actual Behavior**: `KeyError` o `AttributeError` porque `request_id` no está disponible.
- **Status**: Open
- **Fix Details**: Corregir los tests para usar `session.wait_for_event("Fetch.requestPaused")` antes de llamar `fail_request`/`fulfill_request`/`continue_request`.

---

## BUG-044: Tests de CSS fallan por dependencia de DOM y inicialización

- **Bug ID**: BUG-044
- **Domain**: CSS
- **Severity**: Low
- **Description**: TC-CSS-005, TC-CSS-007 a TC-CSS-010, TC-CSS-014 fallan con traceback. Los tests no habilitan `DOM.enable()` antes de `CSS.enable()` y no obtienen `node_id` válido antes de llamar métodos que lo requieren.
- **Steps to Reproduce**: Ejecutar cualquier test de CSS que requiere node_id.
- **Expected Behavior**: Los tests obtienen un node_id válido primero.
- **Actual Behavior**: Traceback por falta de inicialización.
- **Status**: Open
- **Fix Details**: Corregir los tests para habilitar DOM, obtener document, y luego usar CSS.

---

## BUG-045: Tests de CacheStorage fallan por falta de inicialización

- **Bug ID**: BUG-045
- **Domain**: CacheStorage
- **Severity**: Low
- **Description**: TC-CS-002 a TC-CS-007 fallan con traceback. Los tests intentan usar `cache_storage` sin habilitar DOM primero y sin navegar a una página con cache storage.
- **Steps to Reproduce**: Ejecutar cualquier test de CacheStorage.
- **Expected Behavior**: Los tests navegan a una página con service worker / cache.
- **Actual Behavior**: Traceback por falta de inicialización.
- **Status**: Open
- **Fix Details**: Corregir los tests para navegar a una página apropiada antes de probar CacheStorage.

---

## BUG-046: Tests de Sensor fallan porque `Sensor.enable` no existe

- **Bug ID**: BUG-046
- **Domain**: Sensor
- **Severity**: Low
- **Description**: TC-SENSOR-002 a TC-SENSOR-004 fallan con traceback. El dominio `Sensor` no está disponible en Chrome moderno. Los tests deberían skip en lugar de error.
- **Steps to Reproduce**: Ejecutar cualquier test de Sensor.
- **Expected Behavior**: Skip del test.
- **Actual Behavior**: Traceback.
- **Status**: Open
- **Fix Details**: Corregir los tests para catch `CommandError` y marcar como SKIP.

---

## BUG-047: Tests de integración multi-tab fallan por timing

- **Bug ID**: BUG-047
- **Domain**: Integration
- **Severity**: Medium
- **Description**: TC-INT-006 y TC-MAN-009 fallan porque `assert r1["result"]` no encuentra la clave esperada en la respuesta de navegación. El formato de respuesta puede variar.
- **Steps to Reproduce**: Ejecutar test multi-tab.
- **Expected Behavior**: La navegación retorna el formato esperado.
- **Actual Behavior**: `KeyError` o `AssertionError`.
- **Status**: Open
- **Fix Details**: Corregir los tests para manejar el formato de respuesta correctamente.

---

## BUG-048: `Page.crash` hace timeout en headless

- **Bug ID**: BUG-048
- **Domain**: Page
- **Severity**: Low
- **Description**: TC-PAGE-021: `Page.crash` hace timeout en modo headless. El comando envía crash al renderer pero no retorna respuesta (el proceso muere antes).
- **Steps to Reproduce**: `await session.page.crash()`
- **Expected Behavior**: El comando retorna o la sesión se cierra.
- **Actual Behavior**: `CommandTimeoutError: Command timeout: Page.crash`
- **Status**: Open
- **Fix Details**: Documentar que `Page.crash` puede no retornar respuesta. Usar timeout corto y catch `CommandTimeoutError`.

---

## BUG-049: `Page.navigate_to_history_entry` — error en test por falta de historial

- **Bug ID**: BUG-049
- **Domain**: Page
- **Severity**: Low
- **Description**: TC-PAGE-030 falla con traceback porque intenta navegar a una entry de historial que no existe (índice fuera de rango).
- **Steps to Reproduce**: Navegar a history entry sin suficientes entries.
- **Expected Behavior**: Error descriptivo.
- **Actual Behavior**: Traceback.
- **Status**: Open
- **Fix Details**: Corregir el test para verificar que hay suficientes entries antes de navegar.

---

## BUG-050: `Runtime.get_exception_details` — error en test

- **Bug ID**: BUG-050
- **Domain**: Runtime
- **Severity**: Low
- **Description**: TC-RUNTIME-019 y TC-RUNTIME-023 fallan con traceback. Los tests intentan obtener exception details pero el método o los parámetros no son correctos.
- **Steps to Reproduce**: Ejecutar test get_exception_details.
- **Expected Behavior**: Retornar details de la excepción.
- **Actual Behavior**: Traceback.
- **Status**: Open
- **Fix Details**: Corregir los tests para usar el método correcto con parámetros válidos.

---

## BUG-052: `Target.set_auto_attach` — error en test

- **Bug ID**: BUG-052
- **Domain**: Target
- **Severity**: Low
- **Description**: TC-TARGET-007 falla con traceback al llamar `set_auto_attach`. El test puede no estar pasando los parámetros correctos.
- **Steps to Reproduce**: `await session.target.set_auto_attach(auto_attach=True, wait_forDebuggerOnStart=False)`
- **Expected Behavior**: Configurar auto-attach.
- **Actual Behavior**: Traceback.
- **Status**: Open
- **Fix Details**: Corregir el test o el método en `cdpwave/domains/target.py`.

---

## BUG-054: `WebAuthn` — authenticator ID no se persiste entre tests

- **Bug ID**: BUG-054
- **Domain**: WebAuthn
- **Severity**: Low
- **Description**: TC-WA-003 a TC-WA-010 fallan porque el authenticator ID creado en TC-WA-002 no está disponible en tests posteriores (cada test usa sesión nueva).
- **Steps to Reproduce**: Crear authenticator en un test, usarlo en otro.
- **Expected Behavior**: Authenticator disponible.
- **Actual Behavior**: `CommandError: [-32602] Could not find a Virtual Authenticator matching the ID`
- **Status**: Open
- **Fix Details**: Cada test debe crear su propio authenticator. Corregir los tests.

---

## Resumen

| ID | Severidad | Tipo | Descripción |
|----|-----------|------|-------------|
| BUG-007 | Medium | Test | `set_emulated_media` confusa para features |
| BUG-010 | Low | Test | `compile_script` no acepta `return_by_value` |
| BUG-013 | Low | Test | Orden de params en `dispatch_mouse_event` |
| BUG-014 | Medium | API | `print_to_pdf` retorna `str`, no `dict` |
| BUG-016 | High | Runtime | `set_idle_override` deprecado en Chrome moderno |
| BUG-018 | High | Runtime | `Fetch.enable` bloquea `Page.navigate` |
| BUG-019 | High | Runtime | `while(true){}` corrompe sesión entera |
| BUG-020 | Low | Test | Redirecciones crean entries extra en historial |
| BUG-021 | Low | Logging | Warnings innecesarios de eventos de sesión cerrada |
| BUG-022 | Low | Test | `tc_021` no acepta argumento `client` |
| BUG-031 | Medium | Test | `CacheStorageDomain` no tiene `enable` |
| BUG-032 | Medium | Test | `OverlayDomain` requiere DOM habilitado |
| BUG-033 | Low | Test | `CSSDomain.enable` requiere DOM habilitado |
| BUG-034 | Medium | Runtime | Storage DOM Storage commands removidos |
| BUG-036 | Low | Runtime | 24+ comandos CDP removidos en Chrome moderno |
| BUG-037 | Low | Funcionalidad | `SystemInfo` solo en browser target |
| BUG-040 | Medium | API | `set_script_execution_disabled` parámetros inválidos |
| BUG-041 | Low | API | `display_feature` parámetros inválidos |
| BUG-042 | High | Test | Tests de Fetch interception fallan por timing |
| BUG-044 | Low | Test | Tests de CSS fallan por dependencia DOM |
| BUG-045 | Low | Test | Tests de CacheStorage fallan por inicialización |
| BUG-046 | Low | Test | Tests de Sensor fallan (dominio removido) |
| BUG-047 | Medium | Test | Tests multi-tab fallan por formato de respuesta |
| BUG-048 | Low | Runtime | `Page.crash` hace timeout en headless |
| BUG-049 | Low | Test | `navigate_to_history_entry` error en test |
| BUG-050 | Low | Test | `get_exception_details` error en test |
| BUG-052 | Low | Test | `set_auto_attach` error en test |
| BUG-054 | Low | Test | WebAuthn authenticator ID no persiste entre tests |

**Total:** 28 bugs pendientes
- 4 High
- 9 Medium
- 15 Low

**Fixed:** 27 bugs (BUG-001-006, 008-009, 011-012, 015, 017, 023-030, 035, 038-039, 043, 051, 053, 055)
