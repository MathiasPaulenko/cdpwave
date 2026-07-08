from typing import Any

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
        assert fake.last_call == ("Target.createTarget", {"url": "https://example.com"})

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
        assert fake.last_call == ("Target.getTargets", None)

    async def test_set_auto_attach(self) -> None:
        fake = FakeSender({})
        domain = TargetDomain(fake)
        await domain.set_auto_attach(True, flatten=True)
        assert fake.last_call == (
            "Target.setAutoAttach",
            {"autoAttach": True, "flatten": True},
        )


class TestPageDomain:
    async def test_enable_no_params(self) -> None:
        fake = FakeSender({})
        domain = PageDomain(fake)
        await domain.enable()
        assert fake.last_call == ("Page.enable", None)

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
        assert fake.last_call == ("Page.stop", None)

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
        await domain.print_to_pdf()
        method, params = fake.last_call
        assert method == "Page.printToPDF"
        assert params is not None
        assert params["landscape"] is False
        assert params["scale"] == 1.0
        assert params["paperWidth"] == 8.5
        assert params["paperHeight"] == 11.0

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
        # After fix: only expression is sent when using defaults
        assert "returnByValue" not in params
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
        await domain.call_function_on("OBJ-1", "function() { return 'ok'; }")
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
            "OBJ-1", "function(a, b) { return a + b; }", args=args
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
        assert params["ownProperties"] is True
