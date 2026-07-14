"""E2E tests for the Browser domain (browser-level commands).

These tests launch a real browser and exercise Browser domain methods
end-to-end. Destructive commands (close, crash, crashGpuProcess) are
tested last or skipped to avoid interfering with other tests.
"""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.e2e
class TestBrowserE2E:
    async def test_get_version(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_version()
            assert "protocolVersion" in result
            assert "product" in result
            assert "userAgent" in result

    async def test_get_window_for_target(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await client.browser.get_window_for_target(
                target_id=session.target_id
            )
            assert "windowId" in result
            assert "bounds" in result

    async def test_get_and_set_window_bounds(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            window = await client.browser.get_window_for_target(
                target_id=session.target_id
            )
            window_id = window["windowId"]
            await client.browser.set_window_bounds(
                window_id, {"width": 1024, "height": 768}
            )
            result = await client.browser.get_window_bounds(window_id)
            assert "bounds" in result

    async def test_set_download_behavior(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.set_download_behavior("deny")

    async def test_set_download_behavior_with_events(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.set_download_behavior(
                "allow", download_path="/tmp", events_enabled=True
            )

    async def test_get_histograms(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_histograms()
            assert "histograms" in result

    async def test_get_histograms_with_query(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_histograms(query="V8")
            assert "histograms" in result

    @pytest.mark.skip(reason="V8.ExecuteJS histogram not available in CI Chrome")
    async def test_get_histogram(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_histogram("V8.ExecuteJS")
            assert "histogram" in result

    async def test_set_permission_and_reset(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            with contextlib.suppress(Exception):
                await client.browser.set_permission(
                    {"name": "geolocation"}, "granted",
                    origin="https://example.com",
                )
            await client.browser.reset_permissions()

    async def test_grant_permissions_deprecated(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.grant_permissions(
                "https://example.com", ["geolocation"]
            )
            await client.browser.reset_permissions()

    async def test_close(self) -> None:
        client = await CDPClient.launch(headless=True)
        await client.browser.close()
        assert client.is_closed
        await client.close()
