"""Edge case unit tests for the DigitalCredentials domain."""

import inspect
import typing

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.digital_credentials import DigitalCredentialsDomain
from tests.unit.fake_sender import FakeSender

PDL_METHODS = ["set_virtual_wallet_behavior"]

PDL_TYPES = ["VirtualWalletAction"]

PDL_EVENTS: list[str] = []


@pytest.mark.unit
class TestDigitalCredentialsMethodCoverage:
    def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(DigitalCredentialsDomain)
            if not name.startswith("_") and callable(getattr(DigitalCredentialsDomain, name))
        }
        assert public_methods == set(PDL_METHODS)

    def test_method_count_matches_pdl(self) -> None:
        public_methods = [
            name
            for name in DigitalCredentialsDomain.__dict__
            if not name.startswith("_") and callable(DigitalCredentialsDomain.__dict__[name])
        ]
        assert len(public_methods) == len(PDL_METHODS)

    def test_order_matches_pdl(self) -> None:
        methods = [
            name
            for name in DigitalCredentialsDomain.__dict__
            if not name.startswith("_") and callable(DigitalCredentialsDomain.__dict__[name])
        ]
        assert methods == PDL_METHODS

    def test_inherits_basedomain(self) -> None:
        assert issubclass(DigitalCredentialsDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        for name in PDL_METHODS:
            method = getattr(DigitalCredentialsDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_set_virtual_wallet_behavior_signature(self) -> None:
        sig = inspect.signature(DigitalCredentialsDomain.set_virtual_wallet_behavior)
        params = list(sig.parameters.keys())
        assert params == ["self", "action", "protocol", "response", "frame_id"]
        assert sig.parameters["action"].default is inspect.Parameter.empty
        assert sig.parameters["protocol"].default is None
        assert sig.parameters["response"].default is None
        assert sig.parameters["frame_id"].default is None
        assert sig.return_annotation == dict[str, typing.Any]


@pytest.mark.unit
class TestDigitalCredentialsSerialization:
    async def test_action_only(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline")
        method, params = fake.last_call
        assert method == "DigitalCredentials.setVirtualWalletBehavior"
        assert params == {"action": "decline"}

    async def test_action_with_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", protocol="openid4vp"
        )
        method, params = fake.last_call
        assert params == {"action": "respond", "protocol": "openid4vp"}

    async def test_action_with_response(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response={"token": "abc123"}
        )
        method, params = fake.last_call
        assert params == {"action": "respond", "response": {"token": "abc123"}}

    async def test_action_with_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "wait", frame_id="frame123"
        )
        method, params = fake.last_call
        assert params == {"action": "wait", "frameId": "frame123"}

    async def test_all_params(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond",
            protocol="openid4vp",
            response={"token": "abc"},
            frame_id="frame1",
        )
        method, params = fake.last_call
        assert params == {
            "action": "respond",
            "protocol": "openid4vp",
            "response": {"token": "abc"},
            "frameId": "frame1",
        }

    async def test_optional_params_omitted_when_none(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("clear")
        method, params = fake.last_call
        assert params == {"action": "clear"}
        assert "protocol" not in params
        assert "response" not in params
        assert "frameId" not in params

    async def test_camel_case_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline", frame_id="F1")
        method, params = fake.last_call
        assert "frameId" in params
        assert "frame_id" not in params


@pytest.mark.unit
class TestDigitalCredentialsTypeValidation:
    async def test_action_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]

    async def test_action_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(True)  # type: ignore[arg-type]

    async def test_action_float_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(3.14)  # type: ignore[arg-type]

    async def test_action_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(b"respond")  # type: ignore[arg-type]

    async def test_action_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior({"a": 1})  # type: ignore[arg-type]

    async def test_action_list_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(["respond"])  # type: ignore[arg-type]

    async def test_action_none_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(None)  # type: ignore[arg-type]

    async def test_protocol_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=42)  # type: ignore[arg-type]

    async def test_protocol_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=True)  # type: ignore[arg-type]

    async def test_protocol_float_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=3.14)  # type: ignore[arg-type]

    async def test_protocol_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=b"x")  # type: ignore[arg-type]

    async def test_protocol_list_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=["x"])  # type: ignore[arg-type]

    async def test_response_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=42)  # type: ignore[arg-type]

    async def test_response_str_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response="x")  # type: ignore[arg-type]

    async def test_response_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=True)  # type: ignore[arg-type]

    async def test_response_list_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=[1])  # type: ignore[arg-type]

    async def test_response_float_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=3.14)  # type: ignore[arg-type]

    async def test_frame_id_int_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=42)  # type: ignore[arg-type]

    async def test_frame_id_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=True)  # type: ignore[arg-type]

    async def test_frame_id_float_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=3.14)  # type: ignore[arg-type]

    async def test_frame_id_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=b"f")  # type: ignore[arg-type]

    async def test_frame_id_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id={"a": 1})  # type: ignore[arg-type]

    async def test_frame_id_list_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=["f"])  # type: ignore[arg-type]


