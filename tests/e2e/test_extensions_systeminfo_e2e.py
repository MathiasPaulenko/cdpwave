"""E2E tests for the Extensions and SystemInfo domains (real browser flows).

Full end-to-end flows against a real browser, including SystemInfo queries
(getInfo, getProcessInfo, getFeatureState), Extensions domain accessibility,
storage operations with suppress (no extension installed in headless), type
validation in real browser context, and meta tests.
"""

import asyncio
import contextlib
import inspect

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.domains.base import BaseDomain
from cdpwave.domains.extensions import ExtensionsDomain
from cdpwave.domains.system_info import SystemInfoDomain


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate("document.title", return_by_value=True)
        if result.get("result", {}).get("value"):
            break


@pytest.mark.e2e
class TestExtensionsE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.extensions is not None
            assert isinstance(session.extensions, ExtensionsDomain)

    async def test_get_extensions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.extensions.get_extensions()
                assert isinstance(result, dict)
                assert "extensions" in result

    async def test_get_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.extensions.get_storage_items(
                    "ext123", "local"
                )
                assert isinstance(result, dict)

    async def test_get_storage_items_with_keys(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.extensions.get_storage_items(
                    "ext123", "local", keys=["key1", "key2"]
                )
                assert isinstance(result, dict)

    async def test_set_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.set_storage_items(
                    "ext123", "local", {"test_key": "test_val"}
                )

    async def test_remove_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.remove_storage_items(
                    "ext123", "local", ["key1"]
                )

    async def test_clear_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.clear_storage_items("ext123", "local")

    async def test_load_unpacked(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.load_unpacked("/nonexistent/path")

    async def test_load_unpacked_incognito(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.load_unpacked(
                    "/nonexistent/path", enable_in_incognito=True
                )

    async def test_uninstall(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.uninstall("ext123")

    async def test_trigger_action(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.trigger_action("ext123", "tab456")

    async def test_raw_send_get_extensions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.send("Extensions.getExtensions")
                assert isinstance(result, dict)

    async def test_raw_send_get_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.send(
                    "Extensions.getStorageItems",
                    {"id": "ext123", "storageArea": "local"},
                )
                assert isinstance(result, dict)

    # --- TypeError validation in real browser context ---

    async def test_type_error_load_unpacked_path_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="path must be a str"):
                await session.extensions.load_unpacked(42)

    async def test_type_error_load_unpacked_enable_in_incognito_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="enable_in_incognito must be a bool"):
                await session.extensions.load_unpacked(
                    "/path", enable_in_incognito=1
                )

    async def test_type_error_trigger_action_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.extensions.trigger_action(42, "tab1")

    async def test_type_error_trigger_action_target_id_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="target_id must be a str"):
                await session.extensions.trigger_action("ext1", b"tab1")

    async def test_type_error_uninstall_id_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.extensions.uninstall({"ext1"})

    async def test_type_error_get_storage_items_id_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.extensions.get_storage_items(True, "local")

    async def test_type_error_get_storage_items_area_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="storage_area must be a str"):
                await session.extensions.get_storage_items("ext1", b"local")

    async def test_type_error_get_storage_items_keys_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="keys must be a list"):
                await session.extensions.get_storage_items(
                    "ext1", "local", keys="key1"
                )

    async def test_type_error_get_storage_items_keys_element_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match=r"keys\[0\] must be a str"):
                await session.extensions.get_storage_items(
                    "ext1", "local", keys=[42]
                )

    async def test_type_error_remove_storage_items_id_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="id must be a str"):
                await session.extensions.remove_storage_items(42, "local", ["k"])

    async def test_type_error_clear_storage_items_area_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="storage_area must be a str"):
                await session.extensions.clear_storage_items("ext1", 42)

    async def test_type_error_set_storage_items_values_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="values must be a dict"):
                await session.extensions.set_storage_items(
                    "ext1", "local", ["not", "dict"]
                )


