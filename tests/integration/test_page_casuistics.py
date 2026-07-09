import asyncio

import pytest

from cdpwave import CDPSession


@pytest.mark.integration
class TestPageCasuistics:
    async def test_get_navigation_history(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        await page.page.navigate("https://example.org")
        await asyncio.sleep(1)
        
        history = await page.page.get_navigation_history()
        assert "entries" in history
        assert len(history["entries"]) >= 2

    async def test_reset_navigation_history(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.reset_navigation_history()
        assert result == {}

    async def test_navigate_to_history_entry(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        await page.page.navigate("https://example.org")
        await asyncio.sleep(1)
        
        history = await page.page.get_navigation_history()
        if len(history["entries"]) > 0:
            entry_id = history["entries"][0]["id"]
            result = await page.page.navigate_to_history_entry(entry_id)
            assert isinstance(result, dict)

    async def test_remove_script_to_evaluate_on_new_document(self, page: CDPSession) -> None:
        await page.page.enable()
        script_result = await page.page.add_script_to_evaluate_on_new_document(
            "console.log('test')"
        )
        script_id = script_result["identifier"]
        result = await page.page.remove_script_to_evaluate_on_new_document(script_id)
        assert result == {}

    async def test_get_resource_tree(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        tree = await page.page.get_resource_tree()
        assert "frameTree" in tree

    async def test_get_resource_content(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        tree = await page.page.get_resource_tree()
        frame_id = tree["frameTree"]["frame"]["id"]
        result = await page.page.get_resource_content(frame_id, "https://example.com")
        assert "content" in result or "base64Encoded" in result

    async def test_set_bypass_csp(self, page: CDPSession) -> None:
        await page.page.enable()
        result = await page.page.set_bypass_csp(True)
        assert result == {}

    async def test_set_web_lifecycle_state_active(self, page: CDPSession) -> None:
        await page.page.enable()
        result = await page.page.set_web_lifecycle_state("active")
        assert result == {}

    async def test_set_web_lifecycle_state_frozen(self, page: CDPSession) -> None:
        await page.page.enable()
        result = await page.page.set_web_lifecycle_state("frozen")
        assert result == {}

    async def test_get_app_manifest(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.get_app_manifest()
        # May not have manifest on example.com
        assert "url" in result or result == {}

    async def test_set_intercept_file_chooser_dialog(self, page: CDPSession) -> None:
        await page.page.enable()
        result = await page.page.set_intercept_file_chooser_dialog(True)
        assert result == {}

    async def test_capture_screenshot_webp_format(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.capture_screenshot(format="webp")
        assert "data" in result

    async def test_capture_screenshot_with_quality(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.capture_screenshot(format="jpeg", quality=80)
        assert "data" in result

    async def test_print_to_pdf_with_header_footer(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(display_header_footer=True)
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_custom_header(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(header_template="Test Header")
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_custom_footer(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(footer_template="Test Footer")
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_prefer_css_page_size(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(prefer_css_page_size=True)
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_scale(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(scale=0.5)
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_paper_size(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(paper_width=8.5, paper_height=11)
        assert isinstance(result, str) and len(result) > 0

    async def test_print_to_pdf_with_page_ranges(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.print_to_pdf(page_ranges="1")
        assert isinstance(result, str) and len(result) > 0

    async def test_capture_screenshot_with_clip(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        clip = {"x": 0, "y": 0, "width": 100, "height": 100, "scale": 1}
        result = await page.page.capture_screenshot(clip=clip)
        assert "data" in result

    async def test_capture_screenshot_with_from_surface(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.capture_screenshot(from_surface=False)
        assert "data" in result

    async def test_capture_screenshot_with_capture_beyond_viewport(self, page: CDPSession) -> None:
        await page.page.enable()
        await page.page.navigate("https://example.com")
        await asyncio.sleep(1)
        
        result = await page.page.capture_screenshot(capture_beyond_viewport=True)
        assert "data" in result
