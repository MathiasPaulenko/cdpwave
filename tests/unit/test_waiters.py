"""Unit tests for wait_for_* helpers."""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from cdpwave.waiters import (
    wait_for_load_state,
    wait_for_navigation,
    wait_for_network_idle,
    wait_for_selector,
)


def make_session(
    dispatch: dict[str, list] | None = None,
    query_results: list[dict[str, Any]] | None = None,
) -> Any:
    """Create a mock CDPSession for waiter tests."""
    session = MagicMock()
    session._dispatcher = MagicMock()
    session.on = MagicMock(return_value=MagicMock(unsubscribe=MagicMock()))
    session.off = MagicMock()

    dom = MagicMock()
    dom.enable = AsyncMock(return_value={})
    query_idx = 0
    query_results = query_results or []

    async def _query(root: int, selector: str) -> dict[str, Any]:
        nonlocal query_idx
        if query_idx < len(query_results):
            r = query_results[query_idx]
            query_idx += 1
            return r
        return {"nodeId": 0}

    dom.query_selector = _query
    session.dom = dom

    network = MagicMock()
    network.enable = AsyncMock(return_value={})
    network.disable = AsyncMock(return_value={})
    session.network = network

    dispatch = dispatch or {}

    def _on(event_name: str, handler: Any) -> Any:
        if event_name not in dispatch:
            dispatch[event_name] = []
        dispatch[event_name].append(handler)
        return MagicMock(unsubscribe=MagicMock())

    session.on = _on
    return session, dispatch


class TestWaitForNavigation:
    async def test_resolves_on_frame_navigated(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.frameNavigated", []):
                await handler({"frame": {"url": "https://example.com"}})

        task = asyncio.create_task(_fire())
        result = await wait_for_navigation(session, timeout=2.0)
        await task
        assert result["frame"]["url"] == "https://example.com"

    async def test_filters_by_url(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.frameNavigated", []):
                await handler({"frame": {"url": "https://other.com"}})
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.frameNavigated", []):
                await handler({"frame": {"url": "https://example.com/page"}})

        task = asyncio.create_task(_fire())
        result = await wait_for_navigation(
            session, url="example.com", timeout=2.0,
        )
        await task
        assert "example.com" in result["frame"]["url"]

    async def test_timeout(self) -> None:
        session, _ = make_session()
        with pytest.raises(TimeoutError):
            await wait_for_navigation(session, timeout=0.1)


class TestWaitForLoadState:
    async def test_resolves_on_lifecycle_event(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.lifecycleEvent", []):
                await handler({"name": "load"})

        task = asyncio.create_task(_fire())
        result = await wait_for_load_state(session, state="load", timeout=2.0)
        await task
        assert result["name"] == "load"

    async def test_ignores_other_states(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.lifecycleEvent", []):
                await handler({"name": "DOMContentLoaded"})
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.lifecycleEvent", []):
                await handler({"name": "load"})

        task = asyncio.create_task(_fire())
        result = await wait_for_load_state(session, state="load", timeout=2.0)
        await task
        assert result["name"] == "load"

    async def test_timeout(self) -> None:
        session, _ = make_session()
        with pytest.raises(TimeoutError):
            await wait_for_load_state(session, timeout=0.1)

    async def test_invalid_state_raises_value_error(self) -> None:
        session, _ = make_session()
        with pytest.raises(ValueError, match="Invalid load state"):
            await wait_for_load_state(session, state="invalid", timeout=1.0)

    async def test_valid_states_accepted(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Page.lifecycleEvent", []):
                await handler({"name": "networkIdle"})

        task = asyncio.create_task(_fire())
        result = await wait_for_load_state(
            session, state="networkIdle", timeout=2.0,
        )
        await task
        assert result["name"] == "networkIdle"


class TestWaitForSelector:
    async def test_finds_immediately(self) -> None:
        session, _ = make_session(query_results=[{"nodeId": 42}])
        node_id = await wait_for_selector(session, ".btn", timeout=1.0)
        assert node_id == 42

    async def test_finds_after_polling(self) -> None:
        session, _ = make_session(
            query_results=[
                {"nodeId": 0},
                {"nodeId": 0},
                {"nodeId": 7},
            ],
        )
        node_id = await wait_for_selector(
            session, ".btn", timeout=2.0, poll_interval=0.05,
        )
        assert node_id == 7

    async def test_timeout(self) -> None:
        session, _ = make_session(query_results=[{"nodeId": 0}])
        with pytest.raises(TimeoutError):
            await wait_for_selector(
                session, ".missing", timeout=0.2, poll_interval=0.05,
            )


class TestWaitForNetworkIdle:
    async def test_resolves_when_idle(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Network.requestWillBeSent", []):
                await handler({"requestId": "r1"})
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Network.responseReceived", []):
                await handler({"requestId": "r1"})

        task = asyncio.create_task(_fire())
        await wait_for_network_idle(
            session, idle_time=0.2, timeout=2.0,
        )
        await task

    async def test_timeout(self) -> None:
        session, dispatch = make_session()

        async def _keep_firing() -> None:
            while True:
                await asyncio.sleep(0.02)
                for handler in dispatch.get("Network.requestWillBeSent", []):
                    await handler({"requestId": "r"})

        task = asyncio.create_task(_keep_firing())
        with pytest.raises(TimeoutError):
            await wait_for_network_idle(
                session, idle_time=0.3, timeout=0.3,
            )
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    async def test_enable_called_before_wait(self) -> None:
        session, dispatch = make_session()

        async def _fire() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Network.requestWillBeSent", []):
                await handler({"requestId": "r1"})
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Network.responseReceived", []):
                await handler({"requestId": "r1"})

        task = asyncio.create_task(_fire())
        await wait_for_network_idle(
            session, idle_time=0.2, timeout=2.0,
        )
        await task
        session.network.enable.assert_awaited_once()
        session.network.disable.assert_not_awaited()

    async def test_disable_called_on_timeout(self) -> None:
        session, _ = make_session()
        with pytest.raises(TimeoutError):
            await wait_for_network_idle(
                session, idle_time=0.3, timeout=0.1,
            )
        session.network.enable.assert_awaited_once()
        session.network.disable.assert_not_awaited()
