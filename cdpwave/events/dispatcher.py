import logging
from typing import Any

from cdpwave.events.handlers import EventHandler, Subscription

logger = logging.getLogger("cdpwave.events")


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def on(self, event_name: str, handler: EventHandler) -> Subscription:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        return Subscription(self, event_name, handler)

    def off(self, event_name: str, handler: EventHandler) -> None:
        handlers = self._handlers.get(event_name)
        if handlers is None:
            return
        if handler in handlers:
            handlers.remove(handler)
            if not handlers:
                del self._handlers[event_name]

    async def dispatch(self, event_name: str, params: dict[str, Any]) -> None:
        handlers = list(self._handlers.get(event_name, []))
        for handler in handlers:
            try:
                await handler(params)
            except Exception:
                logger.exception(
                    "Handler error for event %s",
                    event_name,
                )

    @property
    def handler_count(self) -> int:
        return sum(len(h) for h in self._handlers.values())

    def clear(self) -> None:
        self._handlers.clear()
