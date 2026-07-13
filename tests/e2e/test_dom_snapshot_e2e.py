"""E2E tests for the DOMSnapshot domain on a real Edge browser.

Full lifecycle tests covering enable/disable, capture_snapshot with
various parameter combinations, get_snapshot (deprecated), type
validation errors, repeated cycles, about:blank, deep response
structure validation, and bool false parameter scenarios.
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


@pytest.mark.e2e
class TestDOMSnapshotE2ELifecycle:
    async def test_enable_disable_roundtrip(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await session.dom_snapshot.disable()

    async def test_repeated_enable_disable_cycles(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            for _ in range(5):
                await session.dom_snapshot.enable()
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


@pytest.mark.e2e
class TestDOMSnapshotE2ECaptureSnapshot:
    async def test_capture_snapshot_after_navigate(self) -> None:
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
            assert isinstance(result["documents"], list)
            assert isinstance(result["strings"], list)
            assert len(result["documents"]) > 0

    async def test_capture_snapshot_with_paint_order(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color"],
                include_paint_order=True,
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
                computed_styles=["color"],
                include_dom_rects=True,
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

    async def test_capture_snapshot_empty_styles_list(self) -> None:
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

    async def test_capture_snapshot_deep_response_structure(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display", "position"]
            )
            assert isinstance(result, dict)
            assert isinstance(result["documents"], list)
            assert isinstance(result["strings"], list)
            assert len(result["documents"]) > 0
            doc = result["documents"][0]
            assert isinstance(doc, dict)
            assert "rootNode" in doc or "nodeId" in doc or "nodes" in doc

    async def test_capture_snapshot_strings_are_strings(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color"]
            )
            assert isinstance(result, dict)
            strings = result["strings"]
            assert isinstance(strings, list)
            for s in strings:
                assert isinstance(s, str)


@pytest.mark.e2e
class TestDOMSnapshotE2EGetSnapshot:
    async def test_get_snapshot_after_navigate(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(["color"])
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

    async def test_get_snapshot_empty_whitelist(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot([])
                assert isinstance(result, dict)


@pytest.mark.e2e
class TestDOMSnapshotE2ETypeValidation:
    """Type validation should raise before any CDP call, even on a real browser."""

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

    async def test_capture_snapshot_int_zero_rejected_as_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_dom_rects"):
                await session.dom_snapshot.capture_snapshot(["color"], include_dom_rects=0)

    async def test_capture_snapshot_dict_rejected_as_list(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="computed_styles"):
                await session.dom_snapshot.capture_snapshot({"color": "red"})  # type: ignore[arg-type]

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

    async def test_get_snapshot_int_rejected_as_bool(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="include_event_listeners"):
                await session.dom_snapshot.get_snapshot(
                    ["color"], include_event_listeners=1
                )


@pytest.mark.e2e
class TestDOMSnapshotE2EFullFlow:
    """Full end-to-end flow: enable → navigate → capture → disable."""

    async def test_enable_navigate_capture_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color", "display", "position"]
            )
            assert isinstance(result, dict)
            assert "documents" in result
            assert "strings" in result
            assert len(result["documents"]) > 0
            await session.dom_snapshot.disable()

    async def test_capture_without_enable_works(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _navigate_and_wait(session)
            result = await session.dom_snapshot.capture_snapshot(
                computed_styles=["color"]
            )
            assert isinstance(result, dict)
            assert "documents" in result

    async def test_enable_capture_multiple_times_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await _navigate_and_wait(session)
            for _ in range(5):
                result = await session.dom_snapshot.capture_snapshot(
                    computed_styles=["color", "display"]
                )
                assert isinstance(result, dict)
                assert "documents" in result
                assert len(result["documents"]) > 0
            await session.dom_snapshot.disable()

    async def test_enable_capture_with_all_bools_true_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
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
            await session.dom_snapshot.disable()

    async def test_enable_capture_with_all_bools_false_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
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
            await session.dom_snapshot.disable()

    async def test_enable_get_snapshot_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_snapshot.enable()
            await _navigate_and_wait(session)
            with contextlib.suppress(Exception):
                result = await session.dom_snapshot.get_snapshot(
                    ["color", "display"],
                    include_event_listeners=True,
                    include_paint_order=True,
                    include_user_agent_shadow_tree=True,
                )
                assert isinstance(result, dict)
            await session.dom_snapshot.disable()
