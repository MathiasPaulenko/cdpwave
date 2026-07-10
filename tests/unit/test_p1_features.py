"""Unit tests for P1 features: TypedDicts, event error recovery, DOMStorage separation."""

import pytest

from cdpwave.domains.dom_storage import DOMStorageDomain
from cdpwave.events.dispatcher import EventDispatcher
from cdpwave.types import (
    DOMGetDocumentResult,
    DOMNode,
    ExceptionDetails,
    NetworkCookie,
    NetworkGetCookiesResult,
    PageNavigateResult,
    RemoteObject,
    RuntimeEvaluateResult,
    TargetAttachToTargetResult,
    TargetCreateTargetResult,
)
from tests.unit.fake_sender import FakeSender


class TestTypedDicts:
    def test_page_navigate_result_is_dict(self) -> None:
        result: PageNavigateResult = {
            "frameId": "F1",
            "loaderId": "L1",
        }
        assert result["frameId"] == "F1"

    def test_runtime_evaluate_result_is_dict(self) -> None:
        result: RuntimeEvaluateResult = {
            "result": {"type": "number", "value": 42},
        }
        assert result["result"]["value"] == 42

    def test_dom_get_document_result_is_dict(self) -> None:
        result: DOMGetDocumentResult = {
            "root": {"nodeId": 1, "nodeType": 9, "nodeName": "#document"},
        }
        assert result["root"]["nodeId"] == 1

    def test_network_get_cookies_result_is_dict(self) -> None:
        result: NetworkGetCookiesResult = {
            "cookies": [{"name": "k", "value": "v"}],
        }
        assert len(result["cookies"]) == 1

    def test_target_create_target_result_is_dict(self) -> None:
        result: TargetCreateTargetResult = {"targetId": "T-1"}
        assert result["targetId"] == "T-1"

    def test_target_attach_to_target_result_is_dict(self) -> None:
        result: TargetAttachToTargetResult = {"sessionId": "S-1"}
        assert result["sessionId"] == "S-1"

    def test_remote_object_typed_dict(self) -> None:
        obj: RemoteObject = {"type": "string", "value": "hello"}
        assert obj["type"] == "string"

    def test_exception_details_typed_dict(self) -> None:
        exc: ExceptionDetails = {"exceptionId": 1, "text": "Error"}
        assert exc["exceptionId"] == 1

    def test_network_cookie_typed_dict(self) -> None:
        cookie: NetworkCookie = {"name": "k", "value": "v", "domain": ".example.com"}
        assert cookie["name"] == "k"

    def test_dom_node_typed_dict(self) -> None:
        node: DOMNode = {"nodeId": 1, "nodeType": 1, "nodeName": "div"}
        assert node["nodeId"] == 1


class TestEventErrorRecovery:
    async def test_default_fire_and_forget(self) -> None:
        dispatcher = EventDispatcher()
        errors: list[str] = []

        async def good_handler(params: dict) -> None:
            errors.append("good")

        async def bad_handler(params: dict) -> None:
            raise ValueError("boom")

        async def good_handler2(params: dict) -> None:
            errors.append("good2")

        dispatcher.on("test", good_handler)
        dispatcher.on("test", bad_handler)
        dispatcher.on("test", good_handler2)
        await dispatcher.dispatch("test", {})
        assert errors == ["good", "good2"]

    async def test_strict_events_reraises(self) -> None:
        dispatcher = EventDispatcher(strict_events=True)

        async def bad_handler(params: dict) -> None:
            raise ValueError("boom")

        dispatcher.on("test", bad_handler)
        with pytest.raises(ValueError, match="boom"):
            await dispatcher.dispatch("test", {})

    async def test_on_event_error_callback(self) -> None:
        captured: list[tuple[str, BaseException]] = []

        def on_error(
            event_name: str,
            params: dict,
            exc: BaseException,
        ) -> None:
            captured.append((event_name, exc))

        dispatcher = EventDispatcher(on_event_error=on_error)

        async def bad_handler(params: dict) -> None:
            raise RuntimeError("fail")

        dispatcher.on("test", bad_handler)
        await dispatcher.dispatch("test", {"v": 1})
        assert len(captured) == 1
        assert captured[0][0] == "test"
        assert isinstance(captured[0][1], RuntimeError)

    async def test_on_event_error_async_callback(self) -> None:
        captured: list[str] = []

        async def on_error(
            event_name: str,
            params: dict,
            exc: BaseException,
        ) -> None:
            captured.append(f"{event_name}:{exc}")

        dispatcher = EventDispatcher(on_event_error=on_error)

        async def bad_handler(params: dict) -> None:
            raise RuntimeError("fail")

        dispatcher.on("test", bad_handler)
        await dispatcher.dispatch("test", {})
        assert captured == ["test:fail"]

    async def test_strict_with_error_callback(self) -> None:
        captured: list[str] = []

        def on_error(
            event_name: str,
            params: dict,
            exc: BaseException,
        ) -> None:
            captured.append(str(exc))

        dispatcher = EventDispatcher(strict_events=True, on_event_error=on_error)

        async def bad_handler(params: dict) -> None:
            raise ValueError("boom")

        dispatcher.on("test", bad_handler)
        with pytest.raises(ValueError):
            await dispatcher.dispatch("test", {})
        assert captured == ["boom"]


class TestDOMStorageSeparation:
    async def test_dom_storage_domain_get_items(self) -> None:
        fake = FakeSender({"entries": [["k", "v"]]})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.get_dom_storage_items(sid)
        method, params = fake.last_call
        assert method == "DOMStorage.getDOMStorageItems"
        assert params is not None
        assert params["storageId"] == sid

    async def test_dom_storage_domain_set_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.set_dom_storage_item(sid, "key", "val")
        method, params = fake.last_call
        assert method == "DOMStorage.setDOMStorageItem"
        assert params is not None
        assert params["key"] == "key"

    async def test_dom_storage_domain_remove_item(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.remove_dom_storage_item(sid, "key")
        method, params = fake.last_call
        assert method == "DOMStorage.removeDOMStorageItem"
        assert params is not None
        assert params["key"] == "key"

    async def test_dom_storage_domain_clear_items(self) -> None:
        fake = FakeSender({})
        domain = DOMStorageDomain(fake)
        sid = {"securityOrigin": "https://example.com", "isLocalStorage": True}
        await domain.clear_dom_storage_items(sid)
        method, params = fake.last_call
        assert method == "DOMStorage.clear"
        assert params is not None
        assert params["storageId"] == sid

    async def test_storage_domain_has_no_dom_storage_methods(self) -> None:
        from cdpwave.domains.storage import StorageDomain

        fake = FakeSender({})
        domain = StorageDomain(fake)
        assert not hasattr(domain, "get_dom_storage_items")
        assert not hasattr(domain, "set_dom_storage_item")
        assert not hasattr(domain, "remove_dom_storage_item")
        assert not hasattr(domain, "clear_dom_storage_items")
