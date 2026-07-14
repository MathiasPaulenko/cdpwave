"""Emulation domain: device emulation, viewport, CPU throttling, and sensors."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_SCROLLBAR_TYPES = frozenset({"default", "overlay"})
_VALID_MEDIA_TYPES = frozenset({"print", "screen", ""})
_VALID_VIRTUAL_TIME_POLICIES = frozenset({
    "advance",
    "pause",
    "pauseIfNetworkFetchesPending",
})
_VALID_VISION_DEFICIENCIES = frozenset({
    "none",
    "blurredVision",
    "reducedContrast",
    "achromatopsia",
    "deuteranopia",
    "protanopia",
    "tritanopia",
})
_VALID_DEVICE_POSTURES = frozenset({"continuous", "folded"})
_VALID_PRESSURE_STATES = frozenset({
    "nominal",
    "fair",
    "serious",
    "critical",
})
_VALID_TOUCH_CONFIGURATIONS = frozenset({"mobile", "desktop"})
_VALID_SENSOR_TYPES = frozenset({
    "accelerometer",
    "gyroscope",
    "linear-acceleration",
    "absolute-orientation",
    "relative-orientation",
    "ambient-light",
    "gravity",
    "magnetometer",
})
_VALID_PRESSURE_SOURCES = frozenset({"cpu"})


class EmulationDomain(BaseDomain):
    """Wrapper for the CDP Emulation domain.

    Provides methods for emulating devices, viewports, CPU throttling,
    sensors, and other environmental conditions.

    Events:
        - ``Emulation.screenOrientationLockChanged`` — fired when
          ``screen.orientation.lock()`` is called while device emulation
          is enabled.
        - ``Emulation.virtualTimeBudgetExpired`` — fired when the virtual
          time budget for the current VirtualTimePolicy has run out.

    Use ``session.on("Emulation.virtualTimeBudgetExpired", handler)``
    to subscribe to these events.
    """

    async def set_device_metrics_override(
        self,
        width: int,
        height: int,
        device_scale_factor: float = 1.0,
        mobile: bool = False,
        scale: float | None = None,
        screen_width: int | None = None,
        screen_height: int | None = None,
        position_x: int | None = None,
        position_y: int | None = None,
        dont_set_visible_size: bool = False,
        screen_orientation: dict[str, Any] | None = None,
        viewport: dict[str, Any] | None = None,
        scrollbar_type: str | None = None,
        screen_orientation_lock_emulation: bool = False,
    ) -> dict[str, Any]:
        """Override device metrics for the page.

        Args:
            width: Viewport width in CSS pixels.
            height: Viewport height in CSS pixels.
            device_scale_factor: Device pixel scale factor.
            mobile: Whether the device is mobile.
            scale: Scale to apply to resulting view image.
            screen_width: Screen width in CSS pixels.
            screen_height: Screen height in CSS pixels.
            position_x: Screen X position offset.
            position_y: Screen Y position offset.
            dont_set_visible_size: Do not set visible view size.
            screen_orientation: Screen orientation dict with ``type`` and
                ``angle``.
            viewport: Page viewport dict.
            scrollbar_type: Scrollbar type (``"default"``, ``"overlay"``).
            screen_orientation_lock_emulation: Enable screen orientation lock
                emulation.

        Returns:
            Response dict from the CDP command.
        """
        if isinstance(width, bool) or not isinstance(width, int):
            raise TypeError("width must be an int")
        if isinstance(height, bool) or not isinstance(height, int):
            raise TypeError("height must be an int")
        params: dict[str, Any] = {
            "width": width,
            "height": height,
            "deviceScaleFactor": device_scale_factor,
            "mobile": mobile,
            "dontSetVisibleSize": dont_set_visible_size,
            "screenOrientationLockEmulation": screen_orientation_lock_emulation,
        }
        if scale is not None:
            params["scale"] = scale
        if screen_width is not None:
            params["screenWidth"] = screen_width
        if screen_height is not None:
            params["screenHeight"] = screen_height
        if position_x is not None:
            params["positionX"] = position_x
        if position_y is not None:
            params["positionY"] = position_y
        if screen_orientation is not None:
            params["screenOrientation"] = screen_orientation
        if viewport is not None:
            params["viewport"] = viewport
        if scrollbar_type is not None:
            if not isinstance(scrollbar_type, str):
                raise TypeError("scrollbar_type must be a str or None")
            if scrollbar_type and scrollbar_type not in _VALID_SCROLLBAR_TYPES:
                raise ValueError(
                    "scrollbar_type must be 'default' or 'overlay'"
                )
            if scrollbar_type:
                params["scrollbarType"] = scrollbar_type
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
        if accept_language:
            params["acceptLanguage"] = accept_language
        if platform:
            params["platform"] = platform
        if user_agent_metadata is not None:
            params["userAgentMetadata"] = user_agent_metadata
        return await self._call("Emulation.setUserAgentOverride", params)

    async def set_cpu_throttling_rate(self, rate: float) -> dict[str, Any]:
        """Set CPU throttling rate.

        Args:
            rate: Throttling rate (1.0 = no throttling, 2.0 = 2x slower).
        """
        if not isinstance(rate, (int, float)) or isinstance(rate, bool):
            raise TypeError("rate must be a number")
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
        latitude: float | None = None,
        longitude: float | None = None,
        accuracy: float | None = None,
        altitude: float | None = None,
        altitude_accuracy: float | None = None,
        heading: float | None = None,
        speed: float | None = None,
    ) -> dict[str, Any]:
        """Override the geolocation position.

        Omitting all parameters emulates position unavailable.

        Args:
            latitude: Mock latitude.
            longitude: Mock longitude.
            accuracy: Mock accuracy.
            altitude: Mock altitude.
            altitude_accuracy: Mock altitude accuracy.
            heading: Mock heading.
            speed: Mock speed.
        """
        params: dict[str, Any] = {}
        if latitude is not None:
            params["latitude"] = latitude
        if longitude is not None:
            params["longitude"] = longitude
        if accuracy is not None:
            params["accuracy"] = accuracy
        if altitude is not None:
            params["altitude"] = altitude
        if altitude_accuracy is not None:
            params["altitudeAccuracy"] = altitude_accuracy
        if heading is not None:
            params["heading"] = heading
        if speed is not None:
            params["speed"] = speed
        return await self._call("Emulation.setGeolocationOverride", params)

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
        """Emulate CSS media type or media features.

        Args:
            media: Media type to emulate (``"print"``, ``"screen"``, ``""``
                to clear).
            features: List of media feature dicts with ``name`` and ``value``.
        """
        if media and media not in _VALID_MEDIA_TYPES:
            raise ValueError(
                "media must be 'print', 'screen', or ''"
            )
        if features is not None:
            if not isinstance(features, list):
                raise TypeError("features must be a list of dicts or None")
            for feat in features:
                if not isinstance(feat, dict):
                    raise TypeError("each feature must be a dict")
        params: dict[str, Any] = {}
        if media:
            params["media"] = media
        if features:
            params["features"] = features
        return await self._call("Emulation.setEmulatedMedia", params)

    async def clear_emulated_media(self) -> dict[str, Any]:
        """Clear all emulated media settings.

        Resets both media type and features to their defaults.
        """
        return await self._call("Emulation.setEmulatedMedia")

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
        a: float | None = None,
    ) -> dict[str, Any]:
        """Override the default background color of the page.

        If ``color`` is provided, uses it directly. Otherwise builds
        the color dict from ``r``, ``g``, ``b``, ``a``.
        If no arguments are provided, clears the override.

        Args:
            r: Red channel (0-255).
            g: Green channel (0-255).
            b: Blue channel (0-255).
            a: Alpha channel (0-1).
            color: Pre-built color dict with ``r``, ``g``, ``b``, ``a``.
        """
        if color is None and (r is not None or g is not None or b is not None or a is not None):
            color = {
                    "r": r if r is not None else 0,
                    "g": g if g is not None else 0,
                    "b": b if b is not None else 0,
                    "a": a if a is not None else 1.0,
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

        Uses ``set_default_background_color_override`` with no color,
        which resets the override in modern Chrome.
        """
        return await self._call(
            "Emulation.setDefaultBackgroundColorOverride",
            {},
        )

    async def set_idle_override(
        self,
        is_user_active: bool,
        is_screen_unlocked: bool,
    ) -> dict[str, Any]:
        """Override the idle state.

        Args:
            is_user_active: Whether the user is active.
            is_screen_unlocked: Whether the screen is unlocked.
        """
        return await self._call(
            "Emulation.setIdleOverride",
            {
                "isUserActive": is_user_active,
                "isScreenUnlocked": is_screen_unlocked,
            },
        )

    async def clear_idle_override(self) -> dict[str, Any]:
        """Clear the idle state override.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Emulation.clearIdleOverride")

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

    async def set_locale_override(self, locale: str = "") -> dict[str, Any]:
        """Override the system locale.

        If ``locale`` is empty, clears the override and restores the
        default host system locale.

        Args:
            locale: Locale string (e.g. ``"en-US"``, ``"es-ES"``).
        """
        params: dict[str, Any] = {}
        if locale:
            params["locale"] = locale
        return await self._call("Emulation.setLocaleOverride", params)

    async def set_sensor_override_readings(
        self,
        type: str,
        reading: dict[str, Any],
    ) -> dict[str, Any]:
        """Override sensor readings.

        Args:
            type: Sensor type (``"accelerometer"``, ``"gyroscope"``,
                ``"linear-acceleration"``, ``"absolute-orientation"``,
                ``"relative-orientation"``, ``"ambient-light"``,
                ``"gravity"``, ``"magnetometer"``).
            reading: Sensor reading dict. Format depends on sensor type:
                ``{"xyz": {"x": 1.0, "y": 0.0, "z": 9.8}}`` for
                accelerometer/gyroscope/gravity/magnetometer/linear-acceleration,
                ``{"single": {"value": 100.0}}`` for ambient-light,
                ``{"quaternion": {"x": 0, "y": 0, "z": 0, "w": 1}}``
                for absolute/relative orientation.
        """
        if not isinstance(type, str):
            raise TypeError("type must be a str")
        if type not in _VALID_SENSOR_TYPES:
            raise ValueError(
                f"type must be one of {sorted(_VALID_SENSOR_TYPES)}"
            )
        return await self._call(
            "Emulation.setSensorOverrideReadings",
            {"type": type, "reading": reading},
        )

    async def set_page_scale_factor(self, page_scale_factor: float) -> dict[str, Any]:
        """Set the page scale factor for the current page.

        Args:
            page_scale_factor: Scale factor (1.0 = default).
        """
        if not isinstance(page_scale_factor, (int, float)) or isinstance(page_scale_factor, bool):
            raise TypeError("page_scale_factor must be a number")
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

        .. deprecated::
            This command is deprecated in the CDP spec. Use
            ``set_device_metrics_override`` instead.

        Args:
            width: Frame width in DIP (Device Independent Pixels).
            height: Frame height in DIP (Device Independent Pixels).
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
        configuration: str | None = None,
    ) -> dict[str, Any]:
        """Emit touch events for mouse events.

        Args:
            enabled: Whether to emit touch events for mouse.
            configuration: ``"mobile"`` or ``"desktop"``. If not specified,
                defaults to current platform.
        """
        params: dict[str, Any] = {"enabled": enabled}
        if configuration is not None:
            if not isinstance(configuration, str):
                raise TypeError("configuration must be a str or None")
            if configuration and configuration not in _VALID_TOUCH_CONFIGURATIONS:
                raise ValueError(
                    "configuration must be 'mobile' or 'desktop'"
                )
            if configuration:
                params["configuration"] = configuration
        return await self._call("Emulation.setEmitTouchEventsForMouse", params)

    async def set_auto_dark_mode_override(
        self,
        enabled: bool = False,
    ) -> dict[str, Any]:
        """Override the auto dark mode setting.

        Args:
            enabled: Whether to enable auto dark mode. ``False`` clears
                any existing override.
        """
        return await self._call(
            "Emulation.setAutoDarkModeOverride",
            {"enabled": enabled},
        )

    async def clear_auto_dark_mode_override(self) -> dict[str, Any]:
        """Clear the auto dark mode override.

        Removes the auto dark mode override by calling
        ``setAutoDarkModeOverride`` with ``enabled=False``.

        Returns:
            Response dict from the CDP.
        """
        return await self._call(
            "Emulation.setAutoDarkModeOverride",
            {"enabled": False},
        )

    async def set_navigator_overrides(
        self,
        platform: str,
    ) -> dict[str, Any]:
        """Override the navigator platform.

        .. deprecated::
            This command is deprecated in the CDP spec.

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
        budget: float | None = None,
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
        if not isinstance(policy, str):
            raise TypeError("policy must be a str")
        if policy not in _VALID_VIRTUAL_TIME_POLICIES:
            raise ValueError(
                "policy must be 'advance', 'pause', or "
                "'pauseIfNetworkFetchesPending'"
            )
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

        Args:
            type: Vision deficiency to emulate (``"none"``,
                ``"blurredVision"``, ``"reducedContrast"``,
                ``"achromatopsia"``, ``"deuteranopia"``,
                ``"protanopia"``, ``"tritanopia"``).
        """
        if not isinstance(type, str):
            raise TypeError("type must be a str")
        if type not in _VALID_VISION_DEFICIENCIES:
            raise ValueError(
                "type must be 'none', 'blurredVision', 'reducedContrast', "
                "'achromatopsia', 'deuteranopia', 'protanopia', or 'tritanopia'"
            )
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

    async def can_emulate(self) -> dict[str, Any]:
        """Check if emulation is supported.

        .. deprecated::
            This command is deprecated in the CDP spec.

        Returns:
            Dict with ``result`` boolean.
        """
        return await self._call("Emulation.canEmulate")

    async def reset_page_scale_factor(self) -> dict[str, Any]:
        """Reset the page scale factor to its default."""
        return await self._call("Emulation.resetPageScaleFactor")

    async def set_safe_area_insets_override(
        self,
        top: int | None = None,
        left: int | None = None,
        bottom: int | None = None,
        right: int | None = None,
        top_max: int | None = None,
        left_max: int | None = None,
        bottom_max: int | None = None,
        right_max: int | None = None,
    ) -> dict[str, Any]:
        """Override safe area insets.

        Unset values will cause the respective env variables to be
        undefined, even if previously overridden.

        Args:
            top: Top safe area inset in CSS pixels.
            left: Left safe area inset in CSS pixels.
            bottom: Bottom safe area inset in CSS pixels.
            right: Right safe area inset in CSS pixels.
            top_max: Max top safe area inset in CSS pixels.
            left_max: Max left safe area inset in CSS pixels.
            bottom_max: Max bottom safe area inset in CSS pixels.
            right_max: Max right safe area inset in CSS pixels.
        """
        insets: dict[str, Any] = {}
        if top is not None:
            insets["top"] = top
        if left is not None:
            insets["left"] = left
        if bottom is not None:
            insets["bottom"] = bottom
        if right is not None:
            insets["right"] = right
        if top_max is not None:
            insets["topMax"] = top_max
        if left_max is not None:
            insets["leftMax"] = left_max
        if bottom_max is not None:
            insets["bottomMax"] = bottom_max
        if right_max is not None:
            insets["rightMax"] = right_max
        return await self._call(
            "Emulation.setSafeAreaInsetsOverride",
            {"insets": insets},
        )

    async def set_device_posture_override(
        self,
        posture: str,
    ) -> dict[str, Any]:
        """Override device posture.

        Args:
            posture: Device posture (``"continuous"``, ``"folded"``).
        """
        if not isinstance(posture, str):
            raise TypeError("posture must be a str")
        if posture not in _VALID_DEVICE_POSTURES:
            raise ValueError("posture must be 'continuous' or 'folded'")
        return await self._call(
            "Emulation.setDevicePostureOverride",
            {"posture": {"type": posture}},
        )

    async def clear_device_posture_override(self) -> dict[str, Any]:
        """Clear device posture override."""
        return await self._call("Emulation.clearDevicePostureOverride")

    async def set_display_features_override(
        self,
        features: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Override display features (e.g. hinges, cutouts).

        Args:
            features: List of display feature dicts with
                ``orientation``, ``offset``, ``maskLength``.
        """
        return await self._call(
            "Emulation.setDisplayFeaturesOverride",
            {"features": features},
        )

    async def clear_display_features_override(self) -> dict[str, Any]:
        """Clear display features override."""
        return await self._call("Emulation.clearDisplayFeaturesOverride")

    async def set_emulated_os_text_scale(
        self,
        scale: float = 0.0,
    ) -> dict[str, Any]:
        """Override the OS-level text scaling factor.

        Args:
            scale: Text scaling factor (1.0 = default). ``0`` clears
                the override.
        """
        params: dict[str, Any] = {}
        if scale is not None:
            params["scale"] = scale
        return await self._call(
            "Emulation.setEmulatedOSTextScale",
            params,
        )

    async def set_sensor_override_enabled(
        self,
        enabled: bool,
        type: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Enable or disable sensor override for a specific sensor type.

        Unlike ``set_sensor_override_readings``, this only toggles the
        override without setting specific values.

        Args:
            enabled: Whether to enable the sensor override.
            type: Sensor type (``"accelerometer"``, ``"gyroscope"``,
                ``"linear-acceleration"``, ``"absolute-orientation"``,
                ``"relative-orientation"``, ``"ambient-light"``,
                ``"gravity"``, ``"magnetometer"``).
            metadata: Optional sensor metadata dict.
        """
        if not isinstance(type, str):
            raise TypeError("type must be a str")
        if type not in _VALID_SENSOR_TYPES:
            raise ValueError(
                f"type must be one of {sorted(_VALID_SENSOR_TYPES)}"
            )
        params: dict[str, Any] = {"enabled": enabled, "type": type}
        if metadata is not None:
            params["metadata"] = metadata
        return await self._call(
            "Emulation.setSensorOverrideEnabled",
            params,
        )

    async def get_overridden_sensor_information(
        self,
        type: str,
    ) -> dict[str, Any]:
        """Get information about an overridden sensor.

        Args:
            type: Sensor type to query.

        Returns:
            Dict with ``requestedSamplingFrequency``.
        """
        if not isinstance(type, str):
            raise TypeError("type must be a str")
        if type not in _VALID_SENSOR_TYPES:
            raise ValueError(
                f"type must be one of {sorted(_VALID_SENSOR_TYPES)}"
            )
        return await self._call(
            "Emulation.getOverriddenSensorInformation",
            {"type": type},
        )

    async def set_pressure_source_override_enabled(
        self,
        source: str,
        enabled: bool,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Enable or disable pressure source override.

        Args:
            source: Pressure source (``"cpu"``).
            enabled: Whether to enable the override.
            metadata: Optional metadata dict.
        """
        if not isinstance(source, str):
            raise TypeError("source must be a str")
        if source not in _VALID_PRESSURE_SOURCES:
            raise ValueError("source must be 'cpu'")
        params: dict[str, Any] = {"source": source, "enabled": enabled}
        if metadata is not None:
            params["metadata"] = metadata
        return await self._call(
            "Emulation.setPressureSourceOverrideEnabled",
            params,
        )

    async def set_pressure_state_override(
        self,
        source: str,
        state: str,
    ) -> dict[str, Any]:
        """Override pressure state for a source.

        Args:
            source: Pressure source (``"cpu"``).
            state: Pressure state (``"nominal"``, ``"fair"`,
                ``"serious"``, ``"critical"``).
        """
        if not isinstance(source, str):
            raise TypeError("source must be a str")
        if source not in _VALID_PRESSURE_SOURCES:
            raise ValueError("source must be 'cpu'")
        if not isinstance(state, str):
            raise TypeError("state must be a str")
        if state not in _VALID_PRESSURE_STATES:
            raise ValueError(
                "state must be 'nominal', 'fair', 'serious', or 'critical'"
            )
        return await self._call(
            "Emulation.setPressureStateOverride",
            {"source": source, "state": state},
        )

    async def set_disabled_image_types(
        self,
        image_types: list[str],
    ) -> dict[str, Any]:
        """Disable specific image types from loading.

        Args:
            image_types: List of image types to disable (e.g.
                ``["avif", "webp", "jxl"]``).
        """
        return await self._call(
            "Emulation.setDisabledImageTypes",
            {"imageTypes": image_types},
        )

    async def set_data_saver_override(self, enabled: bool) -> dict[str, Any]:
        """Override Data Saver mode.

        Args:
            enabled: Whether Data Saver is enabled.
        """
        return await self._call(
            "Emulation.setDataSaverOverride",
            {"dataSaverEnabled": enabled},
        )

    async def set_hardware_concurrency_override(
        self,
        hardware_concurrency: int,
    ) -> dict[str, Any]:
        """Override ``navigator.hardwareConcurrency``.

        Args:
            hardware_concurrency: Number of logical CPU cores to report.
        """
        return await self._call(
            "Emulation.setHardwareConcurrencyOverride",
            {"hardwareConcurrency": hardware_concurrency},
        )

    async def set_automation_override(self, enabled: bool) -> dict[str, Any]:
        """Override the automation flag (``navigator.webdriver``).

        Args:
            enabled: If True, sets ``navigator.webdriver`` to ``true``.
        """
        return await self._call(
            "Emulation.setAutomationOverride",
            {"enabled": enabled},
        )

    async def set_small_viewport_height_difference_override(
        self,
        difference: int,
    ) -> dict[str, Any]:
        """Override the small viewport height difference.

        Args:
            difference: Pixels difference between 100svh and 100lvh.
        """
        return await self._call(
            "Emulation.setSmallViewportHeightDifferenceOverride",
            {"difference": difference},
        )

    async def get_screen_infos(self) -> dict[str, Any]:
        """Get information about all screens.

        Returns:
            Dict with ``screenInfos`` list.
        """
        return await self._call("Emulation.getScreenInfos")

    async def add_screen(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        work_area_insets: dict[str, Any] | None = None,
        device_pixel_ratio: float | None = None,
        rotation: int | None = None,
        color_depth: int | None = None,
        label: str | None = None,
        is_internal: bool = False,
    ) -> dict[str, Any]:
        """Add a virtual screen.

        Args:
            left: Offset of the left edge in pixels.
            top: Offset of the top edge in pixels.
            width: Screen width in pixels.
            height: Screen height in pixels.
            work_area_insets: Screen work area insets dict.
            device_pixel_ratio: Device pixel ratio (default 1).
            rotation: Rotation angle (0, 90, 180, 270).
            color_depth: Color depth in bits (default 24).
            label: Descriptive label for the screen.
            is_internal: Whether the screen is internal.

        Returns:
            Dict with ``screenInfo``.
        """
        params: dict[str, Any] = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "isInternal": is_internal,
        }
        if work_area_insets is not None:
            params["workAreaInsets"] = work_area_insets
        if device_pixel_ratio is not None:
            params["devicePixelRatio"] = device_pixel_ratio
        if rotation is not None:
            params["rotation"] = rotation
        if color_depth is not None:
            params["colorDepth"] = color_depth
        if label is not None:
            params["label"] = label
        return await self._call("Emulation.addScreen", params)

    async def update_screen(
        self,
        screen_id: str,
        left: int | None = None,
        top: int | None = None,
        width: int | None = None,
        height: int | None = None,
        work_area_insets: dict[str, Any] | None = None,
        device_pixel_ratio: float | None = None,
        rotation: int | None = None,
        color_depth: int | None = None,
        label: str | None = None,
        is_internal: bool = False,
    ) -> dict[str, Any]:
        """Update a virtual screen.

        Args:
            screen_id: Screen ID to update.
            left: Offset of the left edge in pixels.
            top: Offset of the top edge in pixels.
            width: New width in pixels.
            height: New height in pixels.
            work_area_insets: Screen work area insets dict.
            device_pixel_ratio: Device pixel ratio.
            rotation: Rotation angle (0, 90, 180, 270).
            color_depth: Color depth in bits.
            label: New screen label.
            is_internal: Whether the screen is internal.

        Returns:
            Dict with ``screenInfo``.
        """
        params: dict[str, Any] = {
            "screenId": screen_id,
            "isInternal": is_internal,
        }
        if left is not None:
            params["left"] = left
        if top is not None:
            params["top"] = top
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if work_area_insets is not None:
            params["workAreaInsets"] = work_area_insets
        if device_pixel_ratio is not None:
            params["devicePixelRatio"] = device_pixel_ratio
        if rotation is not None:
            params["rotation"] = rotation
        if color_depth is not None:
            params["colorDepth"] = color_depth
        if label is not None:
            params["label"] = label
        return await self._call("Emulation.updateScreen", params)

    async def remove_screen(self, screen_id: str) -> dict[str, Any]:
        """Remove a virtual screen.

        Args:
            screen_id: Screen ID to remove.
        """
        return await self._call(
            "Emulation.removeScreen",
            {"screenId": screen_id},
        )

    async def set_primary_screen(self, screen_id: str) -> dict[str, Any]:
        """Set the primary screen.

        Args:
            screen_id: Screen ID to set as primary.
        """
        return await self._call(
            "Emulation.setPrimaryScreen",
            {"screenId": screen_id},
        )
