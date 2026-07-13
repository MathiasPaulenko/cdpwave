"""Edge case unit tests for the WebMCP domain."""

import inspect
import typing

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.web_mcp import WebMCPDomain
from tests.unit.fake_sender import FakeSender

PDL_METHODS = ["enable", "disable"]

PDL_TYPES = ["Annotation", "InvocationStatus", "Tool"]

PDL_EVENTS = ["toolsAdded", "toolsRemoved", "toolInvoked", "toolResponded"]


@pytest.mark.unit
class TestWebMCPMethodCoverage:
    def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(WebMCPDomain)
            if not name.startswith("_") and callable(getattr(WebMCPDomain, name))
        }
        assert public_methods == set(PDL_METHODS)

    def test_method_count_matches_pdl(self) -> None:
        public_methods = [
            name
            for name in WebMCPDomain.__dict__
            if not name.startswith("_") and callable(WebMCPDomain.__dict__[name])
        ]
        assert len(public_methods) == len(PDL_METHODS)

    def test_order_matches_pdl(self) -> None:
        methods = [
            name
            for name in WebMCPDomain.__dict__
            if not name.startswith("_") and callable(WebMCPDomain.__dict__[name])
        ]
        assert methods == PDL_METHODS

    def test_inherits_basedomain(self) -> None:
        assert issubclass(WebMCPDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        for name in PDL_METHODS:
            method = getattr(WebMCPDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_enable_signature(self) -> None:
        sig = inspect.signature(WebMCPDomain.enable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, typing.Any]

    def test_disable_signature(self) -> None:
        sig = inspect.signature(WebMCPDomain.disable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, typing.Any]


@pytest.mark.unit
class TestWebMCPSerialization:
    async def test_enable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "WebMCP.enable"
        assert params is None

    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "WebMCP.disable"
        assert params is None


@pytest.mark.unit
class TestWebMCPReturnPassthrough:
    async def test_enable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = WebMCPDomain(fake)
        result = await domain.enable()
        assert result == {"result": "ok"}

    async def test_disable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = WebMCPDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}


@pytest.mark.unit
class TestWebMCPLifecycle:
    async def test_enable_disable_cycle(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("WebMCP.enable", None)
        assert fake.calls[1] == ("WebMCP.disable", None)

    async def test_enable_disable_repeated(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("WebMCP.enable", None)
            assert fake.calls[i * 2 + 1] == ("WebMCP.disable", None)

    async def test_disable_without_enable(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("WebMCP.disable", None)

    async def test_enable_twice(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        await domain.enable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("WebMCP.enable", None)
        assert fake.calls[1] == ("WebMCP.enable", None)


@pytest.mark.unit
class TestWebMCPConcurrency:
    async def test_concurrent_calls(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.enable(),
            domain.disable(),
        )
        assert len(fake.calls) == 4
        methods = [call[0] for call in fake.calls]
        assert methods.count("WebMCP.enable") == 2
        assert methods.count("WebMCP.disable") == 2


@pytest.mark.unit
class TestWebMCPErrorPropagation:
    async def test_command_error_propagated(self) -> None:
        from cdpwave.exceptions import CommandError

        class ErrorSender:
            async def __call__(
                self, method: str, params: dict | None = None
            ) -> dict:
                raise CommandError(-32000, "Domain not available")

        domain = WebMCPDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(CommandError, match="Domain not available"):
            await domain.enable()


@pytest.mark.unit
class TestWebMCPDocstrings:
    def test_module_describes_domain(self) -> None:
        import cdpwave.domains.web_mcp as mod

        assert "WebMCP" in mod.__doc__
        assert "experimental" in mod.__doc__

    def test_module_lists_events(self) -> None:
        import cdpwave.domains.web_mcp as mod

        for event in PDL_EVENTS:
            assert event in mod.__doc__, f"{event} not in module docstring"

    def test_module_lists_commands(self) -> None:
        import cdpwave.domains.web_mcp as mod

        for cmd in PDL_METHODS:
            assert cmd in mod.__doc__, f"{cmd} not in module docstring"

    def test_module_lists_types(self) -> None:
        import cdpwave.domains.web_mcp as mod

        for typ in PDL_TYPES:
            assert typ in mod.__doc__, f"{typ} not in module docstring"

    def test_class_describes_purpose(self) -> None:
        assert "Web MCP" in WebMCPDomain.__doc__

    def test_class_lists_events(self) -> None:
        for event in PDL_EVENTS:
            assert event in WebMCPDomain.__doc__, f"{event} not in class docstring"

    def test_class_marks_experimental(self) -> None:
        assert "experimental" in WebMCPDomain.__doc__

    def test_enable_has_returns(self) -> None:
        assert "Returns:" in WebMCPDomain.enable.__doc__

    def test_disable_has_returns(self) -> None:
        assert "Returns:" in WebMCPDomain.disable.__doc__

    def test_no_deprecated_wording(self) -> None:
        for name in PDL_METHODS:
            doc = getattr(WebMCPDomain, name).__doc__ or ""
            assert "Activates" not in doc
            assert "Deactivates" not in doc


@pytest.mark.unit
class TestWebMCPAdditionalDocstrings:
    def test_module_marks_experimental(self) -> None:
        import cdpwave.domains.web_mcp as mod

        assert "experimental" in mod.__doc__

    def test_module_lists_dependencies(self) -> None:
        import cdpwave.domains.web_mcp as mod

        assert "Runtime" in mod.__doc__
        assert "Page" in mod.__doc__
        assert "DOM" in mod.__doc__

    def test_module_types_in_pdl_order(self) -> None:
        import cdpwave.domains.web_mcp as mod

        doc = mod.__doc__ or ""
        idx_annotation = doc.index("Annotation")
        idx_invocation = doc.index("InvocationStatus")
        idx_tool = doc.index("Tool")
        assert idx_annotation < idx_invocation < idx_tool

    def test_module_events_in_pdl_order(self) -> None:
        import cdpwave.domains.web_mcp as mod

        doc = mod.__doc__ or ""
        idx_added = doc.index("toolsAdded")
        idx_removed = doc.index("toolsRemoved")
        idx_invoked = doc.index("toolInvoked")
        idx_responded = doc.index("toolResponded")
        assert idx_added < idx_removed < idx_invoked < idx_responded

    def test_module_commands_in_pdl_order(self) -> None:
        import cdpwave.domains.web_mcp as mod

        doc = mod.__doc__ or ""
        idx_enable = doc.index("enable")
        idx_disable = doc.index("disable")
        assert idx_enable < idx_disable

    def test_class_has_subscription_hint(self) -> None:
        assert "session.on" in WebMCPDomain.__doc__

    def test_enable_docstring_describes_tools_added_trigger(self) -> None:
        doc = WebMCPDomain.enable.__doc__ or ""
        assert "toolsAdded" in doc

    def test_enable_docstring_describes_enables(self) -> None:
        doc = WebMCPDomain.enable.__doc__ or ""
        assert "Enable" in doc or "enable" in doc

    def test_disable_docstring_describes_disables(self) -> None:
        doc = WebMCPDomain.disable.__doc__ or ""
        assert "Disable" in doc or "disable" in doc

    def test_module_describes_monitoring(self) -> None:
        import cdpwave.domains.web_mcp as mod

        assert "monitoring" in mod.__doc__


@pytest.mark.unit
class TestWebMCPAdditionalLifecycle:
    async def test_alternating_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 4
        assert fake.calls[0] == ("WebMCP.enable", None)
        assert fake.calls[1] == ("WebMCP.disable", None)
        assert fake.calls[2] == ("WebMCP.enable", None)
        assert fake.calls[3] == ("WebMCP.disable", None)

    async def test_enable_return_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_disable_return_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_multiple_calls_tracked_in_order(self) -> None:
        fake = FakeSender({})
        domain = WebMCPDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.enable()
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 5
        expected = [
            ("WebMCP.enable", None),
            ("WebMCP.disable", None),
            ("WebMCP.enable", None),
            ("WebMCP.enable", None),
            ("WebMCP.disable", None),
        ]
        assert fake.calls == expected

    async def test_disable_return_passthrough_with_data(self) -> None:
        fake = FakeSender({"status": "disabled"})
        domain = WebMCPDomain(fake)
        result = await domain.disable()
        assert result == {"status": "disabled"}

    async def test_enable_return_passthrough_with_data(self) -> None:
        fake = FakeSender({"status": "enabled"})
        domain = WebMCPDomain(fake)
        result = await domain.enable()
        assert result == {"status": "enabled"}


@pytest.mark.unit
class TestWebMCPNoSpuriousMethodsExplicit:
    def test_no_invoke_tool(self) -> None:
        assert not hasattr(WebMCPDomain, "invoke_tool")

    def test_no_cancel_invocation(self) -> None:
        assert not hasattr(WebMCPDomain, "cancel_invocation")

    def test_no_invoke_tool_method(self) -> None:
        assert not hasattr(WebMCPDomain, "invokeTool")

    def test_no_cancel_invocation_method(self) -> None:
        assert not hasattr(WebMCPDomain, "cancelInvocation")


@pytest.mark.unit
class TestWebMCPClientPropertyDocstring:
    def test_property_docstring_not_stale(self) -> None:
        from cdpwave.client import CDPSession

        doc = CDPSession.web_mcp.__doc__ or ""
        assert "tool invocation" not in doc
        assert "monitoring" in doc
