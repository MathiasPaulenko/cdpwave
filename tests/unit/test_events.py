import asyncio
from typing import Any

from cdpwave.events.dispatcher import EventDispatcher
from cdpwave.events.handlers import Subscription


class TestEventDispatcher:
    async def test_on_and_dispatch(self) -> None:
        dispatcher = EventDispatcher()
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        dispatcher.on("Page.loadEventFired", handler)
        await dispatcher.dispatch("Page.loadEventFired", {"timestamp": 123.45})
        assert received == [{"timestamp": 123.45}]

    async def test_multiple_handlers_all_called(self) -> None:
        dispatcher = EventDispatcher()
        calls: list[str] = []

        async def h1(params: dict[str, Any]) -> None:
            calls.append("h1")

        async def h2(params: dict[str, Any]) -> None:
            calls.append("h2")

        dispatcher.on("Page.frameNavigated", h1)
        dispatcher.on("Page.frameNavigated", h2)
        await dispatcher.dispatch("Page.frameNavigated", {"frame": {}})
        assert calls == ["h1", "h2"]

    async def test_handler_error_does_not_stop_others(self) -> None:
        dispatcher = EventDispatcher()
        calls: list[str] = []

        async def bad_handler(params: dict[str, Any]) -> None:
            calls.append("bad")
            raise ValueError("boom")

        async def good_handler(params: dict[str, Any]) -> None:
            calls.append("good")

        dispatcher.on("Runtime.consoleAPICalled", bad_handler)
        dispatcher.on("Runtime.consoleAPICalled", good_handler)
        await dispatcher.dispatch("Runtime.consoleAPICalled", {"type": "log"})
        assert calls == ["bad", "good"]

    async def test_handler_error_does_not_propagate(self) -> None:
        dispatcher = EventDispatcher()

        async def bad_handler(params: dict[str, Any]) -> None:
            raise ValueError("boom")

        dispatcher.on("Page.loadEventFired", bad_handler)
        await dispatcher.dispatch("Page.loadEventFired", {})
        assert dispatcher.handler_count == 1

    async def test_off_removes_handler(self) -> None:
        dispatcher = EventDispatcher()
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        dispatcher.on("Page.loadEventFired", handler)
        assert dispatcher.handler_count == 1
        dispatcher.off("Page.loadEventFired", handler)
        assert dispatcher.handler_count == 0
        await dispatcher.dispatch("Page.loadEventFired", {})
        assert received == []

    async def test_off_nonexistent_event_is_noop(self) -> None:
        dispatcher = EventDispatcher()

        async def handler(params: dict[str, Any]) -> None:
            pass

        dispatcher.off("Nonexistent", handler)

    async def test_off_nonexistent_handler_is_noop(self) -> None:
        dispatcher = EventDispatcher()

        async def handler(params: dict[str, Any]) -> None:
            pass

        async def other(params: dict[str, Any]) -> None:
            pass

        dispatcher.on("Event", handler)
        dispatcher.off("Event", other)
        assert dispatcher.handler_count == 1

    async def test_subscription_unsubscribe(self) -> None:
        dispatcher = EventDispatcher()
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        sub = dispatcher.on("Page.loadEventFired", handler)
        assert isinstance(sub, Subscription)
        sub.unsubscribe()
        assert dispatcher.handler_count == 0
        await dispatcher.dispatch("Page.loadEventFired", {})
        assert received == []

    async def test_unsubscribe_during_dispatch(self) -> None:
        dispatcher = EventDispatcher()
        calls: list[str] = []

        async def h1(params: dict[str, Any]) -> None:
            calls.append("h1")
            sub2.unsubscribe()

        async def h2(params: dict[str, Any]) -> None:
            calls.append("h2")

        dispatcher.on("Event", h1)
        sub2 = dispatcher.on("Event", h2)
        await dispatcher.dispatch("Event", {})
        assert calls == ["h1", "h2"]
        assert dispatcher.handler_count == 1

    async def test_clear_removes_all(self) -> None:
        dispatcher = EventDispatcher()

        async def h1(params: dict[str, Any]) -> None:
            pass

        async def h2(params: dict[str, Any]) -> None:
            pass

        dispatcher.on("Event1", h1)
        dispatcher.on("Event2", h2)
        assert dispatcher.handler_count == 2
        dispatcher.clear()
        assert dispatcher.handler_count == 0

    async def test_event_no_subscribers_is_noop(self) -> None:
        dispatcher = EventDispatcher()
        await dispatcher.dispatch("Nonexistent", {"data": 1})

    async def test_handler_count(self) -> None:
        dispatcher = EventDispatcher()

        async def h(params: dict[str, Any]) -> None:
            pass

        assert dispatcher.handler_count == 0
        dispatcher.on("A", h)
        assert dispatcher.handler_count == 1
        dispatcher.on("B", h)
        assert dispatcher.handler_count == 2
        dispatcher.off("A", h)
        assert dispatcher.handler_count == 1


