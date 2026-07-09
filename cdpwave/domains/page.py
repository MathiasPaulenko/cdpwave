"""Page domain: navigation, screenshots, and PDF generation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PageDomain(BaseDomain):
    """Wrapper for the CDP Page domain."""

    async def enable(self) -> dict[str, Any]:
        """Enable Page domain events.

        Activates reporting of page lifecycle events such as navigation,
        frame tree changes, dialog opening, and lifecycle state transitions.
        Must be called before using most other Page methods or listening
        to Page events.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable Page domain events.

        Stops reporting of page lifecycle events. All Page events will
        cease until ``enable`` is called again.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.disable")

    async def navigate(
        self,
        url: str,
        referrer: str | None = None,
        transition_type: str | None = None,
    ) -> dict[str, Any]:
        """Navigate the page to a URL.

        Args:
            url: The URL to navigate to.
            referrer: Optional referrer URL.
            transition_type: Optional transition type hint.

        Returns:
            Response dict containing ``frameId`` and ``loaderId``.
        """
        params: dict[str, Any] = {"url": url}
        if referrer is not None:
            params["referrer"] = referrer
        if transition_type is not None:
            params["transitionType"] = transition_type
        return await self._call("Page.navigate", params)

    async def reload(self, ignore_cache: bool = False) -> dict[str, Any]:
        """Reload the current page.

        Args:
            ignore_cache: If True, bypass the browser cache.
        """
        return await self._call(
            "Page.reload",
            {"ignoreCache": ignore_cache},
        )

    async def stop(self) -> dict[str, Any]:
        """Stop all pending navigations and resource loads.

        Aborts any in-progress navigation or fetch operations on the page.
        Equivalent to pressing the stop button in the browser.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.stop")

    async def capture_screenshot(
        self,
        format: str = "png",
        quality: int = 80,
        clip: dict[str, Any] | None = None,
        from_surface: bool = True,
        capture_beyond_viewport: bool = False,
    ) -> dict[str, Any]:
        """Capture a screenshot of the page.

        Args:
            format: Image format (``"png"`` or ``"jpeg"``).
            quality: JPEG quality (0-100). Ignored for PNG.
            clip: Optional clip region dict with x, y, width, height, scale.
            from_surface: Capture from the surface rather than the view.
            capture_beyond_viewport: Capture content beyond the viewport.

        Returns:
            Response dict containing base64-encoded ``data``.
        """
        if format not in ("png", "jpeg", "webp"):
            raise ValueError("format must be 'png', 'jpeg', or 'webp'")
        if not 0 <= quality <= 100:
            raise ValueError("quality must be between 0 and 100")
        params: dict[str, Any] = {
            "format": format,
            "quality": quality,
            "fromSurface": from_surface,
            "captureBeyondViewport": capture_beyond_viewport,
        }
        if clip is not None:
            params["clip"] = clip
        return await self._call("Page.captureScreenshot", params)

    async def print_to_pdf(
        self,
        landscape: bool = False,
        display_header_footer: bool = False,
        print_background: bool = False,
        scale: float = 1.0,
        paper_width: float = 8.5,
        paper_height: float = 11.0,
        margin_top: float = 0.4,
        margin_bottom: float = 0.4,
        margin_left: float = 0.4,
        margin_right: float = 0.4,
        page_ranges: str | None = None,
        header_template: str | None = None,
        footer_template: str | None = None,
        prefer_css_page_size: bool = False,
        return_as_stream: bool = False,
    ) -> str | dict[str, Any]:
        """Print the page to PDF.

        Args:
            landscape: Use landscape orientation.
            display_header_footer: Include header/footer.
            print_background: Print background graphics.
            scale: Scale factor (0.1 to 2.0).
            paper_width: Paper width in inches.
            paper_height: Paper height in inches.
            margin_top: Top margin in inches.
            margin_bottom: Bottom margin in inches.
            margin_left: Left margin in inches.
            margin_right: Right margin in inches.
            page_ranges: Optional paper ranges to print (e.g. ``"1-5, 8, 11-13"``).
            header_template: Optional HTML template for the header.
            footer_template: Optional HTML template for the footer.
            prefer_css_page_size: Use CSS page sizes over default paper size.
            return_as_stream: Return a stream handle instead of base64 data.

        Returns:
            Response dict with ``data`` (base64-encoded PDF) when
            ``return_as_stream`` is False, or response dict with
            ``stream`` handle when ``return_as_stream`` is True.
        """
        if not 0.1 <= scale <= 2.0:
            raise ValueError("scale must be between 0.1 and 2.0")
        params: dict[str, Any] = {
            "landscape": landscape,
            "displayHeaderFooter": display_header_footer,
            "printBackground": print_background,
            "scale": scale,
            "paperWidth": paper_width,
            "paperHeight": paper_height,
            "marginTop": margin_top,
            "marginBottom": margin_bottom,
            "marginLeft": margin_left,
            "marginRight": margin_right,
            "preferCSSPageSize": prefer_css_page_size,
            "transferMode": "ReturnAsStream" if return_as_stream else "ReturnAsBase64",
        }
        if page_ranges is not None:
            params["pageRanges"] = page_ranges
        if header_template is not None:
            params["headerTemplate"] = header_template
        if footer_template is not None:
            params["footerTemplate"] = footer_template
        result = await self._call("Page.printToPDF", params)
        if return_as_stream:
            return result
        return str(result.get("data", ""))

    async def get_layout_metrics(self) -> dict[str, Any]:
        """Return page layout metrics (viewport, content size)."""
        return await self._call("Page.getLayoutMetrics")

    async def go_back(self) -> dict[str, Any]:
        """Navigate to the previous page in history.

        Convenience method that uses ``get_navigation_history`` and
        ``navigate_to_history_entry`` internally.

        Returns:
            Response dict from ``Page.navigateToHistoryEntry``.
        """
        history = await self.get_navigation_history()
        idx = history.get("currentIndex", 0)
        if idx > 0:
            entries = history.get("entries", [])
            return await self.navigate_to_history_entry(entries[idx - 1]["id"])
        return {}

    async def go_forward(self) -> dict[str, Any]:
        """Navigate to the next page in history.

        Convenience method that uses ``get_navigation_history`` and
        ``navigate_to_history_entry`` internally.

        Returns:
            Response dict from ``Page.navigateToHistoryEntry``.
        """
        history = await self.get_navigation_history()
        idx = history.get("currentIndex", 0)
        entries = history.get("entries", [])
        if idx < len(entries) - 1:
            return await self.navigate_to_history_entry(entries[idx + 1]["id"])
        return {}

    async def get_navigation_history(self) -> dict[str, Any]:
        """Return the navigation history of the page.

        Contains the current entry index and a list of all navigation
        entries, each with URL, title, and transition type.

        Returns:
            Response dict with ``currentIndex`` and ``entries`` list.
        """
        return await self._call("Page.getNavigationHistory")

    async def reset_navigation_history(self) -> dict[str, Any]:
        """Reset the navigation history of the page.

        Clears all navigation entries, effectively removing the ability
        to navigate back or forward. The current page remains loaded.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.resetNavigationHistory")

    async def navigate_to_history_entry(self, entry_id: int) -> dict[str, Any]:
        """Navigate to a specific history entry.

        Args:
            entry_id: Navigation entry ID from ``get_navigation_history``.
        """
        return await self._call(
            "Page.navigateToHistoryEntry",
            {"entryId": entry_id},
        )

    async def add_script_to_evaluate_on_new_document(
        self,
        source: str,
        world_name: str | None = None,
        run_immediately: bool = False,
    ) -> dict[str, Any]:
        """Add a script to evaluate on every new document.

        The script runs before any other scripts on the page. Useful for
        injecting polyfills, overriding APIs, or setting up test harnesses.

        Args:
            source: JavaScript source code to inject.
            world_name: Optional isolated world name to run the script in.
            run_immediately: If True, run the script immediately in existing documents.

        Returns:
            Dict with ``identifier`` — save it to remove the script later.
        """
        params: dict[str, Any] = {"source": source}
        if world_name is not None:
            params["worldName"] = world_name
        if run_immediately:
            params["runImmediately"] = True
        return await self._call("Page.addScriptToEvaluateOnNewDocument", params)

    async def remove_script_to_evaluate_on_new_document(
        self,
        identifier: str,
    ) -> dict[str, Any]:
        """Remove a previously added script.

        Args:
            identifier: Script identifier from ``add_script_to_evaluate_on_new_document``.
        """
        return await self._call(
            "Page.removeScriptToEvaluateOnNewDocument",
            {"identifier": identifier},
        )

    async def get_frame_tree(self) -> dict[str, Any]:
        """Get the frame tree of the current page.

        Returns:
            Dict with ``frameTree`` containing the root frame and its children.
        """
        return await self._call("Page.getFrameTree")

    async def get_resource_tree(self) -> dict[str, Any]:
        """Get the resource tree of the current page.

        Returns:
            Dict with ``frameTree`` containing frames and their resources.
        """
        return await self._call("Page.getResourceTree")

    async def get_resource_content(
        self,
        frame_id: str,
        url: str,
    ) -> dict[str, Any]:
        """Get the content of a resource by URL.

        Args:
            frame_id: Frame ID containing the resource.
            url: URL of the resource.

        Returns:
            Dict with ``content`` (base64 or text) and ``base64Encoded`` flag.
        """
        return await self._call(
            "Page.getResourceContent",
            {"frameId": frame_id, "url": url},
        )

    async def set_bypass_csp(self, enabled: bool) -> dict[str, Any]:
        """Enable or disable Content Security Policy bypass.

        When enabled, the page will not enforce CSP rules. Useful for
        testing and injecting scripts on sites with strict CSP.

        Args:
            enabled: Whether to bypass CSP.
        """
        return await self._call("Page.setBypassCSP", {"enabled": enabled})

    async def crash(self) -> dict[str, Any]:
        """Crash the renderer process.

        Useful for testing crash recovery and error handling.
        """
        return await self._call("Page.crash")

    async def close(self) -> dict[str, Any]:
        """Close the page.

        This is equivalent to closing the tab in the browser.
        """
        return await self._call("Page.close")

    async def bring_to_front(self) -> dict[str, Any]:
        """Bring the page to the front and focus it.

        Raises the browser window and switches to the tab containing
        this page. Equivalent to clicking the tab in the browser UI.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.bringToFront")

    async def set_web_lifecycle_state(self, state: str) -> dict[str, Any]:
        """Set the web lifecycle state of the page.

        Args:
            state: ``"frozen"`` or ``"active"``.
        """
        if state not in ("frozen", "active"):
            raise ValueError("state must be 'frozen' or 'active'")
        return await self._call(
            "Page.setWebLifecycleState",
            {"state": state},
        )

    async def handle_java_script_dialog(
        self,
        accept: bool,
        prompt_text: str | None = None,
    ) -> dict[str, Any]:
        """Accept or dismiss a JavaScript dialog (alert, confirm, prompt).

        Args:
            accept: Whether to accept the dialog.
            prompt_text: Text to enter in a prompt dialog.
        """
        params: dict[str, Any] = {"accept": accept}
        if prompt_text is not None:
            params["promptText"] = prompt_text
        return await self._call("Page.handleJavaScriptDialog", params)

    handle_javascript_dialog = handle_java_script_dialog

    async def get_app_manifest(self) -> dict[str, Any]:
        """Get the web app manifest for the current page.

        Returns:
            Dict with ``url``, ``data``, ``errors``, and ``parsed`` keys.
        """
        return await self._call("Page.getAppManifest")

    async def create_isolated_world(
        self,
        frame_id: str,
        world_name: str | None = None,
        grant_universal_access: bool = False,
    ) -> dict[str, Any]:
        """Create an isolated world for the given frame.

        Args:
            frame_id: Frame ID to create the world in.
            world_name: Optional name for the isolated world.
            grant_universal_access: Whether to grant universal access.

        Returns:
            Dict with ``executionContextId``.
        """
        params: dict[str, Any] = {"frameId": frame_id}
        if world_name is not None:
            params["worldName"] = world_name
        if grant_universal_access:
            params["grantUniversalAccess"] = True
        return await self._call("Page.createIsolatedWorld", params)

    async def set_document_content(
        self,
        frame_id: str,
        html: str,
    ) -> dict[str, Any]:
        """Set the HTML content of a frame.

        Args:
            frame_id: Frame ID to set content for.
            html: HTML content to set.
        """
        return await self._call(
            "Page.setDocumentContent",
            {"frameId": frame_id, "html": html},
        )

    async def set_intercept_file_chooser_dialog(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable file chooser dialog interception.

        When enabled, ``Page.fileChooserOpened`` events will be emitted
        instead of the native file dialog.

        Args:
            enabled: Whether to intercept file chooser dialogs.
        """
        return await self._call(
            "Page.setInterceptFileChooserDialog",
            {"enabled": enabled},
        )

    async def capture_snapshot(
        self,
        format: str = "mhtml",
    ) -> dict[str, Any]:
        """Capture a snapshot of the page as MHTML.

        Args:
            format: Snapshot format (``"mhtml"``).

        Returns:
            Dict with ``data`` containing the MHTML content.
        """
        return await self._call("Page.captureSnapshot", {"format": format})
