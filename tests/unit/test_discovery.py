from unittest.mock import patch

import pytest

from cdpwave.browser.discovery import TargetDiscovery, TargetInfo, VersionInfo


class TestTargetDiscovery:
    @pytest.fixture
    def discovery(self) -> TargetDiscovery:
        return TargetDiscovery(host="localhost", port=9222)

    async def test_get_version(self, discovery: TargetDiscovery) -> None:
        mock_data = {
            "Browser": "Chrome/125.0",
            "Protocol-Version": "1.3",
            "User-Agent": "Mozilla/5.0",
            "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/abc",
        }
        with patch("cdpwave.browser.discovery._http_get", return_value=mock_data):
            result = await discovery.get_version()
        assert isinstance(result, VersionInfo)
        assert result.browser == "Chrome/125.0"
        assert result.protocol_version == "1.3"
        assert result.user_agent == "Mozilla/5.0"
        assert result.web_socket_debugger_url == "ws://localhost:9222/devtools/browser/abc"

    async def test_list_targets(self, discovery: TargetDiscovery) -> None:
        mock_data = [
            {
                "id": "target-1",
                "type": "page",
                "title": "Example",
                "url": "https://example.com",
                "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/target-1",
            },
            {
                "id": "target-2",
                "type": "background_page",
                "title": "Background",
                "url": "chrome://extension",
                "webSocketDebuggerUrl": None,
            },
        ]
        with patch("cdpwave.browser.discovery._http_get", return_value=mock_data):
            result = await discovery.list_targets()
        assert len(result) == 2
        assert isinstance(result[0], TargetInfo)
        assert result[0].target_id == "target-1"
        assert result[0].type == "page"
        assert result[0].web_socket_debugger_url == "ws://localhost:9222/devtools/page/target-1"
        assert result[1].web_socket_debugger_url is None

    async def test_new_tab(self, discovery: TargetDiscovery) -> None:
        mock_data = {
            "id": "new-target",
            "type": "page",
            "title": "",
            "url": "about:blank",
            "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/new-target",
        }
        with patch("cdpwave.browser.discovery._http_put", return_value=mock_data):
            result = await discovery.new_tab("about:blank")
        assert isinstance(result, TargetInfo)
        assert result.target_id == "new-target"

    async def test_activate_tab(self, discovery: TargetDiscovery) -> None:
        with patch("cdpwave.browser.discovery._http_get", return_value={}):
            await discovery.activate_tab("target-1")

    async def test_close_tab(self, discovery: TargetDiscovery) -> None:
        with patch("cdpwave.browser.discovery._http_get", return_value={}):
            await discovery.close_tab("target-1")

    async def test_base_url_construction(self) -> None:
        discovery = TargetDiscovery(host="127.0.0.1", port=8888)
        mock_data = {
            "Browser": "Chrome/125.0",
            "Protocol-Version": "1.3",
            "User-Agent": "test",
            "webSocketDebuggerUrl": "ws://127.0.0.1:8888/devtools/browser/xyz",
        }
        with patch("cdpwave.browser.discovery._http_get", return_value=mock_data) as mock_get:
            await discovery.get_version()
            mock_get.assert_called_once_with("http://127.0.0.1:8888/json/version")
