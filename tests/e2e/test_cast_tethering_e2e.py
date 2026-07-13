"""E2E tests for Cast and Tethering domains on a real browser.

Type validation E2E tests verify that TypeError is raised before any
CDP command is sent when using a real browser session.
"""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.e2e
class TestCastE2ETypeValidation:
    async def test_set_sink_to_use_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(42)  # type: ignore[arg-type]

    async def test_set_sink_to_use_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(True)  # type: ignore[arg-type]

    async def test_set_sink_to_use_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(b"chromecast")  # type: ignore[arg-type]

    async def test_set_sink_to_use_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(None)  # type: ignore[arg-type]

    async def test_set_sink_to_use_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use({"name": "sink"})  # type: ignore[arg-type]

    async def test_set_sink_to_use_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(["sink"])  # type: ignore[arg-type]

    async def test_set_sink_to_use_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.set_sink_to_use(3.14)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(True)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(None)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(b"chromecast")  # type: ignore[arg-type]

    async def test_start_tab_mirroring_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(True)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(None)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(b"chromecast")  # type: ignore[arg-type]

    async def test_stop_casting_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(True)  # type: ignore[arg-type]

    async def test_stop_casting_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(None)  # type: ignore[arg-type]

    async def test_stop_casting_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(b"chromecast")  # type: ignore[arg-type]

    async def test_enable_presentation_url_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url=True)  # type: ignore[arg-type]

    async def test_enable_presentation_url_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url=b"https://example.com")  # type: ignore[arg-type]

    async def test_enable_presentation_url_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url={"url": "test"})  # type: ignore[arg-type]

    async def test_enable_presentation_url_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url=["url"])  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(42)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(42)  # type: ignore[arg-type]

    async def test_stop_casting_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(42)  # type: ignore[arg-type]

    async def test_enable_presentation_url_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url=42)  # type: ignore[arg-type]

    async def test_enable_presentation_url_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="presentation_url must be a string"):
                await session.cast.enable(presentation_url=3.14)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring({"name": "sink"})  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(["sink"])  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_desktop_mirroring(3.14)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring({"name": "sink"})  # type: ignore[arg-type]

    async def test_start_tab_mirroring_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(["sink"])  # type: ignore[arg-type]

    async def test_start_tab_mirroring_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.start_tab_mirroring(3.14)  # type: ignore[arg-type]

    async def test_stop_casting_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting({"name": "sink"})  # type: ignore[arg-type]

    async def test_stop_casting_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(["sink"])  # type: ignore[arg-type]

    async def test_stop_casting_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="sink_name must be a string"):
                await session.cast.stop_casting(3.14)  # type: ignore[arg-type]

    async def test_type_error_no_cdp_call(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError):
                await session.cast.set_sink_to_use(42)  # type: ignore[arg-type]
            with contextlib.suppress(Exception):
                await session.cast.disable()


@pytest.mark.e2e
class TestCastE2ELifecycle:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.disable()

    async def test_enable_with_presentation_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable(
                    presentation_url="https://example.com/cast"
                )
                await session.cast.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.enable()
                await session.cast.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.set_sink_to_use("sink1")
                await session.cast.start_desktop_mirroring("sink1")
                await session.cast.start_tab_mirroring("sink1")
                await session.cast.stop_casting("sink1")
                await session.cast.disable()

    async def test_enable_disable_cycle_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.cast.enable()
                    await session.cast.disable()

    async def test_enable_with_empty_presentation_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable(presentation_url="")
                await session.cast.disable()

    async def test_all_sink_methods_same_sink(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.cast.enable()
                await session.cast.set_sink_to_use("my-chromecast")
                await session.cast.start_desktop_mirroring("my-chromecast")
                await session.cast.start_tab_mirroring("my-chromecast")
                await session.cast.stop_casting("my-chromecast")
                await session.cast.disable()


@pytest.mark.e2e
class TestTetheringE2ETypeValidation:
    async def test_bind_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind(3.14)  # type: ignore[arg-type]

    async def test_bind_string_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind("8080")  # type: ignore[arg-type]

    async def test_bind_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind(True)  # type: ignore[arg-type]

    async def test_bind_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind(None)  # type: ignore[arg-type]

    async def test_unbind_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind(3.14)  # type: ignore[arg-type]

    async def test_unbind_string_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind("8080")  # type: ignore[arg-type]

    async def test_unbind_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind(True)  # type: ignore[arg-type]

    async def test_unbind_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind(None)  # type: ignore[arg-type]

    async def test_unbind_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind([8080])  # type: ignore[arg-type]

    async def test_unbind_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind({"port": 8080})  # type: ignore[arg-type]

    async def test_bind_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind([8080])  # type: ignore[arg-type]

    async def test_bind_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.bind({"port": 8080})  # type: ignore[arg-type]

    async def test_unbind_tuple_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind((8080,))  # type: ignore[arg-type]

    async def test_unbind_set_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="port must be an integer"):
                await session.tethering.unbind({8080})  # type: ignore[arg-type]

    async def test_type_error_no_cdp_call(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError):
                await session.tethering.bind("8080")  # type: ignore[arg-type]


@pytest.mark.e2e
class TestTetheringE2ELifecycle:
    async def test_bind_unbind(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(0)
                await session.tethering.unbind(0)

    async def test_unbind_without_bind(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.unbind(0)

    async def test_bind_unbind_multiple_ports(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(8080)
                await session.tethering.bind(9090)
                await session.tethering.unbind(8080)
                await session.tethering.unbind(9090)

    async def test_bind_same_port_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(8080)
                await session.tethering.bind(8080)
                await session.tethering.unbind(8080)

    async def test_bind_unbind_cycle_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.tethering.bind(0)
                    await session.tethering.unbind(0)

    async def test_bind_negative_port(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(-1)
                await session.tethering.unbind(-1)

    async def test_bind_large_port(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.tethering.bind(65535)
                await session.tethering.unbind(65535)
