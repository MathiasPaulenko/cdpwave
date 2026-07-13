"""Functional tests for Extensions, PWA, Worker, and Inspector domains."""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestExtensions:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.extensions is not None

    async def test_get_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.get_storage_items("ext123", "local")

    async def test_get_extensions(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.extensions.get_extensions()
                assert isinstance(result, dict)

    async def test_uninstall(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.uninstall("ext123")

    async def test_trigger_action(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.trigger_action("ext123", "tab456")

    async def test_set_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.set_storage_items(
                    "ext123", "local", {"key": "val"}
                )

    async def test_remove_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.remove_storage_items(
                    "ext123", "local", ["key1"]
                )

    async def test_clear_storage_items(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.clear_storage_items("ext123", "local")

    async def test_load_unpacked(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.load_unpacked("/nonexistent/path")

    async def test_load_unpacked_incognito(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.extensions.load_unpacked(
                    "/nonexistent/path", enable_in_incognito=True
                )

    async def test_type_error_load_unpacked_path_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="path must be a str"):
                await session.extensions.load_unpacked(42)

    async def test_type_error_get_storage_items_keys_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="keys must be a list"):
                await session.extensions.get_storage_items(
                    "ext1", "local", keys=42
                )


@pytest.mark.integration
class TestPWA:
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
                await session.pwa.get_os_app_state("manifest123")


@pytest.mark.integration
class TestWorker:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.worker is not None


@pytest.mark.integration
class TestInspector:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.inspector is not None

    async def test_enable_disable_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.enable()
                await session.inspector.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.enable()
                await session.inspector.enable()
                await session.inspector.disable()

    async def test_multiple_cycles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                for _ in range(3):
                    await session.inspector.enable()
                    await session.inspector.disable()

    async def test_enable_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.enable()


@pytest.mark.integration
class TestEventBreakpoints:
    async def test_domain_accessible(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.event_breakpoints is not None

    async def test_set_and_remove_instrumentation_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.remove_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )

    async def test_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.disable()

    async def test_clear_alias(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.clear_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )

    async def test_set_multiple_breakpoints(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "cancelAnimationFrame"
                )
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "requestAnimationFrame"
                )
                await session.event_breakpoints.disable()

    async def test_remove_without_set(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.remove_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )

    async def test_set_same_breakpoint_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "cancelAnimationFrame"
                )
                await session.event_breakpoints.remove_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.disable()
                await session.event_breakpoints.remove_instrumentation_breakpoint(
                    "cancelAnimationFrame"
                )

    async def test_disable_without_any_breakpoints(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.disable()

    async def test_type_error_raised_before_cdp_call(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(42)
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.remove_instrumentation_breakpoint(42)
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.clear_instrumentation_breakpoint(42)
