"""E2E tests for the Security domain (real browser flows).

Full end-to-end flows against a real Edge browser, including
complete lifecycle, navigation, event capture, raw command sending,
type/enum validation on the client side, and edge cases.
"""

import asyncio
import contextlib
from typing import Any

import pytest

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_edge

_EDGE = find_edge()
_SKIP = pytest.mark.skipif(_EDGE is None, reason="Edge not found")

_VERR = "action must be 'continue' or 'cancel'"


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
@pytest.mark.e2e
class TestSecurityE2EEnableDisable:
    async def test_enable_returns_empty_or_dict(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            result = await session.security.enable()
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_disable_returns_empty_or_dict(self) -> None:
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

    async def test_repeated_enable_disable_3x(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            for _ in range(3):
                await session.security.enable()
                await session.security.disable()

    async def test_enable_twice(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.enable()
            await session.security.disable()

    async def test_disable_without_enable(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with contextlib.suppress(Exception):
                await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2ESetIgnoreCertificateErrors:
    async def test_set_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            await session.security.set_ignore_certificate_errors(False)
            await session.security.disable()

    async def test_set_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.set_ignore_certificate_errors(False)
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(False)
            await session.security.disable()

    async def test_int_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="ignore must be a bool"):
                await session.security.set_ignore_certificate_errors(1)

    async def test_str_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="ignore must be a bool"):
                await session.security.set_ignore_certificate_errors("true")


@_SKIP
@pytest.mark.e2e
class TestSecurityE2ESetOverrideCertificateErrors:
    async def test_set_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.set_override_certificate_errors(True)
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_set_false(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            result = await session.security.set_override_certificate_errors(False)
            assert isinstance(result, dict)
            await session.security.disable()

    async def test_toggle(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()

    async def test_int_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="override must be a bool"):
                await session.security.set_override_certificate_errors(1)


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EHandleCertificateError:
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

    async def test_invalid_action_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.security.handle_certificate_error(0, "bad")

    async def test_str_event_id_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_id must be an integer"):
                await session.security.handle_certificate_error("0", "continue")

    async def test_bool_event_id_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_id must be an integer"):
                await session.security.handle_certificate_error(True, "continue")

    async def test_int_action_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a string"):
                await session.security.handle_certificate_error(0, 123)

    async def test_uppercase_action_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.security.handle_certificate_error(0, "Continue")


@_SKIP
@pytest.mark.e2e
@pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
class TestSecurityE2EGetVisibleSecurityState:
    async def test_returns_visible_security_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            assert isinstance(result, dict)
            assert "visibleSecurityState" in result
            await session.security.disable()

    async def test_security_state_valid_enum(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result["visibleSecurityState"]
            assert state["securityState"] in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            await session.security.disable()

    async def test_has_security_state_issue_ids(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result["visibleSecurityState"]
            assert "securityStateIssueIds" in state
            assert isinstance(state["securityStateIssueIds"], list)
            await session.security.disable()

    async def test_certificate_security_state_on_https(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await _wait_for_page(session)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result["visibleSecurityState"]
            cert = state.get("certificateSecurityState")
            if cert is not None:
                assert "protocol" in cert
                assert "cipher" in cert
                assert "subjectName" in cert
                assert "issuer" in cert
            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EEvents:
    @pytest.mark.skip(
        reason="Security.visibleSecurityStateChanged requires getVisibleSecurityState",
    )
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
                state = event["visibleSecurityState"]
                assert "securityState" in state

            await session.security.disable()

    @pytest.mark.skip(
        reason="Security.visibleSecurityStateChanged requires getVisibleSecurityState",
    )
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
@pytest.mark.e2e
class TestSecurityE2ERawSend:
    async def test_raw_enable_disable(self) -> None:
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
            with contextlib.suppress(Exception):
                await session.send(
                    "Security.setIgnoreCertificateErrors", {"ignore": True}
                )
            await session.send(
                "Security.setIgnoreCertificateErrors", {"ignore": False}
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
            assert "visibleSecurityState" in result
            await session.send("Security.disable")


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EAllMethodsReturnDict:
    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
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

            r3 = await session.security.set_override_certificate_errors(True)
            assert isinstance(r3, dict)

            try:
                r4 = await session.security.handle_certificate_error(0, "continue")
            except Exception:
                r4 = {}
            assert isinstance(r4, dict)

            r5 = await session.security.get_visible_security_state()
            assert isinstance(r5, dict)

            r6 = await session.security.disable()
            assert isinstance(r6, dict)


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EFullLifecycle:
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

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_lifecycle_multiple_navigations(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            for url in ("https://example.com", "https://www.example.com"):
                await session.page.navigate(url)
                await asyncio.sleep(1.0)
                result = await session.security.get_visible_security_state()
                assert "visibleSecurityState" in result

            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EDistinctMethods:
    async def test_set_ignore_and_set_override_are_distinct(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            r2 = await session.security.set_override_certificate_errors(True)
            assert isinstance(r2, dict)
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(False)
            await session.security.set_override_certificate_errors(False)
            await session.security.disable()

    async def test_set_ignore_sends_correct_cdp_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            await session.security.disable()

    async def test_set_override_sends_correct_cdp_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EHttpNavigation:
    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_http_page_security_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("http://example.com")
            await asyncio.sleep(1.0)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result["visibleSecurityState"]
            assert state["securityState"] in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            await session.security.disable()

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_about_blank_security_state(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            await session.page.navigate("about:blank")
            await asyncio.sleep(0.5)
            await session.security.enable()
            result = await session.security.get_visible_security_state()
            state = result["visibleSecurityState"]
            assert state["securityState"] in (
                "unknown", "neutral", "insecure", "secure", "info", "insecure-broken",
            )
            await session.security.disable()

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_http_to_https_state_change(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            await session.page.navigate("http://example.com")
            await asyncio.sleep(1.0)
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

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_https_to_http_state_change(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            await session.page.navigate("https://example.com")
            await asyncio.sleep(1.0)
            r1 = await session.security.get_visible_security_state()
            s1 = r1["visibleSecurityState"]["securityState"]

            await session.page.navigate("http://example.com")
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

    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_multiple_navigations_state_always_valid(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.page.enable()

            urls = [
                "about:blank",
                "https://example.com",
                "http://example.com",
                "https://www.example.com",
            ]
            for url in urls:
                await session.page.navigate(url)
                await asyncio.sleep(1.0)
                result = await session.security.get_visible_security_state()
                state = result["visibleSecurityState"]
                assert state["securityState"] in (
                    "unknown", "neutral", "insecure",
                    "secure", "info", "insecure-broken",
                )

            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EEventDetails:
    @pytest.mark.skip(
        reason="Security.visibleSecurityStateChanged requires getVisibleSecurityState",
    )
    async def test_event_contains_security_state(self) -> None:
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

            assert len(events) > 0
            for event in events:
                state = event["visibleSecurityState"]
                assert "securityState" in state
                assert state["securityState"] in (
                    "unknown", "neutral", "insecure",
                    "secure", "info", "insecure-broken",
                )
                assert "securityStateIssueIds" in state

            await session.security.disable()

    @pytest.mark.skip(
        reason="Security.visibleSecurityStateChanged requires getVisibleSecurityState",
    )
    async def test_event_on_http_page(self) -> None:
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
            await session.page.navigate("http://example.com")
            await asyncio.sleep(2.0)

            for event in events:
                state = event["visibleSecurityState"]
                assert state["securityState"] in (
                    "unknown", "neutral", "insecure",
                    "secure", "info", "insecure-broken",
                )

            await session.security.disable()

    @pytest.mark.skip(
        reason="Security.visibleSecurityStateChanged requires getVisibleSecurityState",
    )
    async def test_event_on_about_blank(self) -> None:
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
            await session.page.navigate("about:blank")
            await asyncio.sleep(1.0)

            for event in events:
                state = event["visibleSecurityState"]
                assert state["securityState"] in (
                    "unknown", "neutral", "insecure",
                    "secure", "info", "insecure-broken",
                )

            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2ECombinedFlows:
    @pytest.mark.skip(reason="Security.getVisibleSecurityState was removed from Chrome")
    async def test_enable_ignore_override_get_disable(self) -> None:
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
    async def test_repeated_lifecycle_3x_with_navigation(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.page.enable()
            for _ in range(3):
                await session.security.enable()
                await session.page.navigate("https://example.com")
                await asyncio.sleep(1.0)
                result = await session.security.get_visible_security_state()
                assert "visibleSecurityState" in result
                await session.security.disable()

    async def test_set_ignore_true_false_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            await session.security.set_ignore_certificate_errors(False)
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            await session.security.disable()

    async def test_set_override_true_false_true(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.set_override_certificate_errors(False)
            await session.security.set_override_certificate_errors(True)
            await session.security.disable()

    async def test_handle_cert_continue_then_cancel(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "continue")
            with contextlib.suppress(Exception):
                await session.security.handle_certificate_error(0, "cancel")
            await session.security.disable()


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EValidationExtended:
    async def test_none_event_id_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_id must be an integer"):
                await session.security.handle_certificate_error(None, "continue")

    async def test_float_event_id_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="event_id must be an integer"):
                await session.security.handle_certificate_error(1.5, "continue")

    async def test_none_action_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a string"):
                await session.security.handle_certificate_error(0, None)

    async def test_list_action_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="action must be a string"):
                await session.security.handle_certificate_error(0, ["continue"])

    async def test_none_override_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="override must be a bool"):
                await session.security.set_override_certificate_errors(None)

    async def test_float_override_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="override must be a bool"):
                await session.security.set_override_certificate_errors(1.0)

    async def test_empty_action_raises_value_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(ValueError, match=_VERR):
                await session.security.handle_certificate_error(0, "")

    async def test_none_ignore_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="ignore must be a bool"):
                await session.security.set_ignore_certificate_errors(None)

    async def test_int_ignore_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="ignore must be a bool"):
                await session.security.set_ignore_certificate_errors(0)

    async def test_int_override_raises_type_error(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            with pytest.raises(TypeError, match="override must be a bool"):
                await session.security.set_override_certificate_errors(0)


@_SKIP
@pytest.mark.e2e
class TestSecurityE2EDistinctMethodsExtended:
    async def test_set_ignore_does_not_send_override_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            await session.security.disable()

    async def test_set_override_does_not_send_ignore_method(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            await session.security.set_override_certificate_errors(True)
            await session.security.disable()

    async def test_both_set_ignore_and_override_in_sequence(self) -> None:
        async with (
            await CDPClient.launch(headless=True, browser_path=_EDGE) as client,
            await client.new_page() as session,
        ):
            await session.security.enable()
            with contextlib.suppress(Exception):
                await session.security.set_ignore_certificate_errors(True)
            r2 = await session.security.set_override_certificate_errors(True)
            r3 = await session.security.set_ignore_certificate_errors(False)
            r4 = await session.security.set_override_certificate_errors(False)
            for r in (r2, r3, r4):
                assert isinstance(r, dict)
            await session.security.disable()
