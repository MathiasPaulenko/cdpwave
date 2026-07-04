"""Unit tests for CacheStorage, CSS, DOMDebugger, and EventBreakpoints domains."""

import pytest

from cdpwave.domains.cache_storage import CacheStorageDomain
from cdpwave.domains.css import CSSDomain
from cdpwave.domains.dom_debugger import DOMDebuggerDomain
from cdpwave.domains.event_breakpoints import EventBreakpointsDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestCacheStorageDomain:
    async def test_delete_cache(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_cache("cache1")
        assert fake.last_call == (
            "CacheStorage.deleteCache",
            {"cacheId": "cache1"},
        )

    async def test_delete_entry(self) -> None:
        fake = FakeSender({})
        domain = CacheStorageDomain(fake)
        await domain.delete_entry("cache1", "https://example.com/data")
        assert fake.last_call == (
            "CacheStorage.deleteEntry",
            {"cacheId": "cache1", "request": "https://example.com/data"},
        )

    async def test_request_cache_names(self) -> None:
        fake = FakeSender({"caches": []})
        domain = CacheStorageDomain(fake)
        await domain.request_cache_names(security_origin="https://example.com")
        method, params = fake.last_call
        assert method == "CacheStorage.requestCacheNames"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"

    async def test_request_entries(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("cache1", skip_count=5, page_size=50)
        method, params = fake.last_call
        assert method == "CacheStorage.requestEntries"
        assert params is not None
        assert params["cacheId"] == "cache1"
        assert params["skipCount"] == 5
        assert params["pageSize"] == 50

    async def test_request_entries_with_path_filter(self) -> None:
        fake = FakeSender({"cacheDataEntries": [], "returnCount": 0})
        domain = CacheStorageDomain(fake)
        await domain.request_entries("cache1", path_filter="/api/")
        method, params = fake.last_call
        assert params is not None
        assert params["pathFilter"] == "/api/"


@pytest.mark.unit
class TestCSSDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.enable()
        assert fake.last_call == ("CSS.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.disable()
        assert fake.last_call == ("CSS.disable", None)

    async def test_get_inline_styles(self) -> None:
        fake = FakeSender({"inlineStyle": {}, "attributesStyle": {}})
        domain = CSSDomain(fake)
        await domain.get_inline_styles(42)
        assert fake.last_call == ("CSS.getInlineStyles", {"nodeId": 42})

    async def test_get_computed_style_for_node(self) -> None:
        fake = FakeSender({"computedStyle": []})
        domain = CSSDomain(fake)
        await domain.get_computed_style_for_node(42)
        assert fake.last_call == (
            "CSS.getComputedStyleForNode",
            {"nodeId": 42},
        )

    async def test_get_layout_tree_and_styles(self) -> None:
        fake = FakeSender({"layoutTree": {}, "computedStyles": []})
        domain = CSSDomain(fake)
        await domain.get_layout_tree_and_styles(node_ids=[1, 2, 3])
        method, params = fake.last_call
        assert method == "CSS.getLayoutTreeAndStyles"
        assert params is not None
        assert params["nodeIds"] == [1, 2, 3]

    async def test_get_stylesheet_text(self) -> None:
        fake = FakeSender({"text": "body { color: red; }"})
        domain = CSSDomain(fake)
        await domain.get_stylesheet_text("sheet1")
        assert fake.last_call == (
            "CSS.getStyleSheetText",
            {"styleSheetId": "sheet1"},
        )

    async def test_set_stylesheet_text(self) -> None:
        fake = FakeSender({})
        domain = CSSDomain(fake)
        await domain.set_stylesheet_text("sheet1", "body { color: blue; }")
        assert fake.last_call == (
            "CSS.setStyleSheetText",
            {"styleSheetId": "sheet1", "text": "body { color: blue; }"},
        )

    async def test_get_media_queries(self) -> None:
        fake = FakeSender({"medias": []})
        domain = CSSDomain(fake)
        await domain.get_media_queries()
        assert fake.last_call == ("CSS.getMediaQueries", None)


@pytest.mark.unit
class TestDOMDebuggerDomain:
    async def test_set_dom_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_dom_breakpoint(42, "subtree-modified")
        assert fake.last_call == (
            "DOMDebugger.setDOMBreakpoint",
            {"nodeId": 42, "type": "subtree-modified"},
        )

    async def test_remove_dom_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_dom_breakpoint(42, "subtree-modified")
        assert fake.last_call == (
            "DOMDebugger.removeDOMBreakpoint",
            {"nodeId": 42, "type": "subtree-modified"},
        )

    async def test_set_event_listener_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_event_listener_breakpoint("click")
        assert fake.last_call == (
            "DOMDebugger.setEventListenerBreakpoint",
            {"eventName": "click"},
        )

    async def test_set_event_listener_breakpoint_with_target(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_event_listener_breakpoint("click", target_name="window")
        method, params = fake.last_call
        assert params is not None
        assert params["targetName"] == "window"

    async def test_remove_event_listener_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_event_listener_breakpoint("click")
        assert fake.last_call == (
            "DOMDebugger.removeEventListenerBreakpoint",
            {"eventName": "click"},
        )

    async def test_set_xhr_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.set_xhr_breakpoint("/api/")
        assert fake.last_call == (
            "DOMDebugger.setXHRBreakpoint",
            {"url": "/api/"},
        )

    async def test_remove_xhr_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = DOMDebuggerDomain(fake)
        await domain.remove_xhr_breakpoint("/api/")
        assert fake.last_call == (
            "DOMDebugger.removeXHRBreakpoint",
            {"url": "/api/"},
        )


@pytest.mark.unit
class TestEventBreakpointsDomain:
    async def test_set_instrumentation_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_instrumentation_breakpoint("scriptFirstStatement")
        assert fake.last_call == (
            "EventBreakpoints.setInstrumentationBreakpoint",
            {"eventName": "scriptFirstStatement"},
        )

    async def test_clear_instrumentation_breakpoint(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.clear_instrumentation_breakpoint("scriptFirstStatement")
        assert fake.last_call == (
            "EventBreakpoints.clearInstrumentationBreakpoint",
            {"eventName": "scriptFirstStatement"},
        )

    async def test_set_breakpoint_on_native_event(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_breakpoint_on_native_event("click")
        assert fake.last_call == (
            "EventBreakpoints.setBreakpointOnNativeEvent",
            {"eventName": "click"},
        )

    async def test_set_breakpoint_on_native_event_with_target(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.set_breakpoint_on_native_event("click", target_name="document")
        method, params = fake.last_call
        assert params is not None
        assert params["targetName"] == "document"

    async def test_clear_breakpoint_on_native_event(self) -> None:
        fake = FakeSender({})
        domain = EventBreakpointsDomain(fake)
        await domain.clear_breakpoint_on_native_event("click")
        assert fake.last_call == (
            "EventBreakpoints.clearBreakpointOnNativeEvent",
            {"eventName": "click"},
        )
