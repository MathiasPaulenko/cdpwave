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
