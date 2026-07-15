"""Network domain: monitoring, cookies, cache, and emulation."""

from typing import Any, cast

from cdpwave.domains.base import BaseDomain
from cdpwave.types import (
    NetworkGetCookiesResult,
    NetworkGetRequestPostDataResult,
    NetworkGetResponseBodyResult,
    NetworkLoadNetworkResourceResult,
)

_VALID_SAME_SITE = frozenset({"Strict", "Lax", "None"})
_VALID_COOKIE_PRIORITY = frozenset({"Low", "Medium", "High"})
_VALID_SOURCE_SCHEME = frozenset({"Secure", "NonSecure"})
_VALID_CONNECTION_TYPES = frozenset({
    "none",
    "cellular2g",
    "cellular3g",
    "cellular4g",
    "bluetooth",
    "ethernet",
    "wifi",
    "wimax",
    "other",
})


class NetworkDomain(BaseDomain):
    """Wrapper for the CDP Network domain."""

    async def enable(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
        max_post_data_size: int | None = None,
        report_direct_socket_traffic: bool = False,
        enable_durable_messages: bool = False,
    ) -> dict[str, Any]:
        """Enable Network domain events.

        Args:
            max_total_buffer_size: Optional max total buffer size in bytes.
            max_resource_buffer_size: Optional max per-resource buffer size.
            max_post_data_size: Optional max POST data size to capture.
            report_direct_socket_traffic: Whether DirectSocket chunk events
                should be reported.
            enable_durable_messages: Enable storing response bodies outside
                renderer. Deprecated in favor of configure_durable_messages.
        """
        if not isinstance(report_direct_socket_traffic, bool):
            raise TypeError("report_direct_socket_traffic must be a bool")
        if not isinstance(enable_durable_messages, bool):
            raise TypeError("enable_durable_messages must be a bool")
        params: dict[str, Any] = {}
        if report_direct_socket_traffic:
            params["reportDirectSocketTraffic"] = report_direct_socket_traffic
        if enable_durable_messages:
            params["enableDurableMessages"] = enable_durable_messages
        if max_total_buffer_size is not None:
            if isinstance(max_total_buffer_size, bool) or not isinstance(
                max_total_buffer_size, int
            ):
                raise TypeError("max_total_buffer_size must be an int or None")
            params["maxTotalBufferSize"] = max_total_buffer_size
        if max_resource_buffer_size is not None:
            if isinstance(max_resource_buffer_size, bool) or not isinstance(
                max_resource_buffer_size, int
            ):
                raise TypeError(
                    "max_resource_buffer_size must be an int or None"
                )
            params["maxResourceBufferSize"] = max_resource_buffer_size
        if max_post_data_size is not None:
            if isinstance(max_post_data_size, bool) or not isinstance(
                max_post_data_size, int
            ):
                raise TypeError("max_post_data_size must be an int or None")
            params["maxPostDataSize"] = max_post_data_size
        return await self._call("Network.enable", params)

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
        user_agent_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Override the browser's User-Agent string.

        Args:
            user_agent: The User-Agent string to use.
            accept_language: Optional Accept-Language header value.
            platform: Optional platform override.
            user_agent_metadata: Optional metadata for Sec-CH-UA-* headers.
        """
        params: dict[str, Any] = {"userAgent": user_agent}
        if not isinstance(user_agent, str):
            raise TypeError("user_agent must be a str")
        if accept_language is not None:
            if not isinstance(accept_language, str):
                raise TypeError("accept_language must be a str or None")
            params["acceptLanguage"] = accept_language
        if platform is not None:
            if not isinstance(platform, str):
                raise TypeError("platform must be a str or None")
            params["platform"] = platform
        if user_agent_metadata is not None:
            if not isinstance(user_agent_metadata, dict):
                raise TypeError("user_agent_metadata must be a dict or None")
            params["userAgentMetadata"] = user_agent_metadata
        return await self._call("Network.setUserAgentOverride", params)

    async def set_extra_request_headers(
        self,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        """Set extra HTTP headers for all requests.

        Args:
            headers: Dict of header name to value.
        """
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dict")
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
    ) -> NetworkGetCookiesResult:
        """Get cookies for the current page or specified URLs.

        Args:
            urls: Optional list of URLs to get cookies for.

        Returns:
            Response dict containing ``cookies`` list.
            Typed as ``NetworkGetCookiesResult`` for autocompletion.
        """
        params: dict[str, Any] = {}
        if urls is not None:
            if not isinstance(urls, list):
                raise TypeError("urls must be a list or None")
            for i, u in enumerate(urls):
                if not isinstance(u, str):
                    raise TypeError(
                        f"urls[{i}] must be a str, "
                        f"got {type(u).__name__}"
                    )
            params["urls"] = urls
        return cast("NetworkGetCookiesResult", await self._call("Network.getCookies", params))

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
        priority: str | None = None,
        source_scheme: str | None = None,
        source_port: int | None = None,
        partition_key: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Set a cookie with the given cookie data; may overwrite equivalent.

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
            priority: Optional cookie priority ("Low", "Medium", "High").
            source_scheme: Optional cookie source scheme.
            source_port: Optional cookie source port.
            partition_key: Optional cookie partition key.

        Returns:
            Response dict indicating success.
        """
        params: dict[str, Any] = {
            "name": name,
            "value": value,
            "secure": secure,
            "httpOnly": http_only,
        }
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        if not isinstance(value, str):
            raise TypeError("value must be a str")
        if not isinstance(secure, bool):
            raise TypeError("secure must be a bool")
        if not isinstance(http_only, bool):
            raise TypeError("http_only must be a bool")
        if url is not None:
            if not isinstance(url, str):
                raise TypeError("url must be a str or None")
            params["url"] = url
        if domain is not None:
            if not isinstance(domain, str):
                raise TypeError("domain must be a str or None")
            params["domain"] = domain
        if path is not None:
            if not isinstance(path, str):
                raise TypeError("path must be a str or None")
            params["path"] = path
        if same_site is not None:
            if not isinstance(same_site, str):
                raise TypeError("same_site must be a str or None")
            if same_site not in _VALID_SAME_SITE:
                raise ValueError(
                    f"same_site must be one of "
                    f"{sorted(_VALID_SAME_SITE)}, got {same_site!r}"
                )
            params["sameSite"] = same_site
        if expires is not None:
            if isinstance(expires, bool) or not isinstance(expires, (int, float)):
                raise TypeError("expires must be a number or None")
            params["expires"] = expires
        if priority is not None:
            if not isinstance(priority, str):
                raise TypeError("priority must be a str or None")
            if priority not in _VALID_COOKIE_PRIORITY:
                raise ValueError(
                    f"priority must be one of "
                    f"{sorted(_VALID_COOKIE_PRIORITY)}, got {priority!r}"
                )
            params["priority"] = priority
        if source_scheme is not None:
            if not isinstance(source_scheme, str):
                raise TypeError("source_scheme must be a str or None")
            if source_scheme not in _VALID_SOURCE_SCHEME:
                raise ValueError(
                    f"source_scheme must be one of "
                    f"{sorted(_VALID_SOURCE_SCHEME)}, "
                    f"got {source_scheme!r}"
                )
            params["sourceScheme"] = source_scheme
        if source_port is not None:
            if isinstance(source_port, bool) or not isinstance(source_port, int):
                raise TypeError("source_port must be an int or None")
            params["sourcePort"] = source_port
        if partition_key is not None:
            if not isinstance(partition_key, dict):
                raise TypeError("partition_key must be a dict or None")
            params["partitionKey"] = partition_key
        return await self._call("Network.setCookie", params)

    async def delete_cookies(
        self,
        name: str,
        url: str | None = None,
        domain: str | None = None,
        path: str | None = None,
        partition_key: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Delete cookies matching the given name and constraints.

        Args:
            name: Cookie name to delete.
            url: Optional URL to scope the deletion.
            domain: Optional domain to scope the deletion.
            path: Optional path to scope the deletion.
            partition_key: Optional cookie partition key.
        """
        params: dict[str, Any] = {"name": name}
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        if url is not None:
            if not isinstance(url, str):
                raise TypeError("url must be a str or None")
            params["url"] = url
        if domain is not None:
            if not isinstance(domain, str):
                raise TypeError("domain must be a str or None")
            params["domain"] = domain
        if path is not None:
            if not isinstance(path, str):
                raise TypeError("path must be a str or None")
            params["path"] = path
        if partition_key is not None:
            if not isinstance(partition_key, dict):
                raise TypeError("partition_key must be a dict or None")
            params["partitionKey"] = partition_key
        return await self._call("Network.deleteCookies", params)

    async def get_response_body(
        self,
        request_id: str,
    ) -> NetworkGetResponseBodyResult:
        """Get the body of a response by request ID.

        Args:
            request_id: The CDP request ID.

        Returns:
            Response dict containing ``body`` and ``base64Encoded``.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a str")
        return cast("NetworkGetResponseBodyResult", await self._call(
            "Network.getResponseBody",
            {"requestId": request_id},
        ))

    async def set_cache_disabled(
        self,
        cache_disabled: bool,
    ) -> dict[str, Any]:
        """Enable or disable the browser cache.

        Args:
            cache_disabled: If True, disable the cache.
        """
        if not isinstance(cache_disabled, bool):
            raise TypeError("cache_disabled must be a bool")
        return await self._call(
            "Network.setCacheDisabled",
            {"cacheDisabled": cache_disabled},
        )

    async def set_blocked_urls(
        self,
        urls: list[str] | None = None,
        url_patterns: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Block specific URLs from loading.

        Args:
            urls: List of URL patterns to block (supports wildcards).
            url_patterns: List of BlockPattern dicts with ``urlPattern``
                (absolute URLPattern syntax, e.g. ``*://*:*/*.css``) and
                ``block`` (bool).
        """
        params: dict[str, Any] = {}
        if url_patterns is not None:
            if not isinstance(url_patterns, list):
                raise TypeError("url_patterns must be a list or None")
            params["urlPatterns"] = url_patterns
        if urls is not None:
            if not isinstance(urls, list):
                raise TypeError("urls must be a list or None")
            for i, u in enumerate(urls):
                if not isinstance(u, str):
                    raise TypeError(
                        f"urls[{i}] must be a str, "
                        f"got {type(u).__name__}"
                    )
            params["urls"] = urls
        return await self._call("Network.setBlockedURLs", params)

    async def set_bypass_service_worker(self, bypass: bool) -> dict[str, Any]:
        """Bypass the service worker for all network requests.

        Args:
            bypass: Whether to bypass service workers.
        """
        if not isinstance(bypass, bool):
            raise TypeError("bypass must be a bool")
        return await self._call(
            "Network.setBypassServiceWorker",
            {"bypass": bypass},
        )

    async def load_network_resource(
        self,
        url: str,
        options: dict[str, Any],
        frame_id: str | None = None,
    ) -> NetworkLoadNetworkResourceResult:
        """Load a network resource directly.

        Args:
            url: URL of the resource to load.
            options: Resource load options dict.
            frame_id: Optional frame ID (mandatory for frame targets,
                omitted for worker targets).

        Returns:
            Dict with ``resource`` containing ``headers`` and ``statusCode``.
        """
        params: dict[str, Any] = {"url": url, "options": options}
        if not isinstance(url, str):
            raise TypeError("url must be a str")
        if not isinstance(options, dict):
            raise TypeError("options must be a dict")
        if frame_id is not None:
            if not isinstance(frame_id, str):
                raise TypeError("frame_id must be a str or None")
            params["frameId"] = frame_id
        return cast(
            "NetworkLoadNetworkResourceResult",
            await self._call("Network.loadNetworkResource", params),
        )

    async def get_request_post_data(self, request_id: str) -> NetworkGetRequestPostDataResult:
        """Get the POST data of a request.

        Args:
            request_id: Request ID from a network event.

        Returns:
            Dict with ``postData`` string.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a str")
        return cast("NetworkGetRequestPostDataResult", await self._call(
            "Network.getRequestPostData",
            {"requestId": request_id},
        ))

    async def set_cookies(
        self,
        cookies: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set multiple cookies at once.

        Args:
            cookies: List of cookie dicts with ``name``, ``value``,
                ``domain``, ``path``, etc.
        """
        if not isinstance(cookies, list):
            raise TypeError("cookies must be a list")
        return await self._call("Network.setCookies", {"cookies": cookies})

    async def emulate_network_conditions_by_rule(
        self,
        matched_network_conditions: list[dict[str, Any]],
        emulate_offline_service_worker: bool = False,
    ) -> dict[str, Any]:
        """Emulate network conditions for individual requests using URL patterns.

        Unlike the deprecated emulate_network_conditions, this does not affect
        navigator state. Use override_network_state to modify navigator behavior.

        Args:
            matched_network_conditions: List of NetworkConditions dicts with
                ``urlPattern``, ``offline``, ``latency``, ``downloadThroughput``,
                ``uploadThroughput``.
            emulate_offline_service_worker: True to emulate offline service worker.
        """
        if not isinstance(matched_network_conditions, list):
            raise TypeError("matched_network_conditions must be a list")
        if not isinstance(emulate_offline_service_worker, bool):
            raise TypeError("emulate_offline_service_worker must be a bool")
        return await self._call(
            "Network.emulateNetworkConditionsByRule",
            {
                "emulateOfflineServiceWorker": emulate_offline_service_worker,
                "matchedNetworkConditions": matched_network_conditions,
            },
        )

    async def override_network_state(
        self,
        offline: bool,
        latency: float,
        download_throughput: float,
        upload_throughput: float,
        connection_type: str | None = None,
    ) -> dict[str, Any]:
        """Override the state of navigator.onLine and navigator.connection.

        Args:
            offline: True to emulate internet disconnection.
            latency: Minimum latency from request sent to response headers (ms).
            download_throughput: Max download throughput (bytes/sec). -1 disables.
            upload_throughput: Max upload throughput (bytes/sec). -1 disables.
            connection_type: Optional connection type if known.
        """
        params: dict[str, Any] = {
            "offline": offline,
            "latency": latency,
            "downloadThroughput": download_throughput,
            "uploadThroughput": upload_throughput,
        }
        if not isinstance(offline, bool):
            raise TypeError("offline must be a bool")
        if isinstance(latency, bool) or not isinstance(latency, (int, float)):
            raise TypeError("latency must be a number")
        if isinstance(download_throughput, bool) or not isinstance(
            download_throughput, (int, float)
        ):
            raise TypeError("download_throughput must be a number")
        if isinstance(upload_throughput, bool) or not isinstance(
            upload_throughput, (int, float)
        ):
            raise TypeError("upload_throughput must be a number")
        if connection_type is not None:
            if not isinstance(connection_type, str):
                raise TypeError("connection_type must be a str or None")
            if connection_type not in _VALID_CONNECTION_TYPES:
                raise ValueError(
                    f"connection_type must be one of "
                    f"{sorted(_VALID_CONNECTION_TYPES)}, "
                    f"got {connection_type!r}"
                )
            params["connectionType"] = connection_type
        return await self._call("Network.overrideNetworkState", params)

    async def set_accepted_encodings(
        self,
        encodings: list[str],
    ) -> dict[str, Any]:
        """Set accepted content encodings.

        Args:
            encodings: List of accepted encodings (e.g.
                ``["gzip", "deflate", "br"]``).
        """
        if not isinstance(encodings, list):
            raise TypeError("encodings must be a list")
        for i, e in enumerate(encodings):
            if not isinstance(e, str):
                raise TypeError(
                    f"encodings[{i}] must be a str, "
                    f"got {type(e).__name__}"
                )
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
        if not isinstance(origin, str):
            raise TypeError("origin must be a str")
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
            if not isinstance(frame_id, str):
                raise TypeError("frame_id must be a str or None")
            params["frameId"] = frame_id
        return await self._call(
            "Network.getSecurityIsolationStatus",
            params,
        )

    async def enable_reporting_api(self, enable: bool) -> dict[str, Any]:
        """Enable or disable the Reporting API.

        Args:
            enable: Whether to enable the Reporting API.
        """
        if not isinstance(enable, bool):
            raise TypeError("enable must be a bool")
        return await self._call(
            "Network.enableReportingApi",
            {"enable": enable},
        )

    async def replay_xhr(self, request_id: str) -> dict[str, Any]:
        """Replay an XHR request.

        Args:
            request_id: The request ID to replay.
        """
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a str")
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
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a str")
        if not isinstance(query, str):
            raise TypeError("query must be a str")
        if not isinstance(case_sensitive, bool):
            raise TypeError("case_sensitive must be a bool")
        if not isinstance(is_regex, bool):
            raise TypeError("is_regex must be a bool")
        return await self._call("Network.searchInResponseBody", params)

    async def set_attach_debug_stack(self, enabled: bool) -> dict[str, Any]:
        """Enable or disable attaching debug stack traces to requests.

        Args:
            enabled: Whether to attach debug stacks.
        """
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a bool")
        return await self._call(
            "Network.setAttachDebugStack",
            {"enabled": enabled},
        )

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
        if not isinstance(interception_id, str):
            raise TypeError("interception_id must be a str")
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
        if not isinstance(interception_id, str):
            raise TypeError("interception_id must be a str")
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
        if not isinstance(request_id, str):
            raise TypeError("request_id must be a str")
        return await self._call(
            "Network.streamResourceContent",
            {"requestId": request_id},
        )

    async def fetch_schemeful_site(
        self,
        origin: str,
    ) -> dict[str, Any]:
        """Fetch the schemeful site for a specific origin.

        Args:
            origin: The URL origin.

        Returns:
            Dict with ``schemefulSite`` string.
        """
        if not isinstance(origin, str):
            raise TypeError("origin must be a str")
        return await self._call(
            "Network.fetchSchemefulSite",
            {"origin": origin},
        )

    async def set_cookie_controls(
        self,
        enable_third_party_cookie_restriction: bool = False,
    ) -> dict[str, Any]:
        """Set controls for third-party cookie access.

        Page reload is required before the new cookie behavior will be observed.

        Args:
            enable_third_party_cookie_restriction: Whether 3pc restriction is enabled.
        """
        if not isinstance(enable_third_party_cookie_restriction, bool):
            raise TypeError(
                "enable_third_party_cookie_restriction must be a bool"
            )
        return await self._call(
            "Network.setCookieControls",
            {"enableThirdPartyCookieRestriction": enable_third_party_cookie_restriction},
        )

    async def enable_device_bound_sessions(self, enable: bool) -> dict[str, Any]:
        """Enable or disable device bound sessions.

        Args:
            enable: Whether to enable device bound sessions.
        """
        if not isinstance(enable, bool):
            raise TypeError("enable must be a bool")
        return await self._call(
            "Network.enableDeviceBoundSessions",
            {"enable": enable},
        )

    async def delete_device_bound_session(
        self,
        key: dict[str, Any],
    ) -> dict[str, Any]:
        """Delete a device bound session.

        Args:
            key: DeviceBoundSessionKey dict identifying the session.
        """
        if not isinstance(key, dict):
            raise TypeError("key must be a dict")
        return await self._call(
            "Network.deleteDeviceBoundSession",
            {"key": key},
        )

    async def configure_durable_messages(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
    ) -> dict[str, Any]:
        """Configure storing response bodies outside of renderer.

        If max_total_buffer_size is not set, durable messages are disabled.

        Args:
            max_total_buffer_size: Optional buffer size in bytes.
            max_resource_buffer_size: Optional per-resource buffer size in bytes.
        """
        params: dict[str, Any] = {}
        if max_total_buffer_size is not None:
            if isinstance(max_total_buffer_size, bool) or not isinstance(
                max_total_buffer_size, int
            ):
                raise TypeError(
                    "max_total_buffer_size must be an int or None"
                )
            params["maxTotalBufferSize"] = max_total_buffer_size
        if max_resource_buffer_size is not None:
            if isinstance(max_resource_buffer_size, bool) or not isinstance(
                max_resource_buffer_size, int
            ):
                raise TypeError(
                    "max_resource_buffer_size must be an int or None"
                )
            params["maxResourceBufferSize"] = max_resource_buffer_size
        return await self._call(
            "Network.configureDurableMessages",
            params,
        )
