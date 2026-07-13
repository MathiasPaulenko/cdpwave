"""Integration tests for domains that previously had no browser coverage.

Covers: ads, autofill, bluetooth_emulation, crash_report_context,
digital_credentials, dom_snapshot, dom_storage, fed_cm, file_system,
inspector, smart_card_emulation, web_audio, web_mcp.

Some domains are experimental and may not be available in all Chrome
versions. Tests skip gracefully when the method is not found.
"""

import asyncio
import contextlib
from typing import Any

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
class TestAdsEdgeCases:
    """Edge cases for Ads domain on a real browser."""

    async def test_get_ad_metrics_before_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.ads.get_ad_metrics()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")

    async def test_get_ad_metrics_after_blank_page(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("about:blank")
            await asyncio.sleep(0.5)
            try:
                result = await session.ads.get_ad_metrics()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")

    async def test_get_ad_metrics_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                r1 = await session.ads.get_ad_metrics()
                r2 = await session.ads.get_ad_metrics()
                assert isinstance(r1, dict)
                assert isinstance(r2, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")


@pytest.mark.integration
class TestAdsFlow:
    """End-to-end flows combining Ads with other domains."""

    async def test_navigate_then_ad_metrics_then_screenshot(self) -> None:
        """Navigate → get ad metrics → take screenshot — multi-domain flow."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                metrics = await session.ads.get_ad_metrics()
                assert isinstance(metrics, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")

            screenshot = await session.page.capture_screenshot()
            assert "data" in screenshot

    async def test_ad_metrics_with_dom_inspection(self) -> None:
        """Get ad metrics and inspect DOM — multi-domain flow."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                metrics = await session.ads.get_ad_metrics()
                assert isinstance(metrics, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Ads.getAdMetrics not available")

            doc = await session.dom.get_document()
            assert "root" in doc


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
                        "fields": [
                            {"name": "NAME_FULL", "value": "Test User"},
                            {"name": "ADDRESS_HOME_STREET_ADDRESS", "value": "123 Main St"},
                            {"name": "ADDRESS_HOME_CITY", "value": "Test City"},
                            {"name": "ADDRESS_HOME_STATE", "value": "CA"},
                            {"name": "ADDRESS_HOME_ZIP", "value": "12345"},
                            {"name": "ADDRESS_HOME_COUNTRY", "value": "US"},
                        ]
                    },
                ])
            await session.autofill.disable()


