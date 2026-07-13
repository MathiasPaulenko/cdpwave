"""E2E tests for EventBreakpoints and Inspector domains on a real browser.

Type validation E2E tests verify that TypeError is raised before any
CDP command is sent when using a real browser session.
"""

import contextlib

import pytest

from cdpwave import CDPClient


@pytest.mark.e2e
class TestEventBreakpointsE2ETypeValidation:
    async def test_set_instrumentation_breakpoint_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(42)

    async def test_set_instrumentation_breakpoint_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(True)

    async def test_set_instrumentation_breakpoint_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    ["scriptFirstStatement"]
                )

    async def test_remove_instrumentation_breakpoint_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.remove_instrumentation_breakpoint(42)

    async def test_remove_instrumentation_breakpoint_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.remove_instrumentation_breakpoint(True)

    async def test_clear_alias_int_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.clear_instrumentation_breakpoint(42)

    async def test_set_instrumentation_breakpoint_dict_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    {"name": "test"}
                )

    async def test_set_instrumentation_breakpoint_bytes_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    b"scriptFirstStatement"
                )

    async def test_set_instrumentation_breakpoint_none_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.set_instrumentation_breakpoint(None)  # type: ignore[arg-type]

    async def test_remove_instrumentation_breakpoint_list_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.remove_instrumentation_breakpoint(
                    ["scriptFirstStatement"]
                )

    async def test_clear_alias_bool_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_name must be a string"):
                await session.event_breakpoints.clear_instrumentation_breakpoint(True)


@pytest.mark.e2e
class TestEventBreakpointsE2ELifecycle:
    async def test_set_remove_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
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
            await session.event_breakpoints.disable()

    async def test_clear_alias_works(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.clear_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )

    async def test_set_disable_remove(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.disable()
                await session.event_breakpoints.remove_instrumentation_breakpoint(
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
            await session.event_breakpoints.disable()

    async def test_type_error_no_cdp_call(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError):
                await session.event_breakpoints.set_instrumentation_breakpoint(42)
            await session.event_breakpoints.disable()


@pytest.mark.e2e
class TestInspectorE2ELifecycle:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.inspector.enable()
            await session.inspector.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.inspector.disable()

    async def test_enable_then_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.inspector.enable()
            await session.inspector.disable()
            await session.inspector.enable()
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
                for _ in range(5):
                    await session.inspector.enable()
                    await session.inspector.disable()

    async def test_enable_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.enable()

    async def test_disable_only(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.inspector.disable()
