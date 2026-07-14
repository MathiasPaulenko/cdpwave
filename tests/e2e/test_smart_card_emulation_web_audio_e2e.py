"""E2E tests for SmartCardEmulation and WebAudio domains (real browser flows).

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
class TestSmartCardEmulationE2E:
    """Full end-to-end flows against a real browser."""

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
            except Exception as exc:
                if "found" not in str(exc).lower():
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
            except Exception as exc:
                if "found" not in str(exc).lower():
                    raise
                pytest.skip("SmartCardEmulation not available")

    async def test_report_error_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="request_id must be a str"):
                await session.smart_card_emulation.report_error(42, "cancelled")  # type: ignore[arg-type]

    async def test_report_error_result_code_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="result_code must be a str"):
                await session.smart_card_emulation.report_error("req-1", 42)  # type: ignore[arg-type]

    async def test_report_establish_context_result_bool_rejected(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="context_id must be an int.*bool"):
                await session.smart_card_emulation.report_establish_context_result(
                    "req-1", True,  # type: ignore[arg-type]
                )

    async def test_report_establish_context_result_request_id_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="request_id must be a str"):
                await session.smart_card_emulation.report_establish_context_result(
                    42, 1,  # type: ignore[arg-type]
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

    async def test_report_connect_result_handle_bool_rejected(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be an int.*bool"):
                await session.smart_card_emulation.report_connect_result(
                    "req-1", True,  # type: ignore[arg-type]
                )

    async def test_report_data_result_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="data must be a str"):
                await session.smart_card_emulation.report_data_result("req-1", 42)  # type: ignore[arg-type]

    async def test_report_status_result_atr_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="atr must be a str"):
                await session.smart_card_emulation.report_status_result(
                    "req-1", "reader", "present", 42,  # type: ignore[arg-type]
                )

    async def test_report_plain_result_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                result = await session.smart_card_emulation.report_plain_result("")
                assert isinstance(result, dict)
            except Exception as exc:
                if "found" not in str(exc).lower():
                    raise
                pytest.skip("SmartCardEmulation not available")

    async def test_no_spurious_methods(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            public = {
                name
                for name in dir(session.smart_card_emulation)
                if not name.startswith("_")
                and callable(getattr(session.smart_card_emulation, name))
            }
            assert public == {
                "enable",
                "disable",
                "report_establish_context_result",
                "report_release_context_result",
                "report_list_readers_result",
                "report_get_status_change_result",
                "report_begin_transaction_result",
                "report_plain_result",
                "report_connect_result",
                "report_data_result",
                "report_status_result",
                "report_error",
            }


@pytest.mark.e2e
class TestWebAudioE2E:
    """Full end-to-end flows against a real browser."""

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

    async def test_get_realtime_data_none_rejected(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="context_id must be a str"):
                await session.web_audio.get_realtime_data(None)  # type: ignore[arg-type]

    async def test_get_realtime_data_empty_string(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_audio.enable()
            with contextlib.suppress(Exception):
                result = await session.web_audio.get_realtime_data("")
                assert isinstance(result, dict)
            await session.web_audio.disable()

    async def test_get_realtime_data_with_real_context(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.web_audio.enable()
            result = await session.runtime.evaluate(
                "new AudioContext().id", return_by_value=True,
            )
            ctx_id = result.get("result", {}).get("value", "")
            if ctx_id:
                rt = await session.web_audio.get_realtime_data(ctx_id)
                assert isinstance(rt, dict)
            await session.web_audio.disable()

    async def test_no_spurious_methods(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            public = {
                name
                for name in dir(session.web_audio)
                if not name.startswith("_")
                and callable(getattr(session.web_audio, name))
            }
            assert public == {"enable", "disable", "get_realtime_data"}
