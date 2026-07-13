"""WebMCP domain: Web MCP protocol for monitoring tool registration and invocation.

This domain is **experimental**.

Depends on: Runtime, Page, DOM.

Types:
    Annotation
    InvocationStatus
    Tool

Commands:
    enable
    disable

Events:
    toolsAdded
    toolsRemoved
    toolInvoked
    toolResponded
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class WebMCPDomain(BaseDomain):
    """Wrapper for the CDP WebMCP domain.

    This domain is **experimental**.

    Provides control over the Web MCP (Model Context Protocol)
    for monitoring tool registration and invocation in web pages.

    Events:
        ``WebMCP.toolsAdded`` — fired when new tools are added.
            Params: ``tools`` (array of Tool).
        ``WebMCP.toolsRemoved`` — fired when tools are removed.
            Params: ``tools`` (array of Tool).
        ``WebMCP.toolInvoked`` — fired when a tool invocation starts.
            Params: ``toolName`` (string), ``frameId`` (Page.FrameId),
            ``invocationId`` (string), ``input`` (string).
        ``WebMCP.toolResponded`` — fired when a tool invocation
            completes or fails.
            Params: ``invocationId`` (string), ``status``
            (InvocationStatus), optional ``output`` (any),
            optional ``errorText`` (string), optional ``exception``
            (Runtime.RemoteObject).

    Use ``session.on("WebMCP.toolsAdded", handler)``
    to subscribe to these events.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the WebMCP domain, allowing events to be sent.

        Enabling the domain will trigger a ``toolsAdded`` event for
        all currently registered tools.

        Returns:
            The CDP response result dict.
        """
        return await self._call("WebMCP.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the WebMCP domain.

        Returns:
            The CDP response result dict.
        """
        return await self._call("WebMCP.disable")
