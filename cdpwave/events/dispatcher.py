"""Event dispatcher for routing CDP events to registered handlers."""

import inspect
import logging
from typing import Any

from cdpwave.events.handlers import EventHandler, Subscription
from cdpwave.types import EventErrorCallback

logger = logging.getLogger("cdpwave.events")


class EventDispatcher:
    """Dispatches CDP events to registered async handlers.

    Each CDPSession and CDPClient owns an EventDispatcher. Handlers are
    isolated: if one raises, others still run.

    Args:
        strict_events: If True, handler exceptions are re-raised after
            logging, stopping dispatch to remaining handlers. Default False
            (fire-and-forget).
        on_event_error: Optional callback invoked when a handler raises.
            Receives (event_name, params, exception). May be sync or async.
    """

    def __init__(
        self,
        strict_events: bool = False,
        on_event_error: EventErrorCallback | None = None,
    ) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._strict = strict_events
        self._on_event_error = on_event_error

    def on(self, event_name: str, handler: EventHandler) -> Subscription:
        """Register an async handler for a CDP event.

        Args:
            event_name: CDP event name (e.g. ``"Page.loadEventFired"``).
            handler: Async callable that receives the event params dict.

        Returns:
            A Subscription that can be used to unsubscribe.
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        return Subscription(self, event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        """Remove a previously registered handler.

        Args:
            event_name: CDP event name.
            handler: The handler to remove.
        """
        handlers = self._handlers.get(event_name)
        if handlers is None:
            return
        if handler in handlers:
            handlers.remove(handler)
            if not handlers:
                del self._handlers[event_name]

    async def dispatch(self, event_name: str, params: dict[str, Any]) -> None:
        """Dispatch an event to all registered handlers.

        Handler exceptions are caught and logged; other handlers still run.
        In strict mode, the first handler exception is re-raised after
        logging and the error callback runs.

        Args:
            event_name: CDP event name.
            params: Event parameters dict from the CDP message.

        Raises:
            Exception: If ``strict_events`` is True and a handler raises.
        """
        handlers = list(self._handlers.get(event_name, []))
        first_exc: BaseException | None = None
        for handler in handlers:
            try:
                result = handler(params)
                if inspect.isawaitable(result):
                    await result
            except Exception as exc:
                logger.exception(
                    "Handler error for event %s",
                    event_name,
                )
                if self._on_event_error is not None:
                    cb_result = self._on_event_error(event_name, params, exc)
                    if inspect.isawaitable(cb_result):
                        await cb_result
                if self._strict and first_exc is None:
                    first_exc = exc
        if first_exc is not None:
            raise first_exc

    @property
    def handler_count(self) -> int:
        """Total number of registered handlers across all events."""
        return sum(len(h) for h in self._handlers.values())

    def clear(self) -> None:
        """Remove all registered handlers."""
        self._handlers.clear()
