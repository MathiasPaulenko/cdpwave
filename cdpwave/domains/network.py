"""Network domain: monitoring, cookies, cache, and emulation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class NetworkDomain(BaseDomain):
    """Wrapper for the CDP Network domain."""

    async def enable(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
        max_post_data_size: int | None = None,
    ) -> dict[str, Any]:
        """Enable Network domain events.

        Args:
            max_total_buffer_size: Optional max total buffer size in bytes.
            max_resource_buffer_size: Optional max per-resource buffer size.
            max_post_data_size: Optional max POST data size to capture.
        """
        params: dict[str, Any] = {}
        if max_total_buffer_size is not None:
            params["maxTotalBufferSize"] = max_total_buffer_size
        if max_resource_buffer_size is not None:
            params["maxResourceBufferSize"] = max_resource_buffer_size
        if max_post_data_size is not None:
            params["maxPostDataSize"] = max_post_data_size
        return await self._call("Network.enable", params if params else None)

    async def disable(self) -> dict[str, Any]:
        """Disable Network domain events.

        Stops reporting of network requests, responses, loading events,
        and WebSocket activity.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Network.disable")

    async def set_user_agent_override(
        self,
        user_agent: str,
        accept_language: str | None = None,
        platform: str | None = None,
    ) -> dict[str, Any]:
        """Override the browser's User-Agent string.

        Args:
            user_agent: The User-Agent string to use.
            accept_language: Optional Accept-Language header value.
            platform: Optional platform override.
        """
        params: dict[str, Any] = {"userAgent": user_agent}
        if accept_language is not None:
            params["acceptLanguage"] = accept_language
        if platform is not None:
            params["platform"] = platform
        return await self._call("Network.setUserAgentOverride", params)

    async def set_extra_request_headers(
        self,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        """Set extra HTTP headers for all requests.

        Args:
            headers: Dict of header name to value.
        """
        return await self._call(
            "Network.setExtraHTTPHeaders",
            {"headers": headers},
        )

    async def clear_browser_cookies(self) -> dict[str, Any]:
        """Clear all browser cookies.

        Removes all cookies from the browser's cookie jar, including
        cookies for all domains and all contexts.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Network.clearBrowserCookies")

    async def clear_browser_cache(self) -> dict[str, Any]:
        """Clear the browser cache.

        Removes all entries from the browser's HTTP cache, forcing
        all subsequent requests to hit the network.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Network.clearBrowserCache")

    async def get_cookies(
        self,
        urls: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get cookies for the current page or specified URLs.

        Args:
            urls: Optional list of URLs to get cookies for.

        Returns:
            Response dict containing ``cookies`` list.
            Typed as ``NetworkGetCookiesResult`` for autocompletion.
        """
        params: dict[str, Any] = {}
        if urls is not None:
            params["urls"] = urls
        return await self._call("Network.getCookies", params if params else None)

    async def set_cookie(
        self,
        name: str,
        value: str,
        url: str | None = None,
        domain: str | None = None,
        path: str | None = None,
        secure: bool = False,
        http_only: bool = False,
        same_site: str | None = None,
        expires: float | None = None,
    ) -> dict[str, Any]:
        """Set a cookie.

        Args:
            name: Cookie name.
            value: Cookie value.
            url: Optional URL to associate the cookie with.
            domain: Optional cookie domain.
            path: Optional cookie path.
            secure: If True, cookie is secure-only.
            http_only: If True, cookie is HTTP-only.
            same_site: Optional SameSite attribute.
            expires: Optional expiration time as Unix timestamp.

        Returns:
            Response dict indicating success.
        """
        params: dict[str, Any] = {
            "name": name,
            "value": value,
            "secure": secure,
            "httpOnly": http_only,
        }
        if url is not None:
            params["url"] = url
        if domain is not None:
            params["domain"] = domain
        if path is not None:
            params["path"] = path
        if same_site is not None:
            params["sameSite"] = same_site
        if expires is not None:
            params["expires"] = expires
        return await self._call("Network.setCookie", params)

    async def delete_cookies(
        self,
        name: str,
        url: str | None = None,
        domain: str | None = None,
        path: str | None = None,
    ) -> dict[str, Any]:
        """Delete cookies matching the given name and constraints.

        Args:
            name: Cookie name to delete.
            url: Optional URL to scope the deletion.
            domain: Optional domain to scope the deletion.
            path: Optional path to scope the deletion.
        """
        params: dict[str, Any] = {"name": name}
        if url is not None:
            params["url"] = url
        if domain is not None:
            params["domain"] = domain
        if path is not None:
            params["path"] = path
        return await self._call("Network.deleteCookies", params)

    async def get_response_body(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Get the body of a response by request ID.

        Args:
            request_id: The CDP request ID.

        Returns:
            Response dict containing ``body`` and ``base64Encoded``.
        """
        return await self._call(
            "Network.getResponseBody",
            {"requestId": request_id},
        )

    async def set_cache_disabled(
        self,
        cache_disabled: bool,
        resource_types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Enable or disable the browser cache.

        Args:
            cache_disabled: If True, disable the cache.
            resource_types: Optional list of resource types to apply to.
        """
        params: dict[str, Any] = {"cacheDisabled": cache_disabled}
        if resource_types is not None:
            params["resourceTypes"] = resource_types
        return await self._call("Network.setCacheDisabled", params)

    async def emulate_network_conditions(
        self,
        offline: bool = False,
        latency: int = 0,
        download_throughput: float = -1,
        upload_throughput: float = -1,
        resource_types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Emulate network conditions.

        Args:
            offline: If True, emulate being offline.
            latency: Latency in milliseconds.
            download_throughput: Download throughput in bytes/sec (-1 for unlimited).
            upload_throughput: Upload throughput in bytes/sec (-1 for unlimited).
            resource_types: Optional list of resource types to apply to.
        """
        params: dict[str, Any] = {
            "offline": offline,
            "latency": latency,
            "downloadThroughput": download_throughput,
            "uploadThroughput": upload_throughput,
        }
        if resource_types is not None:
            params["resourceTypes"] = resource_types
        return await self._call("Network.emulateNetworkConditions", params)

    async def get_all_cookies(self) -> dict[str, Any]:
        """Get all cookies from the browser.

        Unlike ``get_cookies``, this returns cookies from all contexts.

        Returns:
            Dict with ``cookies`` list.
        """
        return await self._call("Network.getAllCookies")

    async def set_blocked_urls(self, urls: list[str]) -> dict[str, Any]:
        """Block specific URLs from loading.

        Args:
            urls: List of URL patterns to block (supports wildcards).
        """
        return await self._call(
            "Network.setBlockedURLs",
            {"urls": urls},
        )

    async def set_bypass_service_worker(self, bypass: bool) -> dict[str, Any]:
        """Bypass the service worker for all network requests.

        Args:
            bypass: Whether to bypass service workers.
        """
        return await self._call(
            "Network.setBypassServiceWorker",
            {"bypass": bypass},
        )

    async def load_network_resource(
        self,
        frame_id: str,
        url: str,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Load a network resource directly.

        Args:
            frame_id: Frame ID to load the resource for.
            url: URL of the resource to load.
            options: Optional resource load options dict.

        Returns:
            Dict with ``resource`` containing ``headers`` and ``statusCode``.
        """
        params: dict[str, Any] = {"frameId": frame_id, "url": url}
        if options is not None:
            params["options"] = options
        return await self._call("Network.loadNetworkResource", params)

    async def get_request_post_data(self, request_id: str) -> dict[str, Any]:
        """Get the POST data of a request.

        Args:
            request_id: Request ID from a network event.

        Returns:
            Dict with ``postData`` string.
        """
        return await self._call(
            "Network.getRequestPostData",
            {"requestId": request_id},
        )

    async def can_emulate_network_conditions(self) -> dict[str, Any]:
        """Check if network conditions emulation is supported.

        Returns:
            Dict with ``result`` boolean.
        """
        return await self._call("Network.canEmulateNetworkConditions")

    async def can_clear_browser_cache(self) -> dict[str, Any]:
        """Check if the browser cache can be cleared.

        Returns:
            Dict with ``result`` boolean.
        """
        return await self._call("Network.canClearBrowserCache")

    async def can_clear_browser_cookies(self) -> dict[str, Any]:
        """Check if browser cookies can be cleared.

        Returns:
            Dict with ``result`` boolean.
        """
        return await self._call("Network.canClearBrowserCookies")

    async def set_cookies(
        self,
        cookies: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set multiple cookies at once.

        Args:
            cookies: List of cookie dicts with ``name``, ``value``,
                ``domain``, ``path``, etc.
        """
        return await self._call("Network.setCookies", {"cookies": cookies})

    async def emulate_network_conditions_by_rule(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """Emulate network conditions by a pre-defined rule ID.

        Args:
            network_id: Network rule ID (e.g. ``"Slow 3G"``).
        """
        return await self._call(
            "Network.emulateNetworkConditionsByRule",
            {"networkId": network_id},
        )

    async def override_network_state(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """Override the network state by a pre-defined rule ID.

        Args:
            network_id: Network rule ID.
        """
        return await self._call(
            "Network.overrideNetworkState",
            {"networkId": network_id},
        )

    async def set_accepted_encodings(
        self,
        encodings: list[str],
    ) -> dict[str, Any]:
        """Set accepted content encodings.

        Args:
            encodings: List of accepted encodings (e.g.
                ``["gzip", "deflate", "br"]``).
        """
        return await self._call(
            "Network.setAcceptedEncodings",
            {"encodings": encodings},
        )

    async def clear_accepted_encodings_override(self) -> dict[str, Any]:
        """Clear the accepted encodings override."""
        return await self._call("Network.clearAcceptedEncodingsOverride")

    async def get_certificate(self, origin: str) -> dict[str, Any]:
        """Get the certificate for a given origin.

        Args:
            origin: Security origin to query.

        Returns:
            Dict with ``tableNames`` list.
        """
        return await self._call("Network.getCertificate", {"origin": origin})

    async def get_security_isolation_status(
        self,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the security isolation status of a page.

        Args:
            frame_id: Optional frame ID to query.

        Returns:
            Dict with ``status`` containing COEP, CORP, and CSP info.
        """
        params: dict[str, Any] = {}
        if frame_id is not None:
            params["frameId"] = frame_id
        return await self._call(
            "Network.getSecurityIsolationStatus",
            params if params else None,
        )

    async def enable_reporting_api(self, enable: bool) -> dict[str, Any]:
        """Enable or disable the Reporting API.

        Args:
            enable: Whether to enable the Reporting API.
        """
        return await self._call(
            "Network.enableReportingApi",
            {"enable": enable},
        )

    async def replay_xhr(self, request_id: str) -> dict[str, Any]:
        """Replay an XHR request.

        Args:
            request_id: The request ID to replay.
        """
        return await self._call("Network.replayXHR", {"requestId": request_id})

    async def search_in_response_body(
        self,
        request_id: str,
        query: str,
        case_sensitive: bool = False,
        is_regex: bool = False,
    ) -> dict[str, Any]:
        """Search in a response body.

        Args:
            request_id: Request ID from a network event.
            query: Search query string.
            case_sensitive: Whether the search is case sensitive.
            is_regex: Whether the query is a regex.

        Returns:
            Dict with ``result`` list of matches.
        """
        params: dict[str, Any] = {
            "requestId": request_id,
            "query": query,
            "caseSensitive": case_sensitive,
            "isRegex": is_regex,
        }
        return await self._call("Network.searchInResponseBody", params)

    async def set_attach_debug_stack(self, attach: bool) -> dict[str, Any]:
        """Enable or disable attaching debug stack traces to requests.

        Args:
            attach: Whether to attach debug stacks.
        """
        return await self._call(
            "Network.setAttachDebugStack",
            {"attach": attach},
        )

    async def set_request_interception(
        self,
        patterns: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set up request interception.

        Args:
            patterns: List of interception pattern dicts with
                ``urlPattern``, ``resourceType``, ``interceptionStage``.
        """
        return await self._call(
            "Network.setRequestInterception",
            {"patterns": patterns},
        )

    async def continue_intercepted_request(
        self,
        interception_id: str,
        error_reason: str | None = None,
        raw_response: str | None = None,
        url: str | None = None,
        method: str | None = None,
        headers: dict[str, str] | None = None,
        post_data: str | None = None,
    ) -> dict[str, Any]:
        """Continue an intercepted request.

        Args:
            interception_id: Interception ID from ``Network.requestIntercepted``.
            error_reason: Optional error reason to fail the request.
            raw_response: Optional raw HTTP response to return.
            url: Optional URL override.
            method: Optional HTTP method override.
            headers: Optional headers override.
            post_data: Optional POST data override.
        """
        params: dict[str, Any] = {"interceptionId": interception_id}
        if error_reason is not None:
            params["errorReason"] = error_reason
        if raw_response is not None:
            params["rawResponse"] = raw_response
        if url is not None:
            params["url"] = url
        if method is not None:
            params["method"] = method
        if headers is not None:
            params["headers"] = headers
        if post_data is not None:
            params["postData"] = post_data
        return await self._call("Network.continueInterceptedRequest", params)

    async def get_response_body_for_interception(
        self,
        interception_id: str,
    ) -> dict[str, Any]:
        """Get the response body for an intercepted request.

        Args:
            interception_id: Interception ID.

        Returns:
            Dict with ``body`` and ``base64Encoded``.
        """
        return await self._call(
            "Network.getResponseBodyForInterception",
            {"interceptionId": interception_id},
        )

    async def take_response_body_for_interception_as_stream(
        self,
        interception_id: str,
    ) -> dict[str, Any]:
        """Take the response body for an intercepted request as a stream.

        Args:
            interception_id: Interception ID.

        Returns:
            Dict with ``stream`` handle.
        """
        return await self._call(
            "Network.takeResponseBodyForInterceptionAsStream",
            {"interceptionId": interception_id},
        )

    async def stream_resource_content(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Stream resource content for a request.

        Args:
            request_id: Request ID from a network event.

        Returns:
            Dict with ``bufferedData``.
        """
        return await self._call(
            "Network.streamResourceContent",
            {"requestId": request_id},
        )

    async def fetch_schemeful_site(
        self,
        request_id: str,
    ) -> dict[str, Any]:
        """Fetch the schemeful site for a request.

        Args:
            request_id: Request ID from a network event.

        Returns:
            Dict with ``schemefulSite`` string.
        """
        return await self._call(
            "Network.fetchSchemefulSite",
            {"requestId": request_id},
        )

    async def set_cookie_controls(
        self,
        enable_third_party_cookie_restriction: bool = False,
        enable_same_site_by_default: bool = False,
        without_same_site_lax_by_default: bool = False,
    ) -> dict[str, Any]:
        """Set cookie controls.

        Args:
            enable_third_party_cookie_restriction: Block third-party cookies.
            enable_same_site_by_default: Enable SameSite by default.
            without_same_site_lax_by_default: Disable SameSite=Lax by default.
        """
        return await self._call(
            "Network.setCookieControls",
            {
                "enableThirdPartyCookieRestriction": enable_third_party_cookie_restriction,
                "enableSameSiteByDefault": enable_same_site_by_default,
                "withoutSameSiteLaxByDefault": without_same_site_lax_by_default,
            },
        )

    async def enable_device_bound_sessions(self, enable: bool) -> dict[str, Any]:
        """Enable or disable device bound sessions.

        Args:
            enable: Whether to enable device bound sessions.
        """
        return await self._call(
            "Network.enableDeviceBoundSessions",
            {"enable": enable},
        )

    async def delete_device_bound_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Delete a device bound session.

        Args:
            session_id: Session ID to delete.
        """
        return await self._call(
            "Network.deleteDeviceBoundSession",
            {"sessionId": session_id},
        )

    async def configure_durable_messages(
        self,
        max_messages: int | None = None,
    ) -> dict[str, Any]:
        """Configure durable messages.

        Args:
            max_messages: Optional max number of durable messages.
        """
        params: dict[str, Any] = {}
        if max_messages is not None:
            params["maxMessages"] = max_messages
        return await self._call(
            "Network.configureDurableMessages",
            params if params else None,
        )
