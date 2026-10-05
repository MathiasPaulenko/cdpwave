"""Integration regression tests for bugs fixed in the full audit.

Covers: auto-attach event routing, waiter setup (Page.enable /
lifecycle events), and the synchronous API over a real connection.
"""

import asyncio
import contextlib
import sys

import pytest

from cdpwave import CDPClient
from cdpwave.sync import SyncCDPClient

pytestmark = pytest.mark.integration


@pytest.fixture
async def client():
    c = await CDPClient.launch(headless=True)
    yield c
    with contextlib.suppress(Exception):
        await c.close()


class TestAutoAttachIntegration:
    async def test_sub_session_created_for_worker(self, client) -> None:
        """Target.attachedToTarget must create a sub-session on the
        parent session (the top-level sessionId is the parent, not
        params.sessionId)."""
        session = await client.new_page("about:blank", auto_attach=True)

        await session.runtime.evaluate(
            "new Worker(URL.createObjectURL(new Blob([''], "
            "{type: 'text/javascript'})))"
        )

        for _ in range(50):
            if session.sub_sessions:
                break
            await asyncio.sleep(0.1)
        assert len(session.sub_sessions) >= 1

        await session.close()

    async def test_attach_event_reaches_handler(self, client) -> None:
        """attachedToTarget events must still be dispatched to handlers
        after the internal sub-session bookkeeping."""
        session = await client.new_page("about:blank", auto_attach=True)
        captured: list[dict] = []

        async def _on_attach(params: dict) -> None:
            captured.append(params)

        session.on("Target.attachedToTarget", _on_attach)

        await session.runtime.evaluate(
            "new Worker(URL.createObjectURL(new Blob([''], "
            "{type: 'text/javascript'})))"
        )

        for _ in range(50):
            if captured:
                break
            await asyncio.sleep(0.1)
        assert captured
        assert captured[0]["targetInfo"]["type"] == "worker"

        await session.close()


class TestWaitersIntegration:
    async def test_wait_for_load_state(self, client) -> None:
        """wait_for_load_state must enable Page + lifecycle events
        itself — previously it timed out unless the caller did it."""
        session = await client.new_page("about:blank")
        task = asyncio.create_task(session.wait_for_load_state("load", timeout=15))
        await asyncio.sleep(0)  # let the waiter subscribe first
        await session.page.navigate(
            "data:text/html,<html><body><h1>hi</h1></body></html>"
        )
        result = await task
        assert result
        await session.close()

    async def test_wait_for_navigation(self, client) -> None:
        """wait_for_navigation must enable the Page domain itself."""
        session = await client.new_page("about:blank")
        task = asyncio.create_task(
            session.wait_for_navigation(url="example", timeout=15)
        )
        await asyncio.sleep(0)
        await session.page.navigate("https://example.com")
        result = await task
        assert "example" in result["frame"]["url"]
        await session.close()

    async def test_wait_for_load_state_dom_content_loaded(self, client) -> None:
        session = await client.new_page("about:blank")
        task = asyncio.create_task(
            session.wait_for_load_state("DOMContentLoaded", timeout=15)
        )
        await asyncio.sleep(0)
        await session.page.navigate(
            "data:text/html,<html><body><h1>hi</h1></body></html>"
        )
        result = await task
        assert result
        await session.close()


class TestSyncAPIIntegration:
    def test_sync_client_full_flow(self) -> None:
        """The sync client must keep a persistent loop — launch, page,
        evaluate, and close all on the same event loop."""
        with SyncCDPClient.launch(headless=True) as client:
            page = client.new_page("about:blank")
            page.page.navigate("data:text/html,<title>SyncTest</title>")
            result = page.runtime.evaluate(
                "document.title", return_by_value=True
            )
            assert result["result"]["value"] == "SyncTest"
            page.close()

    @pytest.mark.skipif(sys.platform != "linux", reason="pipe is POSIX-only")
    def test_sync_client_pipe_launch(self) -> None:
        with SyncCDPClient.launch(headless=True, pipe=True) as client:
            info = client.send("Browser.getVersion")
            assert "product" in info
