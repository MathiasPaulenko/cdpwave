import json

from cdpwave.transport.serializer import (
    deserialize_message,
    is_error,
    is_event,
    is_response,
    serialize_command,
)


class TestSerializeCommand:
    def test_basic_command(self) -> None:
        result = serialize_command(1, "Page.navigate", {"url": "https://example.com"})
        data = json.loads(result)
        assert data["id"] == 1
        assert data["method"] == "Page.navigate"
        assert data["params"] == {"url": "https://example.com"}
        assert "sessionId" not in data

    def test_no_params_omits_key(self) -> None:
        result = serialize_command(2, "Network.enable")
        data = json.loads(result)
        assert data["id"] == 2
        assert data["method"] == "Network.enable"
        assert "params" not in data
        assert "sessionId" not in data

    def test_none_params_omits_key(self) -> None:
        result = serialize_command(3, "Page.enable", None)
        data = json.loads(result)
        assert "params" not in data

    def test_with_session_id(self) -> None:
        result = serialize_command(4, "Runtime.evaluate", {"expression": "1+1"}, "SESSION-123")
        data = json.loads(result)
        assert data["sessionId"] == "SESSION-123"
        assert data["params"] == {"expression": "1+1"}

    def test_session_id_only_no_params(self) -> None:
        result = serialize_command(5, "Page.enable", None, "SESSION-456")
        data = json.loads(result)
        assert data["sessionId"] == "SESSION-456"
        assert "params" not in data

    def test_empty_params_included(self) -> None:
        result = serialize_command(6, "Page.reload", {})
        data = json.loads(result)
        assert data["params"] == {}

    def test_none_session_id_omits_key(self) -> None:
        result = serialize_command(7, "Page.enable", None, None)
        data = json.loads(result)
        assert "sessionId" not in data


class TestDeserializeMessage:
    def test_deserialize_response(self) -> None:
        raw = '{"id": 1, "result": {"value": 42}}'
        data = deserialize_message(raw)
        assert data["id"] == 1
        assert data["result"]["value"] == 42

    def test_deserialize_event(self) -> None:
        raw = '{"method": "Page.loadEventFired", "params": {}}'
        data = deserialize_message(raw)
        assert data["method"] == "Page.loadEventFired"

    def test_deserialize_error(self) -> None:
        raw = '{"id": 1, "error": {"code": -32602, "message": "Invalid params"}}'
        data = deserialize_message(raw)
        assert data["error"]["code"] == -32602


class TestMessageClassification:
    def test_is_response_with_id(self) -> None:
        assert is_response({"id": 1, "result": {}}) is True

    def test_is_response_without_id(self) -> None:
        assert is_response({"method": "Page.loadEventFired"}) is False

    def test_is_event_with_method_no_id(self) -> None:
        assert is_event({"method": "Page.loadEventFired", "params": {}}) is True

    def test_is_event_with_id_is_not_event(self) -> None:
        assert is_event({"id": 1, "method": "Page.navigate"}) is False

    def test_is_error_with_error_key(self) -> None:
        assert is_error({"id": 1, "error": {"code": -1, "message": "fail"}}) is True

    def test_is_error_without_error_key(self) -> None:
        assert is_error({"id": 1, "result": {}}) is False
