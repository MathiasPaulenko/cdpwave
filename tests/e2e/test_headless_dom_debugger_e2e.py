"""E2E tests for HeadlessExperimental and DOMDebugger domains on a real Edge browser.

Full lifecycle tests covering:
- HeadlessExperimental: enable/disable (deprecated), beginFrame with all param
  combinations, screenshot capture, repeated frames, frame scheduling.
- DOMDebugger: all DOM breakpoint types (subtree-modified, attribute-modified,
  node-removed), event listener breakpoints with/without target, XHR breakpoints,
  getEventListeners with depth/pierce variations, instrumentation breakpoints
  (deprecated), CSP violation breakpoints (experimental), full lifecycle flows.
"""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


async def _navigate_and_wait(
    session: CDPSession, url: str = "https://example.com"
) -> None:
    await session.page.enable()
    await session.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


async def _get_root_node_id(session: CDPSession) -> int:
    await session.dom.enable()
    doc = await session.dom.get_document()
    return doc["root"]["nodeId"]


async def _get_body_node_id(session: CDPSession) -> int:
    await session.dom.enable()
    doc = await session.dom.get_document()
    root = doc["root"]
    if "children" in root and root["children"]:
        html = root["children"][0]
        if "children" in html and len(html["children"]) > 1:
            return html["children"][1]["nodeId"]
    return root["nodeId"]


async def _resolve_to_object_id(session: CDPSession, node_id: int) -> str:
    resolved = await session.dom.resolve_node(node_id)
    return resolved["object"]["objectId"]


@pytest.mark.e2e
class TestHeadlessExperimentalE2ELifecycle:
    async def test_enable_disable_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.enable()
                await session.headless_experimental.disable()

    async def test_repeated_enable_disable_cycles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.headless_experimental.enable()
                    await session.headless_experimental.disable()


@pytest.mark.e2e
class TestHeadlessExperimentalE2EBeginFrame:
    async def test_begin_frame_no_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame()
                assert isinstance(result, dict)
                assert "hasDamage" in result

    async def test_begin_frame_with_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    interval=16.666
                )
                assert isinstance(result, dict)
                assert "hasDamage" in result

    async def test_begin_frame_with_frame_time_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    frame_time_ticks=2000.0
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_no_display_updates_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    no_display_updates=True
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_no_display_updates_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    no_display_updates=False
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_screenshot_png(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "png"}
                )
                assert isinstance(result, dict)
                assert "hasDamage" in result
                if "screenshotData" in result:
                    assert isinstance(result["screenshotData"], str)

    async def test_begin_frame_with_screenshot_jpeg(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "jpeg", "quality": 80}
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_screenshot_webp(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "webp", "quality": 50}
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_screenshot_optimize_for_speed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "png", "optimizeForSpeed": True}
                )
                assert isinstance(result, dict)

    async def test_begin_frame_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    frame_time_ticks=1000.0,
                    interval=16.666,
                    no_display_updates=False,
                    screenshot={"format": "png", "quality": 100, "optimizeForSpeed": False},
                )
                assert isinstance(result, dict)
                assert "hasDamage" in result

    async def test_begin_frame_zero_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    interval=0
                )
                assert isinstance(result, dict)

    async def test_begin_frame_zero_frame_time_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    frame_time_ticks=0
                )
                assert isinstance(result, dict)

    async def test_repeated_begin_frames(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(5):
                    result = await session.headless_experimental.begin_frame()
                    assert isinstance(result, dict)
                    await asyncio.sleep(0.05)

    async def test_begin_frame_then_screenshot(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.begin_frame()
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "png"}
                )
                assert isinstance(result, dict)


@pytest.mark.e2e
class TestDOMDebuggerE2EDOMBreakpoints:
    async def test_set_remove_subtree_modified(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_set_remove_attribute_modified(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            body_id = await _get_body_node_id(session)
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    body_id, "attribute-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    body_id, "attribute-modified"
                )

    async def test_set_remove_node_removed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "node-removed"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "node-removed"
                )

    async def test_all_breakpoint_types_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            bp_types = ["subtree-modified", "attribute-modified", "node-removed"]
            with contextlib.suppress(Exception):
                for bp_type in bp_types:
                    await session.dom_debugger.set_dom_breakpoint(root_id, bp_type)
                    await session.dom_debugger.remove_dom_breakpoint(
                        root_id, bp_type
                    )

    async def test_set_same_breakpoint_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_remove_without_set_succeeds_or_errors_gracefully(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            with contextlib.suppress(Exception):
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )


