# Test Plan — cdpwave

Comprehensive test plan covering all 386 methods across 48 CDP domains.

## Test Coverage Summary

| Domain | Methods | Test Cases | Priority |
|--------|---------|------------|----------|
| Page | 27 | 27 | P0 |
| Runtime | 20 | 20 | P0 |
| Target | 12 | 12 | P0 |
| Network | 17 | 17 | P0 |
| DOM | 26 | 26 | P0 |
| Browser | 9 | 9 | P0 |
| Emulation | 26 | 26 | P1 |
| Input | 11 | 11 | P1 |
| Fetch | 10 | 10 | P1 |
| Storage | 13 | 13 | P1 |
| CSS | 14 | 14 | P1 |
| Overlay | 15 | 15 | P1 |
| Debugger | 22 | 22 | P1 |
| Log | 5 | 5 | P2 |
| Performance | 4 | 4 | P2 |
| Profiler | 9 | 9 | P2 |
| HeapProfiler | 10 | 10 | P2 |
| Security | 4 | 4 | P2 |
| Accessibility | 7 | 7 | P2 |
| Animation | 9 | 9 | P2 |
| IndexedDB | 7 | 7 | P2 |
| ServiceWorker | 11 | 11 | P2 |
| WebAuthn | 4 | 4 | P2 |
| Tier 3 Other | 80 | 80 | P3 |
| **Total** | **386** | **386** | - |

---

# PAGE DOMAIN (P0)

## TC-PAGE-001: enable/disable
**Preconditions:** Browser launched
**Steps:** 
1. Call session.page.enable()
2. Call session.page.disable()
**Expected:** No errors, domain enabled/disabled

## TC-PAGE-002: navigate
**Preconditions:** Page enabled
**Steps:** Navigate to https://example.com
**Expected:** Navigation completes, page loads

## TC-PAGE-003: navigate with referrer
**Steps:** Navigate with referrer parameter
**Expected:** Referrer sent in request

## TC-PAGE-004: navigate with transition_type
**Steps:** Navigate with transition_type="typed"
**Expected:** Transition type applied

## TC-PAGE-005: reload
**Steps:** Call session.page.reload()
**Expected:** Page reloads

## TC-PAGE-006: goBack
**Steps:** Navigate twice, call goBack()
**Expected:** Returns to previous page

## TC-PAGE-007: goForward
**Steps:** Navigate back, call goForward()
**Expected:** Returns to next page

## TC-PAGE-008: captureScreenshot PNG
**Steps:** Call capture_screenshot()
**Expected:** Returns PNG data

## TC-PAGE-009: captureScreenshot JPEG
**Steps:** Call capture_screenshot(format="jpeg")
**Expected:** Returns JPEG data

## TC-PAGE-010: captureScreenshot with clip
**Steps:** Call with clip parameter
**Expected:** Returns clipped screenshot

## TC-PAGE-011: printToPDF basic
**Steps:** Call print_to_pdf()
**Expected:** Returns PDF data

## TC-PAGE-012: printToPDF landscape
**Steps:** Call with landscape=True
**Expected:** Returns landscape PDF

## TC-PAGE-013: printToPDF background
**Steps:** Call with print_background=True
**Expected:** PDF includes background

## TC-PAGE-014: printToPDF margins
**Steps:** Call with margin parameters
**Expected:** PDF with custom margins

## TC-PAGE-015: printToPDF pageRanges
**Steps:** Call with page_ranges="1-3"
**Expected:** PDF with specified pages

## TC-PAGE-016: getLayoutMetrics
**Steps:** Call get_layout_metrics()
**Expected:** Returns layout metrics

## TC-PAGE-017: getNavigationHistory
**Steps:** Navigate twice, call get_navigation_history()
**Expected:** Returns history with 2 entries

## TC-PAGE-018: setDocumentContent
**Steps:** Call with HTML string
**Expected:** Document content updated

## TC-PAGE-019: getFrameTree
**Steps:** Call get_frame_tree()
**Expected:** Returns frame tree

## TC-PAGE-020: setBypassCSP
**Steps:** Call set_bypass_csp(True)
**Expected:** CSP bypassed

## TC-PAGE-021: crash
**Steps:** Call crash()
**Expected:** Page crashes

## TC-PAGE-022: close
**Steps:** Call close()
**Expected:** Page closed

## TC-PAGE-023: bringToFront
**Steps:** Create 2 pages, call bring_to_front()
**Expected:** Page brought to front

## TC-PAGE-024: handleJavaScriptDialog
**Steps:** Trigger alert, call handle_javascript_dialog(True)
**Expected:** Dialog accepted

## TC-PAGE-025: createIsolatedWorld
**Steps:** Call create_isolated_world("test")
**Expected:** Isolated world created

## TC-PAGE-026: captureSnapshot
**Steps:** Call capture_snapshot()
**Expected:** Snapshot captured

## TC-PAGE-027: addScriptToEvaluateOnNewDocument
**Steps:** Call add_script_to_evaluate_on_new_document()
**Expected:** Script added

---

# RUNTIME DOMAIN (P0)

## TC-RUNTIME-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-RUNTIME-002: evaluate basic
**Steps:** Evaluate "1+1", return_by_value=True
**Expected:** Returns 2

## TC-RUNTIME-003: evaluate async
**Steps:** Evaluate Promise, await_promise=True
**Expected:** Returns resolved value

## TC-RUNTIME-004: evaluate with context
**Steps:** Set variable, evaluate variable
**Expected:** Returns variable value

## TC-RUNTIME-005: callFunctionOn
**Steps:** Get object, call function on it
**Expected:** Returns function result

## TC-RUNTIME-006: releaseObject
**Steps:** Get object, release it
**Expected:** Object released

## TC-RUNTIME-007: getProperties
**Steps:** Get window properties
**Expected:** Returns properties

## TC-RUNTIME-008: compileScript
**Steps:** Compile script
**Expected:** Returns script ID

## TC-RUNTIME-009: runScript
**Steps:** Run compiled script
**Expected:** Script executes

## TC-RUNTIME-010: queryObjects
**Steps:** Query objects by prototype
**Expected:** Returns matching objects

## TC-RUNTIME-011: globalLexicalScopeNames
**Steps:** Call global_lexical_scope_names()
**Expected:** Returns scope names

## TC-RUNTIME-012: addBinding
**Steps:** Call add_binding("test")
**Expected:** Binding added

## TC-RUNTIME-013: removeBinding
**Steps:** Call remove_binding("test")
**Expected:** Binding removed

## TC-RUNTIME-014: getHeapUsage
**Steps:** Call get_heap_usage()
**Expected:** Returns heap usage