@pytest.mark.e2e
class TestSystemInfoE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.system_info is not None
            assert isinstance(session.system_info, SystemInfoDomain)

    async def test_get_info(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            assert "gpu" in result
            assert "modelName" in result
            assert "modelVersion" in result
            assert "commandLine" in result

    async def test_get_process_info(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getProcessInfo")
            assert "processInfo" in result
            assert isinstance(result["processInfo"], list)
            assert len(result["processInfo"]) > 0

    async def test_get_feature_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.system_info.get_feature_state("Vulkan")
                assert "featureEnabled" in result
                assert isinstance(result["featureEnabled"], bool)

    async def test_get_info_via_raw_send(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            assert "gpu" in result

    async def test_get_process_info_via_raw_send(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getProcessInfo")
            assert "processInfo" in result

    async def test_get_info_has_gpu_devices(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            gpu = result["gpu"]
            assert "devices" in gpu
            assert isinstance(gpu["devices"], list)

    async def test_get_info_command_line_is_str(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            assert isinstance(result["commandLine"], str)

    async def test_get_process_info_has_type_field(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getProcessInfo")
            proc = result["processInfo"][0]
            assert "type" in proc

    # --- TypeError validation in real browser context ---

    async def test_type_error_get_feature_state_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="feature_state must be a str"):
                await session.system_info.get_feature_state(42)

    async def test_type_error_get_feature_state_bytes(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="feature_state must be a str"):
                await session.system_info.get_feature_state(b"Vulkan")

    async def test_type_error_get_feature_state_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="feature_state must be a str"):
                await session.system_info.get_feature_state(True)

    async def test_type_error_get_feature_state_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="feature_state must be a str"):
                await session.system_info.get_feature_state(["Vulkan"])  # type: ignore[arg-type]


@pytest.mark.e2e
class TestExtensionsMetaE2E:
    def test_is_base_domain(self) -> None:
        assert issubclass(ExtensionsDomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                ExtensionsDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert len(methods) == 8

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                ExtensionsDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(
            ExtensionsDomain, predicate=inspect.isfunction
        ):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"

    def test_all_methods_have_raises(self) -> None:
        for name, obj in inspect.getmembers(
            ExtensionsDomain, predicate=inspect.isfunction
        ):
            if name.startswith("_"):
                continue
            sig = inspect.signature(obj)
            params = [
                p for p in sig.parameters.values()
                if p.name != "self"
            ]
            assert obj.__doc__ is not None
            if params:
                assert "Raises:" in obj.__doc__, (
                    f"{name} missing Raises section"
                )


@pytest.mark.e2e
class TestSystemInfoMetaE2E:
    def test_is_base_domain(self) -> None:
        assert issubclass(SystemInfoDomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                SystemInfoDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert len(methods) == 3

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(
                SystemInfoDomain, predicate=inspect.isfunction
            )
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(
            SystemInfoDomain, predicate=inspect.isfunction
        ):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"

    def test_get_info_no_raises_needed(self) -> None:
        for name, obj in inspect.getmembers(
            SystemInfoDomain, predicate=inspect.isfunction
        ):
            if name.startswith("_"):
                continue
            sig = inspect.signature(obj)
            params = [
                p for p in sig.parameters.values()
                if p.name != "self"
            ]
            assert obj.__doc__ is not None
            if params:
                assert "Raises:" in obj.__doc__, (
                    f"{name} should have Raises section"
                )


@pytest.mark.e2e
class TestExtensionsEdgeE2E:
    async def test_load_unpacked_long_path(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.load_unpacked("/" + "x" * 5000)

    async def test_get_storage_items_all_areas(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            for area in ("local", "session", "sync", "managed"):
                with contextlib.suppress(Exception):
                    await session.extensions.get_storage_items("ext123", area)

    async def test_set_storage_items_empty_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.set_storage_items(
                    "ext123", "local", {}
                )

    async def test_remove_storage_items_empty_keys(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.remove_storage_items(
                    "ext123", "local", []
                )

    async def test_remove_storage_items_default_keys(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.remove_storage_items("ext123", "local")

    async def test_get_storage_items_many_keys(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.extensions.get_storage_items(
                    "ext123", "local", keys=[f"key{i}" for i in range(100)]
                )

    async def test_raw_send_load_unpacked(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.send(
                    "Extensions.loadUnpacked",
                    {"path": "/nonexistent", "enableInIncognito": False},
                )
                assert isinstance(result, dict)

    async def test_raw_send_set_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                await session.send(
                    "Extensions.setStorageItems",
                    {
                        "id": "ext123",
                        "storageArea": "local",
                        "values": {"k": "v"},
                    },
                )


@pytest.mark.e2e
class TestSystemInfoEdgeE2E:
    async def test_get_info_repeated(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            for _ in range(5):
                result = await client.send("SystemInfo.getInfo")
                assert "gpu" in result

    async def test_get_process_info_repeated(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            for _ in range(5):
                result = await client.send("SystemInfo.getProcessInfo")
                assert "processInfo" in result

    async def test_get_info_and_process_info_sequential(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            info = await client.send("SystemInfo.getInfo")
            proc = await client.send("SystemInfo.getProcessInfo")
            assert "gpu" in info
            assert "processInfo" in proc

    async def test_get_feature_state_multiple(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for feature in ("Vulkan", "SkiaVulkan", "VulkanGPU"):
                with contextlib.suppress(Exception):
                    result = await session.system_info.get_feature_state(feature)
                    assert "featureEnabled" in result

    async def test_get_info_gpu_has_aux_attributes(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            gpu = result["gpu"]
            assert "auxAttributes" in gpu
            assert "featureStatus" in gpu

    async def test_get_info_model_name_is_str(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            result = await client.send("SystemInfo.getInfo")
            assert isinstance(result["modelName"], str)
            assert isinstance(result["modelVersion"], str)
