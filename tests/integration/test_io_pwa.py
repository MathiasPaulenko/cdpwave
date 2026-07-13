"""Integration tests for IO and PWA domains.

Tests cover:
- IO.read with a real stream handle (Page.printToPDF with returnAsStream)
- IO.close after read
- IO.resolveBlob with a real blob
- PWA install/uninstall/getOsAppState/launch/changeAppUserSettings (with suppress)
- Type errors in integration context
"""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestIOIntegration:
    async def test_read_and_close_stream(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                assert "stream" in result
                handle = result["stream"]

                read_result = await session.io.read(handle, size=1024)
                assert "data" in read_result
                assert "eof" in read_result

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_read_with_offset(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                read_result = await session.io.read(handle, offset=0, size=512)
                assert "data" in read_result

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_read_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                all_data: list[str] = []
                while True:
                    chunk = await session.io.read(handle, size=4096)
                    all_data.append(chunk.get("data", ""))
                    if chunk.get("eof"):
                        break

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_resolve_blob(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "new Blob(['hello world'], {type: 'text/plain'})",
                return_by_value=False,
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                with contextlib.suppress(Exception):
                    result = await session.io.resolve_blob(object_id)
                    assert "uuid" in result

    async def test_close(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]
                await session.io.close(handle)

    async def test_type_error_read_handle_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.read(42)

    async def test_type_error_read_offset_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="offset must be an int"):
                await session.io.read("h1", offset=True)

    async def test_type_error_read_size_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="size must be an int"):
                await session.io.read("h1", size="1024")

    async def test_type_error_close_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.close(42)

    async def test_type_error_resolve_blob_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="object_id must be a str"):
                await session.io.resolve_blob(42)

    async def test_raw_send_read(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]
                read_result = await session.send("IO.read", {"handle": handle, "size": 512})
                assert isinstance(read_result, dict)

                with contextlib.suppress(Exception):
                    await session.send("IO.close", {"handle": handle})


