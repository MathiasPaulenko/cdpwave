"""Synchronous wrappers for cdpwave's async API.

Provides ``SyncCDPClient`` and ``SyncCDPSession`` that run all async
operations on a single persistent event loop in a dedicated background
thread. This keeps the WebSocket connection, receive task, and pending
futures bound to one loop for the whole client lifetime.

Notes:
- All sync calls block the calling thread until the coroutine finishes
  on the background loop.
- Sync calls are also safe from inside a running event loop (the work
  still runs on the client's dedicated loop).
- Event handlers registered via ``on()`` must be ``async def`` — they
  run on the background loop.
- Do not call sync methods from inside event handlers (they run on the
  loop thread and would deadlock); use the async objects instead.
"""

from __future__ import annotations

import asyncio
import inspect
import threading
from typing import Any

from cdpwave.client import CDPClient, CDPSession


class _SyncRunner:
    """Runs coroutines on a dedicated event loop in a background thread.

    One runner = one loop = one thread. All coroutines for a client and
    its sessions must share the same loop because the WebSocket and its
    receive task are bound to the loop where they were created.
    """

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._closed = False
        self._thread = threading.Thread(
            target=self._thread_main,
            name="cdpwave-sync-loop",
            daemon=True,
        )
        self._thread.start()

    def _thread_main(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
        pending = asyncio.all_tasks(self._loop)
        for task in pending:
            task.cancel()
        if pending:
            self._loop.run_until_complete(
                asyncio.gather(*pending, return_exceptions=True)
            )
        self._loop.close()

    def run(self, awaitable: Any) -> Any:
        """Run an awaitable synchronously, blocking until it completes."""
        if threading.get_ident() == self._thread.ident:
            if inspect.iscoroutine(awaitable):
                awaitable.close()
            raise RuntimeError(
                "Cannot call the sync API from the cdpwave event loop "
                "thread. Use the async API inside event handlers."
            )
        if self._closed:
            if inspect.iscoroutine(awaitable):
                awaitable.close()
            raise RuntimeError("Sync runner is closed")

        async def _wrap() -> Any:
            return await awaitable

        future = asyncio.run_coroutine_threadsafe(_wrap(), self._loop)
        return future.result()

    def shutdown(self) -> None:
        """Stop the event loop and join the thread."""
        if self._closed:
            return
        self._closed = True
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)


class _SyncDomainWrapper:
    """Sync wrapper around an async CDP domain.

    Wraps all async methods of a domain (e.g. ``PageDomain``,
    ``RuntimeDomain``) so they execute on the shared runner's event
    loop.
    """

    def __init__(self, domain: Any, runner: _SyncRunner) -> None:
        self._domain = domain
        self._runner = runner
        self._sync_cache: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name in self._sync_cache:
            return self._sync_cache[name]
        attr = getattr(self._domain, name)
        if inspect.iscoroutinefunction(attr):

            def _sync_method(*args: Any, **kwargs: Any) -> Any:
                return self._runner.run(attr(*args, **kwargs))

            self._sync_cache[name] = _sync_method
            return _sync_method
        return attr


def _wrap(value: Any, runner: _SyncRunner) -> Any:
    """Wrap domains and coroutine functions for sync execution."""
    if hasattr(value, "_send"):
        return _SyncDomainWrapper(value, runner)
    if inspect.iscoroutinefunction(value):

        def _sync_method(*args: Any, **kwargs: Any) -> Any:
            return runner.run(value(*args, **kwargs))

        return _sync_method
    return value


