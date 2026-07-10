"""WebMCP domain: Web MCP protocol for tool invocation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class WebMCPDomain(BaseDomain):
    """Wrapper for the CDP WebMCP domain.

    Provides control over the Web MCP (Model Context Protocol)
    for invoking tools in web pages.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the WebMCP domain."""
        return await self._call("WebMCP.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the WebMCP domain."""
        return await self._call("WebMCP.disable")

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """Invoke a Web MCP tool.

        Args:
            tool_name: Name of the tool to invoke.
            arguments: Arguments dict for the tool.
        """
        return await self._call(
            "WebMCP.invokeTool",
            {"toolName": tool_name, "arguments": arguments},
        )

    async def cancel_invocation(
        self,
        invocation_id: str,
    ) -> dict[str, Any]:
        """Cancel an ongoing tool invocation.

        Args:
            invocation_id: Invocation ID to cancel.
        """
        return await self._call(
            "WebMCP.cancelInvocation",
            {"invocationId": invocation_id},
        )
