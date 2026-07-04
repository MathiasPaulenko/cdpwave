"""cdpwave — Chrome DevTools Protocol client for Python.

Public API exports for the cdpwave package.
"""

__version__ = "1.10.0"

from cdpwave.client import CDPClient, CDPSession
from cdpwave.events.dispatcher import EventDispatcher
from cdpwave.events.handlers import EventHandler, Subscription
from cdpwave.exceptions import (
    BrowserNotFoundError,
    CDPError,
    CommandError,
    CommandTimeoutError,
    ConnectionClosedError,
    DiscoveryError,
    LaunchError,
    LaunchTimeoutError,
    SessionClosedError,
)

__all__ = [
    "CDPClient",
    "CDPSession",
    "CDPError",
    "ConnectionClosedError",
    "CommandError",
    "CommandTimeoutError",
    "BrowserNotFoundError",
    "SessionClosedError",
    "DiscoveryError",
    "EventDispatcher",
    "Subscription",
    "EventHandler",
    "LaunchError",
    "LaunchTimeoutError",
    "__version__",
]