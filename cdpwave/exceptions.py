class CDPError(Exception):
    """Base exception for all cdpwave errors."""


class ConnectionClosedError(CDPError):
    """WebSocket connection was closed."""


class CommandError(CDPError):
    """CDP command returned an error response."""

    def __init__(self, code: int, message: str, data: dict[str, object] | None = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}")


class CommandTimeoutError(CDPError):
    """CDP command did not respond within timeout."""


class BrowserNotFoundError(CDPError):
    """No Chromium-based browser found on the system."""


class SessionClosedError(CDPError):
    """CDP session was closed by the browser."""


class DiscoveryError(CDPError):
    """HTTP discovery endpoint request failed."""


class LaunchTimeoutError(CDPError):
    """Browser did not start within the specified timeout."""


class LaunchError(CDPError):
    """Browser crashed or failed during startup."""
