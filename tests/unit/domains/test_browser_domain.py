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

    async def test_get_window_for_target_no_params(self) -> None:
        fake = FakeSender({"windowId": 1, "bounds": {}})
        domain = BrowserDomain(fake)
        await domain.get_window_for_target()
        assert fake.last_call == ("Browser.getWindowForTarget", None)

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
        await domain.reset_permissions()
        assert fake.last_call == ("Browser.resetPermissions", None)

    async def test_reset_permissions_with_context(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.reset_permissions(browser_context_id="ctx1")
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
        method, params = fake.last_call
        assert method == "Browser.setDownloadBehavior"
        assert params is not None
        assert params["behavior"] == "deny"
        assert params["eventsEnabled"] is False

    async def test_set_download_behavior_all_params(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_download_behavior(
            "allowAndName",
            browser_context_id="ctx1",
            download_path="/tmp",
            events_enabled=True,
        )
        method, params = fake.last_call
        assert params is not None
        assert params["behavior"] == "allowAndName"
        assert params["browserContextId"] == "ctx1"
        assert params["downloadPath"] == "/tmp"
        assert params["eventsEnabled"] is True

    async def test_set_permission(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_permission(
            {"name": "geolocation"}, "granted"
        )
        method, params = fake.last_call
        assert method == "Browser.setPermission"
        assert params is not None
        assert params["permission"] == {"name": "geolocation"}
        assert params["setting"] == "granted"

    async def test_set_permission_all_params(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_permission(
            {"name": "geolocation"},
            "denied",
            origin="https://example.com",
            embedded_origin="https://embedded.com",
            browser_context_id="ctx1",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["origin"] == "https://example.com"
        assert params["embeddedOrigin"] == "https://embedded.com"
        assert params["browserContextId"] == "ctx1"

    async def test_cancel_download(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.cancel_download("guid-123")
        assert fake.last_call == (
            "Browser.cancelDownload",
            {"guid": "guid-123"},
        )

    async def test_cancel_download_with_context(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.cancel_download("guid-123", browser_context_id="ctx1")
        method, params = fake.last_call
        assert params is not None
        assert params["browserContextId"] == "ctx1"

    async def test_crash(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.crash()
        assert fake.last_call == ("Browser.crash", None)

    async def test_crash_gpu_process(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.crash_gpu_process()
        assert fake.last_call == ("Browser.crashGpuProcess", None)

    async def test_get_histograms_with_query(self) -> None:
        fake = FakeSender({"histograms": []})
        domain = BrowserDomain(fake)
        await domain.get_histograms(query="V8", delta=True)
        method, params = fake.last_call
        assert method == "Browser.getHistograms"
        assert params is not None
        assert params["query"] == "V8"
        assert params["delta"] is True

    async def test_get_histograms_defaults(self) -> None:
        fake = FakeSender({"histograms": []})
        domain = BrowserDomain(fake)
        await domain.get_histograms()
        method, params = fake.last_call
        assert params is not None
        assert params["delta"] is False
        assert "query" not in params

    async def test_get_histogram_defaults(self) -> None:
        fake = FakeSender({"histogram": {"name": "test"}})
        domain = BrowserDomain(fake)
        await domain.get_histogram("V8.ExecuteJS")
        method, params = fake.last_call
        assert params is not None
        assert params["name"] == "V8.ExecuteJS"
        assert params["delta"] is False

    async def test_set_contents_size(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_contents_size(1, width=800, height=600)
        method, params = fake.last_call
        assert method == "Browser.setContentsSize"
        assert params is not None
        assert params["windowId"] == 1
        assert params["width"] == 800
        assert params["height"] == 600

    async def test_set_contents_size_width_only(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_contents_size(1, width=800)
        method, params = fake.last_call
        assert params is not None
        assert params["width"] == 800
        assert "height" not in params

    async def test_set_dock_tile(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_dock_tile(badge_label="5", image="base64data")
        method, params = fake.last_call
        assert method == "Browser.setDockTile"
        assert params is not None
        assert params["badgeLabel"] == "5"
        assert params["image"] == "base64data"

    async def test_set_dock_tile_no_params(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.set_dock_tile()
        assert fake.last_call == ("Browser.setDockTile", None)

    async def test_execute_browser_command(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.execute_browser_command("openTabSearch")
        assert fake.last_call == (
            "Browser.executeBrowserCommand",
            {"commandId": "openTabSearch"},
        )

    async def test_add_privacy_sandbox_enrollment_override(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.add_privacy_sandbox_enrollment_override(
            "https://example.test"
        )
        assert fake.last_call == (
            "Browser.addPrivacySandboxEnrollmentOverride",
            {"url": "https://example.test"},
        )

    async def test_add_privacy_sandbox_coordinator_key_config(self) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.add_privacy_sandbox_coordinator_key_config(
            "TrustedKeyValue",
            "https://coordinator.test",
            "key-config-data",
        )
        method, params = fake.last_call
        assert method == "Browser.addPrivacySandboxCoordinatorKeyConfig"
        assert params is not None
        assert params["api"] == "TrustedKeyValue"
        assert params["coordinatorOrigin"] == "https://coordinator.test"
        assert params["keyConfig"] == "key-config-data"

    async def test_add_privacy_sandbox_coordinator_key_config_with_context(
        self,
    ) -> None:
        fake = FakeSender({})
        domain = BrowserDomain(fake)
        await domain.add_privacy_sandbox_coordinator_key_config(
            "BiddingAndAuctionServices",
            "https://coordinator.test",
            "key-config-data",
            browser_context_id="ctx1",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["browserContextId"] == "ctx1"
