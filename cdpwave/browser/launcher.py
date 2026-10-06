"""Browser process launcher with auto-detection and CI support."""

import asyncio
import contextlib
import inspect
import json
import logging
import os
import shutil
import socket
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass
from typing import Any

from cdpwave.browser.finder import find_browser
from cdpwave.exceptions import LaunchError, LaunchTimeoutError

fcntl: Any
if os.name == "posix":
    import fcntl
else:
    fcntl = None

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
    """Bind an ephemeral socket to find a free port.

    Returns the port and the bound socket. The caller should keep the
    socket open until just before spawning the browser, then close it —
    this shrinks the TOCTOU window where another process could grab the
    port between finding it and the browser binding it.

    Returns:
        A tuple of (port, socket) where socket is the bound socket
        holding the port, or None if a specific port was requested.
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
        pipe: Whether the browser was launched with ``--remote-debugging-pipe``.
    """

    web_socket_debugger_url: str
    browser_version: str
    protocol_version: str
    user_agent: str
    port: int
    pipe: bool = False


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
        pipe: bool = False,
    ) -> None:
        self._browser_path = browser_path
        self._port = port
        self._headless = headless
        self._user_data_dir = user_data_dir
        self._extra_args = extra_args
        self._pipe = pipe
        self._process: asyncio.subprocess.Process | subprocess.Popen[bytes] | None = None
        self._temp_dir: str | None = None
        self._info: BrowserInfo | None = None
        self._pipe_read_fd: int | None = None
        self._pipe_write_fd: int | None = None

    def _build_args(self) -> tuple[list[str], socket.socket | None]:
        """Build the command-line arguments for the browser process.

        Returns:
            A tuple of (args, port_socket) where port_socket is a bound
            socket holding the port until the browser starts, or None.
        """
        if self._browser_path is None:
            self._browser_path = find_browser()

        port_socket: socket.socket | None = None
        if self._pipe:
            port = 0
        elif self._port != 0:
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
            f"--user-data-dir={user_data_dir}",
            *_DEFAULT_FLAGS,
        ]

        if self._pipe:
            args.append("--remote-debugging-pipe")
        else:
            args.append(f"--remote-debugging-port={port}")
            args.append("--remote-allow-origins=*")

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

        if self._pipe:
            return await self._launch_pipe(timeout=timeout)

        max_retries = 3 if self._port == 0 else 1
        for attempt in range(max_retries):
            if attempt > 0:
                self._port = 0
                self._user_data_dir = None
            args, port_socket = self._build_args()

            self._process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )
            if port_socket is not None:
                port_socket.close()

            try:
                self._info = await self._wait_for_endpoint(timeout=timeout)
                return self._info
            except (LaunchError, LaunchTimeoutError):
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

    async def _launch_pipe(self, timeout: float = 10.0) -> BrowserInfo:
        """Launch browser with ``--remote-debugging-pipe``.

        Chrome's pipe protocol uses file descriptors 3 (commands in)
        and 4 (messages out) with NUL-delimited JSON. POSIX only.

        No HTTP discovery is needed — readiness is implicit once the
        process is alive.
        """
        if os.name != "posix":
            raise LaunchError(
                "--remote-debugging-pipe is only supported on POSIX systems"
            )

        args, _ = self._build_args()

        # rd3/wr3: parent writes to wr3, browser reads from fd 3 (rd3).
        # rd4/wr4: browser writes to fd 4 (wr4), parent reads from rd4.
        rd3, wr3 = os.pipe()
        rd4, wr4 = os.pipe()

        # Chrome requires the pipe ends at exactly fd 3 and fd 4. Since
        # preexec_fn runs before subprocess closes extra fds, remap in
        # the parent instead: move rd3 -> 3 and wr4 -> 4, then pass them
        # via pass_fds. Our other pipe ends occupying 3/4 are first moved
        # to a higher fd so nothing gets clobbered.
        assert fcntl is not None

        def _rehome(fd: int) -> int:
            newfd: int = fcntl.fcntl(fd, fcntl.F_DUPFD, 5)
            os.close(fd)
            return newfd

        if rd4 in (3, 4):
            rd4 = _rehome(rd4)
        if wr3 in (3, 4):
            wr3 = _rehome(wr3)
        if rd3 == 4:
            rd3 = _rehome(rd3)
        if wr4 == 3:
            wr4 = _rehome(wr4)
        # If 3/4 are already open in the parent (not our pipe ends), move
        # them aside so dup2 doesn't clobber an unrelated descriptor.
        ours = {rd3, wr3, rd4, wr4}
        for target in (3, 4):
            try:
                fcntl.fcntl(target, fcntl.F_GETFD)
            except OSError:
                continue  # fd not open — free to use
            if target not in ours:
                _rehome(target)
        if rd3 != 3:
            os.dup2(rd3, 3)
            os.close(rd3)
            rd3 = 3
        if wr4 != 4:
            os.dup2(wr4, 4)
            os.close(wr4)
            wr4 = 4

        try:
            # asyncio.subprocess cannot pass fds 3/4 to the child or run
            # a preexec_fn, so Chrome's pipe protocol requires Popen here.
            self._process = subprocess.Popen(  # noqa: ASYNC220
                args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                pass_fds=(rd3, wr4),
            )
        except OSError as exc:
            for fd in (rd3, wr3, rd4, wr4):
                with contextlib.suppress(OSError):
                    os.close(fd)
            raise LaunchError(f"Failed to launch browser process: {exc}") from exc

        os.close(rd3)
        os.close(wr4)
        self._pipe_read_fd = rd4
        self._pipe_write_fd = wr3

        await asyncio.sleep(0.2)
        if self._process.poll() is not None:
            stderr_data = self._process.stderr.read() if self._process.stderr else b""
            stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
            for fd in (rd4, wr3):
                with contextlib.suppress(OSError):
                    os.close(fd)
            self._pipe_read_fd = None
            self._pipe_write_fd = None
            raise LaunchError(
                f"Browser process exited with code {self._process.returncode}"
                + (f": {stderr_text}" if stderr_text else "")
            )

        self._info = BrowserInfo(
            web_socket_debugger_url="",
            browser_version="",
            protocol_version="",
            user_agent="",
            port=0,
            pipe=True,
        )
        return self._info

    async def _wait_for_endpoint(self, timeout: float = 10.0) -> BrowserInfo:
        """Poll the HTTP discovery endpoint until the browser is ready."""
        url = f"http://127.0.0.1:{self._port}/json/version"
        delay = 0.1
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout

        while loop.time() < deadline:
            proc = self._process
            if proc is not None:
                if isinstance(proc, subprocess.Popen):
                    exited = proc.poll() is not None
                else:
                    exited = proc.returncode is not None
            else:
                exited = False
            if exited and proc is not None:
                stderr_data = b""
                if proc.stderr is not None:
                    read_result = proc.stderr.read()
                    if inspect.isawaitable(read_result):
                        stderr_data = await read_result
                    else:
                        stderr_data = read_result
                stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
                raise LaunchError(
                    f"Browser process exited with code {proc.returncode}"
                    + (f": {stderr_text}" if stderr_text else "")
                )

            try:
                fetch_timeout = min(5.0, deadline - loop.time())
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
                delay = min(delay * 1.5, 1.0)

        raise LaunchTimeoutError(
            f"Browser did not become ready within {timeout}s on port {self._port}"
        )

    async def close(self) -> None:
        """Terminate the browser process and clean up temporary files."""
        for fd in (self._pipe_read_fd, self._pipe_write_fd):
            if fd is not None:
                with contextlib.suppress(OSError):
                    os.close(fd)
        self._pipe_read_fd = None
        self._pipe_write_fd = None

        if self._process is not None:
            with contextlib.suppress(Exception):
                if isinstance(self._process, subprocess.Popen):
                    if self._process.poll() is None:
                        self._process.terminate()
                        try:
                            await asyncio.wait_for(
                                asyncio.to_thread(self._process.wait), timeout=2.0
                            )
                        except TimeoutError:
                            self._process.kill()
                            await asyncio.wait_for(
                                asyncio.to_thread(self._process.wait), timeout=5.0
                            )
                elif self._process.returncode is None:
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
            if self._process is not None and self.is_running:
                logger.warning(
                    "BrowserLauncher was not closed; browser process may still be running"
                )

    @property
    def is_running(self) -> bool:
        """Whether the browser process is still running."""
        if isinstance(self._process, subprocess.Popen):
            return self._process.poll() is None
        return self._process is not None and self._process.returncode is None

    @property
    def pipe_fds(self) -> tuple[int, int] | None:
        """The (read_fd, write_fd) pair for pipe mode, or None."""
        if self._pipe_read_fd is None or self._pipe_write_fd is None:
            return None
        return self._pipe_read_fd, self._pipe_write_fd

    @property
    def info(self) -> BrowserInfo | None:
        """BrowserInfo if the browser has been launched, else None."""
        return self._info

    @property
    def process(
        self,
    ) -> asyncio.subprocess.Process | subprocess.Popen[bytes] | None:
        """The browser subprocess, or None if not launched."""
        return self._process

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