@pytest.mark.integration
class TestPWAIntegration:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.pwa is not None

    async def test_get_os_app_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.pwa.get_os_app_state("manifest123")
                assert isinstance(result, dict)

    async def test_install(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.install(
                    "manifest123",
                    install_url_or_bundle_url="https://example.com/app",
                )

    async def test_uninstall(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.uninstall("manifest123")

    async def test_launch(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch("manifest123")

    async def test_launch_with_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch("manifest123", url="https://example.com")

    async def test_launch_files_in_app(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch_files_in_app("manifest123", ["/file1.txt"])

    async def test_open_current_page_in_app(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.open_current_page_in_app("manifest123")

    async def test_change_app_user_settings_default(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings("manifest123")

    async def test_change_app_user_settings_all(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    link_capturing=True,
                    display_mode="standalone",
                )

    async def test_change_app_user_settings_link_capturing_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    link_capturing=False,
                )

    async def test_type_error_install_manifest_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.install(42)

    async def test_type_error_launch_url_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="url must be a str"):
                await session.pwa.launch("m1", url=42)

    async def test_type_error_change_app_user_settings_link_capturing_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="link_capturing must be a bool"):
                await session.pwa.change_app_user_settings("m1", link_capturing=1)

    async def test_type_error_change_app_user_settings_display_mode_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="display_mode must be a str"):
                await session.pwa.change_app_user_settings("m1", display_mode=42)

    async def test_type_error_get_os_app_state_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.get_os_app_state(42)

    async def test_type_error_launch_files_in_app_files_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="files must be a list"):
                await session.pwa.launch_files_in_app("m1", "not a list")

    async def test_type_error_uninstall_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.uninstall(True)

    async def test_raw_send_get_os_app_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.send("PWA.getOsAppState", {"manifestId": "manifest123"})
                assert isinstance(result, dict)


@pytest.mark.integration
class TestIOEdgeIntegration:
    async def test_read_until_eof(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                total = 0
                while True:
                    chunk = await session.io.read(handle, size=4096)
                    total += len(chunk.get("data", ""))
                    if chunk.get("eof"):
                        break
                assert total > 0

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_read_with_offset_and_size(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                chunk = await session.io.read(handle, offset=0, size=100)
                assert "data" in chunk

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_resolve_blob_with_real_blob(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "new Blob(['test data'], {type: 'text/plain'})",
                return_by_value=False,
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                with contextlib.suppress(Exception):
                    result = await session.io.resolve_blob(object_id)
                    assert "uuid" in result
                    assert isinstance(result["uuid"], str)

    async def test_close_invalid_handle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.io.close("invalid-handle")

    async def test_read_invalid_handle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.io.read("invalid-handle")

    async def test_type_error_read_handle_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.read(b"handle")

    async def test_type_error_read_offset_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="offset must be an int"):
                await session.io.read("h", offset={"v": 1})

    async def test_type_error_read_size_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="size must be an int"):
                await session.io.read("h", size={10})

    async def test_type_error_close_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.close({"h"})

    async def test_type_error_resolve_blob_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="object_id must be a str"):
                await session.io.resolve_blob(b"obj")

    async def test_raw_send_resolve_blob(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.runtime.enable()
            eval_result = await session.runtime.evaluate(
                "new Blob(['x'])",
                return_by_value=False,
            )
            object_id = eval_result.get("result", {}).get("objectId")
            if object_id:
                with contextlib.suppress(Exception):
                    result = await session.send("IO.resolveBlob", {"objectId": object_id})
                    assert isinstance(result, dict)


@pytest.mark.integration
class TestPWAEdgeIntegration:
    async def test_install_with_long_manifest_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.install("m" * 5000)

    async def test_launch_with_long_url(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch(
                    "manifest123",
                    url="https://example.com/" + "x" * 1000,
                )

    async def test_launch_files_in_app_many_files(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch_files_in_app(
                    "manifest123",
                    [f"/file{i}.txt" for i in range(50)],
                )

    async def test_change_app_user_settings_display_mode_browser(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    display_mode="browser",
                )

    async def test_change_app_user_settings_link_false_display_standalone(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    link_capturing=False,
                    display_mode="standalone",
                )

    async def test_type_error_install_manifest_id_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.install(b"m1")

    async def test_type_error_install_url_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
                await session.pwa.install("m1", b"https://x.com")

    async def test_type_error_launch_manifest_id_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.launch({"m1"})

    async def test_type_error_launch_files_in_app_files_tuple(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="files must be a list"):
                await session.pwa.launch_files_in_app("m1", ("/f",))

    async def test_type_error_launch_files_in_app_element_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
                await session.pwa.launch_files_in_app("m1", [42])

    async def test_type_error_change_app_user_settings_link_capturing_float(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="link_capturing must be a bool"):
                await session.pwa.change_app_user_settings("m1", link_capturing=1.0)

    async def test_type_error_open_current_page_in_app_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.open_current_page_in_app(b"m1")

    async def test_type_error_uninstall_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.uninstall({"m1"})

    async def test_raw_send_install(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "PWA.install",
                    {"manifestId": "manifest123"},
                )

    async def test_raw_send_change_app_user_settings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send(
                    "PWA.changeAppUserSettings",
                    {
                        "manifestId": "manifest123",
                        "linkCapturing": True,
                        "displayMode": "standalone",
                    },
                )


@pytest.mark.integration
class TestIOEdgeIntegrationRound2:
    async def test_read_after_close(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                await session.io.read(handle, size=100)
                await session.io.close(handle)

                with contextlib.suppress(Exception):
                    await session.io.read(handle, size=100)

    async def test_close_already_closed(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                await session.io.close(handle)

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_resolve_blob_invalid_object_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.io.resolve_blob("invalid-object-id-12345")

    async def test_read_with_negative_offset(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                with contextlib.suppress(Exception):
                    await session.io.read(handle, offset=-1, size=100)

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_raw_send_read_none_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("IO.read", None)

    async def test_raw_send_close_none_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("IO.close", None)

    async def test_read_chunk_count(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                chunks = 0
                while True:
                    chunk = await session.io.read(handle, size=512)
                    chunks += 1
                    if chunk.get("eof"):
                        break

                assert chunks >= 1

                with contextlib.suppress(Exception):
                    await session.io.close(handle)

    async def test_read_base64_encoded(self) -> None:
        async with (
            await CDPClient.launch(headless=True, extra_args=["--headless=new"]) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("https://example.com")

            with contextlib.suppress(Exception):
                result = await session.page.print_to_pdf(return_as_stream=True)
                handle = result["stream"]

                chunk = await session.io.read(handle, size=512)
                assert "base64Encoded" in chunk
                assert isinstance(chunk["base64Encoded"], bool)

                with contextlib.suppress(Exception):
                    await session.io.close(handle)


@pytest.mark.integration
class TestPWAEdgeIntegrationRound2:
    async def test_install_and_uninstall_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.install("manifest-roundtrip")

            with contextlib.suppress(Exception):
                await session.pwa.uninstall("manifest-roundtrip")

    async def test_change_app_user_settings_link_true_display_browser(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    link_capturing=True,
                    display_mode="browser",
                )

    async def test_launch_files_in_app_empty_list(self) -> None:
        """Go source says: 'If no files are provided as the parameter, this API
        also returns an error.' This should raise a CDP error."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch_files_in_app("manifest123", [])

    async def test_raw_send_uninstall_none_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("PWA.uninstall", None)

    async def test_raw_send_get_os_app_state_none_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("PWA.getOsAppState", None)

    async def test_install_with_isolated_app_manifest(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.install(
                    "isolated-app://abc123",
                    install_url_or_bundle_url="file:///path/to/app.swbn",
                )

    async def test_change_app_user_settings_link_true_display_standalone(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.change_app_user_settings(
                    "manifest123",
                    link_capturing=True,
                    display_mode="standalone",
                )

    async def test_type_error_read_handle_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.read(None)

    async def test_type_error_read_offset_float(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="offset must be an int"):
                await session.io.read("h", offset=10.5)

    async def test_type_error_read_size_tuple(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="size must be an int"):
                await session.io.read("h", size=(10,))

    async def test_type_error_close_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="handle must be a str"):
                await session.io.close(None)

    async def test_type_error_resolve_blob_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="object_id must be a str"):
                await session.io.resolve_blob(None)

    async def test_type_error_install_url_none(self) -> None:
        """None is valid for install_url_or_bundle_url (it's optional)."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.install("m1", install_url_or_bundle_url=None)

    async def test_type_error_launch_url_none(self) -> None:
        """None is valid for url (it's optional)."""
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.pwa.launch("m1", url=None)

    async def test_type_error_launch_files_in_app_element_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
                await session.pwa.launch_files_in_app("m1", [None])

    async def test_type_error_change_app_user_settings_link_capturing_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="link_capturing must be a bool"):
                await session.pwa.change_app_user_settings("m1", link_capturing=[True])

    async def test_type_error_open_current_page_in_app_float(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.open_current_page_in_app(3.14)

    async def test_type_error_uninstall_float(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="manifest_id must be a str"):
                await session.pwa.uninstall(3.14)
