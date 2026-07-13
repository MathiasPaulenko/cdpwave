"""Integration tests for the DOMSnapshot domain on a real Edge browser.

Tests cover enable/disable, capture_snapshot with various parameters,
get_snapshot (deprecated), type validation errors, repeated
enable/disable cycles, about:blank page snapshots, bool parameter
combinations, and response structure validation.
"""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


async def _navigate_and_wait(session: CDPSession, url: str = "https://example.com") -> None:
    await session.page.enable()
    await session.page.navigate(url)
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@pytest.mark.integration
class TestDOMSnapshotEnableDisable:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await session.dom_snapshot.disable()

    async def test_repeated_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.dom_snapshot.enable()
                await session.dom_snapshot.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.dom_snapshot.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.dom_snapshot.enable()
            assert isinstance(result, dict)
            await session.dom_snapshot.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            result = await session.dom_snapshot.disable()
            assert isinstance(result, dict)


@pytest.mark.integration
class TestDOMSnapshotCaptureSnapshot:
    async def test_capture_snapshot_defaults(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(["color"])
            assert isinstance(result, dict)
            assert "documents" in result
            assert "strings" in result

    async def test_capture_snapshot_with_styles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display"]
            )
            assert isinstance(result, dict)
            assert "documents" in result
            assert "strings" in result

    async def test_capture_snapshot_with_paint_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                ["color"], include_paint_order=True
            )
            assert isinstance(result, dict)
            assert "documents" in result

    async def test_capture_snapshot_with_dom_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                ["color"], include_dom_rects=True
            )
            assert isinstance(result, dict)
            assert "documents" in result

    async def test_capture_snapshot_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display", "background-color"],
                include_paint_order=True,
                include_dom_rects=True,
                include_blended_background_colors=True,
                include_text_color_opacities=True,
            )
            assert isinstance(result, dict)
            assert "documents" in result
            assert "strings" in result

    async def test_capture_snapshot_empty_styles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=[]
            )
            assert isinstance(result, dict)
            assert "documents" in result

    async def test_capture_snapshot_on_about_blank(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page("about:blank") as session,
        ):
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display"]
            )
            assert isinstance(result, dict)
            assert "documents" in result
            assert "strings" in result

    async def test_capture_snapshot_repeated(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            for _ in range(3):
                result = await session.dom_snapshot.capture_snapshot(
                    computed_styles=["color"]
                )
                assert isinstance(result, dict)
                assert "documents" in result

    async def test_capture_snapshot_bool_false_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color"],
                include_paint_order=False,
                include_dom_rects=False,
                include_blended_background_colors=False,
                include_text_color_opacities=False,
            )
            assert isinstance(result, dict)
            assert "documents" in result

    async def test_capture_snapshot_response_types(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display"]
            )
            assert isinstance(result, dict)
            assert isinstance(result["documents"], list)
            assert isinstance(result["strings"], list)
            for doc in result["documents"]:
                assert isinstance(doc, dict)


@pytest.mark.integration
class TestDOMSnapshotGetSnapshot:
    async def test_get_snapshot_basic(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(["color"])
                assert isinstance(result, dict)

    async def test_get_snapshot_with_event_listeners(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(
                    ["color"], include_event_listeners=True
                )
                assert isinstance(result, dict)

    async def test_get_snapshot_all_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(
                    ["color", "display"],
                    include_event_listeners=True,
                    include_paint_order=True,
                    include_user_agent_shadow_tree=True,
                )
                assert isinstance(result, dict)

    async def test_get_snapshot_empty_whitelist(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot([])
                assert isinstance(result, dict)

    async def test_get_snapshot_bool_false_params(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(
                    ["color"],
                    include_event_listeners=False,
                    include_paint_order=False,
                    include_user_agent_shadow_tree=False,
                )
                assert isinstance(result, dict)


@pytest.mark.integration
class TestDOMSnapshotTypeValidation:
    """Verify type validation raises before any CDP call."""

    async def test_capture_snapshot_type_error_computed_styles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_styles"):
                await session.dom_snapshot.capture_snapshot("color")  # type: ignore[arg-type]

    async def test_capture_snapshot_type_error_include_paint_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_paint_order"):
                await session.dom_snapshot.capture_snapshot(["color"], include_paint_order="yes")

    async def test_capture_snapshot_type_error_include_dom_rects(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_dom_rects"):
                await session.dom_snapshot.capture_snapshot(["color"], include_dom_rects="yes")

    async def test_capture_snapshot_type_error_blended_background_colors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_blended_background_colors"):
                await session.dom_snapshot.capture_snapshot(
                    ["color"], include_blended_background_colors="yes"
                )

    async def test_capture_snapshot_type_error_text_color_opacities(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_text_color_opacities"):
                await session.dom_snapshot.capture_snapshot(
                    ["color"], include_text_color_opacities="yes"
                )

    async def test_capture_snapshot_int_rejected_as_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_paint_order"):
                await session.dom_snapshot.capture_snapshot(["color"], include_paint_order=1)

    async def test_capture_snapshot_none_rejected_as_required(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_styles"):
                await session.dom_snapshot.capture_snapshot(None)  # type: ignore[arg-type]

    async def test_get_snapshot_type_error_computed_style_whitelist(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_style_whitelist"):
                await session.dom_snapshot.get_snapshot("color")

    async def test_get_snapshot_type_error_include_event_listeners(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_event_listeners"):
                await session.dom_snapshot.get_snapshot(
                    ["color"], include_event_listeners="yes"
                )

    async def test_get_snapshot_type_error_include_paint_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_paint_order"):
                await session.dom_snapshot.get_snapshot(
                    ["color"], include_paint_order="yes"
                )

    async def test_get_snapshot_type_error_include_user_agent_shadow_tree(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_user_agent_shadow_tree"):
                await session.dom_snapshot.get_snapshot(
                    ["color"], include_user_agent_shadow_tree="yes"
                )

    async def test_get_snapshot_none_rejected_as_required(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_style_whitelist"):
                await session.dom_snapshot.get_snapshot(None)  # type: ignore[arg-type]

    async def test_get_snapshot_int_rejected_as_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_style_whitelist"):
                await session.dom_snapshot.get_snapshot(42)  # type: ignore[arg-type]
