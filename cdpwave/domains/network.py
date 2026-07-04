from typing import Any

from cdpwave.domains.base import BaseDomain


class NetworkDomain(BaseDomain):
    async def enable(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
        max_post_data_size: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if max_total_buffer_size is not None:
            params["maxTotalBufferSize"] = max_total_buffer_size
        if max_resource_buffer_size is not None:
            params["maxResourceBufferSize"] = max_resource_buffer_size
        if max_post_data_size is not None:
            params["maxPostDataSize"] = max_post_data_size
        return await self._call("Network.enable", params or None)

    async def disable(self) -> dict[str, Any]:
        return await self._call("Network.disable")

    async def set_user_agent_override(
        self,
        user_agent: str,
        accept_language: str | None = None,
        platform: str | None = None,
    ) -> dict[str, Any]:
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
        return await self._call(
            "Network.setExtraRequestHeaders",
            {"headers": headers},
        )

    async def clear_browser_cookies(self) -> dict[str, Any]:
        return await self._call("Network.clearBrowserCookies")

    async def clear_browser_cache(self) -> dict[str, Any]:
        return await self._call("Network.clearBrowserCache")

    async def get_cookies(
        self,
        urls: list[str] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if urls is not None:
            params["urls"] = urls
        return await self._call("Network.getCookies", params or None)

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
        return await self._call(
            "Network.getResponseBody",
            {"requestId": request_id},
        )

    async def set_cache_disabled(
        self,
        cache_disabled: bool,
    ) -> dict[str, Any]:
        return await self._call(
            "Network.setCacheDisabled",
            {"cacheDisabled": cache_disabled},
        )

    async def emulate_network_conditions(
        self,
        offline: bool = False,
        latency: int = 0,
        download_throughput: float = -1,
        upload_throughput: float = -1,
    ) -> dict[str, Any]:
        return await self._call(
            "Network.emulateNetworkConditions",
            {
                "offline": offline,
                "latency": latency,
                "downloadThroughput": download_throughput,
                "uploadThroughput": upload_throughput,
            },
        )