## TC-RUNTIME-015: getIsolateId
**Steps:** Call get_isolate_id()
**Expected:** Returns isolate ID

## TC-RUNTIME-016: collectGarbage
**Steps:** Call collect_garbage()
**Expected:** Garbage collected

## TC-RUNTIME-017: terminateExecution
**Steps:** Call terminate_execution()
**Expected:** Execution terminated

## TC-RUNTIME-018: setCustomObjectFormatterEnabled
**Steps:** Call set_custom_object_formatter_enabled(True)
**Expected:** Formatter enabled

## TC-RUNTIME-019: getExceptionDetails
**Steps:** Throw error, get details
**Expected:** Returns exception details

## TC-RUNTIME-020: awaitPromise timeout
**Steps:** Evaluate never-resolving promise with timeout
**Expected:** Timeout error

---

# TARGET DOMAIN (P0)

## TC-TARGET-001: createTarget
**Steps:** Call create_target("https://example.com")
**Expected:** Target created

## TC-TARGET-002: attachToTarget
**Steps:** Attach to created target
**Expected:** Attached, returns session ID

## TC-TARGET-003: detachFromTarget
**Steps:** Detach from target
**Expected:** Detached

## TC-TARGET-004: closeTarget
**Steps:** Close target
**Expected:** Target closed

## TC-TARGET-005: getTargets
**Steps:** Call get_targets()
**Expected:** Returns all targets

## TC-TARGET-006: activateTarget
**Steps:** Activate target
**Expected:** Target activated

## TC-TARGET-007: setAutoAttach
**Steps:** Call set_auto_attach(True, True, True)
**Expected:** Auto attach enabled

## TC-TARGET-008: sendMessageToTarget
**Steps:** Send message to target
**Expected:** Message sent

## TC-TARGET-009: setDiscoverTargets
**Steps:** Call set_discover_targets(True)
**Expected:** Discovery enabled

## TC-TARGET-010: setRemoteLocations
**Steps:** Set remote locations
**Expected:** Locations set

## TC-TARGET-011: getTargetInfo
**Steps:** Get target info
**Expected:** Returns target info

## TC-TARGET-012: initiateTargetShutdown
**Steps:** Initiate shutdown
**Expected:** Target shuts down

---

# NETWORK DOMAIN (P0)

## TC-NETWORK-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-NETWORK-002: setCacheDisabled
**Steps:** Call set_cache_disabled(True)
**Expected:** Cache disabled

## TC-NETWORK-003: setUserAgentOverride
**Steps:** Call set_user_agent_override("TestBot")
**Expected:** UA overridden

## TC-NETWORK-004: clearBrowserCookies
**Steps:** Call clear_browser_cookies()
**Expected:** Cookies cleared

## TC-NETWORK-005: clearBrowserCache
**Steps:** Call clear_browser_cache()
**Expected:** Cache cleared

## TC-NETWORK-006: getAllCookies
**Steps:** Call get_all_cookies()
**Expected:** Returns all cookies

## TC-NETWORK-007: setCookies
**Steps:** Call set_cookies([cookie])
**Expected:** Cookie set

## TC-NETWORK-008: getCookies
**Steps:** Call get_cookies([url])
**Expected:** Returns cookies for URL

## TC-NETWORK-009: deleteCookies
**Steps:** Call delete_cookies(name, url)
**Expected:** Cookie deleted

## TC-NETWORK-010: setExtraHTTPHeaders
**Steps:** Call set_extra_http_headers({header: value})
**Expected:** Headers set

## TC-NETWORK-011: canEmulateNetworkConditions
**Steps:** Call can_emulate_network_conditions()
**Expected:** Returns capability

## TC-NETWORK-012: emulateNetworkConditions
**Steps:** Call emulate_network_conditions(params)
**Expected:** Conditions emulated

## TC-NETWORK-013: getResponseBody
**Steps:** Get response body for request
**Expected:** Returns body

## TC-NETWORK-014: continueInterceptedRequest
**Steps:** Continue intercepted request
**Expected:** Request continued

## TC-NETWORK-015: getPostData
**Steps:** Get POST data
**Expected:** Returns POST data

## TC-NETWORK-016: replayXHR
**Steps:** Replay XHR
**Expected:** XHR replayed

## TC-NETWORK-017: getResponseBodyForInterception
**Steps:** Get intercepted response body
**Expected:** Returns body

---

# DOM DOMAIN (P0)

## TC-DOM-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-DOM-002: getDocument
**Steps:** Call get_document()
**Expected:** Returns document

## TC-DOM-003: getFlattenedDocument
**Steps:** Call get_flattened_document()
**Expected:** Returns flattened doc

## TC-DOM-004: collectClassNamesFromSubtree
**Steps:** Call collect_class_names_from_subtree(nodeId)
**Expected:** Returns class names

## TC-DOM-005: querySelector
**Steps:** Call query_selector(nodeId, "h1")
**Expected:** Returns h1 node

## TC-DOM-006: querySelectorAll
**Steps:** Call query_selector_all(nodeId, "p")
**Expected:** Returns all p nodes

## TC-DOM-007: removeNode
**Steps:** Call remove_node(nodeId)
**Expected:** Node removed

## TC-DOM-008: setAttributeValue
**Steps:** Call set_attribute_value(nodeId, "data-test", "value")
**Expected:** Attribute set

## TC-DOM-009: setAttributesAsText
**Steps:** Call set_attributes_as_text(nodeId, "class='test'")
**Expected:** Attributes set

## TC-DOM-010: removeAttribute
**Steps:** Call remove_attribute(nodeId, "class")
**Expected:** Attribute removed

## TC-DOM-011: setTextContent
**Steps:** Call set_text_content(nodeId, "text")
**Expected:** Text set

## TC-DOM-012: getBoxModel
**Steps:** Call get_box_model(nodeId)
**Expected:** Returns box model

## TC-DOM-013: getContentQuads
**Steps:** Call get_content_quads(nodeId)
**Expected:** Returns quads

## TC-DOM-014: describeNode
**Steps:** Call describe_node(nodeId)
**Expected:** Returns node description

## TC-DOM-015: focus
**Steps:** Call focus(nodeId)
**Expected:** Element focused

## TC-DOM-016: scrollIntoViewIfNeeded
**Steps:** Call scroll_into_view_if_needed(nodeId)
**Expected:** Element scrolled

## TC-DOM-017: setFileInputFiles
**Steps:** Call set_file_input_files(nodeId, [file])
**Expected:** Files set

## TC-DOM-018: performSearch
**Steps:** Call perform_search("query")
**Expected:** Returns search ID

## TC-DOM-019: getSearchResults
**Steps:** Call get_search_results(searchId, 0, 10)
**Expected:** Returns results

