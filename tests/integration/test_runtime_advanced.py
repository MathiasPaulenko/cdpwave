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
class TestRuntimeAdvanced:
    async def test_evaluate_with_await_promise(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "Promise.resolve(42)",
                await_promise=True,
                return_by_value=True,
            )
            assert result["result"]["value"] == 42

    async def test_evaluate_return_by_value_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "({a: 1, b: 2})",
                return_by_value=False,
            )
            assert "objectId" in result["result"]
            assert result["result"]["type"] == "object"

    async def test_call_function_on(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            obj = await session.runtime.evaluate(
                "({x: 10, y: 20})",
                return_by_value=False,
            )
            object_id = obj["result"]["objectId"]

            result = await session.runtime.call_function_on(
                object_id,
                "function() { return this.x + this.y; }",
                return_by_value=True,
            )
            assert result["result"]["value"] == 30

            await session.runtime.release_object(object_id)

    async def test_call_function_on_with_args(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "({})",
                return_by_value=False,
            )
            object_id = result["result"]["objectId"]

            call_result = await session.runtime.call_function_on(
                object_id,
                "function(a, b) { return a * b; }",
                args=[
                    {"value": 6},
                    {"value": 7},
                ],
                return_by_value=True,
            )
            assert call_result["result"]["value"] == 42

            await session.runtime.release_object(object_id)

    async def test_release_object(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "({test: true})",
                return_by_value=False,
            )
            object_id = result["result"]["objectId"]

            release_result = await session.runtime.release_object(object_id)
            assert release_result == {}

    async def test_release_object_group(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.evaluate(
                "var testGroup = {a: 1}; testGroup;",
                return_by_value=False,
            )

            result = await session.runtime.release_object_group("testGroup")
            assert result == {}

    async def test_get_properties(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            obj = await session.runtime.evaluate(
                "({foo: 'bar', num: 42})",
                return_by_value=False,
            )
            object_id = obj["result"]["objectId"]

            result = await session.runtime.get_properties(
                object_id,
                own_properties=True,
            )
            props = result.get("result", [])
            prop_names = [p.get("name") for p in props]
            assert "foo" in prop_names
            assert "num" in prop_names

            await session.runtime.release_object(object_id)

    async def test_compile_script(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "1 + 1", return_by_value=True,
            )
            assert result["result"]["value"] == 2

    async def test_evaluate_user_gesture(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "document.createElement('div') ? true : false",
                user_gesture=True,
                return_by_value=True,
            )
            assert result["result"]["value"] is True

    async def test_runtime_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            await session.runtime.disable()

    async def test_evaluate_null(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "null",
                return_by_value=True,
            )
            assert result["result"]["value"] is None

    async def test_evaluate_undefined(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.runtime.evaluate(
                "undefined",
                return_by_value=True,
            )
            assert result["result"]["type"] == "undefined"

    async def test_get_layout_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_layout_metrics()
            assert "contentSize" in result or "layoutViewport" in result

    async def test_get_navigation_history(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.page.get_navigation_history()
            assert "entries" in result
            assert "currentIndex" in result
            assert len(result["entries"]) >= 1
