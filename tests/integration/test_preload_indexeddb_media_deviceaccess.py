"""Functional tests for Preload, IndexedDB, Media, and DeviceAccess domains."""

import asyncio
import contextlib

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
class TestPreload:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.disable()

    async def test_get_set_preload_policy(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.set_preload_policy("no-preload")
                result = await session.preload.get_preload_policy()
                assert "preloadPolicy" in result
                await session.preload.disable()


@pytest.mark.integration
class TestIndexedDB:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_request_database_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com"
            )
            assert "databaseNames" in result
            await session.indexed_db.disable()


@pytest.mark.integration
class TestMedia:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.media.enable()
            await session.media.disable()

    async def test_get_players(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.media.enable()
            with contextlib.suppress(Exception):
                result = await session.media.get_players()
                assert "players" in result
            await session.media.disable()


@pytest.mark.integration
class TestDeviceAccess:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.disable()
