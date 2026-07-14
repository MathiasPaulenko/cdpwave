from typing import Any

import pytest

from cdpwave.domains.page import PageDomain
from cdpwave.domains.runtime import RuntimeDomain
from cdpwave.domains.target import TargetDomain
from tests.unit.fake_sender import FakeSender


class TestTargetDomain:
    async def test_create_target(self) -> None:
        fake = FakeSender({"targetId": "T-1"})
        domain = TargetDomain(fake)
        result = await domain.create_target("https://example.com")
        assert result == {"targetId": "T-1"}
        assert fake.last_call == (
            "Target.createTarget",
            {
                "url": "https://example.com",
                "enableBeginFrameControl": False,
                "newWindow": False,
                "background": False,
                "forTab": False,
                "hidden": False,
                "focus": False,
            },
        )

    async def test_attach_to_target_default_flatten(self) -> None:
        fake = FakeSender({"sessionId": "S-1"})
        domain = TargetDomain(fake)
        await domain.attach_to_target("T-1")
        assert fake.last_call == (
            "Target.attachToTarget",
            {"targetId": "T-1", "flatten": True},
        )

    async def test_attach_to_target_flatten_false(self) -> None:
        fake = FakeSender({"sessionId": "S-1"})
        domain = TargetDomain(fake)
        await domain.attach_to_target("T-1", flatten=False)
        assert fake.last_call == (
            "Target.attachToTarget",
            {"targetId": "T-1", "flatten": False},
        )

    async def test_detach_from_target(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.detach_from_target("S-1")
        assert fake.last_call == (
            "Target.detachFromTarget",
            {"sessionId": "S-1"},
        )

    async def test_close_target(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.close_target("T-1")
        assert fake.last_call == ("Target.closeTarget", {"targetId": "T-1"})

    async def test_get_targets(self) -> None:
        fake = FakeSender({"targetInfos": []})
        domain = TargetDomain(fake)
        await domain.get_targets()
        assert fake.last_call == ("Target.getTargets", {})

    async def test_set_auto_attach(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_auto_attach(True, flatten=True)
        assert fake.last_call == (
            "Target.setAutoAttach",
            {"autoAttach": True, "waitForDebuggerOnStart": False, "flatten": True},
        )


class TestPageDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Page.enable", {})

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Page.disable", None)

    async def test_navigate_basic(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate("https://example.com")
        assert fake.last_call == (
            "Page.navigate",
            {"url": "https://example.com"},
        )

    async def test_navigate_with_referrer(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate("https://example.com", referrer="https://ref.com")
        assert fake.last_call == (
            "Page.navigate",
            {"url": "https://example.com", "referrer": "https://ref.com"},
        )

    async def test_navigate_with_transition_type(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate(
            "https://example.com", transition_type="link"
        )
        assert fake.last_call == (
            "Page.navigate",
            {"url": "https://example.com", "transitionType": "link"},
        )

    async def test_reload(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload(ignore_cache=True)
        assert fake.last_call == ("Page.reload", {"ignoreCache": True})

    async def test_stop_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.stop()
        assert fake.last_call == ("Page.stopLoading", None)

    async def test_capture_screenshot_defaults(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot()
        method, params = fake.last_call
        assert method == "Page.captureScreenshot"
        assert params is not None
        assert params["format"] == "png"
        assert params["quality"] == 80
        assert params["fromSurface"] is True
        assert params["captureBeyondViewport"] is False
        assert "clip" not in params

    async def test_capture_screenshot_with_clip(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        clip: dict[str, Any] = {"x": 0, "y": 0, "width": 100, "height": 100}
        await domain.capture_screenshot(clip=clip)
        method, params = fake.last_call
        assert method == "Page.captureScreenshot"
        assert params is not None
        assert params["clip"] == clip

    async def test_print_to_pdf_defaults(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        result = await domain.print_to_pdf()
        method, params = fake.last_call
        assert method == "Page.printToPDF"
        assert params is not None
        assert params["landscape"] is False
        assert params["scale"] == 1.0
        assert params["paperWidth"] == 8.5
        assert params["paperHeight"] == 11.0
        assert result == {"data": "base64pdf"}

    async def test_print_to_pdf_invalid_scale(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="scale must be"):
            await domain.print_to_pdf(scale=5.0)

    async def test_capture_screenshot_invalid_format(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="format must be"):
            await domain.capture_screenshot(format="bmp")

    async def test_capture_screenshot_invalid_quality(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        with pytest.raises(ValueError, match="quality must be"):
            await domain.capture_screenshot(quality=200)

    async def test_get_layout_metrics_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.get_layout_metrics()
        assert fake.last_call == ("Page.getLayoutMetrics", None)

    async def test_get_navigation_history_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.get_navigation_history()
        assert fake.last_call == ("Page.getNavigationHistory", None)


class TestRuntimeDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Runtime.enable", None)

    async def test_disable_no_params(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.disable()
        assert fake.last_call == ("Runtime.disable", None)

    async def test_evaluate_defaults(self) -> None:
        fake = FakeSender({"result": {"type": "string", "value": "hi"}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("document.title")
        method, params = fake.last_call
        assert method == "Runtime.evaluate"
        assert params is not None
        assert params["expression"] == "document.title"
        assert params["returnByValue"] is True
        assert "awaitPromise" not in params
        assert "userGesture" not in params

    async def test_evaluate_await_promise(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 42}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("Promise.resolve(42)", await_promise=True)
        method, params = fake.last_call
        assert params is not None
        assert params["awaitPromise"] is True

    async def test_call_function_on(self) -> None:
        fake = FakeSender({"result": {"type": "string", "value": "ok"}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return 'ok'; }", object_id="OBJ-1"
        )
        method, params = fake.last_call
        assert method == "Runtime.callFunctionOn"
        assert params is not None
        assert params["objectId"] == "OBJ-1"
        assert params["functionDeclaration"] == "function() { return 'ok'; }"
        assert "arguments" not in params

    async def test_call_function_on_with_args(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 3}})
        domain = RuntimeDomain(fake)
        args: list[dict[str, Any]] = [{"value": 1}, {"value": 2}]
        await domain.call_function_on(
            "function(a, b) { return a + b; }", object_id="OBJ-1", args=args
        )
        method, params = fake.last_call
        assert params is not None
        assert params["arguments"] == args

    async def test_release_object(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.release_object("OBJ-1")
        assert fake.last_call == (
            "Runtime.releaseObject",
            {"objectId": "OBJ-1"},
        )

    async def test_release_object_group(self) -> None:
        fake = FakeSender({})
        domain = RuntimeDomain(fake)
        await domain.release_object_group("group1")
        assert fake.last_call == (
            "Runtime.releaseObjectGroup",
            {"objectGroup": "group1"},
        )

    async def test_get_properties(self) -> None:
        fake = FakeSender({"result": []})
        domain = RuntimeDomain(fake)
        await domain.get_properties("OBJ-1")
        method, params = fake.last_call
        assert method == "Runtime.getProperties"
        assert params is not None
        assert params["objectId"] == "OBJ-1"
        assert "ownProperties" not in params


class TestRuntimeEdgeCases:
    async def test_evaluate_return_by_value_false(self) -> None:
        fake = FakeSender({"result": {"type": "object", "objectId": "OBJ-1"}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("({a: 1})", return_by_value=False)
        method, params = fake.last_call
        assert params is not None
        assert "returnByValue" not in params

    async def test_evaluate_with_execution_context_id(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 1}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("1+1", execution_context_id=3)
        method, params = fake.last_call
        assert params is not None
        assert params["contextId"] == 3

    async def test_evaluate_with_silent(self) -> None:
        fake = FakeSender({"result": {"type": "undefined"}})
        domain = RuntimeDomain(fake)
        await domain.evaluate("throw new Error()", silent=True)
        method, params = fake.last_call
        assert params is not None
        assert params["silent"] is True

    async def test_call_function_on_no_object_or_context_raises(self) -> None:
        fake = FakeSender({"result": {}})
        domain = RuntimeDomain(fake)
        with pytest.raises(ValueError, match="Either object_id, execution_context_id"):
            await domain.call_function_on("function() {}")

    async def test_call_function_on_with_execution_context_id(self) -> None:
        fake = FakeSender({"result": {"type": "number", "value": 42}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return 42; }", execution_context_id=5
        )
        method, params = fake.last_call
        assert params is not None
        assert params["executionContextId"] == 5
        assert "objectId" not in params

    async def test_call_function_on_return_by_value_false(self) -> None:
        fake = FakeSender({"result": {"type": "object", "objectId": "OBJ-2"}})
        domain = RuntimeDomain(fake)
        await domain.call_function_on(
            "function() { return {}; }", object_id="OBJ-1", return_by_value=False
        )
        method, params = fake.last_call
        assert params is not None
        assert "returnByValue" not in params


class TestPageEdgeCases:
    async def test_navigate_with_all_params(self) -> None:
        fake = FakeSender({"frameId": "F-1"})
        domain = PageDomain(fake)
        await domain.navigate(
            "https://example.com",
            referrer="https://ref.com",
            transition_type="link",
            frame_id="F-0",
            referrer_policy="noReferrer",
        )
        method, params = fake.last_call
        assert params is not None
        assert params["url"] == "https://example.com"
        assert params["referrer"] == "https://ref.com"
        assert params["transitionType"] == "link"
        assert params["frameId"] == "F-0"
        assert params["referrerPolicy"] == "noReferrer"

    async def test_capture_screenshot_webp_format(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(format="webp")
        method, params = fake.last_call
        assert params is not None
        assert params["format"] == "webp"

    async def test_capture_screenshot_quality_zero(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(format="jpeg", quality=0)
        method, params = fake.last_call
        assert params is not None
        assert params["quality"] == 0

    async def test_capture_screenshot_quality_100(self) -> None:
        fake = FakeSender({"data": "base64data"})
        domain = PageDomain(fake)
        await domain.capture_screenshot(format="jpeg", quality=100)
        method, params = fake.last_call
        assert params is not None
        assert params["quality"] == 100

    async def test_print_to_pdf_scale_lower_bound(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(scale=0.1)
        method, params = fake.last_call
        assert params is not None
        assert params["scale"] == 0.1

    async def test_print_to_pdf_scale_upper_bound(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(scale=2.0)
        method, params = fake.last_call
        assert params is not None
        assert params["scale"] == 2.0

    async def test_print_to_pdf_return_as_stream(self) -> None:
        fake = FakeSender({"stream": "stream-handle"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(return_as_stream=True)
        method, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReturnAsStream"

    async def test_print_to_pdf_return_as_base64(self) -> None:
        fake = FakeSender({"data": "base64pdf"})
        domain = PageDomain(fake)
        await domain.print_to_pdf(return_as_stream=False)
        method, params = fake.last_call
        assert params is not None
        assert params["transferMode"] == "ReturnAsBase64"

    async def test_reload_default_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.reload()
        assert fake.last_call == ("Page.reload", None)


class TestTargetEdgeCases:
    async def test_create_target_with_width_height(self) -> None:
        fake = FakeSender({"targetId": "T-1"})
        domain = TargetDomain(fake)
        await domain.create_target("https://example.com", width=800, height=600)
        method, params = fake.last_call
        assert params is not None
        assert params["url"] == "https://example.com"
        assert params["width"] == 800
        assert params["height"] == 600

    async def test_set_auto_attach_no_flatten(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_auto_attach(True, flatten=False)
        assert fake.last_call == (
            "Target.setAutoAttach",
            {"autoAttach": True, "waitForDebuggerOnStart": False, "flatten": False},
        )

    async def test_set_auto_attach_false(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_auto_attach(False)
        assert fake.last_call == (
            "Target.setAutoAttach",
            {"autoAttach": False, "waitForDebuggerOnStart": False, "flatten": True},
        )


class TestDOMEdgeCases:
    async def test_get_attribute_with_name_found(self) -> None:
        from cdpwave.domains.dom import DOMDomain

        fake = FakeSender({"attributes": ["class", "highlight", "id", "main"]})
        domain = DOMDomain(fake)
        result = await domain.get_attribute(42, name="class")
        assert result == {"value": "highlight"}
        assert fake.last_call == ("DOM.getAttributes", {"nodeId": 42})

    async def test_get_attribute_with_name_not_found(self) -> None:
        from cdpwave.domains.dom import DOMDomain

        fake = FakeSender({"attributes": ["class", "highlight"]})
        domain = DOMDomain(fake)
        result = await domain.get_attribute(42, name="id")
        assert result == {"value": None}

    async def test_get_attribute_without_name_returns_all(self) -> None:
        from cdpwave.domains.dom import DOMDomain

        fake = FakeSender({"attributes": ["class", "highlight", "id", "main"]})
        domain = DOMDomain(fake)
        result = await domain.get_attribute(42)
        assert result == {"attributes": ["class", "highlight", "id", "main"]}

    async def test_get_attribute_empty_attributes(self) -> None:
        from cdpwave.domains.dom import DOMDomain

        fake = FakeSender({"attributes": []})
        domain = DOMDomain(fake)
        result = await domain.get_attribute(42, name="class")
        assert result == {"value": None}
