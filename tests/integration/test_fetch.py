import asyncio
import contextlib
from typing import Any

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
class TestFetch:
    async def test_enable_disable_fetch(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.fetch.enable(
                patterns=[{"urlPattern": "*", "requestStage": "Request"}],
            )
            await session.fetch.disable()

    async def test_intercept_and_continue_request(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            intercepted: list[dict[str, Any]] = []

            async def on_request_paused(params: dict[str, Any]) -> None:
                intercepted.append(params)
                request_id = params["requestId"]
                await session.fetch.continue_request(request_id)

            await session.fetch.enable(
                patterns=[{"urlPattern": "*", "requestStage": "Request"}],
            )
            session.on("Fetch.requestPaused", on_request_paused)

            navigate_task = asyncio.create_task(
                session.page.navigate("https://example.com")
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if intercepted:
                    break

            await navigate_task

            assert len(intercepted) > 0
            assert "requestId" in intercepted[0]
            assert "request" in intercepted[0]

            await session.fetch.disable()

    async def test_intercept_and_fulfill_request(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            fulfilled: list[str] = []

            async def on_request_paused(params: dict[str, Any]) -> None:
                request_id = params["requestId"]
                await session.fetch.fulfill_request(
                    request_id,
                    response_code=200,
                    response_headers=[
                        {"name": "Content-Type", "value": "text/html"},
                    ],
                    body="PGh0bWw+PGJvZHk+aGVsbG88L2JvZHk+PC9odG1sPg==",
                )
                fulfilled.append(request_id)

            await session.fetch.enable(
                patterns=[{"urlPattern": "*example.com*", "requestStage": "Request"}],
            )
            session.on("Fetch.requestPaused", on_request_paused)

            navigate_task = asyncio.create_task(
                session.page.navigate("https://example.com")
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if fulfilled:
                    break

            await navigate_task

            assert len(fulfilled) > 0

            result = await session.runtime.evaluate(
                "document.body.textContent", return_by_value=True,
            )
            assert result["result"]["value"] == "hello"

            await session.fetch.disable()

    async def test_intercept_and_fail_request(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            failed: list[str] = []

            async def on_request_paused(params: dict[str, Any]) -> None:
                request_id = params["requestId"]
                await session.fetch.fail_request(request_id, "Failed")
                failed.append(request_id)

            await session.fetch.enable(
                patterns=[{"urlPattern": "*example.com*", "requestStage": "Request"}],
            )
            session.on("Fetch.requestPaused", on_request_paused)

            navigate_task = asyncio.create_task(
                session.page.navigate("https://example.com")
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if failed:
                    break

            with contextlib.suppress(Exception):
                await navigate_task

            assert len(failed) > 0

            await session.fetch.disable()

    async def test_intercept_response_stage(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            response_intercepted: list[dict[str, Any]] = []

            async def on_request_paused(params: dict[str, Any]) -> None:
                response_intercepted.append(params)
                request_id = params["requestId"]
                await session.fetch.continue_response(request_id)

            await session.fetch.enable(
                patterns=[{"urlPattern": "*", "requestStage": "Response"}],
            )
            session.on("Fetch.requestPaused", on_request_paused)

            navigate_task = asyncio.create_task(
                session.page.navigate("https://example.com")
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if response_intercepted:
                    break

            await navigate_task

            assert len(response_intercepted) > 0
            assert "requestId" in response_intercepted[0]

            await session.fetch.disable()

    async def test_get_response_body(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            body_captured: list[dict[str, Any]] = []

            async def on_request_paused(params: dict[str, Any]) -> None:
                request_id = params["requestId"]
                body_result = await session.fetch.get_response_body(request_id)
                body_captured.append(body_result)
                await session.fetch.continue_response(request_id)

            await session.fetch.enable(
                patterns=[{"urlPattern": "*", "requestStage": "Response"}],
            )
            session.on("Fetch.requestPaused", on_request_paused)

            navigate_task = asyncio.create_task(
                session.page.navigate("https://example.com")
            )

            for _ in range(20):
                await asyncio.sleep(0.5)
                if body_captured:
                    break

            await navigate_task

            assert len(body_captured) > 0
            assert "body" in body_captured[0]

            await session.fetch.disable()
