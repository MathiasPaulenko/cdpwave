"""WebSocket connection for CDP communication."""

import asyncio
import contextlib
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import websockets
from websockets.asyncio.client import ClientConnection

from cdpwave.exceptions import (
    CommandError,
    CommandTimeoutError,
    ConnectionClosedError,
    ConnectionReconnectError,
)
from cdpwave.transport.correlation import Correlator
from cdpwave.transport.serializer import (
    deserialize_message,
    is_error,
    is_event,
    is_response,
    serialize_command,
)

logger = logging.getLogger("cdpwave.transport")

EventCallback = Callable[
    [str, dict[str, Any], str | None],
    Awaitable[None],
]
"""Async callback for CDP events: (method, params, session_id)."""

ReconnectCallback = Callable[[], Awaitable[None]]
"""Async callback invoked after a successful reconnection."""


def _log_task_exception(task: asyncio.Future[None]) -> None:
    """Log exceptions from completed event dispatch tasks."""
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logger.error("Unhandled exception in event dispatch task: %s", exc, exc_info=exc)


class Connection:
    """WebSocket connection to a CDP endpoint.

    Manages the WebSocket lifecycle, command correlation, and event
    dispatching. A single Connection serves all sessions (flatten mode).

    Args:
        url: WebSocket URL of the CDP endpoint.
        event_callback: Async callback for CDP events.
        default_timeout: Default timeout for commands in seconds.
        max_retries: Maximum reconnection attempts (0 = no reconnect).
        backoff_base: Initial backoff delay in seconds.
        backoff_max: Maximum backoff delay in seconds.
        on_reconnect: Async callback invoked after a successful reconnection.
    """

    def __init__(
        self,
        url: str,
        event_callback: EventCallback | None = None,
        default_timeout: float = 30.0,
        max_retries: int = 0,
        backoff_base: float = 1.0,
        backoff_max: float = 30.0,
        on_reconnect: ReconnectCallback | None = None,
        max_event_tasks: int = 100,
    ) -> None:
        self._url = url
        self._correlator = Correlator()
        self._ws: ClientConnection | None = None
        self._receive_task: asyncio.Task[None] | None = None
        self._closed = False
        self._event_callback = event_callback
        self._default_timeout = default_timeout
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_max = backoff_max
        self._reconnect_lock = asyncio.Lock()
        self._on_reconnect = on_reconnect
        self._event_semaphore = asyncio.Semaphore(max_event_tasks)

    async def connect(self) -> None:
        """Open the WebSocket connection and start the receive loop."""
        self._ws = await websockets.connect(
            self._url,
            max_size=None,
            ping_interval=20,
            ping_timeout=20,
        )
        self._receive_task = asyncio.create_task(self._receive_loop())
        logger.info("Connected to %s", self._url)

    async def _dispatch_event(
        self,
        method: str,
        params: dict[str, Any],
        session: str | None,
    ) -> None:
        """Dispatch an event with backpressure via semaphore."""
        async with self._event_semaphore:
            if self._event_callback is not None:
                await self._event_callback(method, params, session)

    async def send_command(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Send a CDP command and await its response.

        Args:
            method: CDP method name (e.g. ``"Page.navigate"``).
            params: Optional command parameters.
            session_id: Optional target session ID for flatten sessions.
            timeout: Optional timeout in seconds. Defaults to
                ``default_timeout`` set at construction.

        Returns:
            The CDP response result dict.

        Raises:
            ConnectionClosedError: If the connection is not open.
            CommandTimeoutError: If the command does not respond in time.
            CommandError: If the CDP response contains an error.
        """
        if self._closed:
            raise ConnectionClosedError("Connection is closed")

        ws = self._ws
        if ws is None:
            if self._max_retries > 0:
                async with self._reconnect_lock:
                    ws = self._ws
                    if ws is None or self._closed:
                        raise ConnectionClosedError("Connection is closed")
            else:
                raise ConnectionClosedError("Connection is closed")

        if ws is None or self._closed:
            raise ConnectionClosedError("Connection is closed")

        effective_timeout = self._default_timeout if timeout is None else timeout

        cmd_id = self._correlator.next_id()
        future = self._correlator.register(cmd_id)

        message = serialize_command(cmd_id, method, params, session_id)
        await ws.send(message)
        logger.debug("→ [%d] %s", cmd_id, method)

        if effective_timeout <= 0:
            return await future

        try:
            return await asyncio.wait_for(future, timeout=effective_timeout)
        except TimeoutError:
            self._correlator.reject(
                cmd_id,
                CommandError(-1, f"Command timeout: {method}"),
            )
            raise CommandTimeoutError(f"Command timeout: {method}") from None

    async def close(self) -> None:
        """Close the WebSocket connection and cancel the receive loop.

        All pending commands are rejected with ConnectionClosedError.
        """
        if self._closed:
            return
        self._closed = True

        if self._receive_task is not None:
            self._receive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._receive_task

        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                logger.warning("Error closing WebSocket", exc_info=True)

        self._correlator.reject_all(ConnectionClosedError("Connection closed"))
        logger.info("Connection closed")

    async def _reconnect(self) -> bool:
        """Attempt to reconnect with exponential backoff.

        Returns:
            True if reconnection succeeded, False if all retries exhausted.
        """
        if self._max_retries <= 0:
            return False

        async with self._reconnect_lock:
            for attempt in range(self._max_retries):
                delay = min(
                    self._backoff_base * (2 ** attempt),
                    self._backoff_max,
                )
                logger.info(
                    "Reconnect attempt %d/%d in %.1fs",
                    attempt + 1,
                    self._max_retries,
                    delay,
                )
                await asyncio.sleep(delay)
                try:
                    self._ws = await websockets.connect(
                        self._url,
                        max_size=None,
                        ping_interval=20,
                        ping_timeout=20,
                    )
                    self._closed = False
                    self._receive_task = asyncio.create_task(self._receive_loop())
                    logger.info("Reconnected to %s", self._url)
                    if self._on_reconnect is not None:
                        await self._on_reconnect()
                    return True
                except Exception as exc:
                    logger.warning(
                        "Reconnect attempt %d failed: %s",
                        attempt + 1,
                        exc,
                    )

            logger.error("All %d reconnection attempts exhausted", self._max_retries)
            return False

    @property
    def url(self) -> str:
        """The WebSocket URL this connection is connected to."""
        return self._url

    @property
    def is_closed(self) -> bool:
        """Whether the connection has been closed."""
        return self._closed

    async def _receive_loop(self) -> None:
        """Background task that reads WebSocket messages and dispatches them."""
        assert self._ws is not None
        try:
            async for raw in self._ws:
                try:
                    data = deserialize_message(str(raw))
                except (json.JSONDecodeError, TypeError, ValueError):
                    logger.warning("Received malformed WebSocket message, skipping")
                    continue

                if is_response(data):
                    cmd_id = data["id"]
                    if is_error(data):
                        error = data.get("error", {})
                        self._correlator.reject(
                            cmd_id,
                            CommandError(
                                code=int(error.get("code", -1)),
                                message=str(error.get("message", "Unknown error")),
                                data=error.get("data"),
                            ),
                        )
                        logger.debug("← [%d] error: %s", cmd_id, error.get("message"))
                    else:
                        result = data.get("result", {})
                        self._correlator.resolve(cmd_id, result)
                        logger.debug("← [%d] success", cmd_id)
                elif is_event(data):
                    method = data.get("method", "unknown")
                    params = data.get("params", {})
                    session = data.get("sessionId")
                    if self._event_callback is not None:
                        task = asyncio.ensure_future(
                            self._dispatch_event(method, params, session)
                        )
                        task.add_done_callback(_log_task_exception)
                    else:
                        logger.debug("← event: %s (session=%s)", method, session)
        except websockets.ConnectionClosedOK:
            logger.info("WebSocket closed normally")
        except websockets.ConnectionClosed:
            logger.info("WebSocket closed by remote")
        except asyncio.CancelledError:
            logger.debug("Receive loop cancelled")
            raise
        finally:
            if not self._closed:
                if self._max_retries > 0:
                    self._correlator.reject_all(
                        ConnectionReconnectError(
                            "Connection lost, pending commands rejected during reconnection",
                        ),
                    )
                    reconnected = await self._reconnect()
                    if not reconnected:
                        self._closed = True
                else:
                    self._correlator.reject_all(
                        ConnectionClosedError("WebSocket closed"),
                    )
                    self._closed = True
            else:
                self._correlator.reject_all(
                    ConnectionClosedError("WebSocket closed"),
                )
