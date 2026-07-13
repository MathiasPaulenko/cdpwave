"""Integration tests for WebMCP, CrashReportContext, and DigitalCredentials domains.

These tests run against a real Chromium-based browser. Experimental domains
may not be available in all browser versions, so CommandError is suppressed
where appropriate.
"""

import contextlib

import pytest

from cdpwave import CommandError


@pytest.mark.integration
class TestWebMCPIntegration:
    async def test_enable_disable(self, page) -> None:
        with contextlib.suppress(CommandError):
            await page.web_mcp.enable()
        with contextlib.suppress(CommandError):
            await page.web_mcp.disable()

    async def test_enable_disable_cycle(self, page) -> None:
        with contextlib.suppress(CommandError):
            for _ in range(3):
                await page.web_mcp.enable()
                await page.web_mcp.disable()

    async def test_disable_without_enable(self, page) -> None:
        with contextlib.suppress(CommandError):
            await page.web_mcp.disable()

    async def test_enable_returns_dict(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.web_mcp.enable()
            assert isinstance(result, dict)
            await page.web_mcp.disable()


@pytest.mark.integration
class TestCrashReportContextIntegration:
    async def test_get_entries_returns_dict(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.crash_report_context.get_entries()
            assert isinstance(result, dict)
            if "entries" in result:
                assert isinstance(result["entries"], list)

    async def test_get_entries_repeated(self, page) -> None:
        with contextlib.suppress(CommandError):
            for _ in range(3):
                result = await page.crash_report_context.get_entries()
                assert isinstance(result, dict)


@pytest.mark.integration
class TestDigitalCredentialsIntegration:
    async def test_set_virtual_wallet_behavior_decline(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                "decline"
            )
            assert isinstance(result, dict)

    async def test_set_virtual_wallet_behavior_with_protocol(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol="openid4vp"
            )
            assert isinstance(result, dict)

    async def test_set_virtual_wallet_behavior_with_response(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", response={"token": "abc"}
            )
            assert isinstance(result, dict)

    async def test_set_virtual_wallet_behavior_with_frame_id(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id="frame1"
            )
            assert isinstance(result, dict)

    async def test_type_error_action_int(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]

    async def test_type_error_action_bool(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(True)  # type: ignore[arg-type]

    async def test_type_error_protocol_int(self, page) -> None:
        with pytest.raises(TypeError, match="protocol must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol=42  # type: ignore[arg-type]
            )

    async def test_type_error_response_str(self, page) -> None:
        with pytest.raises(TypeError, match="response must be a dict"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", response="not a dict"  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_int(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id=42  # type: ignore[arg-type]
            )

    async def test_repeated_calls(self, page) -> None:
        with contextlib.suppress(CommandError):
            await page.digital_credentials.set_virtual_wallet_behavior("decline")
            await page.digital_credentials.set_virtual_wallet_behavior("wait")
            await page.digital_credentials.set_virtual_wallet_behavior("clear")


@pytest.mark.integration
class TestWebMCPAdditionalIntegration:
    async def test_alternating_enable_disable(self, page) -> None:
        with contextlib.suppress(CommandError):
            await page.web_mcp.enable()
            await page.web_mcp.disable()
            await page.web_mcp.enable()
            await page.web_mcp.disable()

    async def test_enable_returns_dict_type(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.web_mcp.enable()
            assert isinstance(result, dict)
            await page.web_mcp.disable()

    async def test_disable_returns_dict_type(self, page) -> None:
        with contextlib.suppress(CommandError):
            await page.web_mcp.enable()
            result = await page.web_mcp.disable()
            assert isinstance(result, dict)

    async def test_no_spurious_methods(self, page) -> None:
        assert not hasattr(page.web_mcp, "invoke_tool")
        assert not hasattr(page.web_mcp, "cancel_invocation")


@pytest.mark.integration
class TestCrashReportContextAdditionalIntegration:
    async def test_get_entries_returns_entries_list(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.crash_report_context.get_entries()
            assert isinstance(result, dict)
            if "entries" in result:
                entries = result["entries"]
                assert isinstance(entries, list)
                for entry in entries:
                    assert isinstance(entry, dict)
                    assert "key" in entry
                    assert "value" in entry
                    assert "frameId" in entry

    async def test_no_spurious_methods(self, page) -> None:
        assert not hasattr(page.crash_report_context, "enable")
        assert not hasattr(page.crash_report_context, "disable")


@pytest.mark.integration
class TestDigitalCredentialsAdditionalIntegration:
    @pytest.mark.parametrize("action", ["respond", "decline", "wait", "clear"])
    async def test_all_enum_values(self, page, action: str) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                action
            )
            assert isinstance(result, dict)

    async def test_all_params_combined(self, page) -> None:
        with contextlib.suppress(CommandError):
            result = await page.digital_credentials.set_virtual_wallet_behavior(
                "respond",
                protocol="openid4vp",
                response={"token": "abc123"},
                frame_id="frame1",
            )
            assert isinstance(result, dict)

    async def test_type_error_action_float(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(3.14)  # type: ignore[arg-type]

    async def test_type_error_action_bytes(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(b"respond")  # type: ignore[arg-type]

    async def test_type_error_action_dict(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior({"a": 1})  # type: ignore[arg-type]

    async def test_type_error_action_list(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(["respond"])  # type: ignore[arg-type]

    async def test_type_error_protocol_bool(self, page) -> None:
        with pytest.raises(TypeError, match="protocol must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol=True  # type: ignore[arg-type]
            )

    async def test_type_error_protocol_float(self, page) -> None:
        with pytest.raises(TypeError, match="protocol must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol=3.14  # type: ignore[arg-type]
            )

    async def test_type_error_protocol_bytes(self, page) -> None:
        with pytest.raises(TypeError, match="protocol must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol=b"x"  # type: ignore[arg-type]
            )

    async def test_type_error_protocol_list(self, page) -> None:
        with pytest.raises(TypeError, match="protocol must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", protocol=["x"]  # type: ignore[arg-type]
            )

    async def test_type_error_response_int(self, page) -> None:
        with pytest.raises(TypeError, match="response must be a dict"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", response=42  # type: ignore[arg-type]
            )

    async def test_type_error_response_bool(self, page) -> None:
        with pytest.raises(TypeError, match="response must be a dict"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", response=True  # type: ignore[arg-type]
            )

    async def test_type_error_response_list(self, page) -> None:
        with pytest.raises(TypeError, match="response must be a dict"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "respond", response=[1, 2]  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_bool(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id=True  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_float(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id=3.14  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_bytes(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id=b"f"  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_dict(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id={"a": 1}  # type: ignore[arg-type]
            )

    async def test_type_error_frame_id_list(self, page) -> None:
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(
                "decline", frame_id=["f"]  # type: ignore[arg-type]
            )

    async def test_type_error_no_cdp_call(self, page) -> None:
        with pytest.raises(TypeError, match="action must be a str"):
            await page.digital_credentials.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]

    async def test_no_spurious_methods(self, page) -> None:
        assert not hasattr(page.digital_credentials, "enable")
        assert not hasattr(page.digital_credentials, "disable")

    async def test_invalid_action_raises_value_error(self, page) -> None:
        with pytest.raises(ValueError, match="action must be"):
            await page.digital_credentials.set_virtual_wallet_behavior("invalid")

    async def test_empty_string_action_raises_value_error(self, page) -> None:
        with pytest.raises(ValueError, match="action must be"):
            await page.digital_credentials.set_virtual_wallet_behavior("")
