"""Unit tests for the Security domain.

Covers all 6 CDP Security commands (disable, enable,
setIgnoreCertificateErrors, handleCertificateError,
setOverrideCertificateErrors, getVisibleSecurityState) with FakeSender —
parameter verification, type/enum validation, return values, CommandError
propagation, method parity, coroutine checks, concurrency, and edge cases.
"""

import asyncio
import inspect
from typing import Any

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.security import SecurityDomain
from cdpwave.exceptions import CommandError
from tests.unit.fake_sender import FakeSender


class ErrorSender:
    """Sender that raises CommandError on every call."""

    def __init__(self, code: int = -32000, message: str = "Server error") -> None:
        self._code = code
        self._message = message
        self._calls: list[tuple[str, dict[str, Any] | None]] = []

    async def __call__(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._calls.append((method, params))
        raise CommandError(self._code, self._message)

    @property
    def calls(self) -> list[tuple[str, dict[str, Any] | None]]:
        return self._calls

    @property
    def last_call(self) -> tuple[str, dict[str, Any] | None]:
        return self._calls[-1]


# ---------------------------------------------------------------------------
# disable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDisable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Security.disable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        result = await domain.disable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = SecurityDomain(fake)
        result = await domain.disable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.disable()
        method, _ = fake.last_call
        assert method == "Security.disable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.disable()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# enable
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnable:
    async def test_params_none(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Security.enable", None)

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        result = await domain.enable()
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = SecurityDomain(fake)
        result = await domain.enable()
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.enable()
        method, _ = fake.last_call
        assert method == "Security.enable"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.enable()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# set_ignore_certificate_errors
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetIgnoreCertificateErrors:
    async def test_params_true(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        method, params = fake.last_call
        assert method == "Security.setIgnoreCertificateErrors"
        assert params is not None
        assert params["ignore"] is True

    async def test_params_false(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(False)
        method, params = fake.last_call
        assert method == "Security.setIgnoreCertificateErrors"
        assert params is not None
        assert params["ignore"] is False

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        result = await domain.set_ignore_certificate_errors(True)
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = SecurityDomain(fake)
        result = await domain.set_ignore_certificate_errors(True)
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        method, _ = fake.last_call
        assert method == "Security.setIgnoreCertificateErrors"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        assert len(fake.calls) == 1

    async def test_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["ignore"]

    async def test_camel_case_key(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert "ignore" in params

    async def test_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        first_params = fake.calls[0][1]
        await domain.set_ignore_certificate_errors(True)
        second_params = fake.calls[1][1]
        assert first_params is not None
        assert second_params is not None
        assert first_params is not second_params
        assert first_params == second_params


# ---------------------------------------------------------------------------
# handle_certificate_error
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHandleCertificateError:
    async def test_params_continue(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        method, params = fake.last_call
        assert method == "Security.handleCertificateError"
        assert params is not None
        assert params["eventId"] == 1
        assert params["action"] == "continue"

    async def test_params_cancel(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(2, "cancel")
        method, params = fake.last_call
        assert method == "Security.handleCertificateError"
        assert params is not None
        assert params["eventId"] == 2
        assert params["action"] == "cancel"

    async def test_params_zero_event_id(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(0, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == 0

    async def test_params_negative_event_id(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(-1, "cancel")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == -1

    async def test_params_large_event_id(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(999999999, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == 999999999

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        result = await domain.handle_certificate_error(1, "continue")
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = SecurityDomain(fake)
        result = await domain.handle_certificate_error(1, "continue")
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        method, _ = fake.last_call
        assert method == "Security.handleCertificateError"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        assert len(fake.calls) == 1

    async def test_only_keys_in_params(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        _, params = fake.last_call
        assert params is not None
        assert set(params.keys()) == {"eventId", "action"}

    async def test_camel_case_keys(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        _, params = fake.last_call
        assert params is not None
        assert "eventId" in params
        assert "action" in params
        assert "event_id" not in params

    async def test_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        first_params = fake.calls[0][1]
        await domain.handle_certificate_error(1, "continue")
        second_params = fake.calls[1][1]
        assert first_params is not None
        assert second_params is not None
        assert first_params is not second_params
        assert first_params == second_params


# ---------------------------------------------------------------------------
# set_override_certificate_errors
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetOverrideCertificateErrors:
    async def test_params_true(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        method, params = fake.last_call
        assert method == "Security.setOverrideCertificateErrors"
        assert params is not None
        assert params["override"] is True

    async def test_params_false(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(False)
        method, params = fake.last_call
        assert method == "Security.setOverrideCertificateErrors"
        assert params is not None
        assert params["override"] is False

    async def test_returns_empty(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        result = await domain.set_override_certificate_errors(True)
        assert result == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"ok": True})
        domain = SecurityDomain(fake)
        result = await domain.set_override_certificate_errors(True)
        assert result == {"ok": True}

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        method, _ = fake.last_call
        assert method == "Security.setOverrideCertificateErrors"

    async def test_single_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        assert len(fake.calls) == 1

    async def test_only_key_in_params(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert list(params.keys()) == ["override"]

    async def test_camel_case_key(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert "override" in params

    async def test_creates_new_dict_each_call(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        first_params = fake.calls[0][1]
        await domain.set_override_certificate_errors(True)
        second_params = fake.calls[1][1]
        assert first_params is not None
        assert second_params is not None
        assert first_params is not second_params
        assert first_params == second_params


# ---------------------------------------------------------------------------
# get_visible_security_state
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetVisibleSecurityState:
    async def test_params_none(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.get_visible_security_state()
        assert fake.last_call == ("Security.getVisibleSecurityState", None)

    async def test_returns_visible_security_state(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "secure",
                "certificateSecurityState": {
                    "protocol": "TLS 1.3",
                    "keyExchange": "X25519",
                    "cipher": "AES_256_GCM",
                    "certificate": ["cert1", "cert2"],
                    "subjectName": "example.com",
                    "issuer": "CA",
                    "validFrom": 1234567890,
                    "validTo": 1234567890,
                    "certificateHasWeakSignature": False,
                    "certificateHasSha1Signature": False,
                    "modernSSL": True,
                    "obsoleteSslProtocol": False,
                    "obsoleteSslKeyExchange": False,
                    "obsoleteSslCipher": False,
                    "obsoleteSslSignature": False,
                },
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert "visibleSecurityState" in result
        state = result["visibleSecurityState"]
        assert state["securityState"] == "secure"
        assert state["certificateSecurityState"]["protocol"] == "TLS 1.3"

    async def test_returns_minimal_state(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "neutral",
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert result["visibleSecurityState"]["securityState"] == "neutral"

    async def test_returns_empty_state(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert "visibleSecurityState" in result

    async def test_returns_response_with_extra_keys(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {"securityState": "info"},
            "extra": "data",
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert "visibleSecurityState" in result
        assert "extra" in result

    async def test_exact_cdp_method_name(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.get_visible_security_state()
        method, _ = fake.last_call
        assert method == "Security.getVisibleSecurityState"

    async def test_single_call(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.get_visible_security_state()
        assert len(fake.calls) == 1

    async def test_sends_none_not_empty_dict(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.get_visible_security_state()
        _, params = fake.last_call
        assert params is None


# ---------------------------------------------------------------------------
# Type validation — set_ignore_certificate_errors
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetIgnoreCertificateErrorsTypeValidation:
    async def test_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(1)
        assert len(fake.calls) == 0

    async def test_int_zero_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(0)
        assert len(fake.calls) == 0

    async def test_str_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors("true")
        assert len(fake.calls) == 0

    async def test_none_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(None)
        assert len(fake.calls) == 0

    async def test_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(1.0)
        assert len(fake.calls) == 0

    async def test_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors([True])
        assert len(fake.calls) == 0

    async def test_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors({"ignore": True})
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — handle_certificate_error (event_id)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHandleCertificateErrorEventIdTypeValidation:
    async def test_none_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(None, "continue")
        assert len(fake.calls) == 0

    async def test_str_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error("1", "continue")
        assert len(fake.calls) == 0

    async def test_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(1.5, "continue")
        assert len(fake.calls) == 0

    async def test_bool_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(True, "continue")
        assert len(fake.calls) == 0

    async def test_false_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(False, "continue")
        assert len(fake.calls) == 0

    async def test_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error([1], "continue")
        assert len(fake.calls) == 0

    async def test_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error({"eventId": 1}, "continue")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — handle_certificate_error (action)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHandleCertificateErrorActionTypeValidation:
    async def test_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, 123)
        assert len(fake.calls) == 0

    async def test_none_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, None)
        assert len(fake.calls) == 0

    async def test_bool_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, True)
        assert len(fake.calls) == 0

    async def test_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, ["continue"])
        assert len(fake.calls) == 0

    async def test_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, {"action": "continue"})
        assert len(fake.calls) == 0

    async def test_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, 1.0)
        assert len(fake.calls) == 0

    async def test_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, b"continue")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Enum validation — handle_certificate_error (action)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHandleCertificateErrorActionEnumValidation:
    async def test_empty_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "")
        assert len(fake.calls) == 0

    async def test_uppercase_continue_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "Continue")
        assert len(fake.calls) == 0

    async def test_uppercase_cancel_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "Cancel")
        assert len(fake.calls) == 0

    async def test_random_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "abc")
        assert len(fake.calls) == 0

    async def test_whitespace_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, " ")
        assert len(fake.calls) == 0

    async def test_continue_with_spaces_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, " continue ")
        assert len(fake.calls) == 0

    async def test_long_string_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "a" * 10000)
        assert len(fake.calls) == 0

    async def test_unicode_raises_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "continue\u00f1")
        assert len(fake.calls) == 0

    async def test_type_error_takes_precedence_over_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error("1", "bad_action")
        assert len(fake.calls) == 0

    async def test_action_type_error_before_enum_check(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, 123)
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Type validation — set_override_certificate_errors
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetOverrideCertificateErrorsTypeValidation:
    async def test_int_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(1)
        assert len(fake.calls) == 0

    async def test_int_zero_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(0)
        assert len(fake.calls) == 0

    async def test_str_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors("true")
        assert len(fake.calls) == 0

    async def test_none_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(None)
        assert len(fake.calls) == 0

    async def test_float_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(1.0)
        assert len(fake.calls) == 0

    async def test_list_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors([True])
        assert len(fake.calls) == 0

    async def test_dict_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors({"override": True})
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Method parity
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodParity:
    def test_six_methods_exist(self) -> None:
        methods = [
            attr for attr in dir(SecurityDomain)
            if not attr.startswith("_") and callable(getattr(SecurityDomain, attr))
        ]
        assert "disable" in methods
        assert "enable" in methods
        assert "set_ignore_certificate_errors" in methods
        assert "handle_certificate_error" in methods
        assert "set_override_certificate_errors" in methods
        assert "get_visible_security_state" in methods

    def test_no_extra_methods(self) -> None:
        expected = {
            "disable",
            "enable",
            "set_ignore_certificate_errors",
            "handle_certificate_error",
            "set_override_certificate_errors",
            "get_visible_security_state",
        }
        actual = {
            attr for attr in dir(SecurityDomain)
            if not attr.startswith("_")
            and callable(getattr(SecurityDomain, attr))
        }
        domain_methods = actual - set(dir(BaseDomain))
        assert domain_methods == expected

    def test_all_coroutines(self) -> None:
        for name in (
            "disable",
            "enable",
            "set_ignore_certificate_errors",
            "handle_certificate_error",
            "set_override_certificate_errors",
            "get_visible_security_state",
        ):
            method = getattr(SecurityDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_isinstance_base_domain(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        assert isinstance(domain, BaseDomain)

    def test_alphabetical_order(self) -> None:
        methods = [
            name for name, value in SecurityDomain.__dict__.items()
            if not name.startswith("_")
            and inspect.iscoroutinefunction(value)
        ]
        assert methods == sorted(methods), f"Methods not in alphabetical order: {methods}"

    def test_no_alias_attribute(self) -> None:
        assert not hasattr(SecurityDomain, "set_ignore_certificate_errors") or \
            SecurityDomain.set_ignore_certificate_errors is not \
            SecurityDomain.set_override_certificate_errors

    def test_set_ignore_is_distinct_method(self) -> None:
        assert (
            SecurityDomain.set_ignore_certificate_errors
            is not SecurityDomain.set_override_certificate_errors
        )


# ---------------------------------------------------------------------------
# Method signatures
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMethodSignatures:
    def test_disable_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.disable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_enable_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.enable)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_set_ignore_certificate_errors_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.set_ignore_certificate_errors)
        params = list(sig.parameters.keys())
        assert params == ["self", "ignore"]
        assert sig.parameters["ignore"].annotation is bool
        assert sig.return_annotation == dict[str, Any]

    def test_handle_certificate_error_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.handle_certificate_error)
        params = list(sig.parameters.keys())
        assert params == ["self", "event_id", "action"]
        assert sig.parameters["event_id"].annotation is int
        assert sig.parameters["action"].annotation is str
        assert sig.return_annotation == dict[str, Any]

    def test_set_override_certificate_errors_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.set_override_certificate_errors)
        params = list(sig.parameters.keys())
        assert params == ["self", "override"]
        assert sig.parameters["override"].annotation is bool
        assert sig.return_annotation == dict[str, Any]

    def test_get_visible_security_state_signature(self) -> None:
        sig = inspect.signature(SecurityDomain.get_visible_security_state)
        params = list(sig.parameters.keys())
        assert params == ["self"]
        assert sig.return_annotation == dict[str, Any]

    def test_all_methods_have_docstrings(self) -> None:
        for name in (
            "disable",
            "enable",
            "set_ignore_certificate_errors",
            "handle_certificate_error",
            "set_override_certificate_errors",
            "get_visible_security_state",
        ):
            method = getattr(SecurityDomain, name)
            assert method.__doc__ is not None, f"{name} missing docstring"
            assert len(method.__doc__) > 10, f"{name} docstring too short"

    def test_class_has_docstring(self) -> None:
        assert SecurityDomain.__doc__ is not None
        assert "Security" in SecurityDomain.__doc__

    def test_module_has_docstring(self) -> None:
        import cdpwave.domains.security as sec_mod
        assert sec_mod.__doc__ is not None
        assert "Security" in sec_mod.__doc__

    def test_module_docstring_mentions_events(self) -> None:
        import cdpwave.domains.security as sec_mod
        doc = sec_mod.__doc__ or ""
        assert "certificateError" in doc
        assert "securityStateChanged" in doc
        assert "visibleSecurityStateChanged" in doc

    def test_class_docstring_mentions_events(self) -> None:
        doc = SecurityDomain.__doc__ or ""
        assert "certificateError" in doc
        assert "securityStateChanged" in doc
        assert "visibleSecurityStateChanged" in doc

    def test_handle_certificate_error_docstring_mentions_deprecated(self) -> None:
        doc = SecurityDomain.handle_certificate_error.__doc__ or ""
        assert "Deprecated" in doc or "deprecated" in doc

    def test_set_override_certificate_errors_docstring_mentions_deprecated(self) -> None:
        doc = SecurityDomain.set_override_certificate_errors.__doc__ or ""
        assert "Deprecated" in doc or "deprecated" in doc

    def test_get_visible_security_state_docstring_mentions_experimental(self) -> None:
        doc = SecurityDomain.get_visible_security_state.__doc__ or ""
        assert "Experimental" in doc or "experimental" in doc


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagation:
    async def test_disable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32000, message="Disable failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -32000
        assert "Disable failed" in exc_info.value.message

    async def test_enable_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32001, message="Enable failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == -32001
        assert "Enable failed" in exc_info.value.message

    async def test_set_ignore_certificate_errors_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32002, message="SetIgnore failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.set_ignore_certificate_errors(True)
        assert exc_info.value.code == -32002
        assert "SetIgnore failed" in exc_info.value.message

    async def test_handle_certificate_error_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32003, message="HandleCert failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.handle_certificate_error(1, "continue")
        assert exc_info.value.code == -32003
        assert "HandleCert failed" in exc_info.value.message

    async def test_set_override_certificate_errors_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32004, message="SetOverride failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.set_override_certificate_errors(True)
        assert exc_info.value.code == -32004
        assert "SetOverride failed" in exc_info.value.message

    async def test_get_visible_security_state_raises_command_error(self) -> None:
        sender = ErrorSender(code=-32005, message="GetVisible failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.get_visible_security_state()
        assert exc_info.value.code == -32005
        assert "GetVisible failed" in exc_info.value.message

    async def test_error_sender_records_call_before_raising(self) -> None:
        sender = ErrorSender()
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 1
        assert sender.calls[0][0] == "Security.disable"

    async def test_error_stops_execution(self) -> None:
        sender = ErrorSender()
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError):
            await domain.enable()
        with pytest.raises(CommandError):
            await domain.disable()
        assert len(sender.calls) == 2


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_100_concurrent_disable(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(*[domain.disable() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_100_concurrent_enable(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(*[domain.enable() for _ in range(100)])
        assert len(fake.calls) == 100

    async def test_100_concurrent_set_ignore(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.set_ignore_certificate_errors(True) for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_100_concurrent_handle_certificate_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.handle_certificate_error(1, "continue") for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_concurrent_mixed_methods(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.enable(),
            domain.set_ignore_certificate_errors(True),
            domain.handle_certificate_error(1, "continue"),
            domain.set_override_certificate_errors(True),
            domain.get_visible_security_state(),
        )
        assert len(fake.calls) == 6

    async def test_concurrent_50_enable_50_disable(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.enable() for _ in range(50)],
            *[domain.disable() for _ in range(50)],
        )
        assert len(fake.calls) == 100


# ---------------------------------------------------------------------------
# Repetition
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRepetition:
    async def test_enable_disable_10x(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        for _ in range(10):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 20
        for i in range(10):
            assert fake.calls[i * 2][0] == "Security.enable"
            assert fake.calls[i * 2 + 1][0] == "Security.disable"

    async def test_repeated_enable_10x(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        for _ in range(10):
            await domain.enable()
        assert len(fake.calls) == 10

    async def test_repeated_set_ignore_10x(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        for _ in range(10):
            await domain.set_ignore_certificate_errors(True)
        assert len(fake.calls) == 10

    async def test_repeated_handle_certificate_error_10x(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        for _ in range(10):
            await domain.handle_certificate_error(1, "continue")
        assert len(fake.calls) == 10

    async def test_repeated_get_visible_security_state_10x(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        for _ in range(10):
            await domain.get_visible_security_state()
        assert len(fake.calls) == 10


# ---------------------------------------------------------------------------
# Call sequences
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCallSequence:
    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.enable()
        await domain.set_ignore_certificate_errors(True)
        await domain.handle_certificate_error(1, "continue")
        await domain.set_override_certificate_errors(True)
        await domain.get_visible_security_state()
        await domain.disable()
        assert len(fake.calls) == 6
        assert fake.calls[0][0] == "Security.enable"
        assert fake.calls[1][0] == "Security.setIgnoreCertificateErrors"
        assert fake.calls[2][0] == "Security.handleCertificateError"
        assert fake.calls[3][0] == "Security.setOverrideCertificateErrors"
        assert fake.calls[4][0] == "Security.getVisibleSecurityState"
        assert fake.calls[5][0] == "Security.disable"

    async def test_all_methods_use_security_prefix(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.disable()
        await domain.enable()
        await domain.set_ignore_certificate_errors(True)
        await domain.handle_certificate_error(1, "continue")
        await domain.set_override_certificate_errors(True)
        await domain.get_visible_security_state()
        for method, _ in fake.calls:
            assert method.startswith("Security.")

    async def test_interleaved_calls(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await domain.enable()
        await domain.set_ignore_certificate_errors(True)
        await domain.disable()
        await domain.set_override_certificate_errors(False)
        await domain.enable()
        await domain.handle_certificate_error(2, "cancel")
        await domain.get_visible_security_state()
        await domain.disable()
        assert len(fake.calls) == 8


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    async def test_set_response_between_calls(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        r1 = await domain.enable()
        assert r1 == {}
        fake.set_response({"ok": True})
        r2 = await domain.enable()
        assert r2 == {"ok": True}

    async def test_large_response_dict(self) -> None:
        large = {f"key{i}": i for i in range(100)}
        fake = FakeSender(large)
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert result == large

    async def test_empty_response_from_sender(self) -> None:
        class EmptySender:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                return {}

        sender = EmptySender()
        domain = SecurityDomain(sender)
        result = await domain.disable()
        assert result == {}

    async def test_none_response_passes_through(self) -> None:
        class NoneReturnSender:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                return None  # type: ignore[return-value]

        sender = NoneReturnSender()
        domain = SecurityDomain(sender)
        result = await domain.disable()
        assert result is None

    async def test_mixed_error_success(self) -> None:
        class MixedSender:
            def __init__(self) -> None:
                self._count = 0
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                self._count += 1
                if self._count % 2 == 0:
                    raise CommandError(-1, "even call error")
                return {"ok": True}

        sender = MixedSender()
        domain = SecurityDomain(sender)
        r1 = await domain.enable()
        assert r1 == {"ok": True}
        with pytest.raises(CommandError):
            await domain.enable()
        assert len(sender.calls) == 2

    async def test_exact_response_object(self) -> None:
        response = {"visibleSecurityState": {"securityState": "secure"}}
        fake = FakeSender(response)
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        assert result is response

    async def test_params_not_mutated_between_calls(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        await domain.handle_certificate_error(2, "cancel")
        assert fake.calls[0][1] == {"eventId": 1, "action": "continue"}
        assert fake.calls[1][1] == {"eventId": 2, "action": "cancel"}

    async def test_domain_works_with_custom_sender(self) -> None:
        class CustomSender:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, Any] | None]] = []

            async def __call__(
                self,
                method: str,
                params: dict[str, Any] | None = None,
            ) -> dict[str, Any]:
                self.calls.append((method, params))
                return {"custom": True}

        sender = CustomSender()
        domain = SecurityDomain(sender)
        result = await domain.disable()
        assert result == {"custom": True}
        assert len(sender.calls) == 1


# ---------------------------------------------------------------------------
# Edge cases — extended
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCasesExtended:
    async def test_disable_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data", "count": 5})
        domain = SecurityDomain(fake)
        result = await domain.disable()
        assert result["extra"] == "data"
        assert result["count"] == 5

    async def test_enable_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = SecurityDomain(fake)
        result = await domain.enable()
        assert result["extra"] == "data"

    async def test_set_ignore_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = SecurityDomain(fake)
        result = await domain.set_ignore_certificate_errors(True)
        assert result["extra"] == "data"

    async def test_handle_certificate_error_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = SecurityDomain(fake)
        result = await domain.handle_certificate_error(1, "continue")
        assert result["extra"] == "data"

    async def test_set_override_with_extra_keys(self) -> None:
        fake = FakeSender({"extra": "data"})
        domain = SecurityDomain(fake)
        result = await domain.set_override_certificate_errors(True)
        assert result["extra"] == "data"

    async def test_get_visible_security_state_with_safety_tip(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "insecure",
                "safetyTipInfo": {
                    "safetyTipStatus": "lookalike",
                    "safeUrl": "https://example.com",
                },
                "securityStateIssueIds": ["issue1"],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert state["safetyTipInfo"]["safetyTipStatus"] == "lookalike"
        assert state["safetyTipInfo"]["safeUrl"] == "https://example.com"
        assert state["securityStateIssueIds"] == ["issue1"]

    async def test_get_visible_security_state_all_security_states(self) -> None:
        for state_name in ("unknown", "neutral", "insecure", "secure", "info", "insecure-broken"):
            fake = FakeSender({
                "visibleSecurityState": {"securityState": state_name},
            })
            domain = SecurityDomain(fake)
            result = await domain.get_visible_security_state()
            assert result["visibleSecurityState"]["securityState"] == state_name

    async def test_error_does_not_swallow_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError):
            await domain.set_ignore_certificate_errors(None)
        assert len(fake.calls) == 0

    async def test_error_does_not_swallow_value_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError):
            await domain.handle_certificate_error(1, "bad")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Extended error propagation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestErrorPropagationExtended:
    async def test_error_with_positive_code(self) -> None:
        sender = ErrorSender(code=100, message="Positive code")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert exc_info.value.code == 100

    async def test_error_with_zero_code(self) -> None:
        sender = ErrorSender(code=0, message="Zero code")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == 0

    async def test_error_with_empty_message(self) -> None:
        sender = ErrorSender(code=-1, message="")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.get_visible_security_state()
        assert exc_info.value.message == ""

    async def test_error_with_long_message(self) -> None:
        msg = "x" * 10000
        sender = ErrorSender(code=-1, message=msg)
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.set_ignore_certificate_errors(True)
        assert exc_info.value.message == msg

    async def test_error_with_unicode_message(self) -> None:
        sender = ErrorSender(code=-1, message="Error \u00f1\u4e2d")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.enable()
        assert "\u00f1" in exc_info.value.message

    async def test_error_propagation_preserves_code_and_message(self) -> None:
        sender = ErrorSender(code=-42, message="Custom error")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError) as exc_info:
            await domain.disable()
        assert exc_info.value.code == -42
        assert exc_info.value.message == "Custom error"
        assert str(exc_info.value) == "[-42] Custom error"

    async def test_error_handle_certificate_error(self) -> None:
        sender = ErrorSender(code=-1, message="Handle failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError):
            await domain.handle_certificate_error(1, "continue")

    async def test_error_set_override_certificate_errors(self) -> None:
        sender = ErrorSender(code=-1, message="Override failed")
        domain = SecurityDomain(sender)
        with pytest.raises(CommandError):
            await domain.set_override_certificate_errors(True)


# ---------------------------------------------------------------------------
# Extended concurrency
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrencyExtended:
    async def test_100_concurrent_set_override(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.set_override_certificate_errors(True) for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_100_concurrent_get_visible_security_state(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.get_visible_security_state() for _ in range(100)],
        )
        assert len(fake.calls) == 100

    async def test_concurrent_all_six_methods(self) -> None:
        fake = FakeSender({"visibleSecurityState": {}})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            domain.disable(),
            domain.enable(),
            domain.set_ignore_certificate_errors(True),
            domain.handle_certificate_error(1, "continue"),
            domain.set_override_certificate_errors(True),
            domain.get_visible_security_state(),
        )
        assert len(fake.calls) == 6

    async def test_concurrent_with_params_all_verified(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            *[domain.set_ignore_certificate_errors(True) for _ in range(50)],
            *[domain.set_override_certificate_errors(False) for _ in range(50)],
        )
        assert len(fake.calls) == 100
        for method, params in fake.calls[:50]:
            assert method == "Security.setIgnoreCertificateErrors"
            assert params is not None
            assert params["ignore"] is True
        for method, params in fake.calls[50:]:
            assert method == "Security.setOverrideCertificateErrors"
            assert params is not None
            assert params["override"] is False


# ---------------------------------------------------------------------------
# Extended type validation — exotic types
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSetIgnoreCertificateErrorsExoticTypes:
    async def test_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(b"true")
        assert len(fake.calls) == 0

    async def test_bytearray_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(bytearray(b"true"))
        assert len(fake.calls) == 0

    async def test_tuple_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors((True,))
        assert len(fake.calls) == 0

    async def test_set_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors({True})
        assert len(fake.calls) == 0

    async def test_frozenset_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(frozenset({True}))
        assert len(fake.calls) == 0

    async def test_complex_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(complex(1, 0))
        assert len(fake.calls) == 0

    async def test_range_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="ignore must be a bool"):
            await domain.set_ignore_certificate_errors(range(1))
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestHandleCertificateErrorEventIdExoticTypes:
    async def test_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(b"1", "continue")
        assert len(fake.calls) == 0

    async def test_bytearray_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(bytearray(b"1"), "continue")
        assert len(fake.calls) == 0

    async def test_tuple_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error((1,), "continue")
        assert len(fake.calls) == 0

    async def test_set_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error({1}, "continue")
        assert len(fake.calls) == 0

    async def test_frozenset_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(frozenset({1}), "continue")
        assert len(fake.calls) == 0

    async def test_complex_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(complex(1, 0), "continue")
        assert len(fake.calls) == 0

    async def test_range_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(range(1), "continue")
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestHandleCertificateErrorActionExoticTypes:
    async def test_bytearray_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, bytearray(b"continue"))
        assert len(fake.calls) == 0

    async def test_tuple_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, ("continue",))
        assert len(fake.calls) == 0

    async def test_set_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, {"continue"})
        assert len(fake.calls) == 0

    async def test_frozenset_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, frozenset({"continue"}))
        assert len(fake.calls) == 0

    async def test_complex_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, complex(1, 0))
        assert len(fake.calls) == 0

    async def test_range_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, range(1))
        assert len(fake.calls) == 0


@pytest.mark.unit
class TestSetOverrideCertificateErrorsExoticTypes:
    async def test_bytes_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(b"true")
        assert len(fake.calls) == 0

    async def test_bytearray_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(bytearray(b"true"))
        assert len(fake.calls) == 0

    async def test_tuple_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors((True,))
        assert len(fake.calls) == 0

    async def test_set_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors({True})
        assert len(fake.calls) == 0

    async def test_frozenset_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(frozenset({True}))
        assert len(fake.calls) == 0

    async def test_complex_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(complex(1, 0))
        assert len(fake.calls) == 0

    async def test_range_raises_type_error(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="override must be a bool"):
            await domain.set_override_certificate_errors(range(1))
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Extended edge cases — value identity and param preservation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValueIdentity:
    async def test_set_ignore_preserves_bool_identity_true(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert params["ignore"] is True

    async def test_set_ignore_preserves_bool_identity_false(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_ignore_certificate_errors(False)
        _, params = fake.last_call
        assert params is not None
        assert params["ignore"] is False

    async def test_set_override_preserves_bool_identity_true(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(True)
        _, params = fake.last_call
        assert params is not None
        assert params["override"] is True

    async def test_set_override_preserves_bool_identity_false(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.set_override_certificate_errors(False)
        _, params = fake.last_call
        assert params is not None
        assert params["override"] is False

    async def test_handle_cert_preserves_int_identity(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(42, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == 42
        assert isinstance(params["eventId"], int)

    async def test_handle_cert_preserves_str_identity(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["action"] == "continue"
        assert isinstance(params["action"], str)

    async def test_handle_cert_preserves_negative_int(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(-999, "cancel")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == -999

    async def test_handle_cert_preserves_max_int(self) -> None:
        import sys
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(sys.maxsize, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["eventId"] == sys.maxsize


# ---------------------------------------------------------------------------
# Extended edge cases — validation order
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValidationOrder:
    async def test_event_id_checked_before_action_type(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error("bad", 123)
        assert len(fake.calls) == 0

    async def test_event_id_checked_before_action_enum(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error("bad", "bad_action")
        assert len(fake.calls) == 0

    async def test_action_type_checked_before_enum(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="action must be a string"):
            await domain.handle_certificate_error(1, 123)
        assert len(fake.calls) == 0

    async def test_both_valid_types_but_bad_enum(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "bad")
        assert len(fake.calls) == 0

    async def test_bool_event_id_with_valid_action_still_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(True, "continue")
        assert len(fake.calls) == 0

    async def test_false_event_id_with_valid_action_still_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(TypeError, match="event_id must be an integer"):
            await domain.handle_certificate_error(False, "cancel")
        assert len(fake.calls) == 0


# ---------------------------------------------------------------------------
# Extended edge cases — response content verification
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestResponseContentVerification:
    async def test_get_visible_security_state_with_certificate(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "secure",
                "certificateSecurityState": {
                    "protocol": "TLS 1.3",
                    "keyExchange": "X25519",
                    "keyExchangeGroup": "x25519",
                    "cipher": "AES_256_GCM",
                    "mac": "AEAD",
                    "certificate": ["-----BEGIN CERTIFICATE-----"],
                    "subjectName": "example.com",
                    "issuer": "DigiCert",
                    "validFrom": 1234567890,
                    "validTo": 9876543210,
                    "certificateHasWeakSignature": False,
                    "certificateHasSha1Signature": False,
                    "modernSSL": True,
                    "obsoleteSslProtocol": False,
                    "obsoleteSslKeyExchange": False,
                    "obsoleteSslCipher": False,
                    "obsoleteSslSignature": False,
                },
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        cert = state["certificateSecurityState"]
        assert cert["protocol"] == "TLS 1.3"
        assert cert["modernSSL"] is True
        assert cert["validFrom"] == 1234567890
        assert cert["validTo"] == 9876543210

    async def test_get_visible_security_state_with_safety_tip_lookalike(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "insecure",
                "safetyTipInfo": {
                    "safetyTipStatus": "lookalike",
                    "safeUrl": "https://safe-example.com",
                },
                "securityStateIssueIds": ["lookalike-url"],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert state["safetyTipInfo"]["safetyTipStatus"] == "lookalike"
        assert state["safetyTipInfo"]["safeUrl"] == "https://safe-example.com"
        assert "lookalike-url" in state["securityStateIssueIds"]

    async def test_get_visible_security_state_with_safety_tip_bad_reputation(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "insecure",
                "safetyTipInfo": {
                    "safetyTipStatus": "badReputation",
                    "safeUrl": None,
                },
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert state["safetyTipInfo"]["safetyTipStatus"] == "badReputation"

    async def test_get_visible_security_state_empty_issue_ids(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "secure",
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert state["securityStateIssueIds"] == []

    async def test_get_visible_security_state_many_issue_ids(self) -> None:
        ids = [f"issue-{i}" for i in range(100)]
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "insecure",
                "securityStateIssueIds": ids,
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert state["securityStateIssueIds"] == ids
        assert len(state["securityStateIssueIds"]) == 100

    async def test_get_visible_security_state_no_certificate_state(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "neutral",
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert "certificateSecurityState" not in state

    async def test_get_visible_security_state_no_safety_tip(self) -> None:
        fake = FakeSender({
            "visibleSecurityState": {
                "securityState": "secure",
                "securityStateIssueIds": [],
            },
        })
        domain = SecurityDomain(fake)
        result = await domain.get_visible_security_state()
        state = result["visibleSecurityState"]
        assert "safetyTipInfo" not in state

    async def test_disable_returns_exact_response(self) -> None:
        response = {"result": True, "count": 42, "data": [1, 2, 3]}
        fake = FakeSender(response)
        domain = SecurityDomain(fake)
        result = await domain.disable()
        assert result is response

    async def test_enable_returns_exact_response(self) -> None:
        response = {"status": "ok", "events": ["a", "b"]}
        fake = FakeSender(response)
        domain = SecurityDomain(fake)
        result = await domain.enable()
        assert result is response


# ---------------------------------------------------------------------------
# Extended edge cases — concurrent validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrentValidation:
    async def test_concurrent_valid_and_invalid_params(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)

        async def valid_call() -> dict[str, Any]:
            return await domain.set_ignore_certificate_errors(True)

        async def invalid_call() -> dict[str, Any]:
            return await domain.set_ignore_certificate_errors("bad")

        results = await asyncio.gather(
            valid_call(),
            invalid_call(),
            valid_call(),
            return_exceptions=True,
        )
        assert isinstance(results[0], dict)
        assert isinstance(results[1], TypeError)
        assert isinstance(results[2], dict)
        assert len(fake.calls) == 2

    async def test_concurrent_handle_cert_mixed_validity(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)

        async def valid_call() -> dict[str, Any]:
            return await domain.handle_certificate_error(1, "continue")

        async def bad_action() -> dict[str, Any]:
            return await domain.handle_certificate_error(2, "bad")

        async def bad_event_id() -> dict[str, Any]:
            return await domain.handle_certificate_error("x", "cancel")

        results = await asyncio.gather(
            valid_call(),
            bad_action(),
            bad_event_id(),
            valid_call(),
            return_exceptions=True,
        )
        assert isinstance(results[0], dict)
        assert isinstance(results[1], ValueError)
        assert isinstance(results[2], TypeError)
        assert isinstance(results[3], dict)
        assert len(fake.calls) == 2

    async def test_concurrent_all_valid_different_params(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await asyncio.gather(
            domain.set_ignore_certificate_errors(True),
            domain.set_ignore_certificate_errors(False),
            domain.set_override_certificate_errors(True),
            domain.set_override_certificate_errors(False),
            domain.handle_certificate_error(1, "continue"),
            domain.handle_certificate_error(2, "cancel"),
        )
        assert len(fake.calls) == 6
        for _, params in fake.calls:
            assert params is not None


# ---------------------------------------------------------------------------
# Extended edge cases — enum boundary
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnumBoundary:
    async def test_continue_exact_match(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "continue")
        _, params = fake.last_call
        assert params is not None
        assert params["action"] == "continue"

    async def test_cancel_exact_match(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        await domain.handle_certificate_error(1, "cancel")
        _, params = fake.last_call
        assert params is not None
        assert params["action"] == "cancel"

    async def test_continue_with_newline_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "continue\n")
        assert len(fake.calls) == 0

    async def test_cancel_with_tab_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "cancel\t")
        assert len(fake.calls) == 0

    async def test_continue_with_null_byte_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "continue\x00")
        assert len(fake.calls) == 0

    async def test_empty_continue_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "")
        assert len(fake.calls) == 0

    async def test_just_continue_letter_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "c")
        assert len(fake.calls) == 0

    async def test_just_cancel_letter_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "c")
        assert len(fake.calls) == 0

    async def test_continue_uppercase_c_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "Continue")
        assert len(fake.calls) == 0

    async def test_cancel_uppercase_c_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "Cancel")
        assert len(fake.calls) == 0

    async def test_continue_all_uppercase_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "CONTINUE")
        assert len(fake.calls) == 0

    async def test_cancel_all_uppercase_raises(self) -> None:
        fake = FakeSender({})
        domain = SecurityDomain(fake)
        with pytest.raises(ValueError, match="action must be 'continue' or 'cancel'"):
            await domain.handle_certificate_error(1, "CANCEL")
        assert len(fake.calls) == 0
