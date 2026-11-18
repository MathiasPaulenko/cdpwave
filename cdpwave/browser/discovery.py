"""HTTP discovery for Chrome DevTools Protocol endpoints."""

import asyncio
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from cdpwave.exceptions import DiscoveryError


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
        data: Any = await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/version"
        )
        if not isinstance(data, dict):
            raise DiscoveryError(
                f"Malformed /json/version response: expected object, "
                f"got {type(data).__name__}"
            )
        return VersionInfo(
            browser=str(data.get("Browser", "")),
            protocol_version=str(data.get("Protocol-Version", "")),
            user_agent=str(data.get("User-Agent", "")),
            web_socket_debugger_url=str(data.get("webSocketDebuggerUrl", "")),
        )

    async def list_targets(self) -> list[TargetInfo]:
        """List all available CDP targets."""
        data: Any = await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/list"
        )
        if not isinstance(data, list) or not all(
            isinstance(item, dict) for item in data
        ):
            raise DiscoveryError(
                "Malformed /json/list response: expected a list of objects"
            )
        targets: list[TargetInfo] = []
        for item in data:
            ws_url = item.get("webSocketDebuggerUrl")
            targets.append(
                TargetInfo(
                    target_id=str(item.get("id", "")),
                    type=str(item.get("type", "")),
                    title=str(item.get("title", "")),
                    url=str(item.get("url", "")),
                    web_socket_debugger_url=(
                        str(ws_url) if ws_url is not None else None
                    ),
                )
            )
        return targets

    async def new_tab(self, url: str = "about:blank") -> TargetInfo:
        """Create a new tab and return its target info."""
        encoded = urllib.parse.quote_plus(url)
        data: Any = await asyncio.to_thread(
            _http_put, f"{self._base_url}/json/new?{encoded}"
        )
        if not isinstance(data, dict):
            raise DiscoveryError(
                f"Malformed /json/new response: expected object, "
                f"got {type(data).__name__}"
            )
        ws_url = data.get("webSocketDebuggerUrl")
        return TargetInfo(
            target_id=str(data.get("id", "")),
            type=str(data.get("type", "")),
            title=str(data.get("title", "")),
            url=str(data.get("url", "")),
            web_socket_debugger_url=(
                str(ws_url) if ws_url is not None else None
            ),
        )

    async def activate_tab(self, target_id: str) -> None:
        """Activate a tab by target ID."""
        quoted = urllib.parse.quote(target_id, safe="")
        await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/activate/{quoted}"
        )

    async def close_tab(self, target_id: str) -> None:
        """Close a tab by target ID."""
        quoted = urllib.parse.quote(target_id, safe="")
        await asyncio.to_thread(
            _http_get, f"{self._base_url}/json/close/{quoted}"
        )