## TC-DOM-020: discardSearchResults
**Steps:** Call discard_search_results(searchId)
**Expected:** Results discarded

## TC-DOM-021: requestChildNodes
**Steps:** Call request_child_nodes(nodeId)
**Expected:** Child nodes requested

## TC-DOM-022: requestNode
**Steps:** Call request_node(nodeId)
**Expected:** Node requested

## TC-DOM-023: getOuterHTML
**Steps:** Call get_outer_html(nodeId)
**Expected:** Returns outer HTML

## TC-DOM-024: setOuterHTML
**Steps:** Call set_outer_html(nodeId, "<html>")
**Expected:** Outer HTML set

## TC-DOM-025: getHighlightObjectForTest
**Steps:** Call get_highlight_object_for_test(nodeId)
**Expected:** Returns highlight object

## TC-DOM-026: setChildNodes
**Steps:** Call set_child_nodes(parentId, nodes)
**Expected:** Child nodes set

---

# BROWSER DOMAIN (P0)

## TC-BROWSER-001: getVersion
**Steps:** Call get_version()
**Expected:** Returns version info

## TC-BROWSER-002: getCommandLine
**Steps:** Call get_command_line()
**Expected:** Returns command line

## TC-BROWSER-003: getHistogram
**Steps:** Call get_histogram("V8.ExecuteJS")
**Expected:** Returns histogram

## TC-BROWSER-004: getHistograms
**Steps:** Call get_histograms()
**Expected:** Returns all histograms

## TC-BROWSER-005: getCPUProfile
**Steps:** Call get_cpu_profile()
**Expected:** Returns CPU profile

## TC-BROWSER-006: getHeapProfile
**Steps:** Call get_heap_profile()
**Expected:** Returns heap profile

## TC-BROWSER-007: resetHistograms
**Steps:** Call reset_histograms()
**Expected:** Histograms reset

## TC-BROWSER-008: getBrowserCommandLine
**Steps:** Call get_browser_command_line()
**Expected:** Returns command line

## TC-BROWSER-009: getBounds
**Steps:** Call get_bounds()
**Expected:** Returns bounds

---

# EMULATION DOMAIN (P1)

## TC-EMULATION-001: setDeviceMetricsOverride
**Steps:** Call set_device_metrics_override(375, 667, 2, True)
**Expected:** Metrics overridden

## TC-EMULATION-002: clearDeviceMetricsOverride
**Steps:** Call clear_device_metrics_override()
**Expected:** Metrics cleared

## TC-EMULATION-003: setGeolocationOverride
**Steps:** Call set_geolocation_override(40.7, -74.0)
**Expected:** Geolocation overridden

## TC-EMULATION-004: clearGeolocationOverride
**Steps:** Call clear_geolocation_override()
**Expected:** Geolocation cleared

## TC-EMULATION-005: setCPUThrottlingRate
**Steps:** Call set_cpu_throttling_rate(4)
**Expected:** CPU throttled

## TC-EMULATION-006: setUserAgentOverride
**Steps:** Call set_user_agent_override("TestBot")
**Expected:** UA overridden

## TC-EMULATION-007: setTouchEmulationEnabled
**Steps:** Call set_touch_emulation_enabled(True)
**Expected:** Touch emulation enabled

## TC-EMULATION-008: setEmulatedMedia
**Steps:** Call set_emulated_media("prefers-color-scheme", "dark")
**Expected:** Media emulated

## TC-EMULATION-009: clearEmulatedMedia
**Steps:** Call clear_emulated_media()
**Expected:** Media cleared

## TC-EMULATION-010: setTimezoneOverride
**Steps:** Call set_timezone_override("America/New_York")
**Expected:** Timezone overridden

## TC-EMULATION-011: clearTimezoneOverride
**Steps:** Call clear_timezone_override()
**Expected:** Timezone cleared

## TC-EMULATION-012: setIdleOverride
**Steps:** Call set_idle_override(False, False)
**Expected:** Idle overridden

## TC-EMULATION-013: clearIdleOverride
**Steps:** Call clear_idle_override()
**Expected:** Idle cleared

## TC-EMULATION-014: setNavigatorOverrides
**Steps:** Call set_navigator_overrides("Win32")
**Expected:** Navigator overridden

## TC-EMULATION-015: setPageScaleFactor
**Steps:** Call set_page_scale_factor(2)
**Expected:** Scale factor set

## TC-EMULATION-016: setScriptExecutionDisabled
**Steps:** Call set_script_execution_disabled(True)
**Expected:** Script execution disabled

## TC-EMULATION-017: setDefaultBackgroundColorOverride
**Steps:** Call set_default_background_color_override(color)
**Expected:** Background color overridden

## TC-EMULATION-018: clearDefaultBackgroundColorOverride
**Steps:** Call clear_default_background_color_override()
**Expected:** Background color cleared

## TC-EMULATION-019: setVirtualTimePolicy
**Steps:** Call set_virtual_time_policy("pause")
**Expected:** Virtual time policy set

## TC-EMULATION-020: setLocale
**Steps:** Call set_locale("es-ES")
**Expected:** Locale set

## TC-EMULATION-021: setScrollPosition
**Steps:** Call set_scroll_position({x: 100, y: 100})
**Expected:** Scroll position set

## TC-EMULATION-022: setFocusEmulationEnabled
**Steps:** Call set_focus_emulation_enabled(True)
**Expected:** Focus emulation enabled

## TC-EMULATION-023: setEmulatedVisionDeficiency
**Steps:** Call set_emulated_vision_deficiency("achromatopsia")
**Expected:** Vision deficiency emulated

## TC-EMULATION-024: clearEmulatedVisionDeficiency
**Steps:** Call clear_emulated_vision_deficiency()
**Expected:** Vision deficiency cleared

## TC-EMULATION-025: setAutoDarkModeOverride
**Steps:** Call set_auto_dark_mode_override(True)
**Expected:** Auto dark mode set

## TC-EMULATION-026: clearAutoDarkModeOverride
**Steps:** Call clear_auto_dark_mode_override()
**Expected:** Auto dark mode cleared

---

# INPUT DOMAIN (P1)

## TC-INPUT-001: dispatchKeyEvent char
**Steps:** Call dispatch_key_event("char", "H")
**Expected:** Key event sent

## TC-INPUT-002: dispatchKeyEvent keyDown
**Steps:** Call dispatch_key_event("keyDown", "Enter")
**Expected:** Key down sent

## TC-INPUT-003: dispatchMouseEvent
**Steps:** Call dispatch_mouse_event("mousePressed", "left", 100, 100)
**Expected:** Mouse event sent

## TC-INPUT-004: dispatchTouchEvent
**Steps:** Call dispatch_touch_event("touchStart", [{x: 100, y: 100}])
**Expected:** Touch event sent

