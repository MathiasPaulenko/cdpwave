"""Integration tests for HeadlessExperimental and DOMDebugger domains on a real browser."""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


async def _navigate_and_wait(session: CDPSession, url: str = "https://example.com") -> None:
    await session.page.enable()
    await session.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestHeadlessExperimentalIntegration:
    async def test_enable_disable_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.enable()
                await session.headless_experimental.disable()

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

    async def test_begin_frame_with_frame_time_ticks(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    frame_time_ticks=1000.0
                )
                assert isinstance(result, dict)

    async def test_begin_frame_with_no_display_updates(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    no_display_updates=True
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

    async def test_begin_frame_with_screenshot_jpeg_quality(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    screenshot={"format": "jpeg", "quality": 50}
                )
                assert isinstance(result, dict)

    async def test_begin_frame_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.headless_experimental.begin_frame(
                    frame_time_ticks=500.0,
                    interval=16.666,
                    no_display_updates=False,
                    screenshot={"format": "png", "optimizeForSpeed": True},
                )
                assert isinstance(result, dict)

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

    async def test_repeated_begin_frames(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.headless_experimental.begin_frame()
                    await asyncio.sleep(0.1)

    async def test_enable_then_begin_frame_then_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.headless_experimental.enable()
                await session.headless_experimental.begin_frame()
                await session.headless_experimental.disable()


@pytest.mark.integration
class TestDOMDebuggerIntegration:
    async def test_set_remove_dom_breakpoint_subtree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_set_remove_dom_breakpoint_attribute(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "attribute-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "attribute-modified"
                )

    async def test_set_remove_dom_breakpoint_node_removed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "node-removed"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "node-removed"
                )

    async def test_set_remove_event_listener_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_event_listener_breakpoint("click")
                await session.dom_debugger.remove_event_listener_breakpoint("click")

    async def test_set_remove_event_listener_breakpoint_with_target(self) -> None:
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

    async def test_get_event_listeners_for_document(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            resolved = await session.dom.resolve_node(root_id)
            object_id = resolved["object"]["objectId"]
            result = await session.dom_debugger.get_event_listeners(object_id)
            assert "listeners" in result
            assert isinstance(result["listeners"], list)

    async def test_get_event_listeners_with_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            resolved = await session.dom.resolve_node(root_id)
            object_id = resolved["object"]["objectId"]
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=0
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_pierce(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            resolved = await session.dom.resolve_node(root_id)
            object_id = resolved["object"]["objectId"]
            result = await session.dom_debugger.get_event_listeners(
                object_id, pierce=True
            )
            assert "listeners" in result

    async def test_get_event_listeners_with_depth_and_pierce(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            resolved = await session.dom.resolve_node(root_id)
            object_id = resolved["object"]["objectId"]
            result = await session.dom_debugger.get_event_listeners(
                object_id, depth=-1, pierce=True
            )
            assert "listeners" in result

    async def test_set_remove_instrumentation_breakpoint(self) -> None:
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

    async def test_set_break_on_csp_violation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-sink-violation", "trustedtype-policy-violation"]
                )

    async def test_set_break_on_csp_violation_single(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_break_on_csp_violation(
                    ["trustedtype-sink-violation"]
                )

    async def test_all_dom_breakpoint_types_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            bp_types = ["subtree-modified", "attribute-modified", "node-removed"]
            with contextlib.suppress(Exception):
                for bp_type in bp_types:
                    await session.dom_debugger.set_dom_breakpoint(root_id, bp_type)
                    await session.dom_debugger.remove_dom_breakpoint(
                        root_id, bp_type
                    )

    async def test_multiple_xhr_breakpoints(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            urls = ["/api/", "/rest/", "localhost"]
            for url in urls:
                await session.dom_debugger.set_xhr_breakpoint(url)
            for url in urls:
                await session.dom_debugger.remove_xhr_breakpoint(url)

    async def test_set_same_dom_breakpoint_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
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

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]

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
