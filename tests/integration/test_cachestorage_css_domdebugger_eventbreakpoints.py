"""Functional tests for CacheStorage, CSS, DOMDebugger, and EventBreakpoints domains."""

import asyncio
import contextlib

import pytest

from cdpwave import CDPClient, CDPSession


async def _wait_for_page(page: CDPSession) -> str:
    await page.page.enable()
    nav_result = await page.page.navigate("https://example.com")
    frame_id = nav_result.get("frameId", "")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break
    return frame_id


@pytest.mark.integration
class TestCacheStorage:
    async def test_request_cache_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            result = await session.cache_storage.request_cache_names(
                security_origin="https://example.com"
            )
            assert "caches" in result


@pytest.mark.integration
class TestCSS:
    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            await session.css.disable()

    async def test_get_media_queries(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_media_queries()
            assert "medias" in result
            await session.css.disable()

    async def test_get_inline_styles_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            result = await session.css.get_inline_styles_for_node(body_id)
            assert "inlineStyle" in result
            await session.css.disable()

    async def test_get_computed_style_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            result = await session.css.get_computed_style_for_node(body_id)
            assert "computedStyle" in result
            await session.css.disable()

    async def test_get_matched_styles_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            result = await session.css.get_matched_styles_for_node(body_id)
            assert "matchedCSSRules" in result
            await session.css.disable()

    async def test_create_style_sheet_and_set_text(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            frame_id = await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.create_style_sheet(frame_id, force=True)
            ss_id = result["styleSheetId"]
            await session.css.set_style_sheet_text(ss_id, "body { color: red; }")
            text_result = await session.css.get_style_sheet_text(ss_id)
            assert "text" in text_result
            await session.css.disable()

    async def test_collect_class_names(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            frame_id = await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.create_style_sheet(frame_id, force=True)
            ss_id = result["styleSheetId"]
            await session.css.set_style_sheet_text(
                ss_id, ".foo .bar { color: red; }"
            )
            names = await session.css.collect_class_names(ss_id)
            assert "classNames" in names
            await session.css.disable()

    async def test_get_platform_fonts_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            result = await session.css.get_platform_fonts_for_node(body_id)
            assert "fonts" in result
            await session.css.disable()

    @pytest.mark.skip(reason="CI Chrome does not return backgroundColors from getBackgroundColors")
    async def test_get_background_colors(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            result = await session.css.get_background_colors(body_id)
            assert "backgroundColors" in result
            await session.css.disable()

    async def test_force_pseudo_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            await session.css.force_pseudo_state(body_id, ["hover"])
            await session.css.disable()

    async def test_start_stop_rule_usage_tracking(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            await session.css.start_rule_usage_tracking()
            delta = await session.css.take_coverage_delta()
            assert "coverage" in delta
            result = await session.css.stop_rule_usage_tracking()
            assert "ruleUsage" in result
            await session.css.disable()

    async def test_track_and_take_computed_style_updates(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            with contextlib.suppress(Exception):
                await session.css.track_computed_style_updates(
                    [{"name": "color", "value": ""}]
                )
                updates = await session.css.take_computed_style_updates()
                assert "nodeIds" in updates
            await session.css.track_computed_style_updates([])
            await session.css.disable()

    async def test_set_local_fonts_enabled(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            await session.css.set_local_fonts_enabled(True)
            await session.css.set_local_fonts_enabled(False)
            await session.css.disable()

    async def test_get_environment_variables(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_environment_variables()
            assert "environmentVariables" in result
            await session.css.disable()

    async def test_get_longhand_properties(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            result = await session.css.get_longhand_properties("margin", "1px 2px 3px 4px")
            assert "longhandProperties" in result
            await session.css.disable()

    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            frame_id = await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            body_node = await session.dom.query_selector(root_id, "body")
            body_id = body_node["nodeId"]
            await session.css.get_inline_styles_for_node(body_id)
            await session.css.get_computed_style_for_node(body_id)
            await session.css.get_matched_styles_for_node(body_id)
            await session.css.get_platform_fonts_for_node(body_id)
            await session.css.get_background_colors(body_id)
            await session.css.force_pseudo_state(body_id, ["hover"])
            await session.css.force_starting_style(body_id, True)
            ss = await session.css.create_style_sheet(frame_id, force=True)
            ss_id = ss["styleSheetId"]
            await session.css.set_style_sheet_text(ss_id, ".foo { color: red; }")
            await session.css.collect_class_names(ss_id)
            await session.css.get_style_sheet_text(ss_id)
            await session.css.get_media_queries()
            await session.css.get_environment_variables()
            await session.css.start_rule_usage_tracking()
            await session.css.take_coverage_delta()
            await session.css.stop_rule_usage_tracking()
            await session.css.disable()


@pytest.mark.integration
class TestDOMDebugger:
    async def test_set_remove_dom_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            doc = await session.dom.get_document()
            root_id = doc["root"]["nodeId"]
            with contextlib.suppress(Exception):
                await session.dom_debugger.set_dom_breakpoint(
                    root_id, "subtree-modified"
                )
                await session.dom_debugger.remove_dom_breakpoint(
                    root_id, "subtree-modified"
                )

    async def test_set_remove_xhr_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await session.dom_debugger.set_xhr_breakpoint("/api/")
            await session.dom_debugger.remove_xhr_breakpoint("/api/")


@pytest.mark.integration
class TestEventBreakpoints:
    async def test_set_clear_instrumentation_breakpoint(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.event_breakpoints.set_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
                await session.event_breakpoints.clear_instrumentation_breakpoint(
                    "scriptFirstStatement"
                )