## TC-INPUT-005: emulateTouchFromMouseEvent
**Steps:** Call emulate_touch_from_mouse_event("touchStart", 100, 100)
**Expected:** Touch emulated

## TC-INPUT-006: synthesizePinchGesture
**Steps:** Call synthesize_pinch_gesture(100, 100, 2)
**Expected:** Pinch gesture sent

## TC-INPUT-007: synthesizeScrollGesture
**Steps:** Call synthesize_scroll_gesture(100, 100, 0, 100)
**Expected:** Scroll gesture sent

## TC-INPUT-008: synthesizeTapGesture
**Steps:** Call synthesize_tap_gesture(100, 100)
**Expected:** Tap gesture sent

## TC-INPUT-009: insertText
**Steps:** Call insert_text("Hello World")
**Expected:** Text inserted

## TC-INPUT-010: setIgnoreInputEvents
**Steps:** Call set_ignore_input_events(True)
**Expected:** Input events ignored

## TC-INPUT-011: cancelDragging
**Steps:** Call cancel_dragging()
**Expected:** Dragging cancelled

---

# FETCH DOMAIN (P1)

## TC-FETCH-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-FETCH-002: failRequest
**Steps:** Fail intercepted request
**Expected:** Request failed

## TC-FETCH-003: fulfillRequest
**Steps:** Fulfill intercepted request
**Expected:** Request fulfilled

## TC-FETCH-004: continueRequest
**Steps:** Continue intercepted request
**Expected:** Request continued

## TC-FETCH-005: continueWithAuth
**Steps:** Continue with auth
**Expected:** Auth continued

## TC-FETCH-006: getResponseBody
**Steps:** Get response body
**Expected:** Returns body

## TC-FETCH-007: takeResponseBodyAsStream
**Steps:** Take as stream
**Expected:** Stream created

## TC-FETCH-008: continueResponse
**Steps:** Continue response
**Expected:** Response continued

## TC-FETCH-009: pause/resume
**Steps:** Call pause(), resume()
**Expected:** Paused/resumed

## TC-FETCH-010: fail
**Steps:** Call fail()
**Expected:** Failed

---

# STORAGE DOMAIN (P1)

## TC-STORAGE-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-STORAGE-002: getDOMStorageItems
**Steps:** Call get_dom_storage_items()
**Expected:** Returns items

## TC-STORAGE-003: setDOMStorageItem
**Steps:** Call set_dom_storage_item("key", "value")
**Expected:** Item set

## TC-STORAGE-004: removeDOMStorageItem
**Steps:** Call remove_dom_storage_item("key")
**Expected:** Item removed

## TC-STORAGE-005: clearDOMStorageItems
**Steps:** Call clear_dom_storage_items()
**Expected:** Items cleared

## TC-STORAGE-006: getUsageAndQuota
**Steps:** Call get_usage_and_quota()
**Expected:** Returns usage

## TC-STORAGE-007: trackCacheStorageForOrigin
**Steps:** Call track_cache_storage_for_origin(url)
**Expected:** Cache tracked

## TC-STORAGE-008: trackIndexedDBForOrigin
**Steps:** Call track_indexed_db_for_origin(url)
**Expected:** IndexedDB tracked

## TC-STORAGE-009: untrackCacheStorageForOrigin
**Steps:** Call untrack_cache_storage_for_origin(url)
**Expected:** Cache untracked

## TC-STORAGE-010: untrackIndexedDBForOrigin
**Steps:** Call untrack_indexed_db_for_origin(url)
**Expected:** IndexedDB untracked

## TC-STORAGE-011: getCacheStorageForOrigin
**Steps:** Call get_cache_storage_for_origin(url)
**Expected:** Returns cache storage

## TC-STORAGE-012: getIndexedDBForOrigin
**Steps:** Call get_indexed_db_for_origin(url)
**Expected:** Returns IndexedDB

## TC-STORAGE-013: getCookies
**Steps:** Call get_cookies([url])
**Expected:** Returns cookies

---

# CSS DOMAIN (P1)

## TC-CSS-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-CSS-002: getComputedStyle
**Steps:** Call get_computed_style(nodeId)
**Expected:** Returns computed style

## TC-CSS-003: getInlineStylesForNode
**Steps:** Call get_inline_styles_for_node(nodeId)
**Expected:** Returns inline styles

## TC-CSS-004: getMatchedStylesForNode
**Steps:** Call get_matched_styles_for_node(nodeId)
**Expected:** Returns matched styles

## TC-CSS-005: getMediaQueries
**Steps:** Call get_media_queries()
**Expected:** Returns media queries

## TC-CSS-006: getPlatformFontsForNode
**Steps:** Call get_platform_fonts_for_node(nodeId)
**Expected:** Returns fonts

## TC-CSS-007: getStyleSheetText
**Steps:** Call get_style_sheet_text(sheetId)
**Expected:** Returns CSS text

## TC-CSS-008: setStyleSheetText
**Steps:** Call set_style_sheet_text(sheetId, text)
**Expected:** CSS text set

## TC-CSS-009: setRuleStyle
**Steps:** Call set_rule_style(sheetId, ruleId, text)
**Expected:** Rule style set

## TC-CSS-010: addRule
**Steps:** Call add_rule(sheetId, rule, location)
**Expected:** Rule added

## TC-CSS-011: forcePseudoState
**Steps:** Call force_pseudo_state(nodeId, ["hover"])
**Expected:** Pseudo state forced

## TC-CSS-012: getBackgroundColors
**Steps:** Call get_background_colors(nodeId)
**Expected:** Returns background colors

## TC-CSS-013: setEffectiveCompositeForNode
**Steps:** Call set_effective_composite_for_node(nodeId, name)
**Expected:** Composite set

## TC-CSS-014: takeCoverageDelta
**Steps:** Call take_coverage_delta()
**Expected:** Returns coverage delta

---

# OVERLAY DOMAIN (P1)

## TC-OVERLAY-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-OVERLAY-002: setShowDevTools
**Steps:** Call set_show_dev_tools(True)
**Expected:** Dev tools shown

## TC-OVERLAY-003: setPausedInOverlayMessage
**Steps:** Call set_paused_in_overlay_message("Paused")
**Expected:** Message set

## TC-OVERLAY-004: highlightNode
**Steps:** Call highlight_node(nodeId)
**Expected:** Node highlighted

## TC-OVERLAY-005: highlightFrame
**Steps:** Call highlight_frame(frameId)
**Expected:** Frame highlighted

## TC-OVERLAY-006: highlightQuad
**Steps:** Call highlight_quad(quad)
**Expected:** Quad highlighted

