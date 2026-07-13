"""Edge case unit tests for the CrashReportContext domain."""

import inspect
import typing

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.crash_report_context import CrashReportContextDomain
from tests.unit.fake_sender import FakeSender

PDL_METHODS = ["get_entries"]

PDL_TYPES = ["CrashReportContextEntry"]

PDL_EVENTS: list[str] = []


@pytest.mark.unit
class TestCrashReportContextMethodCoverage:
    def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(CrashReportContextDomain)
            if not name.startswith("_") and callable(getattr(CrashReportContextDomain, name))
        }
        assert public_methods == set(PDL_METHODS)

    def test_method_count_matches_pdl(self) -> None:
        public_methods = [
            name
            for name in CrashReportContextDomain.__dict__
            if not name.startswith("_") and callable(CrashReportContextDomain.__dict__[name])
        ]
        assert len(public_methods) == len(PDL_METHODS)

    def test_order_matches_pdl(self) -> None:
        methods = [
            name
            for name in CrashReportContextDomain.__dict__
            if not name.startswith("_") and callable(CrashReportContextDomain.__dict__[name])
        ]
        assert methods == PDL_METHODS

    def test_inherits_basedomain(self) -> None:
        assert issubclass(CrashReportContextDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        for name in PDL_METHODS:
            method = getattr(CrashReportContextDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_get_entries_signature(self) -> None:
        sig = inspect.signature(CrashReportContextDomain.get_entries)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, typing.Any]


@pytest.mark.unit
class TestCrashReportContextSerialization:
    async def test_get_entries_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = CrashReportContextDomain(fake)
        await domain.get_entries()
        method, params = fake.last_call
        assert method == "CrashReportContext.getEntries"
        assert params is None


@pytest.mark.unit
class TestCrashReportContextReturnPassthrough:
    async def test_get_entries_return_passthrough(self) -> None:
        fake = FakeSender({"entries": []})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert result == {"entries": []}

    async def test_get_entries_with_data(self) -> None:
        entries = [
            {"key": "k1", "value": "v1", "frameId": "frame1"},
            {"key": "k2", "value": "v2", "frameId": "frame2"},
        ]
        fake = FakeSender({"entries": entries})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert result == {"entries": entries}
        assert len(result["entries"]) == 2


@pytest.mark.unit
class TestCrashReportContextLifecycle:
    async def test_repeated_calls(self) -> None:
        fake = FakeSender({})
        domain = CrashReportContextDomain(fake)
        for _ in range(5):
            await domain.get_entries()
        assert len(fake.calls) == 5
        for call in fake.calls:
            assert call == ("CrashReportContext.getEntries", None)


@pytest.mark.unit
class TestCrashReportContextConcurrency:
    async def test_concurrent_calls(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = CrashReportContextDomain(fake)
        await asyncio.gather(
            domain.get_entries(),
            domain.get_entries(),
            domain.get_entries(),
        )
        assert len(fake.calls) == 3
        for call in fake.calls:
            assert call[0] == "CrashReportContext.getEntries"


@pytest.mark.unit
class TestCrashReportContextErrorPropagation:
    async def test_command_error_propagated(self) -> None:
        from cdpwave.exceptions import CommandError

        class ErrorSender:
            async def __call__(
                self, method: str, params: dict | None = None
            ) -> dict:
                raise CommandError(-32000, "Domain not available")

        domain = CrashReportContextDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(CommandError, match="Domain not available"):
            await domain.get_entries()


@pytest.mark.unit
class TestCrashReportContextDocstrings:
    def test_module_describes_domain(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "CrashReportContext" in mod.__doc__
        assert "experimental" in mod.__doc__

    def test_module_lists_types(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        for typ in PDL_TYPES:
            assert typ in mod.__doc__, f"{typ} not in module docstring"

    def test_module_lists_commands(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "getEntries" in mod.__doc__

    def test_class_describes_purpose(self) -> None:
        assert "CrashReportContext" in CrashReportContextDomain.__doc__

    def test_class_marks_experimental(self) -> None:
        assert "experimental" in CrashReportContextDomain.__doc__

    def test_get_entries_has_returns(self) -> None:
        assert "Returns:" in CrashReportContextDomain.get_entries.__doc__

    def test_get_entries_returns_describes_entries(self) -> None:
        doc = CrashReportContextDomain.get_entries.__doc__
        assert "entries" in doc


@pytest.mark.unit
class TestCrashReportContextAdditionalDocstrings:
    def test_module_marks_experimental(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "experimental" in mod.__doc__

    def test_module_lists_dependencies(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "Page" in mod.__doc__

    def test_module_docstring_lists_types_in_order(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "CrashReportContextEntry" in mod.__doc__

    def test_module_lists_no_events(self) -> None:
        import cdpwave.domains.crash_report_context as mod

        assert "(none)" in mod.__doc__

    def test_get_entries_docstring_describes_key_field(self) -> None:
        doc = CrashReportContextDomain.get_entries.__doc__ or ""
        assert "key" in doc

    def test_get_entries_docstring_describes_value_field(self) -> None:
        doc = CrashReportContextDomain.get_entries.__doc__ or ""
        assert "value" in doc

    def test_get_entries_docstring_describes_frame_id_field(self) -> None:
        doc = CrashReportContextDomain.get_entries.__doc__ or ""
        assert "frameId" in doc

    def test_class_describes_crash_report_context_api(self) -> None:
        assert "CrashReportContext" in CrashReportContextDomain.__doc__

    def test_no_deprecated_wording(self) -> None:
        doc = CrashReportContextDomain.get_entries.__doc__ or ""
        assert "Activates" not in doc
        assert "Deactivates" not in doc


@pytest.mark.unit
class TestCrashReportContextAdditionalReturn:
    async def test_get_entries_with_three_entries(self) -> None:
        entries = [
            {"key": "k1", "value": "v1", "frameId": "f1"},
            {"key": "k2", "value": "v2", "frameId": "f2"},
            {"key": "k3", "value": "v3", "frameId": "f3"},
        ]
        fake = FakeSender({"entries": entries})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert len(result["entries"]) == 3
        assert result["entries"][0]["key"] == "k1"
        assert result["entries"][2]["frameId"] == "f3"

    async def test_get_entries_with_unicode_values(self) -> None:
        entries = [
            {"key": "🔑", "value": "值", "frameId": "frame🔑"},
        ]
        fake = FakeSender({"entries": entries})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert result["entries"][0]["key"] == "🔑"
        assert result["entries"][0]["value"] == "值"

    async def test_get_entries_empty_response(self) -> None:
        fake = FakeSender({})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert result == {}

    async def test_get_entries_with_extra_fields(self) -> None:
        fake = FakeSender({"entries": [], "extra": "field"})
        domain = CrashReportContextDomain(fake)
        result = await domain.get_entries()
        assert result == {"entries": [], "extra": "field"}


@pytest.mark.unit
class TestCrashReportContextNoSpuriousMethodsExplicit:
    def test_no_enable(self) -> None:
        assert not hasattr(CrashReportContextDomain, "enable")

    def test_no_disable(self) -> None:
        assert not hasattr(CrashReportContextDomain, "disable")

    def test_no_clear(self) -> None:
        assert not hasattr(CrashReportContextDomain, "clear")

    def test_no_set_entries(self) -> None:
        assert not hasattr(CrashReportContextDomain, "set_entries")


@pytest.mark.unit
class TestCrashReportContextAdditionalErrorPropagation:
    async def test_command_error_not_caught(self) -> None:
        from cdpwave.exceptions import CommandError

        class ErrorSender:
            async def __call__(
                self, method: str, params: dict | None = None
            ) -> dict:
                raise CommandError(-32601, "Method not found")

        domain = CrashReportContextDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(CommandError, match="Method not found"):
            await domain.get_entries()

    async def test_generic_exception_propagated(self) -> None:
        class CrashSender:
            async def __call__(
                self, method: str, params: dict | None = None
            ) -> dict:
                raise RuntimeError("Connection lost")

        domain = CrashReportContextDomain(CrashSender())  # type: ignore[arg-type]
        with pytest.raises(RuntimeError, match="Connection lost"):
            await domain.get_entries()
