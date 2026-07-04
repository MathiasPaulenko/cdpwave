from __future__ import annotations

import weakref
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cdpwave.events.dispatcher import EventDispatcher

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]


class Subscription:
    def __init__(
        self,
        dispatcher: EventDispatcher,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        self._dispatcher_ref: weakref.ReferenceType[EventDispatcher] = (
            weakref.ref(dispatcher)
        )
        self._event_name = event_name
        self._handler = handler

    def unsubscribe(self) -> None:
        dispatcher = self._dispatcher_ref()
        if dispatcher is not None:
            dispatcher.off(self._event_name, self._handler)

    @property
    def event_name(self) -> str:
        return self._event_name

    @property
    def handler(self) -> EventHandler:
        return self._handler
