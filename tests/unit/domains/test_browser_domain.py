"""Unit tests for Browser domain (browser-level, not session)."""

import pytest

from cdpwave.domains.browser import BrowserDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestBrowserDomain:
    async def test_get_version(self) -> None:
        fake = FakeSender({"protocolVersion": "1.3", "product": "Chrome"})
        domain = BrowserDomain(fake)
        await domain.get_version()
        assert fake.last_call == ("Browser.getVersion", None)

    async def test_close(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.close()
        assert fake.last_call == ("Browser.close", None)

    async def test_get_window_for_target(self) -> None:
        fake = FakeSender({"windowId": 1, "bounds": {"width": 800}})
        domain = BrowserDomain(fake)
        await domain.get_window_for_target(target_id="target123")
        method, params = fake.last_call
        assert method == "Browser.getWindowForTarget"
        assert params is not None
        assert params["targetId"] == "target123"

    async def test_get_window_for_target_with_window_id(self) -> None:
        fake = FakeSender({"windowId": 1, "bounds": {}})
        domain = BrowserDomain(fake)
        await domain.get_window_for_target(window_id=1)
        method, params = fake.last_call
        assert params is not None
        assert params["windowId"] == 1

    async def test_set_window_bounds(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_window_bounds(1, {"width": 1024, "height": 768})
        method, params = fake.last_call
        assert method == "Browser.setWindowBounds"
        assert params is not None
        assert params["windowId"] == 1
        assert params["bounds"]["width"] == 1024

    async def test_get_window_bounds(self) -> None:
        fake = FakeSender({"bounds": {"width": 800, "height": 600}})
        domain = BrowserDomain(fake)
        await domain.get_window_bounds(1)
        assert fake.last_call == (
            "Browser.getWindowBounds",
            {"windowId": 1},
        )

    async def test_grant_permissions(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.grant_permissions(
            "https://example.com", ["geolocation", "notifications"]
        )
        method, params = fake.last_call
        assert method == "Browser.grantPermissions"
        assert params is not None
        assert params["origin"] == "https://example.com"
        assert params["permissions"] == ["geolocation", "notifications"]

    async def test_grant_permissions_with_context(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.grant_permissions(
            "https://example.com",
            ["camera"],
            browser_context_id="ctx1",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_reset_permissions(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.reset_permissions("https://example.com")
        assert fake.last_call == (
            "Browser.resetPermissions",
            {"origin": "https://example.com"},
        )

    async def test_reset_permissions_with_context(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.reset_permissions(
            "https://example.com", browser_context_id="ctx1"
        )
        method, params = fake.last_call
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_set_download_behavior(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_download_behavior(
            "allow", download_path="/tmp/downloads", events_enabled=True
        )
        method, params = fake.last_call
        assert method == "Browser.setDownloadBehavior"
        assert params is not None
        assert params["behavior"] == "allow"
        assert params["downloadPath"] == "/tmp/downloads"
        assert params["eventsEnabled"] is True

    async def test_set_download_behavior_deny(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_download_behavior("deny")
        assert fake.last_call == (
            "Browser.setDownloadBehavior",
            {"behavior": "deny"},
        )
