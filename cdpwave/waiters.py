"""Wait helpers for common CDP automation conditions.

Provides convenience methods that combine event subscriptions and
polling to wait for navigation, selectors, load states, and network
idle. All helpers accept a configurable timeout.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cdpwave.client import CDPSession

logger = logging.getLogger("cdpwave.waiters")

DEFAULT_TIMEOUT = 30.0
POLL_INTERVAL = 0.1
NETWORK_IDLE_THRESHOLD = 500  # ms without requests


async def wait_for_navigation(
    session: CDPSession,
    url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Wait for a navigation event.

    Subscribes to ``Page.frameNavigated`` and resolves when the
    main frame navigates. If ``url`` is provided, waits until the
    navigation reaches that URL.

    Args:
        session: The CDP session to wait on.
        url: Optional URL to wait for (substring match).
        timeout: Maximum seconds to wait.

    Returns:
        The ``Page.frameNavigated`` event params.

    Raises:
        TimeoutError: If navigation doesn't happen within ``timeout``.
    """
    event = asyncio.Event()
    captured: list[dict[str, Any]] = []

    async def _handler(params: dict[str, Any]) -> None:
        frame = params.get("frame", {})
        if url is not None and url not in frame.get("url", ""):
            return
        captured.append(params)
        event.set()

    sub = session.on("Page.frameNavigated", _handler)
    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        return captured[0]
    finally:
        sub.unsubscribe()


async def wait_for_load_state(
    session: CDPSession,
    state: str = "load",
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Wait for a specific page lifecycle event.

    Listens for ``Page.lifecycleEvent`` and resolves when the
    given lifecycle state is reached.

    Args:
        session: The CDP session to wait on.
        state: Lifecycle state to wait for. One of:
            ``"DOMContentLoaded"``, ``"load"``, ``"networkIdle"``,
            ``"firstPaint"``, ``"firstContentfulPaint"``,
            ``"firstMeaningfulPaint"``.
        timeout: Maximum seconds to wait.

    Returns:
        The ``Page.lifecycleEvent`` event params.

    Raises:
        TimeoutError: If the state isn't reached within ``timeout``.
    """
    event = asyncio.Event()
    captured: list[dict[str, Any]] = []

    async def _handler(params: dict[str, Any]) -> None:
        if params.get("name") == state:
            captured.append(params)
            event.set()

    sub = session.on("Page.lifecycleEvent", _handler)
    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        return captured[0]
    finally:
        sub.unsubscribe()


async def wait_for_selector(
    session: CDPSession,
    selector: str,
    root_node_id: int = 1,
    timeout: float = DEFAULT_TIMEOUT,
    poll_interval: float = POLL_INTERVAL,
) -> int:
    """Wait for a CSS selector to appear in the DOM.

    Polls ``DOM.querySelector`` until the selector matches a node
    or the timeout expires.

    Args:
        session: The CDP session to use.
        selector: CSS selector to wait for.
        root_node_id: Root node ID to query from (default: document).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.

    Returns:
        The DOM node ID of the matched element.

    Raises:
        TimeoutError: If the selector doesn't match within ``timeout``.
    """
    deadline = asyncio.get_running_loop().time() + timeout
    while asyncio.get_running_loop().time() < deadline:
        result = await session.dom.query_selector(root_node_id, selector)
        node_id: int = result.get("nodeId", 0)
        if node_id and node_id != 0:
            return node_id
        remaining = deadline - asyncio.get_running_loop().time()
        if remaining <= 0:
            break
        await asyncio.sleep(min(poll_interval, remaining))
    raise TimeoutError(
        f"Selector '{selector}' not found within {timeout}s",
    )


async def wait_for_network_idle(
    session: CDPSession,
    idle_time: float = 0.5,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """Wait until network activity settles.

    Tracks ``Network.requestWillBeSent`` and ``Network.responseReceived``
    events. Resolves when no new requests have been initiated for at
    least ``idle_time`` seconds.

    Args:
        session: The CDP session to wait on.
        idle_time: Seconds of no new requests before resolving.
        timeout: Maximum seconds to wait overall.

    Raises:
        TimeoutError: If network doesn't settle within ``timeout``.
    """
    loop = asyncio.get_running_loop()
    last_request_time = loop.time()

    async def _on_request(params: dict[str, Any]) -> None:
        nonlocal last_request_time
        last_request_time = loop.time()

    sub = session.on("Network.requestWillBeSent", _on_request)
    try:
        deadline = loop.time() + timeout
        while True:
            now = loop.time()
            if now >= deadline:
                raise TimeoutError(
                    f"Network did not become idle within {timeout}s",
                )
            if now - last_request_time >= idle_time:
                return
            remaining = deadline - now
            wait = min(idle_time - (now - last_request_time), remaining)
            if wait > 0:
                await asyncio.sleep(wait)
    finally:
        sub.unsubscribe()