class SyncCDPSession:
    """Synchronous wrapper around :class:`CDPSession`.

    Domain access (``page``, ``runtime``, ``network``, ...) returns
    sync wrappers — methods can be called directly. Use :meth:`run`
    for arbitrary coroutines.
    """

    def __init__(self, session: CDPSession, runner: _SyncRunner | None = None) -> None:
        self._session = session
        self._owns_runner = runner is None
        self._runner = runner or _SyncRunner()

    def run(self, coro: Any) -> Any:
        """Run an async coroutine synchronously.

        Args:
            coro: An awaitable (e.g. ``session.wait_for_event(...)``).

        Returns:
            The coroutine's result.
        """
        return self._runner.run(coro)

    def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command synchronously."""
        result: dict[str, Any] = self._runner.run(self._session.send(method, params))
        return result

    def wait_for_event(
        self,
        event_name: str,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Wait for a single CDP event synchronously."""
        result: dict[str, Any] = self._runner.run(
            self._session.wait_for_event(event_name, timeout=timeout)
        )
        return result

    def wait_for_navigation(
        self,
        url: str | None = None,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Wait for navigation synchronously."""
        result: dict[str, Any] = self._runner.run(
            self._session.wait_for_navigation(url=url, timeout=timeout),
        )
        return result

    def wait_for_load_state(
        self,
        state: str = "load",
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Wait for a load state synchronously."""
        result: dict[str, Any] = self._runner.run(
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
        result: int = self._runner.run(
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
        self._runner.run(self._session.wait_for_network_idle(idle_time=idle_time, timeout=timeout))

    def close(self) -> None:
        """Close the session synchronously."""
        try:
            self._runner.run(self._session.close())
        finally:
            if self._owns_runner:
                self._runner.shutdown()

    def on(self, event_name: str, handler: Any) -> Any:
        """Register an async event handler.

        The handler must be ``async def`` — it runs on the client's
        background event loop.
        """
        return self._session.on(event_name, handler)

    def off(self, event_name: str, handler: Any) -> None:
        """Remove a previously registered event handler."""
        self._session.off(event_name, handler)

    @property
    def session_id(self) -> str:
        """The CDP session ID."""
        return self._session.session_id

    @property
    def target_id(self) -> str:
        """The CDP target ID."""
        return self._session.target_id

    @property
    def is_closed(self) -> bool:
        """Whether the session has been closed."""
        return self._session.is_closed

    @property
    def sub_sessions(self) -> list[SyncCDPSession]:
        """Sub-sessions for auto-attached iframes and workers."""
        return [
            SyncCDPSession(s, self._runner) for s in self._session.sub_sessions
        ]

    def __enter__(self) -> SyncCDPSession:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying session.

        Domain objects are wrapped so their methods run synchronously;
        coroutine methods are wrapped likewise. Everything else is
        returned as-is.
        """
        return _wrap(getattr(self._session, name), self._runner)


class SyncCDPClient:
    """Synchronous wrapper around :class:`CDPClient`.

    Provides a sync API for launching a browser, creating pages,
    and executing CDP commands without async/await.

    Example::

        with SyncCDPClient.launch() as client:
            with client.new_page() as page:
                page.page.navigate("https://example.com")
                page.wait_for_load_state("load")
    """

    def __init__(self, client: CDPClient) -> None:
        self._client = client
        self._runner = _SyncRunner()

    @classmethod
    def launch(
        cls,
        headless: bool = True,
        browser_path: str | None = None,
        port: int = 0,
        user_data_dir: str | None = None,
        **kwargs: Any,
    ) -> SyncCDPClient:
        """Launch a browser and return a sync client.

        Args:
            headless: Whether to run in headless mode.
            browser_path: Optional path to browser executable.
            port: Optional debugging port (0 for auto-assigned).
            user_data_dir: Optional user data directory.
            **kwargs: Additional arguments passed to ``CDPClient.launch()``.

        Returns:
            A :class:`SyncCDPClient` instance.
        """
        client = cls.__new__(cls)
        runner = _SyncRunner()
        try:
            client._runner = runner
            client._client = runner.run(
                CDPClient.launch(
                    headless=headless,
                    browser_path=browser_path,
                    port=port,
                    user_data_dir=user_data_dir,
                    **kwargs,
                )
            )
        except Exception:
            runner.shutdown()
            raise
        return client

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
        client = cls.__new__(cls)
        runner = _SyncRunner()
        try:
            client._runner = runner
            client._client = runner.run(
                CDPClient.connect(host=host, port=port, **kwargs)
            )
        except Exception:
            runner.shutdown()
            raise
        return client

    def run(self, coro: Any) -> Any:
        """Run an async coroutine synchronously."""
        return self._runner.run(coro)

    def new_page(self, url: str = "about:blank") -> SyncCDPSession:
        """Create a new page target.

        Args:
            url: Initial URL.

        Returns:
            A :class:`SyncCDPSession` for the new page.
        """
        session = self._runner.run(self._client.new_page(url=url))
        return SyncCDPSession(session, self._runner)

    def connect_to_page(self, target_id: str) -> SyncCDPSession:
        """Attach to an existing page by target ID.

        Args:
            target_id: Target ID to attach to.

        Returns:
            A :class:`SyncCDPSession` for the target.
        """
        session = self._runner.run(self._client.connect_to_page(target_id))
        return SyncCDPSession(session, self._runner)

    def get_pages(self) -> list[Any]:
        """List available page targets."""
        result: list[Any] = self._runner.run(self._client.get_pages())
        return result

    def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command at the browser level."""
        result: dict[str, Any] = self._runner.run(self._client.send(method, params))
        return result

    def on(self, event_name: str, handler: Any) -> Any:
        """Register an async handler for a browser-level CDP event.

        The handler must be ``async def`` — it runs on the client's
        background event loop.
        """
        return self._client.on(event_name, handler)

    def off(self, event_name: str, handler: Any) -> None:
        """Remove a previously registered browser-level event handler."""
        self._client.off(event_name, handler)

    @property
    def is_closed(self) -> bool:
        """Whether the client has been closed or the connection dropped."""
        return self._client.is_closed

    @property
    def sessions(self) -> list[SyncCDPSession]:
        """List of currently active sessions."""
        return [SyncCDPSession(s, self._runner) for s in self._client.sessions]

    def close(self) -> None:
        """Close the client and browser."""
        try:
            self._runner.run(self._client.close())
        finally:
            self._runner.shutdown()

    def __enter__(self) -> SyncCDPClient:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying client.

        ``client.browser`` and ``client.system_info`` are returned as
        sync domain wrappers; coroutine methods are wrapped likewise.
        """
        return _wrap(getattr(self._client, name), self._runner)
