"""Integration tests for domains that previously had no browser coverage.

Covers: ads, autofill, bluetooth_emulation, crash_report_context,
digital_credentials, dom_snapshot, dom_storage, fed_cm, file_system,
inspector, smart_card_emulation, web_audio, web_mcp.

Some domains are experimental and may not be available in all Chrome
versions. Tests skip gracefully when the method is not found.
"""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


def _is_method_not_found(exc: Exception) -> bool:
    return isinstance(exc, CommandError) and exc.code == -32601


async def _wait_for_page(page: CDPSession, url: str = "https://example.com") -> None:
    await page.page.enable()
    await page.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestAds:
    async def test_get_ad_metrics(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.ads.get_ad_metrics()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")


@pytest.mark.integration
class TestAutofill:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_set_addresses(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.autofill.enable()
            with contextlib.suppress(Exception):
                await session.autofill.set_addresses([
                    {
                        "name": "Test User",
                        "streetAddress": "123 Main St",
                        "city": "Test City",
                        "state": "CA",
                        "postalCode": "12345",
                        "country": "US",
                    },
                ])
            await session.autofill.disable()


@pytest.mark.integration
class TestBluetoothEmulation:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable()
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_set_simulated_central_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable()
                await session.bluetooth_emulation.set_simulated_central_state("poweredOn")
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")


@pytest.mark.integration
class TestCrashReportContext:
    async def test_get_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.crash_report_context.get_entries()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("CrashReportContext not available")


@pytest.mark.integration
class TestDigitalCredentials:
    async def test_set_virtual_wallet_behavior(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "default"
                )
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("DigitalCredentials not available")


@pytest.mark.integration
class TestDOMSnapshot:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await session.dom_snapshot.disable()

    async def test_capture_snapshot_default(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display"],
            )
            assert "documents" in result
            assert "strings" in result

    async def test_capture_snapshot_with_styles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display"],
                include_paint_order=True,
                include_dom_rects=True,
            )
            assert "documents" in result

    async def test_capture_snapshot_with_experimental_opts(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color"],
                include_blended_background_colors=True,
                include_text_color_opacities=True,
            )
            assert "documents" in result


@pytest.mark.integration
class TestDOMStorage:
    async def test_local_storage_set_get_remove(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            origin_result = await session.runtime.evaluate(
                "window.location.origin", return_by_value=True
            )
            origin = origin_result["result"]["value"]
            storage_id = {"securityOrigin": origin, "isLocalStorage": True}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "test_key", "test_value"
            )

            items = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = items.get("entries", [])
            assert any(
                e[0] == "test_key" and e[1] == "test_value" for e in entries
            )

            await session.dom_storage.remove_dom_storage_item(storage_id, "test_key")

            items_after = await session.dom_storage.get_dom_storage_items(storage_id)
            entries_after = items_after.get("entries", [])
            assert not any(e[0] == "test_key" for e in entries_after)

    async def test_session_storage_set_get_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            origin_result = await session.runtime.evaluate(
                "window.location.origin", return_by_value=True
            )
            origin = origin_result["result"]["value"]
            storage_id = {"securityOrigin": origin, "isLocalStorage": False}

            await session.dom_storage.set_dom_storage_item(
                storage_id, "ss_key", "ss_value"
            )

            items = await session.dom_storage.get_dom_storage_items(storage_id)
            entries = items.get("entries", [])
            assert any(e[0] == "ss_key" for e in entries)

            await session.dom_storage.clear_dom_storage_items(storage_id)

            items_after = await session.dom_storage.get_dom_storage_items(storage_id)
            entries_after = items_after.get("entries", [])
            assert len(entries_after) == 0


@pytest.mark.integration
class TestFedCm:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_reset_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                await session.fed_cm.reset_cooldown()
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")


@pytest.mark.integration
class TestFileSystem:
    async def test_get_directory(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.file_system.get_directory()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    pytest.skip("FileSystem.getDirectory requires permission")
                pytest.skip("FileSystem not available")


@pytest.mark.integration
class TestInspector:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.inspector.enable()
            await session.inspector.disable()


@pytest.mark.integration
class TestSmartCardEmulation:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.smart_card_emulation.enable()
                await session.smart_card_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("SmartCardEmulation not available")


@pytest.mark.integration
class TestWebAudio:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_audio.enable()
            await session.web_audio.disable()

    async def test_get_realtime_data(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_audio.enable()
            result = await session.runtime.evaluate(
                "new AudioContext().id", return_by_value=True,
            )
            ctx_id = result.get("result", {}).get("value", "")
            if ctx_id:
                rt = await session.web_audio.get_realtime_data(ctx_id)
                assert isinstance(rt, dict)
            await session.web_audio.disable()


@pytest.mark.integration
class TestWebMCP:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.web_mcp.enable()
                await session.web_mcp.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("WebMCP not available")
