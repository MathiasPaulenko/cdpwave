from __future__ import annotations

import contextlib
import logging
from typing import Any

from cdpwave.browser.discovery import TargetDiscovery, TargetInfo
from cdpwave.browser.launcher import BrowserLauncher
from cdpwave.domains.console import ConsoleDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.log import LogDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.page import PageDomain
from cdpwave.domains.runtime import RuntimeDomain
from cdpwave.domains.target import TargetDomain
from cdpwave.events.dispatcher import EventDispatcher
from cdpwave.events.handlers import EventHandler, Subscription
from cdpwave.exceptions import SessionClosedError
from cdpwave.session.manager import SessionManager
from cdpwave.transport.connection import Connection
from cdpwave.types import CommandSender

logger = logging.getLogger("cdpwave.client")


class CDPSession:
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

    @property
    def page(self) -> PageDomain:
        return self._page

    @property
    def runtime(self) -> RuntimeDomain:
        return self._runtime

    @property
    def target(self) -> TargetDomain:
        return self._target

    @property
    def network(self) -> NetworkDomain:
        return self._network

    @property
    def dom(self) -> DOMDomain:
        return self._dom

    @property
    def log(self) -> LogDomain:
        return self._log

    @property
    def console(self) -> ConsoleDomain:
        return self._console

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def target_id(self) -> str:
        return self._target_id

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def send(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._closed:
            raise SessionClosedError(
                f"Session {self._session_id} is closed"
            )
        return await self._sender(method, params)

    async def close(self) -> None:
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
        return self._dispatcher.on(event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        self._dispatcher.off(event_name, handler)

    async def __aenter__(self) -> CDPSession:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        await self.close()


class CDPClient:
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
        return self._dispatcher.on(event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        self._dispatcher.off(event_name, handler)

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
        if self._discovery is None:
            raise RuntimeError("Discovery is not available")
        targets = await self._discovery.list_targets()
        return [t for t in targets if t.type == "page"]

    async def connect_to_page(self, target_id: str) -> CDPSession:
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
        return self._closed or self._connection.is_closed

    @property
    def is_connected(self) -> bool:
        return not self._connection.is_closed

    async def __aenter__(self) -> CDPClient:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        await self.close()
