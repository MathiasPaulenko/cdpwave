from __future__ import annotations

import weakref
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cdpwave.events.dispatcher import EventDispatcher

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]
"""Async callable that receives CDP event params."""


class Subscription:
    """Handle returned by ``on()`` for unsubscribing a handler.

    Holds a weak reference to the dispatcher so that unsubscribing after
    the dispatcher is garbage-collected is a no-op.
    """

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
        """Remove the handler from the dispatcher."""
        dispatcher = self._dispatcher_ref()
        if dispatcher is not None:
            dispatcher.off(self._event_name, self._handler)

    @property
    def event_name(self) -> str:
        """The CDP event name this subscription is for."""
        return self._event_name

    @property
    def handler(self) -> EventHandler:
        """The handler callable attached to this subscription."""
        return self._handler
