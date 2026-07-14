"""HTTP discovery for Chrome DevTools Protocol endpoints."""

import asyncio
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TargetInfo:
    """Information about a CDP target (tab/page).

    Attributes:
        target_id: Unique target identifier.
        type: Target type (e.g. ``"page"``).
        title: Page title.
        url: Page URL.
        web_socket_debugger_url: Optional direct WebSocket URL for the target.
    """

    target_id: str
    type: str
    title: str
    url: str
    web_socket_debugger_url: str | None


@dataclass(frozen=True)
class VersionInfo:
    """Browser version information from ``/json/version``.

    Attributes:
        browser: Browser name and version string.
        protocol_version: CDP protocol version.
        user_agent: Browser user agent string.
        web_socket_debugger_url: Browser-level WebSocket URL.
    """

    browser: str
    protocol_version: str
    user_agent: str
    web_socket_debugger_url: str


def _http_get(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data


def _http_put(url: str) -> Any:
    req = urllib.request.Request(url, method="PUT")
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data


class TargetDiscovery:
    """HTTP-based discovery for CDP targets via ``/json/version`` and ``/json/list``."""

    def __init__(self, host: str = "localhost", port: int = 9222) -> None:
        self._base_url = f"http://{host}:{port}"

    async def get_version(self) -> VersionInfo:
        """Fetch browser version information."""
        data: dict[str, Any] = await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/version"
        )
        return VersionInfo(
            browser=str(data.get("Browser", "")),
            protocol_version=str(data.get("Protocol-Version", "")),
            user_agent=str(data.get("User-Agent", "")),
            web_socket_debugger_url=str(data.get("webSocketDebuggerUrl", "")),
        )

    async def list_targets(self) -> list[TargetInfo]:
        """List all available CDP targets."""
        data: list[dict[str, Any]] = await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/list"
        )
        targets: list[TargetInfo] = []
        for item in data:
            targets.append(
                TargetInfo(
                    target_id=str(item.get("id", "")),
                    type=str(item.get("type", "")),
                    title=str(item.get("title", "")),
                    url=str(item.get("url", "")),
                    web_socket_debugger_url=item.get("webSocketDebuggerUrl"),
                )
            )
        return targets

    async def new_tab(self, url: str = "about:blank") -> TargetInfo:
        """Create a new tab and return its target info."""
        encoded = urllib.parse.quote_plus(url)
        data: dict[str, Any] = await asyncio.to_thread(
            _http_put, f"{self._base_url}/json/new?{encoded}"
        )
        return TargetInfo(
            target_id=str(data.get("id", "")),
            type=str(data.get("type", "")),
            title=str(data.get("title", "")),
            url=str(data.get("url", "")),
            web_socket_debugger_url=data.get("webSocketDebuggerUrl"),
        )

    async def activate_tab(self, target_id: str) -> None:
        """Activate a tab by target ID."""
        await asyncio.to_thread(_http_get, f"{self._base_url}/json/activate/{target_id}")

    async def close_tab(self, target_id: str) -> None:
        """Close a tab by target ID."""
        await asyncio.to_thread(_http_get, f"{self._base_url}/json/close/{target_id}")
