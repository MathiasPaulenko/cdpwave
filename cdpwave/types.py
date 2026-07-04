from collections.abc import Awaitable, Callable
from typing import Any, Literal

CommandSender = Callable[[str, dict[str, Any] | None], Awaitable[dict[str, Any]]]

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]

BrowserType = Literal["chrome", "edge", "brave", "chromium"]
