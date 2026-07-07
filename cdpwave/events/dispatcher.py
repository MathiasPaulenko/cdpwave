"""Event dispatcher for routing CDP events to registered handlers."""

import inspect
import logging
from typing import Any

from cdpwave.events.handlers import EventHandler, Subscription

logger = logging.getLogger("cdpwave.events")


class EventDispatcher:
    """Dispatches CDP events to registered async handlers.

    Each CDPSession and CDPClient owns an EventDispatcher. Handlers are
    isolated: if one raises, others still run.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

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

        Args:
            event_name: CDP event name.
            params: Event parameters dict from the CDP message.
        """
        handlers = list(self._handlers.get(event_name, []))
        for handler in handlers:
            try:
                result = handler(params)
                if inspect.isawaitable(result):
                    await result
            except Exception:
                logger.exception(
                    "Handler error for event %s",
                    event_name,
                )

    @property
    def handler_count(self) -> int:
        """Total number of registered handlers across all events."""
        return sum(len(h) for h in self._handlers.values())

    def clear(self) -> None:
        """Remove all registered handlers."""
        self._handlers.clear()
