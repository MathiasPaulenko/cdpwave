"""E2E tests for Preload and DeviceAccess domains.

These tests launch a real browser and exercise domain methods
end-to-end against a live Chrome instance.
"""

import contextlib
import inspect

import pytest

from cdpwave import CDPClient
from cdpwave.domains.device_access import DeviceAccessDomain
from cdpwave.domains.preload import PreloadDomain


@pytest.mark.e2e
class TestPreloadE2E:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                await session.preload.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.preload.enable()
                assert isinstance(result, dict)
                await session.preload.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.preload.enable()
                result = await session.preload.disable()
                assert isinstance(result, dict)

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.preload is not None
            assert isinstance(session.preload, PreloadDomain)

    async def test_raw_send_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("Preload.enable")
                await session.send("Preload.disable")

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(PreloadDomain)
            if not m.startswith("_") and callable(getattr(PreloadDomain, m))
        ]
        assert len(methods) == 2

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(PreloadDomain)
            if not m.startswith("_") and callable(getattr(PreloadDomain, m))
        ]
        assert methods == ["disable", "enable"]

    async def test_all_methods_are_coroutines(self) -> None:
        for name in ("disable", "enable"):
            method = getattr(PreloadDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_class_docstring_has_experimental(self) -> None:
        doc = PreloadDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_module_docstring_has_types_and_events(self) -> None:
        import cdpwave.domains.preload as mod
        doc = mod.__doc__
        assert "Types:" in doc
        assert "Events:" in doc

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

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(PreloadDomain, "get_preload_policy")
        assert not hasattr(PreloadDomain, "set_preload_policy")

    async def test_enable_no_params_sent(self) -> None:
        methods = [
            m for m in dir(PreloadDomain)
            if not m.startswith("_") and callable(getattr(PreloadDomain, m))
        ]
        assert "enable" in methods
        sig = inspect.signature(PreloadDomain.enable)
        params = [k for k in sig.parameters if k != "self"]
        assert len(params) == 0

    async def test_disable_no_params_sent(self) -> None:
        sig = inspect.signature(PreloadDomain.disable)
        params = [k for k in sig.parameters if k != "self"]
        assert len(params) == 0

    async def test_class_docstring_has_description(self) -> None:
        doc = PreloadDomain.__doc__
        assert doc is not None
        assert "speculative loading" in doc

    async def test_module_docstring_has_description(self) -> None:
        import cdpwave.domains.preload as mod
        doc = mod.__doc__
        assert "speculative loading" in doc
        assert "prefetching" in doc

    async def test_enable_docstring_no_activates_text(self) -> None:
        doc = PreloadDomain.enable.__doc__
        assert doc is not None
        assert "Activates" not in doc
        assert "Must be called" not in doc

    async def test_disable_docstring_no_deactivates_text(self) -> None:
        doc = PreloadDomain.disable.__doc__
        assert doc is not None
        assert "Deactivates" not in doc

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        assert issubclass(PreloadDomain, BaseDomain)


@pytest.mark.e2e
class TestDeviceAccessE2E:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                await session.device_access.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.device_access.enable()
                assert isinstance(result, dict)
                await session.device_access.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.device_access.enable()
                result = await session.device_access.disable()
                assert isinstance(result, dict)

    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.device_access is not None
            assert isinstance(session.device_access, DeviceAccessDomain)

    async def test_cancel_prompt_type_validation(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt(123)

    async def test_select_prompt_type_validation_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(123, "dev1")

    async def test_select_prompt_type_validation_device_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="device_id must be a str"):
                await session.device_access.select_prompt("req1", 456)

    async def test_raw_send_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("DeviceAccess.enable")
                await session.send("DeviceAccess.disable")

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(DeviceAccessDomain)
            if not m.startswith("_") and callable(getattr(DeviceAccessDomain, m))
        ]
        assert len(methods) == 4

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(DeviceAccessDomain)
            if not m.startswith("_") and callable(getattr(DeviceAccessDomain, m))
        ]
        assert methods == ["cancel_prompt", "disable", "enable", "select_prompt"]

    async def test_all_methods_are_coroutines(self) -> None:
        for name in ("cancel_prompt", "disable", "enable", "select_prompt"):
            method = getattr(DeviceAccessDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_class_docstring_has_experimental(self) -> None:
        doc = DeviceAccessDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_module_docstring_has_types_and_events(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "Types:" in doc
        assert "Events:" in doc

    # --- edge case tests ---

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

    async def test_cancel_prompt_list_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt(["req1"])

    async def test_cancel_prompt_dict_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.cancel_prompt({"id": "req1"})

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

    async def test_select_prompt_list_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.device_access.select_prompt(["req1"], "dev1")

    async def test_select_prompt_dict_device_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="device_id must be a str"):
                await session.device_access.select_prompt("req1", {"id": "dev1"})

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

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(DeviceAccessDomain, "select_bluetooth_device")

    async def test_select_prompt_signature(self) -> None:
        sig = inspect.signature(DeviceAccessDomain.select_prompt)
        params = [k for k in sig.parameters if k != "self"]
        assert params == ["id", "device_id"]

    async def test_cancel_prompt_signature(self) -> None:
        sig = inspect.signature(DeviceAccessDomain.cancel_prompt)
        params = [k for k in sig.parameters if k != "self"]
        assert params == ["id"]

    async def test_class_docstring_has_description(self) -> None:
        doc = DeviceAccessDomain.__doc__
        assert doc is not None
        assert "device access" in doc

    async def test_module_docstring_has_description(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "Bluetooth" in doc

    async def test_enable_docstring_no_activates_text(self) -> None:
        doc = DeviceAccessDomain.enable.__doc__
        assert doc is not None
        assert "Activates" not in doc
        assert "Must be called" not in doc

    async def test_disable_docstring_no_deactivates_text(self) -> None:
        doc = DeviceAccessDomain.disable.__doc__
        assert doc is not None
        assert "Deactivates" not in doc

    async def test_select_prompt_docstring_mentions_device_request_prompted(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "deviceRequestPrompted" in doc

    async def test_cancel_prompt_docstring_mentions_device_request_prompted(self) -> None:
        doc = DeviceAccessDomain.cancel_prompt.__doc__
        assert doc is not None
        assert "deviceRequestPrompted" in doc

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        assert issubclass(DeviceAccessDomain, BaseDomain)
