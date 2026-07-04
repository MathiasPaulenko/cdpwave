import pytest

from cdpwave.exceptions import (
    BrowserNotFoundError,
    CDPError,
    CommandError,
    CommandTimeoutError,
    ConnectionClosedError,
    DiscoveryError,
    SessionClosedError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_cdp_error(self) -> None:
        for exc_class in [
            ConnectionClosedError,
            CommandError,
            CommandTimeoutError,
            BrowserNotFoundError,
            SessionClosedError,
            DiscoveryError,
        ]:
            assert issubclass(exc_class, CDPError)

    def test_cdp_error_inherits_from_exception(self) -> None:
        assert issubclass(CDPError, Exception)

    def test_command_error_stores_code_and_message(self) -> None:
        exc = CommandError(code=-32602, message="Invalid params")
        assert exc.code == -32602
        assert exc.message == "Invalid params"
        assert exc.data is None

    def test_command_error_with_data(self) -> None:
        data = {"field": "url"}
        exc = CommandError(code=-32602, message="Invalid params", data=data)
        assert exc.data == data

    def test_command_error_str(self) -> None:
        exc = CommandError(code=-32000, message="Server error")
        assert str(exc) == "[-32000] Server error"

    def test_command_error_is_cdp_error(self) -> None:
        exc = CommandError(code=-1, message="fail")
        assert isinstance(exc, CDPError)

    def test_can_raise_and_catch_as_base(self) -> None:
        with pytest.raises(CDPError):
            raise ConnectionClosedError("closed")

    def test_can_raise_and_catch_specific(self) -> None:
        with pytest.raises(CommandTimeoutError):
            raise CommandTimeoutError("timeout")
