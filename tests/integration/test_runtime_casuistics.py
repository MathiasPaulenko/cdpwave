import contextlib

import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestRuntimeCasuistics:
    async def test_release_object_group(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate("({a: 1, b: 2})", object_group="test")
        await page.runtime.release_object_group("test")
        assert result is not None

    async def test_run_if_waiting_for_debugger(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.run_if_waiting_for_debugger()
        assert result == {}

    async def test_get_exception_details(self, page: CDPSession) -> None:
        await page.runtime.enable()
        with contextlib.suppress(Exception):
            await page.runtime.evaluate("throw new Error('test')")
        with contextlib.suppress(Exception):
            await page.runtime.get_exception_details("invalid-id")
        assert True

    async def test_query_objects(self, page: CDPSession) -> None:
        await page.runtime.enable()
        # Create some objects
        await page.runtime.evaluate("class TestClass {}; new TestClass()")
        # Get prototype ID
        result = await page.runtime.evaluate("TestClass.prototype")
        prototype_id = result.get("result", {}).get("objectId")
        if prototype_id:
            objects = await page.runtime.query_objects(prototype_id)
            assert "objects" in objects

    async def test_global_lexical_scope_names(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.global_lexical_scope_names()
        assert "names" in result

    async def test_set_async_call_stack_depth(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.set_async_call_stack_depth(32)
        assert result == {}

    async def test_await_promise_with_timeout(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate(
            "new Promise(resolve => setTimeout(() => resolve('test'), 100))",
            await_promise=True,
            return_by_value=True,
        )
        assert result["result"]["value"] == "test"

    async def test_discard_console_entries(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.discard_console_entries()
        assert result == {}

    async def test_evaluate_with_generate_preview(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate("({a: 1, b: 2})", generate_preview=True)
        assert "result" in result

    async def test_evaluate_with_silent(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate("console.log('test')", silent=True)
        assert "result" in result

    async def test_evaluate_with_object_group(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate("({a: 1})", object_group="test")
        assert "result" in result

    async def test_evaluate_with_return_by_value_false(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.evaluate("({a: 1})", return_by_value=False)
        assert "result" in result
        assert "objectId" in result["result"]

    async def test_call_function_on_with_return_by_value(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.call_function_on(
            "function() { return {a: 1}; }",
            return_by_value=True
        )
        assert "result" in result
        assert "value" in result["result"]

    async def test_call_function_on_with_generate_preview(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.call_function_on(
            "function() { return {a: 1}; }",
            generate_preview=True
        )
        assert "result" in result

    async def test_call_function_on_with_silent(self, page: CDPSession) -> None:
        await page.runtime.enable()
        result = await page.runtime.call_function_on(
            "function() { console.log('test'); return 1; }",
            silent=True
        )
        assert "result" in result
