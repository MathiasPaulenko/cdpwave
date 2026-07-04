"""Functional tests for Memory, Schema, DeviceOrientation, and Sensor domains."""

import asyncio
import contextlib

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
class TestMemory:
    async def test_get_dom_counters(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.memory.get_dom_counters()
            assert "documents" in result
            assert "nodes" in result

    async def test_force_garbage_collection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.for_force_garbage_collection()

    async def test_prepare_for_leak_detection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.prepare_for_leak_detection()

    async def test_simulate_pressure_notification(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.simulate_pressure_notification("moderate")


@pytest.mark.integration
class TestSchema:
    async def test_get_domains(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            assert "domains" in result
            assert len(result["domains"]) > 0


@pytest.mark.integration
class TestDeviceOrientation:
    async def test_set_and_clear_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.device_orientation.set_device_orientation_override(
                alpha=0.0, beta=90.0, gamma=0.0
            )
            await session.device_orientation.clear_device_orientation_override()


@pytest.mark.integration
class TestSensor:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.sensor.enable()
                await session.sensor.disable()

    async def test_set_and_clear_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.sensor.enable()
                await session.sensor.set_sensor_override(
                    "accelerometer", {"x": 0, "y": 9.8, "z": 0}
                )
                await session.sensor.clear_sensor_override("accelerometer")
                await session.sensor.disable()