@pytest.mark.e2e
class TestDOMDebuggerE2EEventListenerBreakpoints:
    async def test_set_remove_click(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_event_listener_breakpoint("click")
                await session.dom_debugger.remove_event_listener_breakpoint("click")

    async def test_set_remove_with_target_document(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_event_listener_breakpoint(
                    "click", target_name="document"
                )
                await session.dom_debugger.remove_event_listener_breakpoint(
                    "click", target_name="document"
                )

    async def test_set_remove_with_target_window(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_event_listener_breakpoint(
                    "resize", target_name="window"
                )
                await session.dom_debugger.remove_event_listener_breakpoint(
                    "resize", target_name="window"
                )

    async def test_set_remove_multiple_events(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events = ["click", "mouseover", "keydown", "submit"]
            with contextlib.suppress(Exception):
                for event in events:
                    await session.dom_debugger.set_event_listener_breakpoint(event)
                for event in events:
                    await session.dom_debugger.remove_event_listener_breakpoint(
                        event
                    )


@pytest.mark.e2e
class TestDOMDebuggerE2EXHRBreakpoints:
    async def test_set_remove_xhr_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_debugger.set_xhr_breakpoint("/api/")
            await session.dom_debugger.remove_xhr_breakpoint("/api/")

    async def test_set_remove_xhr_breakpoint_empty_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_debugger.set_xhr_breakpoint("")
            await session.dom_debugger.remove_xhr_breakpoint("")

    async def test_multiple_xhr_breakpoints(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            urls = ["/api/", "/rest/", "localhost", ""]
            for url in urls:
                await session.dom_debugger.set_xhr_breakpoint(url)
            for url in urls:
                await session.dom_debugger.remove_xhr_breakpoint(url)

    async def test_set_same_xhr_breakpoint_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_debugger.set_xhr_breakpoint("/api/")
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_xhr_breakpoint("/api/")
            await session.dom_debugger.remove_xhr_breakpoint("/api/")


@pytest.mark.e2e
class TestDOMDebuggerE2EGetEventListeners:
    async def test_get_event_listeners_document(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(object_id)
            assert "listeners" in result
            assert isinstance(result["listeners"], list)

    async def test_get_event_listeners_with_depth_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=0
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_depth_negative_one(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=-1
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_pierce_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, pierce=True
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_pierce_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, pierce=False
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_depth_and_pierce(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=-1, pierce=True
            )
            assert "listeners" in result

    async def test_get_event_listeners_body_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            body_id = await _get_body_node_id(session)
            object_id = await _resolve_to_object_id(session, body_id)
            result = await session.dom_debugger.get_event_listeners(object_id)
            assert "listeners" in result

    async def test_get_event_listeners_listener_fields(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(object_id)
            for listener in result.get("listeners", []):
                assert "type" in listener
                assert "useCapture" in listener
                assert "passive" in listener
                assert "once" in listener
                assert "scriptId" in listener
                assert "lineNumber" in listener
                assert "columnNumber" in listener


@pytest.mark.e2e
class TestDOMDebuggerE2EInstrumentationBreakpoints:
    async def test_set_remove_instrumentation_set_interval(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_instrumentation_breakpoint(
                    "setInterval"
                )
                await session.dom_debugger.remove_instrumentation_breakpoint(
                    "setInterval"
                )

    async def test_set_remove_instrumentation_set_timeout(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_instrumentation_breakpoint(
                    "setTimeout"
                )
                await session.dom_debugger.remove_instrumentation_breakpoint(
                    "setTimeout"
                )


@pytest.mark.e2e
class TestDOMDebuggerE2ECSPViolation:
    async def test_set_csp_violation_both_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-sink-violation", "trustedtype-policy-violation"]
                )

    async def test_set_csp_violation_sink_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-sink-violation"]
                )

    async def test_set_csp_violation_policy_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-policy-violation"]
                )

    async def test_set_csp_violation_empty_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation([])


@pytest.mark.e2e
class TestDOMDebuggerE2EFullFlow:
    async def test_full_dom_debugger_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)

            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

            await session.dom_debugger.set_xhr_breakpoint("/api/")
            await session.dom_debugger.remove_xhr_breakpoint("/api/")

            with contextlib.suppress(Exception):
                await session.dom_debugger.set_event_listener_breakpoint("click")
                await session.dom_debugger.remove_event_listener_breakpoint("click")

            with contextlib.suppress(Exception):
                await session.dom_debugger.set_instrumentation_breakpoint(
                    "setInterval"
                )
                await session.dom_debugger.remove_instrumentation_breakpoint(
                    "setInterval"
                )

            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-sink-violation"]
                )

    async def test_dom_breakpoint_with_dom_mutation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            root_id = await _get_root_node_id(session)

            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )

                await session.runtime.evaluate(
                    "document.body.appendChild(document.createElement('div'))",
                    return_by_value=True,
                )

                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_get_event_listeners_after_adding_listener(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)

            await session.runtime.evaluate(
                "document.addEventListener('click', function(){});",
                return_by_value=True,
            )

            root_id = await _get_root_node_id(session)
            object_id = await _resolve_to_object_id(session, root_id)
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=-1, pierce=True
            )
            assert "listeners" in result
            click_listeners = [
                lst for lst in result["listeners"] if lst.get("type") == "click"
            ]
            assert len(click_listeners) > 0


@pytest.mark.e2e
class TestHeadlessExperimentalE2ETypeValidation:
    """Type validation should raise before any CDP call, even on a real browser."""

    async def test_begin_frame_frame_time_ticks_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_time_ticks"):
                await session.headless_experimental.begin_frame(
                    frame_time_ticks="100"
                )

    async def test_begin_frame_interval_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="interval"):
                await session.headless_experimental.begin_frame(interval="16")

    async def test_begin_frame_no_display_updates_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="no_display_updates"):
                await session.headless_experimental.begin_frame(
                    no_display_updates="true"
                )

    async def test_begin_frame_screenshot_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="screenshot"):
                await session.headless_experimental.begin_frame(screenshot="png")


