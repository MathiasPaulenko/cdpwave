"""E2E tests for the CSS domain."""

import asyncio

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.exceptions import CommandError


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


@pytest.mark.e2e
class TestCSSE2E:
    async def test_full_css_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            frame_id = await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()

            doc = await session.dom.get_document()
            body_id = await session.dom.query_selector(doc["root"]["nodeId"], "body")
            body_id = body_id["nodeId"]

            inline = await session.css.get_inline_styles_for_node(body_id)
            assert "inlineStyle" in inline

            computed = await session.css.get_computed_style_for_node(body_id)
            assert "computedStyle" in computed

            matched = await session.css.get_matched_styles_for_node(body_id)
            assert "matchedCSSRules" in matched

            fonts = await session.css.get_platform_fonts_for_node(body_id)
            assert "fonts" in fonts

            bg = await session.css.get_background_colors(body_id)
            assert "backgroundColors" in bg

            await session.css.force_pseudo_state(body_id, ["hover"])
            await session.css.force_starting_style(body_id, True)

            ss = await session.css.create_style_sheet(frame_id, force=True)
            ss_id = ss["styleSheetId"]
            await session.css.set_style_sheet_text(ss_id, ".foo { color: red; }")
            text_result = await session.css.get_style_sheet_text(ss_id)
            assert "text" in text_result

            names = await session.css.collect_class_names(ss_id)
            assert "classNames" in names

            medias = await session.css.get_media_queries()
            assert "medias" in medias

            env_vars = await session.css.get_environment_variables()
            assert "environmentVariables" in env_vars

            await session.css.start_rule_usage_tracking()
            delta = await session.css.take_coverage_delta()
            assert "coverage" in delta
            usage = await session.css.stop_rule_usage_tracking()
            assert "ruleUsage" in usage

            await session.css.track_computed_style_updates(
                [{"name": "color"}, {"name": "background-color"}]
            )
            updates = await session.css.take_computed_style_updates()
            assert "nodeIds" in updates
            await session.css.track_computed_style_updates([])

            await session.css.set_local_fonts_enabled(True)
            await session.css.set_local_fonts_enabled(False)

            await session.css.disable()

    async def test_css_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.css.enable()
            await session.css.disable()
            await session.css.enable()
            await session.css.disable()

    async def test_css_without_enable_raises(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with pytest.raises(CommandError):
                await session.css.get_media_queries()

    async def test_css_create_and_modify_stylesheet(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            frame_id = await _wait_for_page(session)
            await session.css.enable()

            ss = await session.css.create_style_sheet(frame_id, force=True)
            ss_id = ss["styleSheetId"]

            await session.css.set_style_sheet_text(
                ss_id, "body { color: red; margin: 1px 2px; }"
            )

            text = await session.css.get_style_sheet_text(ss_id)
            assert "color: red" in text["text"]

            longhand = await session.css.get_longhand_properties(
                "margin", "1px 2px"
            )
            assert "longhandProperties" in longhand

            await session.css.disable()

    async def test_css_track_computed_style_for_node(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.dom.enable()
            await session.css.enable()

            doc = await session.dom.get_document()
            body_id = await session.dom.query_selector(doc["root"]["nodeId"], "body")
            body_id = body_id["nodeId"]

            await session.css.track_computed_style_updates_for_node(body_id)
            await session.css.track_computed_style_updates_for_node()

            await session.css.disable()
