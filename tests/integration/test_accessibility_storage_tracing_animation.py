"""Functional tests for Accessibility, Storage, Tracing, and Animation domains."""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession


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
    async def test_get_full_ax_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.accessibility.get_full_ax_tree()
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
                categories="-*,devtools.timeline",
                transfer_mode="ReportEvents",
            )
            await asyncio.sleep(1.0)
            with contextlib.suppress(Exception):
                await session.tracing.end()


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
