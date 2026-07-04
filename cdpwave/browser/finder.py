"""Browser executable discovery for Chrome, Edge, Brave, and Chromium."""

import os
import shutil
import sys

from cdpwave.exceptions import BrowserNotFoundError
from cdpwave.types import BrowserType

_WIN_CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

_WIN_EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

_WIN_BRAVE_PATHS = [
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
]

_WIN_CHROMIUM_PATHS = [
    r"C:\Program Files\Chromium\Application\chromium.exe",
    r"C:\Program Files (x86)\Chromium\Application\chromium.exe",
]

_MAC_CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
_MAC_EDGE_PATH = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
_MAC_BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
_MAC_CHROMIUM_PATH = "/Applications/Chromium.app/Contents/MacOS/Chromium"

_LINUX_NAMES: dict[str, list[str]] = {
    "chrome": ["google-chrome", "google-chrome-stable", "chrome"],
    "edge": ["microsoft-edge", "microsoft-edge-stable"],
    "brave": ["brave-browser", "brave"],
    "chromium": ["chromium", "chromium-browser"],
}


def _check_paths(paths: list[str]) -> str | None:
    """Return the first existing path from a list, or None."""
    for path in paths:
        if os.path.isfile(path):
            return path
    return None


def _find_on_linux(names: list[str]) -> str | None:
    """Find an executable by name on Linux using PATH lookup."""
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def find_chrome() -> str | None:
    """Find a Chrome executable path, or None if not found."""
    env_path = os.environ.get("CDPWAVE_CHROME_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path
    if sys.platform == "win32":
        return _check_paths(_WIN_CHROME_PATHS)
    if sys.platform == "darwin":
        return _check_paths([_MAC_CHROME_PATH])
    return _find_on_linux(_LINUX_NAMES["chrome"])


def find_edge() -> str | None:
    """Find an Edge executable path, or None if not found."""
    env_path = os.environ.get("CDPWAVE_EDGE_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path
    if sys.platform == "win32":
        return _check_paths(_WIN_EDGE_PATHS)
    if sys.platform == "darwin":
        return _check_paths([_MAC_EDGE_PATH])
    return _find_on_linux(_LINUX_NAMES["edge"])


def find_brave() -> str | None:
    """Find a Brave executable path, or None if not found."""
    env_path = os.environ.get("CDPWAVE_BRAVE_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path
    if sys.platform == "win32":
        return _check_paths(_WIN_BRAVE_PATHS)
    if sys.platform == "darwin":
        return _check_paths([_MAC_BRAVE_PATH])
    return _find_on_linux(_LINUX_NAMES["brave"])


def find_chromium() -> str | None:
    """Find a Chromium executable path, or None if not found."""
    env_path = os.environ.get("CDPWAVE_CHROMIUM_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path
    if sys.platform == "win32":
        return _check_paths(_WIN_CHROMIUM_PATHS)
    if sys.platform == "darwin":
        return _check_paths([_MAC_CHROMIUM_PATH])
    return _find_on_linux(_LINUX_NAMES["chromium"])


_FINDER_NAMES: dict[BrowserType, str] = {
    "chrome": "find_chrome",
    "edge": "find_edge",
    "brave": "find_brave",
    "chromium": "find_chromium",
}

_SEARCH_ORDER: list[BrowserType] = ["chrome", "edge", "brave", "chromium"]


def find_browser(preferred: BrowserType | None = None) -> str:
    """Find a Chromium-based browser executable.

    Searches Chrome, Edge, Brave, and Chromium in order. The
    ``CDPWAVE_BROWSER_PATH`` environment variable overrides all detection.

    Args:
        preferred: Optional preferred browser type to search first.

    Returns:
        The path to the browser executable.

    Raises:
        BrowserNotFoundError: If no browser is found.
    """
    env_override = os.environ.get("CDPWAVE_BROWSER_PATH")
    if env_override and os.path.isfile(env_override):
        return env_override

    search_order: list[BrowserType] = []
    if preferred is not None:
        search_order.append(preferred)
    search_order.extend([b for b in _SEARCH_ORDER if b != preferred])

    for browser_type in search_order:
        finder = globals()[_FINDER_NAMES[browser_type]]
        path: str | None = finder()
        if path:
            return path

    raise BrowserNotFoundError(
        "No Chromium-based browser found."
        " Set CDPWAVE_BROWSER_PATH or install Chrome/Edge/Brave/Chromium."
    )