@pytest.mark.unit
class TestDigitalCredentialsValidationOrder:
    async def test_action_validated_before_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42, protocol=99)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_protocol_validated_before_response(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=99, response=42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_response_validated_before_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=42, frame_id=99)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_type_error_no_cdp_call(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestDigitalCredentialsSubclassAcceptance:
    async def test_action_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(MyStr("decline"))
        method, params = fake.last_call
        assert params == {"action": "decline"}

    async def test_protocol_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", protocol=MyStr("openid4vp")
        )
        method, params = fake.last_call
        assert params == {"action": "respond", "protocol": "openid4vp"}

    async def test_frame_id_str_subclass_accepted(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "decline", frame_id=MyStr("frame1")
        )
        method, params = fake.last_call
        assert params == {"action": "decline", "frameId": "frame1"}


@pytest.mark.unit
class TestDigitalCredentialsEdgeValues:
    async def test_empty_string_action_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="action must be"):
            await domain.set_virtual_wallet_behavior("")

    async def test_unicode_action_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="action must be"):
            await domain.set_virtual_wallet_behavior("respond🔑")

    async def test_empty_string_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("respond", protocol="")
        method, params = fake.last_call
        assert params == {"action": "respond", "protocol": ""}

    async def test_empty_string_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline", frame_id="")
        method, params = fake.last_call
        assert params == {"action": "decline", "frameId": ""}

    async def test_empty_response_dict(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("respond", response={})
        method, params = fake.last_call
        assert params == {"action": "respond", "response": {}}

    async def test_none_optionals_explicit(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "decline", protocol=None, response=None, frame_id=None
        )
        method, params = fake.last_call
        assert params == {"action": "decline"}


@pytest.mark.unit
class TestDigitalCredentialsReturnPassthrough:
    async def test_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = DigitalCredentialsDomain(fake)
        result = await domain.set_virtual_wallet_behavior("decline")
        assert result == {"result": "ok"}


@pytest.mark.unit
class TestDigitalCredentialsConcurrency:
    async def test_concurrent_calls(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await asyncio.gather(
            domain.set_virtual_wallet_behavior("decline"),
            domain.set_virtual_wallet_behavior("wait"),
            domain.set_virtual_wallet_behavior("clear"),
        )
        assert len(fake.calls) == 3
        actions = [call[1]["action"] for call in fake.calls]
        assert "decline" in actions
        assert "wait" in actions
        assert "clear" in actions


@pytest.mark.unit
class TestDigitalCredentialsErrorPropagation:
    async def test_command_error_propagated(self) -> None:
        from cdpwave.exceptions import CommandError

        class ErrorSender:
            async def __call__(
                self, method: str, params: dict | None = None
            ) -> dict:
                raise CommandError(-32000, "Domain not available")

        domain = DigitalCredentialsDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(CommandError, match="Domain not available"):
            await domain.set_virtual_wallet_behavior("decline")

    async def test_type_error_not_caught(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestDigitalCredentialsRepeatedCalls:
    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline")
        await domain.set_virtual_wallet_behavior("wait")
        await domain.set_virtual_wallet_behavior("respond", protocol="openid4vp")
        assert len(fake.calls) == 3
        assert fake.calls[0] == (
            "DigitalCredentials.setVirtualWalletBehavior",
            {"action": "decline"},
        )
        assert fake.calls[1] == (
            "DigitalCredentials.setVirtualWalletBehavior",
            {"action": "wait"},
        )
        assert fake.calls[2] == (
            "DigitalCredentials.setVirtualWalletBehavior",
            {"action": "respond", "protocol": "openid4vp"},
        )


@pytest.mark.unit
class TestDigitalCredentialsDocstrings:
    def test_module_describes_domain(self) -> None:
        import cdpwave.domains.digital_credentials as mod

        assert "DigitalCredentials" in mod.__doc__
        assert "experimental" in mod.__doc__

    def test_module_lists_types(self) -> None:
        import cdpwave.domains.digital_credentials as mod

        for typ in PDL_TYPES:
            assert typ in mod.__doc__, f"{typ} not in module docstring"

    def test_module_lists_commands(self) -> None:
        import cdpwave.domains.digital_credentials as mod

        assert "setVirtualWalletBehavior" in mod.__doc__

    def test_class_describes_purpose(self) -> None:
        assert "Digital Credentials" in DigitalCredentialsDomain.__doc__

    def test_class_marks_experimental(self) -> None:
        assert "experimental" in DigitalCredentialsDomain.__doc__

    def test_method_has_args(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__
        assert "Args:" in doc

    def test_method_has_returns(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__
        assert "Returns:" in doc

    def test_method_has_raises(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__
        assert "Raises:" in doc

    def test_method_docstring_mentions_value_error(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__ or ""
        assert "ValueError" in doc

    def test_method_lists_enum_values(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__
        assert "respond" in doc
        assert "decline" in doc
        assert "wait" in doc
        assert "clear" in doc

    def test_no_deprecated_wording(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__
        assert "Activates" not in doc
        assert "Deactivates" not in doc


@pytest.mark.unit
class TestDigitalCredentialsAdditionalDocstrings:
    def test_module_marks_experimental(self) -> None:
        import cdpwave.domains.digital_credentials as mod

        assert "experimental" in mod.__doc__

    def test_module_lists_no_events(self) -> None:
        import cdpwave.domains.digital_credentials as mod

        assert "(none)" in mod.__doc__

    def test_class_describes_virtual_wallet(self) -> None:
        assert "virtual wallet" in DigitalCredentialsDomain.__doc__

    def test_method_docstring_describes_protocol(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__ or ""
        assert "protocol" in doc

    def test_method_docstring_describes_response(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__ or ""
        assert "response" in doc

    def test_method_docstring_no_misleading_required_when(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__ or ""
        assert "Required when" not in doc
        assert "forbidden" not in doc

    def test_method_docstring_describes_frame_id(self) -> None:
        doc = DigitalCredentialsDomain.set_virtual_wallet_behavior.__doc__ or ""
        assert "frame_id" in doc


@pytest.mark.unit
class TestDigitalCredentialsAdditionalTypeValidation:
    async def test_action_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(("respond",))  # type: ignore[arg-type]

    async def test_action_set_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior({"respond"})  # type: ignore[arg-type]

    async def test_protocol_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol={"a": 1})  # type: ignore[arg-type]

    async def test_protocol_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=("x",))  # type: ignore[arg-type]

    async def test_protocol_set_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol={"x"})  # type: ignore[arg-type]

    async def test_protocol_none_accepted(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("respond", protocol=None)
        method, params = fake.last_call
        assert "protocol" not in params

    async def test_response_none_accepted(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("respond", response=None)
        method, params = fake.last_call
        assert "response" not in params

    async def test_frame_id_none_accepted(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline", frame_id=None)
        method, params = fake.last_call
        assert "frameId" not in params

    async def test_response_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=b"x")  # type: ignore[arg-type]

    async def test_response_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response=(1, 2))  # type: ignore[arg-type]

    async def test_response_set_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="response must be a dict"):
            await domain.set_virtual_wallet_behavior("respond", response={1})  # type: ignore[arg-type]

    async def test_frame_id_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id=("f",))  # type: ignore[arg-type]

    async def test_frame_id_set_raises(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="frame_id must be a str"):
            await domain.set_virtual_wallet_behavior("decline", frame_id={"f"})  # type: ignore[arg-type]

    async def test_response_dict_subclass_accepted(self) -> None:
        class MyDict(dict):
            pass

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response=MyDict({"token": "abc"})
        )
        method, params = fake.last_call
        assert params["response"] == {"token": "abc"}


@pytest.mark.unit
class TestDigitalCredentialsAllEnumValues:
    @pytest.mark.parametrize("action", ["respond", "decline", "wait", "clear"])
    async def test_each_enum_value(self, action: str) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(action)
        method, params = fake.last_call
        assert params == {"action": action}


@pytest.mark.unit
class TestDigitalCredentialsAdditionalEdgeValues:
    async def test_unicode_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("respond", protocol="openid🔑")
        method, params = fake.last_call
        assert params["protocol"] == "openid🔑"

    async def test_unicode_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline", frame_id="frame🔑")
        method, params = fake.last_call
        assert params["frameId"] == "frame🔑"

    async def test_response_with_nested_dict(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        nested = {"outer": {"inner": "value"}}
        await domain.set_virtual_wallet_behavior("respond", response=nested)
        method, params = fake.last_call
        assert params["response"] == {"outer": {"inner": "value"}}

    async def test_response_with_list_values(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response={"items": [1, 2, 3]}
        )
        method, params = fake.last_call
        assert params["response"] == {"items": [1, 2, 3]}

    async def test_response_with_int_values(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response={"count": 42}
        )
        method, params = fake.last_call
        assert params["response"] == {"count": 42}

    async def test_response_with_bool_values(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response={"ok": True}
        )
        method, params = fake.last_call
        assert params["response"] == {"ok": True}

    async def test_long_string_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        long_proto = "p" * 1000
        await domain.set_virtual_wallet_behavior("respond", protocol=long_proto)
        method, params = fake.last_call
        assert params["protocol"] == long_proto

    async def test_long_string_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        long_fid = "f" * 1000
        await domain.set_virtual_wallet_behavior("decline", frame_id=long_fid)
        method, params = fake.last_call
        assert params["frameId"] == long_fid


@pytest.mark.unit
class TestDigitalCredentialsAdditionalValidationOrder:
    async def test_action_validated_before_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42, frame_id=99)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_protocol_validated_before_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="protocol must be a str"):
            await domain.set_virtual_wallet_behavior("respond", protocol=99, frame_id=99)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_action_validated_before_response(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42, response={"a": 1})  # type: ignore[arg-type]
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestDigitalCredentialsAdditionalConcurrency:
    async def test_concurrent_calls_with_all_params(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await asyncio.gather(
            domain.set_virtual_wallet_behavior("respond", protocol="openid4vp"),
            domain.set_virtual_wallet_behavior("decline", frame_id="f1"),
            domain.set_virtual_wallet_behavior(
                "respond", response={"token": "abc"}
            ),
            domain.set_virtual_wallet_behavior("clear"),
        )
        assert len(fake.calls) == 4
        actions = [call[1]["action"] for call in fake.calls]
        assert "respond" in actions
        assert "decline" in actions
        assert "clear" in actions


@pytest.mark.unit
class TestDigitalCredentialsNoSpuriousMethodsExplicit:
    def test_no_enable(self) -> None:
        assert not hasattr(DigitalCredentialsDomain, "enable")

    def test_no_disable(self) -> None:
        assert not hasattr(DigitalCredentialsDomain, "disable")

    def test_no_get(self) -> None:
        assert not hasattr(DigitalCredentialsDomain, "get")

    def test_no_set_behavior(self) -> None:
        assert not hasattr(DigitalCredentialsDomain, "set_behavior")


@pytest.mark.unit
class TestDigitalCredentialsEnumValidation:
    async def test_invalid_action_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="action must be"):
            await domain.set_virtual_wallet_behavior("invalid")

    async def test_empty_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="action must be"):
            await domain.set_virtual_wallet_behavior("")

    async def test_typo_action_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="action must be"):
            await domain.set_virtual_wallet_behavior("responnd")

    async def test_value_error_no_cdp_call(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError):
            await domain.set_virtual_wallet_behavior("invalid")
        assert len(fake.calls) == 0

    async def test_type_error_raised_before_value_error(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(TypeError, match="action must be a str"):
            await domain.set_virtual_wallet_behavior(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_valid_enum_values_pass(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        for action in ("respond", "decline", "wait", "clear"):
            await domain.set_virtual_wallet_behavior(action)
        assert len(fake.calls) == 4

    async def test_value_error_message_includes_action(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        with pytest.raises(ValueError, match="invalid"):
            await domain.set_virtual_wallet_behavior("invalid")


@pytest.mark.unit
class TestDigitalCredentialsAdditionalSerialization:
    async def test_protocol_and_response_without_frame_id(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", protocol="openid4vp", response={"token": "abc"}
        )
        method, params = fake.last_call
        assert params == {
            "action": "respond",
            "protocol": "openid4vp",
            "response": {"token": "abc"},
        }
        assert "frameId" not in params

    async def test_response_and_frame_id_without_protocol(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", response={"token": "x"}, frame_id="f1"
        )
        method, params = fake.last_call
        assert params == {
            "action": "respond",
            "response": {"token": "x"},
            "frameId": "f1",
        }
        assert "protocol" not in params

    async def test_protocol_and_frame_id_without_response(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior(
            "respond", protocol="openid4vp", frame_id="f1"
        )
        method, params = fake.last_call
        assert params == {
            "action": "respond",
            "protocol": "openid4vp",
            "frameId": "f1",
        }
        assert "response" not in params

    async def test_params_dict_is_not_none(self) -> None:
        fake = FakeSender({})
        domain = DigitalCredentialsDomain(fake)
        await domain.set_virtual_wallet_behavior("decline")
        method, params = fake.last_call
        assert params is not None
        assert isinstance(params, dict)
