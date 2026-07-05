"""Browser process launcher with auto-detection and CI support."""

import asyncio
import contextlib
import json
import os
import shutil
import socket
import tempfile
import urllib.request
from dataclasses import dataclass

from cdpwave.browser.finder import find_browser
from cdpwave.exceptions import LaunchError, LaunchTimeoutError

_DEFAULT_FLAGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-features=Translate",
]

_CI_ENV_VARS = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"]


def _is_ci() -> bool:
    return any(os.environ.get(var) for var in _CI_ENV_VARS)


def _find_free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port: int = s.getsockname()[1]
        return port


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

    def _build_args(self) -> list[str]:
        """Build the command-line arguments for the browser process."""
        if self._browser_path is None:
            self._browser_path = find_browser()

        port = self._port if self._port != 0 else _find_free_port()
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
        return args

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

        args = self._build_args()

        self._process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )

        self._info = await self._wait_for_endpoint(timeout=timeout)
        return self._info

    async def _wait_for_endpoint(self, timeout: float = 10.0) -> BrowserInfo:
        """Poll the HTTP discovery endpoint until the browser is ready."""
        url = f"http://localhost:{self._port}/json/version"
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
                data = await asyncio.to_thread(_fetch_version, url)
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
                        await self._process.wait()
            self._process = None

        if self._temp_dir is not None:
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None

        self._info = None

    @property
    def is_running(self) -> bool:
        """Whether the browser process is still running."""
        return self._process is not None and self._process.returncode is None

    @property
    def info(self) -> BrowserInfo | None:
        """BrowserInfo if the browser has been launched, else None."""
        return self._info


def _fetch_version(url: str) -> dict[str, object]:
    """Fetch and parse JSON from the ``/json/version`` endpoint."""
    with urllib.request.urlopen(url, timeout=5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data  # type: ignore[no-any-return]
