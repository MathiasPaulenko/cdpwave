"""Type aliases and TypedDicts used across cdpwave."""

from collections.abc import Awaitable, Callable
from typing import Any, Literal, TypedDict

CommandSender = Callable[[str, dict[str, Any] | None], Awaitable[dict[str, Any]]]
"""Callable that sends a CDP command and awaits the response dict."""

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]
"""Async callable that receives CDP event params."""

EventErrorCallback = Callable[[str, dict[str, Any], BaseException], Awaitable[None] | None]
"""Callback invoked when an event handler raises an exception.

Receives (event_name, params, exception). May be sync or async.
"""

BrowserType = Literal["chrome", "edge", "brave", "chromium"]
"""Supported Chromium-based browser types."""


class RemoteObject(TypedDict, total=False):
    """Runtime.RemoteObject as returned by ``Runtime.evaluate``."""

    type: str
    subtype: str | None
    className: str | None
    value: Any
    unserializableValue: str | None
    description: str | None
    objectId: str | None
    preview: dict[str, Any] | None


class ExceptionDetails(TypedDict, total=False):
    """Runtime.ExceptionDetails."""

    exceptionId: int
    text: str
    lineNumber: int
    columnNumber: int
    scriptId: str | None
    stackTrace: dict[str, Any] | None
    exception: RemoteObject | None
    executionContextId: int | None


class RuntimeEvaluateResult(TypedDict, total=False):
    """Response from ``Runtime.evaluate``."""

    result: RemoteObject
    exceptionDetails: ExceptionDetails


class PageNavigateResult(TypedDict, total=False):
    """Response from ``Page.navigate``."""

    frameId: str
    loaderId: str
    errorText: str | None


class DOMNode(TypedDict, total=False):
    """DOM.Node (simplified)."""

    nodeId: int
    parentId: int | None
    backendNodeId: int
    nodeType: int
    nodeName: str
    nodeValue: str
    attributes: list[str]
    children: list[dict[str, Any]]
    documentURL: str | None
    baseURL: str | None


class DOMGetDocumentResult(TypedDict, total=False):
    """Response from ``DOM.getDocument``."""

    root: DOMNode


class NetworkCookie(TypedDict, total=False):
    """Network.Cookie."""

    name: str
    value: str
    domain: str
    path: str
    expires: float | None
    size: int
    httpOnly: bool
    secure: bool
    session: bool
    sameSite: str | None
    priority: str | None


class NetworkGetCookiesResult(TypedDict, total=False):
    """Response from ``Network.getCookies``."""

    cookies: list[NetworkCookie]


class TargetCreateTargetResult(TypedDict, total=False):
    """Response from ``Target.createTarget``."""

    targetId: str


class TargetAttachToTargetResult(TypedDict, total=False):
    """Response from ``Target.attachToTarget``."""

    sessionId: str
