"""CDPClient and CDPSession: the main public API for cdpwave."""

from __future__ import annotations

import contextlib
import logging
from typing import Any

from cdpwave.browser.discovery import TargetDiscovery, TargetInfo
from cdpwave.browser.launcher import BrowserLauncher
from cdpwave.domains.accessibility import AccessibilityDomain
from cdpwave.domains.animation import AnimationDomain
from cdpwave.domains.audits import AuditsDomain
from cdpwave.domains.console import ConsoleDomain
from cdpwave.domains.debugger import DebuggerDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.emulation import EmulationDomain
from cdpwave.domains.fetch import FetchDomain
from cdpwave.domains.input import InputDomain
from cdpwave.domains.io import IODomain
from cdpwave.domains.log import LogDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.overlay import OverlayDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.performance import PerformanceDomain
from cdpwave.domains.profiler import ProfilerDomain
from cdpwave.domains.runtime import RuntimeDomain
from cdpwave.domains.security import SecurityDomain
from cdpwave.domains.service_worker import ServiceWorkerDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.domains.system_info import SystemInfoDomain
from cdpwave.domains.target import TargetDomain
from cdpwave.domains.tracing import TracingDomain
from cdpwave.domains.web_authn import WebAuthnDomain
from cdpwave.events.dispatcher import EventDispatcher
from cdpwave.events.handlers import EventHandler, Subscription
from cdpwave.exceptions import SessionClosedError
from cdpwave.session.manager import SessionManager
from cdpwave.transport.connection import Connection
from cdpwave.types import CommandSender

logger = logging.getLogger("cdpwave.client")


