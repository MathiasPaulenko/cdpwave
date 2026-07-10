"""Synchronous wrappers for cdpwave's async API.

Provides ``SyncCDPClient`` and ``SyncCDPSession`` that wrap the async
API using ``asyncio.run()`` internally. Designed for simple scripts
that don't need concurrent operations.

Limitations:
- Cannot call sync methods from within an async context.
- Each call runs in its own event loop if none is running, or uses
  the running loop via ``run_until_complete`` if one exists.
- Event handlers are not supported (no event loop persistence).
"""

from __future__ import annotations

import asyncio
from typing import Any

from cdpwave.client import CDPClient, CDPSession


def _run(coro: Any) -> Any:
    """Run a coroutine synchronously.

    If an event loop is already running, creates a new loop in a
    thread. Otherwise, uses ``asyncio.run()``.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


class SyncCDPSession:
    """Synchronous wrapper around :class:`CDPSession`.

    Delegates calls to the underlying async session, running each
    in an event loop. Domain access (page, runtime, network, etc.)
    is available via properties that return the raw async domain
    — use :meth:`run` to execute async domain methods.
    """

    def __init__(self, session: CDPSession) -> None:
        self._session = session

    def run(self, coro: Any) -> Any:
        """Run an async coroutine synchronously.

        Args:
            coro: A coroutine (e.g. ``session.page.navigate(url)``).

        Returns:
            The coroutine's result.
        """
        return _run(coro)

    def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command synchronously."""
        result: dict[str, Any] = _run(self._session.send(method, params))
        return result

    def wait_for_navigation(
        self,
        url: str | None = None,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Wait for navigation synchronously."""
        result: dict[str, Any] = _run(
            self._session.wait_for_navigation(url=url, timeout=timeout),
        )
        return result

    def wait_for_load_state(
        self,
        state: str = "load",
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Wait for a load state synchronously."""
        result: dict[str, Any] = _run(
            self._session.wait_for_load_state(state=state, timeout=timeout),
        )
        return result

    def wait_for_selector(
        self,
        selector: str,
        root_node_id: int = 1,
        timeout: float = 30.0,
        poll_interval: float = 0.1,
    ) -> int:
        """Wait for a selector synchronously."""
        result: int = _run(
            self._session.wait_for_selector(
                selector,
                root_node_id=root_node_id,
                timeout=timeout,
                poll_interval=poll_interval,
            ),
        )
        return result

    def wait_for_network_idle(
        self,
        idle_time: float = 0.5,
        timeout: float = 30.0,
    ) -> None:
        """Wait for network idle synchronously."""
        _run(self._session.wait_for_network_idle(idle_time=idle_time, timeout=timeout))

    def close(self) -> None:
        """Close the session synchronously."""
        _run(self._session.close())

    @property
    def page(self) -> Any:
        """Page domain (use ``run()`` to execute methods)."""
        return self._session.page

    @property
    def runtime(self) -> Any:
        """Runtime domain."""
        return self._session.runtime

    @property
    def network(self) -> Any:
        """Network domain."""
        return self._session.network

    @property
    def dom(self) -> Any:
        """DOM domain."""
        return self._session.dom

    @property
    def input(self) -> Any:
        """Input domain."""
        return self._session.input

    @property
    def emulation(self) -> Any:
        """Emulation domain."""
        return self._session.emulation

    @property
    def fetch(self) -> Any:
        """Fetch domain."""
        return self._session.fetch

    @property
    def target(self) -> Any:
        """Target domain."""
        return self._session.target

    @property
    def session_id(self) -> str:
        """The CDP session ID."""
        return self._session.session_id

    @property
    def target_id(self) -> str:
        """The CDP target ID."""
        return self._session.target_id

    def __enter__(self) -> SyncCDPSession:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()


class SyncCDPClient:
    """Synchronous wrapper around :class:`CDPClient`.

    Provides a sync API for launching a browser, creating pages,
    and executing CDP commands without async/await.

    Example::

        with SyncCDPClient.launch() as client:
            with client.new_page() as page:
                page.run(page.page.navigate("https://example.com"))
                page.run(page.wait_for_load_state("load"))
    """

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    @classmethod
    def launch(
        cls,
        headless: bool = True,
        browser_path: str | None = None,
        **kwargs: Any,
    ) -> SyncCDPClient:
        """Launch a browser and return a sync client.

        Args:
            headless: Whether to run in headless mode.
            browser_path: Optional path to browser executable.
            **kwargs: Additional arguments passed to ``CDPClient.launch()``.

        Returns:
            A :class:`SyncCDPClient` instance.
        """
        client = _run(CDPClient.launch(headless=headless, browser_path=browser_path, **kwargs))
        return cls(client)

    @classmethod
    def connect(
        cls,
        host: str = "localhost",
        port: int = 9222,
        **kwargs: Any,
    ) -> SyncCDPClient:
        """Connect to an existing browser and return a sync client.

        Args:
            host: Browser host.
            port: Browser debugging port.
            **kwargs: Additional arguments passed to ``CDPClient.connect()``.

        Returns:
            A :class:`SyncCDPClient` instance.
        """
        client = _run(CDPClient.connect(host=host, port=port, **kwargs))
        return cls(client)

    def new_page(self, url: str = "about:blank") -> SyncCDPSession:
        """Create a new page target.

        Args:
            url: Initial URL.

        Returns:
            A :class:`SyncCDPSession` for the new page.
        """
        session = _run(self._client.new_page(url=url))
        return SyncCDPSession(session)

    def connect_to_page(self, target_id: str) -> SyncCDPSession:
        """Attach to an existing page by target ID.

        Args:
            target_id: Target ID to attach to.

        Returns:
            A :class:`SyncCDPSession` for the target.
        """
        session = _run(self._client.connect_to_page(target_id))
        return SyncCDPSession(session)

    def get_pages(self) -> list[Any]:
        """List available page targets."""
        result: list[Any] = _run(self._client.get_pages())
        return result

    def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command at the browser level."""
        result: dict[str, Any] = _run(self._client.send(method, params))
        return result

    def close(self) -> None:
        """Close the client and browser."""
        _run(self._client.close())

    def __enter__(self) -> SyncCDPClient:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()
