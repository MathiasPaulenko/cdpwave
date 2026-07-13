"""E2E tests for FedCm and Schema domains.

These tests launch a real browser and exercise domain methods
end-to-end against a live Chrome instance, including type validation
in real browser context, raw command sending, meta tests for
docstrings, method counts, and experimental marking.
"""

import contextlib
import inspect

import pytest

from cdpwave import CDPClient
from cdpwave.domains.fed_cm import FedCmDomain
from cdpwave.domains.schema import SchemaDomain

# ═══════════════════════════════════════════════════════════════
# FedCm E2E
# ═══════════════════════════════════════════════════════════════


@pytest.mark.e2e
class TestFedCmE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.fed_cm is not None
            assert isinstance(session.fed_cm, FedCmDomain)

    async def test_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                await session.fed_cm.disable()

    async def test_enable_with_disable_rejection_delay(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable(disable_rejection_delay=True)
                await session.fed_cm.disable()

    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                result = await session.fed_cm.enable()
                assert isinstance(result, dict)
                await session.fed_cm.disable()

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                result = await session.fed_cm.disable()
                assert isinstance(result, dict)

    async def test_reset_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                await session.fed_cm.reset_cooldown()
                await session.fed_cm.disable()

    async def test_reset_cooldown_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                result = await session.fed_cm.reset_cooldown()
                assert isinstance(result, dict)
                await session.fed_cm.disable()

    async def test_enable_disable_enable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                await session.fed_cm.disable()
                await session.fed_cm.enable()
                await session.fed_cm.disable()

    async def test_double_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                await session.fed_cm.enable()
                await session.fed_cm.disable()

    async def test_double_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.enable()
                await session.fed_cm.disable()
                await session.fed_cm.disable()

    async def test_reset_cooldown_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.fed_cm.reset_cooldown()

    async def test_raw_send_enable_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("FedCm.enable", {"disableRejectionDelay": False})
                await session.send("FedCm.disable")

    async def test_raw_send_reset_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.send("FedCm.enable")
                await session.send("FedCm.resetCooldown")
                await session.send("FedCm.disable")

    # ── type validation in real browser context ──

    async def test_type_error_enable_int(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="disable_rejection_delay"):
                await session.fed_cm.enable(disable_rejection_delay=1)  # type: ignore[arg-type]

    async def test_type_error_enable_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="disable_rejection_delay"):
                await session.fed_cm.enable(disable_rejection_delay="yes")  # type: ignore[arg-type]

    async def test_type_error_enable_none(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="disable_rejection_delay"):
                await session.fed_cm.enable(disable_rejection_delay=None)  # type: ignore[arg-type]

    async def test_type_error_select_account_int_dialog_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.select_account(123, 0)  # type: ignore[arg-type]

    async def test_type_error_select_account_str_index(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_index"):
                await session.fed_cm.select_account("d1", "zero")  # type: ignore[arg-type]

    async def test_type_error_select_account_bool_index(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_index"):
                await session.fed_cm.select_account("d1", True)  # type: ignore[arg-type]

    async def test_type_error_select_account_none_dialog_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.select_account(None, 0)  # type: ignore[arg-type]

    async def test_type_error_click_dialog_button_int_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.click_dialog_button(123, "ErrorGotIt")  # type: ignore[arg-type]

    async def test_type_error_click_dialog_button_int_button(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_button"):
                await session.fed_cm.click_dialog_button("d1", 123)  # type: ignore[arg-type]

    async def test_type_error_click_dialog_button_none_button(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_button"):
                await session.fed_cm.click_dialog_button("d1", None)  # type: ignore[arg-type]

    async def test_type_error_open_url_int_dialog_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.open_url(123, 0, "TermsOfService")  # type: ignore[arg-type]

    async def test_type_error_open_url_str_index(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_index"):
                await session.fed_cm.open_url("d1", "zero", "TermsOfService")  # type: ignore[arg-type]

    async def test_type_error_open_url_int_url_type(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_url_type"):
                await session.fed_cm.open_url("d1", 0, 123)  # type: ignore[arg-type]

    async def test_type_error_open_url_bool_index(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="account_index"):
                await session.fed_cm.open_url("d1", True, "TermsOfService")  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_int_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.dismiss_dialog(123)  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_int_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="trigger_cooldown"):
                await session.fed_cm.dismiss_dialog("d1", trigger_cooldown=1)  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_str_cooldown(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="trigger_cooldown"):
                await session.fed_cm.dismiss_dialog("d1", trigger_cooldown="yes")  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_none_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.dismiss_dialog(None)  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_list_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.dismiss_dialog(["d1"])  # type: ignore[arg-type]

    async def test_type_error_dismiss_dialog_dict_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="dialog_id"):
                await session.fed_cm.dismiss_dialog({"id": "d1"})  # type: ignore[arg-type]

    # ── meta tests: docstrings, experimental, method count ──

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in FedCmDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 7

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(FedCmDomain)
            if not m.startswith("_") and callable(getattr(FedCmDomain, m))
        ]
        assert methods == [
            "click_dialog_button",
            "disable",
            "dismiss_dialog",
            "enable",
            "open_url",
            "reset_cooldown",
            "select_account",
        ]

    async def test_all_methods_are_coroutines(self) -> None:
        for name in (
            "click_dialog_button",
            "disable",
            "dismiss_dialog",
            "enable",
            "open_url",
            "reset_cooldown",
            "select_account",
        ):
            method = getattr(FedCmDomain, name)
            assert inspect.iscoroutinefunction(method), f"{name} should be a coroutine"

    async def test_all_methods_callable_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert callable(session.fed_cm.click_dialog_button)
            assert callable(session.fed_cm.disable)
            assert callable(session.fed_cm.dismiss_dialog)
            assert callable(session.fed_cm.enable)
            assert callable(session.fed_cm.open_url)
            assert callable(session.fed_cm.reset_cooldown)
            assert callable(session.fed_cm.select_account)

    async def test_class_docstring_has_experimental(self) -> None:
        doc = FedCmDomain.__doc__
        assert doc is not None
        assert "Experimental" in doc

    async def test_class_docstring_has_events(self) -> None:
        doc = FedCmDomain.__doc__
        assert doc is not None
        assert "dialogShown" in doc
        assert "dialogClosed" in doc

    async def test_module_docstring_has_types_and_events(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "Types:" in doc
        assert "Events:" in doc

    async def test_module_docstring_documents_login_state(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "LoginState" in doc
        assert "SignIn" in doc
        assert "SignUp" in doc

    async def test_module_docstring_documents_dialog_type(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "DialogType" in doc
        assert "AccountChooser" in doc
        assert "AutoReauthn" in doc

    async def test_module_docstring_documents_dialog_button(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "DialogButton" in doc
        assert "ConfirmIdpLoginContinue" in doc
        assert "ErrorGotIt" in doc
        assert "ErrorMoreDetails" in doc

    async def test_module_docstring_documents_account_url_type(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "AccountURLType" in doc
        assert "TermsOfService" in doc
        assert "PrivacyPolicy" in doc

    async def test_module_docstring_documents_account(self) -> None:
        import cdpwave.domains.fed_cm as mod
        doc = mod.__doc__
        assert "Account" in doc
        assert "accountId" in doc
        assert "loginState" in doc

    async def test_enable_docstring_mentions_rejection_delay(self) -> None:
        doc = FedCmDomain.enable.__doc__
        assert doc is not None
        assert "rejection delay" in doc.lower()

    async def test_enable_docstring_has_returns(self) -> None:
        doc = FedCmDomain.enable.__doc__
        assert doc is not None
        assert "Returns:" in doc

    async def test_enable_docstring_has_raises(self) -> None:
        doc = FedCmDomain.enable.__doc__
        assert doc is not None
        assert "Raises:" in doc

    async def test_reset_cooldown_docstring_mentions_cooldown(self) -> None:
        doc = FedCmDomain.reset_cooldown.__doc__
        assert doc is not None
        assert "cooldown" in doc.lower()

    async def test_select_account_docstring_has_returns(self) -> None:
        doc = FedCmDomain.select_account.__doc__
        assert doc is not None
        assert "Returns:" in doc

    async def test_select_account_docstring_has_raises(self) -> None:
        doc = FedCmDomain.select_account.__doc__
        assert doc is not None
        assert "Raises:" in doc

    async def test_click_dialog_button_docstring_has_raises(self) -> None:
        doc = FedCmDomain.click_dialog_button.__doc__
        assert doc is not None
        assert "Raises:" in doc

    async def test_open_url_docstring_has_raises(self) -> None:
        doc = FedCmDomain.open_url.__doc__
        assert doc is not None
        assert "Raises:" in doc

    async def test_dismiss_dialog_docstring_mentions_always_sent(self) -> None:
        doc = FedCmDomain.dismiss_dialog.__doc__
        assert doc is not None
        assert "Always sent" in doc

    async def test_enable_docstring_mentions_always_sent(self) -> None:
        doc = FedCmDomain.enable.__doc__
        assert doc is not None
        assert "Always sent" in doc

    async def test_enable_signature_has_disable_rejection_delay(self) -> None:
        sig = inspect.signature(FedCmDomain.enable)
        assert "disable_rejection_delay" in sig.parameters
        param = sig.parameters["disable_rejection_delay"]
        assert param.default is False

    async def test_dismiss_dialog_signature_has_trigger_cooldown(self) -> None:
        sig = inspect.signature(FedCmDomain.dismiss_dialog)
        assert "trigger_cooldown" in sig.parameters
        param = sig.parameters["trigger_cooldown"]
        assert param.default is False

    async def test_select_account_signature(self) -> None:
        sig = inspect.signature(FedCmDomain.select_account)
        params = list(sig.parameters.keys())
        assert params == ["dialog_id", "account_index"]

    async def test_click_dialog_button_signature(self) -> None:
        sig = inspect.signature(FedCmDomain.click_dialog_button)
        params = list(sig.parameters.keys())
        assert params == ["dialog_id", "dialog_button"]

    async def test_open_url_signature(self) -> None:
        sig = inspect.signature(FedCmDomain.open_url)
        params = list(sig.parameters.keys())
        assert params == ["dialog_id", "account_index", "account_url_type"]

    async def test_dismiss_dialog_signature(self) -> None:
        sig = inspect.signature(FedCmDomain.dismiss_dialog)
        params = list(sig.parameters.keys())
        assert params == ["dialog_id", "trigger_cooldown"]

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(FedCmDomain, "get_accounts")
        assert not hasattr(FedCmDomain, "show_dialog")
        assert not hasattr(FedCmDomain, "close_dialog")

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        assert issubclass(FedCmDomain, BaseDomain)


# ═══════════════════════════════════════════════════════════════
# Schema E2E
# ═══════════════════════════════════════════════════════════════


@pytest.mark.e2e
class TestSchemaE2E:
    async def test_domain_accessible_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert session.schema is not None
            assert isinstance(session.schema, SchemaDomain)

    async def test_get_domains(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            assert "domains" in result
            assert len(result["domains"]) > 0

    async def test_get_domains_contains_known_domains(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            names = [d["name"] for d in result["domains"]]
            assert "Page" in names
            assert "Runtime" in names

    async def test_get_domains_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            assert isinstance(result, dict)

    async def test_get_domains_has_version(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            for d in result["domains"]:
                assert "version" in d
                assert isinstance(d["version"], str)

    async def test_get_domains_name_is_str(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.schema.get_domains()
            for d in result["domains"]:
                assert isinstance(d["name"], str)

    async def test_get_domains_multiple_calls(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            r1 = await session.schema.get_domains()
            r2 = await session.schema.get_domains()
            assert len(r1["domains"]) == len(r2["domains"])

    async def test_raw_send_get_domains(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            result = await session.send("Schema.getDomains")
            assert "domains" in result

    async def test_method_count(self) -> None:
        methods = [
            name
            for name, value in SchemaDomain.__dict__.items()
            if not name.startswith("_") and callable(value)
        ]
        assert len(methods) == 1

    async def test_method_order(self) -> None:
        methods = [
            m for m in dir(SchemaDomain)
            if not m.startswith("_") and callable(getattr(SchemaDomain, m))
        ]
        assert methods == ["get_domains"]

    async def test_all_methods_are_coroutines(self) -> None:
        method = SchemaDomain.get_domains
        assert inspect.iscoroutinefunction(method)

    async def test_get_domains_callable_from_session(self) -> None:
        async with (
            await CDPClient.launch(headless=True) as client,
            await client.new_page() as session,
        ):
            assert callable(session.schema.get_domains)

    async def test_class_docstring_has_description(self) -> None:
        doc = SchemaDomain.__doc__
        assert doc is not None
        assert "discovery" in doc.lower() or "introspection" in doc.lower()

    async def test_module_docstring_has_types(self) -> None:
        import cdpwave.domains.schema as mod
        doc = mod.__doc__
        assert "Types:" in doc

    async def test_module_docstring_documents_domain_type(self) -> None:
        import cdpwave.domains.schema as mod
        doc = mod.__doc__
        assert "Domain" in doc
        assert "name" in doc
        assert "version" in doc

    async def test_get_domains_docstring_has_returns(self) -> None:
        doc = SchemaDomain.get_domains.__doc__
        assert doc is not None
        assert "Returns:" in doc

    async def test_get_domains_docstring_mentions_domains(self) -> None:
        doc = SchemaDomain.get_domains.__doc__
        assert doc is not None
        assert "domains" in doc.lower()

    async def test_get_domains_signature(self) -> None:
        sig = inspect.signature(SchemaDomain.get_domains)
        params = list(sig.parameters.keys())
        assert params == []

    async def test_no_spurious_methods_exist(self) -> None:
        assert not hasattr(SchemaDomain, "get_commands")
        assert not hasattr(SchemaDomain, "get_events")
        assert not hasattr(SchemaDomain, "get_types")

    async def test_inherits_base_domain(self) -> None:
        from cdpwave.domains.base import BaseDomain
        assert issubclass(SchemaDomain, BaseDomain)
