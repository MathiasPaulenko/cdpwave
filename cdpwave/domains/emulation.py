"""Emulation domain: device emulation, viewport, CPU throttling, and sensors."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class EmulationDomain(BaseDomain):
    """Wrapper for the CDP Emulation domain.

    Provides methods for emulating devices, viewports, CPU throttling,
    sensors, and other environmental conditions.
    """

    async def set_device_metrics_override(
        self,
        width: int,
        height: int,
        device_scale_factor: float = 1.0,
        mobile: bool = False,
        screen_width: int | None = None,
        screen_height: int | None = None,
        position_x: int | None = None,
        position_y: int | None = None,
        user_agent: str | None = None,
        screen_orientation: dict[str, Any] | None = None,
        viewport: dict[str, Any] | None = None,
        display_feature: dict[str, Any] | None = None,
        device_posture: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Override device metrics for the page.

        Args:
            width: Viewport width in CSS pixels.
            height: Viewport height in CSS pixels.
            device_scale_factor: Device pixel scale factor.
            mobile: Whether the device is mobile.
            screen_width: Screen width in CSS pixels.
            screen_height: Screen height in CSS pixels.
            position_x: Screen X position offset.
            position_y: Screen Y position offset.
            user_agent: User agent string override.
            screen_orientation: Screen orientation dict with ``type`` and
                ``angle``.
            viewport: Page viewport dict.
            display_feature: Display feature dict (e.g. hinge).
            device_posture: Device posture dict.

        Returns:
            Response dict from the CDP command.
        """
        params: dict[str, Any] = {
            "width": width,
            "height": height,
            "deviceScaleFactor": device_scale_factor,
            "mobile": mobile,
        }
        if screen_width is not None:
            params["screenWidth"] = screen_width
        if screen_height is not None:
            params["screenHeight"] = screen_height
        if position_x is not None:
            params["positionX"] = position_x
        if position_y is not None:
            params["positionY"] = position_y
        if user_agent is not None:
            params["userAgent"] = user_agent
        if screen_orientation is not None:
            params["screenOrientation"] = screen_orientation
        if viewport is not None:
            params["viewport"] = viewport
        if display_feature is not None:
            params["displayFeature"] = {
                "orientation": display_feature.get("orientation", display_feature.get("Orientation", "")),
                "offset": display_feature.get("offset", display_feature.get("Offset", 0)),
                "maskLength": display_feature.get("maskLength", display_feature.get("mask_length", 0)),
                "maskThickness": display_feature.get("maskThickness", display_feature.get("mask_thickness", 0)),
            }
        if device_posture is not None:
            params["devicePosture"] = device_posture
        return await self._call("Emulation.setDeviceMetricsOverride", params)

    async def clear_device_metrics_override(self) -> dict[str, Any]:
        """Clear any overridden device metrics.

        Removes the device metrics override set by
        ``set_device_metrics_override``, restoring the real device
        metrics.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.clearDeviceMetricsOverride")

    async def set_user_agent_override(
        self,
        user_agent: str,
        accept_language: str | None = None,
        platform: str | None = None,
        user_agent_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Override the browser user agent.

        Args:
            user_agent: The user agent string to use.
            accept_language: Accept-Language header value.
            platform: Platform string.
            user_agent_metadata: Client hints metadata dict.

        Returns:
            Response dict from the CDP command.
        """
        params: dict[str, Any] = {"userAgent": user_agent}
        if accept_language is not None:
            params["acceptLanguage"] = accept_language
        if platform is not None:
            params["platform"] = platform
        if user_agent_metadata is not None:
            params["userAgentMetadata"] = user_agent_metadata
        return await self._call("Emulation.setUserAgentOverride", params)

    async def set_cpu_throttling_rate(self, rate: float) -> dict[str, Any]:
        """Set CPU throttling rate.

        Args:
            rate: Throttling rate (1.0 = no throttling, 2.0 = 2x slower).
        """
        return await self._call(
            "Emulation.setCPUThrottlingRate",
            {"rate": rate},
        )

    async def set_script_execution_disabled(self, disabled: bool) -> dict[str, Any]:
        """Disable or enable script execution in the page.

        Args:
            disabled: Whether to disable script execution.
        """
        return await self._call(
            "Emulation.setScriptExecutionDisabled",
            {"value": disabled},
        )

    async def set_geolocation_override(
        self,
        latitude: float,
        longitude: float,
        accuracy: float = 100.0,
    ) -> dict[str, Any]:
        """Override the geolocation position.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            accuracy: Accuracy in meters.
        """
        return await self._call(
            "Emulation.setGeolocationOverride",
            {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
            },
        )

    async def clear_geolocation_override(self) -> dict[str, Any]:
        """Clear any overridden geolocation.

        Removes the geolocation override set by
        ``set_geolocation_override``, restoring the real device
        location.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.clearGeolocationOverride")

    async def set_touch_emulation_enabled(
        self,
        enabled: bool,
        max_touch_points: int | None = None,
    ) -> dict[str, Any]:
        """Enable or disable touch emulation.

        Args:
            enabled: Whether to enable touch emulation.
            max_touch_points: Maximum number of touch points supported.
        """
        params: dict[str, Any] = {"enabled": enabled}
        if max_touch_points is not None:
            params["maxTouchPoints"] = max_touch_points
        return await self._call("Emulation.setTouchEmulationEnabled", params)

    async def set_emulated_media(
        self,
        media: str = "",
        features: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Emulate CSS media features.

        Args:
            media: Media type to emulate (``"print"``, ``"screen"``, ``""``
                to clear).
            features: List of media feature dicts with ``name`` and ``value``.
        """
        params: dict[str, Any] = {"media": media}
        if features is not None:
            params["features"] = features
        return await self._call("Emulation.setEmulatedMedia", params)

    async def clear_emulated_media(self) -> dict[str, Any]:
        """Clear all emulated media settings.

        Resets both media type and features to their defaults.
        """
        return await self._call("Emulation.setEmulatedMedia", {"media": ""})

    async def set_emulated_media_feature(
        self,
        name: str,
        value: str,
    ) -> dict[str, Any]:
        """Set a single CSS media feature.

        Convenience method for the common case of setting one media
        feature (e.g. ``prefers-color-scheme``).

        Args:
            name: Media feature name (e.g. ``"prefers-color-scheme"``).
            value: Media feature value (e.g. ``"dark"``, ``"light"``).
        """
        return await self.set_emulated_media(
            features=[{"name": name, "value": value}],
        )

    async def set_default_background_color_override(
        self,
        color: dict[str, Any] | None = None,
        r: int | None = None,
        g: int | None = None,
        b: int | None = None,
        a: int | None = None,
    ) -> dict[str, Any]:
        """Override the default background color of the page.

        If ``color`` is provided, uses it directly. Otherwise builds
        the color dict from ``r``, ``g``, ``b``, ``a`` (0-255 range).
        If no arguments are provided, clears the override.

        Args:
            r: Red channel (0-255).
            g: Green channel (0-255).
            b: Blue channel (0-255).
            a: Alpha channel (0-255).
            color: Pre-built color dict with ``r``, ``g``, "b", ``a``.
        """
        if color is None and (r is not None or g is not None or b is not None or a is not None):
            color = {
                    "r": r if r is not None else 0,
                    "g": g if g is not None else 0,
                    "b": b if b is not None else 0,
                    "a": a if a is not None else 255,
                }
        params: dict[str, Any] = {}
        if color is not None:
            params["color"] = color
        return await self._call(
            "Emulation.setDefaultBackgroundColorOverride",
            params,
        )

    async def clear_default_background_color_override(self) -> dict[str, Any]:
        """Clear the default background color override.

        .. deprecated::
            ``Emulation.clearDefaultBackgroundColorOverride`` was removed
            in modern Chrome. Use ``set_default_background_color_override``
            with no arguments to clear the override.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.clearDefaultBackgroundColorOverride")

    async def set_idle_override(
        self,
        is_user_active: bool,
        is_screen_active: bool,
    ) -> dict[str, Any]:
        """Override the idle state.

        .. deprecated::
            ``Emulation.setIdleOverride`` was removed in Chrome 120+.
            This method may return ``CommandError`` on modern Chrome.
            Use ``set_emulated_idle_state`` instead if available.

        Args:
            is_user_active: Whether the user is active.
            is_screen_active: Whether the screen is unlocked.
        """
        return await self._call(
            "Emulation.setIdleOverride",
            {
                "isUserActive": is_user_active,
                "isScreenActive": is_screen_active,
            },
        )

    async def clear_idle_override(self) -> dict[str, Any]:
        """Clear the idle state override.

        .. deprecated::
            ``Emulation.clearIdleOverride`` was removed in Chrome 120+.
            This method may return ``CommandError`` on modern Chrome.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.clearIdleOverride")

    async def set_disabled_sensors(self, disabled: bool) -> dict[str, Any]:
        """Disable or enable device sensors.

        .. deprecated::
            ``Emulation.setDisabledSensors`` was removed in modern Chrome.
            This method may return ``CommandError``.

        Args:
            disabled: Whether to disable sensors.
        """
        return await self._call(
            "Emulation.setDisabledSensors",
            {"disabled": disabled},
        )

    async def set_timezone_override(self, timezone_id: str) -> dict[str, Any]:
        """Override the system timezone.

        Args:
            timezone_id: IANA timezone ID (e.g. ``"America/New_York"``).
        """
        return await self._call(
            "Emulation.setTimezoneOverride",
            {"timezoneId": timezone_id},
        )

    async def clear_timezone_override(self) -> dict[str, Any]:
        """Clear the timezone override.

        Removes the timezone override set by ``set_timezone_override``,
        restoring the system timezone.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Emulation.setTimezoneOverride",
            {"timezoneId": ""},
        )

    async def set_locale_override(self, locale: str) -> dict[str, Any]:
        """Override the system locale.

        Args:
            locale: Locale string (e.g. ``"en-US"``, ``"es-ES"``).
        """
        return await self._call(
            "Emulation.setLocaleOverride",
            {"locale": locale},
        )

    async def set_sensor_override_readings(
        self,
        type: str,
        reading: dict[str, Any],
    ) -> dict[str, Any]:
        """Override sensor readings.

        Args:
            type: Sensor type (``"accelerometer"``, ``"gyroscope"``,
                ``"linear-accelerometer"``, ``"absolute-orientation"``,
                ``"relative-orientation"``).
            reading: Sensor reading dict (e.g. ``{"x": 0, "y": 0, "z": 0}``).
        """
        return await self._call(
            "Emulation.setSensorOverrideReadings",
            {"type": type, "reading": reading},
        )

    async def clear_sensor_override_readings(self, type: str) -> dict[str, Any]:
        """Clear sensor override readings for a specific sensor type.

        Args:
            type: Sensor type to clear.
        """
        return await self._call(
            "Emulation.clearSensorOverrideReadings",
            {"type": type},
        )

    async def set_page_scale_factor(self, page_scale_factor: float) -> dict[str, Any]:
        """Set the page scale factor for the current page.

        Args:
            page_scale_factor: Scale factor (1.0 = default).
        """
        return await self._call(
            "Emulation.setPageScaleFactor",
            {"pageScaleFactor": page_scale_factor},
        )

    async def set_visible_size(
        self,
        width: int,
        height: int,
    ) -> dict[str, Any]:
        """Set the visible size of the page.

        Args:
            width: Width in CSS pixels.
            height: Height in CSS pixels.
        """
        return await self._call(
            "Emulation.setVisibleSize",
            {"width": width, "height": height},
        )

    async def set_scrollbars_hidden(self, hidden: bool) -> dict[str, Any]:
        """Hide or show scrollbars.

        Args:
            hidden: Whether to hide scrollbars.
        """
        return await self._call(
            "Emulation.setScrollbarsHidden",
            {"hidden": hidden},
        )

    async def set_javascript_disabled(self, disabled: bool) -> dict[str, Any]:
        """Disable or enable JavaScript execution.

        Args:
            disabled: Whether to disable JavaScript.
        """
        return await self._call(
            "Emulation.setJavaScriptDisabled",
            {"disabled": disabled},
        )

    async def set_document_cookie_disabled(self, disabled: bool) -> dict[str, Any]:
        """Disable or enable document.cookie access.

        Args:
            disabled: Whether to disable document.cookie.
        """
        return await self._call(
            "Emulation.setDocumentCookieDisabled",
            {"disabled": disabled},
        )

    async def set_emit_touch_events_for_mouse(
        self,
        enabled: bool,
        configuration: str = "mobile",
    ) -> dict[str, Any]:
        """Emit touch events for mouse events.

        Args:
            enabled: Whether to emit touch events for mouse.
            configuration: ``"mobile"`` or ``"desktop"``.
        """
        return await self._call(
            "Emulation.setEmitTouchEventsForMouse",
            {"enabled": enabled, "configuration": configuration},
        )

    async def set_auto_dark_mode_override(
        self,
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Override the auto dark mode setting.

        Args:
            enabled: Whether to enable auto dark mode. If not specified,
                any existing override will be cleared.
        """
        params: dict[str, Any] = {}
        if enabled is not None:
            params["enabled"] = enabled
        return await self._call(
            "Emulation.setAutoDarkModeOverride",
            params,
        )

    async def clear_auto_dark_mode_override(self) -> dict[str, Any]:
        """Clear the auto dark mode override.

        Removes the auto dark mode override by calling
        ``setAutoDarkModeOverride`` with no enabled parameter.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.setAutoDarkModeOverride")

    async def set_navigator_overrides(
        self,
        platform: str,
    ) -> dict[str, Any]:
        """Override the navigator platform.

        Args:
            platform: The platform string navigator.platform should return.
        """
        return await self._call(
            "Emulation.setNavigatorOverrides",
            {"platform": platform},
        )

    async def set_virtual_time_policy(
        self,
        policy: str,
        budget: int | None = None,
        max_virtual_time_task_starvation_count: int | None = None,
        initial_virtual_time: float | None = None,
    ) -> dict[str, Any]:
        """Turn on virtual time for all frames.

        Replaces real-time with a synthetic time source and sets the
        current virtual time policy.

        Args:
            policy: Virtual time policy (``"advance"``, ``"pause"``,
                ``"pauseIfNetworkFetchesPending"``).
            budget: After this many virtual milliseconds have elapsed,
                virtual time will be paused.
            max_virtual_time_task_starvation_count: Maximum number of tasks
                that can be run before virtual is forced forwards.
            initial_virtual_time: Base time that will be initially returned.

        Returns:
            Dict with ``virtualTimeTicksBase``.
        """
        params: dict[str, Any] = {"policy": policy}
        if budget is not None:
            params["budget"] = budget
        if max_virtual_time_task_starvation_count is not None:
            params["maxVirtualTimeTaskStarvationCount"] = max_virtual_time_task_starvation_count
        if initial_virtual_time is not None:
            params["initialVirtualTime"] = initial_virtual_time
        return await self._call("Emulation.setVirtualTimePolicy", params)

    async def set_focus_emulation_enabled(
        self,
        enabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable simulating a focused and active page.

        .. deprecated::
            ``Emulation.setFocusEmulationEnabled`` was removed in modern
            Chrome. This method may return ``CommandError``.

        Args:
            enabled: Whether to enable or disable focus emulation.
        """
        return await self._call(
            "Emulation.setFocusEmulationEnabled",
            {"enabled": enabled},
        )

    async def set_emulated_vision_deficiency(
        self,
        type: str,
    ) -> dict[str, Any]:
        """Emulate a vision deficiency.

        .. deprecated::
            ``Emulation.setEmulatedVisionDeficiency`` was removed in
            modern Chrome. This method may return ``CommandError``.

        Args:
            type: Vision deficiency to emulate (``"none"``,
                ``"blurredVision"``, ``"reducedContrast"``,
                ``"achromatopsia"``, ``"deuteranopia"``,
                ``"protanopia"``, ``"tritanopia"``).
        """
        return await self._call(
            "Emulation.setEmulatedVisionDeficiency",
            {"type": type},
        )

    async def clear_emulated_vision_deficiency(self) -> dict[str, Any]:
        """Clear the emulated vision deficiency.

        Resets the vision deficiency to ``"none"``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Emulation.setEmulatedVisionDeficiency",
            {"type": "none"},
        )

    async def set_scroll_position(
        self,
        x: float = 0,
        y: float = 0,
    ) -> dict[str, Any]:
        """Set the scroll position for the current page.

        .. deprecated::
            ``Emulation.setScrollPositionOverride`` was removed in
            modern Chrome. This method may return ``CommandError``.

        Args:
            x: Horizontal scroll position.
            y: Vertical scroll position.
        """
        return await self._call(
            "Emulation.setScrollPositionOverride",
            {"x": x, "y": y},
        )