## TC-OVERLAY-007: highlightRect
**Steps:** Call highlight_rect(x, y, w, h)
**Expected:** Rect highlighted

## TC-OVERLAY-008: highlightShape
**Steps:** Call highlight_shape(shapes)
**Expected:** Shape highlighted

## TC-OVERLAY-009: setShowGridOverlays
**Steps:** Call set_show_grid_overlays(True)
**Expected:** Grid overlays shown

## TC-OVERLAY-010: setShowPaintRects
**Steps:** Call set_show_paint_rects(True)
**Expected:** Paint rects shown

## TC-OVERLAY-011: setShowLayoutRects
**Steps:** Call set_show_layout_rects(True)
**Expected:** Layout rects shown

## TC-OVERLAY-012: setShowScrollBottleneckRects
**Steps:** Call set_show_scroll_bottleneck_rects(True)
**Expected:** Scroll rects shown

## TC-OVERLAY-013: setShowHitTestRects
**Steps:** Call set_show_hit_test_rects(True)
**Expected:** Hit test rects shown

## TC-OVERLAY-014: setShowWebVitals
**Steps:** Call set_show_web_vitals(True)
**Expected:** Web vitals shown

## TC-OVERLAY-015: setShowViewportSizeOnResize
**Steps:** Call set_show_viewport_size_on_resize(True)
**Expected:** Viewport size shown

---

# DEBUGGER DOMAIN (P1)

## TC-DEBUGGER-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-DEBUGGER-002: setBreakpointsByUrl
**Steps:** Call set_breakpoints_by_url(url, line)
**Expected:** Breakpoints set

## TC-DEBUGGER-003: removeBreakpoint
**Steps:** Call remove_breakpoint(breakpointId)
**Expected:** Breakpoint removed

## TC-DEBUGGER-004: getPossibleBreakpoints
**Steps:** Call get_possible_breakpoints(locations)
**Expected:** Returns possible breakpoints

## TC-DEBUGGER-005: setBreakpointByScriptId
**Steps:** Call set_breakpoint_by_script_id(scriptId, line)
**Expected:** Breakpoint set

## TC-DEBUGGER-006: setBreakpointActive
**Steps:** Call set_breakpoint_active(breakpointId, True)
**Expected:** Breakpoint activated

## TC-DEBUGGER-007: setBreakpointsActive
**Steps:** Call set_breakpoints_active(True)
**Expected:** All breakpoints activated

## TC-DEBUGGER-008: stepInto
**Steps:** Call step_into()
**Expected:** Stepped into

## TC-DEBUGGER-009: stepOver
**Steps:** Call step_over()
**Expected:** Stepped over

## TC-DEBUGGER-010: stepOut
**Steps:** Call step_out()
**Expected:** Stepped out

## TC-DEBUGGER-011: pause
**Steps:** Call pause()
**Expected:** Paused

## TC-DEBUGGER-012: resume
**Steps:** Call resume()
**Expected:** Resumed

## TC-DEBUGGER-013: searchInContent
**Steps:** Call search_in_content(scriptId, "query")
**Expected:** Returns search results

## TC-DEBUGGER-014: setScriptSource
**Steps:** Call set_script_source(scriptId, source)
**Expected:** Script source set

## TC-DEBUGGER-015: restartFrame
**Steps:** Call restart_frame(frameId)
**Expected:** Frame restarted

## TC-DEBUGGER-016: getScriptSource
**Steps:** Call get_script_source(scriptId)
**Expected:** Returns script source

## TC-DEBUGGER-017: setPauseOnExceptions
**Steps:** Call set_pause_on_exceptions("all")
**Expected:** Pause on exceptions set

## TC-DEBUGGER-018: evaluateOnCallFrame
**Steps:** Call evaluate_on_call_frame(frameId, "expression")
**Expected:** Returns evaluation result

## TC-DEBUGGER-019: setVariableValue
**Steps:** Call set_variable_value(frameId, scope, var, value)
**Expected:** Variable value set

## TC-DEBUGGER-020: setAsyncStackTrace
**Steps:** Call set_async_stack_trace(parentId)
**Expected:** Stack trace set

## TC-DEBUGGER-021: setBlackboxPatterns
**Steps:** Call set_blackbox_patterns(["pattern"])
**Expected:** Patterns set

## TC-DEBUGGER-022: getProperties
**Steps:** Call get_properties(objectId)
**Expected:** Returns properties

---

# LOG DOMAIN (P2)

## TC-LOG-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-LOG-002: clear
**Steps:** Call clear()
**Expected:** Log cleared

## TC-LOG-003: startViolationsReport
**Steps:** Call start_violations_report(["longTask"])
**Expected:** Report started

## TC-LOG-004: stopViolationsReport
**Steps:** Call stop_violations_report()
**Expected:** Report stopped

## TC-LOG-005: getViolationsReport
**Steps:** Call get_violations_report()
**Expected:** Returns violations

---

# PERFORMANCE DOMAIN (P2)

## TC-PERF-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-PERF-002: getMetrics
**Steps:** Call get_metrics()
**Expected:** Returns metrics

## TC-PERF-003: setTimeDomain
**Steps:** Call set_time_domain("timeStamp")
**Expected:** Time domain set

## TC-PERF-004: setDisableMetrics
**Steps:** Call set_disable_metrics(["metric"])
**Expected:** Metrics disabled

---

# PROFILER DOMAIN (P2)

## TC-PROFILER-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-PROFILER-002: start
**Steps:** Call start()
**Expected:** Profiler started

## TC-PROFILER-003: stop
**Steps:** Call stop()
**Expected:** Profiler stopped, returns profile

## TC-PROFILER-004: setSamplingInterval
**Steps:** Call set_sampling_interval(100)
**Expected:** Interval set

## TC-PROFILER-005: setPreciseCoverage
**Steps:** Call set_precise_coverage(True, False, True)
**Expected:** Precise coverage set

## TC-PROFILER-006: takePreciseCoverage
**Steps:** Call take_precise_coverage()
**Expected:** Returns coverage

## TC-PROFILER-007: getBestEffortCoverage
**Steps:** Call get_best_effort_coverage()
**Expected:** Returns coverage

## TC-PROFILER-008: startTypeProfile
**Steps:** Call start_type_profile()
**Expected:** Type profile started

## TC-PROFILER-009: stopTypeProfile
**Steps:** Call stop_type_profile()
**Expected:** Type profile stopped

---

# HEAP PROFILER DOMAIN (P2)

## TC-HEAP-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-HEAP-002: startSampling
**Steps:** Call start_sampling(64)
**Expected:** Sampling started

## TC-HEAP-003: stopSampling
**Steps:** Call stop_sampling()
**Expected:** Sampling stopped

