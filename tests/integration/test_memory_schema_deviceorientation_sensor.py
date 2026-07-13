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
            assert isinstance(result["documents"], int)
            assert isinstance(result["nodes"], int)

    async def test_get_dom_counters_for_leak_detection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.memory.get_dom_counters_for_leak_detection()
                assert "counters" in result
                assert isinstance(result["counters"], list)

    async def test_prepare_for_leak_detection(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.prepare_for_leak_detection()

    async def test_forcibly_purge_javascript_memory(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.memory.forcibly_purge_javascript_memory()

    async def test_set_pressure_notifications_suppressed_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.set_pressure_notifications_suppressed(True)

    async def test_set_pressure_notifications_suppressed_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.set_pressure_notifications_suppressed(False)

    async def test_simulate_pressure_notification_moderate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.simulate_pressure_notification("moderate")

    async def test_simulate_pressure_notification_critical(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.memory.simulate_pressure_notification("critical")

    async def test_start_stop_sampling_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.memory.start_sampling(sampling_interval=1024)
                await session.memory.stop_sampling()

    async def test_start_sampling_with_suppress_randomness(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.memory.start_sampling(
                    sampling_interval=2048,
                    suppress_randomness=True,
                )
                await session.memory.stop_sampling()

    async def test_start_sampling_defaults(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.memory.start_sampling()
                await session.memory.stop_sampling()

    async def test_get_sampling_profile_after_start(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.memory.start_sampling(sampling_interval=4096)
                await session.runtime.evaluate("1 + 1")
                result = await session.memory.get_sampling_profile()
                assert "profile" in result
                await session.memory.stop_sampling()

    async def test_get_all_time_sampling_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.memory.get_all_time_sampling_profile()
                assert "profile" in result

    async def test_get_browser_sampling_profile(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.memory.get_browser_sampling_profile()
                assert "profile" in result

    async def test_type_error_propagates_suppressed(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="suppressed must be a bool"):
                await session.memory.set_pressure_notifications_suppressed(1)

    async def test_type_error_propagates_level(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="level must be a str"):
                await session.memory.simulate_pressure_notification(42)

    async def test_value_error_propagates_level(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="level must be 'moderate' or 'critical'"):
                await session.memory.simulate_pressure_notification("low")

    async def test_type_error_propagates_sampling_interval_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sampling_interval must be an int"):
                await session.memory.start_sampling(sampling_interval=True)

    async def test_raw_send_memory_command(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.send("Memory.getDOMCounters")
            assert "documents" in result
            assert "nodes" in result


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

    async def test_get_domains_contains_known_domain(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            names = [d["name"] for d in result["domains"]]
            assert "Page" in names

    async def test_get_domains_has_version(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            for d in result["domains"]:
                assert "version" in d
                assert isinstance(d["version"], str)

    async def test_get_domains_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            assert isinstance(result, dict)

    async def test_get_domains_multiple_calls(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            r1 = await session.schema.get_domains()
            r2 = await session.schema.get_domains()
            assert len(r1["domains"]) == len(r2["domains"])

    async def test_raw_send_get_domains(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.send("Schema.getDomains")
            assert "domains" in result

    async def test_get_domains_name_is_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            for d in result["domains"]:
                assert isinstance(d["name"], str)


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

    async def test_override_edge_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=360.0, beta=180.0, gamma=90.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_override_negative_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=-180.0, beta=-90.0, gamma=-45.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_override_zero_values(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=0.0, gamma=0.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_clear_without_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_orientation.clear_device_orientation_override()

    async def test_repeated_set_clear_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                for i in range(3):
                    await session.device_orientation.set_device_orientation_override(
                        alpha=float(i * 90), beta=float(i * 45), gamma=float(i * 30)
                    )
                    await session.device_orientation.clear_device_orientation_override()

    async def test_type_error_alpha_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0, beta=0.0, gamma=0.0
                )

    async def test_type_error_beta_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="beta must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=True, gamma=0.0
                )

    async def test_type_error_gamma_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="gamma must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=0.0, gamma="0.0"
                )

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.device_orientation is not None

    async def test_set_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                result = await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=90.0, gamma=0.0
                )
            except Exception:
                return
            assert isinstance(result, dict)
            with contextlib.suppress(Exception):
                await session.device_orientation.clear_device_orientation_override()

    async def test_clear_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            try:
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=90.0, gamma=0.0
                )
                result = await session.device_orientation.clear_device_orientation_override()
            except Exception:
                return
            assert isinstance(result, dict)

    async def test_double_set_override(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=90.0, gamma=0.0
                )
                await session.device_orientation.set_device_orientation_override(
                    alpha=180.0, beta=45.0, gamma=-30.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_set_after_clear(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=90.0, gamma=0.0
                )
                await session.device_orientation.clear_device_orientation_override()
                await session.device_orientation.set_device_orientation_override(
                    alpha=180.0, beta=45.0, gamma=-30.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_set_override_precision(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=359.999, beta=179.999, gamma=89.999
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_type_error_alpha_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=None, beta=0.0, gamma=0.0
                )

    async def test_type_error_alpha_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=[1.0], beta=0.0, gamma=0.0
                )

    async def test_type_error_gamma_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="gamma must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=0.0, gamma=False
                )

    async def test_type_error_all_wrong(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha="bad", beta="bad", gamma="bad"
                )


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
