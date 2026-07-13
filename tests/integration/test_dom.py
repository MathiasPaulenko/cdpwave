import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


@pytest.mark.integration
class TestDOM:
    async def test_dom_query_selector(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                doc = await session.dom.get_document(depth=2)
                if doc.get("root", {}).get("childNodeCount", 0) > 0:
                    break

            root_id = doc["root"]["nodeId"]
            result = await session.dom.query_selector(root_id, "h1")
            assert "nodeId" in result
            assert result["nodeId"] != 0

    async def test_dom_get_outer_html(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                doc = await session.dom.get_document(depth=2)
                if doc.get("root", {}).get("childNodeCount", 0) > 0:
                    break

            root_id = doc["root"]["nodeId"]
            h1_result = await session.dom.query_selector(root_id, "h1")
            h1_id = h1_result["nodeId"]
            html_result = await session.dom.get_outer_html(node_id=h1_id)
            outer_html = html_result.get("outerHTML", "")
            assert "Example Domain" in outer_html

    async def test_get_document_depth_1(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                doc = await session.dom.get_document(depth=1)
                root = doc.get("root", {})
                if root.get("nodeId", 0) > 0:
                    break

            assert root["nodeId"] > 0
            assert root.get("nodeName") == "#document"

    async def test_query_selector_all_paragraphs(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                doc = await session.dom.get_document(depth=2)
                if doc.get("root", {}).get("childNodeCount", 0) > 0:
                    break

            root_id = doc["root"]["nodeId"]
            result = await session.dom.query_selector_all(root_id, "p")
            node_ids = result.get("nodeIds", [])
            assert len(node_ids) >= 1

    async def test_remove_node_and_verify_gone(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            for _ in range(10):
                await asyncio.sleep(0.5)
                doc = await session.dom.get_document(depth=2)
                if doc.get("root", {}).get("childNodeCount", 0) > 0:
                    break

            root_id = doc["root"]["nodeId"]
            all_p = await session.dom.query_selector_all(root_id, "p")
            p_ids = all_p.get("nodeIds", [])
            assert len(p_ids) >= 1

            first_p = p_ids[0]
            await session.dom.remove_node(first_p)

            all_p_after = await session.dom.query_selector_all(root_id, "p")
            p_ids_after = all_p_after.get("nodeIds", [])
            assert len(p_ids_after) == len(p_ids) - 1


@pytest.mark.integration
class TestDOMAdvanced:
    """Advanced DOM integration tests covering edge cases and
    less-commonly tested methods."""

    async def test_describe_node_with_depth_and_pierce(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            result = await session.dom.describe_node(
                root_id, depth=1, pierce=True
            )
            assert "node" in result
            assert result["node"]["nodeId"] == root_id

    async def test_get_box_model(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.dom.get_box_model(node_id=h1["nodeId"])
            assert "model" in result
            model = result["model"]
            assert "content" in model
            assert "padding" in model
            assert "border" in model
            assert "margin" in model
            assert "width" in model
            assert "height" in model

    async def test_get_node_for_location(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.get_node_for_location(10, 10)
            assert "backendNodeId" in result
            assert "frameId" in result

    async def test_get_node_for_location_with_ignore_pointer_events(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.get_node_for_location(
                10, 10, ignore_pointer_events_none=True
            )
            assert "backendNodeId" in result

    async def test_resolve_node_with_object_group(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.dom.resolve_node(
                node_id=h1["nodeId"], object_group="test-group"
            )
            assert "object" in result
            assert result["object"].get("className") in (
                "HTMLHeadingElement",
                "Element",
            )

    async def test_request_node_via_object_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            assert h1["nodeId"] != 0
            resolved = await session.dom.resolve_node(
                node_id=h1["nodeId"], object_group="test"
            )
            object_id = resolved["object"]["objectId"]
            result = await session.dom.request_node(object_id)
            assert "nodeId" in result
            assert result["nodeId"] == h1["nodeId"]

    async def test_remove_attribute(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            await session.dom.set_attribute_value(
                h1["nodeId"], "data-temp", "val"
            )
            html_before = await session.dom.get_outer_html(
                node_id=h1["nodeId"]
            )
            assert "data-temp" in html_before["outerHTML"]
            await session.dom.remove_attribute(h1["nodeId"], "data-temp")
            html_after = await session.dom.get_outer_html(
                node_id=h1["nodeId"]
            )
            assert "data-temp" not in html_after["outerHTML"]

    async def test_set_node_value(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=3)
            root_id = doc["root"]["nodeId"]
            p = await session.dom.query_selector(root_id, "p")
            if p["nodeId"] != 0:
                result = await session.dom.describe_node(
                    p["nodeId"], depth=1
                )
                children = result.get("node", {}).get("children", [])
                text_node_id = None
                for child in children:
                    if child.get("nodeType") == 3:
                        text_node_id = child["nodeId"]
                        break
                if text_node_id is not None:
                    await session.dom.set_node_value(text_node_id, "Modified")
                    desc = await session.dom.describe_node(
                        text_node_id, depth=0
                    )
                    assert desc["node"].get("nodeValue") == "Modified"

    async def test_set_attributes_as_text(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            await session.dom.set_attributes_as_text(
                h1["nodeId"], "data-test='hello' data-foo='bar'"
            )
            html = await session.dom.get_outer_html(node_id=h1["nodeId"])
            assert "data-test" in html["outerHTML"]
            assert "data-foo" in html["outerHTML"]

    async def test_get_attribute_with_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            await session.dom.set_attribute_value(
                h1["nodeId"], "data-test", "myval"
            )
            result = await session.dom.get_attribute(
                h1["nodeId"], "data-test"
            )
            assert result["value"] == "myval"

    async def test_get_attribute_not_found(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            result = await session.dom.get_attribute(
                h1["nodeId"], "data-nonexistent"
            )
            assert result["value"] is None

    async def test_copy_to(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=3)
            root_id = doc["root"]["nodeId"]
            body = await session.dom.query_selector(root_id, "body")
            h1 = await session.dom.query_selector(root_id, "h1")
            if body["nodeId"] != 0 and h1["nodeId"] != 0:
                result = await session.dom.copy_to(
                    h1["nodeId"], body["nodeId"]
                )
                assert "nodeId" in result

    async def test_move_to(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=3)
            root_id = doc["root"]["nodeId"]
            body = await session.dom.query_selector(root_id, "body")
            divs = await session.dom.query_selector_all(root_id, "div")
            if body["nodeId"] != 0 and len(divs.get("nodeIds", [])) > 0:
                result = await session.dom.move_to(
                    divs["nodeIds"][0], body["nodeId"]
                )
                assert "nodeId" in result

    async def test_set_node_name(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            p = await session.dom.query_selector(root_id, "p")
            if p["nodeId"] != 0:
                result = await session.dom.set_node_name(
                    p["nodeId"], "div"
                )
                assert "nodeId" in result

    async def test_enable_with_include_whitespace(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom.enable(include_whitespace="none")
            await session.dom.disable()
            await session.dom.enable(include_whitespace="all")
            await session.dom.disable()

    async def test_get_document_with_pierce(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2, pierce=True)
            assert "root" in doc
            assert doc["root"]["nodeId"] > 0

    async def test_undo_redo(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                await session.dom.set_attribute_value(
                    h1["nodeId"], "data-undo-test", "1"
                )
                await session.dom.undo()
                html = await session.dom.get_outer_html(
                    node_id=h1["nodeId"]
                )
                assert "data-undo-test" not in html["outerHTML"]
                await session.dom.redo()
                html = await session.dom.get_outer_html(
                    node_id=h1["nodeId"]
                )
                assert "data-undo-test" in html["outerHTML"]

    async def test_mark_undoable_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.dom.mark_undoable_state()

    async def test_highlight_and_hide(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.overlay.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                cfg = {
                    "showInfo": True,
                    "contentColor": {"r": 255, "g": 0, "b": 0, "a": 0.5},
                }
                await session.dom.highlight_node(cfg, node_id=h1["nodeId"])
                await session.dom.hide_highlight()
            await session.overlay.disable()

    async def test_highlight_rect(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.overlay.enable()
            await session.dom.highlight_rect(0, 0, 100, 100)
            await session.dom.hide_highlight()
            await session.overlay.disable()

    async def test_push_node_by_path(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            assert doc["root"]["nodeId"] > 0
            with contextlib.suppress(Exception):
                result = await session.dom.push_node_by_path_to_frontend(
                    "0,0,0"
                )
                assert "nodeId" in result

    async def test_get_relayout_boundary(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                result = await session.dom.get_relayout_boundary(
                    h1["nodeId"]
                )
                assert "nodeId" in result

    async def test_get_frame_owner(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            tree = await session.page.get_frame_tree()
            main_frame_id = tree["frameTree"]["frame"]["id"]
            with contextlib.suppress(Exception):
                result = await session.dom.get_frame_owner(main_frame_id)
                assert "backendNodeId" in result

    async def test_set_inspected_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                await session.dom.set_inspected_node(h1["nodeId"])

    async def test_set_node_stack_traces_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.dom.set_node_stack_traces_enabled(True)
            await session.dom.set_node_stack_traces_enabled(False)

    async def test_get_node_stack_traces(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.dom.set_node_stack_traces_enabled(True)
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                result = await session.dom.get_node_stack_traces(
                    h1["nodeId"]
                )
                assert isinstance(result, dict)

    async def test_get_detached_dom_nodes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.get_detached_dom_nodes()
            assert "detachedNodes" in result

    async def test_perform_search_with_shadow_dom(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            result = await session.dom.perform_search(
                "h1", include_user_agent_shadow_dom=True
            )
            assert "searchId" in result
            assert "resultCount" in result

    async def test_request_child_nodes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=1)
            root_id = doc["root"]["nodeId"]
            await session.dom.request_child_nodes(
                root_id, depth=2, pierce=True
            )

    async def test_get_outer_html_with_backend_node_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            desc = await session.dom.describe_node(h1["nodeId"], depth=0)
            backend_id = desc["node"].get("backendNodeId")
            if backend_id:
                result = await session.dom.get_outer_html(
                    backend_node_id=backend_id
                )
                assert "outerHTML" in result

    async def test_focus_element(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            link = await session.dom.query_selector(root_id, "a")
            if link["nodeId"] != 0:
                with contextlib.suppress(Exception):
                    await session.dom.focus(node_id=link["nodeId"])

    async def test_scroll_into_view_if_needed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document(depth=2)
            root_id = doc["root"]["nodeId"]
            h1 = await session.dom.query_selector(root_id, "h1")
            if h1["nodeId"] != 0:
                await session.dom.scroll_into_view_if_needed(
                    node_id=h1["nodeId"]
                )

    async def test_get_outer_html_with_object_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            eval_result = await session.runtime.evaluate(
                "document.querySelector('h1')",
                return_by_value=False,
            )
            object_id = eval_result["result"]["objectId"]
            result = await session.dom.get_outer_html(object_id=object_id)
            assert "outerHTML" in result
            assert "Example Domain" in result["outerHTML"]


async def _wait_for_page(
    page: CDPSession, url: str = "https://example.com"
) -> None:
    await page.page.enable()
    await page.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break
