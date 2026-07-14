"""Edge-case tests for the Fetch domain — validation branches only.

Targets every TypeError/ValueError raise in FetchDomain to push
coverage from 74% to >=90%.
"""

import pytest

from cdpwave.domains.fetch import FetchDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestFetchEdgeValidation:
    async def test_enable_handle_auth_not_bool(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="handle_auth_requests must be a bool"):
            await d.enable(handle_auth_requests="yes")  # type: ignore[arg-type]

    async def test_enable_patterns_not_list(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="patterns must be a list or None"):
            await d.enable(patterns="not-a-list")  # type: ignore[arg-type]

    async def test_continue_request_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.continue_request(123)  # type: ignore[arg-type]

    async def test_continue_request_intercept_response_not_bool(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="intercept_response must be a bool"):
            await d.continue_request("req", intercept_response="yes")  # type: ignore[arg-type]

    async def test_continue_request_url_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url must be a string or None"):
            await d.continue_request("req", url=123)  # type: ignore[arg-type]

    async def test_continue_request_method_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="method must be a string or None"):
            await d.continue_request("req", method=123)  # type: ignore[arg-type]

    async def test_continue_request_post_data_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="post_data must be a string or None"):
            await d.continue_request("req", post_data=123)  # type: ignore[arg-type]

    async def test_continue_request_headers_not_list(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="headers must be a list or None"):
            await d.continue_request("req", headers="not-a-list")  # type: ignore[arg-type]

    async def test_continue_request_with_auth_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.continue_request_with_auth(123, {"response": "Default"})  # type: ignore[arg-type]

    async def test_continue_request_with_auth_response_not_dict(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="auth_challenge_response must be a dict"):
            await d.continue_request_with_auth("req", "not-a-dict")  # type: ignore[arg-type]

    async def test_continue_request_with_auth_missing_response_key(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(ValueError, match="auth_challenge_response must contain 'response'"):
            await d.continue_request_with_auth("req", {})

    async def test_continue_request_with_auth_response_value_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(
            TypeError,
            match="auth_challenge_response\\['response'\\] must be a string",
        ):
            await d.continue_request_with_auth("req", {"response": 123})

    async def test_continue_request_with_auth_response_invalid_value(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(
            ValueError,
            match="auth_challenge_response\\['response'\\] must be one of",
        ):
            await d.continue_request_with_auth("req", {"response": "Invalid"})

    async def test_continue_with_auth_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.continue_with_auth(123, "Default")  # type: ignore[arg-type]

    async def test_continue_with_auth_response_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response must be a string"):
            await d.continue_with_auth("req", 123)  # type: ignore[arg-type]

    async def test_continue_with_auth_response_invalid(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(ValueError, match="response must be one of"):
            await d.continue_with_auth("req", "Invalid")

    async def test_continue_with_auth_username_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="username must be a string or None"):
            await d.continue_with_auth("req", "Default", username=123)  # type: ignore[arg-type]

    async def test_continue_with_auth_password_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="password must be a string or None"):
            await d.continue_with_auth("req", "Default", password=123)  # type: ignore[arg-type]

    async def test_continue_response_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.continue_response(123)  # type: ignore[arg-type]

    async def test_continue_response_response_code_not_int(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_code must be an int or None"):
            await d.continue_response("req", response_code="200")  # type: ignore[arg-type]

    async def test_continue_response_response_code_bool(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_code must be an int or None"):
            await d.continue_response("req", response_code=True)  # type: ignore[arg-type]

    async def test_continue_response_response_headers_not_list(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_headers must be a list or None"):
            await d.continue_response("req", response_headers="not-a-list")  # type: ignore[arg-type]

    async def test_continue_response_binary_response_headers_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="binary_response_headers must be a string or None"):
            await d.continue_response("req", binary_response_headers=123)  # type: ignore[arg-type]

    async def test_continue_response_response_phrase_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_phrase must be a string or None"):
            await d.continue_response("req", response_phrase=123)  # type: ignore[arg-type]

    async def test_fulfill_request_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.fulfill_request(123, response_code=200)  # type: ignore[arg-type]

    async def test_fulfill_request_no_code(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(
            ValueError,
            match="Either response_code or status_code must be provided",
        ):
            await d.fulfill_request("req")

    async def test_fulfill_request_code_not_int(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_code/status_code must be an int"):
            await d.fulfill_request("req", response_code="200")  # type: ignore[arg-type]

    async def test_fulfill_request_code_bool(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_code/status_code must be an int"):
            await d.fulfill_request("req", response_code=True)  # type: ignore[arg-type]

    async def test_fulfill_request_response_headers_not_list(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_headers must be a list or None"):
            await d.fulfill_request("req", response_code=200, response_headers="not-a-list")  # type: ignore[arg-type]

    async def test_fulfill_request_body_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="body must be a string or None"):
            await d.fulfill_request("req", response_code=200, body=123)  # type: ignore[arg-type]

    async def test_fulfill_request_binary_response_headers_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="binary_response_headers must be a string or None"):
            await d.fulfill_request("req", response_code=200, binary_response_headers=123)  # type: ignore[arg-type]

    async def test_fulfill_request_response_phrase_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="response_phrase must be a string or None"):
            await d.fulfill_request("req", response_code=200, response_phrase=123)  # type: ignore[arg-type]

    async def test_fail_request_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.fail_request(123, "Failed")  # type: ignore[arg-type]

    async def test_fail_request_error_reason_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="error_reason must be a string"):
            await d.fail_request("req", 123)  # type: ignore[arg-type]

    async def test_fail_request_error_reason_invalid(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(ValueError, match="error_reason must be one of"):
            await d.fail_request("req", "NotAValidReason")

    async def test_get_request_post_data_request_id_not_str(self) -> None:
        d = FetchDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a string"):
            await d.get_request_post_data(123)  # type: ignore[arg-type]
