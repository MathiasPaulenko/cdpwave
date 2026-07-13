"""Fetch domain: intercepting and modifying network requests."""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_ERROR_REASONS = frozenset({
    "Failed",
    "Aborted",
    "TimedOut",
    "AccessDenied",
    "ConnectionClosed",
    "ConnectionReset",
    "ConnectionRefused",
    "ConnectionAborted",
    "ConnectionFailed",
    "NameNotResolved",
    "InternetDisconnected",
    "AddressUnreachable",
    "BlockedByClient",
    "BlockedByResponse",
})

_VALID_AUTH_RESPONSES = frozenset({
    "Default",
    "CancelAuth",
    "ProvideCredentials",
})


class FetchDomain(BaseDomain):
    """Wrapper for the CDP Fetch domain.

    Provides methods for enabling request interception, continuing
    intercepted requests, and providing responses to intercepted requests.
    """

    async def enable(
        self,
        patterns: list[dict[str, Any]] | None = None,
        handle_auth_requests: bool = False,
    ) -> dict[str, Any]:
        """Enable Fetch domain for request interception.

        Args:
            patterns: List of request pattern dicts with ``urlPattern``,
                ``requestStage`` (``"Request"`` or ``"Response"``), and
                optional ``resourceType``.
            handle_auth_requests: Whether to handle authentication
                challenges.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(handle_auth_requests, bool):
            raise TypeError("handle_auth_requests must be a bool")
        if patterns is not None and not isinstance(patterns, list):
            raise TypeError("patterns must be a list or None")
        params: dict[str, Any] = {"handleAuthRequests": handle_auth_requests}
        if patterns is not None:
            params["patterns"] = patterns
        return await self._call("Fetch.enable", params)

    async def disable(self) -> dict[str, Any]:
        """Disable Fetch domain request interception.

        Stops intercepting network requests. All pending paused
        requests will be automatically resumed.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Fetch.disable")

    async def continue_request(
        self,
        request_id: str,
        url: str | None = None,
        method: str | None = None,
        post_data: str | None = None,
        headers: list[dict[str, str]] | None = None,
        intercept_response: bool = False,
    ) -> dict[str, Any]:
        """Continue an intercepted request with optional modifications.

        Args:
            request_id: The ID of the intercepted request.
            url: Modified URL for the request.
            method: Modified HTTP method.
            post_data: Modified POST body as base64-encoded string.
            headers: Modified headers as list of ``{"name": ..., "value": ...}``.
            intercept_response: Whether to intercept the response stage too.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        if not isinstance(intercept_response, bool):
            raise TypeError("intercept_response must be a bool")
        params: dict[str, Any] = {
            "requestId": request_id,
            "interceptResponse": intercept_response,
        }
        if url is not None:
            if not isinstance(url, str):
                raise TypeError("url must be a string or None")
            params["url"] = url
        if method is not None:
            if not isinstance(method, str):
                raise TypeError("method must be a string or None")
            params["method"] = method
        if post_data is not None:
            if not isinstance(post_data, str):
                raise TypeError("post_data must be a string or None")
            params["postData"] = post_data
        if headers is not None:
            if not isinstance(headers, list):
                raise TypeError("headers must be a list or None")
            params["headers"] = headers
        return await self._call("Fetch.continueRequest", params)

    async def continue_request_with_auth(
        self,
        request_id: str,
        auth_challenge_response: dict[str, Any],
    ) -> dict[str, Any]:
        """Continue an intercepted request with authentication credentials.

        Args:
            request_id: The ID of the intercepted request.
            auth_challenge_response: Auth response dict with ``response``
                (``"Default"``, ``"CancelAuth"``, ``"ProvideCredentials"``),
                ``username``, and ``password``.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        if not isinstance(auth_challenge_response, dict):
            raise TypeError("auth_challenge_response must be a dict")
        if "response" not in auth_challenge_response:
            raise ValueError("auth_challenge_response must contain 'response'")
        resp = auth_challenge_response["response"]
        if not isinstance(resp, str):
            raise TypeError("auth_challenge_response['response'] must be a string")
        if resp not in _VALID_AUTH_RESPONSES:
            raise ValueError(
                f"auth_challenge_response['response'] must be one of "
                f"{sorted(_VALID_AUTH_RESPONSES)}"
            )
        return await self._call(
            "Fetch.continueWithAuth",
            {
                "requestId": request_id,
                "authChallengeResponse": auth_challenge_response,
            },
        )

    async def continue_with_auth(
        self,
        request_id: str,
        response: str,
        username: str | None = None,
        password: str | None = None,
    ) -> dict[str, Any]:
        """Continue an intercepted request with auth response.

        Convenience wrapper around ``continue_request_with_auth`` that
        accepts a simple response string instead of a dict.

        Args:
            request_id: The ID of the intercepted request.
            response: Auth response (``"Default"``, ``"CancelAuth"``,
                ``"ProvideCredentials"``).
            username: Optional username for credentials.
            password: Optional password for credentials.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        if not isinstance(response, str):
            raise TypeError("response must be a string")
        if response not in _VALID_AUTH_RESPONSES:
            raise ValueError(
                f"response must be one of {sorted(_VALID_AUTH_RESPONSES)}"
            )
        if username is not None and not isinstance(username, str):
            raise TypeError("username must be a string or None")
        if password is not None and not isinstance(password, str):
            raise TypeError("password must be a string or None")
        auth_challenge_response: dict[str, Any] = {"response": response}
        if username is not None:
            auth_challenge_response["username"] = username
        if password is not None:
            auth_challenge_response["password"] = password
        return await self._call(
            "Fetch.continueWithAuth",
            {
                "requestId": request_id,
                "authChallengeResponse": auth_challenge_response,
            },
        )

    async def continue_response(
        self,
        request_id: str,
        response_code: int | None = None,
        response_headers: list[dict[str, str]] | None = None,
        binary_response_headers: str | None = None,
        response_phrase: str | None = None,
    ) -> dict[str, Any]:
        """Continue an intercepted response with optional modifications.

        Args:
            request_id: The ID of the intercepted request.
            response_code: HTTP response code.
            response_headers: Response headers as list of
                ``{"name": ..., "value": ...}``.
            binary_response_headers: Base64-encoded response headers.
            response_phrase: Textual representation of responseCode.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        if response_code is not None and (
            isinstance(response_code, bool) or not isinstance(response_code, int)
        ):
            raise TypeError("response_code must be an int or None")
        if response_headers is not None and not isinstance(response_headers, list):
            raise TypeError("response_headers must be a list or None")
        if binary_response_headers is not None and not isinstance(binary_response_headers, str):
            raise TypeError("binary_response_headers must be a string or None")
        if response_phrase is not None and not isinstance(response_phrase, str):
            raise TypeError("response_phrase must be a string or None")
        params: dict[str, Any] = {"requestId": request_id}
        if response_code is not None:
            params["responseCode"] = response_code
        if response_headers is not None:
            params["responseHeaders"] = response_headers
        if binary_response_headers is not None:
            params["binaryResponseHeaders"] = binary_response_headers
        if response_phrase is not None:
            params["responsePhrase"] = response_phrase
        return await self._call("Fetch.continueResponse", params)

    async def fulfill_request(
        self,
        request_id: str,
        response_code: int | None = None,
        response_headers: list[dict[str, str]] | None = None,
        body: str | None = None,
        binary_response_headers: str | None = None,
        response_phrase: str | None = None,
        status_code: int | None = None,
    ) -> dict[str, Any]:
        """Provide a complete response to an intercepted request.

        Args:
            request_id: The ID of the intercepted request.
            response_code: HTTP response code.
            response_headers: Response headers as list of
                ``{"name": ..., "value": ...}``.
            body: Response body as base64-encoded string.
            binary_response_headers: Base64-encoded response headers.
            response_phrase: Textual representation of responseCode.
            status_code: Alias for ``response_code``.

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        code = response_code if response_code is not None else status_code
        if code is None:
            raise ValueError("Either response_code or status_code must be provided")
        if isinstance(code, bool) or not isinstance(code, int):
            raise TypeError("response_code/status_code must be an int")
        if response_headers is not None and not isinstance(response_headers, list):
            raise TypeError("response_headers must be a list or None")
        if body is not None and not isinstance(body, str):
            raise TypeError("body must be a string or None")
        if binary_response_headers is not None and not isinstance(binary_response_headers, str):
            raise TypeError("binary_response_headers must be a string or None")
        if response_phrase is not None and not isinstance(response_phrase, str):
            raise TypeError("response_phrase must be a string or None")
        params: dict[str, Any] = {
            "requestId": request_id,
            "responseCode": code,
        }
        if response_headers is not None:
            params["responseHeaders"] = response_headers
        if body is not None:
            params["body"] = body
        if binary_response_headers is not None:
            params["binaryResponseHeaders"] = binary_response_headers
        if response_phrase is not None:
            params["responsePhrase"] = response_phrase
        return await self._call("Fetch.fulfillRequest", params)

    async def fail_request(
        self,
        request_id: str,
        error_reason: str,
    ) -> dict[str, Any]:
        """Fail an intercepted request with an error.

        Args:
            request_id: The ID of the intercepted request.
            error_reason: Error reason (``"Failed"``, ``"Aborted"``,
                ``"TimedOut"``, ``"AccessDenied"``, etc.).

        Returns:
            Response dict from the CDP command.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        if not isinstance(error_reason, str):
            raise TypeError("error_reason must be a string")
        if error_reason not in _VALID_ERROR_REASONS:
            raise ValueError(
                f"error_reason must be one of {sorted(_VALID_ERROR_REASONS)}"
            )
        return await self._call(
            "Fetch.failRequest",
            {"requestId": request_id, "errorReason": error_reason},
        )

    async def get_response_body(self, request_id: str) -> dict[str, Any]:
        """Get the body of an intercepted response.

        Args:
            request_id: The ID of the intercepted request.

        Returns:
            Response dict containing ``body`` (base64-encoded) and
            ``base64Encoded`` flag.
        """
        return await self._call(
            "Fetch.getResponseBody",
            {"requestId": request_id},
        )

    async def take_response_body_as_stream(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Take the response body as a stream.

        Args:
            request_id: The ID of the intercepted request.

        Returns:
            Response dict containing the stream handle.
        """
        return await self._call(
            "Fetch.takeResponseBodyAsStream",
            {"requestId": request_id},
        )

    async def get_request_post_data(self, request_id: str) -> dict[str, Any]:
        """Get the POST data of an intercepted request.

        Args:
            request_id: The ID of the intercepted request.

        Returns:
            Dict with ``postData`` string.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a string")
        return await self._call(
            "Fetch.getRequestPostData",
            {"requestId": request_id},
        )
