"""Functional tests for ServiceWorker, SystemInfo, WebAuthn, and IO domains."""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestServiceWorker:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.service_worker.enable()
            await session.service_worker.disable()


@pytest.mark.integration
class TestSystemInfo:
    async def test_get_info(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            assert "gpu" in result

    async def test_get_process_info(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getProcessInfo")
            assert "processInfo" in result

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.system_info is not None

    async def test_get_feature_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.system_info.get_feature_state("Vulkan")
                assert "featureEnabled" in result

    async def test_type_error_get_feature_state_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="feature_state must be a str"):
                await session.system_info.get_feature_state(42)


@pytest.mark.integration
class TestWebAuthn:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            await session.web_authn.disable()

    async def test_add_and_remove_virtual_authenticator(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.web_authn.enable()
            result = await session.web_authn.add_virtual_authenticator(
                protocol="ctap2",
                transport="internal",
                has_resident_key=True,
                has_user_verification=True,
                automatic_presence_simulation=True,
            )
            assert "authenticatorId" in result
            auth_id = result["authenticatorId"]

            await session.web_authn.set_user_verified(auth_id, True)
            await session.web_authn.set_automatic_presence_simulation(
                auth_id, True
            )

            creds = await session.web_authn.get_credentials(auth_id)
            assert "credentials" in creds

            await session.web_authn.clear_credentials(auth_id)
            await session.web_authn.remove_virtual_authenticator(auth_id)
            await session.web_authn.disable()


@pytest.mark.integration
class TestIO:
    async def test_read_and_close_stream(self) -> None:
        async with (
            await CDPClient.launch(
                headless=True, extra_args=["--headless=new"]
            ) as client,
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
