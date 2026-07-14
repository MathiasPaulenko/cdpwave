"""Functional tests for the Browser domain (browser-level commands)."""

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestBrowser:
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

    async def test_grant_and_reset_permissions(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.grant_permissions(
                "https://example.com", ["geolocation"]
            )
            await client.browser.reset_permissions()

    async def test_set_download_behavior(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.set_download_behavior("deny")

    async def test_get_histograms(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_histograms()
            assert "histograms" in result

    @pytest.mark.skip(reason="V8.ExecuteJS histogram not available in CI Chrome")
    async def test_get_histogram(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.browser.get_histogram("V8.ExecuteJS")
            assert "histogram" in result

    async def test_set_permission(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            await client.browser.set_permission(
                {"name": "geolocation"}, "granted",
                origin="https://example.com",
            )
            await client.browser.reset_permissions()
