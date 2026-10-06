"""Pipe-based transport for CDP communication via process file descriptors.

Implements Chrome's ``--remote-debugging-pipe`` protocol: each JSON
message is terminated by a NUL byte (``\\0``). Chrome reads commands
from fd 3 and writes responses/events to fd 4. This transport is only
supported on POSIX systems.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
from typing import Any

from cdpwave.exceptions import (
    CommandError,
    CommandTimeoutError,
    ConnectionClosedError,
)
from cdpwave.transport.connection import EventCallback, ReconnectCallback
from cdpwave.transport.correlation import Correlator
from cdpwave.transport.serializer import (
    deserialize_message,
    is_error,
    is_event,
    is_response,
    serialize_command,
)

logger = logging.getLogger("cdpwave.transport.pipe")

_MESSAGE_DELIMITER = b"\x00"


class _ReadProtocol(asyncio.Protocol):
    """Forwards raw pipe bytes to the owning connection."""

    def __init__(self, connection: PipeConnection) -> None:
        self._connection = connection

    def data_received(self, data: bytes) -> None:
        self._connection._on_data(data)

    def connection_lost(self, exc: Exception | None) -> None:
        self._connection._on_connection_lost()


class PipeConnection:
    """Pipe-based connection to a CDP endpoint via process file descriptors.

    Has the same public interface as :class:`Connection` so it can be
    used interchangeably by :class:`CDPClient`.

    Args:
        read_fd: File descriptor for reading messages from the browser
            (the parent-side read end of the fd-4 pipe).
        write_fd: File descriptor for writing messages to the browser
            (the parent-side write end of the fd-3 pipe).
        process: Optional browser ``Popen`` used for liveness logging.
        event_callback: Async callback for CDP events.
        default_timeout: Default timeout for commands in seconds.
    """

    def __init__(
        self,
        read_fd: int,
        write_fd: int,
        process: Any = None,
        event_callback: EventCallback | None = None,
        default_timeout: float = 30.0,
        max_event_tasks: int = 100,
    ) -> None:
        self._read_fd = read_fd
        self._write_fd = write_fd
        self._process = process
        self._correlator = Correlator()
        self._receive_task: asyncio.Task[None] | None = None
        self._closed = False
        self._event_callback = event_callback
        self._default_timeout = default_timeout
        self._on_reconnect: ReconnectCallback | None = None
        self._event_semaphore = asyncio.Semaphore(max_event_tasks)
        self._read_transport: asyncio.ReadTransport | None = None
        self._write_transport: asyncio.WriteTransport | None = None
        self._read_file: Any = None
        self._write_file: Any = None
        self._buffer = bytearray()

    async def connect(self) -> None:
        """Attach the pipe file descriptors to the event loop."""
        if os.name != "posix":
            raise ConnectionClosedError(
                "Pipe connections are only supported on POSIX systems"
            )
        loop = asyncio.get_running_loop()
        self._read_file = os.fdopen(self._read_fd, "rb", buffering=0)
        self._write_file = os.fdopen(self._write_fd, "wb", buffering=0)
        transport, _ = await loop.connect_read_pipe(
            lambda: _ReadProtocol(self),
            self._read_file,
        )
        self._read_transport = transport
        write_transport, _ = await loop.connect_write_pipe(
            asyncio.Protocol,
            self._write_file,
        )
        self._write_transport = write_transport
        pid = self._process.pid if self._process is not None else -1
        logger.info("Pipe connection established (pid=%d)", pid)

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

    def _on_data(self, data: bytes) -> None:
        """Handle raw bytes from the browser pipe (fd 4)."""
        self._buffer.extend(data)
        while True:
            idx = self._buffer.find(_MESSAGE_DELIMITER)
            if idx < 0:
                break
            raw = bytes(self._buffer[:idx])
            del self._buffer[: idx + 1]
            self._handle_message(raw)

    def _handle_message(self, raw: bytes) -> None:
        """Parse and route a single NUL-delimited JSON message."""
        try:
            data = deserialize_message(raw.decode("utf-8"))
        except (json.JSONDecodeError, TypeError, ValueError, UnicodeDecodeError):
            logger.warning("Received malformed pipe message, skipping")
            return

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

    def _on_connection_lost(self) -> None:
        """Handle the browser closing its write pipe (fd 4)."""
        if not self._closed:
            self._closed = True
            self._correlator.reject_all(
                ConnectionClosedError("Pipe closed unexpectedly"),
            )
            logger.info("Pipe read end closed by browser")

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
            timeout: Optional timeout in seconds.

        Returns:
            The CDP response result dict.

        Raises:
            ConnectionClosedError: If the pipe is not open.
            CommandTimeoutError: If the command does not respond in time.
            CommandError: If the CDP response contains an error.
        """
        if self._closed or self._write_transport is None:
            raise ConnectionClosedError("Pipe connection is closed")

        effective_timeout = self._default_timeout if timeout is None else timeout

        cmd_id = self._correlator.next_id()
        future = self._correlator.register(cmd_id)

        message = serialize_command(cmd_id, method, params, session_id)
        payload = message.encode("utf-8") + _MESSAGE_DELIMITER
        try:
            self._write_transport.write(payload)
        except (ConnectionResetError, BrokenPipeError, RuntimeError):
            self._correlator.reject(
                cmd_id,
                ConnectionClosedError("Pipe connection is closed"),
            )
            raise ConnectionClosedError("Pipe connection is closed") from None
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
        """Close the pipe transports and reject pending commands."""
        if self._closed:
            return
        self._closed = True

        if self._receive_task is not None:
            self._receive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._receive_task

        if self._read_transport is not None:
            self._read_transport.close()
            self._read_transport = None
        if self._write_transport is not None:
            self._write_transport.close()
            self._write_transport = None

        self._correlator.reject_all(ConnectionClosedError("Pipe connection closed"))
        logger.info("Pipe connection closed")

    @property
    def url(self) -> str:
        """Identifier for this connection (always ``pipe://``)."""
        return "pipe://"

    @property
    def is_closed(self) -> bool:
        """Whether the connection has been closed."""
        return self._closed


def _log_task_exception(task: asyncio.Future[None]) -> None:
    """Log exceptions from completed event dispatch tasks."""
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logger.error("Unhandled exception in event dispatch task: %s", exc, exc_info=exc)
