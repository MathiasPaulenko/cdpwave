import asyncio

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestInput:
    async def test_insert_text_into_input_field(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                const input = document.createElement('input');
                input.id = 'test-input';
                input.type = 'text';
                document.body.appendChild(input);
                input.focus();
                """
            )

            await session.input.insert_text("hello world")

            result = await session.runtime.evaluate(
                "document.getElementById('test-input').value",
                return_by_value=True,
            )
            assert result["result"]["value"] == "hello world"

    async def test_dispatch_key_event_types_letter(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                const input = document.createElement('input');
                input.id = 'key-input';
                input.type = 'text';
                document.body.appendChild(input);
                input.focus();
                """
            )

            await session.input.dispatch_key_event(
                "keyDown", key="a", code="KeyA",
                windows_virtual_key_code=65, native_virtual_key_code=65,
                text="a",
            )
            await session.input.dispatch_key_event(
                "keyUp", key="a", code="KeyA",
                windows_virtual_key_code=65, native_virtual_key_code=65,
            )

            result = await session.runtime.evaluate(
                "document.getElementById('key-input').value",
                return_by_value=True,
            )
            assert result["result"]["value"] == "a"

    async def test_dispatch_mouse_event_move(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.dispatch_mouse_event(
                "mouseMoved", 50.0, 50.0,
            )
            assert result == {}

    async def test_dispatch_mouse_event_click(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                window._clickCount = 0;
                document.addEventListener('click', () => {
                    window._clickCount++;
                });
                """
            )

            await session.input.dispatch_mouse_event(
                "mousePressed", 10.0, 10.0,
                button="left", click_count=1,
            )
            await session.input.dispatch_mouse_event(
                "mouseReleased", 10.0, 10.0,
                button="left", click_count=1,
            )

            await asyncio.sleep(0.5)
            result = await session.runtime.evaluate(
                "window._clickCount", return_by_value=True,
            )
            assert result["result"]["value"] == 1

    async def test_dispatch_touch_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.dispatch_touch_event(
                "touchStart",
                [{"x": 50.0, "y": 50.0, "id": 1}],
            )
            assert result == {}

    async def test_dispatch_drag_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.dispatch_drag_event(
                "dragEnter", 10.0, 20.0,
                data={"items": [], "dragOperationsMask": 1, "files": []},
            )
            assert result == {}

    async def test_synthesize_tap_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.synthesize_tap_gesture(50.0, 50.0)
            assert result == {}

    async def test_synthesize_scroll_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.synthesize_scroll_gesture(
                50.0, 50.0, y_distance=200.0,
            )
            assert result == {}

    async def test_synthesize_pinch_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.synthesize_pinch_gesture(
                100.0, 100.0, 1.5,
            )
            assert result == {}

    async def test_cancel_dragging(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            result = await session.input.cancel_dragging()
            assert result == {}

    async def test_set_intercept_drags(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.input.set_intercept_drags(True)
            await session.input.set_intercept_drags(False)

    async def test_ime_set_composition(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                const input = document.createElement('input');
                input.id = 'ime-input';
                document.body.appendChild(input);
                input.focus();
                """
            )

            result = await session.input.ime_set_composition("text", 0, 4)
            assert result == {}
