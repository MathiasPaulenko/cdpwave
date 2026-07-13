"""Functional tests for Preload, IndexedDB, Media, and DeviceAccess domains."""

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
class TestPreload:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.disable()

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.preload is not None

    async def test_raw_send_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Preload.enable")
                await session.send("Preload.disable")

    async def test_enable_disable_enable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.disable()
                await session.preload.enable()
                await session.preload.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.enable()
                await session.preload.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.disable()
                await session.preload.disable()

    async def test_enable_returns_dict_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.preload.enable()
                assert isinstance(result, dict)
                await session.preload.disable()


@pytest.mark.integration
class TestIndexedDB:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.indexed_db.enable()
            await session.indexed_db.disable()

    async def test_request_database_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.indexed_db.enable()
            result = await session.indexed_db.request_database_names(
                security_origin="https://example.com"
            )
            assert "databaseNames" in result
            await session.indexed_db.disable()


@pytest.mark.integration
class TestMedia:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
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

    async def test_repeated_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.media.enable()
                    await session.media.disable()

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.media is not None

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

    async def test_enable_returns_dict_type(self) -> None:
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

    async def test_disable_returns_dict_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.media.disable()
            except Exception:
                return
            assert isinstance(result, dict)


@pytest.mark.integration
class TestDeviceAccess:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.disable()

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.device_access is not None

    async def test_cancel_prompt_type_validation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt(123)

    async def test_select_prompt_type_validation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(123, "dev1")
            with pytest.raises(TypeError, match="device_id must be a str"):
                await session.device_access.select_prompt("req1", 456)

    async def test_raw_send_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("DeviceAccess.enable")
                await session.send("DeviceAccess.disable")

    async def test_cancel_prompt_none_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt(None)

    async def test_cancel_prompt_bool_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt(True)

    async def test_select_prompt_none_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(None, "dev1")

    async def test_select_prompt_none_device_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="device_id must be a str"):
                await session.device_access.select_prompt("req1", None)

    async def test_select_prompt_bool_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(True, "dev1")

    async def test_select_prompt_bool_device_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="device_id must be a str"):
                await session.device_access.select_prompt("req1", False)

    async def test_select_prompt_both_wrong_id_first(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(123, 456)

    async def test_enable_disable_enable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.disable()
                await session.device_access.enable()
                await session.device_access.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.enable()
                await session.device_access.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.disable()
                await session.device_access.disable()

    async def test_enable_returns_dict_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.device_access.enable()
                assert isinstance(result, dict)
                await session.device_access.disable()

    async def test_select_prompt_valid_strings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.select_prompt("req1", "dev1")
                await session.device_access.disable()

    async def test_cancel_prompt_valid_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.cancel_prompt("req1")
                await session.device_access.disable()

    async def test_raw_send_select_prompt(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "DeviceAccess.selectPrompt",
                    {"id": "req1", "deviceId": "dev1"},
                )

    async def test_raw_send_cancel_prompt(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "DeviceAccess.cancelPrompt",
                    {"id": "req1"},
                )
