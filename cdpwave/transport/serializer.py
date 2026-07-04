import json
from typing import Any


def serialize_command(
    cmd_id: int,
    method: str,
    params: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> str:
    message: dict[str, Any] = {"id": cmd_id, "method": method}
    if params is not None:
        message["params"] = params
    if session_id is not None:
        message["sessionId"] = session_id
    return json.dumps(message)


def deserialize_message(raw: str) -> dict[str, Any]:
    result: dict[str, Any] = json.loads(raw)
    return result


def is_response(msg: dict[str, Any]) -> bool:
    return "id" in msg


def is_event(msg: dict[str, Any]) -> bool:
    return "method" in msg and "id" not in msg


def is_error(msg: dict[str, Any]) -> bool:
    return "error" in msg