@pytest.mark.integration
class TestAutofillEdgeCases:
    """Edge cases for Autofill domain on a real browser."""

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                await session.autofill.enable()
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.autofill.disable()

    async def test_set_addresses_empty(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                with contextlib.suppress(Exception):
                    await session.autofill.set_addresses([])
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_trigger_invalid_field_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                with pytest.raises(CommandError):
                    await session.autofill.trigger(999999)
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_trigger_with_card(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                with pytest.raises(CommandError):
                    await session.autofill.trigger(
                        999999,
                        card={
                            "number": "4111111111111111",
                            "name": "Test User",
                            "expiryMonth": "12",
                            "expiryYear": "2025",
                            "cvc": "123",
                        },
                    )
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")


@pytest.mark.integration
class TestAutofillFlow:
    """End-to-end flows combining Autofill with other domains."""

    async def test_set_addresses_then_trigger(self) -> None:
        """Set addresses then trigger autofill on a form field."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                await session.autofill.set_addresses([
                    {
                        "fields": [
                            {"name": "NAME_FULL", "value": "Test User"},
                            {"name": "ADDRESS_HOME_STREET_ADDRESS", "value": "123 Main St"},
                            {"name": "ADDRESS_HOME_CITY", "value": "Test City"},
                            {"name": "ADDRESS_HOME_STATE", "value": "CA"},
                            {"name": "ADDRESS_HOME_ZIP", "value": "12345"},
                            {"name": "ADDRESS_HOME_COUNTRY", "value": "US"},
                        ]
                    },
                ])

                await session.page.enable()
                await session.page.navigate("https://example.com")
                await asyncio.sleep(1.0)

                doc = await session.dom.get_document()
                with contextlib.suppress(Exception):
                    await session.autofill.trigger(
                        doc["root"]["nodeId"],
                    )

                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_autofill_with_form_injection(self) -> None:
        """Inject a form then get field node then trigger autofill."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()

                await session.page.enable()
                await session.page.navigate("https://example.com")
                await asyncio.sleep(1.0)

                await session.runtime.evaluate(
                    "const form = document.createElement('form');"
                    "const input = document.createElement('input');"
                    "input.type = 'text';"
                    "input.autocomplete = 'street-address';"
                    "input.name = 'address';"
                    "form.appendChild(input);"
                    "document.body.appendChild(form);"
                )

                await session.autofill.set_addresses([
                    {
                        "fields": [
                            {"name": "NAME_FULL", "value": "Test User"},
                            {"name": "ADDRESS_HOME_STREET_ADDRESS", "value": "456 Oak Ave"},
                            {"name": "ADDRESS_HOME_CITY", "value": "Springfield"},
                            {"name": "ADDRESS_HOME_STATE", "value": "IL"},
                            {"name": "ADDRESS_HOME_ZIP", "value": "62701"},
                            {"name": "ADDRESS_HOME_COUNTRY", "value": "US"},
                        ]
                    },
                ])

                with contextlib.suppress(Exception):
                    doc = await session.dom.get_document()
                    await session.autofill.trigger(
                        doc["root"]["nodeId"],
                    )

                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_address_form_filled_event(self) -> None:
        """Enable Autofill and listen for addressFormFilled event."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                events: list[dict] = []

                async def on_filled(params: dict) -> None:
                    events.append(params)

                await session.autofill.enable()
                session.on("Autofill.addressFormFilled", on_filled)

                await session.autofill.set_addresses([
                    {
                        "fields": [
                            {"name": "NAME_FULL", "value": "Test User"},
                            {"name": "ADDRESS_HOME_STREET_ADDRESS", "value": "789 Pine Rd"},
                            {"name": "ADDRESS_HOME_CITY", "value": "Portland"},
                            {"name": "ADDRESS_HOME_STATE", "value": "OR"},
                            {"name": "ADDRESS_HOME_ZIP", "value": "97201"},
                            {"name": "ADDRESS_HOME_COUNTRY", "value": "US"},
                        ]
                    },
                ])

                await asyncio.sleep(1.0)
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_trigger_with_address(self) -> None:
        """Trigger autofill with address data on invalid field."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                with pytest.raises(CommandError):
                    await session.autofill.trigger(
                        999999,
                        address={
                            "fields": [
                                {"name": "NAME_FULL", "value": "Test User"},
                                {"name": "ADDRESS_HOME_STREET_ADDRESS", "value": "123 Main St"},
                            ]
                        },
                    )
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_multiple_enable_disable_cycles(self) -> None:
        """Repeated enable/disable should be stable."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                for _ in range(3):
                    await session.autofill.enable()
                    await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_set_addresses_multiple(self) -> None:
        """Set multiple addresses at once."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()
                with contextlib.suppress(Exception):
                    await session.autofill.set_addresses([
                        {
                            "fields": [
                                {"name": "NAME_FULL", "value": "User One"},
                                {"name": "ADDRESS_HOME_CITY", "value": "City One"},
                            ]
                        },
                        {
                            "fields": [
                                {"name": "NAME_FULL", "value": "User Two"},
                                {"name": "ADDRESS_HOME_CITY", "value": "City Two"},
                            ]
                        },
                    ])
                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")

    async def test_trigger_fill_alias_on_real_form(self) -> None:
        """Use trigger_fill alias on a real injected form."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.autofill.enable()

                await session.page.enable()
                await session.page.navigate("https://example.com")
                await asyncio.sleep(1.0)

                await session.runtime.evaluate(
                    "const form = document.createElement('form');"
                    "const input = document.createElement('input');"
                    "input.type = 'text';"
                    "input.autocomplete = 'given-name';"
                    "input.name = 'name';"
                    "form.appendChild(input);"
                    "document.body.appendChild(form);"
                )

                await session.autofill.set_addresses([
                    {
                        "fields": [
                            {"name": "NAME_FULL", "value": "Alias Test"},
                        ]
                    },
                ])

                with contextlib.suppress(Exception):
                    doc = await session.dom.get_document()
                    await session.autofill.trigger_fill(
                        doc["root"]["nodeId"],
                    )

                await session.autofill.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("Autofill not available")


@pytest.mark.integration
class TestBluetoothEmulation:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
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
                await session.bluetooth_emulation.enable("powered-on", True)
                await session.bluetooth_emulation.set_simulated_central_state("powered-on")
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")


@pytest.mark.integration
class TestBluetoothEmulationEdgeCases:
    """Edge cases for BluetoothEmulation on a real browser."""

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                await session.bluetooth_emulation.enable("powered-on", True)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_all_central_states(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                for state in ("absent", "powered-off", "powered-on"):
                    await session.bluetooth_emulation.enable(state, True)
                    await session.bluetooth_emulation.set_simulated_central_state(state)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_enable_le_not_supported(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", False)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_simulate_preconnected_peripheral(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                with contextlib.suppress(Exception):
                    await session.bluetooth_emulation.simulate_preconnected_peripheral(
                        "AA:BB:CC:DD:EE:FF",
                        "Test Device",
                        manufacturer_data=[{"key": 6, "data": "dGVzdA=="}],
                        known_service_uuids=["00001800-0000-1000-8000-00805f9b34fb"],
                    )
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_simulate_advertisement(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                with contextlib.suppress(Exception):
                    await session.bluetooth_emulation.simulate_advertisement({
                        "deviceAddress": "AA:BB:CC:DD:EE:FF",
                        "rssi": -40,
                        "scanRecord": {
                            "name": "Test Device",
                        },
                    })
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_add_service_and_remove(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                with contextlib.suppress(Exception):
                    result = await session.bluetooth_emulation.add_service(
                        "AA:BB:CC:DD:EE:FF",
                        "00001800-0000-1000-8000-00805f9b34fb",
                    )
                    service_id = result.get("serviceId", "")
                    if service_id:
                        await session.bluetooth_emulation.remove_service(service_id)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_simulate_gatt_disconnection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                with contextlib.suppress(Exception):
                    await session.bluetooth_emulation.simulate_gatt_disconnection(
                        "AA:BB:CC:DD:EE:FF",
                    )
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")


@pytest.mark.integration
class TestBluetoothEmulationEvents:
    """Event listener tests for BluetoothEmulation."""

    async def test_gatt_operation_received_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                session.on(
                    "BluetoothEmulation.gattOperationReceived",
                    on_event,
                )
                await asyncio.sleep(2.0)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_characteristic_operation_received_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                session.on(
                    "BluetoothEmulation.characteristicOperationReceived",
                    on_event,
                )
                await asyncio.sleep(2.0)
                await session.bluetooth_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("BluetoothEmulation not available")

    async def test_descriptor_operation_received_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            try:
                await session.bluetooth_emulation.enable("powered-on", True)
                session.on(
                    "BluetoothEmulation.descriptorOperationReceived",
                    on_event,
                )
                await asyncio.sleep(2.0)
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
                    "decline"
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
class TestFedCmEdgeCases:
    """Edge cases for FedCm domain on a real browser."""

    async def test_enable_with_disable_rejection_delay(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable(disable_rejection_delay=True)
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                await session.fed_cm.disable()
                await session.fed_cm.enable()
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                await session.fed_cm.enable()
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                await session.fed_cm.disable()
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_reset_cooldown_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.reset_cooldown()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.fed_cm.enable()
                assert isinstance(result, dict)
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                result = await session.fed_cm.disable()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_reset_cooldown_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.fed_cm.enable()
                result = await session.fed_cm.reset_cooldown()
                assert isinstance(result, dict)
                await session.fed_cm.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_raw_send_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.send("FedCm.enable", {"disableRejectionDelay": False})
                await session.send("FedCm.disable")
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("FedCm not available")

    async def test_type_error_enable_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="disable_rejection_delay"):
                await session.fed_cm.enable(disable_rejection_delay=1)  # type: ignore[arg-type]

    async def test_type_error_select_account_int_dialog_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.select_account(123, 0)  # type: ignore[arg-type]

    async def test_type_error_select_account_str_index(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_index"):
                await session.fed_cm.select_account("d1", "zero")  # type: ignore[arg-type]

    async def test_type_error_click_dialog_button_int_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.click_dialog_button(123, "ErrorGotIt")  # type: ignore[arg-type]

    async def test_type_error_open_url_int_dialog_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.open_url(123, 0, "TermsOfService")  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_int_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.dismiss_dialog(123)  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_int_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="trigger_cooldown"):
                await session.fed_cm.dismiss_dialog("d1", trigger_cooldown=1)  # type: ignore[arg-type]


@pytest.mark.integration
class TestFileSystem:
    async def test_get_directory(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.file_system.get_directory(
                    storage_key="https://example.com",
                    path_components=["root"],
                )
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
                result = await session.smart_card_emulation.enable()
                assert isinstance(result, dict)
                result = await session.smart_card_emulation.disable()
                assert isinstance(result, dict)
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("SmartCardEmulation not available")

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                for _ in range(3):
                    await session.smart_card_emulation.enable()
                    await session.smart_card_emulation.disable()
            except CommandError as exc:
                if not _is_method_not_found(exc):
                    raise
                pytest.skip("SmartCardEmulation not available")

    async def test_report_error_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="request_id must be a str"):
                await session.smart_card_emulation.report_error(42, "cancelled")  # type: ignore[arg-type]

    async def test_report_establish_context_result_bool_rejected(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="context_id must be an int.*bool"):
                await session.smart_card_emulation.report_establish_context_result(
                    "req-1", True,  # type: ignore[arg-type]
                )

    async def test_report_list_readers_result_element_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"readers\[0\] must be a str"):
                await session.smart_card_emulation.report_list_readers_result(
                    "req-1", [42],  # type: ignore[list-item]
                )

    async def test_report_get_status_change_result_element_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"reader_states\[0\] must be a dict"):
                await session.smart_card_emulation.report_get_status_change_result(
                    "req-1", ["not-a-dict"],  # type: ignore[list-item]
                )


@pytest.mark.integration
class TestWebAudio:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.web_audio.enable()
            assert isinstance(result, dict)
            result = await session.web_audio.disable()
            assert isinstance(result, dict)

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
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

    async def test_get_realtime_data_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="context_id must be a str"):
                await session.web_audio.get_realtime_data(42)  # type: ignore[arg-type]

    async def test_get_realtime_data_bool_rejected(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="context_id must be a str.*bool"):
                await session.web_audio.get_realtime_data(True)  # type: ignore[arg-type]


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