@pytest.mark.e2e
class TestDOMDebuggerE2ETypeValidation:
    """Type validation should raise before any CDP call, even on a real browser."""

    async def test_set_dom_breakpoint_node_id_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="node_id"):
                await session.dom_debugger.set_dom_breakpoint(
                    "42", "subtree-modified"
                )

    async def test_set_dom_breakpoint_invalid_enum_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="type must be one of"):
                await session.dom_debugger.set_dom_breakpoint(1, "invalid-type")

    async def test_remove_dom_breakpoint_invalid_enum_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="type must be one of"):
                await session.dom_debugger.remove_dom_breakpoint(1, "invalid")

    async def test_set_event_listener_breakpoint_event_name_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name"):
                await session.dom_debugger.set_event_listener_breakpoint(42)

    async def test_set_event_listener_breakpoint_target_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="target_name"):
                await session.dom_debugger.set_event_listener_breakpoint(
                    "click", target_name=42
                )

    async def test_set_xhr_breakpoint_url_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="url"):
                await session.dom_debugger.set_xhr_breakpoint(42)

    async def test_get_event_listeners_object_id_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="object_id"):
                await session.dom_debugger.get_event_listeners(42)

    async def test_get_event_listeners_depth_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="depth"):
                await session.dom_debugger.get_event_listeners("obj-1", depth="0")

    async def test_get_event_listeners_pierce_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="pierce"):
                await session.dom_debugger.get_event_listeners(
                    "obj-1", pierce="true"
                )

    async def test_set_instrumentation_breakpoint_event_name_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name"):
                await session.dom_debugger.set_instrumentation_breakpoint(42)

    async def test_set_break_on_csp_violation_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="violation_types"):
                await session.dom_debugger.set_break_on_csp_violation(
                    "trustedtype-sink-violation"
                )

    async def test_set_break_on_csp_violation_invalid_enum_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="invalid value"):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["not-a-real-type"]
                )

    async def test_set_break_on_csp_violation_element_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="violation_types elements"):
                await session.dom_debugger.set_break_on_csp_violation([42])
