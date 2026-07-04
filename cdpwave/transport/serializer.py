"""JSON serialization helpers for CDP messages."""

import json
from typing import Any


def serialize_command(
    cmd_id: int,
    method: str,
    params: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> str:
    """Serialize a CDP command into a JSON string.

    Args:
        cmd_id: Unique command ID for correlating responses.
        method: CDP method name (e.g. ``"Page.navigate"``).
        params: Optional command parameters.
        session_id: Optional target session ID for flatten sessions.

    Returns:
        JSON-encoded string ready to send over the WebSocket.
    """
    message: dict[str, Any] = {"id": cmd_id, "method": method}
    if params is not None:
        message["params"] = params
    if session_id is not None:
        message["sessionId"] = session_id
    return json.dumps(message)


def deserialize_message(raw: str) -> dict[str, Any]:
    """Deserialize a JSON string into a CDP message dict.

    Args:
        raw: Raw JSON string received from the WebSocket.

    Returns:
        Parsed CDP message dict.
    """
    result: dict[str, Any] = json.loads(raw)
    return result


def is_response(msg: dict[str, Any]) -> bool:
    """Check whether a message is a CDP response (has an ``id`` field)."""
    return "id" in msg


def is_event(msg: dict[str, Any]) -> bool:
    """Check whether a message is a CDP event (has ``method`` but no ``id``)."""
    return "method" in msg and "id" not in msg


def is_error(msg: dict[str, Any]) -> bool:
    """Check whether a response message contains a CDP error."""
    return "error" in msg
