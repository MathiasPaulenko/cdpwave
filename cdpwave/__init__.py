"""cdpwave — Chrome DevTools Protocol client for Python.

Public API exports for the cdpwave package.
"""

__version__ = "3.1.1"

from cdpwave.client import BrowserContext, CDPClient, CDPSession
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
from cdpwave.types import (
    DOMGetDocumentResult,
    DOMNode,
    ExceptionDetails,
    NetworkCookie,
    NetworkGetCookiesResult,
    PageNavigateResult,
    RemoteObject,
    RuntimeEvaluateResult,
    TargetAttachToTargetResult,
    TargetCreateTargetResult,
)

__all__ = [
    "BrowserContext",
    "BrowserNotFoundError",
    "CDPClient",
    "CDPError",
    "CDPSession",
    "CommandError",
    "CommandTimeoutError",
    "ConnectionClosedError",
    "DOMGetDocumentResult",
    "DOMNode",
    "DiscoveryError",
    "EventDispatcher",
    "EventHandler",
    "ExceptionDetails",
    "LaunchError",
    "LaunchTimeoutError",
    "NetworkCookie",
    "NetworkGetCookiesResult",
    "PageNavigateResult",
    "RemoteObject",
    "RuntimeEvaluateResult",
    "SessionClosedError",
    "Subscription",
    "TargetAttachToTargetResult",
    "TargetCreateTargetResult",
    "__version__",
]