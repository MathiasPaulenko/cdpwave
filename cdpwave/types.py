"""Type aliases and TypedDicts used across cdpwave."""

from collections.abc import Awaitable, Callable
from typing import Any, Literal, TypedDict

CommandSender = Callable[[str, dict[str, Any] | None], Awaitable[dict[str, Any]]]
"""Callable that sends a CDP command and awaits the response dict."""

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


class PageCaptureScreenshotResult(TypedDict, total=False):
    """Response from ``Page.captureScreenshot``."""

    data: str


class PagePrintToPDFResult(TypedDict, total=False):
    """Response from ``Page.printToPDF``."""

    data: str
    stream: str | None


class PageGetLayoutMetricsResult(TypedDict, total=False):
    """Response from ``Page.getLayoutMetrics``."""

    layoutViewport: dict[str, Any]
    visualViewport: dict[str, Any]
    contentSize: dict[str, Any]
    cssLayoutViewport: dict[str, Any]
    cssVisualViewport: dict[str, Any]
    cssContentSize: dict[str, Any]


class PageGetNavigationHistoryResult(TypedDict, total=False):
    """Response from ``Page.getNavigationHistory``."""

    currentIndex: int
    entries: list[dict[str, Any]]


class PageGetFrameTreeResult(TypedDict, total=False):
    """Response from ``Page.getFrameTree``."""

    frameTree: dict[str, Any]


class PageGetResourceTreeResult(TypedDict, total=False):
    """Response from ``Page.getResourceTree``."""

    frameTree: dict[str, Any]


class PageGetResourceContentResult(TypedDict, total=False):
    """Response from ``Page.getResourceContent``."""

    content: str
    base64Encoded: bool


class PageAddScriptToEvaluateOnNewDocumentResult(TypedDict, total=False):
    """Response from ``Page.addScriptToEvaluateOnNewDocument``."""

    identifier: str


class RuntimeCallFunctionOnResult(TypedDict, total=False):
    """Response from ``Runtime.callFunctionOn``."""

    result: RemoteObject
    exceptionDetails: ExceptionDetails


class RuntimeGetPropertiesResult(TypedDict, total=False):
    """Response from ``Runtime.getProperties``."""

    result: list[dict[str, Any]]
    internalProperties: list[dict[str, Any]] | None
    privateProperties: list[dict[str, Any]] | None
    exceptionDetails: ExceptionDetails | None


class RuntimeCompileScriptResult(TypedDict, total=False):
    """Response from ``Runtime.compileScript``."""

    scriptId: str
    exceptionDetails: ExceptionDetails | None


class RuntimeRunScriptResult(TypedDict, total=False):
    """Response from ``Runtime.runScript``."""

    result: RemoteObject
    exceptionDetails: ExceptionDetails | None


class RuntimeAwaitPromiseResult(TypedDict, total=False):
    """Response from ``Runtime.awaitPromise``."""

    result: RemoteObject
    exceptionDetails: ExceptionDetails | None


class RuntimeQueryObjectsResult(TypedDict, total=False):
    """Response from ``Runtime.queryObjects``."""

    objects: RemoteObject


class RuntimeGlobalLexicalScopeNamesResult(TypedDict, total=False):
    """Response from ``Runtime.globalLexicalScopeNames``."""

    names: list[str]


class RuntimeGetHeapUsageResult(TypedDict, total=False):
    """Response from ``Runtime.getHeapUsage``."""

    usedSize: float
    totalSize: float
    embedderHeapUsedSize: float | None
    backingStorageSize: float | None


class RuntimeGetExceptionDetailsResult(TypedDict, total=False):
    """Response from ``Runtime.getExceptionDetails``."""

    exceptionDetails: ExceptionDetails


class RuntimeGetIsolateIdResult(TypedDict, total=False):
    """Response from ``Runtime.getIsolateId``."""

    id: str


class NetworkGetResponseBodyResult(TypedDict, total=False):
    """Response from ``Network.getResponseBody``."""

    body: str
    base64Encoded: bool


class NetworkGetRequestPostDataResult(TypedDict, total=False):
    """Response from ``Network.getRequestPostData``."""

    postData: str


class NetworkLoadNetworkResourceResult(TypedDict, total=False):
    """Response from ``Network.loadNetworkResource``."""

    resource: dict[str, Any]
    httpStatusCode: int | None


class DOMQuerySelectorResult(TypedDict, total=False):
    """Response from ``DOM.querySelector``."""

    nodeId: int


class DOMDescribeNodeResult(TypedDict, total=False):
    """Response from ``DOM.describeNode``."""

    node: dict[str, Any]


class DOMGetOuterHTMLResult(TypedDict, total=False):
    """Response from ``DOM.getOuterHTML``."""

    outerHTML: str


class DOMResolveNodeResult(TypedDict, total=False):
    """Response from ``DOM.resolveNode``."""

    object: RemoteObject


class DOMSearchResult(TypedDict, total=False):
    """Response from ``DOM.performSearch``."""

    searchId: str
    resultCount: int


class DOMGetSearchResultsResult(TypedDict, total=False):
    """Response from ``DOM.getSearchResults``."""

    nodeIds: list[int]


class TargetGetTargetsResult(TypedDict, total=False):
    """Response from ``Target.getTargets``."""

    targetInfos: list[dict[str, Any]]


class TargetGetTargetInfoResult(TypedDict, total=False):
    """Response from ``Target.getTargetInfo``."""

    targetInfo: dict[str, Any]
