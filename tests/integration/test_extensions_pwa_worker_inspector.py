"""Functional tests for Extensions, PWA, Worker, and Inspector domains."""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestExtensions:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.extensions is not None

    async def test_get_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.get_storage_items("ext123", "local")


@pytest.mark.integration
class TestPWA:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.pwa is not None

    async def test_get_os_app_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.get_os_app_state("manifest123")


@pytest.mark.integration
class TestWorker:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.worker is not None


@pytest.mark.integration
class TestInspector:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.inspector is not None
