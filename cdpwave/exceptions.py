"""Custom exception classes for cdpwave errors."""

class CDPError(Exception):
    """Base exception for all cdpwave errors."""


class ConnectionClosedError(CDPError):
    """Raised when the WebSocket connection is closed."""


class ConnectionReconnectError(ConnectionClosedError):
    """Raised when a pending command is lost during reconnection.

    Inherits from ConnectionClosedError so existing ``except ConnectionClosedError``
    handlers still catch it. Users can catch this specifically to retry commands.
    """


class CommandError(CDPError):
    """Raised when a CDP command returns an error response.

    Attributes:
        code: The CDP error code.
        message: The CDP error message.
        data: Optional additional error data from the CDP response.
    """

    def __init__(self, code: int, message: str, data: dict[str, object] | None = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}")


class CommandTimeoutError(CDPError):
    """Raised when a CDP command does not respond within the timeout."""


class BrowserNotFoundError(CDPError):
    """Raised when no Chromium-based browser is found on the system."""


class SessionClosedError(CDPError):
    """Raised when a CDP session is closed by the browser."""


class DiscoveryError(CDPError):
    """Raised when an HTTP discovery endpoint request fails."""


class LaunchTimeoutError(CDPError):
    """Raised when the browser does not start within the specified timeout."""


class LaunchError(CDPError):
    """Raised when the browser crashes or fails during startup."""


class ProtocolError(CDPError):
    """Raised when a CDP response is missing expected fields."""
