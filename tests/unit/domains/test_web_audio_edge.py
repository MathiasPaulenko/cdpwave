"""Edge case unit tests for the WebAudio domain."""

import asyncio
import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.web_audio import WebAudioDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestWebAudioEdgeCases:
    """Comprehensive edge-case coverage for WebAudioDomain."""

    # ------------------------------------------------------------------
    # Structure: method order, count, no spurious methods, inheritance,
    # coroutines, signatures.
    # ------------------------------------------------------------------

    def test_method_order_matches_pdl(self) -> None:
        methods = [
            name
            for name in WebAudioDomain.__dict__
            if not name.startswith("_") and callable(WebAudioDomain.__dict__[name])
        ]
        assert methods == ["enable", "disable", "get_realtime_data"]

    def test_method_count(self) -> None:
        public = [
            name
            for name in WebAudioDomain.__dict__
            if not name.startswith("_") and callable(WebAudioDomain.__dict__[name])
        ]
        assert len(public) == 3

    def test_no_spurious_methods(self) -> None:
        public = {
            name
            for name in dir(WebAudioDomain)
            if not name.startswith("_") and callable(getattr(WebAudioDomain, name))
        }
        assert public == {"enable", "disable", "get_realtime_data"}

    def test_inherits_base_domain(self) -> None:
        assert issubclass(WebAudioDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        for name in ("enable", "disable", "get_realtime_data"):
            method = getattr(WebAudioDomain, name)
            assert inspect.iscoroutinefunction(method)

    def test_enable_signature(self) -> None:
        sig = inspect.signature(WebAudioDomain.enable)
        params = list(sig.parameters)
        assert params == ["self"]

    def test_disable_signature(self) -> None:
        sig = inspect.signature(WebAudioDomain.disable)
        params = list(sig.parameters)
        assert params == ["self"]

    def test_get_realtime_data_signature(self) -> None:
        sig = inspect.signature(WebAudioDomain.get_realtime_data)
        params = list(sig.parameters)
        assert params == ["self", "context_id"]

    # ------------------------------------------------------------------
    # enable / disable: params=None, return passthrough.
    # ------------------------------------------------------------------

    async def test_enable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "WebAudio.enable"
        assert params is None

    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "WebAudio.disable"
        assert params is None

    async def test_enable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = WebAudioDomain(fake)
        result = await domain.enable()
        assert result == {"result": "ok"}

    async def test_disable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = WebAudioDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}

    # ------------------------------------------------------------------
    # get_realtime_data: correct params, return passthrough.
    # ------------------------------------------------------------------

    async def test_get_realtime_data_sends_context_id(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.get_realtime_data("ctx-1")
        method, params = fake.last_call
        assert method == "WebAudio.getRealtimeData"
        assert params == {"contextId": "ctx-1"}

    async def test_get_realtime_data_return_passthrough(self) -> None:
        fake = FakeSender({"currentTime": 1.5})
        domain = WebAudioDomain(fake)
        result = await domain.get_realtime_data("ctx-1")
        assert result == {"currentTime": 1.5}

    async def test_get_realtime_data_empty_string(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.get_realtime_data("")
        method, params = fake.last_call
        assert params == {"contextId": ""}

    async def test_get_realtime_data_unicode(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.get_realtime_data("ctx-🎵")
        method, params = fake.last_call
        assert params == {"contextId": "ctx-🎵"}

    async def test_get_realtime_data_long_string(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        cid = "c" * 1000
        await domain.get_realtime_data(cid)
        method, params = fake.last_call
        assert params == {"contextId": cid}

    async def test_get_realtime_data_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.get_realtime_data(MyStr("ctx-1"))
        method, params = fake.last_call
        assert params == {"contextId": "ctx-1"}

    # ------------------------------------------------------------------
    # get_realtime_data: type validation — every wrong type.
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        "bad_value,expected_type",
        [
            (42, "int"),
            (True, "bool"),
            (3.14, "float"),
            (None, "NoneType"),
            (["ctx"], "list"),
            ({"id": "ctx"}, "dict"),
            (b"ctx", "bytes"),
            (("ctx",), "tuple"),
            ({"ctx"}, "set"),
            (complex(1, 2), "complex"),
        ],
        ids=["int", "bool", "float", "none", "list", "dict", "bytes", "tuple", "set", "complex"],
    )
    async def test_get_realtime_data_type_error(
        self, bad_value: object, expected_type: str
    ) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        with pytest.raises(TypeError, match=f"context_id must be a str.*{expected_type}"):
            await domain.get_realtime_data(bad_value)  # type: ignore[arg-type]

    async def test_type_error_no_cdp_call(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        with pytest.raises(TypeError):
            await domain.get_realtime_data(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_type_error_message_includes_actual_type(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        with pytest.raises(TypeError) as exc_info:
            await domain.get_realtime_data(42)  # type: ignore[arg-type]
        assert "int" in str(exc_info.value)

    # ------------------------------------------------------------------
    # Lifecycle, repeated cycles, concurrency, error propagation.
    # ------------------------------------------------------------------

    async def test_lifecycle_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("WebAudio.enable", None)
        assert fake.calls[1] == ("WebAudio.disable", None)

    async def test_repeated_cycles(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("WebAudio.enable", None)
            assert fake.calls[i * 2 + 1] == ("WebAudio.disable", None)

    async def test_concurrency(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.disable(),
            domain.get_realtime_data("ctx-1"),
        )
        assert len(fake.calls) == 3
        methods = [c[0] for c in fake.calls]
        assert "WebAudio.enable" in methods
        assert "WebAudio.disable" in methods
        assert "WebAudio.getRealtimeData" in methods

    async def test_error_propagation_runtime_error(self) -> None:
        class ErrorSender:
            async def __call__(self, method: str, params: dict | None = None) -> dict:
                raise RuntimeError("cdp error")

        domain = WebAudioDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(RuntimeError, match="cdp error"):
            await domain.enable()

    # ------------------------------------------------------------------
    # Multiple calls tracked.
    # ------------------------------------------------------------------

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = WebAudioDomain(fake)
        await domain.enable()
        await domain.get_realtime_data("ctx-a")
        await domain.get_realtime_data("ctx-b")
        await domain.disable()
        assert len(fake.calls) == 4
        assert fake.calls[0] == ("WebAudio.enable", None)
        assert fake.calls[1] == ("WebAudio.getRealtimeData", {"contextId": "ctx-a"})
        assert fake.calls[2] == ("WebAudio.getRealtimeData", {"contextId": "ctx-b"})
        assert fake.calls[3] == ("WebAudio.disable", None)

    # ------------------------------------------------------------------
    # Docstring tests.
    # ------------------------------------------------------------------

    def test_module_docstring_describes_domain(self) -> None:
        from cdpwave.domains import web_audio

        doc = web_audio.__doc__ or ""
        assert "WebAudio" in doc
        assert "experimental" in doc.lower()

    def test_module_docstring_lists_events(self) -> None:
        from cdpwave.domains import web_audio

        doc = web_audio.__doc__ or ""
        assert "contextCreated" in doc
        assert "contextWillBeDestroyed" in doc
        assert "contextChanged" in doc
        assert "audioListenerCreated" in doc
        assert "audioListenerWillBeDestroyed" in doc
        assert "audioNodeCreated" in doc
        assert "audioNodeWillBeDestroyed" in doc
        assert "audioParamCreated" in doc
        assert "audioParamWillBeDestroyed" in doc
        assert "nodesConnected" in doc
        assert "nodesDisconnected" in doc
        assert "nodeParamConnected" in doc
        assert "nodeParamDisconnected" in doc

    def test_module_docstring_lists_commands(self) -> None:
        from cdpwave.domains import web_audio

        doc = web_audio.__doc__ or ""
        assert "enable" in doc
        assert "disable" in doc
        assert "getRealtimeData" in doc

    def test_module_docstring_lists_types(self) -> None:
        from cdpwave.domains import web_audio

        doc = web_audio.__doc__ or ""
        assert "GraphObjectId" in doc
        assert "ContextType" in doc
        assert "ContextState" in doc
        assert "ContextRealtimeData" in doc
        assert "BaseAudioContext" in doc
        assert "AudioListener" in doc
        assert "AudioNode" in doc
        assert "AudioParam" in doc
        assert "NodeType" in doc
        assert "ParamType" in doc
        assert "AutomationRate" in doc
        assert "ChannelCountMode" in doc
        assert "ChannelInterpretation" in doc

    def test_class_docstring_describes_purpose(self) -> None:
        doc = WebAudioDomain.__doc__ or ""
        assert "WebAudio" in doc
        assert "event" in doc.lower()
        assert "experimental" in doc.lower()

    def test_class_docstring_lists_events(self) -> None:
        doc = WebAudioDomain.__doc__ or ""
        assert "contextCreated" in doc
        assert "contextWillBeDestroyed" in doc
        assert "contextChanged" in doc
        assert "audioListenerCreated" in doc
        assert "audioListenerWillBeDestroyed" in doc
        assert "audioNodeCreated" in doc
        assert "audioNodeWillBeDestroyed" in doc
        assert "audioParamCreated" in doc
        assert "audioParamWillBeDestroyed" in doc
        assert "nodesConnected" in doc
        assert "nodesDisconnected" in doc
        assert "nodeParamConnected" in doc
        assert "nodeParamDisconnected" in doc

    def test_enable_docstring_has_returns(self) -> None:
        doc = WebAudioDomain.enable.__doc__ or ""
        assert "Returns:" in doc

    def test_disable_docstring_has_returns(self) -> None:
        doc = WebAudioDomain.disable.__doc__ or ""
        assert "Returns:" in doc

    def test_enable_docstring_lists_all_events(self) -> None:
        doc = WebAudioDomain.enable.__doc__ or ""
        assert "contextCreated" in doc
        assert "contextWillBeDestroyed" in doc
        assert "contextChanged" in doc
        assert "audioListenerCreated" in doc
        assert "audioListenerWillBeDestroyed" in doc
        assert "audioNodeCreated" in doc
        assert "audioNodeWillBeDestroyed" in doc
        assert "audioParamCreated" in doc
        assert "audioParamWillBeDestroyed" in doc
        assert "nodesConnected" in doc
        assert "nodesDisconnected" in doc
        assert "nodeParamConnected" in doc
        assert "nodeParamDisconnected" in doc

    def test_enable_docstring_uses_enable_not_activates(self) -> None:
        doc = WebAudioDomain.enable.__doc__ or ""
        assert "Activates" not in doc
        assert "Enable" in doc

    def test_disable_docstring_uses_disable_not_deactivates(self) -> None:
        doc = WebAudioDomain.disable.__doc__ or ""
        assert "Deactivates" not in doc
        assert "Disable" in doc

    def test_get_realtime_data_docstring_has_args(self) -> None:
        doc = WebAudioDomain.get_realtime_data.__doc__ or ""
        assert "Args:" in doc

    def test_get_realtime_data_docstring_has_returns(self) -> None:
        doc = WebAudioDomain.get_realtime_data.__doc__ or ""
        assert "Returns:" in doc

    def test_get_realtime_data_docstring_has_raises(self) -> None:
        doc = WebAudioDomain.get_realtime_data.__doc__ or ""
        assert "Raises:" in doc

    def test_get_realtime_data_docstring_no_wrong_fields(self) -> None:
        doc = WebAudioDomain.get_realtime_data.__doc__ or ""
        assert "currentValue" not in doc
        assert "currentTick" not in doc

    def test_get_realtime_data_docstring_correct_fields(self) -> None:
        doc = WebAudioDomain.get_realtime_data.__doc__ or ""
        assert "currentTime" in doc
        assert "renderCapacity" in doc
        assert "callbackIntervalMean" in doc
        assert "callbackIntervalVariance" in doc