## TC-HEAP-004: startTrackingHeapObjects
**Steps:** Call start_tracking_heap_objects()
**Expected:** Tracking started

## TC-HEAP-005: stopTrackingHeapObjects
**Steps:** Call stop_tracking_heap_objects()
**Expected:** Tracking stopped

## TC-HEAP-006: takeHeapSnapshot
**Steps:** Call take_heap_snapshot()
**Expected:** Snapshot taken

## TC-HEAP-007: collectGarbage
**Steps:** Call collect_garbage()
**Expected:** Garbage collected

## TC-HEAP-008: getObjectByHeapObjectId
**Steps:** Call get_object_by_heap_object_id(objId)
**Expected:** Returns object

## TC-HEAP-009: addHeapSnapshotChunk
**Steps:** Call add_heap_snapshot_chunk(chunk)
**Expected:** Chunk added

## TC-HEAP-010: getLastSeenObjectID
**Steps:** Call get_last_seen_object_id()
**Expected:** Returns object ID

---

# SECURITY DOMAIN (P2)

## TC-SECURITY-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-SECURITY-002: setIgnoreCertificateErrors
**Steps:** Call set_ignore_certificate_errors(True)
**Expected:** Certificate errors ignored

## TC-SECURITY-003: handleCertificateError
**Steps:** Call handle_certificate_error(eventId, True)
**Expected:** Certificate error handled

## TC-SECURITY-004: getVisibleSecurityState
**Steps:** Call get_visible_security_state()
**Expected:** Returns security state

---

# ACCESSIBILITY DOMAIN (P2)

## TC-A11Y-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-A11Y-002: getPartialAXTree
**Steps:** Call get_partial_ax_tree(nodeId)
**Expected:** Returns partial tree

## TC-A11Y-003: getFullAXTree
**Steps:** Call get_full_ax_tree(nodeId)
**Expected:** Returns full tree

## TC-A11Y-004: getRootAXNode
**Steps:** Call get_root_ax_node()
**Expected:** Returns root node

## TC-A11Y-005: getAXNodeAndAncestors
**Steps:** Call get_ax_node_and_ancestors(nodeId)
**Expected:** Returns node and ancestors

## TC-A11Y-006: getAXNode
**Steps:** Call get_ax_node(nodeId)
**Expected:** Returns node

## TC-A11Y-007: getImageData
**Steps:** Call get_image_data(nodeId)
**Expected:** Returns image data

---

# ANIMATION DOMAIN (P2)

## TC-ANIM-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-ANIM-002: getPlayState
**Steps:** Call get_play_state(nodeId)
**Expected:** Returns play state

## TC-ANIM-003: getCurrentTime
**Steps:** Call get_current_time(nodeId)
**Expected:** Returns current time

## TC-ANIM-004: setPlaybackRate
**Steps:** Call set_playback_rate(nodeId, 2)
**Expected:** Playback rate set

## TC-ANIM-005: setTiming
**Steps:** Call set_timing(nodeId, timing)
**Expected:** Timing set

## TC-ANIM-006: seekAnimations
**Steps:** Call seek_animations(animations, time)
**Expected:** Animations sought

## TC-ANIM-007: pause
**Steps:** Call pause(animations)
**Expected:** Animations paused

## TC-ANIM-008: resume
**Steps:** Call resume(animations)
**Expected:** Animations resumed

## TC-ANIM-009: releaseAnimations
**Steps:** Call release_animations(animations)
**Expected:** Animations released

---

# INDEXEDDB DOMAIN (P2)

## TC-IDB-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-IDB-002: requestDatabaseNames
**Steps:** Call request_database_names()
**Expected:** Returns database names

## TC-IDB-003: requestDatabase
**Steps:** Call request_database(name)
**Expected:** Returns database

## TC-IDB-004: deleteDatabase
**Steps:** Call delete_database(name)
**Expected:** Database deleted

## TC-IDB-005: requestData
**Steps:** Call request_data(db, store, index, skip, count)
**Expected:** Returns data

## TC-IDB-006: deleteObjectStore
**Steps:** Call delete_object_store(db, store)
**Expected:** Object store deleted

## TC-IDB-007: clearObjectStore
**Steps:** Call clear_object_store(db, store)
**Expected:** Object store cleared

---

# SERVICE WORKER DOMAIN (P2)

## TC-SW-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-SW-002: unregister
**Steps:** Call unregister(scope)
**Expected:** Service worker unregistered

## TC-SW-003: updateRegistration
**Steps:** Call update_registration(scope)
**Expected:** Registration updated

## TC-SW-004: startWorker
**Steps:** Call start_worker(scope)
**Expected:** Worker started

## TC-SW-005: skipWaiting
**Steps:** Call skip_waiting(scope)
**Expected:** Skipped waiting

## TC-SW-006: stopWorker
**Steps:** Call stop_worker(scope)
**Expected:** Worker stopped

## TC-SW-007: stopAllWorkers
**Steps:** Call stop_all_workers()
**Expected:** All workers stopped

## TC-SW-008: dispatchSyncEvent
**Steps:** Call dispatch_sync_event(origin, id, tag, data)
**Expected:** Sync event dispatched

## TC-SW-009: inspectWorker
**Steps:** Call inspect_worker(versionId)
**Expected:** Worker inspected

## TC-SW-010: getWorkers
**Steps:** Call get_workers()
**Expected:** Returns workers

## TC-SW-011: getVersion
**Steps:** Call get_version()
**Expected:** Returns version

---

# WEBAUTHN DOMAIN (P2)

## TC-WA-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-WA-002: addVirtualAuthenticator
**Steps:** Call add_virtual_authenticator(config)
**Expected:** Authenticator added

## TC-WA-003: removeVirtualAuthenticator
**Steps:** Call remove_virtual_authenticator(id)
**Expected:** Authenticator removed

## TC-WA-004: getCredentials
**Steps:** Call get_credentials(authenticatorId)
**Expected:** Returns credentials

---

# AUDITS DOMAIN (P3)

## TC-AUDITS-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-AUDITS-002: checkContrast
**Steps:** Call check_contrast()
**Expected:** Returns contrast issues

## TC-AUDITS-003: getEncodedResponse
**Steps:** Call get_encoded_response(requestId, "base64")
**Expected:** Returns encoded response

---

# BACKGROUND SERVICE DOMAIN (P3)

## TC-BGSRV-001: startObserving
**Steps:** Call start_observing("backgroundFetch")
**Expected:** Observing started

## TC-BGSRV-002: stopObserving
**Steps:** Call stop_observing("backgroundFetch")
**Expected:** Observing stopped

## TC-BGSRV-003: setRecording
**Steps:** Call set_recording(True, "backgroundFetch")
**Expected:** Recording enabled

