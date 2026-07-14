"""Edge-case tests for the Target domain — validation branches only.

Targets every TypeError/ValueError raise in TargetDomain to push
coverage from 80% to >=90%.
"""

import pytest

from cdpwave.domains.target import TargetDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestTargetEdgeValidation:
    async def test_create_target_url_not_str(self) -> None:
        d = TargetDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url must be a string"):
            await d.create_target(123)  # type: ignore[arg-type]

    async def test_create_target_url_empty(self) -> None:
        d = TargetDomain(FakeSender({}))
        with pytest.raises(ValueError, match="url must not be empty"):
            await d.create_target("")

    async def test_create_target_window_state_not_str(self) -> None:
        d = TargetDomain(FakeSender({}))
        with pytest.raises(TypeError, match="window_state must be a string or None"):
            await d.create_target("http://x", window_state=123)  # type: ignore[arg-type]

    async def test_create_target_window_state_invalid(self) -> None:
        d = TargetDomain(FakeSender({}))
        with pytest.raises(ValueError, match="window_state must be one of"):
            await d.create_target("http://x", window_state="invalid")

    async def test_expose_dev_tools_protocol_no_binding_name(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.expose_dev_tools_protocol("target-1")
        _, params = fake.last_call
        assert "bindingName" not in params

    async def test_set_remote_locations(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.set_remote_locations([{"host": "localhost", "port": "9222"}])
        _, params = fake.last_call
        assert params["locations"] == [{"host": "localhost", "port": "9222"}]

    async def test_open_dev_tools_no_panel_id(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.open_dev_tools("target-1")
        _, params = fake.last_call
        assert "panelId" not in params


@pytest.mark.unit
class TestTargetEdgeHappyPaths:
    async def test_create_target_with_left_top(self) -> None:
        fake = FakeSender({"targetId": "t1"})
        d = TargetDomain(fake)
        await d.create_target("http://x", left=0, top=0)
        method, params = fake.last_call
        assert method == "Target.createTarget"
        assert params["left"] == 0
        assert params["top"] == 0

    async def test_create_target_with_width_height(self) -> None:
        fake = FakeSender({"targetId": "t1"})
        d = TargetDomain(fake)
        await d.create_target("http://x", width=800, height=600)
        _, params = fake.last_call
        assert params["width"] == 800
        assert params["height"] == 600

    async def test_create_target_with_browser_context_id(self) -> None:
        fake = FakeSender({"targetId": "t1"})
        d = TargetDomain(fake)
        await d.create_target("http://x", browser_context_id="ctx-1")
        _, params = fake.last_call
        assert params["browserContextId"] == "ctx-1"

    async def test_get_targets_with_filter(self) -> None:
        fake = FakeSender({"targetInfos": []})
        d = TargetDomain(fake)
        await d.get_targets(filter={"type": "page"})
        _, params = fake.last_call
        assert params["filter"] == {"type": "page"}

    async def test_set_auto_attach_with_filter(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.set_auto_attach(True, filter={"type": "page"})
        _, params = fake.last_call
        assert params["filter"] == {"type": "page"}

    async def test_set_discover_targets_with_filter(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.set_discover_targets(True, filter={"type": "page"})
        _, params = fake.last_call
        assert params["filter"] == {"type": "page"}

    async def test_create_browser_context_with_proxy(self) -> None:
        fake = FakeSender({"browserContextId": "ctx-1"})
        d = TargetDomain(fake)
        await d.create_browser_context(
            proxy_server="http://proxy:8080",
            proxy_bypass_list="localhost",
            origins_with_universal_network_access=["http://x"],
        )
        _, params = fake.last_call
        assert params["proxyServer"] == "http://proxy:8080"
        assert params["proxyBypassList"] == "localhost"
        assert params["originsWithUniversalNetworkAccess"] == ["http://x"]

    async def test_auto_attach_related_with_filter(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.auto_attach_related("target-1", filter={"type": "page"})
        _, params = fake.last_call
        assert params["filter"] == {"type": "page"}

    async def test_open_dev_tools_with_panel_id(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.open_dev_tools("target-1", panel_id="elements")
        _, params = fake.last_call
        assert params["panelId"] == "elements"

    async def test_expose_dev_tools_with_binding_name(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.expose_dev_tools_protocol("target-1", binding_name="cdp")
        _, params = fake.last_call
        assert params["bindingName"] == "cdp"

    async def test_send_message_to_target_with_target_id(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.send_message_to_target("msg", target_id="t1")
        _, params = fake.last_call
        assert params["targetId"] == "t1"

    async def test_send_message_to_target_with_session_id(self) -> None:
        fake = FakeSender({})
        d = TargetDomain(fake)
        await d.send_message_to_target("msg", session_id="s1")
        _, params = fake.last_call
        assert params["sessionId"] == "s1"
