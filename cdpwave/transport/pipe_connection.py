"""Pipe-based transport for CDP communication via stdin/stdout.

Uses the ``--remote-debugging-pipe`` protocol: messages are framed with
a 4-byte little-endian uint32 length prefix followed by the JSON payload.
"""

import asyncio
import contextlib
import json
import logging
import struct
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

_HEADER_FORMAT = "<I"
_HEADER_SIZE = 4


class PipeConnection:
    """Pipe-based connection to a CDP endpoint via process stdin/stdout.

    Has the same public interface as :class:`Connection` so it can be
    used interchangeably by :class:`CDPClient`.

    Args:
        process: The browser subprocess with stdin/stdout pipes.
        event_callback: Async callback for CDP events.
        default_timeout: Default timeout for commands in seconds.
    """

    def __init__(
        self,
        process: asyncio.subprocess.Process,
        event_callback: EventCallback | None = None,
        default_timeout: float = 30.0,
        max_event_tasks: int = 100,
    ) -> None:
        self._process = process
        self._correlator = Correlator()
        self._receive_task: asyncio.Task[None] | None = None
        self._closed = False
        self._event_callback = event_callback
        self._default_timeout = default_timeout
        self._on_reconnect: ReconnectCallback | None = None
        self._event_semaphore = asyncio.Semaphore(max_event_tasks)

    async def connect(self) -> None:
        """Start the receive loop reading from the process stdout."""
        if self._process.stdout is None:
            raise ConnectionClosedError("Process stdout is not available")
        self._receive_task = asyncio.create_task(self._receive_loop())
        logger.info("Pipe connection established (pid=%d)", self._process.pid)

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
            timeout: Optional timeout in seconds.

        Returns:
            The CDP response result dict.

        Raises:
            ConnectionClosedError: If the pipe is not open.
            CommandTimeoutError: If the command does not respond in time.
            CommandError: If the CDP response contains an error.
        """
        if self._closed:
            raise ConnectionClosedError("Pipe connection is closed")

        stdin = self._process.stdin
        if stdin is None:
            raise ConnectionClosedError("Process stdin is not available")

        effective_timeout = self._default_timeout if timeout is None else timeout

        cmd_id = self._correlator.next_id()
        future = self._correlator.register(cmd_id)

        message = serialize_command(cmd_id, method, params, session_id)
        payload = message.encode("utf-8")
        header = struct.pack(_HEADER_FORMAT, len(payload))
        try:
            stdin.write(header + payload)
            await stdin.drain()
        except (ConnectionResetError, BrokenPipeError):
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
        """Close the pipe connection and cancel the receive loop."""
        if self._closed:
            return
        self._closed = True

        if self._receive_task is not None:
            self._receive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._receive_task

        self._correlator.reject_all(ConnectionClosedError("Pipe connection closed"))
        logger.info("Pipe connection closed")

    async def _receive_loop(self) -> None:
        """Background task that reads framed messages from stdout."""
        stdout = self._process.stdout
        assert stdout is not None
        try:
            while True:
                header = await stdout.readexactly(_HEADER_SIZE)
                (length,) = struct.unpack(_HEADER_FORMAT, header)
                raw = await stdout.readexactly(length)
                try:
                    data = deserialize_message(raw.decode("utf-8"))
                except (json.JSONDecodeError, TypeError, ValueError):
                    logger.warning("Received malformed pipe message, skipping")
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
        except asyncio.IncompleteReadError:
            logger.info("Pipe stdout closed (end of stream)")
        except asyncio.CancelledError:
            logger.debug("Pipe receive loop cancelled")
            raise
        finally:
            if not self._closed:
                self._correlator.reject_all(
                    ConnectionClosedError("Pipe closed unexpectedly"),
                )
                self._closed = True

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
