"""HeadlessExperimental domain: headless mode control (experimental)."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_SCREENSHOT_FORMATS = frozenset({"jpeg", "png", "webp"})


class HeadlessExperimentalDomain(BaseDomain):
    """Wrapper for the CDP HeadlessExperimental domain.

    Provides control over headless frame scheduling for testing
    viewport-dependent behavior in headless mode.

    Note: This entire domain is **experimental**.
    """

    async def begin_frame(
        self,
        frame_time_ticks: float | None = None,
        interval: float | None = None,
        no_display_updates: bool | None = None,
        screenshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a BeginFrame to the target and return when the frame was completed.

        Optionally captures a screenshot from the resulting frame. Requires
        that the target was created with enabled BeginFrameControl.

        Args:
            frame_time_ticks: Timestamp of this BeginFrame in Renderer
                TimeTicks (milliseconds of uptime). If not set, the current
                time will be used.
            interval: The interval between BeginFrames reported to the
                compositor, in milliseconds. Defaults to ~16.666 ms (60 fps).
            no_display_updates: Whether updates should not be committed and
                drawn onto the display. False by default.
            screenshot: Screenshot capture options. Dict with optional
                ``format`` (``"jpeg"``, ``"png"``, ``"webp"``),
                ``quality`` (int 0-100), and ``optimizeForSpeed`` (bool).

        Returns:
            Dict with ``hasDamage`` (bool) and optional ``screenshotData``
            (base64-encoded image data).
        """
        params: dict[str, Any] = {}
        if frame_time_ticks is not None:
            if isinstance(frame_time_ticks, bool) or not isinstance(
                frame_time_ticks, (int, float)
            ):
                raise TypeError("frame_time_ticks must be a number or None")
            params["frameTimeTicks"] = frame_time_ticks
        if interval is not None:
            if isinstance(interval, bool) or not isinstance(
                interval, (int, float)
            ):
                raise TypeError("interval must be a number or None")
            params["interval"] = interval
        if no_display_updates is not None:
            if not isinstance(no_display_updates, bool):
                raise TypeError(
                    "no_display_updates must be a bool or None"
                )
            params["noDisplayUpdates"] = no_display_updates
        if screenshot is not None:
            if not isinstance(screenshot, dict):
                raise TypeError("screenshot must be a dict or None")
            if "format" in screenshot:
                fmt = screenshot["format"]
                if not isinstance(fmt, str):
                    raise TypeError("screenshot['format'] must be a str")
                if fmt not in _VALID_SCREENSHOT_FORMATS:
                    raise ValueError(
                        f"screenshot['format'] must be one of "
                        f"{sorted(_VALID_SCREENSHOT_FORMATS)}, "
                        f"got {fmt!r}"
                    )
            params["screenshot"] = screenshot
        return await self._call("HeadlessExperimental.beginFrame", params)

    async def enable(self) -> dict[str, Any]:
        """Enable the HeadlessExperimental domain.

        .. deprecated::
            Marked as deprecated in the CDP specification.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeadlessExperimental.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the HeadlessExperimental domain.

        .. deprecated::
            Marked as deprecated in the CDP specification.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("HeadlessExperimental.disable")