class CDPSession:
    """Represents a single CDP target session.

    Provides access to CDP domain wrappers (page, runtime, network, etc.)
    and event handling for a single browser target. Use ``async with`` for
    automatic cleanup.
    """

    def __init__(
        self,
        connection: Connection,
        session_id: str,
        target_id: str,
        client: CDPClient | None = None,
    ) -> None:
        self._connection = connection
        self._session_id = session_id
        self._target_id = target_id
        self._closed = False
        self._dispatcher = EventDispatcher()

        if client is not None:
            client._session_dispatchers[session_id] = self._dispatcher
        self._client = client

        async def _send(
            method: str,
            params: dict[str, Any] | None = None,
        ) -> dict[str, Any]:
            return await connection.send_command(
                method,
                params,
                session_id=session_id,
            )

        self._sender: CommandSender = _send
        self._page = PageDomain(self._sender)
        self._runtime = RuntimeDomain(self._sender)
        self._target = TargetDomain(self._sender)
        self._network = NetworkDomain(self._sender)
        self._dom = DOMDomain(self._sender)
        self._log = LogDomain(self._sender)
        self._console = ConsoleDomain(self._sender)
        self._input = InputDomain(self._sender)
        self._emulation = EmulationDomain(self._sender)
        self._fetch = FetchDomain(self._sender)
        self._performance = PerformanceDomain(self._sender)
        self._profiler = ProfilerDomain(self._sender)
        self._debugger = DebuggerDomain(self._sender)
        self._overlay = OverlayDomain(self._sender)
        self._security = SecurityDomain(self._sender)
        self._audits = AuditsDomain(self._sender)
        self._accessibility = AccessibilityDomain(self._sender)
        self._storage = StorageDomain(self._sender)
        self._tracing = TracingDomain(self._sender)
        self._animation = AnimationDomain(self._sender)
        self._service_worker = ServiceWorkerDomain(self._sender)
        self._system_info = SystemInfoDomain(self._sender)
        self._web_authn = WebAuthnDomain(self._sender)
        self._io = IODomain(self._sender)

    @property
    def page(self) -> PageDomain:
        """Page domain wrapper for navigation, screenshots, and PDF."""
        return self._page

    @property
    def runtime(self) -> RuntimeDomain:
        """Runtime domain wrapper for JS evaluation and remote objects."""
        return self._runtime

    @property
    def target(self) -> TargetDomain:
        """Target domain wrapper for session management."""
        return self._target

    @property
    def network(self) -> NetworkDomain:
        """Network domain wrapper for monitoring, cookies, and cache."""
        return self._network

    @property
    def dom(self) -> DOMDomain:
        """DOM domain wrapper for document inspection and manipulation."""
        return self._dom

    @property
    def log(self) -> LogDomain:
        """Log domain wrapper for browser log entries."""
        return self._log

    @property
    def console(self) -> ConsoleDomain:
        """Console domain wrapper (deprecated, use Runtime events)."""
        return self._console

    @property
    def input(self) -> InputDomain:
        """Input domain wrapper for synthetic input events (mouse, keyboard, touch)."""
        return self._input

    @property
    def emulation(self) -> EmulationDomain:
        """Emulation domain wrapper for device metrics, sensors, and throttling."""
        return self._emulation

    @property
    def fetch(self) -> FetchDomain:
        """Fetch domain wrapper for request interception and modification."""
        return self._fetch

    @property
    def performance(self) -> PerformanceDomain:
        """Performance domain wrapper for runtime metrics and timeline."""
        return self._performance

    @property
    def profiler(self) -> ProfilerDomain:
        """Profiler domain wrapper for CPU profiling and code coverage."""
        return self._profiler

    @property
    def debugger(self) -> DebuggerDomain:
        """Debugger domain wrapper for breakpoints, stepping, and script inspection."""
        return self._debugger

    @property
    def overlay(self) -> OverlayDomain:
        """Overlay domain wrapper for visual highlighting and inspect mode."""
        return self._overlay

    @property
    def security(self) -> SecurityDomain:
        """Security domain wrapper for certificate error handling."""
        return self._security

    @property
    def audits(self) -> AuditsDomain:
        """Audits domain wrapper for Lighthouse-style audits and contrast checks."""
        return self._audits

    @property
    def accessibility(self) -> AccessibilityDomain:
        """Accessibility domain wrapper for AX tree inspection."""
        return self._accessibility

    @property
    def storage(self) -> StorageDomain:
        """Storage domain wrapper for cookies, IndexedDB, and cache storage."""
        return self._storage

    @property
    def tracing(self) -> TracingDomain:
        """Tracing domain wrapper for performance tracing and timeline recording."""
        return self._tracing

    @property
    def animation(self) -> AnimationDomain:
        """Animation domain wrapper for CSS/Web animation inspection and control."""
        return self._animation

    @property
    def service_worker(self) -> ServiceWorkerDomain:
        """ServiceWorker domain wrapper for service worker inspection and control."""
        return self._service_worker

    @property
    def system_info(self) -> SystemInfoDomain:
        """SystemInfo domain wrapper for system and GPU information."""
        return self._system_info

    @property
    def web_authn(self) -> WebAuthnDomain:
        """WebAuthn domain wrapper for virtual authenticator management."""
        return self._web_authn

    @property
    def io(self) -> IODomain:
        """IO domain wrapper for reading stream handles."""
        return self._io

    @property
    def session_id(self) -> str:
        """The CDP session ID for this target."""
        return self._session_id

    @property
    def target_id(self) -> str:
        """The CDP target ID for this session."""
        return self._target_id

    @property
    def is_closed(self) -> bool:
        """Whether this session has been closed."""
        return self._closed

    async def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command as an escape hatch.

        Args:
            method: CDP method name (e.g. ``"Page.navigate"``).
            params: Optional command parameters.

        Returns:
            The CDP response result dict.

        Raises:
            SessionClosedError: If the session is closed.
        """
        if self._closed:
            raise SessionClosedError(
                f"Session {self._session_id} is closed"
            )
        return await self._sender(method, params)

    async def close(self) -> None:
        """Close the session and detach from the target."""
        if self._closed:
            return
        self._closed = True
        self._dispatcher.clear()
        if self._client is not None:
            self._client._session_dispatchers.pop(self._session_id, None)
        with contextlib.suppress(Exception):
            await self._connection.send_command(
                "Target.detachFromTarget",
                {"sessionId": self._session_id},
            )
        logger.info("Session %s closed", self._session_id)

    def on(self, event_name: str, handler: EventHandler) -> Subscription:
        """Register an async handler for a CDP event.

        Args:
            event_name: CDP event name (e.g. ``"Page.loadEventFired"``).
            handler: Async callable that receives the event params dict.

        Returns:
            A Subscription that can be used to unsubscribe.
        """
        return self._dispatcher.on(event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        """Remove a previously registered event handler.

        Args:
            event_name: CDP event name.
            handler: The handler to remove.
        """
        self._dispatcher.off(event_name, handler)

    async def __aenter__(self) -> CDPSession:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        """Exit async context manager and close the session."""
        await self.close()


class CDPClient:
    """Main entry point for cdpwave.

    Manages a browser process (via ``launch()``) or connects to an existing
    browser (via ``connect()``). Provides session creation, event handling,
    and lifecycle management. Use ``async with`` for automatic cleanup.
    """

    def __init__(
        self,
        connection: Connection,
        launcher: BrowserLauncher | None = None,
        discovery: TargetDiscovery | None = None,
    ) -> None:
        self._connection = connection
        self._launcher = launcher
        self._discovery = discovery
        self._session_manager = SessionManager(connection)
        self._dispatcher = EventDispatcher()
        self._session_dispatchers: dict[str, EventDispatcher] = {}
        self._sessions: dict[str, CDPSession] = {}
        self._closed = False

    async def _event_callback(
        self,
        event_name: str,
        params: dict[str, Any],
        session_id: str | None,
    ) -> None:
        """Internal callback for routing CDP events to the correct dispatcher."""
        if event_name == "Target.detachedFromTarget":
            detached_session_id = params.get("sessionId")
            if detached_session_id is not None:
                session = self._sessions.get(detached_session_id)
                if session is not None:
                    session._closed = True
                    session._dispatcher.clear()
                    self._session_dispatchers.pop(detached_session_id, None)
                    self._sessions.pop(detached_session_id, None)
                    logger.info(
                        "Session %s detached by browser",
                        detached_session_id,
                    )
                else:
                    logger.warning(
                        "Target.detachedFromTarget for unknown session %s",
                        detached_session_id,
                    )
            return

        if session_id is None:
            await self._dispatcher.dispatch(event_name, params)
        else:
            dispatcher = self._session_dispatchers.get(session_id)
            if dispatcher is not None:
                await dispatcher.dispatch(event_name, params)
            else:
                logger.warning(
                    "Event %s for unknown session %s",
                    event_name,
                    session_id,
                )

    def on(self, event_name: str, handler: EventHandler) -> Subscription:
        """Register an async handler for a browser-level CDP event.

        Args:
            event_name: CDP event name.
            handler: Async callable that receives the event params dict.

        Returns:
            A Subscription that can be used to unsubscribe.
        """
        return self._dispatcher.on(event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        """Remove a previously registered browser-level event handler.

        Args:
            event_name: CDP event name.
            handler: The handler to remove.
        """
        self._dispatcher.off(event_name, handler)

    async def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a raw CDP command to the browser target (no session).

        Use this for browser-level commands like ``SystemInfo.getInfo``
        that are only supported on the browser target, not page sessions.

        Args:
            method: CDP method name (e.g. ``"SystemInfo.getInfo"``).
            params: Optional command parameters.

        Returns:
            The CDP response result dict.
        """
        return await self._connection.send_command(method, params)

    @classmethod
    async def launch(
        cls,
        headless: bool = True,
        browser_path: str | None = None,
        port: int = 0,
        user_data_dir: str | None = None,
        extra_args: list[str] | None = None,
        timeout: float = 10.0,
    ) -> CDPClient:
        """Launch a new browser and return a connected CDPClient.

        Args:
            headless: Run browser in headless mode.
            browser_path: Optional path to browser executable.
            port: Optional debugging port (0 for auto-assigned).
            user_data_dir: Optional user data directory.
            extra_args: Optional extra command-line arguments.
            timeout: Maximum seconds to wait for browser startup.

        Returns:
            A connected CDPClient instance.
        """
        launcher = BrowserLauncher(
            browser_path=browser_path,
            port=port,
            headless=headless,
            user_data_dir=user_data_dir,
            extra_args=extra_args,
        )
        info = await launcher.launch(timeout=timeout)
        discovery = TargetDiscovery(port=info.port)
        client = cls.__new__(cls)
        client._connection = Connection(
            info.web_socket_debugger_url,
            event_callback=client._event_callback,
        )
        await client._connection.connect()
        client._launcher = launcher
        client._discovery = discovery
        client._session_manager = SessionManager(client._connection)
        client._dispatcher = EventDispatcher()
        client._session_dispatchers = {}
        client._sessions = {}
        client._closed = False
        return client

    @classmethod
    async def connect(
        cls,
        host: str = "localhost",
        port: int = 9222,
    ) -> CDPClient:
        """Connect to an existing browser's CDP endpoint.

        Args:
            host: Host where the browser is running.
            port: Remote debugging port.

        Returns:
            A connected CDPClient instance.
        """
        discovery = TargetDiscovery(host=host, port=port)
        version = await discovery.get_version()
        client = cls.__new__(cls)
        client._connection = Connection(
            version.web_socket_debugger_url,
            event_callback=client._event_callback,
        )
        await client._connection.connect()
        client._launcher = None
        client._discovery = discovery
        client._session_manager = SessionManager(client._connection)
        client._dispatcher = EventDispatcher()
        client._session_dispatchers = {}
        client._sessions = {}
        client._closed = False
        return client

    async def new_page(self, url: str = "about:blank") -> CDPSession:
        """Create a new page target and return a CDPSession for it.

        Args:
            url: Initial URL for the new page.

        Returns:
            A CDPSession connected to the new page.
        """
        target_id = await self._session_manager.create_target(url)
        session_id = await self._session_manager.attach_to_target(target_id)
        session = CDPSession(
            connection=self._connection,
            session_id=session_id,
            target_id=target_id,
            client=self,
        )
        self._sessions[session_id] = session
        return session

    async def get_pages(self) -> list[TargetInfo]:
        """List all open page targets in the browser."""
        if self._discovery is None:
            raise RuntimeError("Discovery is not available")
        targets = await self._discovery.list_targets()
        return [t for t in targets if t.type == "page"]

    async def connect_to_page(self, target_id: str) -> CDPSession:
        """Attach to an existing page target by ID.

        Args:
            target_id: The target ID to attach to.

        Returns:
            A CDPSession connected to the specified target.
        """
        session_id = await self._session_manager.attach_to_target(target_id)
        session = CDPSession(
            connection=self._connection,
            session_id=session_id,
            target_id=target_id,
            client=self,
        )
        self._sessions[session_id] = session
        return session

    async def close(self) -> None:
        """Close all sessions, the WebSocket connection, and the browser process."""
        if self._closed:
            return
        self._closed = True

        for session in list(self._sessions.values()):
            with contextlib.suppress(Exception):
                session._closed = True
                session._dispatcher.clear()
            self._session_dispatchers.pop(session._session_id, None)
        self._sessions.clear()
        self._dispatcher.clear()

        with contextlib.suppress(Exception):
            await self._connection.close()

        if self._launcher is not None:
            with contextlib.suppress(Exception):
                await self._launcher.close()

        logger.info("CDPClient closed")

    @property
    def is_closed(self) -> bool:
        """Whether the client has been closed or the connection dropped."""
        return self._closed or self._connection.is_closed

    @property
    def is_connected(self) -> bool:
        """Whether the WebSocket connection is still open."""
        return not self._connection.is_closed

    async def __aenter__(self) -> CDPClient:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        """Exit async context manager and close the client."""
        await self.close()
