"""Integration tests for the Security domain with a real browser."""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_edge

_EDGE = find_edge()
_SKIP = pytest.mark.skipif(_EDGE is None, reason="Edge not found")


async def _wait_for_page(page: CDPSession) -> None:
    await page.page.enable()
    await page.page.navigate("https://example.com")
    for _ in range(20):
        await asyncio.sleep(0.5)
        result = await page.runtime.evaluate(
            "document.title", return_by_value=True
        )
        if result.get("result", {}).get("value"):
            break


@_SKIP
@pytest.mark.integration
class TestSecurityEnableDisable:
    async def test_enable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            result = await session.security.enable()
            assert isinstance(result, dict)

    async def test_disable_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.disable()
            assert isinstance(result, dict)

    async def test_enable_disable_cycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.security.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.enable()
            await session.security.disable()

    async def test_repeated_enable_disable_3x(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.security.enable()
                await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecuritySetIgnoreCertificateErrors:
    async def test_set_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_ignore_certificate_errors(True)
            await session.security.disable()

    async def test_set_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_ignore_certificate_errors(False)
            await session.security.disable()

    async def test_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.set_ignore_certificate_errors(True)
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_toggle_true_then_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_ignore_certificate_errors(True)
            await session.security.set_ignore_certificate_errors(False)
            await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecuritySetOverrideCertificateErrors:
    async def test_set_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.disable()

    async def test_set_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()

    async def test_returns_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.set_override_certificate_errors(True)
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_toggle_true_then_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecurityHandleCertificateError:
    async def test_continue(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "continue")
            await session.security.disable()

    async def test_cancel(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "cancel")
            await session.security.disable()

    async def test_returns_dict_when_succeeds(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            try:
                result = await session.security.handle_certificate_error(0, "continue")
            except Exception:
                pass
            else:
                assert isinstance(result, dict)
            await session.security.disable()


@_SKIP
@pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
@pytest.mark.integration
class TestSecurityGetVisibleSecurityState:
    async def test_returns_dict_with_visible_security_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            assert isinstance(result, dict)
            assert "visibleSecurityState" in result

    async def test_security_state_is_valid_enum(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result.get("visibleSecurityState", {})
            security_state = state.get("securityState")
            assert security_state in (
                "unknown",
                "neutral",
                "insecure",
                "secure",
                "info",
                "insecure-broken",
            )

    async def test_has_security_state_issue_ids(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result.get("visibleSecurityState", {})
            assert "securityStateIssueIds" in state
            assert isinstance(state["securityStateIssueIds"], list)

    async def test_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.security.get_visible_security_state()
                assert isinstance(result, dict)


@_SKIP
@pytest.mark.integration
class TestSecurityEvents:
    async def test_visible_security_state_changed_event(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            await session.security.enable()
            session.on("Security.visibleSecurityStateChanged", on_event)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(2.0)

            for event in events:
                assert "visibleSecurityState" in event

            await session.security.disable()

    async def test_no_events_after_disable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            events: list[dict[str, Any]] = []

            async def on_event(params: dict[str, Any]) -> None:
                events.append(params)

            await session.security.enable()
            await session.security.disable()
            session.on("Security.visibleSecurityStateChanged", on_event)

            await session.page.enable()
            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            assert len(events) == 0


@_SKIP
@pytest.mark.integration
class TestSecurityRawSend:
    async def test_raw_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.send("Security.enable")
            await session.send("Security.disable")

    async def test_raw_set_ignore_certificate_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.send("Security.enable")
            await session.send(
                "Security.setIgnoreCertificateErrors", {"ignore": True}
            )
            await session.send("Security.disable")

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_raw_get_visible_security_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.send("Security.enable")
            result = await session.send("Security.getVisibleSecurityState")
            assert isinstance(result, dict)
            await session.send("Security.disable")


@_SKIP
@pytest.mark.integration
class TestSecurityAllMethodsReturnDict:
    async def test_all_methods_return_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            r1 = await session.security.enable()
            assert isinstance(r1, dict)

            r2 = await session.security.set_ignore_certificate_errors(True)
            assert isinstance(r2, dict)

            await session.security.set_ignore_certificate_errors(False)
            r3 = await session.security.set_override_certificate_errors(True)
            assert isinstance(r3, dict)

            try:
                r4 = await session.security.handle_certificate_error(0, "continue")
            except Exception:
                r4 = {}
            assert isinstance(r4, dict)

            with contextlib.suppress(Exception):
                r5 = await session.security.get_visible_security_state()
                assert isinstance(r5, dict)

            r6 = await session.security.disable()
            assert isinstance(r6, dict)


@_SKIP
@pytest.mark.integration
class TestSecurityFullLifecycle:
    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_full_lifecycle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)

            await session.security.enable()
            await session.security.set_ignore_certificate_errors(True)
            await session.security.set_override_certificate_errors(True)
            result = await session.security.get_visible_security_state()
            assert "visibleSecurityState" in result
            await session.security.set_override_certificate_errors(False)
            await session.security.set_ignore_certificate_errors(False)
            await session.security.disable()

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_lifecycle_with_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)

            result = await session.security.get_visible_security_state()
            assert "visibleSecurityState" in result

            await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecurityWithoutEnable:
    async def test_set_ignore_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)

    async def test_set_override_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.security.set_override_certificate_errors(True)

    async def test_handle_certificate_error_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "continue")

    async def test_get_visible_security_state_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            with contextlib.suppress(Exception):
                result = await session.security.get_visible_security_state()
                assert isinstance(result, dict)


@_SKIP
@pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
@pytest.mark.integration
class TestSecurityGetVisibleSecurityStateExtended:
    async def test_about_blank(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("about:blank")
            await asyncio.sleep(0.5)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            assert isinstance(result, dict)
            assert "visibleSecurityState" in result
            state = result["visibleSecurityState"]
            assert state["securityState"] in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            await session.security.disable()

    async def test_http_page(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("http://example.com")
            await asyncio.sleep(1.0)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            assert isinstance(result, dict)
            state = result.get("visibleSecurityState", {})
            assert state.get("securityState") in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            await session.security.disable()

    async def test_https_has_certificate_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result.get("visibleSecurityState", {})
            cert = state.get("certificateSecurityState")
            if cert is not None:
                assert "protocol" in cert
                assert "cipher" in cert
                assert "subjectName" in cert
                assert "issuer" in cert
                assert "validFrom" in cert
                assert "validTo" in cert
            await session.security.disable()

    async def test_state_changes_between_navigations(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            await session.page.navigate("about:blank")
            await asyncio.sleep(0.5)
            r1 = await session.security.get_visible_security_state()
            s1 = r1["visibleSecurityState"]["securityState"]

            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            r2 = await session.security.get_visible_security_state()
            s2 = r2["visibleSecurityState"]["securityState"]

            assert s1 in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            assert s2 in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )

            await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecurityCombinedOperations:
    async def test_set_ignore_and_override_together(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_ignore_certificate_errors(True)
            await session.security.set_ignore_certificate_errors(False)
            await session.security.set_override_certificate_errors(True)
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()

    async def test_override_then_handle_certificate_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "continue")
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()

    async def test_handle_certificate_error_large_event_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(999999, "continue")
            await session.security.disable()

    async def test_handle_certificate_error_negative_event_id(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(-1, "cancel")
            await session.security.disable()

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_multiple_enable_disable_with_state_check(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            for _ in range(3):
                await session.security.enable()
                result = await session.security.get_visible_security_state()
                assert "visibleSecurityState" in result
                await session.security.disable()


@_SKIP
@pytest.mark.integration
class TestSecurityRawSendExtended:
    async def test_raw_handle_certificate_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.send("Security.enable")
            with contextlib.suppress(Exception):
                await session.send(
                    "Security.handleCertificateError",
                    {"eventId": 0, "action": "continue"},
                )
            await session.send("Security.disable")

    async def test_raw_set_override_certificate_errors(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.send("Security.enable")
            await session.send(
                "Security.setOverrideCertificateErrors", {"override": True}
            )
            await session.send(
                "Security.setOverrideCertificateErrors", {"override": False}
            )
            await session.send("Security.disable")
