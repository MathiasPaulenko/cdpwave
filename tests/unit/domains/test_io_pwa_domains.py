"""Unit tests for the IO and PWA domains.

Tests cover:
- Each method (basic call, correct params, return value)
- omitempty behaviour (None, 0, "" omitted; link_capturing always sent)
- Type validation (TypeError for each param, bool rejected for int)
- Meta-tests (method count, alphabetical order, docstrings, Raises, BaseDomain)
- Multi-call parameter isolation
- Raw send correctness
- Empty strings for str params
"""

import inspect

import pytest

from cdpwave.domains.base import BaseDomain
from cdpwave.domains.io import IODomain
from cdpwave.domains.pwa import PWADomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestIODomain:
    # --- close ---

    async def test_close(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain.close("handle1")
        assert fake.last_call == ("IO.close", {"handle": "handle1"})

    async def test_close_empty_string(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain.close("")
        assert fake.last_call == ("IO.close", {"handle": ""})

    async def test_close_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(42)  # type: ignore[arg-type]

    async def test_close_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(True)  # type: ignore[arg-type]

    async def test_close_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(["h1"])  # type: ignore[arg-type]

    async def test_close_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close({"id": "h1"})  # type: ignore[arg-type]

    async def test_close_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(None)  # type: ignore[arg-type]

    async def test_close_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(3.14)  # type: ignore[arg-type]

    # --- read ---

    async def test_read_basic(self) -> None:
        fake = FakeSender({"data": "abc", "eof": True, "base64Encoded": False})
        domain = IODomain(fake)
        result = await domain.read("handle1")
        method, params = fake.last_call
        assert method == "IO.read"
        assert params is not None
        assert params["handle"] == "handle1"
        assert "offset" not in params
        assert "size" not in params
        assert result["data"] == "abc"
        assert result["eof"] is True
        assert result["base64Encoded"] is False

    async def test_read_with_offset(self) -> None:
        fake = FakeSender({"data": "def", "eof": False})
        domain = IODomain(fake)
        await domain.read("handle1", offset=10)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 10

    async def test_read_with_size(self) -> None:
        fake = FakeSender({"data": "def", "eof": False})
        domain = IODomain(fake)
        await domain.read("handle1", size=1024)
        _, params = fake.last_call
        assert params is not None
        assert params["size"] == 1024

    async def test_read_with_offset_and_size(self) -> None:
        fake = FakeSender({"data": "def", "eof": False})
        domain = IODomain(fake)
        await domain.read("handle1", offset=10, size=1024)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 10
        assert params["size"] == 1024

    async def test_read_omit_offset_zero(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", offset=0)
        _, params = fake.last_call
        assert params is not None
        assert "offset" not in params

    async def test_read_omit_size_zero(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", size=0)
        _, params = fake.last_call
        assert params is not None
        assert "size" not in params

    async def test_read_omit_offset_and_size_zero(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", offset=0, size=0)
        _, params = fake.last_call
        assert params is not None
        assert "offset" not in params
        assert "size" not in params

    async def test_read_omit_offset_none(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", offset=None)
        _, params = fake.last_call
        assert params is not None
        assert "offset" not in params

    async def test_read_omit_size_none(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", size=None)
        _, params = fake.last_call
        assert params is not None
        assert "size" not in params

    async def test_read_negative_offset_sent(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", offset=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == -1

    async def test_read_negative_size_sent(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("handle1", size=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["size"] == -1

    async def test_read_empty_string_handle(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("")
        assert fake.last_call == ("IO.read", {"handle": ""})

    async def test_read_type_error_handle_int(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(42)  # type: ignore[arg-type]

    async def test_read_type_error_handle_bool(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(True)  # type: ignore[arg-type]

    async def test_read_type_error_handle_list(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(["h1"])  # type: ignore[arg-type]

    async def test_read_type_error_handle_dict(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read({"id": "h1"})  # type: ignore[arg-type]

    async def test_read_type_error_handle_none(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(None)  # type: ignore[arg-type]

    async def test_read_type_error_handle_float(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(3.14)  # type: ignore[arg-type]

    async def test_read_type_error_offset_str(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset="10")  # type: ignore[arg-type]

    async def test_read_type_error_offset_bool(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset=True)  # type: ignore[arg-type,unused-ignore]

    async def test_read_type_error_offset_float(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset=10.5)  # type: ignore[arg-type]

    async def test_read_type_error_offset_list(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset=[10])  # type: ignore[arg-type]

    async def test_read_type_error_size_str(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size="1024")  # type: ignore[arg-type]

    async def test_read_type_error_size_bool(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size=False)  # type: ignore[arg-type,unused-ignore]

    async def test_read_type_error_size_float(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size=1024.5)  # type: ignore[arg-type]

    async def test_read_type_error_size_dict(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size={"n": 1})  # type: ignore[arg-type]

    # --- resolve_blob ---

    async def test_resolve_blob(self) -> None:
        fake = FakeSender({"uuid": "blob-uuid-123"})
        domain = IODomain(fake)
        result = await domain.resolve_blob("obj1")
        assert fake.last_call == ("IO.resolveBlob", {"objectId": "obj1"})
        assert result["uuid"] == "blob-uuid-123"

    async def test_resolve_blob_empty_string(self) -> None:
        fake = FakeSender({"uuid": ""})
        domain = IODomain(fake)
        await domain.resolve_blob("")
        assert fake.last_call == ("IO.resolveBlob", {"objectId": ""})

    async def test_resolve_blob_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(42)  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(True)  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(["o1"])  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob({"id": "o1"})  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(None)  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(3.14)  # type: ignore[arg-type]

    # --- multi-call isolation ---

    async def test_multi_call_read_isolation(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=10, size=1024)
        await domain.read("h2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["handle"] == "h1"
        assert params1["offset"] == 10
        assert params1["size"] == 1024
        assert params2["handle"] == "h2"
        assert "offset" not in params2
        assert "size" not in params2

    # --- raw send ---

    async def test_raw_send_read(self) -> None:
        fake = FakeSender({"data": "abc", "eof": True})
        domain = IODomain(fake)
        await domain._call("IO.read", {"handle": "h1", "offset": 5})
        assert fake.last_call == ("IO.read", {"handle": "h1", "offset": 5})

    async def test_raw_send_close(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain._call("IO.close", {"handle": "h1"})
        assert fake.last_call == ("IO.close", {"handle": "h1"})

    async def test_raw_send_resolve_blob(self) -> None:
        fake = FakeSender({"uuid": "u1"})
        domain = IODomain(fake)
        await domain._call("IO.resolveBlob", {"objectId": "o1"})
        assert fake.last_call == ("IO.resolveBlob", {"objectId": "o1"})


@pytest.mark.unit
class TestIOMeta:
    def test_is_base_domain(self) -> None:
        assert issubclass(IODomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(IODomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        ]
        assert len(methods) == 3

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(IODomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_expected_methods(self) -> None:
        expected = {"close", "read", "resolve_blob"}
        actual = {
            name
            for name, obj in inspect.getmembers(IODomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        }
        assert actual == expected

    def test_module_docstring_exists(self) -> None:
        import cdpwave.domains.io as mod

        assert mod.__doc__ is not None

    def test_module_docstring_has_stream_handle(self) -> None:
        import cdpwave.domains.io as mod

        assert mod.__doc__ is not None
        assert "StreamHandle" in mod.__doc__

    def test_module_docstring_has_events_none(self) -> None:
        import cdpwave.domains.io as mod

        assert mod.__doc__ is not None
        assert "Events" in mod.__doc__

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(IODomain, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"

    def test_all_methods_have_raises(self) -> None:
        for name, obj in inspect.getmembers(IODomain, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None
            assert "Raises:" in obj.__doc__, f"{name} missing Raises section"

    def test_omitempty_documented_in_read(self) -> None:
        method = IODomain.read
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__


@pytest.mark.unit
class TestPWADomain:
    # --- change_app_user_settings ---

    async def test_change_app_user_settings_default(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1")
        method, params = fake.last_call
        assert method == "PWA.changeAppUserSettings"
        assert params is not None
        assert params["manifestId"] == "manifest1"
        assert params["linkCapturing"] is False
        assert "displayMode" not in params

    async def test_change_app_user_settings_link_capturing_true(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", link_capturing=True)
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is True

    async def test_change_app_user_settings_link_capturing_false(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", link_capturing=False)
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is False

    async def test_change_app_user_settings_with_display_mode(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", display_mode="standalone")
        _, params = fake.last_call
        assert params is not None
        assert params["displayMode"] == "standalone"
        assert params["linkCapturing"] is False

    async def test_change_app_user_settings_all_params(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings(
            "manifest1", link_capturing=True, display_mode="browser"
        )
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "manifest1"
        assert params["linkCapturing"] is True
        assert params["displayMode"] == "browser"

    async def test_change_app_user_settings_omit_display_mode_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", display_mode="")
        _, params = fake.last_call
        assert params is not None
        assert "displayMode" not in params

    async def test_change_app_user_settings_omit_display_mode_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1", display_mode=None)
        _, params = fake.last_call
        assert params is not None
        assert "displayMode" not in params

    async def test_change_app_user_settings_link_capturing_always_sent(self) -> None:
        """link_capturing has no omitempty in Go — always sent, even False."""
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("manifest1")
        _, params = fake.last_call
        assert params is not None
        assert "linkCapturing" in params
        assert params["linkCapturing"] is False

    async def test_change_app_user_settings_type_error_manifest_id_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.change_app_user_settings(42)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_manifest_id_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.change_app_user_settings(True)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_manifest_id_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.change_app_user_settings(["m1"])  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_link_capturing_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="link_capturing must be a bool"):
            await domain.change_app_user_settings("m1", link_capturing=1)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_link_capturing_str(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="link_capturing must be a bool"):
            await domain.change_app_user_settings("m1", link_capturing="yes")  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_link_capturing_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="link_capturing must be a bool"):
            await domain.change_app_user_settings("m1", link_capturing=None)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode=42)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode=True)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode=["s"])  # type: ignore[arg-type]

    # --- get_os_app_state ---

    async def test_get_os_app_state(self) -> None:
        fake = FakeSender({"badgeCount": 3, "fileHandlers": []})
        domain = PWADomain(fake)
        result = await domain.get_os_app_state("manifest1")
        assert fake.last_call == (
            "PWA.getOsAppState",
            {"manifestId": "manifest1"},
        )
        assert result["badgeCount"] == 3

    async def test_get_os_app_state_empty_string(self) -> None:
        fake = FakeSender({"badgeCount": 0, "fileHandlers": []})
        domain = PWADomain(fake)
        await domain.get_os_app_state("")
        assert fake.last_call == (
            "PWA.getOsAppState",
            {"manifestId": ""},
        )

    async def test_get_os_app_state_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(42)  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(True)  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(["m1"])  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(None)  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(3.14)  # type: ignore[arg-type]

    # --- install ---

    async def test_install_basic(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest1")
        assert fake.last_call == (
            "PWA.install",
            {"manifestId": "manifest1"},
        )

    async def test_install_with_url(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest1", "https://example.com/app")
        method, params = fake.last_call
        assert method == "PWA.install"
        assert params is not None
        assert params["installUrlOrBundleUrl"] == "https://example.com/app"

    async def test_install_omit_url_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest1", "")
        _, params = fake.last_call
        assert params is not None
        assert "installUrlOrBundleUrl" not in params

    async def test_install_omit_url_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("manifest1", None)
        _, params = fake.last_call
        assert params is not None
        assert "installUrlOrBundleUrl" not in params

    async def test_install_empty_string_manifest_id(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("")
        assert fake.last_call == ("PWA.install", {"manifestId": ""})

    async def test_install_type_error_manifest_id_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install(42)  # type: ignore[arg-type]

    async def test_install_type_error_manifest_id_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install(True)  # type: ignore[arg-type]

    async def test_install_type_error_manifest_id_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install(["m1"])  # type: ignore[arg-type]

    async def test_install_type_error_url_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", 42)  # type: ignore[arg-type]

    async def test_install_type_error_url_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", True)  # type: ignore[arg-type]

    async def test_install_type_error_url_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", ["u1"])  # type: ignore[arg-type]

    # --- launch ---

    async def test_launch_basic(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        result = await domain.launch("manifest1")
        method, params = fake.last_call
        assert method == "PWA.launch"
        assert params is not None
        assert params["manifestId"] == "manifest1"
        assert "url" not in params
        assert result["targetId"] == "T1"

    async def test_launch_with_url(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("manifest1", "https://example.com")
        _, params = fake.last_call
        assert params is not None
        assert params["url"] == "https://example.com"

    async def test_launch_omit_url_empty(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("manifest1", "")
        _, params = fake.last_call
        assert params is not None
        assert "url" not in params

    async def test_launch_omit_url_none(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("manifest1", None)
        _, params = fake.last_call
        assert params is not None
        assert "url" not in params

    async def test_launch_empty_string_manifest_id(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("")
        assert fake.last_call == ("PWA.launch", {"manifestId": ""})

    async def test_launch_type_error_manifest_id_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch(42)  # type: ignore[arg-type]

    async def test_launch_type_error_manifest_id_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch(True)  # type: ignore[arg-type]

    async def test_launch_type_error_manifest_id_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch(["m1"])  # type: ignore[arg-type]

    async def test_launch_type_error_url_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", 42)  # type: ignore[arg-type]

    async def test_launch_type_error_url_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", True)  # type: ignore[arg-type]

    async def test_launch_type_error_url_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", {"u": 1})  # type: ignore[arg-type]

    # --- launch_files_in_app ---

    async def test_launch_files_in_app(self) -> None:
        fake = FakeSender({"targetIds": ["T1"]})
        domain = PWADomain(fake)
        result = await domain.launch_files_in_app("manifest1", ["/file1.txt"])
        method, params = fake.last_call
        assert method == "PWA.launchFilesInApp"
        assert params is not None
        assert params["manifestId"] == "manifest1"
        assert params["files"] == ["/file1.txt"]
        assert result["targetIds"] == ["T1"]

    async def test_launch_files_in_app_multiple_files(self) -> None:
        fake = FakeSender({"targetIds": ["T1", "T2"]})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("manifest1", ["/f1.txt", "/f2.txt", "/f3.txt"])
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == ["/f1.txt", "/f2.txt", "/f3.txt"]

    async def test_launch_files_in_app_empty_list(self) -> None:
        fake = FakeSender({"targetIds": []})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("manifest1", [])
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == []

    async def test_launch_files_in_app_type_error_manifest_id_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch_files_in_app(42, ["f"])  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_str(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", "not a list")  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", 42)  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", True)  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", {"f": 1})  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_element_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [42])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [True])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [{"f": 1}])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_int_at_index_1(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[1\] must be a str"):
            await domain.launch_files_in_app("m1", ["ok", 42])  # type: ignore[list-item]

    # --- open_current_page_in_app ---

    async def test_open_current_page_in_app(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.open_current_page_in_app("manifest1")
        assert fake.last_call == (
            "PWA.openCurrentPageInApp",
            {"manifestId": "manifest1"},
        )

    async def test_open_current_page_in_app_empty_string(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.open_current_page_in_app("")
        assert fake.last_call == (
            "PWA.openCurrentPageInApp",
            {"manifestId": ""},
        )

    async def test_open_current_page_in_app_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(42)  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(True)  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(["m1"])  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(None)  # type: ignore[arg-type]

    # --- uninstall ---

    async def test_uninstall(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.uninstall("manifest1")
        assert fake.last_call == (
            "PWA.uninstall",
            {"manifestId": "manifest1"},
        )

    async def test_uninstall_empty_string(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.uninstall("")
        assert fake.last_call == (
            "PWA.uninstall",
            {"manifestId": ""},
        )

    async def test_uninstall_type_error_int(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(42)  # type: ignore[arg-type]

    async def test_uninstall_type_error_bool(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(True)  # type: ignore[arg-type]

    async def test_uninstall_type_error_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(["m1"])  # type: ignore[arg-type]

    async def test_uninstall_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall({"id": "m1"})  # type: ignore[arg-type]

    async def test_uninstall_type_error_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(None)  # type: ignore[arg-type]

    # --- multi-call isolation ---

    async def test_multi_call_install_isolation(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("m1", "https://example.com")
        await domain.install("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["manifestId"] == "m1"
        assert params1["installUrlOrBundleUrl"] == "https://example.com"
        assert params2["manifestId"] == "m2"
        assert "installUrlOrBundleUrl" not in params2

    async def test_multi_call_change_app_user_settings_isolation(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("m1", link_capturing=True, display_mode="standalone")
        await domain.change_app_user_settings("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["manifestId"] == "m1"
        assert params1["linkCapturing"] is True
        assert params1["displayMode"] == "standalone"
        assert params2["manifestId"] == "m2"
        assert params2["linkCapturing"] is False
        assert "displayMode" not in params2

    # --- raw send ---

    async def test_raw_send_install(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain._call("PWA.install", {"manifestId": "m1"})
        assert fake.last_call == ("PWA.install", {"manifestId": "m1"})

    async def test_raw_send_launch(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain._call("PWA.launch", {"manifestId": "m1", "url": "https://x.com"})
        assert fake.last_call == ("PWA.launch", {"manifestId": "m1", "url": "https://x.com"})

    async def test_raw_send_change_app_user_settings(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain._call(
            "PWA.changeAppUserSettings",
            {"manifestId": "m1", "linkCapturing": True, "displayMode": "standalone"},
        )
        assert fake.last_call == (
            "PWA.changeAppUserSettings",
            {"manifestId": "m1", "linkCapturing": True, "displayMode": "standalone"},
        )


@pytest.mark.unit
class TestPWAMeta:
    def test_is_base_domain(self) -> None:
        assert issubclass(PWADomain, BaseDomain)

    def test_method_count(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(PWADomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        ]
        assert len(methods) == 7

    def test_methods_alphabetical(self) -> None:
        methods = [
            name
            for name, obj in inspect.getmembers(PWADomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        ]
        assert methods == sorted(methods)

    def test_expected_methods(self) -> None:
        expected = {
            "change_app_user_settings",
            "get_os_app_state",
            "install",
            "launch",
            "launch_files_in_app",
            "open_current_page_in_app",
            "uninstall",
        }
        actual = {
            name
            for name, obj in inspect.getmembers(PWADomain, predicate=inspect.isfunction)
            if not name.startswith("_")
        }
        assert actual == expected

    def test_module_docstring_exists(self) -> None:
        import cdpwave.domains.pwa as mod

        assert mod.__doc__ is not None

    def test_module_docstring_has_display_mode(self) -> None:
        import cdpwave.domains.pwa as mod

        assert mod.__doc__ is not None
        assert "DisplayMode" in mod.__doc__

    def test_module_docstring_has_file_handler(self) -> None:
        import cdpwave.domains.pwa as mod

        assert mod.__doc__ is not None
        assert "FileHandler" in mod.__doc__

    def test_module_docstring_has_file_handler_accept(self) -> None:
        import cdpwave.domains.pwa as mod

        assert mod.__doc__ is not None
        assert "FileHandlerAccept" in mod.__doc__

    def test_module_docstring_has_events_none(self) -> None:
        import cdpwave.domains.pwa as mod

        assert mod.__doc__ is not None
        assert "Events" in mod.__doc__

    def test_all_methods_have_docstrings(self) -> None:
        for name, obj in inspect.getmembers(PWADomain, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None, f"{name} missing docstring"

    def test_all_methods_have_raises(self) -> None:
        for name, obj in inspect.getmembers(PWADomain, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            assert obj.__doc__ is not None
            assert "Raises:" in obj.__doc__, f"{name} missing Raises section"

    def test_omitempty_documented_in_install(self) -> None:
        method = PWADomain.install
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__

    def test_omitempty_documented_in_launch(self) -> None:
        method = PWADomain.launch
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__

    def test_omitempty_documented_in_change_app_user_settings(self) -> None:
        method = PWADomain.change_app_user_settings
        assert method.__doc__ is not None
        assert "omitempty" in method.__doc__

    def test_get_os_app_state_docstring_has_badge_count(self) -> None:
        method = PWADomain.get_os_app_state
        assert method.__doc__ is not None
        assert "badgeCount" in method.__doc__

    def test_get_os_app_state_docstring_has_file_handlers(self) -> None:
        method = PWADomain.get_os_app_state
        assert method.__doc__ is not None
        assert "fileHandlers" in method.__doc__

    def test_get_os_app_state_docstring_no_wrong_fields(self) -> None:
        method = PWADomain.get_os_app_state
        assert method.__doc__ is not None
        assert "badgeIconIndex" not in method.__doc__
        assert "appInstalledState" not in method.__doc__
        assert "isAppInstalled" not in method.__doc__


# ---------------------------------------------------------------------------
# Edge case tests — large values, exotic types, combo omitempty, etc.
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestIOEdgeCases:
    # --- large / boundary values ---

    async def test_read_large_offset(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=2**31)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 2**31

    async def test_read_large_size(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", size=2**31)
        _, params = fake.last_call
        assert params is not None
        assert params["size"] == 2**31

    async def test_read_max_int64(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=2**63 - 1, size=2**63 - 1)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 2**63 - 1
        assert params["size"] == 2**63 - 1

    async def test_read_negative_offset_and_size(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=-100, size=-200)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == -100
        assert params["size"] == -200

    # --- combo omitempty ---

    async def test_read_offset_zero_size_nonzero(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=0, size=512)
        _, params = fake.last_call
        assert params is not None
        assert "offset" not in params
        assert params["size"] == 512

    async def test_read_offset_nonzero_size_zero(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=10, size=0)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 10
        assert "size" not in params

    # --- exotic types ---

    async def test_read_type_error_handle_bytes(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(b"h1")  # type: ignore[arg-type]

    async def test_read_type_error_handle_set(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read({"h1"})  # type: ignore[arg-type]

    async def test_read_type_error_handle_tuple(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.read(("h1",))  # type: ignore[arg-type]

    async def test_read_type_error_offset_bytes(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset=b"10")  # type: ignore[arg-type]

    async def test_read_type_error_offset_dict(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset={"v": 1})  # type: ignore[arg-type]

    async def test_read_type_error_offset_set(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="offset must be an int"):
            await domain.read("h1", offset={1})  # type: ignore[arg-type]

    async def test_read_type_error_size_bytes(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size=b"10")  # type: ignore[arg-type]

    async def test_read_type_error_size_tuple(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size=(10,))  # type: ignore[arg-type]

    async def test_read_type_error_size_set(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="size must be an int"):
            await domain.read("h1", size={10})  # type: ignore[arg-type]

    async def test_close_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(b"h1")  # type: ignore[arg-type]

    async def test_close_type_error_set(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close({"h1"})  # type: ignore[arg-type]

    async def test_close_type_error_tuple(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="handle must be a str"):
            await domain.close(("h1",))  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(b"obj1")  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_set(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob({"obj1"})  # type: ignore[arg-type]

    async def test_resolve_blob_type_error_tuple(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        with pytest.raises(TypeError, match="object_id must be a str"):
            await domain.resolve_blob(("obj1",))  # type: ignore[arg-type]

    # --- return value structure ---

    async def test_read_return_all_fields(self) -> None:
        fake = FakeSender(
            {
                "base64Encoded": True,
                "data": "SGVsbG8=",
                "eof": False,
            }
        )
        domain = IODomain(fake)
        result = await domain.read("h1")
        assert result["base64Encoded"] is True
        assert result["data"] == "SGVsbG8="
        assert result["eof"] is False

    async def test_read_return_minimal(self) -> None:
        fake = FakeSender({"eof": True})
        domain = IODomain(fake)
        result = await domain.read("h1")
        assert result["eof"] is True

    async def test_close_return_empty(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        result = await domain.close("h1")
        assert result == {}

    async def test_resolve_blob_return(self) -> None:
        fake = FakeSender({"uuid": "abc-123-def"})
        domain = IODomain(fake)
        result = await domain.resolve_blob("obj1")
        assert result["uuid"] == "abc-123-def"

    # --- multi-call isolation for all methods ---

    async def test_multi_call_close_isolation(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain.close("h1")
        await domain.close("h2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 == {"handle": "h1"}
        assert params2 == {"handle": "h2"}

    async def test_multi_call_resolve_blob_isolation(self) -> None:
        fake = FakeSender({"uuid": "u1"})
        domain = IODomain(fake)
        await domain.resolve_blob("o1")
        await domain.resolve_blob("o2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 == {"objectId": "o1"}
        assert params2 == {"objectId": "o2"}

    async def test_multi_call_mixed_methods(self) -> None:
        fake = FakeSender({"data": "x", "eof": True, "uuid": "u"})
        domain = IODomain(fake)
        await domain.read("h1", offset=10, size=20)
        await domain.close("h2")
        await domain.resolve_blob("o3")
        assert fake.calls[0] == ("IO.read", {"handle": "h1", "offset": 10, "size": 20})
        assert fake.calls[1] == ("IO.close", {"handle": "h2"})
        assert fake.calls[2] == ("IO.resolveBlob", {"objectId": "o3"})

    # --- raw send combos ---

    async def test_raw_send_read_with_all_params(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain._call(
            "IO.read",
            {"handle": "h1", "offset": 100, "size": 200},
        )
        assert fake.last_call == (
            "IO.read",
            {"handle": "h1", "offset": 100, "size": 200},
        )

    async def test_raw_send_read_no_params(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain._call("IO.read", None)
        assert fake.last_call == ("IO.read", None)

    async def test_raw_send_close_no_params(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain._call("IO.close", None)
        assert fake.last_call == ("IO.close", None)


@pytest.mark.unit
class TestPWAEdgeCases:
    # --- large / boundary values ---

    async def test_install_long_url(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        long_url = "https://example.com/" + "a" * 10000
        await domain.install("m1", long_url)
        _, params = fake.last_call
        assert params is not None
        assert params["installUrlOrBundleUrl"] == long_url

    async def test_launch_long_url(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        long_url = "https://example.com/" + "b" * 10000
        await domain.launch("m1", long_url)
        _, params = fake.last_call
        assert params is not None
        assert params["url"] == long_url

    async def test_launch_files_in_app_many_files(self) -> None:
        fake = FakeSender({"targetIds": []})
        domain = PWADomain(fake)
        files = [f"/file{i}.txt" for i in range(100)]
        await domain.launch_files_in_app("m1", files)
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == files
        assert len(params["files"]) == 100

    async def test_install_long_manifest_id(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        long_id = "m" * 5000
        await domain.install(long_id)
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == long_id

    # --- empty strings in files list ---

    async def test_launch_files_in_app_with_empty_string_element(self) -> None:
        fake = FakeSender({"targetIds": []})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("m1", ["", "/real.txt", ""])
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == ["", "/real.txt", ""]

    async def test_launch_files_in_app_all_empty_strings(self) -> None:
        fake = FakeSender({"targetIds": []})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("m1", ["", "", ""])
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == ["", "", ""]

    # --- combo omitempty ---

    async def test_change_app_user_settings_link_true_display_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("m1", link_capturing=True, display_mode="")
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is True
        assert "displayMode" not in params

    async def test_change_app_user_settings_link_false_display_standalone(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("m1", link_capturing=False, display_mode="standalone")
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is False
        assert params["displayMode"] == "standalone"

    async def test_install_omit_url_zero(self) -> None:
        """install_url_or_bundle_url=0 should raise TypeError, not be silently omitted."""
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", 0)  # type: ignore[arg-type]

    # --- exotic types ---

    async def test_install_type_error_manifest_id_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install(b"m1")  # type: ignore[arg-type]

    async def test_install_type_error_manifest_id_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install({"m1"})  # type: ignore[arg-type]

    async def test_install_type_error_manifest_id_tuple(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.install(("m1",))  # type: ignore[arg-type]

    async def test_install_type_error_url_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", b"https://x.com")  # type: ignore[arg-type]

    async def test_install_type_error_url_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", {"u": 1})  # type: ignore[arg-type]

    async def test_install_type_error_url_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="install_url_or_bundle_url must be a str"):
            await domain.install("m1", {"u"})  # type: ignore[arg-type]

    async def test_launch_type_error_manifest_id_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch(b"m1")  # type: ignore[arg-type]

    async def test_launch_type_error_manifest_id_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.launch({"m1"})  # type: ignore[arg-type]

    async def test_launch_type_error_url_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", b"https://x.com")  # type: ignore[arg-type]

    async def test_launch_type_error_url_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", {"u"})  # type: ignore[arg-type]

    async def test_launch_type_error_url_tuple(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="url must be a str"):
            await domain.launch("m1", ("u",))  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_tuple(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", ("/f1",))  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", {"/f1"})  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_files_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="files must be a list"):
            await domain.launch_files_in_app("m1", None)  # type: ignore[arg-type]

    async def test_launch_files_in_app_type_error_element_none(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [None])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_float(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [3.14])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [["nested"]])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [b"f1"])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[0\] must be a str"):
            await domain.launch_files_in_app("m1", [{"f"}])  # type: ignore[list-item]

    async def test_launch_files_in_app_type_error_element_at_index_2(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match=r"files\[2\] must be a str"):
            await domain.launch_files_in_app("m1", ["ok", "ok2", 42])  # type: ignore[list-item]

    async def test_change_app_user_settings_type_error_manifest_id_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.change_app_user_settings(b"m1")  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_manifest_id_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.change_app_user_settings({"m1"})  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_link_capturing_float(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="link_capturing must be a bool"):
            await domain.change_app_user_settings("m1", link_capturing=1.0)  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_link_capturing_list(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="link_capturing must be a bool"):
            await domain.change_app_user_settings("m1", link_capturing=[True])  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode=b"standalone")  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode={"s"})  # type: ignore[arg-type]

    async def test_change_app_user_settings_type_error_display_mode_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="display_mode must be a str"):
            await domain.change_app_user_settings("m1", display_mode={"m": "s"})  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(b"m1")  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state({"m1"})  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_tuple(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state(("m1",))  # type: ignore[arg-type]

    async def test_get_os_app_state_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.get_os_app_state({"id": "m1"})  # type: ignore[arg-type]

    async def test_uninstall_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(b"m1")  # type: ignore[arg-type]

    async def test_uninstall_type_error_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall({"m1"})  # type: ignore[arg-type]

    async def test_uninstall_type_error_tuple(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(("m1",))  # type: ignore[arg-type]

    async def test_uninstall_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.uninstall(3.14)  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_bytes(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(b"m1")  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_set(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app({"m1"})  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_float(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app(3.14)  # type: ignore[arg-type]

    async def test_open_current_page_in_app_type_error_dict(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        with pytest.raises(TypeError, match="manifest_id must be a str"):
            await domain.open_current_page_in_app({"id": "m1"})  # type: ignore[arg-type]

    # --- return value structure ---

    async def test_get_os_app_state_return(self) -> None:
        fake = FakeSender(
            {
                "badgeCount": 5,
                "fileHandlers": [
                    {"action": "/open", "accepts": [], "displayName": "Open"},
                ],
            }
        )
        domain = PWADomain(fake)
        result = await domain.get_os_app_state("m1")
        assert result["badgeCount"] == 5
        assert len(result["fileHandlers"]) == 1
        assert result["fileHandlers"][0]["action"] == "/open"

    async def test_get_os_app_state_return_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.get_os_app_state("m1")
        assert result == {}

    async def test_install_return_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.install("m1")
        assert result == {}

    async def test_uninstall_return_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.uninstall("m1")
        assert result == {}

    async def test_open_current_page_in_app_return_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.open_current_page_in_app("m1")
        assert result == {}

    async def test_change_app_user_settings_return_empty(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.change_app_user_settings("m1")
        assert result == {}

    async def test_launch_return(self) -> None:
        fake = FakeSender({"targetId": "TARGET-ABC-123"})
        domain = PWADomain(fake)
        result = await domain.launch("m1")
        assert result["targetId"] == "TARGET-ABC-123"

    async def test_launch_files_in_app_return(self) -> None:
        fake = FakeSender({"targetIds": ["T1", "T2", "T3"]})
        domain = PWADomain(fake)
        result = await domain.launch_files_in_app("m1", ["/f1", "/f2"])
        assert result["targetIds"] == ["T1", "T2", "T3"]

    # --- multi-call isolation for all PWA methods ---

    async def test_multi_call_launch_isolation(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("m1", url="https://a.com")
        await domain.launch("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["manifestId"] == "m1"
        assert params1["url"] == "https://a.com"
        assert params2["manifestId"] == "m2"
        assert "url" not in params2

    async def test_multi_call_uninstall_isolation(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.uninstall("m1")
        await domain.uninstall("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 == {"manifestId": "m1"}
        assert params2 == {"manifestId": "m2"}

    async def test_multi_call_get_os_app_state_isolation(self) -> None:
        fake = FakeSender({"badgeCount": 0})
        domain = PWADomain(fake)
        await domain.get_os_app_state("m1")
        await domain.get_os_app_state("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 == {"manifestId": "m1"}
        assert params2 == {"manifestId": "m2"}

    async def test_multi_call_open_current_page_in_app_isolation(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.open_current_page_in_app("m1")
        await domain.open_current_page_in_app("m2")
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 == {"manifestId": "m1"}
        assert params2 == {"manifestId": "m2"}

    async def test_multi_call_launch_files_in_app_isolation(self) -> None:
        fake = FakeSender({"targetIds": []})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("m1", ["/f1", "/f2"])
        await domain.launch_files_in_app("m2", ["/f3"])
        _, params1 = fake.calls[-2]
        _, params2 = fake.calls[-1]
        assert params1 is not None
        assert params2 is not None
        assert params1["manifestId"] == "m1"
        assert params1["files"] == ["/f1", "/f2"]
        assert params2["manifestId"] == "m2"
        assert params2["files"] == ["/f3"]

    async def test_multi_call_mixed_methods(self) -> None:
        fake = FakeSender({"targetId": "T", "targetIds": [], "badgeCount": 0})
        domain = PWADomain(fake)
        await domain.install("m1", "https://x.com")
        await domain.uninstall("m2")
        await domain.launch("m3", url="https://y.com")
        await domain.get_os_app_state("m4")
        await domain.change_app_user_settings("m5", link_capturing=True, display_mode="browser")
        assert fake.calls[0] == (
            "PWA.install",
            {"manifestId": "m1", "installUrlOrBundleUrl": "https://x.com"},
        )
        assert fake.calls[1] == ("PWA.uninstall", {"manifestId": "m2"})
        assert fake.calls[2] == ("PWA.launch", {"manifestId": "m3", "url": "https://y.com"})
        assert fake.calls[3] == ("PWA.getOsAppState", {"manifestId": "m4"})
        assert fake.calls[4] == (
            "PWA.changeAppUserSettings",
            {"manifestId": "m5", "linkCapturing": True, "displayMode": "browser"},
        )

    # --- raw send combos ---

    async def test_raw_send_uninstall(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain._call("PWA.uninstall", {"manifestId": "m1"})
        assert fake.last_call == ("PWA.uninstall", {"manifestId": "m1"})

    async def test_raw_send_get_os_app_state(self) -> None:
        fake = FakeSender({"badgeCount": 0})
        domain = PWADomain(fake)
        await domain._call("PWA.getOsAppState", {"manifestId": "m1"})
        assert fake.last_call == ("PWA.getOsAppState", {"manifestId": "m1"})

    async def test_raw_send_launch_files_in_app(self) -> None:
        fake = FakeSender({"targetIds": ["T1"]})
        domain = PWADomain(fake)
        await domain._call(
            "PWA.launchFilesInApp",
            {"manifestId": "m1", "files": ["/f1", "/f2"]},
        )
        assert fake.last_call == (
            "PWA.launchFilesInApp",
            {"manifestId": "m1", "files": ["/f1", "/f2"]},
        )

    async def test_raw_send_open_current_page_in_app(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain._call("PWA.openCurrentPageInApp", {"manifestId": "m1"})
        assert fake.last_call == ("PWA.openCurrentPageInApp", {"manifestId": "m1"})

    async def test_raw_send_install_no_params(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain._call("PWA.install", None)
        assert fake.last_call == ("PWA.install", None)

    async def test_raw_send_launch_no_params(self) -> None:
        fake = FakeSender({"targetId": "T"})
        domain = PWADomain(fake)
        await domain._call("PWA.launch", None)
        assert fake.last_call == ("PWA.launch", None)

    # --- special manifest IDs ---

    async def test_install_manifest_id_with_special_chars(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install("https://example.com/manifest.json?id=123&v=2")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "https://example.com/manifest.json?id=123&v=2"

    async def test_launch_manifest_id_with_unicode(self) -> None:
        fake = FakeSender({"targetId": "T"})
        domain = PWADomain(fake)
        await domain.launch("isolated-app://éxämple-123")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "isolated-app://éxämple-123"

    async def test_change_app_user_settings_display_mode_browser(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("m1", display_mode="browser")
        _, params = fake.last_call
        assert params is not None
        assert params["displayMode"] == "browser"
        assert params["linkCapturing"] is False

    # --- combo: link_capturing=True + display_mode="browser" ---

    async def test_change_app_user_settings_link_true_display_browser(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings(
            "m1", link_capturing=True, display_mode="browser"
        )
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is True
        assert params["displayMode"] == "browser"

    async def test_change_app_user_settings_link_true_display_standalone(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings(
            "m1", link_capturing=True, display_mode="standalone"
        )
        _, params = fake.last_call
        assert params is not None
        assert params["linkCapturing"] is True
        assert params["displayMode"] == "standalone"

    # --- return value edge cases (omitzero in Go source) ---

    async def test_resolve_blob_return_empty_uuid(self) -> None:
        """Go source: uuid has omitempty,omitzero — empty string may be omitted."""
        fake = FakeSender({})
        domain = IODomain(fake)
        result = await domain.resolve_blob("obj1")
        assert result == {}

    async def test_launch_return_empty_target_id(self) -> None:
        """Go source: targetId has omitempty,omitzero — empty string may be omitted."""
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.launch("m1")
        assert result == {}

    async def test_launch_files_in_app_return_empty_target_ids(self) -> None:
        """Go source: targetIds has omitempty,omitzero — empty list may be omitted."""
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.launch_files_in_app("m1", ["/f1"])
        assert result == {}

    async def test_get_os_app_state_return_badge_zero(self) -> None:
        """Go source: badgeCount has omitempty,omitzero — 0 may be omitted."""
        fake = FakeSender({"fileHandlers": []})
        domain = PWADomain(fake)
        result = await domain.get_os_app_state("m1")
        assert "badgeCount" not in result
        assert result["fileHandlers"] == []

    async def test_get_os_app_state_return_no_fields(self) -> None:
        """Both badgeCount and fileHandlers have omitzero — both may be omitted."""
        fake = FakeSender({})
        domain = PWADomain(fake)
        result = await domain.get_os_app_state("m1")
        assert result == {}

    async def test_read_return_data_omitted(self) -> None:
        """Go source: data has omitempty,omitzero — empty string may be omitted."""
        fake = FakeSender({"base64Encoded": False, "eof": True})
        domain = IODomain(fake)
        result = await domain.read("h1")
        assert "data" not in result
        assert result["base64Encoded"] is False
        assert result["eof"] is True

    # --- blob: prefix handle (documented in module docstring) ---

    async def test_read_with_blob_handle(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("blob:550e8400-e29b-41d4-a716-446655440000")
        _, params = fake.last_call
        assert params is not None
        assert params["handle"] == "blob:550e8400-e29b-41d4-a716-446655440000"

    async def test_close_with_blob_handle(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        await domain.close("blob:550e8400-e29b-41d4-a716-446655440000")
        assert fake.last_call == (
            "IO.close",
            {"handle": "blob:550e8400-e29b-41d4-a716-446655440000"},
        )

    # --- smallest non-zero values ---

    async def test_read_offset_one(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=1)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == 1

    async def test_read_size_one(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", size=1)
        _, params = fake.last_call
        assert params is not None
        assert params["size"] == 1

    # --- long handle strings ---

    async def test_read_long_handle(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        long_handle = "h" * 10000
        await domain.read(long_handle)
        _, params = fake.last_call
        assert params is not None
        assert params["handle"] == long_handle

    async def test_close_long_handle(self) -> None:
        fake = FakeSender({})
        domain = IODomain(fake)
        long_handle = "h" * 10000
        await domain.close(long_handle)
        assert fake.last_call == ("IO.close", {"handle": long_handle})

    async def test_resolve_blob_long_object_id(self) -> None:
        fake = FakeSender({"uuid": "u"})
        domain = IODomain(fake)
        long_id = "o" * 10000
        await domain.resolve_blob(long_id)
        assert fake.last_call == ("IO.resolveBlob", {"objectId": long_id})

    # --- handle with special chars ---

    async def test_read_handle_with_newlines(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        handle = "handle\nwith\nnewlines"
        await domain.read(handle)
        _, params = fake.last_call
        assert params is not None
        assert params["handle"] == "handle\nwith\nnewlines"

    async def test_read_handle_with_unicode(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        handle = "händle-é-日本語"
        await domain.read(handle)
        _, params = fake.last_call
        assert params is not None
        assert params["handle"] == "händle-é-日本語"

    # --- IWA-style URLs ---

    async def test_install_with_isolated_app_url(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.install(
            "isolated-app://abc123",
            install_url_or_bundle_url="file:///path/to/app.swbn",
        )
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "isolated-app://abc123"
        assert params["installUrlOrBundleUrl"] == "file:///path/to/app.swbn"

    async def test_launch_with_isolated_app_manifest(self) -> None:
        fake = FakeSender({"targetId": "T1"})
        domain = PWADomain(fake)
        await domain.launch("isolated-app://def456")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "isolated-app://def456"
        assert "url" not in params

    # --- unicode in manifest IDs for all PWA methods ---

    async def test_uninstall_manifest_id_with_unicode(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.uninstall("https://éxämple.com/manifest.json")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "https://éxämple.com/manifest.json"

    async def test_get_os_app_state_manifest_id_with_unicode(self) -> None:
        fake = FakeSender({"badgeCount": 0})
        domain = PWADomain(fake)
        await domain.get_os_app_state("https://éxämple.com/manifest.json")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "https://éxämple.com/manifest.json"

    async def test_open_current_page_in_app_manifest_id_with_unicode(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.open_current_page_in_app("https://éxämple.com/manifest.json")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "https://éxämple.com/manifest.json"

    async def test_change_app_user_settings_manifest_id_with_unicode(self) -> None:
        fake = FakeSender({})
        domain = PWADomain(fake)
        await domain.change_app_user_settings("https://éxämple.com/manifest.json")
        _, params = fake.last_call
        assert params is not None
        assert params["manifestId"] == "https://éxämple.com/manifest.json"

    # --- launch_files_in_app with single file ---

    async def test_launch_files_in_app_single_file(self) -> None:
        fake = FakeSender({"targetIds": ["T1"]})
        domain = PWADomain(fake)
        await domain.launch_files_in_app("m1", ["/only.txt"])
        _, params = fake.last_call
        assert params is not None
        assert params["files"] == ["/only.txt"]

    # --- read with both offset and size as negative ---

    async def test_read_both_negative_offset_and_size(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=-999, size=-1)
        _, params = fake.last_call
        assert params is not None
        assert params["offset"] == -999
        assert params["size"] == -1

    # --- read with offset=0 and size=0 explicitly (both omitted) ---

    async def test_read_both_zero_omitted(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=0, size=0)
        _, params = fake.last_call
        assert params is not None
        assert "offset" not in params
        assert "size" not in params
        assert params["handle"] == "h1"

    # --- params dict not mutated between calls ---

    async def test_read_params_not_mutated(self) -> None:
        fake = FakeSender({"data": "", "eof": True})
        domain = IODomain(fake)
        await domain.read("h1", offset=10, size=20)
        _, params1 = fake.last_call
        await domain.read("h2")
        _, params2 = fake.last_call
        assert params1 is not None
        assert params2 is not None
        assert "offset" in params1
        assert "offset" not in params2
        assert "size" in params1
        assert "size" not in params2
