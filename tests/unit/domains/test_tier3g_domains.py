"""Unit tests for Preload, IndexedDB, Media, and DeviceAccess domains."""

import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.device_access import DeviceAccessDomain
from cdpwave.domains.indexed_db import IndexedDBDomain
from cdpwave.domains.media import MediaDomain
from cdpwave.domains.preload import PreloadDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestPreloadDomain:
    # --- disable ---

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Preload.disable", None)

    async def test_disable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        result = await domain.disable()
        assert result == {}

    # --- enable ---

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Preload.enable", None)

    async def test_enable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        result = await domain.enable()
        assert result == {}

    # --- meta tests ---

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(PreloadDomain)
            if not m.startswith("_") and callable(getattr(PreloadDomain, m))
        ]
        assert len(methods) == 2

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(PreloadDomain)
            if not m.startswith("_") and callable(getattr(PreloadDomain, m))
        ]
        expected = ["disable", "enable"]
        assert methods == expected

    async def test_inherits_base_domain(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        for name in ("disable", "enable"):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    # --- docstring tests ---

    async def test_enable_docstring_no_description(self) -> None:
        doc = PreloadDomain.enable.__doc__
        assert doc is not None
        assert "[no description]" in doc

    async def test_disable_docstring_no_description(self) -> None:
        doc = PreloadDomain.disable.__doc__
        assert doc is not None
        assert "[no description]" in doc

    async def test_enable_docstring_empty_return(self) -> None:
        doc = PreloadDomain.enable.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_disable_docstring_empty_return(self) -> None:
        doc = PreloadDomain.disable.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_module_docstring_has_types_section(self) -> None:
        import cdpwave.domains.preload as mod
        doc = mod.__doc__
        assert "Types:" in doc
        assert "RuleSetID" in doc
        assert "RuleSet" in doc
        assert "RuleSetErrorType" in doc
        assert "SpeculationAction" in doc
        assert "SpeculationTargetHint" in doc
        assert "IngAttemptKey" in doc
        assert "IngAttemptSource" in doc
        assert "PipelineID" in doc
        assert "PrerenderFinalStatus" in doc
        assert "IngStatus" in doc
        assert "PrefetchStatus" in doc
        assert "PrerenderMismatchedHeaders" in doc

    async def test_module_docstring_has_events_section(self) -> None:
        import cdpwave.domains.preload as mod
        doc = mod.__doc__
        assert "Events:" in doc
        assert "ruleSetUpdated" in doc
        assert "ruleSetRemoved" in doc
        assert "preloadEnabledStateUpdated" in doc
        assert "prefetchStatusUpdated" in doc
        assert "prerenderStatusUpdated" in doc
        assert "preloadingAttemptSourcesUpdated" in doc

    async def test_class_docstring_has_experimental_mark(self) -> None:
        doc = PreloadDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_documents_all_events(self) -> None:
        doc = PreloadDomain.__doc__
        assert doc is not None
        assert "ruleSetUpdated" in doc
        assert "ruleSetRemoved" in doc
        assert "preloadEnabledStateUpdated" in doc
        assert "prefetchStatusUpdated" in doc
        assert "prerenderStatusUpdated" in doc
        assert "preloadingAttemptSourcesUpdated" in doc

    # --- edge case tests ---

    async def test_enable_no_params_sent(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_disable_no_params_sent(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    async def test_multiple_calls_recorded(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.enable()
        assert len(fake.calls) == 3
        assert fake.calls[0] == ("Preload.enable", None)
        assert fake.calls[1] == ("Preload.disable", None)
        assert fake.calls[2] == ("Preload.enable", None)

    async def test_enable_disable_enable_cycle(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        await domain.enable()
        await domain.disable()
        result = await domain.enable()
        assert result == {}
        assert len(fake.calls) == 3

    async def test_class_docstring_has_description(self) -> None:
        doc = PreloadDomain.__doc__
        assert doc is not None
        assert "speculative loading" in doc

    async def test_module_docstring_has_description(self) -> None:
        import cdpwave.domains.preload as mod
        doc = mod.__doc__
        assert "speculative loading" in doc
        assert "prefetching" in doc

    async def test_enable_docstring_no_activates_text(self) -> None:
        doc = PreloadDomain.enable.__doc__
        assert doc is not None
        assert "Activates" not in doc
        assert "Must be called" not in doc

    async def test_disable_docstring_no_deactivates_text(self) -> None:
        doc = PreloadDomain.disable.__doc__
        assert doc is not None
        assert "Deactivates" not in doc

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(PreloadDomain, "get_preload_policy")
        assert not hasattr(PreloadDomain, "set_preload_policy")

    async def test_enable_does_not_accept_args(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        sig = inspect.signature(domain.enable)
        assert len(sig.parameters) == 0

    async def test_disable_does_not_accept_args(self) -> None:
        fake = FakeSender({})
        domain = PreloadDomain(fake)
        sig = inspect.signature(domain.disable)
        assert len(sig.parameters) == 0


@pytest.mark.unit
class TestIndexedDBDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.enable()
        assert fake.last_call == ("IndexedDB.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.disable()
        assert fake.last_call == ("IndexedDB.disable", None)

    async def test_request_database_names(self) -> None:
        fake = FakeSender({"databaseNames": ["db1", "db2"]})
        domain = IndexedDBDomain(fake)
        await domain.request_database_names(security_origin="https://example.com")
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabaseNames"
        assert params is not None
        assert params["securityOrigin"] == "https://example.com"

    async def test_request_database(self) -> None:
        fake = FakeSender({"databaseWithObjectStores": []})
        domain = IndexedDBDomain(fake)
        await domain.request_database(
            security_origin="https://example.com", database_name="testdb"
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestDatabase"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["securityOrigin"] == "https://example.com"

    async def test_request_data(self) -> None:
        fake = FakeSender({"objectStoreDataEntries": [], "hasMore": False})
        domain = IndexedDBDomain(fake)
        await domain.request_data(
            security_origin="https://example.com",
            database_name="testdb",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.requestData"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["objectStoreName"] == "store1"
        assert params["skipCount"] == 0
        assert params["pageSize"] == 10

    async def test_delete_database(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.delete_database(
            security_origin="https://example.com", database_name="testdb"
        )
        method, params = fake.last_call
        assert method == "IndexedDB.deleteDatabase"
        assert params is not None
        assert params["databaseName"] == "testdb"

    async def test_clear_object_store(self) -> None:
        fake = FakeSender({})
        domain = IndexedDBDomain(fake)
        await domain.clear_object_store(
            security_origin="https://example.com",
            database_name="testdb",
            object_store_name="store1",
        )
        method, params = fake.last_call
        assert method == "IndexedDB.clearObjectStore"
        assert params is not None
        assert params["databaseName"] == "testdb"
        assert params["objectStoreName"] == "store1"


@pytest.mark.unit
class TestMediaDomain:
    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Media.enable", None)

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = MediaDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Media.disable", None)


@pytest.mark.unit
class TestDeviceAccessDomain:
    # --- cancel_prompt ---

    async def test_cancel_prompt(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.cancel_prompt("req1")
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"id": "req1"},
        )

    async def test_cancel_prompt_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        result = await domain.cancel_prompt("req1")
        assert result == {}

    async def test_cancel_prompt_type_error_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt(123)  # type: ignore[arg-type]

    async def test_cancel_prompt_empty_string(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.cancel_prompt("")
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"id": ""},
        )

    # --- disable ---

    async def test_disable(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.disable()
        assert fake.last_call == ("DeviceAccess.disable", None)

    async def test_disable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        result = await domain.disable()
        assert result == {}

    # --- enable ---

    async def test_enable(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.enable()
        assert fake.last_call == ("DeviceAccess.enable", None)

    async def test_enable_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        result = await domain.enable()
        assert result == {}

    # --- select_prompt ---

    async def test_select_prompt(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.select_prompt("req1", "dev1")
        assert fake.last_call == (
            "DeviceAccess.selectPrompt",
            {"id": "req1", "deviceId": "dev1"},
        )

    async def test_select_prompt_returns_empty_dict(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        result = await domain.select_prompt("req1", "dev1")
        assert result == {}

    async def test_select_prompt_type_error_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(123, "dev1")  # type: ignore[arg-type]

    async def test_select_prompt_type_error_device_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="device_id must be a str"):
            await domain.select_prompt("req1", 456)  # type: ignore[arg-type]

    async def test_select_prompt_empty_strings(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.select_prompt("", "")
        assert fake.last_call == (
            "DeviceAccess.selectPrompt",
            {"id": "", "deviceId": ""},
        )

    # --- meta tests ---

    async def test_method_count(self) -> None:
        methods = [
            m for m in dir(DeviceAccessDomain)
            if not m.startswith("_") and callable(getattr(DeviceAccessDomain, m))
        ]
        assert len(methods) == 4

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(DeviceAccessDomain)
            if not m.startswith("_") and callable(getattr(DeviceAccessDomain, m))
        ]
        expected = ["cancel_prompt", "disable", "enable", "select_prompt"]
        assert methods == expected

    async def test_inherits_base_domain(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        assert isinstance(domain, BaseDomain)

    async def test_all_methods_are_coroutines(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        for name in ("cancel_prompt", "disable", "enable", "select_prompt"):
            method = getattr(domain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    # --- docstring tests ---

    async def test_enable_docstring_enable_events(self) -> None:
        doc = DeviceAccessDomain.enable.__doc__
        assert doc is not None
        assert "Enable events in this domain" in doc

    async def test_disable_docstring_disable_events(self) -> None:
        doc = DeviceAccessDomain.disable.__doc__
        assert doc is not None
        assert "Disable events in this domain" in doc

    async def test_enable_docstring_empty_return(self) -> None:
        doc = DeviceAccessDomain.enable.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_disable_docstring_empty_return(self) -> None:
        doc = DeviceAccessDomain.disable.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_select_prompt_docstring_empty_return(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_cancel_prompt_docstring_empty_return(self) -> None:
        doc = DeviceAccessDomain.cancel_prompt.__doc__
        assert doc is not None
        assert "Empty dict" in doc

    async def test_select_prompt_docstring_has_raises(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "Raises:" in doc
        assert "TypeError" in doc

    async def test_cancel_prompt_docstring_has_raises(self) -> None:
        doc = DeviceAccessDomain.cancel_prompt.__doc__
        assert doc is not None
        assert "Raises:" in doc
        assert "TypeError" in doc

    async def test_module_docstring_has_types_section(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "Types:" in doc
        assert "RequestID" in doc
        assert "DeviceID" in doc
        assert "PromptDevice" in doc

    async def test_module_docstring_has_events_section(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "Events:" in doc
        assert "deviceRequestPrompted" in doc

    async def test_class_docstring_has_experimental_mark(self) -> None:
        doc = DeviceAccessDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_documents_event(self) -> None:
        doc = DeviceAccessDomain.__doc__
        assert doc is not None
        assert "deviceRequestPrompted" in doc
        assert "selectPrompt" in doc
        assert "cancelPrompt" in doc

    # --- edge case tests ---

    async def test_cancel_prompt_none_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt(None)  # type: ignore[arg-type]

    async def test_cancel_prompt_bool_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt(True)  # type: ignore[arg-type]

    async def test_cancel_prompt_list_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt(["req1"])  # type: ignore[arg-type]

    async def test_cancel_prompt_dict_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt({"id": "req1"})  # type: ignore[arg-type]

    async def test_cancel_prompt_bytes_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.cancel_prompt(b"req1")  # type: ignore[arg-type]

    async def test_cancel_prompt_unicode(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.cancel_prompt("réq1")
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"id": "réq1"},
        )

    async def test_cancel_prompt_long_string(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        long_id = "x" * 1000
        await domain.cancel_prompt(long_id)
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"id": long_id},
        )

    async def test_cancel_prompt_special_chars(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.cancel_prompt("req-1_2.3@#$%")
        assert fake.last_call == (
            "DeviceAccess.cancelPrompt",
            {"id": "req-1_2.3@#$%"},
        )

    async def test_select_prompt_none_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(None, "dev1")  # type: ignore[arg-type]

    async def test_select_prompt_none_device_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="device_id must be a str"):
            await domain.select_prompt("req1", None)  # type: ignore[arg-type]

    async def test_select_prompt_bool_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(True, "dev1")  # type: ignore[arg-type]

    async def test_select_prompt_bool_device_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="device_id must be a str"):
            await domain.select_prompt("req1", False)  # type: ignore[arg-type]

    async def test_select_prompt_list_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(["req1"], "dev1")  # type: ignore[arg-type]

    async def test_select_prompt_dict_device_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="device_id must be a str"):
            await domain.select_prompt("req1", {"id": "dev1"})  # type: ignore[arg-type]

    async def test_select_prompt_bytes_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(b"req1", "dev1")  # type: ignore[arg-type]

    async def test_select_prompt_bytes_device_id(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="device_id must be a str"):
            await domain.select_prompt("req1", b"dev1")  # type: ignore[arg-type]

    async def test_select_prompt_both_params_wrong_id_first(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        with pytest.raises(TypeError, match="id must be a str"):
            await domain.select_prompt(123, 456)  # type: ignore[arg-type]

    async def test_select_prompt_unicode(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.select_prompt("réq1", "dév1")
        assert fake.last_call == (
            "DeviceAccess.selectPrompt",
            {"id": "réq1", "deviceId": "dév1"},
        )

    async def test_select_prompt_long_strings(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        long_id = "x" * 500
        long_dev = "y" * 500
        await domain.select_prompt(long_id, long_dev)
        assert fake.last_call == (
            "DeviceAccess.selectPrompt",
            {"id": long_id, "deviceId": long_dev},
        )

    async def test_select_prompt_special_chars(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.select_prompt("req-1@#$", "dev-2@#$")
        assert fake.last_call == (
            "DeviceAccess.selectPrompt",
            {"id": "req-1@#$", "deviceId": "dev-2@#$"},
        )

    async def test_multiple_calls_recorded(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.enable()
        await domain.disable()
        await domain.cancel_prompt("req1")
        await domain.select_prompt("req1", "dev1")
        assert len(fake.calls) == 4
        assert fake.calls[0] == ("DeviceAccess.enable", None)
        assert fake.calls[1] == ("DeviceAccess.disable", None)
        assert fake.calls[2] == ("DeviceAccess.cancelPrompt", {"id": "req1"})
        assert fake.calls[3] == (
            "DeviceAccess.selectPrompt",
            {"id": "req1", "deviceId": "dev1"},
        )

    async def test_enable_disable_enable_cycle(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.enable()
        await domain.disable()
        result = await domain.enable()
        assert result == {}
        assert len(fake.calls) == 3

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(DeviceAccessDomain, "select_bluetooth_device")

    async def test_class_docstring_has_description(self) -> None:
        doc = DeviceAccessDomain.__doc__
        assert doc is not None
        assert "device access" in doc

    async def test_module_docstring_has_description(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "Bluetooth" in doc

    async def test_enable_docstring_no_activates_text(self) -> None:
        doc = DeviceAccessDomain.enable.__doc__
        assert doc is not None
        assert "Activates" not in doc
        assert "Must be called" not in doc

    async def test_disable_docstring_no_deactivates_text(self) -> None:
        doc = DeviceAccessDomain.disable.__doc__
        assert doc is not None
        assert "Deactivates" not in doc

    async def test_select_prompt_docstring_mentions_device_request_prompted(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "deviceRequestPrompted" in doc

    async def test_cancel_prompt_docstring_mentions_device_request_prompted(self) -> None:
        doc = DeviceAccessDomain.cancel_prompt.__doc__
        assert doc is not None
        assert "deviceRequestPrompted" in doc

    async def test_select_prompt_docstring_describes_id_param(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "id:" in doc
        assert "Device request id" in doc

    async def test_select_prompt_docstring_describes_device_id_param(self) -> None:
        doc = DeviceAccessDomain.select_prompt.__doc__
        assert doc is not None
        assert "device_id:" in doc
        assert "device id" in doc.lower()

    async def test_cancel_prompt_docstring_describes_id_param(self) -> None:
        doc = DeviceAccessDomain.cancel_prompt.__doc__
        assert doc is not None
        assert "id:" in doc
        assert "Device request id" in doc

    async def test_select_prompt_signature(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        sig = inspect.signature(domain.select_prompt)
        params = list(sig.parameters.keys())
        assert params == ["id", "device_id"]

    async def test_cancel_prompt_signature(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        sig = inspect.signature(domain.cancel_prompt)
        params = list(sig.parameters.keys())
        assert params == ["id"]

    async def test_enable_no_params_sent(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.enable()
        _, params = fake.last_call
        assert params is None

    async def test_disable_no_params_sent(self) -> None:
        fake = FakeSender({})
        domain = DeviceAccessDomain(fake)
        await domain.disable()
        _, params = fake.last_call
        assert params is None

    async def test_module_docstring_prompt_device_fields(self) -> None:
        import cdpwave.domains.device_access as mod
        doc = mod.__doc__
        assert "id" in doc
        assert "name" in doc
        assert "display name" in doc
