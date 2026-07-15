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

_VALID_LOAD_STATES = frozenset({
    "DOMContentLoaded",
    "load",
    "networkIdle",
    "firstPaint",
    "firstContentfulPaint",
    "firstMeaningfulPaint",
})


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
        ValueError: If ``state`` is not a valid lifecycle state.
        TimeoutError: If the state isn't reached within ``timeout``.
    """
    if state not in _VALID_LOAD_STATES:
        raise ValueError(
            f"Invalid load state {state!r}. "
            f"Valid states: {sorted(_VALID_LOAD_STATES)}",
        )

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

    Uses a ``MutationObserver`` via ``Runtime.evaluate`` to detect when
    the selector appears without polling. Falls back to polling
    ``DOM.querySelector`` if the observer approach fails.

    Args:
        session: The CDP session to use.
        selector: CSS selector to wait for.
        root_node_id: Root node ID to query from (default: document).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls (fallback only).

    Returns:
        The DOM node ID of the matched element.

    Raises:
        TimeoutError: If the selector doesn't match within ``timeout``.
    """
    await session.dom.enable()

    js = (
        "new Promise((resolve) => {"
        f"const el = document.querySelector({selector!r});"
        "if (el) { resolve(true); return; }"
        "const obs = new MutationObserver(() => {"
        f"if (document.querySelector({selector!r})) {{ obs.disconnect(); resolve(true); }}"
        "});"
        "obs.observe(document, {childList: true, subtree: true});"
        "})"
    )

    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout

    try:
        eval_result = await asyncio.wait_for(
            session.runtime.evaluate(js, await_promise=True, return_by_value=True),
            timeout=timeout,
        )
        if eval_result.get("result", {}).get("value") is True:
            query = await session.dom.query_selector(root_node_id, selector)
            node_id: int = query.get("nodeId", 0)
            if node_id and node_id != 0:
                return node_id
    except TimeoutError:
        pass

    while loop.time() < deadline:
        query = await session.dom.query_selector(root_node_id, selector)
        node_id = query.get("nodeId", 0)
        if node_id and node_id != 0:
            return node_id
        remaining = deadline - loop.time()
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

    Tracks ``Network.requestWillBeSent``, ``Network.loadingFinished``,
    and ``Network.loadingFailed`` events. Resolves when there are no
    pending requests (requests without a corresponding completion or
    failure) for at least ``idle_time`` seconds.

    Args:
        session: The CDP session to wait on.
        idle_time: Seconds of no pending requests before resolving.
        timeout: Maximum seconds to wait overall.

    Raises:
        TimeoutError: If network doesn't settle within ``timeout``.
    """
    await session.network.enable()

    loop = asyncio.get_running_loop()
    pending: set[str] = set()
    last_activity = loop.time()

    async def _on_request(params: dict[str, Any]) -> None:
        nonlocal last_activity
        req_id = params.get("requestId")
        if req_id:
            pending.add(req_id)
        last_activity = loop.time()

    async def _on_loading_finished(params: dict[str, Any]) -> None:
        nonlocal last_activity
        req_id = params.get("requestId")
        if req_id:
            pending.discard(req_id)
        last_activity = loop.time()

    async def _on_loading_failed(params: dict[str, Any]) -> None:
        nonlocal last_activity
        req_id = params.get("requestId")
        if req_id:
            pending.discard(req_id)
        last_activity = loop.time()

    sub_req = session.on("Network.requestWillBeSent", _on_request)
    sub_done = session.on("Network.loadingFinished", _on_loading_finished)
    sub_fail = session.on("Network.loadingFailed", _on_loading_failed)
    try:
        deadline = loop.time() + timeout
        while True:
            now = loop.time()
            if now >= deadline:
                raise TimeoutError(
                    f"Network did not become idle within {timeout}s",
                )
            if not pending and now - last_activity >= idle_time:
                return
            remaining = deadline - now
            wait = min(idle_time, remaining)
            if wait > 0:
                await asyncio.sleep(max(wait, 0.05))
    finally:
        sub_req.unsubscribe()
        sub_done.unsubscribe()
        sub_fail.unsubscribe()
