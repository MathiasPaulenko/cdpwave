"""Unit tests for DOMSnapshot domain."""

from cdpwave.domains.dom_snapshot import DOMSnapshotDomain
from tests.unit.domains.test_domains import FakeSender


class TestDOMSnapshotDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.enable()
        assert fake.last_call == ("DOMSnapshot.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = DOMSnapshotDomain(fake)
        await domain.disable()
        assert fake.last_call == ("DOMSnapshot.disable", None)

    async def test_capture_snapshot_defaults(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot()
        method, params = fake.last_call
        assert method == "DOMSnapshot.captureSnapshot"
        assert params == {}

    async def test_capture_snapshot_with_styles(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            computed_styles=["color", "display"],
            include_paint_order=True,
            include_dom_rects=True,
        )
        method, params = fake.last_call
        assert method == "DOMSnapshot.captureSnapshot"
        assert params is not None
        assert params["computedStyles"] == ["color", "display"]
        assert params["includePaintOrder"] is True
        assert params["includeDOMRects"] is True

    async def test_capture_snapshot_experimental_params(self) -> None:
        fake = FakeSender({"documents": [], "strings": []})
        domain = DOMSnapshotDomain(fake)
        await domain.capture_snapshot(
            include_blended_background_colors=True,
            include_text_color_opacities=True,
        )
        method, params = fake.last_call
        assert method == "DOMSnapshot.captureSnapshot"
        assert params is not None
        assert params["includeBlendedBackgroundColors"] is True
        assert params["includeTextColorOpacities"] is True