## TC-BGSRV-004: clearEvents
**Steps:** Call clear_events("backgroundFetch")
**Expected:** Events cleared

---

# CACHE STORAGE DOMAIN (P3)

## TC-CACHE-001: deleteCache
**Steps:** Call delete_cache(cacheId)
**Expected:** Cache deleted

## TC-CACHE-002: deleteEntry
**Steps:** Call delete_entry(cacheId, request)
**Expected:** Entry deleted

## TC-CACHE-003: requestCacheNames
**Steps:** Call request_cache_names(security_origin)
**Expected:** Returns cache names

## TC-CACHE-004: requestEntries
**Steps:** Call request_entries(cacheId)
**Expected:** Returns entries

---

# CAST DOMAIN (P3)

## TC-CAST-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-CAST-002: setSinkToUse
**Steps:** Call set_sink_to_use(sinkName)
**Expected:** Sink selected

## TC-CAST-003: startTabMirroring
**Steps:** Call start_tab_mirroring(sinkName)
**Expected:** Mirroring started

## TC-CAST-004: stopCasting
**Steps:** Call stop_casting(sinkName)
**Expected:** Casting stopped

---

# CONSOLE DOMAIN (P3)

## TC-CONSOLE-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-CONSOLE-002: clearMessages
**Steps:** Call clear_messages()
**Expected:** Messages cleared

---

# DEVICE ACCESS DOMAIN (P3)

## TC-DEVACC-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-DEVACC-002: selectBluetoothDevice
**Steps:** Call select_bluetooth_device(requestId, device)
**Expected:** Device selected

## TC-DEVACC-003: cancelPrompt
**Steps:** Call cancel_prompt(requestId)
**Expected:** Prompt cancelled

---

# DEVICE ORIENTATION DOMAIN (P3)

## TC-DEVORI-001: setDeviceOrientationOverride
**Steps:** Call set_device_orientation_override(0, 0, 0)
**Expected:** Orientation overridden

## TC-DEVORI-002: clearDeviceOrientationOverride
**Steps:** Call clear_device_orientation_override()
**Expected:** Orientation cleared

---

# DOM DEBUGGER DOMAIN (P3)

## TC-DOMDBG-001: setDOMBreakpoint
**Steps:** Call set_dom_breakpoint(nodeId, "subtree-modified")
**Expected:** Breakpoint set

## TC-DOMDBG-002: removeDOMBreakpoint
**Steps:** Call remove_dom_breakpoint(nodeId, "subtree-modified")
**Expected:** Breakpoint removed

## TC-DOMDBG-003: setEventListenerBreakpoint
**Steps:** Call set_event_listener_breakpoint("click")
**Expected:** Breakpoint set

## TC-DOMDBG-004: removeEventListenerBreakpoint
**Steps:** Call remove_event_listener_breakpoint("click")
**Expected:** Breakpoint removed

## TC-DOMDBG-005: setXHRBreakpoint
**Steps:** Call set_xhr_breakpoint("api")
**Expected:** XHR breakpoint set

## TC-DOMDBG-006: removeXHRBreakpoint
**Steps:** Call remove_xhr_breakpoint("api")
**Expected:** XHR breakpoint removed

---

# EVENT BREAKPOINTS DOMAIN (P3)

## TC-EVBRK-001: setInstrumentationBreakpoint
**Steps:** Call set_instrumentation_breakpoint("scriptFirstStatement")
**Expected:** Breakpoint set

## TC-EVBRK-002: clearInstrumentationBreakpoint
**Steps:** Call clear_instrumentation_breakpoint("scriptFirstStatement")
**Expected:** Breakpoint cleared

## TC-EVBRK-003: setBreakpointOnNativeEvent
**Steps:** Call set_breakpoint_on_native_event("click")
**Expected:** Breakpoint set

## TC-EVBRK-004: clearBreakpointOnNativeEvent
**Steps:** Call clear_breakpoint_on_native_event("click")
**Expected:** Breakpoint cleared

---

# EXTENSIONS DOMAIN (P3)

## TC-EXT-001: loadUnpacked
**Steps:** Call load_unpacked(path)
**Expected:** Extension loaded

## TC-EXT-002: getStorageItems
**Steps:** Call get_storage_items(id, "local")
**Expected:** Returns storage items

## TC-EXT-003: removeStorageItems
**Steps:** Call remove_storage_items(id, "local", ["key"])
**Expected:** Items removed

## TC-EXT-004: clearStorageItems
**Steps:** Call clear_storage_items(id, "local")
**Expected:** Storage cleared

---

# HEADLESS EXPERIMENTAL DOMAIN (P3)

## TC-HEAD-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-HEAD-002: setWindowBounds
**Steps:** Call set_window_bounds(bounds={width: 800, height: 600})
**Expected:** Bounds set

---

# INSPECTOR DOMAIN (P3)

## TC-INSP-001: Event Subscription
**Steps:** Subscribe to Inspector.detached event
**Expected:** Event received when detached

---

# IO DOMAIN (P3)

## TC-IO-001: read
**Steps:** Call read(handle)
**Expected:** Returns data

## TC-IO-002: close
**Steps:** Call close(handle)
**Expected:** Stream closed

## TC-IO-003: resolveBlob
**Steps:** Call resolve_blob(objectId)
**Expected:** Returns blob UUID

---

# LAYER TREE DOMAIN (P3)

## TC-LAYER-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-LAYER-002: getLayers
**Steps:** Call get_layers()
**Expected:** Returns layers

## TC-LAYER-003: compositingReasons
**Steps:** Call compositing_reasons(layerId)
**Expected:** Returns reasons

## TC-LAYER-004: loadSnapshot
**Steps:** Call load_snapshot(tiles)
**Expected:** Snapshot loaded

## TC-LAYER-005: releaseSnapshot
**Steps:** Call release_snapshot(snapshotId)
**Expected:** Snapshot released

## TC-LAYER-006: profileSnapshot
**Steps:** Call profile_snapshot(snapshotId)
**Expected:** Returns timings

---

# MEDIA DOMAIN (P3)

## TC-MEDIA-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-MEDIA-002: getPlayerProperties
**Steps:** Call get_player_properties(playerId)
**Expected:** Returns properties

## TC-MEDIA-003: getPlayers
**Steps:** Call get_players()
**Expected:** Returns players

---

# MEMORY DOMAIN (P3)

## TC-MEM-001: getDOMCounters
**Steps:** Call get_dom_counters()
**Expected:** Returns counters

## TC-MEM-002: prepareForLeakDetection
**Steps:** Call prepare_for_leak_detection()
**Expected:** Prepared for leak detection

