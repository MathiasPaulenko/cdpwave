"""E2E tests for the Input domain.

These tests exercise the full CDP pipeline: launch a real browser,
navigate to a page, and verify that synthetic input events produce
the expected side effects in the DOM.
"""

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
class TestInputE2E:
    async def test_type_text_into_input_field(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                const input = document.createElement('input');
                input.id = 'e2e-input';
                input.type = 'text';
                document.body.appendChild(input);
                input.focus();
                """
            )

            await session.input.type_text("hello")

            result = await session.runtime.evaluate(
                "document.getElementById('e2e-input').value",
                return_by_value=True,
            )
            assert result["result"]["value"] == "hello"

    async def test_click_button_and_verify_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                window._clicked = false;
                const btn = document.createElement('button');
                btn.id = 'e2e-btn';
                btn.textContent = 'Click me';
                btn.style.position = 'absolute';
                btn.style.left = '10px';
                btn.style.top = '10px';
                btn.style.width = '100px';
                btn.style.height = '30px';
                btn.addEventListener('click', () => {
                    window._clicked = true;
                });
                document.body.appendChild(btn);
                """
            )

            await session.input.dispatch_mouse_event(
                "mousePressed", 15.0, 15.0,
                button="left", click_count=1,
            )
            await session.input.dispatch_mouse_event(
                "mouseReleased", 15.0, 15.0,
                button="left", click_count=1,
            )

            await asyncio.sleep(0.5)
            result = await session.runtime.evaluate(
                "window._clicked", return_by_value=True,
            )
            assert result["result"]["value"] is True

    async def test_scroll_page_with_wheel_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                document.body.style.height = '5000px';
                window._scrollY = 0;
                window.addEventListener('scroll', () => {
                    window._scrollY = window.scrollY;
                });
                """
            )

            await session.input.dispatch_mouse_event(
                "mouseWheel", 50.0, 50.0,
                delta_x=0.0, delta_y=300.0,
            )

            await asyncio.sleep(0.5)
            result = await session.runtime.evaluate(
                "window._scrollY", return_by_value=True,
            )
            assert result["result"]["value"] > 0

    async def test_key_event_modifiers(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                window._keyEvents = [];
                document.addEventListener('keydown', (e) => {
                    window._keyEvents.push({
                        key: e.key,
                        ctrlKey: e.ctrlKey,
                        shiftKey: e.shiftKey,
                    });
                });
                """
            )

            await session.input.dispatch_key_event(
                "keyDown", key="a", code="KeyA",
                modifiers=2,
                windows_virtual_key_code=65,
                native_virtual_key_code=65,
            )
            await session.input.dispatch_key_event(
                "keyUp", key="a", code="KeyA",
                modifiers=2,
                windows_virtual_key_code=65,
                native_virtual_key_code=65,
            )

            await asyncio.sleep(0.3)
            result = await session.runtime.evaluate(
                "JSON.stringify(window._keyEvents)",
                return_by_value=True,
            )
            import json
            events = json.loads(result["result"]["value"])
            assert len(events) >= 1
            assert events[0]["key"] == "a"
            assert events[0]["ctrlKey"] is True

    async def test_insert_text_into_textarea(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                const ta = document.createElement('textarea');
                ta.id = 'e2e-textarea';
                document.body.appendChild(ta);
                ta.focus();
                """
            )

            await session.input.insert_text("Hello, World!")

            result = await session.runtime.evaluate(
                "document.getElementById('e2e-textarea').value",
                return_by_value=True,
            )
            assert result["result"]["value"] == "Hello, World!"

    async def test_synthesize_tap_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                window._touchEnded = false;
                document.addEventListener('touchend', () => {
                    window._touchEnded = true;
                });
                """
            )

            await session.input.synthesize_tap_gesture(
                70.0, 65.0, duration=200, tap_count=1,
            )

            await asyncio.sleep(0.5)
            result = await session.runtime.evaluate(
                "window._touchEnded", return_by_value=True,
            )
            assert result["result"]["value"] is True

    async def test_set_ignore_input_events(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.input.set_ignore_input_events(True)
            await session.input.set_ignore_input_events(False)

    async def test_drag_and_drop_flow(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.runtime.evaluate(
                """
                window._dragEnterCount = 0;
                window._dragOverCount = 0;
                window._dropCount = 0;
                const target = document.createElement('div');
                target.id = 'e2e-drop-zone';
                target.style.width = '200px';
                target.style.height = '200px';
                target.style.position = 'absolute';
                target.style.left = '10px';
                target.style.top = '10px';
                target.style.backgroundColor = 'lightblue';
                target.addEventListener('dragenter', (e) => {
                    e.preventDefault();
                    window._dragEnterCount++;
                });
                target.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    window._dragOverCount++;
                });
                target.addEventListener('drop', (e) => {
                    e.preventDefault();
                    window._dropCount++;
                });
                document.body.appendChild(target);
                """
            )

            data = {
                "items": [{"mimeType": "text/plain", "data": "hello"}],
                "dragOperationsMask": 1,
                "files": [],
            }

            await session.input.dispatch_drag_event(
                "dragEnter", 50.0, 50.0, data=data,
            )
            await session.input.dispatch_drag_event(
                "dragOver", 50.0, 50.0, data=data,
            )
            await session.input.dispatch_drag_event(
                "drop", 50.0, 50.0, data=data,
            )

            await asyncio.sleep(0.3)
            result = await session.runtime.evaluate(
                "JSON.stringify({"
                "enter: window._dragEnterCount, "
                "over: window._dragOverCount, "
                "drop: window._dropCount})",
                return_by_value=True,
            )
            import json
            counts = json.loads(result["result"]["value"])
            assert counts["enter"] >= 1
            assert counts["drop"] >= 1
