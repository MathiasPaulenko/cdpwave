"""Edge case unit tests for the Cast domain."""

import pytest

from cdpwave.domains.cast import CastDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestCastEdgeCases:
    async def test_enable_no_params_sends_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {}

    async def test_enable_with_presentation_url(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url="https://example.com/cast")
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": "https://example.com/cast"}

    async def test_enable_with_empty_presentation_url(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url="")
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": ""}

    async def test_enable_presentation_url_unicode(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url="https://example.com/🔑")
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": "https://example.com/🔑"}

    async def test_enable_presentation_url_int_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=42)  # type: ignore[arg-type]

    async def test_enable_presentation_url_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=True)  # type: ignore[arg-type]

    async def test_enable_presentation_url_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=b"https://example.com")  # type: ignore[arg-type]

    async def test_enable_presentation_url_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url={"url": "test"})  # type: ignore[arg-type]

    async def test_enable_presentation_url_list_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=["url"])  # type: ignore[arg-type]

    async def test_enable_presentation_url_float_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=3.14)  # type: ignore[arg-type]

    async def test_enable_presentation_url_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url=("url",))  # type: ignore[arg-type]

    async def test_enable_presentation_url_set_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="presentation_url must be a string"):
            await domain.enable(presentation_url={"url"})  # type: ignore[arg-type]

    async def test_enable_presentation_url_none_omits(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url=None)
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {}

    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "Cast.disable"
        assert params is None

    async def test_set_sink_to_use_empty_string(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("")
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": ""}

    async def test_set_sink_to_use_unicode(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("sink-🔑")
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": "sink-🔑"}

    async def test_set_sink_to_use_int_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(42)  # type: ignore[arg-type]

    async def test_set_sink_to_use_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(True)  # type: ignore[arg-type]

    async def test_set_sink_to_use_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(b"chromecast")  # type: ignore[arg-type]

    async def test_set_sink_to_use_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use({"name": "test"})  # type: ignore[arg-type]

    async def test_set_sink_to_use_none_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(None)  # type: ignore[arg-type]

    async def test_set_sink_to_use_list_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(["sink"])  # type: ignore[arg-type]

    async def test_set_sink_to_use_float_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(3.14)  # type: ignore[arg-type]

    async def test_set_sink_to_use_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use(("sink",))  # type: ignore[arg-type]

    async def test_set_sink_to_use_set_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.set_sink_to_use({"sink"})  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_empty_string(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_desktop_mirroring("")
        method, params = fake.last_call
        assert method == "Cast.startDesktopMirroring"
        assert params == {"sinkName": ""}

    async def test_start_desktop_mirroring_int_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(42)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(True)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(b"chromecast")  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_none_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(None)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring({"name": "sink"})  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_list_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(["sink"])  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_float_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(3.14)  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring(("sink",))  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_set_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_desktop_mirroring({"sink"})  # type: ignore[arg-type]

    async def test_start_desktop_mirroring_unicode(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_desktop_mirroring("sink-🔑")
        method, params = fake.last_call
        assert method == "Cast.startDesktopMirroring"
        assert params == {"sinkName": "sink-🔑"}

    async def test_start_desktop_mirroring_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_desktop_mirroring(MyStr("sink1"))
        method, params = fake.last_call
        assert method == "Cast.startDesktopMirroring"
        assert params == {"sinkName": "sink1"}

    async def test_type_error_no_cdp_call_start_desktop(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError):
            await domain.start_desktop_mirroring(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_start_tab_mirroring_empty_string(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_tab_mirroring("")
        method, params = fake.last_call
        assert method == "Cast.startTabMirroring"
        assert params == {"sinkName": ""}

    async def test_start_tab_mirroring_int_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(42)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(True)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(b"chromecast")  # type: ignore[arg-type]

    async def test_start_tab_mirroring_none_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(None)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring({"name": "sink"})  # type: ignore[arg-type]

    async def test_start_tab_mirroring_list_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(["sink"])  # type: ignore[arg-type]

    async def test_start_tab_mirroring_float_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(3.14)  # type: ignore[arg-type]

    async def test_start_tab_mirroring_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring(("sink",))  # type: ignore[arg-type]

    async def test_start_tab_mirroring_set_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.start_tab_mirroring({"sink"})  # type: ignore[arg-type]

    async def test_start_tab_mirroring_unicode(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_tab_mirroring("sink-🔑")
        method, params = fake.last_call
        assert method == "Cast.startTabMirroring"
        assert params == {"sinkName": "sink-🔑"}

    async def test_start_tab_mirroring_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.start_tab_mirroring(MyStr("sink1"))
        method, params = fake.last_call
        assert method == "Cast.startTabMirroring"
        assert params == {"sinkName": "sink1"}

    async def test_type_error_no_cdp_call_start_tab(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError):
            await domain.start_tab_mirroring(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_stop_casting_empty_string(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.stop_casting("")
        method, params = fake.last_call
        assert method == "Cast.stopCasting"
        assert params == {"sinkName": ""}

    async def test_stop_casting_int_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(42)  # type: ignore[arg-type]

    async def test_stop_casting_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(True)  # type: ignore[arg-type]

    async def test_stop_casting_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(b"chromecast")  # type: ignore[arg-type]

    async def test_stop_casting_none_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(None)  # type: ignore[arg-type]

    async def test_stop_casting_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting({"name": "sink"})  # type: ignore[arg-type]

    async def test_stop_casting_list_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(["sink"])  # type: ignore[arg-type]

    async def test_stop_casting_float_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(3.14)  # type: ignore[arg-type]

    async def test_stop_casting_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting(("sink",))  # type: ignore[arg-type]

    async def test_stop_casting_set_raises(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError, match="sink_name must be a string"):
            await domain.stop_casting({"sink"})  # type: ignore[arg-type]

    async def test_stop_casting_unicode(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.stop_casting("sink-🔑")
        method, params = fake.last_call
        assert method == "Cast.stopCasting"
        assert params == {"sinkName": "sink-🔑"}

    async def test_stop_casting_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.stop_casting(MyStr("sink1"))
        method, params = fake.last_call
        assert method == "Cast.stopCasting"
        assert params == {"sinkName": "sink1"}

    async def test_type_error_no_cdp_call_stop_casting(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError):
            await domain.stop_casting(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_return_value_passthrough_enable(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.enable()
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_disable(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.disable()
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_set_sink(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.set_sink_to_use("sink1")
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_start_desktop(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.start_desktop_mirroring("sink1")
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_start_tab(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.start_tab_mirroring("sink1")
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_stop_casting(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = CastDomain(fake)
        result = await domain.stop_casting("sink1")
        assert result == {"result": "ok"}

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable()
        await domain.set_sink_to_use("sink1")
        await domain.start_tab_mirroring("sink1")
        await domain.stop_casting("sink1")
        await domain.disable()
        assert len(fake.calls) == 5
        assert fake.calls[0] == ("Cast.enable", {})
        assert fake.calls[1] == ("Cast.setSinkToUse", {"sinkName": "sink1"})
        assert fake.calls[2] == ("Cast.startTabMirroring", {"sinkName": "sink1"})
        assert fake.calls[3] == ("Cast.stopCasting", {"sinkName": "sink1"})
        assert fake.calls[4] == ("Cast.disable", None)

    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url="https://example.com")
        await domain.set_sink_to_use("sink1")
        await domain.start_desktop_mirroring("sink1")
        await domain.start_tab_mirroring("sink1")
        await domain.stop_casting("sink1")
        await domain.disable()
        assert len(fake.calls) == 6
        assert fake.calls[0] == ("Cast.enable", {"presentationUrl": "https://example.com"})
        assert fake.calls[5] == ("Cast.disable", None)

    async def test_enable_then_enable_with_url(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable()
        await domain.enable(presentation_url="https://example.com")
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("Cast.enable", {})
        assert fake.calls[1] == ("Cast.enable", {"presentationUrl": "https://example.com"})

    async def test_disable_without_enable(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("Cast.disable", None)

    async def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(CastDomain)
            if not name.startswith("_") and callable(getattr(CastDomain, name))
        }
        assert public_methods == {
            "enable",
            "disable",
            "set_sink_to_use",
            "start_desktop_mirroring",
            "start_tab_mirroring",
            "stop_casting",
        }

    async def test_order_matches_pdl(self) -> None:
        methods = [
            name for name in CastDomain.__dict__
            if not name.startswith("_") and callable(CastDomain.__dict__[name])
        ]
        assert methods.index("enable") < methods.index("disable")
        assert methods.index("disable") < methods.index("set_sink_to_use")
        assert methods.index("set_sink_to_use") < methods.index("start_desktop_mirroring")
        assert methods.index("start_desktop_mirroring") < methods.index("start_tab_mirroring")
        assert methods.index("start_tab_mirroring") < methods.index("stop_casting")

    async def test_set_sink_to_use_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use(MyStr("sink1"))
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": "sink1"}

    async def test_enable_presentation_url_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.enable(presentation_url=MyStr("https://example.com"))
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": "https://example.com"}

    async def test_type_error_no_cdp_call_set_sink(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_sink_to_use(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_type_error_no_cdp_call_enable(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        with pytest.raises(TypeError):
            await domain.enable(presentation_url=42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_long_sink_name(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        long_name = "s" * 1000
        await domain.set_sink_to_use(long_name)
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": long_name}

    async def test_long_presentation_url(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        long_url = "https://example.com/" + "a" * 2000
        await domain.enable(presentation_url=long_url)
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": long_url}

    async def test_sink_name_with_newline(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("sink\nname")
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": "sink\nname"}

    async def test_sink_name_with_tab(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("sink\tname")
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": "sink\tname"}

    async def test_sink_name_with_null_byte(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        await domain.set_sink_to_use("sink\x00name")
        method, params = fake.last_call
        assert method == "Cast.setSinkToUse"
        assert params == {"sinkName": "sink\x00name"}

    async def test_presentation_url_with_special_chars(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        url = "https://example.com/path?q=1&p=2#frag"
        await domain.enable(presentation_url=url)
        method, params = fake.last_call
        assert method == "Cast.enable"
        assert params == {"presentationUrl": url}

    async def test_concurrent_calls_interleaved(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = CastDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.set_sink_to_use("sink1"),
            domain.start_tab_mirroring("sink1"),
            domain.stop_casting("sink1"),
            domain.disable(),
        )
        assert len(fake.calls) == 5
        methods = [call[0] for call in fake.calls]
        assert "Cast.enable" in methods
        assert "Cast.setSinkToUse" in methods
        assert "Cast.startTabMirroring" in methods
        assert "Cast.stopCasting" in methods
        assert "Cast.disable" in methods

    async def test_enable_disable_cycle_repeated(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("Cast.enable", {})
            assert fake.calls[i * 2 + 1] == ("Cast.disable", None)

    async def test_all_sink_methods_same_sink(self) -> None:
        fake = FakeSender({})
        domain = CastDomain(fake)
        sink = "my-chromecast"
        await domain.set_sink_to_use(sink)
        await domain.start_desktop_mirroring(sink)
        await domain.start_tab_mirroring(sink)
        await domain.stop_casting(sink)
        assert len(fake.calls) == 4
        for call in fake.calls:
            assert call[1] == {"sinkName": sink}