class TestSubscription:
    async def test_subscription_properties(self) -> None:
        dispatcher = EventDispatcher()

        async def handler(params: dict[str, Any]) -> None:
            pass

        sub = dispatcher.on("MyEvent", handler)
        assert sub.event_name == "MyEvent"
        assert sub.handler is handler

    async def test_subscription_unsubscribe_after_clear(self) -> None:
        dispatcher = EventDispatcher()

        async def handler(params: dict[str, Any]) -> None:
            pass

        sub = dispatcher.on("Event", handler)
        dispatcher.clear()
        sub.unsubscribe()


class TestEventRouting:
    async def test_client_event_callback_browser_level(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        client.on("Target.targetCreated", handler)
        await client._event_callback("Target.targetCreated", {"targetInfo": {}}, None)
        assert received == [{"targetInfo": {}}]

    async def test_client_event_callback_session_level(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        session.on("Page.loadEventFired", handler)
        await client._event_callback("Page.loadEventFired", {"timestamp": 1.0}, "S-1")
        assert received == [{"timestamp": 1.0}]

    async def test_client_event_callback_unknown_session(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        await client._event_callback("Page.loadEventFired", {}, "UNKNOWN-SESSION")

    async def test_session_close_removes_dispatcher(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        assert "S-1" in client._session_dispatchers
        await session.close()
        assert "S-1" not in client._session_dispatchers

    async def test_client_on_off(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient

        conn = AsyncMock()
        conn.is_closed = False
        client = CDPClient(conn)
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        client.on("Target.targetCreated", handler)
        await client._event_callback("Target.targetCreated", {"data": 1}, None)
        assert received == [{"data": 1}]
        client.off("Target.targetCreated", handler)
        await client._event_callback("Target.targetCreated", {"data": 2}, None)
        assert received == [{"data": 1}]

    async def test_session_on_off(self) -> None:
        from unittest.mock import AsyncMock

        from cdpwave.client import CDPClient, CDPSession

        conn = AsyncMock()
        conn.send_command.return_value = {}
        conn.is_closed = False
        client = CDPClient(conn)
        session = CDPSession(conn, "S-1", "T-1", client=client)
        received: list[dict[str, Any]] = []

        async def handler(params: dict[str, Any]) -> None:
            received.append(params)

        session.on("Page.loadEventFired", handler)
        await client._event_callback("Page.loadEventFired", {"ts": 1}, "S-1")
        assert received == [{"ts": 1}]
        session.off("Page.loadEventFired", handler)
        await client._event_callback("Page.loadEventFired", {"ts": 2}, "S-1")
        assert received == [{"ts": 1}]


class TestConnectionEventCallback:
    async def test_event_callback_invoked(self) -> None:
        import json
        from unittest.mock import AsyncMock, patch

        from cdpwave.transport.connection import Connection

        callback = AsyncMock()
        conn = Connection("ws://localhost:9222", event_callback=callback)

        event_msg = json.dumps({
            "method": "Target.targetCreated",
            "params": {"targetInfo": {"targetId": "T-1"}},
        })

        class EventWS:
            def __init__(self) -> None:
                self._queue: asyncio.Queue[str] = asyncio.Queue()
                self._queue.put_nowait(event_msg)

            async def send(self, message: str) -> None:
                pass

            async def close(self) -> None:
                pass

            def __aiter__(self) -> "EventWS":
                return self

            async def __anext__(self) -> str:
                try:
                    return await asyncio.wait_for(self._queue.get(), timeout=0.5)
                except TimeoutError:
                    raise StopAsyncIteration from None

        mock_ws = EventWS()

        with patch(
            "cdpwave.transport.connection.websockets.connect",
            new_callable=AsyncMock,
        ) as mock_connect:
            mock_connect.return_value = mock_ws
            await conn.connect()

        await asyncio.sleep(0.1)
        await conn.close()
        callback.assert_awaited_once_with(
            "Target.targetCreated",
            {"targetInfo": {"targetId": "T-1"}},
            None,
        )

    async def test_no_event_callback_logs_debug(self) -> None:
        from unittest.mock import AsyncMock, patch

        from cdpwave.transport.connection import Connection

        conn = Connection("ws://localhost:9222")

        class EventWS:
            async def send(self, message: str) -> None:
                pass

            async def close(self) -> None:
                pass

            def __aiter__(self) -> "EventWS":
                return self

            async def __anext__(self) -> str:
                raise StopAsyncIteration

        mock_ws = EventWS()

        with patch(
            "cdpwave.transport.connection.websockets.connect",
            new_callable=AsyncMock,
        ) as mock_connect:
            mock_connect.return_value = mock_ws
            await conn.connect()

        await asyncio.sleep(0.05)
        await conn.close()
