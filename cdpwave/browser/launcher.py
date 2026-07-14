"""Browser process launcher with auto-detection and CI support."""

import asyncio
import contextlib
import json
import logging
import os
import shutil
import socket
import tempfile
import urllib.request
from dataclasses import dataclass

from cdpwave.browser.finder import find_browser
from cdpwave.exceptions import LaunchError, LaunchTimeoutError

logger = logging.getLogger("cdpwave.browser.launcher")

_DEFAULT_FLAGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-features=Translate",
]

_CI_ENV_VARS = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"]


def _is_ci() -> bool:
    return any(os.environ.get(var) for var in _CI_ENV_VARS)


def _find_free_port() -> tuple[int, socket.socket | None]:
    """Bind a ephemeral socket to find a free port.

    Returns the port and the bound socket. The caller must keep the socket
    open until the port is in use by the browser, then close it. This
    eliminates the TOCTOU race where another process could grab the port
    between finding it and using it.

    Returns:
        A tuple of (port, socket) where socket is the bound socket to
        hold the port, or None if a specific port was requested.
    """
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port: int = s.getsockname()[1]
    return port, s


@dataclass(frozen=True)
class BrowserInfo:
    """Information about a launched browser instance.

    Attributes:
        web_socket_debugger_url: WebSocket URL for CDP communication.
        browser_version: Browser version string.
        protocol_version: CDP protocol version.
        user_agent: Browser user agent string.
        port: The remote debugging port.
    """

    web_socket_debugger_url: str
    browser_version: str
    protocol_version: str
    user_agent: str
    port: int


