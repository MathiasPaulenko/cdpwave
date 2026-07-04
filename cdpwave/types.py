"""Type aliases used across cdpwave."""

from collections.abc import Awaitable, Callable
from typing import Any, Literal

CommandSender = Callable[[str, dict[str, Any] | None], Awaitable[dict[str, Any]]]
"""Callable that sends a CDP command and awaits the response dict."""

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]
"""Async callable that receives CDP event params."""

BrowserType = Literal["chrome", "edge", "brave", "chromium"]
"""Supported Chromium-based browser types."""
