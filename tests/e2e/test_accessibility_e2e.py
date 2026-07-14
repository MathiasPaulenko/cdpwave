"""E2E tests for the Accessibility domain (real browser flows).

Exercises all Accessibility domain methods end-to-end against a real Chrome
browser, including full AX tree inspection, partial trees, root node, child
nodes, ancestors, queryAXTree, and enable/disable lifecycle.
"""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CDPError


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.dom.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.e2e
class TestAccessibilityE2E:
    """Full end-to-end flows against a real browser."""

    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            await session.accessibility.disable()

    async def test_enable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.enable()
            assert result == {}
            await session.accessibility.disable()

    async def test_disable_returns_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            result = await session.accessibility.disable()
            assert result == {}

    async def test_get_full_ax_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree()
            assert "nodes" in result
            assert len(result["nodes"]) > 0
            node = result["nodes"][0]
            assert "nodeId" in node
            assert "ignored" in node

    async def test_get_full_ax_tree_with_depth(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree(depth=1)
            assert "nodes" in result
            assert len(result["nodes"]) > 0

    async def test_get_full_ax_tree_depth_zero(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree(depth=0)
            assert "nodes" in result

    async def test_get_full_ax_tree_shallow_vs_deep(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            shallow = await session.accessibility.get_full_ax_tree(depth=1)
            full = await session.accessibility.get_full_ax_tree()
            assert len(shallow["nodes"]) <= len(full["nodes"])

    async def test_get_partial_ax_tree_with_node_id(self) -> None:
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
            assert len(result["nodes"]) > 0

    async def test_get_partial_ax_tree_fetch_relatives_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.get_partial_ax_tree(
                node_id=root_id, fetch_relatives=True
            )
            assert "nodes" in result

    async def test_get_partial_ax_tree_fetch_relatives_false(self) -> None:
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

    async def test_get_root_ax_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            result = await session.accessibility.get_root_ax_node()
            assert "node" in result
            assert "nodeId" in result["node"]
            await session.accessibility.disable()

    async def test_get_root_ax_node_without_enable_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CDPError):
                await session.accessibility.get_root_ax_node()

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

    async def test_get_child_ax_nodes_returns_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            root = await session.accessibility.get_root_ax_node()
            root_id = root["node"]["nodeId"]
            result = await session.accessibility.get_child_ax_nodes(root_id)
            assert isinstance(result["nodes"], list)
            await session.accessibility.disable()

    async def test_get_child_ax_nodes_invalid_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            with pytest.raises(CDPError):
                await session.accessibility.get_child_ax_nodes(
                    "nonexistent-ax-id"
                )
            await session.accessibility.disable()

    async def test_query_ax_tree_by_role(self) -> None:
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
            for node in result["nodes"]:
                if node.get("role"):
                    assert node["role"]["value"] == "link"

    async def test_query_ax_tree_by_accessible_name(self) -> None:
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

    async def test_query_ax_tree_role_and_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            result = await session.accessibility.query_ax_tree(
                node_id=root_id, accessible_name="Example", role="link"
            )
            assert "nodes" in result

    async def test_get_ax_node_and_ancestors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.accessibility.enable()
            doc = await session.dom.get_document()
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


@pytest.mark.e2e
class TestAccessibilityFullFlow:
    """Multi-step flows combining Accessibility with other domains."""

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

    async def test_ax_query_multiple_roles(self) -> None:
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

    async def test_full_lifecycle(self) -> None:
        """Full lifecycle: enable → getRoot → getChildren → query → disable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.accessibility.enable()

            root = await session.accessibility.get_root_ax_node()
            assert "node" in root

            children = await session.accessibility.get_child_ax_nodes(
                root["node"]["nodeId"]
            )
            assert "nodes" in children

            doc = await session.dom.get_document()
            tree = await session.accessibility.get_full_ax_tree()
            assert "nodes" in tree

            partial = await session.accessibility.get_partial_ax_tree(
                node_id=doc["root"]["nodeId"]
            )
            assert "nodes" in partial

            queried = await session.accessibility.query_ax_tree(
                node_id=doc["root"]["nodeId"]
            )
            assert "nodes" in queried

            await session.accessibility.disable()

    async def test_repeated_enable_disable(self) -> None:
        """3 cycles of enable/disable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            for _ in range(3):
                await session.accessibility.enable()
                await session.accessibility.disable()
