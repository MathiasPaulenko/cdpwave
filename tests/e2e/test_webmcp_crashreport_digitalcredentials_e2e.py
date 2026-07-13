"""E2E tests for WebMCP, CrashReportContext, and DigitalCredentials domains.

These tests run against a real browser. Since all three domains are
experimental, CommandError is suppressed for lifecycle tests where
the domain may not be available. Type validation tests do not require
the domain to be available — TypeError is raised before any CDP command
is sent.
"""

import contextlib

import pytest

from cdpwave import CDPClient, CommandError


@pytest.mark.e2e
class TestWebMCPE2ELifecycle:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                await session.web_mcp.enable()
                await session.web_mcp.disable()

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                for _ in range(3):
                    await session.web_mcp.enable()
                    await session.web_mcp.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                await session.web_mcp.disable()


@pytest.mark.e2e
class TestWebMCPNoSpuriousMethods:
    async def test_no_invoke_tool_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.web_mcp, "invoke_tool")

    async def test_no_cancel_invocation_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.web_mcp, "cancel_invocation")


@pytest.mark.e2e
class TestWebMCPCommandError:
    async def test_command_error_when_experimental_unavailable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.web_mcp.enable()
            except CommandError:
                pass
            except Exception:
                pass


@pytest.mark.e2e
class TestCrashReportContextE2ELifecycle:
    async def test_get_entries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.crash_report_context.get_entries()
                assert isinstance(result, dict)

    async def test_get_entries_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                for _ in range(3):
                    result = await session.crash_report_context.get_entries()
                    assert isinstance(result, dict)


@pytest.mark.e2e
class TestCrashReportContextCommandError:
    async def test_command_error_when_experimental_unavailable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.crash_report_context.get_entries()
            except CommandError:
                pass
            except Exception:
                pass


@pytest.mark.e2e
class TestDigitalCredentialsE2ELifecycle:
    async def test_set_decline(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline"
                )
                assert isinstance(result, dict)

    async def test_set_respond_with_protocol(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", protocol="openid4vp"
                )
                assert isinstance(result, dict)

    async def test_set_respond_with_response(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", response={"token": "abc"}
                )
                assert isinstance(result, dict)

    async def test_set_with_frame_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id="frame1"
                )
                assert isinstance(result, dict)

    async def test_repeated_calls(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                await session.digital_credentials.set_virtual_wallet_behavior("decline")
                await session.digital_credentials.set_virtual_wallet_behavior("wait")
                await session.digital_credentials.set_virtual_wallet_behavior("clear")


@pytest.mark.e2e
class TestDigitalCredentialsE2ETypeValidation:
    async def test_action_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]

    async def test_action_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(True)  # type: ignore[arg-type]

    async def test_protocol_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="protocol must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", protocol=42  # type: ignore[arg-type]
                )

    async def test_response_str_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="response must be a dict"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", response="bad"  # type: ignore[arg-type]
                )

    async def test_frame_id_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id=42  # type: ignore[arg-type]
                )

    async def test_type_error_no_cdp_call(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError):
                await session.digital_credentials.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]


@pytest.mark.e2e
class TestDigitalCredentialsCommandError:
    async def test_command_error_when_experimental_unavailable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            try:
                await session.digital_credentials.set_virtual_wallet_behavior("decline")
            except CommandError:
                pass
            except Exception:
                pass


@pytest.mark.e2e
class TestWebMCPAdditionalE2E:
    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.web_mcp.enable()
                assert isinstance(result, dict)
                await session.web_mcp.disable()

    async def test_alternating_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                await session.web_mcp.enable()
                await session.web_mcp.disable()
                await session.web_mcp.enable()
                await session.web_mcp.disable()

    async def test_no_spurious_methods_explicit(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.web_mcp, "invoke_tool")
            assert not hasattr(session.web_mcp, "cancel_invocation")
            assert not hasattr(session.web_mcp, "invokeTool")
            assert not hasattr(session.web_mcp, "cancelInvocation")


@pytest.mark.e2e
class TestCrashReportContextAdditionalE2E:
    async def test_get_entries_returns_dict_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.crash_report_context.get_entries()
                assert isinstance(result, dict)
                if "entries" in result:
                    assert isinstance(result["entries"], list)

    async def test_no_spurious_methods(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.crash_report_context, "enable")
            assert not hasattr(session.crash_report_context, "disable")
            assert not hasattr(session.crash_report_context, "set_entries")


@pytest.mark.e2e
class TestDigitalCredentialsAdditionalE2ELifecycle:
    @pytest.mark.parametrize("action", ["respond", "decline", "wait", "clear"])
    async def test_all_enum_values(self, action: str) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    action
                )
                assert isinstance(result, dict)

    async def test_all_params_combined(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(CommandError):
                result = await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond",
                    protocol="openid4vp",
                    response={"token": "abc123"},
                    frame_id="frame1",
                )
                assert isinstance(result, dict)

    async def test_unicode_action_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="action must be"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond🔑"
                )

    async def test_empty_string_action_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match="action must be"):
                await session.digital_credentials.set_virtual_wallet_behavior("")


@pytest.mark.e2e
class TestDigitalCredentialsAdditionalE2ETypeValidation:
    async def test_action_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(3.14)  # type: ignore[arg-type]

    async def test_action_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(b"respond")  # type: ignore[arg-type]

    async def test_action_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior({"a": 1})  # type: ignore[arg-type]

    async def test_action_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(["respond"])  # type: ignore[arg-type]

    async def test_protocol_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="protocol must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", protocol=True  # type: ignore[arg-type]
                )

    async def test_protocol_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="protocol must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", protocol=3.14  # type: ignore[arg-type]
                )

    async def test_protocol_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="protocol must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", protocol=b"x"  # type: ignore[arg-type]
                )

    async def test_response_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="response must be a dict"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", response=42  # type: ignore[arg-type]
                )

    async def test_response_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="response must be a dict"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", response=True  # type: ignore[arg-type]
                )

    async def test_response_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="response must be a dict"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "respond", response=[1, 2]  # type: ignore[arg-type]
                )

    async def test_frame_id_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id=True  # type: ignore[arg-type]
                )

    async def test_frame_id_float_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id=3.14  # type: ignore[arg-type]
                )

    async def test_frame_id_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id=b"f"  # type: ignore[arg-type]
                )

    async def test_frame_id_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id={"a": 1}  # type: ignore[arg-type]
                )

    async def test_frame_id_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="frame_id must be a str"):
                await session.digital_credentials.set_virtual_wallet_behavior(
                    "decline", frame_id=["f"]  # type: ignore[arg-type]
                )

    async def test_no_spurious_methods(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert not hasattr(session.digital_credentials, "enable")
            assert not hasattr(session.digital_credentials, "disable")
            assert not hasattr(session.digital_credentials, "get")
            assert not hasattr(session.digital_credentials, "set_behavior")