class BrowserLauncher:
    """Launches and manages a Chromium-based browser process.

    Handles browser path detection, flag construction, process lifecycle,
    and endpoint discovery via HTTP polling.
    """

    def __init__(
        self,
        browser_path: str | None = None,
        port: int = 0,
        headless: bool = True,
        user_data_dir: str | None = None,
        extra_args: list[str] | None = None,
    ) -> None:
        self._browser_path = browser_path
        self._port = port
        self._headless = headless
        self._user_data_dir = user_data_dir
        self._extra_args = extra_args
        self._process: asyncio.subprocess.Process | None = None
        self._temp_dir: str | None = None
        self._info: BrowserInfo | None = None

    def _build_args(self) -> tuple[list[str], socket.socket | None]:
        """Build the command-line arguments for the browser process.

        Returns:
            A tuple of (args, port_socket) where port_socket is a bound
            socket holding the port until the browser starts, or None.
        """
        if self._browser_path is None:
            self._browser_path = find_browser()

        port_socket: socket.socket | None = None
        if self._port != 0:
            port = self._port
        else:
            port, port_socket = _find_free_port()
            self._port = port

        user_data_dir = self._user_data_dir
        if user_data_dir is None:
            user_data_dir = self._create_temp_user_dir()
        self._user_data_dir = user_data_dir

        args = [
            self._browser_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}",
            "--remote-allow-origins=*",
            *_DEFAULT_FLAGS,
        ]

        if self._headless:
            args.append("--headless=new")

        if _is_ci():
            args.append("--no-sandbox")

        if self._extra_args:
            args.extend(self._extra_args)

        args.append("about:blank")
        return args, port_socket

    def _create_temp_user_dir(self) -> str:
        """Create a temporary user data directory and return its path."""
        self._temp_dir = tempfile.mkdtemp(prefix="cdpwave-")
        return self._temp_dir

    async def launch(self, timeout: float = 10.0) -> BrowserInfo:
        """Launch the browser and wait for the CDP endpoint to be ready.

        Args:
            timeout: Maximum seconds to wait for the browser endpoint.

        Returns:
            BrowserInfo with connection details.

        Raises:
            RuntimeError: If the browser is already running.
            LaunchError: If the browser process exits during startup.
            LaunchTimeoutError: If the endpoint does not become ready in time.
        """
        if self._process is not None:
            raise RuntimeError("Browser is already running")

        max_retries = 3 if self._port == 0 else 1
        for attempt in range(max_retries):
            if attempt > 0:
                self._port = 0
                self._user_data_dir = None
            args, port_socket = self._build_args()

            if port_socket is not None:
                port_socket.close()

            self._process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                self._info = await self._wait_for_endpoint(timeout=timeout)
                return self._info
            except LaunchError:
                if self._process is not None:
                    with contextlib.suppress(Exception):
                        self._process.terminate()
                    with contextlib.suppress(Exception):
                        await asyncio.wait_for(self._process.wait(), timeout=2.0)
                self._process = None
                if self._temp_dir is not None:
                    shutil.rmtree(self._temp_dir, ignore_errors=True)
                    self._temp_dir = None
                if attempt + 1 >= max_retries:
                    raise
                logger.warning(
                    "Browser launch attempt %d failed, retrying with new port",
                    attempt + 1,
                )

        raise LaunchError("Failed to launch browser after retries")

    async def _wait_for_endpoint(self, timeout: float = 10.0) -> BrowserInfo:
        """Poll the HTTP discovery endpoint until the browser is ready."""
        url = f"http://127.0.0.1:{self._port}/json/version"
        delay = 0.1
        elapsed = 0.0

        while elapsed < timeout:
            if self._process is not None and self._process.returncode is not None:
                stderr_data = b""
                if self._process.stderr is not None:
                    stderr_data = await self._process.stderr.read()
                stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
                raise LaunchError(
                    f"Browser process exited with code {self._process.returncode}"
                    + (f": {stderr_text}" if stderr_text else "")
                )

            try:
                fetch_timeout = min(5.0, timeout - elapsed)
                data = await asyncio.to_thread(_fetch_version, url, fetch_timeout)
                return BrowserInfo(
                    web_socket_debugger_url=str(data.get("webSocketDebuggerUrl", "")),
                    browser_version=str(data.get("Browser", "")),
                    protocol_version=str(data.get("Protocol-Version", "")),
                    user_agent=str(data.get("User-Agent", "")),
                    port=self._port,
                )
            except Exception:
                await asyncio.sleep(delay)
                elapsed += delay
                delay = min(delay * 1.5, 1.0)

        raise LaunchTimeoutError(
            f"Browser did not become ready within {timeout}s on port {self._port}"
        )

    async def close(self) -> None:
        """Terminate the browser process and clean up temporary files."""
        if self._process is not None:
            with contextlib.suppress(Exception):
                if self._process.returncode is None:
                    self._process.terminate()
                    try:
                        await asyncio.wait_for(self._process.wait(), timeout=2.0)
                    except TimeoutError:
                        self._process.kill()
                        await asyncio.wait_for(self._process.wait(), timeout=5.0)
            self._process = None

        if self._temp_dir is not None:
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None

        self._info = None

    def __del__(self) -> None:
        with contextlib.suppress(Exception):
            if self._process is not None and self._process.returncode is None:
                import warnings
                warnings.warn(
                    "BrowserLauncher was not closed; browser process may still be running",
                    ResourceWarning,
                    stacklevel=2,
                )

    @property
    def is_running(self) -> bool:
        """Whether the browser process is still running."""
        return self._process is not None and self._process.returncode is None

    @property
    def info(self) -> BrowserInfo | None:
        """BrowserInfo if the browser has been launched, else None."""
        return self._info

    def __repr__(self) -> str:
        state = "running" if self.is_running else "stopped"
        path = self._browser_path or "auto-detected"
        return f"BrowserLauncher({path!r}, {state})"


def _fetch_version(url: str, timeout: float = 5.0) -> dict[str, object]:
    """Fetch and parse JSON from the ``/json/version`` endpoint.

    Args:
        url: The ``/json/version`` URL to fetch.
        timeout: Per-request timeout in seconds.
    """
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data  # type: ignore[no-any-return]
