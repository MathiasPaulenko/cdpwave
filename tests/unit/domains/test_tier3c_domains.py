"""Unit tests for Accessibility, Storage, Tracing, and Animation domains."""

import pytest

from cdpwave.domains.accessibility import AccessibilityDomain
from cdpwave.domains.animation import AnimationDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.domains.tracing import TracingDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestAccessibilityDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = AccessibilityDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Accessibility.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = AccessibilityDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Accessibility.disable", None)

    async def test_get_full_ax_tree(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_full_ax_tree()
        assert fake.last_call == ("Accessibility.getFullAXTree", {})

    async def test_get_partial_ax_tree(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_partial_ax_tree(node_id=42)
        method, params = fake.last_call
        assert method == "Accessibility.getPartialAXTree"
        assert params is not None
        assert params["nodeId"] == 42
        assert params["fetchRelatives"] is True

    async def test_get_root_ax_node(self) -> None:
        fake = FakeSender({"node": {}})
        domain = AccessibilityDomain(fake)
        await domain.get_root_ax_node()
        assert fake.last_call == ("Accessibility.getRootAXNode", {})

    async def test_get_child_ax_nodes(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_child_ax_nodes("node1")
        assert fake.last_call == (
            "Accessibility.getChildAXNodes",
            {"id": "node1"},
        )

    async def test_query_ax_tree(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.query_ax_tree(role="button")
        method, params = fake.last_call
        assert method == "Accessibility.queryAXTree"
        assert params is not None
        assert params["role"] == "button"

    async def test_get_full_ax_tree_with_depth(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_full_ax_tree(depth=2)
        method, params = fake.last_call
        assert params is not None
        assert params["depth"] == 2

    async def test_get_full_ax_tree_with_frame_id(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_full_ax_tree(frame_id="F-1")
        method, params = fake.last_call
        assert params is not None
        assert params["frameId"] == "F-1"

    async def test_get_ax_node_and_ancestors(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_ax_node_and_ancestors(node_id=42)
        method, params = fake.last_call
        assert method == "Accessibility.getAXNodeAndAncestors"
        assert params is not None
        assert params["nodeId"] == 42

    async def test_get_ax_node_and_ancestors_no_params(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake)
        await domain.get_ax_node_and_ancestors()
        assert fake.last_call == ("Accessibility.getAXNodeAndAncestors", {})


@pytest.mark.unit
class TestStorageDomain:
    async def test_get_cookies(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = StorageDomain(fake)
        await domain.get_cookies()
        assert fake.last_call == ("Storage.getCookies", {})

    async def test_set_cookies(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.set_cookies([{"name": "test", "value": "1"}])
        method, params = fake.last_call
        assert method == "Storage.setCookies"
        assert params is not None
        assert len(params["cookies"]) == 1

    async def test_clear_cookies(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_cookies()
        assert fake.last_call == ("Storage.clearCookies", {})

    async def test_get_usage_and_quota(self) -> None:
        fake = FakeSender({"usage": 100, "quota": 1000})
        domain = StorageDomain(fake)
        await domain.get_usage_and_quota("https://example.com")
        assert fake.last_call == (
            "Storage.getUsageAndQuota",
            {"origin": "https://example.com"},
        )

    async def test_clear_data_for_origin(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_data_for_origin("https://example.com", "all")
        assert fake.last_call == (
            "Storage.clearDataForOrigin",
            {"origin": "https://example.com", "storageTypes": "all"},
        )

    async def test_get_trust_tokens(self) -> None:
        fake = FakeSender({"tokens": []})
        domain = StorageDomain(fake)
        await domain.get_trust_tokens()
        assert fake.last_call == ("Storage.getTrustTokens", None)

    async def test_clear_trust_tokens(self) -> None:
        fake = FakeSender({"didDeleteTokens": True})
        domain = StorageDomain(fake)
        await domain.clear_trust_tokens("https://issuer.example.com")
        assert fake.last_call == (
            "Storage.clearTrustTokens",
            {"issuerOrigin": "https://issuer.example.com"},
        )

    async def test_get_storage_key_for_frame(self) -> None:
        fake = FakeSender({"storageKey": "https://example.com"})
        domain = StorageDomain(fake)
        await domain.get_storage_key_for_frame("frame1")
        assert fake.last_call == (
            "Storage.getStorageKeyForFrame",
            {"frameId": "frame1"},
        )


@pytest.mark.unit
class TestTracingDomain:
    async def test_start(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.start(
            trace_config={"recordMode": "recordUntilFull"},
            transfer_mode="ReportEvents",
        )
        method, params = fake.last_call
        assert method == "Tracing.start"
        assert params is not None
        assert params["traceConfig"] == {"recordMode": "recordUntilFull"}
        assert params["transferMode"] == "ReportEvents"

    async def test_end(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.end()
        assert fake.last_call == ("Tracing.end", None)

    async def test_get_categories(self) -> None:
        fake = FakeSender({"categories": ["devtools.timeline"]})
        domain = TracingDomain(fake)
        await domain.get_categories()
        assert fake.last_call == ("Tracing.getCategories", None)

    async def test_record_clock_sync_marker(self) -> None:
        fake = FakeSender({})
        domain = TracingDomain(fake)
        await domain.record_clock_sync_marker("sync1")
        assert fake.last_call == (
            "Tracing.recordClockSyncMarker",
            {"syncId": "sync1"},
        )

    async def test_get_track_event_descriptor(self) -> None:
        fake = FakeSender({"descriptor": "dGVzdA=="})
        domain = TracingDomain(fake)
        await domain.get_track_event_descriptor()
        assert fake.last_call == ("Tracing.getTrackEventDescriptor", None)

    async def test_request_memory_dump(self) -> None:
        fake = FakeSender({"dumpGuid": "guid", "success": True})
        domain = TracingDomain(fake)
        await domain.request_memory_dump()
        method, params = fake.last_call
        assert method == "Tracing.requestMemoryDump"
        assert params is not None
        assert params["deterministic"] is False


@pytest.mark.unit
class TestAnimationDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Animation.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Animation.disable", None)

    async def test_get_current_time(self) -> None:
        fake = FakeSender({"currentTime": 500})
        domain = AnimationDomain(fake)
        await domain.get_current_time("anim1")
        assert fake.last_call == (
            "Animation.getCurrentTime",
            {"id": "anim1"},
        )

    async def test_set_paused(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.set_paused(["anim1", "anim2"], True)
        method, params = fake.last_call
        assert method == "Animation.setPaused"
        assert params is not None
        assert params["animations"] == ["anim1", "anim2"]
        assert params["paused"] is True

    async def test_set_playback_rate(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.set_playback_rate(2.0)
        assert fake.last_call == (
            "Animation.setPlaybackRate",
            {"playbackRate": 2.0},
        )

    async def test_set_timing(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.set_timing("anim1", 1000, 200)
        assert fake.last_call == (
            "Animation.setTiming",
            {"animationId": "anim1", "duration": 1000, "delay": 200},
        )

    async def test_release_animations(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.release_animations(["anim1"])
        assert fake.last_call == (
            "Animation.releaseAnimations",
            {"animations": ["anim1"]},
        )

    async def test_seek_to(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.seek_to(["anim1"], 500)
        method, params = fake.last_call
        assert method == "Animation.seekAnimations"
        assert params is not None
        assert params["animations"] == ["anim1"]
        assert params["currentTime"] == 500

    async def test_seek_animations(self) -> None:
        fake = FakeSender({})
        domain = AnimationDomain(fake)
        await domain.seek_animations(["anim1", "anim2"], 1000)
        method, params = fake.last_call
        assert method == "Animation.seekAnimations"
        assert params is not None
        assert params["animations"] == ["anim1", "anim2"]
        assert params["currentTime"] == 1000

    async def test_get_playback_rate(self) -> None:
        fake = FakeSender({"playbackRate": 1.0})
        domain = AnimationDomain(fake)
        await domain.get_playback_rate()
        assert fake.last_call == ("Animation.getPlaybackRate", None)

    async def test_resolve_animation(self) -> None:
        fake = FakeSender({"remoteObject": {}})
        domain = AnimationDomain(fake)
        await domain.resolve_animation("anim1")
        assert fake.last_call == (
            "Animation.resolveAnimation",
            {"animationId": "anim1"},
        )

    async def test_replay(self) -> None:
        fake = FakeSender({"currentTime": 0})
        domain = AnimationDomain(fake)
        await domain.replay(["anim1"])
        method, params = fake.last_call
        assert method == "Animation.replay"
        assert params is not None
        assert params["animations"] == ["anim1"]
