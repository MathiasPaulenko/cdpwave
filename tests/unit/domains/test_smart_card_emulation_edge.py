"""Edge case unit tests for the SmartCardEmulation domain."""

import asyncio
import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.smart_card_emulation import SmartCardEmulationDomain
from tests.unit.fake_sender import FakeSender

PDL_METHODS = [
    "enable",
    "disable",
    "report_establish_context_result",
    "report_release_context_result",
    "report_list_readers_result",
    "report_get_status_change_result",
    "report_begin_transaction_result",
    "report_plain_result",
    "report_connect_result",
    "report_data_result",
    "report_status_result",
    "report_error",
]


@pytest.mark.unit
class TestSmartCardEmulationEdgeCases:
    """Comprehensive edge-case coverage for SmartCardEmulationDomain."""

    # ------------------------------------------------------------------
    # Structure: method order, count, no spurious, inheritance,
    # coroutines, signatures.
    # ------------------------------------------------------------------

    def test_method_order_matches_pdl(self) -> None:
        methods = [
            name
            for name in SmartCardEmulationDomain.__dict__
            if not name.startswith("_") and callable(SmartCardEmulationDomain.__dict__[name])
        ]
        assert methods == PDL_METHODS

    def test_method_count(self) -> None:
        public = [
            name
            for name in SmartCardEmulationDomain.__dict__
            if not name.startswith("_") and callable(SmartCardEmulationDomain.__dict__[name])
        ]
        assert len(public) == 12

    def test_no_spurious_methods(self) -> None:
        public = {
            name
            for name in dir(SmartCardEmulationDomain)
            if not name.startswith("_") and callable(getattr(SmartCardEmulationDomain, name))
        }
        assert public == set(PDL_METHODS)

    def test_inherits_base_domain(self) -> None:
        assert issubclass(SmartCardEmulationDomain, BaseDomain)

    def test_all_methods_are_coroutines(self) -> None:
        for name in PDL_METHODS:
            method = getattr(SmartCardEmulationDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} is not a coroutine"

    def test_enable_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.enable)
        assert list(sig.parameters) == ["self"]

    def test_disable_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.disable)
        assert list(sig.parameters) == ["self"]

    def test_report_establish_context_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_establish_context_result)
        assert list(sig.parameters) == ["self", "request_id", "context_id"]

    def test_report_release_context_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_release_context_result)
        assert list(sig.parameters) == ["self", "request_id"]

    def test_report_list_readers_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_list_readers_result)
        assert list(sig.parameters) == ["self", "request_id", "readers"]

    def test_report_get_status_change_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_get_status_change_result)
        assert list(sig.parameters) == ["self", "request_id", "reader_states"]

    def test_report_begin_transaction_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_begin_transaction_result)
        assert list(sig.parameters) == ["self", "request_id", "handle"]

    def test_report_plain_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_plain_result)
        assert list(sig.parameters) == ["self", "request_id"]

    def test_report_connect_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_connect_result)
        params = list(sig.parameters)
        assert params == ["self", "request_id", "handle", "active_protocol"]
        assert sig.parameters["active_protocol"].default is None

    def test_report_data_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_data_result)
        assert list(sig.parameters) == ["self", "request_id", "data"]

    def test_report_status_result_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_status_result)
        params = list(sig.parameters)
        assert params == ["self", "request_id", "reader_name", "state", "atr", "protocol"]
        assert sig.parameters["protocol"].default is None

    def test_report_error_signature(self) -> None:
        sig = inspect.signature(SmartCardEmulationDomain.report_error)
        assert list(sig.parameters) == ["self", "request_id", "result_code"]

    # ------------------------------------------------------------------
    # enable / disable: params=None, return passthrough.
    # ------------------------------------------------------------------

    async def test_enable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.enable()
        method, params = fake.last_call
        assert method == "SmartCardEmulation.enable"
        assert params is None

    async def test_disable_sends_none_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.disable()
        method, params = fake.last_call
        assert method == "SmartCardEmulation.disable"
        assert params is None

    async def test_enable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.enable() == {"result": "ok"}

    async def test_disable_return_passthrough(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.disable() == {"result": "ok"}

    # ------------------------------------------------------------------
    # report_establish_context_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_establish_context_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_establish_context_result("req-1", 42)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportEstablishContextResult"
        assert params == {"requestId": "req-1", "contextId": 42}

    async def test_report_establish_context_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_establish_context_result("req-1", 42) == {"result": "ok"}

    async def test_report_establish_context_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_establish_context_result(bad, 42)  # type: ignore[arg-type]

    async def test_report_establish_context_result_context_id_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ([1], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"context_id must be an int.*{tname}"):
                await domain.report_establish_context_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_establish_context_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_establish_context_result(42, "bad")  # type: ignore[arg-type]

    async def test_report_establish_context_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_establish_context_result(42, 1)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_establish_context_result_str_subclass(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_establish_context_result(MyStr("req-1"), 42)
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "contextId": 42}

    async def test_report_establish_context_result_int_subclass(self) -> None:
        class MyInt(int):
            pass

        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_establish_context_result("req-1", MyInt(42))
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "contextId": 42}

    async def test_report_establish_context_result_edge_values(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_establish_context_result("", 0)
        _, params = fake.last_call
        assert params == {"requestId": "", "contextId": 0}
        await domain.report_establish_context_result("🎵", -1)
        _, params = fake.last_call
        assert params == {"requestId": "🎵", "contextId": -1}
        await domain.report_establish_context_result("r" * 500, 2147483647)
        _, params = fake.last_call
        assert params == {"requestId": "r" * 500, "contextId": 2147483647}

    # ------------------------------------------------------------------
    # report_release_context_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_release_context_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_release_context_result("req-1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportReleaseContextResult"
        assert params == {"requestId": "req-1"}

    async def test_report_release_context_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_release_context_result("req-1") == {"result": "ok"}

    async def test_report_release_context_result_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_release_context_result(bad)  # type: ignore[arg-type]

    async def test_report_release_context_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_release_context_result(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_release_context_result_empty_string(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_release_context_result("")
        _, params = fake.last_call
        assert params == {"requestId": ""}

    async def test_report_release_context_result_unicode(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_release_context_result("🎵")
        _, params = fake.last_call
        assert params == {"requestId": "🎵"}

    # ------------------------------------------------------------------
    # report_list_readers_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_list_readers_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("req-1", ["reader-a", "reader-b"])
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportListReadersResult"
        assert params == {"requestId": "req-1", "readers": ["reader-a", "reader-b"]}

    async def test_report_list_readers_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_list_readers_result("req-1", []) == {"result": "ok"}

    async def test_report_list_readers_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_list_readers_result(bad, [])  # type: ignore[arg-type]

    async def test_report_list_readers_result_readers_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"readers must be a list.*{tname}"):
                await domain.report_list_readers_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_list_readers_result_element_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"readers\\[0\\] must be a str.*{tname}"):
                await domain.report_list_readers_result("req-1", [bad])  # type: ignore[list-item]

    async def test_report_list_readers_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_list_readers_result(42, ["ok"])  # type: ignore[arg-type]

    async def test_report_list_readers_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_list_readers_result("req-1", [42])  # type: ignore[list-item]
        assert len(fake.calls) == 0

    async def test_report_list_readers_result_empty_list(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("req-1", [])
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "readers": []}

    async def test_report_list_readers_result_unicode_elements(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("req-1", ["📖-reader"])
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "readers": ["📖-reader"]}

    async def test_report_list_readers_result_str_subclass_elements(self) -> None:
        class MyStr(str):
            pass

        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_list_readers_result("req-1", [MyStr("reader-a")])
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "readers": ["reader-a"]}

    # ------------------------------------------------------------------
    # report_get_status_change_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_get_status_change_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        states = [{"reader": "r1", "state": "present"}]
        await domain.report_get_status_change_result("req-1", states)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportGetStatusChangeResult"
        assert params == {"requestId": "req-1", "readerStates": states}

    async def test_report_get_status_change_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_get_status_change_result("req-1", []) == {"result": "ok"}

    async def test_report_get_status_change_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_get_status_change_result(bad, [])  # type: ignore[arg-type]

    async def test_report_get_status_change_result_reader_states_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"reader_states must be a list.*{tname}"):
                await domain.report_get_status_change_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_get_status_change_result_element_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (42, "int"), (True, "bool"), (3.14, "float"),
                           (None, "NoneType"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"reader_states\\[0\\] must be a dict.*{tname}"):
                await domain.report_get_status_change_result("req-1", [bad])  # type: ignore[list-item]

    async def test_report_get_status_change_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_get_status_change_result(42, [])  # type: ignore[arg-type]

    async def test_report_get_status_change_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_get_status_change_result("req-1", [42])  # type: ignore[list-item]
        assert len(fake.calls) == 0

    async def test_report_get_status_change_result_empty_list(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_get_status_change_result("req-1", [])
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "readerStates": []}

    # ------------------------------------------------------------------
    # report_begin_transaction_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_begin_transaction_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_begin_transaction_result("req-1", 99)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportBeginTransactionResult"
        assert params == {"requestId": "req-1", "handle": 99}

    async def test_report_begin_transaction_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_begin_transaction_result("req-1", 99) == {"result": "ok"}

    async def test_report_begin_transaction_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_begin_transaction_result(bad, 99)  # type: ignore[arg-type]

    async def test_report_begin_transaction_result_handle_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ([1], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"handle must be an int.*{tname}"):
                await domain.report_begin_transaction_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_begin_transaction_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_begin_transaction_result(42, "bad")  # type: ignore[arg-type]

    async def test_report_begin_transaction_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_begin_transaction_result("req-1", True)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_begin_transaction_result_int_subclass(self) -> None:
        class MyInt(int):
            pass

        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_begin_transaction_result("req-1", MyInt(99))
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "handle": 99}

    # ------------------------------------------------------------------
    # report_plain_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_plain_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_plain_result("req-1")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportPlainResult"
        assert params == {"requestId": "req-1"}

    async def test_report_plain_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_plain_result("req-1") == {"result": "ok"}

    async def test_report_plain_result_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_plain_result(bad)  # type: ignore[arg-type]

    async def test_report_plain_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_plain_result(42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_plain_result_empty_string(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_plain_result("")
        _, params = fake.last_call
        assert params == {"requestId": ""}

    # ------------------------------------------------------------------
    # report_connect_result: params, optional, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_connect_result_params_without_optional(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req-1", 7)
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportConnectResult"
        assert params == {"requestId": "req-1", "handle": 7}

    async def test_report_connect_result_params_with_optional(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req-1", 7, active_protocol="t0")
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "handle": 7, "activeProtocol": "t0"}

    async def test_report_connect_result_optional_none_omitted(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req-1", 7, active_protocol=None)
        _, params = fake.last_call
        assert "activeProtocol" not in params

    async def test_report_connect_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_connect_result("req-1", 7) == {"result": "ok"}

    async def test_report_connect_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_connect_result(bad, 7)  # type: ignore[arg-type]

    async def test_report_connect_result_handle_type_errors(self) -> None:
        for bad, tname in [("x", "str"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           ([1], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"handle must be an int.*{tname}"):
                await domain.report_connect_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_connect_result_active_protocol_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"active_protocol must be a str.*{tname}"):
                await domain.report_connect_result("req-1", 7, active_protocol=bad)  # type: ignore[arg-type]

    async def test_report_connect_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_connect_result(42, "bad")  # type: ignore[arg-type]

    async def test_report_connect_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_connect_result("req-1", True)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_connect_result_active_protocol_empty_string(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req-1", 7, active_protocol="")
        _, params = fake.last_call
        assert params["activeProtocol"] == ""

    async def test_report_connect_result_active_protocol_unicode(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_connect_result("req-1", 7, active_protocol="🎵")
        _, params = fake.last_call
        assert params["activeProtocol"] == "🎵"

    # ------------------------------------------------------------------
    # report_data_result: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_data_result_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_data_result("req-1", "base64data==")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportDataResult"
        assert params == {"requestId": "req-1", "data": "base64data=="}

    async def test_report_data_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_data_result("req-1", "data") == {"result": "ok"}

    async def test_report_data_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_data_result(bad, "data")  # type: ignore[arg-type]

    async def test_report_data_result_data_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"data must be a str.*{tname}"):
                await domain.report_data_result("req-1", bad)  # type: ignore[arg-type]

    async def test_report_data_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_data_result(42, "data")  # type: ignore[arg-type]

    async def test_report_data_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_data_result("req-1", 42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_data_result_empty_string(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_data_result("req-1", "")
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "data": ""}

    async def test_report_data_result_unicode(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_data_result("req-1", "🎵")
        _, params = fake.last_call
        assert params == {"requestId": "req-1", "data": "🎵"}

    # ------------------------------------------------------------------
    # report_status_result: params, optional, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_status_result_params_without_optional(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("req-1", "reader-a", "present", "atr==")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportStatusResult"
        assert params == {"requestId": "req-1", "readerName": "reader-a",
                          "state": "present", "atr": "atr=="}

    async def test_report_status_result_params_with_optional(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("req-1", "reader-a", "present", "atr==",
                                          protocol="t0")
        _, params = fake.last_call
        assert params["protocol"] == "t0"

    async def test_report_status_result_optional_none_omitted(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("req-1", "reader-a", "present", "atr==",
                                          protocol=None)
        _, params = fake.last_call
        assert "protocol" not in params

    async def test_report_status_result_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_status_result("req-1", "r", "present", "a") == {"result": "ok"}

    async def test_report_status_result_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_status_result(bad, "r", "present", "a")  # type: ignore[arg-type]

    async def test_report_status_result_reader_name_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"reader_name must be a str.*{tname}"):
                await domain.report_status_result("req-1", bad, "present", "a")  # type: ignore[arg-type]

    async def test_report_status_result_state_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"state must be a str.*{tname}"):
                await domain.report_status_result("req-1", "r", bad, "a")  # type: ignore[arg-type]

    async def test_report_status_result_atr_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"atr must be a str.*{tname}"):
                await domain.report_status_result("req-1", "r", "present", bad)  # type: ignore[arg-type]

    async def test_report_status_result_protocol_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"protocol must be a str.*{tname}"):
                await domain.report_status_result("req-1", "r", "present", "a", protocol=bad)  # type: ignore[arg-type]

    async def test_report_status_result_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_status_result(42, "r", "present", "a")  # type: ignore[arg-type]

    async def test_report_status_result_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_status_result("req-1", "r", "present", 42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_status_result_empty_strings(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("", "", "", "")
        _, params = fake.last_call
        assert params == {"requestId": "", "readerName": "", "state": "", "atr": ""}

    async def test_report_status_result_unicode(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_status_result("🎵", "📖", "present", "🎵==")
        _, params = fake.last_call
        assert params == {"requestId": "🎵", "readerName": "📖",
                          "state": "present", "atr": "🎵=="}

    # ------------------------------------------------------------------
    # report_error: params, return, type validation.
    # ------------------------------------------------------------------

    async def test_report_error_params(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error("req-1", "cancelled")
        method, params = fake.last_call
        assert method == "SmartCardEmulation.reportError"
        assert params == {"requestId": "req-1", "resultCode": "cancelled"}

    async def test_report_error_return(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = SmartCardEmulationDomain(fake)
        assert await domain.report_error("req-1", "timeout") == {"result": "ok"}

    async def test_report_error_request_id_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"request_id must be a str.*{tname}"):
                await domain.report_error(bad, "cancelled")  # type: ignore[arg-type]

    async def test_report_error_result_code_type_errors(self) -> None:
        for bad, tname in [(42, "int"), (True, "bool"), (3.14, "float"), (None, "NoneType"),
                           (["x"], "list"), ({"x": 1}, "dict"), (b"x", "bytes")]:
            fake = FakeSender({})
            domain = SmartCardEmulationDomain(fake)
            with pytest.raises(TypeError, match=f"result_code must be a str.*{tname}"):
                await domain.report_error("req-1", bad)  # type: ignore[arg-type]

    async def test_report_error_validation_order(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError, match="request_id"):
            await domain.report_error(42, "cancelled")  # type: ignore[arg-type]

    async def test_report_error_no_cdp_on_type_error(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        with pytest.raises(TypeError):
            await domain.report_error("req-1", 42)  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_report_error_empty_strings(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error("", "")
        _, params = fake.last_call
        assert params == {"requestId": "", "resultCode": ""}

    async def test_report_error_unicode(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.report_error("🎵", "timeout")
        _, params = fake.last_call
        assert params == {"requestId": "🎵", "resultCode": "timeout"}

    # ------------------------------------------------------------------
    # Lifecycle, repeated cycles, concurrency, error propagation.
    # ------------------------------------------------------------------

    async def test_lifecycle_enable_disable(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.enable()
        await domain.disable()
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("SmartCardEmulation.enable", None)
        assert fake.calls[1] == ("SmartCardEmulation.disable", None)

    async def test_repeated_cycles(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        for _ in range(5):
            await domain.enable()
            await domain.disable()
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("SmartCardEmulation.enable", None)
            assert fake.calls[i * 2 + 1] == ("SmartCardEmulation.disable", None)

    async def test_concurrency(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await asyncio.gather(
            domain.enable(),
            domain.report_establish_context_result("req-1", 1),
            domain.report_error("req-2", "timeout"),
            domain.disable(),
        )
        assert len(fake.calls) == 4
        methods = [c[0] for c in fake.calls]
        assert "SmartCardEmulation.enable" in methods
        assert "SmartCardEmulation.reportEstablishContextResult" in methods
        assert "SmartCardEmulation.reportError" in methods
        assert "SmartCardEmulation.disable" in methods

    async def test_error_propagation(self) -> None:
        class ErrorSender:
            async def __call__(self, method: str, params: dict | None = None) -> dict:
                raise RuntimeError("cdp error")

        domain = SmartCardEmulationDomain(ErrorSender())  # type: ignore[arg-type]
        with pytest.raises(RuntimeError, match="cdp error"):
            await domain.enable()

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = SmartCardEmulationDomain(fake)
        await domain.enable()
        await domain.report_establish_context_result("req-1", 1)
        await domain.report_list_readers_result("req-2", ["r1"])
        await domain.report_error("req-3", "cancelled")
        await domain.disable()
        assert len(fake.calls) == 5

    # ------------------------------------------------------------------
    # Docstring tests.
    # ------------------------------------------------------------------

    def test_module_docstring_describes_domain(self) -> None:
        from cdpwave.domains import smart_card_emulation

        doc = smart_card_emulation.__doc__ or ""
        assert "SmartCardEmulation" in doc
        assert "smart card" in doc.lower()
        assert "experimental" in doc.lower()

    def test_module_docstring_lists_events(self) -> None:
        from cdpwave.domains import smart_card_emulation

        doc = smart_card_emulation.__doc__ or ""
        assert "establishContextRequested" in doc
        assert "releaseContextRequested" in doc
        assert "listReadersRequested" in doc
        assert "getStatusChangeRequested" in doc
        assert "cancelRequested" in doc
        assert "connectRequested" in doc
        assert "disconnectRequested" in doc
        assert "transmitRequested" in doc
        assert "controlRequested" in doc
        assert "getAttribRequested" in doc
        assert "setAttribRequested" in doc
        assert "statusRequested" in doc
        assert "beginTransactionRequested" in doc
        assert "endTransactionRequested" in doc

    def test_module_docstring_lists_commands(self) -> None:
        from cdpwave.domains import smart_card_emulation

        doc = smart_card_emulation.__doc__ or ""
        assert "enable" in doc
        assert "disable" in doc
        assert "reportEstablishContextResult" in doc
        assert "reportReleaseContextResult" in doc
        assert "reportListReadersResult" in doc
        assert "reportGetStatusChangeResult" in doc
        assert "reportBeginTransactionResult" in doc
        assert "reportPlainResult" in doc
        assert "reportConnectResult" in doc
        assert "reportDataResult" in doc
        assert "reportStatusResult" in doc
        assert "reportError" in doc

    def test_module_docstring_lists_types(self) -> None:
        from cdpwave.domains import smart_card_emulation

        doc = smart_card_emulation.__doc__ or ""
        assert "ResultCode" in doc
        assert "ShareMode" in doc
        assert "Disposition" in doc
        assert "ConnectionState" in doc
        assert "Protocol" in doc
        assert "ReaderStateFlags" in doc
        assert "ProtocolSet" in doc
        assert "ReaderStateIn" in doc
        assert "ReaderStateOut" in doc

    def test_class_docstring_describes_purpose(self) -> None:
        doc = SmartCardEmulationDomain.__doc__ or ""
        assert "SmartCardEmulation" in doc
        assert "smart card" in doc.lower()
        assert "experimental" in doc.lower()

    def test_class_docstring_lists_events(self) -> None:
        doc = SmartCardEmulationDomain.__doc__ or ""
        assert "establishContextRequested" in doc
        assert "releaseContextRequested" in doc
        assert "listReadersRequested" in doc
        assert "getStatusChangeRequested" in doc
        assert "cancelRequested" in doc
        assert "connectRequested" in doc
        assert "disconnectRequested" in doc
        assert "transmitRequested" in doc
        assert "controlRequested" in doc
        assert "getAttribRequested" in doc
        assert "setAttribRequested" in doc
        assert "statusRequested" in doc
        assert "beginTransactionRequested" in doc
        assert "endTransactionRequested" in doc

    @pytest.mark.parametrize("method_name", PDL_METHODS)
    def test_method_docstring_has_returns(self, method_name: str) -> None:
        method = getattr(SmartCardEmulationDomain, method_name)
        doc = method.__doc__ or ""
        assert "Returns:" in doc, f"{method_name} missing Returns:"

    def test_report_connect_result_docstring_raises_mentions_active_protocol(self) -> None:
        doc = SmartCardEmulationDomain.report_connect_result.__doc__ or ""
        assert "active_protocol" in doc

    @pytest.mark.parametrize("method_name", [
        "report_establish_context_result",
        "report_release_context_result",
        "report_list_readers_result",
        "report_get_status_change_result",
        "report_begin_transaction_result",
        "report_plain_result",
        "report_connect_result",
        "report_data_result",
        "report_status_result",
        "report_error",
    ])
    def test_method_docstring_has_raises(self, method_name: str) -> None:
        method = getattr(SmartCardEmulationDomain, method_name)
        doc = method.__doc__ or ""
        assert "Raises:" in doc, f"{method_name} missing Raises:"

    @pytest.mark.parametrize("method_name", [
        "report_establish_context_result",
        "report_release_context_result",
        "report_list_readers_result",
        "report_get_status_change_result",
        "report_begin_transaction_result",
        "report_plain_result",
        "report_connect_result",
        "report_data_result",
        "report_status_result",
        "report_error",
    ])
    def test_method_docstring_has_args(self, method_name: str) -> None:
        method = getattr(SmartCardEmulationDomain, method_name)
        doc = method.__doc__ or ""
        assert "Args:" in doc, f"{method_name} missing Args:"

    def test_report_status_result_docstring_raises_mentions_protocol(self) -> None:
        doc = SmartCardEmulationDomain.report_status_result.__doc__ or ""
        assert "protocol" in doc

    def test_enable_docstring_not_activates(self) -> None:
        doc = SmartCardEmulationDomain.enable.__doc__ or ""
        assert "Activates" not in doc

    def test_disable_docstring_not_deactivates(self) -> None:
        doc = SmartCardEmulationDomain.disable.__doc__ or ""
        assert "Deactivates" not in doc