## TC-MEM-003: forceGarbageCollection
**Steps:** Call for_force_garbage_collection()
**Expected:** GC executed

## TC-MEM-004: setPressureNotificationsSuppressed
**Steps:** Call set_pressure_notifications_suppressed(True)
**Expected:** Notifications suppressed

## TC-MEM-005: simulatePressureNotification
**Steps:** Call simulate_pressure_notification("moderate")
**Expected:** Pressure simulated

## TC-MEM-006: startSampling
**Steps:** Call start_sampling()
**Expected:** Sampling started

## TC-MEM-007: stopSampling
**Steps:** Call stop_sampling()
**Expected:** Sampling stopped

## TC-MEM-008: getSamplingProfile
**Steps:** Call get_sampling_profile()
**Expected:** Returns profile

---

# PERFORMANCE TIMELINE DOMAIN (P3)

## TC-PERFTL-001: Event Subscription
**Steps:** Subscribe to PerformanceTimeline.timelineEvent
**Expected:** Events received during recording

---

# PRELOAD DOMAIN (P3)

## TC-PRELOAD-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-PRELOAD-002: getPreloadPolicy
**Steps:** Call get_preload_policy()
**Expected:** Returns policy

## TC-PRELOAD-003: setPreloadPolicy
**Steps:** Call set_preload_policy("always")
**Expected:** Policy set

---

# PWA DOMAIN (P3)

## TC-PWA-001: install
**Steps:** Call install(manifestId)
**Expected:** PWA installed

## TC-PWA-002: uninstall
**Steps:** Call uninstall(manifestId)
**Expected:** PWA uninstalled

## TC-PWA-003: getOsAppState
**Steps:** Call get_os_app_state(manifestId)
**Expected:** Returns app state

---

# SCHEMA DOMAIN (P3)

## TC-SCHEMA-001: getDomains
**Steps:** Call get_domains()
**Expected:** Returns all domains

---

# SENSOR DOMAIN (P3)

## TC-SENSOR-001: enable/disable
**Steps:** Call enable(), disable()
**Expected:** Domain enabled/disabled

## TC-SENSOR-002: setSensorOverride
**Steps:** Call set_sensor_override("accelerometer", reading)
**Expected:** Sensor overridden

## TC-SENSOR-003: clearSensorOverride
**Steps:** Call clear_sensor_override("accelerometer")
**Expected:** Override cleared

---

# SYSTEM INFO DOMAIN (P3)

## TC-SYS-001: getInfo
**Steps:** Call get_info()
**Expected:** Returns system info

## TC-SYS-002: getProcessInfo
**Steps:** Call get_process_info()
**Expected:** Returns process info

## TC-SYS-003: getFeatureState
**Steps:** Call get_feature_state(featureName)
**Expected:** Returns feature state

## TC-SYS-004: getGPUInfo
**Steps:** Call get_gpu_info()
**Expected:** Returns GPU info

---

# TETHERING DOMAIN (P3)

## TC-TETHER-001: enable
**Steps:** Call enable(port=8080)
**Expected:** Tethering enabled

## TC-TETHER-002: disable
**Steps:** Call disable(port=8080)
**Expected:** Tethering disabled

---

# TRACING DOMAIN (P3)

## TC-TRACE-001: start
**Steps:** Call start(categories="devtools.timeline")
**Expected:** Tracing started

## TC-TRACE-002: end
**Steps:** Call end()
**Expected:** Tracing ended

## TC-TRACE-003: getCategories
**Steps:** Call get_categories()
**Expected:** Returns categories

## TC-TRACE-004: recordClockSyncMarker
**Steps:** Call record_clock_sync_marker(syncId)
**Expected:** Marker recorded

## TC-TRACE-005: requestClockSyncMarker
**Steps:** Call request_clock_sync_marker()
**Expected:** Returns sync ID

---

# WORKER DOMAIN (P3)

## TC-WORKER-001: Event Subscription
**Steps:** Subscribe to Worker.dedicatedWorkerStarted
**Expected:** Event received when worker starts

---

# INTEGRATION TESTS

## TC-INT-001: Network + Runtime
**Steps:** Enable network, navigate, evaluate JS
**Expected:** Requests captured, JS executes

## TC-INT-002: DOM + Input
**Steps:** Query element, click it
**Expected:** Element clicked

## TC-INT-003: Emulation + Runtime
**Steps:** Set timezone, verify with JS
**Expected:** Timezone applied

## TC-INT-004: Storage + Runtime
**Steps:** Set localStorage, verify with JS
**Expected:** Storage works

## TC-INT-005: Fetch + Network
**Steps:** Intercept request, continue
**Expected:** Request intercepted

## TC-INT-006: Page + Performance
**Steps:** Navigate, get metrics
**Expected:** Metrics collected

## TC-INT-007: Profiler + Runtime
**Steps:** Profile execution
**Expected:** Profile captured

---

# ERROR HANDLING TESTS

## TC-ERR-001: Invalid URL
**Steps:** Navigate to invalid URL
**Expected:** CommandError caught

## TC-ERR-002: Invalid JavaScript
**Steps:** Evaluate invalid JS
**Expected:** CommandError caught

## TC-ERR-003: Timeout
**Steps:** Evaluate with timeout
**Expected:** CommandTimeoutError caught

## TC-ERR-004: Closed Session
**Steps:** Use closed session
**Expected:** SessionClosedError caught

## TC-ERR-005: Non-existent Element
**Steps:** Query non-existent element
**Expected:** CommandError caught

---

# CLEANUP TESTS

## TC-CLN-001: Target Cleanup
**Steps:** Close session, verify target removed
**Expected:** Target cleaned up

## TC-CLN-002: Resource Cleanup
**Steps:** Launch/close 5 times
**Expected:** No resource leaks

---

# Test Execution

## Priority Order
1. P0 (Critical): 111 test cases
2. P1 (High-Value): 119 test cases
3. P2 (Supporting): 82 test cases
4. P3 (Low): 82 test cases (Audits, BackgroundService, CacheStorage, Cast, Console, DeviceAccess, DeviceOrientation, DOMDebugger, EventBreakpoints, Extensions, HeadlessExperimental, Inspector, IO, LayerTree, Media, Memory, PerformanceTimeline, Preload, PWA, Schema, Sensor, SystemInfo, Tethering, Tracing, Worker)
5. Integration: 7 test cases
6. Error Handling: 5 test cases
7. Cleanup: 2 test cases

**Total: 408 test cases**

## Success Criteria
- All P0 tests pass (100%)
- All P1 tests pass (100%)
- P2 tests pass (≥95%)
- P3 tests pass (≥90%)
- Integration tests pass (100%)
- Error handling tests pass (100%)
- Cleanup tests pass (100%)
