"""Page domain: navigation, screenshots, and PDF generation."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_DOWNLOAD_BEHAVIORS = frozenset({"allow", "deny", "default"})


class PageDomain(BaseDomain):
    """Wrapper for the CDP Page domain."""

    async def enable(
        self,
        enable_file_chooser_opened_event: bool | None = None,
    ) -> dict[str, Any]:
        """Enable Page domain events.

        Activates reporting of page lifecycle events such as navigation,
        frame tree changes, dialog opening, and lifecycle state transitions.
        Must be called before using most other Page methods or listening
        to Page events.

        Args:
            enable_file_chooser_opened_event: If True, emit
                ``Page.fileChooserOpened`` events.

        Returns:
            Response dict from the CDP.
        """
        params: dict[str, Any] = {}
        if enable_file_chooser_opened_event is not None:
            params["enableFileChooserOpenedEvent"] = enable_file_chooser_opened_event
        return await self._call(
            "Page.enable",
            params if params else None,
        )

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
        frame_id: str | None = None,
        referrer_policy: str | None = None,
    ) -> dict[str, Any]:
        """Navigate the page to a URL.

        Args:
            url: The URL to navigate to.
            referrer: Optional referrer URL.
            transition_type: Optional transition type hint.
            frame_id: Optional frame ID to navigate within.
            referrer_policy: Optional referrer policy.

        Returns:
            Response dict containing ``frameId`` and ``loaderId``.
            Typed as ``PageNavigateResult`` for autocompletion.
        """
        params: dict[str, Any] = {"url": url}
        if referrer is not None:
            params["referrer"] = referrer
        if transition_type is not None:
            valid_transitions = {
                "link", "typed", "address_bar", "auto_bookmark",
                "auto_subframe", "manual_subframe", "generated",
                "auto_toplevel", "form_submit", "reload", "keyword",
                "keyword_generated", "other",
            }
            if transition_type not in valid_transitions:
                raise ValueError(
                    f"transition_type must be one of {sorted(valid_transitions)}"
                )
            params["transitionType"] = transition_type
        if frame_id is not None:
            params["frameId"] = frame_id
        if referrer_policy is not None:
            valid_policies = {
                "noReferrer", "noReferrerWhenDowngrade", "origin",
                "originWhenCrossOrigin", "sameOrigin", "strictOrigin",
                "strictOriginWhenCrossOrigin", "unsafeUrl",
            }
            if referrer_policy not in valid_policies:
                raise ValueError(
                    f"referrer_policy must be one of {sorted(valid_policies)}"
                )
            params["referrerPolicy"] = referrer_policy
        return await self._call("Page.navigate", params)

    async def reload(
        self,
        ignore_cache: bool = False,
        script_to_evaluate_on_load: str | None = None,
        loader_id: str | None = None,
    ) -> dict[str, Any]:
        """Reload the current page.

        Args:
            ignore_cache: If True, bypass the browser cache.
            script_to_evaluate_on_load: Optional script to evaluate on load.
            loader_id: Optional loader ID to reload.
        """
        params: dict[str, Any] = {}
        if ignore_cache:
            params["ignoreCache"] = True
        if script_to_evaluate_on_load is not None:
            params["scriptToEvaluateOnLoad"] = script_to_evaluate_on_load
        if loader_id is not None:
            params["loaderId"] = loader_id
        return await self._call(
            "Page.reload",
            params if params else None,
        )

    async def stop(self) -> dict[str, Any]:
        """Stop all pending navigations and resource loads.

        Aborts any in-progress navigation or fetch operations on the page.
        Equivalent to pressing the stop button in the browser.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Page.stopLoading")

    async def capture_screenshot(
        self,
        format: str = "png",
        quality: int = 80,
        clip: dict[str, Any] | None = None,
        from_surface: bool = True,
        capture_beyond_viewport: bool = False,
        optimize_for_speed: bool | None = None,
    ) -> dict[str, Any]:
        """Capture a screenshot of the page.

        Args:
            format: Image format (``"png"``, ``"jpeg"``, or ``"webp"``).
            quality: JPEG/WebP quality (0-100). Ignored for PNG.
            clip: Optional clip region dict with x, y, width, height, scale.
            from_surface: Capture from the surface rather than the view.
            capture_beyond_viewport: Capture content beyond the viewport.
            optimize_for_speed: Optimize screenshot for speed over quality.

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
        if optimize_for_speed is not None:
            params["optimizeForSpeed"] = optimize_for_speed
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
        generate_tagged_pdf: bool | None = None,
        generate_document_outline: bool | None = None,
    ) -> dict[str, Any]:
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
            generate_tagged_pdf: Whether to generate a tagged PDF.
            generate_document_outline: Whether to generate a document outline.

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
        if generate_tagged_pdf is not None:
            params["generateTaggedPDF"] = generate_tagged_pdf
        if generate_document_outline is not None:
            params["generateDocumentOutline"] = generate_document_outline
        return await self._call("Page.printToPDF", params)

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
        include_command_line_api: bool | None = None,
        run_immediately: bool = False,
    ) -> dict[str, Any]:
        """Add a script to evaluate on every new document.

        The script runs before any other scripts on the page. Useful for
        injecting polyfills, overriding APIs, or setting up test harnesses.

        Args:
            source: JavaScript source code to inject.
            world_name: Optional isolated world name to run the script in.
            include_command_line_api: Whether to include the command line API.
            run_immediately: If True, run the script immediately in existing documents.

        Returns:
            Dict with ``identifier`` — save it to remove the script later.
        """
        params: dict[str, Any] = {"source": source}
        if world_name is not None:
            params["worldName"] = world_name
        if include_command_line_api is not None:
            params["includeCommandLineAPI"] = include_command_line_api
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

    async def get_app_manifest(
        self,
        manifest_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the web app manifest for the current page.

        Args:
            manifest_id: Optional manifest ID to retrieve.

        Returns:
            Dict with ``url``, ``data``, ``errors``, and ``parsed`` keys.
        """
        params: dict[str, Any] = {}
        if manifest_id is not None:
            params["manifestId"] = manifest_id
        return await self._call(
            "Page.getAppManifest",
            params if params else None,
        )

    async def create_isolated_world(
        self,
        frame_id: str,
        world_name: str | None = None,
        grant_universal_access: bool = False,
        content_security_policy: str | None = None,
    ) -> dict[str, Any]:
        """Create an isolated world for the given frame.

        Args:
            frame_id: Frame ID to create the world in.
            world_name: Optional name for the isolated world.
            grant_universal_access: Whether to grant universal access.
            content_security_policy: Optional CSP for the isolated world.

        Returns:
            Dict with ``executionContextId``.
        """
        params: dict[str, Any] = {"frameId": frame_id}
        if world_name is not None:
            params["worldName"] = world_name
        if grant_universal_access:
            params["grantUniveralAccess"] = True
        if content_security_policy is not None:
            params["contentSecurityPolicy"] = content_security_policy
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
        cancel: bool | None = None,
    ) -> dict[str, Any]:
        """Enable or disable file chooser dialog interception.

        When enabled, ``Page.fileChooserOpened`` events will be emitted
        instead of the native file dialog.

        Args:
            enabled: Whether to intercept file chooser dialogs.
            cancel: Whether to cancel the dialog instead of showing it.
        """
        params: dict[str, Any] = {"enabled": enabled}
        if cancel is not None:
            params["cancel"] = cancel
        return await self._call("Page.setInterceptFileChooserDialog", params)

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
        if format not in ("mhtml",):
            raise ValueError("format must be 'mhtml'")
        return await self._call("Page.captureSnapshot", {"format": format})

    async def stop_loading(self) -> dict[str, Any]:
        """Force the page to stop loading."""
        return await self._call("Page.stopLoading")

    async def set_lifecycle_events_enabled(self, enabled: bool) -> dict[str, Any]:
        """Enable or disable lifecycle events.

        Args:
            enabled: Whether to emit lifecycle events.
        """
        return await self._call(
            "Page.setLifecycleEventsEnabled",
            {"enabled": enabled},
        )

    async def add_script_to_evaluate_on_load(
        self,
        source: str,
    ) -> dict[str, Any]:
        """Add a script to evaluate on page load.

        Deprecated: Use ``add_script_to_evaluate_on_new_document`` instead.

        Args:
            source: JavaScript source code to evaluate.

        Returns:
            Dict with ``identifier``.
        """
        return await self._call(
            "Page.addScriptToEvaluateOnLoad",
            {"scriptSource": source},
        )

    async def remove_script_to_evaluate_on_load(
        self,
        identifier: str,
    ) -> dict[str, Any]:
        """Remove a script previously added with ``add_script_to_evaluate_on_load``.

        Deprecated.

        Args:
            identifier: Script identifier from ``add_script_to_evaluate_on_load``.
        """
        return await self._call(
            "Page.removeScriptToEvaluateOnLoad",
            {"identifier": identifier},
        )

    async def start_screencast(
        self,
        format: str = "jpeg",
        quality: int = 80,
        max_width: int | None = None,
        max_height: int | None = None,
        every_nth_frame: int = 1,
    ) -> dict[str, Any]:
        """Start screencasting the page.

        Emits ``Page.screencastFrame`` events containing base64-encoded
        frames.

        Args:
            format: Image format (``"jpeg"`` or ``"png"``).
            quality: JPEG quality (0-100). Ignored for PNG.
            max_width: Optional max frame width in CSS pixels.
            max_height: Optional max frame height in CSS pixels.
            every_nth_frame: Capture every Nth frame (1 = every frame).
        """
        if format not in ("jpeg", "png"):
            raise ValueError("format must be 'jpeg' or 'png'")
        if not 0 <= quality <= 100:
            raise ValueError("quality must be between 0 and 100")
        params: dict[str, Any] = {
            "format": format,
            "quality": quality,
            "everyNthFrame": every_nth_frame,
        }
        if max_width is not None:
            params["maxWidth"] = max_width
        if max_height is not None:
            params["maxHeight"] = max_height
        return await self._call("Page.startScreencast", params)

    async def stop_screencast(self) -> dict[str, Any]:
        """Stop screencasting the page."""
        return await self._call("Page.stopScreencast")

    async def screencast_frame_ack(self, session_id: int) -> dict[str, Any]:
        """Acknowledge a screencast frame.

        Must be called after each ``Page.screencastFrame`` event to
        receive the next frame.

        Args:
            session_id: Session ID from the screencast frame event.
        """
        return await self._call(
            "Page.screencastFrameAck",
            {"sessionId": session_id},
        )

    async def search_in_resource(
        self,
        frame_id: str,
        url: str,
        query: str,
        case_sensitive: bool = False,
        is_regex: bool = False,
    ) -> dict[str, Any]:
        """Search within a resource content.

        Args:
            frame_id: Frame ID containing the resource.
            url: URL of the resource to search.
            query: Search query string.
            case_sensitive: Whether the search is case sensitive.
            is_regex: Whether the query is a regex.

        Returns:
            Dict with ``result`` list of matches.
        """
        params: dict[str, Any] = {
            "frameId": frame_id,
            "url": url,
            "query": query,
            "caseSensitive": case_sensitive,
            "isRegex": is_regex,
        }
        return await self._call("Page.searchInResource", params)

    async def set_device_metrics_override(
        self,
        width: int,
        height: int,
        device_scale_factor: float = 1.0,
        mobile: bool = False,
        scale: float = 1.0,
        screen_width: int | None = None,
        screen_height: int | None = None,
        position_x: int | None = None,
        position_y: int | None = None,
        dont_set_visible_size: bool = False,
        screen_orientation: dict[str, Any] | None = None,
        viewport: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Override device metrics.

        Args:
            width: Override width in CSS pixels.
            height: Override height in CSS pixels.
            device_scale_factor: Override device scale factor.
            mobile: Whether to emulate a mobile device.
            scale: Scale to apply to visible size.
            screen_width: Optional screen width override.
            screen_height: Optional screen height override.
            position_x: Optional X position override.
            position_y: Optional Y position override.
            dont_set_visible_size: If True, do not set visible size.
            screen_orientation: Optional screen orientation override.
            viewport: Optional viewport override.
        """
        params: dict[str, Any] = {
            "width": width,
            "height": height,
            "deviceScaleFactor": device_scale_factor,
            "mobile": mobile,
            "scale": scale,
        }
        if screen_width is not None:
            params["screenWidth"] = screen_width
        if screen_height is not None:
            params["screenHeight"] = screen_height
        if position_x is not None:
            params["positionX"] = position_x
        if position_y is not None:
            params["positionY"] = position_y
        if dont_set_visible_size:
            params["dontSetVisibleSize"] = True
        if screen_orientation is not None:
            params["screenOrientation"] = screen_orientation
        if viewport is not None:
            params["viewport"] = viewport
        return await self._call("Page.setDeviceMetricsOverride", params)

    async def clear_device_metrics_override(self) -> dict[str, Any]:
        """Clear device metrics override."""
        return await self._call("Page.clearDeviceMetricsOverride")

    async def set_device_orientation_override(
        self,
        alpha: float,
        beta: float,
        gamma: float,
    ) -> dict[str, Any]:
        """Override device orientation.

        Args:
            alpha: Alpha angle in degrees.
            beta: Beta angle in degrees.
            gamma: Gamma angle in degrees.
        """
        return await self._call(
            "Page.setDeviceOrientationOverride",
            {"alpha": alpha, "beta": beta, "gamma": gamma},
        )

    async def clear_device_orientation_override(self) -> dict[str, Any]:
        """Clear device orientation override."""
        return await self._call("Page.clearDeviceOrientationOverride")

    async def set_geolocation_override(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        accuracy: float | None = None,
    ) -> dict[str, Any]:
        """Override geolocation.

        All parameters are optional — calling with no arguments clears
        the override.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            accuracy: Accuracy in meters.
        """
        params: dict[str, Any] = {}
        if latitude is not None:
            params["latitude"] = latitude
        if longitude is not None:
            params["longitude"] = longitude
        if accuracy is not None:
            params["accuracy"] = accuracy
        return await self._call(
            "Page.setGeolocationOverride",
            params if params else None,
        )

    async def clear_geolocation_override(self) -> dict[str, Any]:
        """Clear geolocation override."""
        return await self._call("Page.clearGeolocationOverride")

    async def set_touch_emulation_enabled(
        self,
        enabled: bool,
        configuration: str | None = None,
    ) -> dict[str, Any]:
        """Enable or disable touch emulation.

        Args:
            enabled: Whether to enable touch emulation.
            configuration: Optional touch configuration (``"mobile"`` or
                ``"desktop"``).
        """
        params: dict[str, Any] = {"enabled": enabled}
        if configuration is not None:
            if configuration not in ("mobile", "desktop"):
                raise ValueError("configuration must be 'mobile' or 'desktop'")
            params["configuration"] = configuration
        return await self._call("Page.setTouchEmulationEnabled", params)

    async def set_download_behavior(
        self,
        behavior: str,
        download_path: str | None = None,
    ) -> dict[str, Any]:
        """Set download behavior for the page.

        Args:
            behavior: ``"allow"``, ``"deny"``, or ``"default"``.
            download_path: Path for downloads (when ``behavior`` is
                ``"allow"``).
        """
        if not isinstance(behavior, str):
            raise TypeError("behavior must be a str")
        if behavior not in _VALID_DOWNLOAD_BEHAVIORS:
            raise ValueError("behavior must be 'allow', 'deny', or 'default'")
        params: dict[str, Any] = {"behavior": behavior}
        if download_path is not None:
            params["downloadPath"] = download_path
        return await self._call("Page.setDownloadBehavior", params)

    async def set_font_families(
        self,
        font_families: dict[str, str],
        for_scripts: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Set font families override.

        Args:
            font_families: Dict mapping font family names to overrides
                (e.g. ``{"standard": "Arial"}``).
            for_scripts: Optional list of per-script font family overrides.
        """
        params: dict[str, Any] = {"fontFamilies": font_families}
        if for_scripts is not None:
            params["forScripts"] = for_scripts
        return await self._call("Page.setFontFamilies", params)

    async def set_font_sizes(
        self,
        standard: int = 16,
        fixed: int = 13,
    ) -> dict[str, Any]:
        """Set font sizes override.

        Args:
            standard: Standard font size in pixels.
            fixed: Fixed font size in pixels.
        """
        return await self._call(
            "Page.setFontSizes",
            {"fontSizes": {"standard": standard, "fixed": fixed}},
        )

    async def set_ad_blocking_enabled(self, enabled: bool) -> dict[str, Any]:
        """Enable or disable ad blocking.

        Args:
            enabled: Whether to enable ad blocking.
        """
        return await self._call(
            "Page.setAdBlockingEnabled",
            {"enabled": enabled},
        )

    async def set_prerendering_allowed(self, is_allowed: bool) -> dict[str, Any]:
        """Enable or disable prerendering.

        Args:
            is_allowed: Whether prerendering is allowed.
        """
        return await self._call(
            "Page.setPrerenderingAllowed",
            {"isAllowed": is_allowed},
        )

    async def wait_for_debugger(self) -> dict[str, Any]:
        """Pause the page until a debugger attaches."""
        return await self._call("Page.waitForDebugger")

    async def generate_test_report(
        self,
        message: str,
        group: str | None = None,
    ) -> dict[str, Any]:
        """Generate a test report.

        Args:
            message: Report message.
            group: Optional report group.
        """
        params: dict[str, Any] = {"message": message}
        if group is not None:
            params["group"] = group
        return await self._call("Page.generateTestReport", params)

    async def produce_compilation_cache(
        self,
        scripts: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Produce compilation cache for scripts.

        Args:
            scripts: List of script dicts with ``url`` and optional
                ``eager`` flag.
        """
        return await self._call(
            "Page.produceCompilationCache",
            {"scripts": scripts},
        )

    async def add_compilation_cache(
        self,
        url: str,
        data: str,
    ) -> dict[str, Any]:
        """Add compilation cache for a URL.

        Args:
            url: URL of the script.
            data: Base64-encoded compilation cache data.
        """
        return await self._call(
            "Page.addCompilationCache",
            {"url": url, "data": data},
        )

    async def clear_compilation_cache(self) -> dict[str, Any]:
        """Clear the compilation cache."""
        return await self._call("Page.clearCompilationCache")

    async def set_spc_transaction_mode(self, mode: str) -> dict[str, Any]:
        """Set the SPC (Secure Payment Confirmation) transaction mode.

        Args:
            mode: One of ``"none"``, ``"autoAccept"``,
                ``"autoChooseToAuthAnotherWay"``, ``"autoReject"``,
                ``"autoOptOut"``.
        """
        valid = {
            "none", "autoAccept", "autoChooseToAuthAnotherWay",
            "autoReject", "autoOptOut",
        }
        if mode not in valid:
            raise ValueError(
                f"mode must be one of {sorted(valid)}"
            )
        return await self._call(
            "Page.setSPCTransactionMode",
            {"mode": mode},
        )

    async def set_rph_registration_mode(self, mode: str) -> dict[str, Any]:
        """Set the RPH (Register Protocol Handler) registration mode.

        Args:
            mode: One of ``"none"``, ``"autoAccept"``, ``"autoReject"``.
        """
        valid = {"none", "autoAccept", "autoReject"}
        if mode not in valid:
            raise ValueError(
                f"mode must be one of {sorted(valid)}"
            )
        return await self._call(
            "Page.setRPHRegistrationMode",
            {"mode": mode},
        )

    async def delete_cookie(
        self,
        cookie_name: str,
        url: str,
    ) -> dict[str, Any]:
        """Delete a cookie by name and URL.

        Args:
            cookie_name: Name of the cookie to delete.
            url: URL associated with the cookie.
        """
        return await self._call(
            "Page.deleteCookie",
            {"cookieName": cookie_name, "url": url},
        )

    async def get_manifest_icons(self) -> dict[str, Any]:
        """Get manifest icons for the current page.

        Returns:
            Dict with ``primaryIcon`` (base64-encoded).
        """
        return await self._call("Page.getManifestIcons")

    async def get_app_id(self) -> dict[str, Any]:
        """Get the app ID for the current page.

        Returns:
            Dict with ``appId`` and ``recommendedId``.
        """
        return await self._call("Page.getAppId")

    async def get_installability_errors(self) -> dict[str, Any]:
        """Get installability errors for the current page.

        Returns:
            Dict with ``installabilityErrors`` list.
        """
        return await self._call("Page.getInstallabilityErrors")

    async def get_ad_script_ancestry(
        self,
        frame_id: str,
    ) -> dict[str, Any]:
        """Get ad script ancestry for a frame.

        Args:
            frame_id: Frame ID to query.

        Returns:
            Dict with ``ancestry`` list.
        """
        return await self._call(
            "Page.getAdScriptAncestry",
            {"frameId": frame_id},
        )

    async def get_permissions_policy_state(
        self,
        frame_id: str,
    ) -> dict[str, Any]:
        """Get permissions policy state for a frame.

        Args:
            frame_id: Frame ID to query.

        Returns:
            Dict with ``states`` list of permission policy states.
        """
        return await self._call(
            "Page.getPermissionsPolicyState",
            {"frameId": frame_id},
        )

    async def get_origin_trials(
        self,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Get origin trials for the current page.

        Args:
            frame_id: Optional frame ID to query.

        Returns:
            Dict with ``trials`` list of origin trial descriptors.
        """
        params: dict[str, Any] = {}
        if frame_id is not None:
            params["frameId"] = frame_id
        return await self._call(
            "Page.getOriginTrials",
            params if params else None,
        )

    async def get_annotated_page_content(
        self,
        include_actionable_information: bool | None = None,
    ) -> dict[str, Any]:
        """Get annotated page content.

        Args:
            include_actionable_information: Whether to include actionable
                information in the annotated content.

        Returns:
            Dict with ``content`` containing annotated DOM tree.
        """
        params: dict[str, Any] = {}
        if include_actionable_information is not None:
            params["includeActionableInformation"] = include_actionable_information
        return await self._call(
            "Page.getAnnotatedPageContent",
            params if params else None,
        )
