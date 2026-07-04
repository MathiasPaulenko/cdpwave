import asyncio

import pytest

from cdpwave import CDPClient


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
            html_result = await session.dom.get_outer_html(h1_id)
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
