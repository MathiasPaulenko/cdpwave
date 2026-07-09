from typing import Any

import pytest

from cdpwave.domains.console import ConsoleDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.log import LogDomain
from cdpwave.domains.network import NetworkDomain
from tests.unit.fake_sender import FakeSender


class TestNetworkDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Network.enable", None)

    async def test_enable_with_all_params(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.enable(
            max_total_buffer_size=10000,
            max_resource_buffer_size=5000,
            max_post_data_size=1000,
        )
        method, params = fake.last_call
        assert method == "Network.enable"
        assert params is not None
        assert params["maxTotalBufferSize"] == 10000
        assert params["maxResourceBufferSize"] == 5000
        assert params["maxPostDataSize"] == 1000

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Network.disable", None)

    async def test_set_user_agent_override(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_user_agent_override(
            "TestAgent/1.0",
            accept_language="en-US",
            platform="Windows",
        )
        method, params = fake.last_call
        assert method == "Network.setUserAgentOverride"
        assert params is not None
        assert params["userAgent"] == "TestAgent/1.0"
        assert params["acceptLanguage"] == "en-US"
        assert params["platform"] == "Windows"

    async def test_set_user_agent_override_required_only(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_user_agent_override("TestAgent/1.0")
        method, params = fake.last_call
        assert method == "Network.setUserAgentOverride"
        assert params is not None
        assert params["userAgent"] == "TestAgent/1.0"
        assert "acceptLanguage" not in params
        assert "platform" not in params

    async def test_set_extra_request_headers(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_extra_request_headers({"X-Custom": "value"})
        assert fake.last_call == (
            "Network.setExtraHTTPHeaders",
            {"headers": {"X-Custom": "value"}},
        )

    async def test_clear_browser_cookies(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.clear_browser_cookies()
        assert fake.last_call == ("Network.clearBrowserCookies", None)

    async def test_clear_browser_cache(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.clear_browser_cache()
        assert fake.last_call == ("Network.clearBrowserCache", None)

    async def test_get_cookies_no_urls(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = NetworkDomain(fake)
        await domain.get_cookies()
        assert fake.last_call == ("Network.getCookies", None)

    async def test_get_cookies_with_urls(self) -> None:
        fake = FakeSender({"cookies": []})
        domain = NetworkDomain(fake)
        await domain.get_cookies(urls=["https://example.com"])
        method, params = fake.last_call
        assert method == "Network.getCookies"
        assert params is not None
        assert params["urls"] == ["https://example.com"]

    async def test_set_cookie_required_only(self) -> None:
        fake = FakeSender({"success": True})
        domain = NetworkDomain(fake)
        await domain.set_cookie("session", "abc123")
        method, params = fake.last_call
        assert method == "Network.setCookie"
        assert params is not None
        assert params["name"] == "session"
        assert params["value"] == "abc123"
        assert params["secure"] is False
        assert params["httpOnly"] is False
        assert "url" not in params
        assert "domain" not in params
        assert "path" not in params
        assert "sameSite" not in params
        assert "expires" not in params

    async def test_set_cookie_all_params(self) -> None:
        fake = FakeSender({"success": True})
        domain = NetworkDomain(fake)
        await domain.set_cookie(
            "session",
            "abc123",
            url="https://example.com",
            domain="example.com",
            path="/",
            secure=True,
            http_only=True,
            same_site="Strict",
            expires=1234567890.0,
        )
        method, params = fake.last_call
        assert method == "Network.setCookie"
        assert params is not None
        assert params["url"] == "https://example.com"
        assert params["domain"] == "example.com"
        assert params["path"] == "/"
        assert params["secure"] is True
        assert params["httpOnly"] is True
        assert params["sameSite"] == "Strict"
        assert params["expires"] == 1234567890.0

    async def test_delete_cookies(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.delete_cookies("session", url="https://example.com")
        method, params = fake.last_call
        assert method == "Network.deleteCookies"
        assert params is not None
        assert params["name"] == "session"
        assert params["url"] == "https://example.com"

    async def test_get_response_body(self) -> None:
        fake = FakeSender({"body": "content", "base64Encoded": False})
        domain = NetworkDomain(fake)
        await domain.get_response_body("REQ-1")
        assert fake.last_call == (
            "Network.getResponseBody",
            {"requestId": "REQ-1"},
        )

    async def test_set_cache_disabled(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cache_disabled(True)
        assert fake.last_call == (
            "Network.setCacheDisabled",
            {"cacheDisabled": True},
        )

    async def test_emulate_network_conditions_defaults(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.emulate_network_conditions()
        method, params = fake.last_call
        assert method == "Network.emulateNetworkConditions"
        assert params is not None
        assert params["offline"] is False
        assert params["latency"] == 0
        assert params["downloadThroughput"] == -1
        assert params["uploadThroughput"] == -1

    async def test_emulate_network_conditions_offline(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.emulate_network_conditions(
            offline=True, latency=100, download_throughput=50000
        )
        method, params = fake.last_call
        assert params is not None
        assert params["offline"] is True
        assert params["latency"] == 100
        assert params["downloadThroughput"] == 50000


class TestDOMDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.enable()
        assert fake.last_call == ("DOM.enable", None)

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.disable()
        assert fake.last_call == ("DOM.disable", None)

    async def test_get_document_defaults(self) -> None:
        fake = FakeSender({"root": {"nodeId": 1}})
        domain = DOMDomain(fake)
        await domain.get_document()
        method, params = fake.last_call
        assert method == "DOM.getDocument"
        assert params is not None
        assert params["depth"] == -1
        assert params["pierce"] is False

    async def test_get_document_with_depth_pierce(self) -> None:
        fake = FakeSender({"root": {"nodeId": 1}})
        domain = DOMDomain(fake)
        await domain.get_document(depth=2, pierce=True)
        method, params = fake.last_call
        assert params is not None
        assert params["depth"] == 2
        assert params["pierce"] is True

    async def test_get_document_invalid_depth(self) -> None:
        fake = FakeSender({"root": {"nodeId": 1}})
        domain = DOMDomain(fake)
        with pytest.raises(ValueError, match="depth must be"):
            await domain.get_document(depth=-2)

    async def test_get_outer_html(self) -> None:
        fake = FakeSender({"outerHTML": "<div>hello</div>"})
        domain = DOMDomain(fake)
        await domain.get_outer_html(42)
        assert fake.last_call == ("DOM.getOuterHTML", {"nodeId": 42})

    async def test_get_inner_html(self) -> None:
        fake = FakeSender({"innerHTML": "hello"})
        domain = DOMDomain(fake)
        await domain.get_inner_html(42)
        assert fake.last_call == ("DOM.getInnerHTML", {"nodeId": 42})

    async def test_query_selector(self) -> None:
        fake = FakeSender({"nodeId": 10})
        domain = DOMDomain(fake)
        await domain.query_selector(1, "h1")
        assert fake.last_call == (
            "DOM.querySelector",
            {"nodeId": 1, "selector": "h1"},
        )

    async def test_query_selector_all(self) -> None:
        fake = FakeSender({"nodeIds": [10, 11]})
        domain = DOMDomain(fake)
        await domain.query_selector_all(1, "div")
        assert fake.last_call == (
            "DOM.querySelectorAll",
            {"nodeId": 1, "selector": "div"},
        )

    async def test_remove_node(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.remove_node(42)
        assert fake.last_call == ("DOM.removeNode", {"nodeId": 42})

    async def test_set_attribute_value(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attribute_value(42, "class", "highlight")
        assert fake.last_call == (
            "DOM.setAttributeValue",
            {"nodeId": 42, "name": "class", "value": "highlight"},
        )

    async def test_get_attribute(self) -> None:
        fake = FakeSender({"attributes": ["class", "highlight"]})
        domain = DOMDomain(fake)
        await domain.get_attribute(42)
        assert fake.last_call == ("DOM.getAttributes", {"nodeId": 42})

    async def test_focus(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.focus(42)
        assert fake.last_call == ("DOM.focus", {"nodeId": 42})

    async def test_scroll_into_view_if_needed(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.scroll_into_view_if_needed(42)
        assert fake.last_call == (
            "DOM.scrollIntoViewIfNeeded",
            {"nodeId": 42},
        )

    async def test_remove_attribute(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.remove_attribute(42, "class")
        assert fake.last_call == (
            "DOM.removeAttribute",
            {"nodeId": 42, "name": "class"},
        )

    async def test_describe_node_with_node_id(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(node_id=42)
        method, params = fake.last_call
        assert method == "DOM.describeNode"
        assert params is not None
        assert params["nodeId"] == 42
        assert params["depth"] == -1
        assert params["pierce"] is False

    async def test_describe_node_with_backend_node_id(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(backend_node_id=10, depth=2, pierce=True)
        method, params = fake.last_call
        assert params is not None
        assert params["backendNodeId"] == 10
        assert params["depth"] == 2
        assert params["pierce"] is True
        assert "nodeId" not in params

    async def test_describe_node_with_object_id(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.describe_node(object_id="obj-1")
        method, params = fake.last_call
        assert params is not None
        assert params["objectId"] == "obj-1"

    async def test_get_box_model_with_node_id(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(node_id=42)
        assert fake.last_call == ("DOM.getBoxModel", {"nodeId": 42})

    async def test_get_box_model_with_backend_node_id(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(backend_node_id=10)
        assert fake.last_call == ("DOM.getBoxModel", {"backendNodeId": 10})

    async def test_get_box_model_with_object_id(self) -> None:
        fake = FakeSender({"model": {}})
        domain = DOMDomain(fake)
        await domain.get_box_model(object_id="obj-1")
        assert fake.last_call == ("DOM.getBoxModel", {"objectId": "obj-1"})

    async def test_get_node_for_location_defaults(self) -> None:
        fake = FakeSender({"nodeId": 5, "backendNodeId": 10, "frameId": "F1"})
        domain = DOMDomain(fake)
        await domain.get_node_for_location(100, 200)
        assert fake.last_call == (
            "DOM.getNodeForLocation",
            {"x": 100, "y": 200},
        )

    async def test_get_node_for_location_with_shadow_dom(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_node_for_location(100, 200, include_user_agent_shadow_dom=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeUserAgentShadowDOM"] is True

    async def test_resolve_node_with_node_id(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(node_id=42)
        assert fake.last_call == ("DOM.resolveNode", {"nodeId": 42})

    async def test_resolve_node_with_backend_and_group(self) -> None:
        fake = FakeSender({"object": {}})
        domain = DOMDomain(fake)
        await domain.resolve_node(backend_node_id=10, object_group="grp")
        method, params = fake.last_call
        assert params is not None
        assert params["backendNodeId"] == 10
        assert params["objectGroup"] == "grp"

    async def test_request_node(self) -> None:
        fake = FakeSender({"node": {}})
        domain = DOMDomain(fake)
        await domain.request_node(42)
        assert fake.last_call == ("DOM.requestNode", {"nodeId": 42})

    async def test_set_attributes_as_text_defaults(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attributes_as_text(42, "class='foo'")
        assert fake.last_call == (
            "DOM.setAttributesAsText",
            {"nodeId": 42, "text": "class='foo'"},
        )

    async def test_set_attributes_as_text_with_name(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_attributes_as_text(42, "class='foo'", name="class")
        method, params = fake.last_call
        assert params is not None
        assert params["name"] == "class"

    async def test_copy_to_defaults(self) -> None:
        fake = FakeSender({"nodeId": 99})
        domain = DOMDomain(fake)
        await domain.copy_to(1, 2)
        assert fake.last_call == (
            "DOM.copyTo",
            {"nodeId": 1, "targetNodeId": 2},
        )

    async def test_copy_to_with_insert_before(self) -> None:
        fake = FakeSender({"nodeId": 99})
        domain = DOMDomain(fake)
        await domain.copy_to(1, 2, insert_before_node_id=3)
        method, params = fake.last_call
        assert params is not None
        assert params["insertBeforeNodeId"] == 3

    async def test_move_to_defaults(self) -> None:
        fake = FakeSender({"nodeId": 99})
        domain = DOMDomain(fake)
        await domain.move_to(1, 2)
        assert fake.last_call == (
            "DOM.moveTo",
            {"nodeId": 1, "targetNodeId": 2},
        )

    async def test_move_to_with_insert_before(self) -> None:
        fake = FakeSender({"nodeId": 99})
        domain = DOMDomain(fake)
        await domain.move_to(1, 2, insert_before_node_id=3)
        method, params = fake.last_call
        assert params is not None
        assert params["insertBeforeNodeId"] == 3

    async def test_request_child_nodes_defaults(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.request_child_nodes(42)
        assert fake.last_call == (
            "DOM.requestChildNodes",
            {"nodeId": 42, "depth": -1, "pierce": False},
        )

    async def test_request_child_nodes_with_depth_pierce(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.request_child_nodes(42, depth=3, pierce=True)
        method, params = fake.last_call
        assert params is not None
        assert params["depth"] == 3
        assert params["pierce"] is True

    async def test_perform_search_defaults(self) -> None:
        fake = FakeSender({"searchId": "s1", "resultCount": 5})
        domain = DOMDomain(fake)
        await domain.perform_search("//div")
        assert fake.last_call == ("DOM.performSearch", {"query": "//div"})

    async def test_perform_search_with_shadow_dom(self) -> None:
        fake = FakeSender({"searchId": "s1", "resultCount": 5})
        domain = DOMDomain(fake)
        await domain.perform_search("//div", include_user_agent_shadow_dom=True)
        method, params = fake.last_call
        assert params is not None
        assert params["includeUserAgentShadowDOM"] is True

    async def test_get_search_results(self) -> None:
        fake = FakeSender({"nodeIds": [1, 2, 3]})
        domain = DOMDomain(fake)
        await domain.get_search_results("s1", 0, 10)
        assert fake.last_call == (
            "DOM.getSearchResults",
            {"searchId": "s1", "fromIndex": 0, "toIndex": 10},
        )

    async def test_discard_search_results(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.discard_search_results("s1")
        assert fake.last_call == (
            "DOM.discardSearchResults",
            {"searchId": "s1"},
        )

    async def test_set_node_value(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        await domain.set_node_value(42, "new value")
        assert fake.last_call == (
            "DOM.setNodeValue",
            {"nodeId": 42, "value": "new value"},
        )


class TestLogDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = LogDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Log.enable", None)

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = LogDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Log.disable", None)

    async def test_clear_no_params(self) -> None:
        fake = FakeSender({})
        domain = LogDomain(fake)
        await domain.clear()
        assert fake.last_call == ("Log.clear", None)

    async def test_start_violation_report(self) -> None:
        fake = FakeSender({})
        domain = LogDomain(fake)
        config: list[dict[str, Any]] = [
            {"name": "longTask", "threshold": 500},
        ]
        await domain.start_violation_report(config)
        assert fake.last_call == (
            "Log.startViolationsReport",
            {"config": config},
        )

    async def test_stop_violation_report(self) -> None:
        fake = FakeSender({})
        domain = LogDomain(fake)
        await domain.stop_violation_report()
        assert fake.last_call == ("Log.stopViolationsReport", None)


class TestConsoleDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Console.enable", None)

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Console.disable", None)

    async def test_clear_messages_no_params(self) -> None:
        fake = FakeSender({})
        domain = ConsoleDomain(fake)
        await domain.clear_messages()
        assert fake.last_call == ("Console.clearMessages", None)
