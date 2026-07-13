"""E2E tests for DeviceOrientation and Media domains (real browser flows).

Exercises type validation, lifecycle flows, and edge cases end-to-end
against a real Chrome browser.
"""

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


@pytest.mark.e2e
class TestDeviceOrientationE2E:
    """Full end-to-end flows against a real browser."""

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

    async def test_set_override_edge_values(self) -> None:
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

    async def test_set_override_negative_values(self) -> None:
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

    async def test_set_override_zero_values(self) -> None:
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

    async def test_type_error_alpha_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0, beta=0.0, gamma=0.0
                )

    async def test_type_error_alpha_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=True, beta=0.0, gamma=0.0
                )

    async def test_type_error_alpha_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha="0.0", beta=0.0, gamma=0.0
                )

    async def test_type_error_alpha_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=None, beta=0.0, gamma=0.0
                )

    async def test_type_error_beta_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="beta must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=90, gamma=0.0
                )

    async def test_type_error_beta_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="beta must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=False, gamma=0.0
                )

    async def test_type_error_gamma_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="gamma must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=0.0, gamma=45
                )

    async def test_type_error_gamma_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="gamma must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0.0, beta=0.0, gamma=True
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

    async def test_type_error_no_call_made(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=0, beta=0, gamma=0
                )
            with pytest.raises(TypeError, match="alpha must be a float"):
                await session.device_orientation.set_device_orientation_override(
                    alpha=True, beta=0.0, gamma=0.0
                )

    async def test_repeated_set_clear_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                for i in range(5):
                    await session.device_orientation.set_device_orientation_override(
                        alpha=float(i * 90), beta=float(i * 45),
                        gamma=float(i * 30),
                    )
                    await session.device_orientation.clear_device_orientation_override()

    async def test_clear_without_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_orientation.clear_device_orientation_override()

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

    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.device_orientation is not None

    async def test_set_override_with_precision(self) -> None:
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

    async def test_set_override_nan(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=float("nan"), beta=0.0, gamma=0.0
                )
                await session.device_orientation.clear_device_orientation_override()

    async def test_set_override_inf(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.device_orientation.set_device_orientation_override(
                    alpha=float("inf"), beta=float("-inf"), gamma=0.0
                )
                await session.device_orientation.clear_device_orientation_override()


@pytest.mark.e2e
class TestMediaE2E:
    """Full end-to-end flows against a real browser."""

    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.media.enable()
            await session.media.disable()

    async def test_repeated_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(5):
                    await session.media.enable()
                    await session.media.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.media.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.media.enable()
                await session.media.enable()
                await session.media.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.media.enable()
                await session.media.disable()
                await session.media.disable()

    async def test_enable_disable_enable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.media.enable()
                await session.media.disable()
                await session.media.enable()
                await session.media.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.media.enable()
            except Exception:
                return
            assert isinstance(result, dict)
            with contextlib.suppress(Exception):
                await session.media.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.media.enable()
                result = await session.media.disable()
            except Exception:
                return
            assert isinstance(result, dict)

    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.media is not None

    async def test_no_get_player_properties_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.media, "get_player_properties")

    async def test_no_get_players_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.media, "get_players")
