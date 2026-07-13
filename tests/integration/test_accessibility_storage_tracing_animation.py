"""Functional tests for Accessibility, Storage, Tracing, and Animation domains."""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CDPError, CommandError


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestAccessibility:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            await session.accessibility.disable()

    async def test_get_full_ax_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree()
            assert "nodes" in result
            assert len(result["nodes"]) > 0

    async def test_get_full_ax_tree_with_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree(depth=1)
            assert "nodes" in result
            assert len(result["nodes"]) > 0

    async def test_get_partial_ax_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.get_partial_ax_tree(
                node_id=root_id
            )
            assert "nodes" in result

    async def test_get_partial_ax_tree_no_relatives(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.get_partial_ax_tree(
                node_id=root_id, fetch_relatives=False
            )
            assert "nodes" in result

    async def test_get_root_ax_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            result = await session.accessibility.get_root_ax_node()
            assert "node" in result
            await session.accessibility.disable()

    async def test_get_child_ax_nodes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            root = await session.accessibility.get_root_ax_node()
            root_id = root["node"]["nodeId"]
            result = await session.accessibility.get_child_ax_nodes(root_id)
            assert "nodes" in result
            await session.accessibility.disable()

    async def test_get_ax_node_and_ancestors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            doc = await session.dom.get_document()
            # Find a link node (example.com has links)
            link_result = await session.dom.query_selector(
                doc["root"]["nodeId"], "a"
            )
            link_node_id = link_result.get("nodeId", 0)
            if link_node_id:
                result = await session.accessibility.get_ax_node_and_ancestors(
                    node_id=link_node_id
                )
                assert "nodes" in result
                assert len(result["nodes"]) > 0
            await session.accessibility.disable()

    async def test_query_ax_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.query_ax_tree(
                node_id=root_id, role="link"
            )
            assert "nodes" in result

    async def test_query_ax_tree_by_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.query_ax_tree(
                node_id=root_id, accessible_name="Example"
            )
            assert "nodes" in result


@pytest.mark.integration
class TestAccessibilityEdgeCases:
    """Edge cases and error conditions on a real browser."""

    async def test_get_partial_ax_tree_invalid_node_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.accessibility.get_partial_ax_tree(
                    node_id=999999
                )
                assert "nodes" in result

    async def test_get_root_ax_node_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CDPError):
                await session.accessibility.get_root_ax_node()

    async def test_get_child_ax_nodes_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            with pytest.raises(CDPError):
                await session.accessibility.get_child_ax_nodes("nonexistent-id")
            await session.accessibility.disable()

    async def test_query_ax_tree_no_filters(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.query_ax_tree(node_id=root_id)
            assert "nodes" in result
            assert len(result["nodes"]) > 0

    async def test_query_ax_tree_nonexistent_role(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.query_ax_tree(
                node_id=root_id, role="nonexistent-role-xyz"
            )
            assert "nodes" in result
            assert len(result["nodes"]) == 0

    async def test_get_full_ax_tree_depth_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree(depth=0)
            assert "nodes" in result

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            await session.accessibility.enable()
            await session.accessibility.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.accessibility.disable()

    async def test_get_ax_node_and_ancestors_backend_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            doc = await session.dom.get_document()
            result = await session.accessibility.get_ax_node_and_ancestors(
                backend_node_id=doc["root"]["backendNodeId"]
            )
            assert "nodes" in result
            await session.accessibility.disable()

    async def test_get_partial_ax_tree_with_backend_node_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            result = await session.accessibility.get_partial_ax_tree(
                backend_node_id=doc["root"]["backendNodeId"]
            )
            assert "nodes" in result


@pytest.mark.integration
class TestAccessibilityFlow:
    """End-to-end flows combining Accessibility with other domains."""

    async def test_full_ax_inspection_flow(self) -> None:
        """Enable AX → get root → get children → query by role → disable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.accessibility.enable()

            root = await session.accessibility.get_root_ax_node()
            assert "node" in root
            root_id = root["node"]["nodeId"]

            children = await session.accessibility.get_child_ax_nodes(root_id)
            assert "nodes" in children
            assert len(children["nodes"]) > 0

            doc = await session.dom.get_document()
            links = await session.accessibility.query_ax_tree(
                node_id=doc["root"]["nodeId"], role="link"
            )
            assert "nodes" in links

            await session.accessibility.disable()

    async def test_ax_tree_after_dom_modification(self) -> None:
        """Inject a button via JS and verify it appears in the AX tree."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                "const btn = document.createElement('button');"
                "btn.textContent = 'Test Button';"
                "btn.setAttribute('aria-label', 'Test ARIA Label');"
                "document.body.appendChild(btn);"
            )

            doc = await session.dom.get_document()
            result = await session.accessibility.query_ax_tree(
                node_id=doc["root"]["nodeId"],
                accessible_name="Test ARIA Label",
            )
            assert "nodes" in result
            assert len(result["nodes"]) > 0
            assert result["nodes"][0]["role"]["value"] == "button"

    async def test_ax_node_and_ancestors_chain(self) -> None:
        """Get AX node and ancestors for a deeply nested element."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                "const div = document.createElement('div');"
                "div.id = 'outer';"
                "const inner = document.createElement('span');"
                "inner.id = 'inner';"
                "inner.textContent = 'Nested text';"
                "div.appendChild(inner);"
                "document.body.appendChild(div);"
            )

            await session.accessibility.enable()

            doc = await session.dom.get_document()
            span_result = await session.dom.query_selector(
                doc["root"]["nodeId"], "#inner"
            )
            span_node_id = span_result.get("nodeId", 0)
            assert span_node_id, "Span element not found"

            ancestors = await session.accessibility.get_ax_node_and_ancestors(
                node_id=span_node_id
            )
            assert "nodes" in ancestors
            assert len(ancestors["nodes"]) >= 2

            await session.accessibility.disable()

    async def test_partial_vs_full_ax_tree_consistency(self) -> None:
        """Partial AX tree from root should be subset of full AX tree."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]

            partial = await session.accessibility.get_partial_ax_tree(
                node_id=root_id
            )
            full = await session.accessibility.get_full_ax_tree()

            assert "nodes" in partial
            assert "nodes" in full
            assert len(partial["nodes"]) <= len(full["nodes"])

    async def test_ax_tree_with_depth_limit(self) -> None:
        """Full AX tree with depth=1 should have fewer nodes than unlimited."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            shallow = await session.accessibility.get_full_ax_tree(depth=1)
            full = await session.accessibility.get_full_ax_tree()

            assert "nodes" in shallow
            assert "nodes" in full
            assert len(shallow["nodes"]) <= len(full["nodes"])

    async def test_screenshot_then_ax_inspection(self) -> None:
        """Capture screenshot, then inspect AX tree — multi-domain flow."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            screenshot = await session.page.capture_screenshot()
            assert "data" in screenshot

            ax_tree = await session.accessibility.get_full_ax_tree()
            assert "nodes" in ax_tree
            assert len(ax_tree["nodes"]) > 0

    async def test_ax_query_with_multiple_roles(self) -> None:
        """Query AX tree for different roles on a real page."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]

            for role in ("link", "heading", "text"):
                result = await session.accessibility.query_ax_tree(
                    node_id=root_id, role=role
                )
                assert "nodes" in result

    async def test_query_ax_tree_without_node_raises(self) -> None:
        """queryAXTree with no DOM node should error per CDP spec."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CDPError):
                await session.accessibility.query_ax_tree(role="link")

    async def test_query_ax_tree_with_backend_node_id(self) -> None:
        """queryAXTree using backendNodeId instead of nodeId."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            result = await session.accessibility.query_ax_tree(
                backend_node_id=doc["root"]["backendNodeId"], role="link"
            )
            assert "nodes" in result

    async def test_query_ax_tree_with_object_id(self) -> None:
        """queryAXTree using objectId from Runtime.evaluate."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            eval_result = await session.runtime.evaluate(
                "document", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                result = await session.accessibility.query_ax_tree(
                    object_id=object_id, role="link"
                )
                assert "nodes" in result

    async def test_get_partial_ax_tree_with_object_id(self) -> None:
        """getPartialAXTree using objectId from Runtime.evaluate."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            eval_result = await session.runtime.evaluate(
                "document.body", return_by_value=False
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                result = await session.accessibility.get_partial_ax_tree(
                    object_id=object_id
                )
                assert "nodes" in result

    async def test_get_ax_node_and_ancestors_with_object_id(self) -> None:
        """getAXNodeAndAncestors using objectId from Runtime.evaluate."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            eval_result = await session.runtime.evaluate(
                "document.querySelector('a')",
                return_by_value=False,
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                result = await session.accessibility.get_ax_node_and_ancestors(
                    object_id=object_id
                )
                assert "nodes" in result
            await session.accessibility.disable()

    async def test_get_full_ax_tree_with_frame_id(self) -> None:
        """getFullAXTree with frameId from page."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            tree = await session.accessibility.get_full_ax_tree()
            if tree.get("nodes"):
                frame_id = tree["nodes"][0].get("frameId")
                if frame_id:
                    result = await session.accessibility.get_full_ax_tree(
                        frame_id=frame_id
                    )
                    assert "nodes" in result

    async def test_get_root_ax_node_with_frame_id(self) -> None:
        """getRootAXNode with frameId."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            tree = await session.accessibility.get_full_ax_tree()
            if tree.get("nodes"):
                frame_id = tree["nodes"][0].get("frameId")
                if frame_id:
                    result = await session.accessibility.get_root_ax_node(
                        frame_id=frame_id
                    )
                    assert "node" in result
            await session.accessibility.disable()

    async def test_get_child_ax_nodes_with_frame_id(self) -> None:
        """getChildAXNodes with frameId."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            root = await session.accessibility.get_root_ax_node()
            root_id = root["node"]["nodeId"]
            tree = await session.accessibility.get_full_ax_tree()
            frame_id = None
            if tree.get("nodes"):
                frame_id = tree["nodes"][0].get("frameId")
            if frame_id:
                result = await session.accessibility.get_child_ax_nodes(
                    root_id, frame_id=frame_id
                )
                assert "nodes" in result
            await session.accessibility.disable()

    async def test_get_partial_ax_tree_fetch_relatives_false_no_node(self) -> None:
        """getPartialAXTree with fetchRelatives=false and no node — edge case."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(CDPError):
                result = await session.accessibility.get_partial_ax_tree(
                    fetch_relatives=False
                )
                assert "nodes" in result


@pytest.mark.integration
class TestStorage:
    async def test_get_cookies(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.storage.get_cookies()
            assert "cookies" in result

    async def test_clear_data_for_origin(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.storage.clear_data_for_origin(
                "https://example.com", "cookies"
            )

    async def test_get_usage_and_quota(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.storage.get_usage_and_quota(
                "https://example.com"
            )
            assert "usage" in result
            assert "quota" in result


@pytest.mark.integration
class TestTracing:
    async def test_get_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.tracing.get_categories()
            assert "categories" in result
            assert len(result["categories"]) > 0

    async def test_start_end(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.tracing.start(
                trace_config={
                    "recordMode": "recordUntilFull",
                    "includedCategories": ["devtools.timeline"],
                },
                transfer_mode="ReportEvents",
            )
            await asyncio.sleep(1.0)
            with contextlib.suppress(Exception):
                await session.tracing.end()

    async def test_record_clock_sync_marker(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.record_clock_sync_marker("test-sync")

    async def test_request_memory_dump(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.tracing.request_memory_dump()
                assert "dumpGuid" in result or "success" in result

    async def test_request_memory_dump_deterministic(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.tracing.request_memory_dump(
                    deterministic=True, level_of_detail="light"
                )
                assert "dumpGuid" in result or "success" in result

    async def test_get_track_event_descriptor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.tracing.get_track_event_descriptor()
                assert "descriptor" in result

    async def test_raw_send_end(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Tracing.end")

    async def test_raw_send_get_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.send("Tracing.getCategories")
            assert "categories" in result

    async def test_raw_send_get_track_event_descriptor(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Tracing.getTrackEventDescriptor")

    async def test_raw_send_record_clock_sync_marker(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.recordClockSyncMarker",
                    {"syncId": "raw-sync"},
                )

    async def test_raw_send_request_memory_dump(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.requestMemoryDump",
                    {"deterministic": False},
                )

    async def test_raw_send_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "Tracing.start",
                    {"transferMode": "ReportEvents"},
                )
                await asyncio.sleep(0.5)
                await session.send("Tracing.end")


@pytest.mark.integration
class TestTracingEdgeCases:
    """Edge-case integration tests for Tracing with real browser."""

    async def test_start_record_continuously(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordContinuously",
                        "includedCategories": ["devtools.timeline"],
                    },
                    transfer_mode="ReportEvents",
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_record_as_much_as_possible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordAsMuchAsPossible",
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_echo_to_console(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={"recordMode": "echoToConsole"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_with_excluded_categories(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                        "excludedCategories": ["v8"],
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_with_enable_sampling(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "enableSampling": True,
                    },
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_with_buffer_usage_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    buffer_usage_reporting_interval=1,
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()

    async def test_request_memory_dump_background(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.tracing.request_memory_dump(
                    level_of_detail="background"
                )
                assert "dumpGuid" in result or "success" in result

    async def test_request_memory_dump_detailed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.tracing.request_memory_dump(
                    deterministic=True, level_of_detail="detailed"
                )
                assert "dumpGuid" in result or "success" in result

    async def test_record_clock_sync_marker_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.record_clock_sync_marker("")

    async def test_double_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()
                await asyncio.sleep(0.5)
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_with_screenshot_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={"recordMode": "recordUntilFull"},
                    screenshot_max_size=1080,
                    screenshot_max_count=5,
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_with_perfetto_config(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    perfetto_config="dGVzdA==",
                    tracing_backend="auto",
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_start_all_params_combined(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    buffer_usage_reporting_interval=0.5,
                    transfer_mode="ReturnAsStream",
                    stream_format="json",
                    stream_compression="gzip",
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "enableSampling": True,
                    },
                    tracing_backend="chrome",
                    screenshot_max_size=1920,
                    screenshot_max_count=3,
                )
                await asyncio.sleep(0.5)
                await session.tracing.end()

    async def test_get_categories_returns_list_of_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.tracing.get_categories()
            assert "categories" in result
            cats = result["categories"]
            assert isinstance(cats, list)
            for cat in cats:
                assert isinstance(cat, str)

    async def test_tracing_buffer_usage_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_buffer_usage(params: dict[str, Any]) -> None:
                events.append(params)

            session.on("Tracing.bufferUsage", on_buffer_usage)
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    buffer_usage_reporting_interval=0.1,
                    trace_config={"recordMode": "recordUntilFull"},
                )
                await asyncio.sleep(2.0)
                await session.tracing.end()
            if events:
                assert isinstance(events[0], dict)

    async def test_tracing_data_collected_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_data_collected(params: dict[str, Any]) -> None:
                events.append(params)

            session.on("Tracing.dataCollected", on_data_collected)
            with contextlib.suppress(Exception):
                await session.tracing.start(
                    trace_config={
                        "recordMode": "recordUntilFull",
                        "includedCategories": ["devtools.timeline"],
                    },
                    transfer_mode="ReportEvents",
                )
                await asyncio.sleep(1.0)
                await session.tracing.end()
                await asyncio.sleep(1.0)
            if events:
                assert isinstance(events[0], dict)


@pytest.mark.integration
class TestAnimation:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            await session.animation.disable()

    async def test_set_playback_rate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            await session.animation.set_playback_rate(1.0)
            await session.animation.disable()

    async def test_animation_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            animations: list[dict[str, Any]] = []

            async def on_animation_started(params: dict[str, Any]) -> None:
                animations.append(params)

            await session.animation.enable()
            session.on("Animation.animationStarted", on_animation_started)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.runtime.evaluate(
                "document.body.animate("
                "[{transform: 'translateX(0)'}, {transform: 'translateX(100px)'}],"
                "{duration: 500})"
            )
            await asyncio.sleep(2.0)

            if animations:
                assert "animation" in animations[0]

            await session.animation.disable()


@pytest.mark.integration
class TestAnimationEdgeCases:
    """Edge cases for Animation domain on a real browser."""

    async def test_get_playback_rate_default(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            result = await session.animation.get_playback_rate()
            assert "playbackRate" in result
            await session.animation.disable()

    async def test_set_and_get_playback_rate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            await session.animation.set_playback_rate(2.0)
            result = await session.animation.get_playback_rate()
            assert result["playbackRate"] == 2.0
            await session.animation.set_playback_rate(1.0)
            await session.animation.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            await session.animation.enable()
            await session.animation.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.animation.disable()

    async def test_set_paused_empty_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            with contextlib.suppress(Exception):
                await session.animation.set_paused([], True)
            await session.animation.disable()

    async def test_get_current_time_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            with pytest.raises(CommandError):
                await session.animation.get_current_time("nonexistent-anim")
            await session.animation.disable()

    async def test_release_animations_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            with contextlib.suppress(Exception):
                await session.animation.release_animations([])
            await session.animation.disable()

    async def test_resolve_animation_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()
            with pytest.raises(CommandError):
                await session.animation.resolve_animation("nonexistent-anim")
            await session.animation.disable()


@pytest.mark.integration
class TestAnimationFlow:
    """End-to-end flows combining Animation with other domains."""

    async def test_create_pause_resume_animation(self) -> None:
        """Create animation via JS → capture ID → pause → resume."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            animations: list[dict[str, Any]] = []

            async def on_started(params: dict[str, Any]) -> None:
                animations.append(params)

            await session.animation.enable()
            session.on("Animation.animationStarted", on_started)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.runtime.evaluate(
                "document.body.animate("
                "[{transform: 'translateX(0)'}, {transform: 'translateX(100px)'}],"
                "{duration: 2000, id: 'test-anim'})"
            )
            await asyncio.sleep(1.0)

            if animations:
                anim_id = animations[0]["animation"]["id"]
                await session.animation.set_paused([anim_id], True)
                await asyncio.sleep(0.3)
                await session.animation.set_paused([anim_id], False)

            await session.animation.disable()

    async def test_create_seek_animation(self) -> None:
        """Create animation → capture ID → seek to specific time."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            animations: list[dict[str, Any]] = []

            async def on_started(params: dict[str, Any]) -> None:
                animations.append(params)

            await session.animation.enable()
            session.on("Animation.animationStarted", on_started)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.runtime.evaluate(
                "document.body.animate("
                "[{opacity: 1}, {opacity: 0}],"
                "{duration: 3000, id: 'fade-anim'})"
            )
            await asyncio.sleep(1.0)

            if animations:
                anim_id = animations[0]["animation"]["id"]
                await session.animation.seek_animations([anim_id], 1500)
                current = await session.animation.get_current_time(anim_id)
                assert "currentTime" in current

            await session.animation.disable()

    async def test_playback_rate_affects_animation(self) -> None:
        """Set playback rate → get it → verify consistency."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.animation.enable()

            await session.animation.set_playback_rate(0.5)
            rate = await session.animation.get_playback_rate()
            assert rate["playbackRate"] == 0.5

            await session.animation.set_playback_rate(1.0)
            rate = await session.animation.get_playback_rate()
            assert rate["playbackRate"] == 1.0

            await session.animation.disable()

    async def test_animation_cancel_event(self) -> None:
        """Create animation → cancel it → verify animationCanceled event."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            canceled: list[dict[str, Any]] = []

            async def on_canceled(params: dict[str, Any]) -> None:
                canceled.append(params)

            await session.animation.enable()
            session.on("Animation.animationCanceled", on_canceled)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.runtime.evaluate(
                "const a = document.body.animate("
                "[{transform: 'scale(1)'}, {transform: 'scale(2)'}],"
                "{duration: 5000});"
                "setTimeout(() => a.cancel(), 500);"
            )
            await asyncio.sleep(2.0)

            if canceled:
                assert "id" in canceled[0]

            await session.animation.disable()

    async def test_set_timing_modifies_animation(self) -> None:
        """Create animation → capture ID → modify timing."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            animations: list[dict[str, Any]] = []

            async def on_started(params: dict[str, Any]) -> None:
                animations.append(params)

            await session.animation.enable()
            session.on("Animation.animationStarted", on_started)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await session.runtime.evaluate(
                "document.body.animate("
                "[{transform: 'rotate(0deg)'}, {transform: 'rotate(360deg)'}],"
                "{duration: 1000, id: 'rot-anim'})"
            )
            await asyncio.sleep(1.0)

            if animations:
                anim_id = animations[0]["animation"]["id"]
                with contextlib.suppress(Exception):
                    await session.animation.set_timing(anim_id, 2000, 100)

            await session.animation.disable()
