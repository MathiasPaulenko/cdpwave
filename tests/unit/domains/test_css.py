"""Unit tests for the CSS domain."""

import pytest

from cdpwave.domains.css import CSSDomain
from tests.unit.fake_sender import FakeSender

RANGE = {"startLine": 0, "startColumn": 0, "endLine": 0, "endColumn": 5}


@pytest.mark.unit
class TestAddRule:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.add_rule("ss1", ".cls { color: red; }", RANGE)
        assert fake.last_call[0] == "CSS.addRule"

    async def test_required_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.add_rule("ss1", ".cls { color: red; }", RANGE)
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["ruleText"] == ".cls { color: red; }"
        assert params["location"] == RANGE

    async def test_optional_node_omitted(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.add_rule("ss1", "rule", RANGE)
        assert "nodeForPropertySyntaxValidation" not in fake.last_call[1]

    async def test_optional_node_present(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.add_rule("ss1", "rule", RANGE, node_for_property_syntax_validation=5)
        assert fake.last_call[1]["nodeForPropertySyntaxValidation"] == 5

    async def test_returns_response(self) -> None:
        fake = FakeSender({"rule": {}})
        domain = CSSDomain(fake.as_sender())
        result = await domain.add_rule("ss1", "rule", RANGE)
        assert result == {"rule": {}}


@pytest.mark.unit
class TestCollectClassNames:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.collect_class_names("ss1")
        assert fake.last_call[0] == "CSS.collectClassNames"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.collect_class_names("ss1")
        assert fake.last_call[1] == {"styleSheetId": "ss1"}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"classNames": ["foo", "bar"]})
        domain = CSSDomain(fake.as_sender())
        result = await domain.collect_class_names("ss1")
        assert result == {"classNames": ["foo", "bar"]}


@pytest.mark.unit
class TestCreateStyleSheet:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.create_style_sheet("frame1")
        assert fake.last_call[0] == "CSS.createStyleSheet"

    async def test_force_false_sent(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.create_style_sheet("frame1")
        assert fake.last_call[1] == {"frameId": "frame1", "force": False}

    async def test_force_true_sent(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.create_style_sheet("frame1", force=True)
        assert fake.last_call[1]["force"] is True

    async def test_returns_response(self) -> None:
        fake = FakeSender({"styleSheetId": "ss1"})
        domain = CSSDomain(fake.as_sender())
        result = await domain.create_style_sheet("frame1")
        assert result == {"styleSheetId": "ss1"}


@pytest.mark.unit
class TestDisable:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.disable()
        assert fake.last_call[0] == "CSS.disable"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.disable()
        assert fake.last_call[1] is None

    async def test_returns_response(self) -> None:
        fake = FakeSender({"result": {}})
        domain = CSSDomain(fake.as_sender())
        result = await domain.disable()
        assert result == {"result": {}}


@pytest.mark.unit
class TestEnable:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.enable()
        assert fake.last_call[0] == "CSS.enable"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.enable()
        assert fake.last_call[1] is None

    async def test_returns_response(self) -> None:
        fake = FakeSender({"result": {}})
        domain = CSSDomain(fake.as_sender())
        result = await domain.enable()
        assert result == {"result": {}}


@pytest.mark.unit
class TestForcePseudoState:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.force_pseudo_state(1, ["hover"])
        assert fake.last_call[0] == "CSS.forcePseudoState"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.force_pseudo_state(1, ["hover", "focus"])
        params = fake.last_call[1]
        assert params["nodeId"] == 1
        assert params["forcedPseudoClasses"] == ["hover", "focus"]


@pytest.mark.unit
class TestForceStartingStyle:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.force_starting_style(1, True)
        assert fake.last_call[0] == "CSS.forceStartingStyle"

    async def test_params_forced_true(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.force_starting_style(1, True)
        params = fake.last_call[1]
        assert params["nodeId"] == 1
        assert params["forced"] is True

    async def test_params_forced_false(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.force_starting_style(1, False)
        assert fake.last_call[1]["forced"] is False


@pytest.mark.unit
class TestGetBackgroundColors:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_background_colors(1)
        assert fake.last_call[0] == "CSS.getBackgroundColors"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_background_colors(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetComputedStyleForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_computed_style_for_node(1)
        assert fake.last_call[0] == "CSS.getComputedStyleForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_computed_style_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestResolveValues:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.resolve_values(["1em"], 1)
        assert fake.last_call[0] == "CSS.resolveValues"

    async def test_required_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.resolve_values(["1em"], 1)
        params = fake.last_call[1]
        assert params["values"] == ["1em"]
        assert params["nodeId"] == 1

    async def test_optionals_omitted(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.resolve_values(["1em"], 1)
        params = fake.last_call[1]
        assert "propertyName" not in params
        assert "pseudoType" not in params
        assert "pseudoIdentifier" not in params

    async def test_optionals_present(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.resolve_values(
            ["1em"], 1,
            property_name="color",
            pseudo_type="::before",
            pseudo_identifier="foo",
        )
        params = fake.last_call[1]
        assert params["propertyName"] == "color"
        assert params["pseudoType"] == "::before"
        assert params["pseudoIdentifier"] == "foo"

    async def test_empty_string_omitted(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.resolve_values(["1em"], 1, property_name="")
        assert "propertyName" not in fake.last_call[1]


@pytest.mark.unit
class TestGetLonghandProperties:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_longhand_properties("margin", "1px 2px")
        assert fake.last_call[0] == "CSS.getLonghandProperties"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_longhand_properties("margin", "1px 2px")
        params = fake.last_call[1]
        assert params["shorthandName"] == "margin"
        assert params["value"] == "1px 2px"
        assert "styleSheetId" not in params


@pytest.mark.unit
class TestGetInlineStylesForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_inline_styles_for_node(1)
        assert fake.last_call[0] == "CSS.getInlineStylesForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_inline_styles_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetAnimatedStylesForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_animated_styles_for_node(1)
        assert fake.last_call[0] == "CSS.getAnimatedStylesForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_animated_styles_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetMatchedStylesForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_matched_styles_for_node(1)
        assert fake.last_call[0] == "CSS.getMatchedStylesForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_matched_styles_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetEnvironmentVariables:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_environment_variables()
        assert fake.last_call[0] == "CSS.getEnvironmentVariables"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_environment_variables()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestGetMediaQueries:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_media_queries()
        assert fake.last_call[0] == "CSS.getMediaQueries"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_media_queries()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestGetPlatformFontsForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_platform_fonts_for_node(1)
        assert fake.last_call[0] == "CSS.getPlatformFontsForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_platform_fonts_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetStyleSheetText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_style_sheet_text("ss1")
        assert fake.last_call[0] == "CSS.getStyleSheetText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_style_sheet_text("ss1")
        assert fake.last_call[1] == {"styleSheetId": "ss1"}


@pytest.mark.unit
class TestGetLayersForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_layers_for_node(1)
        assert fake.last_call[0] == "CSS.getLayersForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_layers_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetLocationForSelector:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_location_for_selector("ss1", ".cls")
        assert fake.last_call[0] == "CSS.getLocationForSelector"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_location_for_selector("ss1", ".cls")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["selectorText"] == ".cls"


@pytest.mark.unit
class TestTrackComputedStyleUpdatesForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates_for_node(1)
        assert fake.last_call[0] == "CSS.trackComputedStyleUpdatesForNode"

    async def test_with_node_id(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates_for_node(1)
        assert fake.last_call[1] == {"nodeId": 1}

    async def test_without_node_id(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates_for_node()
        assert fake.last_call[1] == {}

    async def test_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates_for_node(0)
        assert "nodeId" not in fake.last_call[1]


@pytest.mark.unit
class TestTrackComputedStyleUpdates:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates([{"name": "color"}])
        assert fake.last_call[0] == "CSS.trackComputedStyleUpdates"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        props = [{"name": "color"}, {"name": "background"}]
        await domain.track_computed_style_updates(props)
        assert fake.last_call[1] == {"propertiesToTrack": props}

    async def test_empty_list_sent(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.track_computed_style_updates([])
        assert fake.last_call[1] == {"propertiesToTrack": []}


@pytest.mark.unit
class TestTakeComputedStyleUpdates:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.take_computed_style_updates()
        assert fake.last_call[0] == "CSS.takeComputedStyleUpdates"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.take_computed_style_updates()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestSetEffectivePropertyValueForNode:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_effective_property_value_for_node(1, "color", "red")
        assert fake.last_call[0] == "CSS.setEffectivePropertyValueForNode"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_effective_property_value_for_node(1, "color", "red")
        params = fake.last_call[1]
        assert params["nodeId"] == 1
        assert params["propertyName"] == "color"
        assert params["value"] == "red"


@pytest.mark.unit
class TestSetPropertyRulePropertyName:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_property_rule_property_name("ss1", RANGE, "color")
        assert fake.last_call[0] == "CSS.setPropertyRulePropertyName"

    async def test_sends_property_name_not_name(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_property_rule_property_name("ss1", RANGE, "color")
        params = fake.last_call[1]
        assert params["propertyName"] == "color"
        assert "name" not in params

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_property_rule_property_name("ss1", RANGE, "color")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["range"] == RANGE


@pytest.mark.unit
class TestSetKeyframeKey:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_keyframe_key("ss1", RANGE, "0%")
        assert fake.last_call[0] == "CSS.setKeyframeKey"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_keyframe_key("ss1", RANGE, "0%")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["range"] == RANGE
        assert params["keyText"] == "0%"


@pytest.mark.unit
class TestSetMediaText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_media_text("ss1", RANGE, "screen")
        assert fake.last_call[0] == "CSS.setMediaText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_media_text("ss1", RANGE, "screen")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["range"] == RANGE
        assert params["text"] == "screen"


@pytest.mark.unit
class TestSetContainerQueryConditionText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_container_query_condition_text("ss1", RANGE, "(min-width: 100px)")
        assert fake.last_call[0] == "CSS.setContainerQueryConditionText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_container_query_condition_text("ss1", RANGE, "(min-width: 100px)")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["range"] == RANGE
        assert params["text"] == "(min-width: 100px)"


@pytest.mark.unit
class TestSetSupportsText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_supports_text("ss1", RANGE, "(display: grid)")
        assert fake.last_call[0] == "CSS.setSupportsText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_supports_text("ss1", RANGE, "(display: grid)")
        params = fake.last_call[1]
        assert params["text"] == "(display: grid)"


@pytest.mark.unit
class TestSetNavigationText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_navigation_text("ss1", RANGE, "(prefers-color: dark)")
        assert fake.last_call[0] == "CSS.setNavigationText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_navigation_text("ss1", RANGE, "(prefers-color: dark)")
        params = fake.last_call[1]
        assert params["text"] == "(prefers-color: dark)"


@pytest.mark.unit
class TestSetScopeText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_scope_text("ss1", RANGE, "div")
        assert fake.last_call[0] == "CSS.setScopeText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_scope_text("ss1", RANGE, "div")
        params = fake.last_call[1]
        assert params["text"] == "div"


@pytest.mark.unit
class TestSetRuleSelector:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_rule_selector("ss1", RANGE, ".cls")
        assert fake.last_call[0] == "CSS.setRuleSelector"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_rule_selector("ss1", RANGE, ".cls")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["range"] == RANGE
        assert params["selector"] == ".cls"


@pytest.mark.unit
class TestSetStyleSheetText:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_sheet_text("ss1", "body { color: red; }")
        assert fake.last_call[0] == "CSS.setStyleSheetText"

    async def test_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_sheet_text("ss1", "body { color: red; }")
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["text"] == "body { color: red; }"


@pytest.mark.unit
class TestSetStyleTexts:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_texts([{"styleSheetId": "ss1", "text": "color: red"}])
        assert fake.last_call[0] == "CSS.setStyleTexts"

    async def test_required_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        edits = [{"styleSheetId": "ss1", "text": "color: red", "range": RANGE}]
        await domain.set_style_texts(edits)
        assert fake.last_call[1]["edits"] == edits

    async def test_optional_node_omitted(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_texts([{"styleSheetId": "ss1", "text": "color: red"}])
        assert "nodeForPropertySyntaxValidation" not in fake.last_call[1]

    async def test_optional_node_present(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_texts(
            [{"styleSheetId": "ss1", "text": "color: red"}],
            node_for_property_syntax_validation=5,
        )
        assert fake.last_call[1]["nodeForPropertySyntaxValidation"] == 5


@pytest.mark.unit
class TestStartRuleUsageTracking:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.start_rule_usage_tracking()
        assert fake.last_call[0] == "CSS.startRuleUsageTracking"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.start_rule_usage_tracking()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestStopRuleUsageTracking:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.stop_rule_usage_tracking()
        assert fake.last_call[0] == "CSS.stopRuleUsageTracking"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.stop_rule_usage_tracking()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestTakeCoverageDelta:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.take_coverage_delta()
        assert fake.last_call[0] == "CSS.takeCoverageDelta"

    async def test_params_none(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.take_coverage_delta()
        assert fake.last_call[1] is None


@pytest.mark.unit
class TestSetLocalFontsEnabled:
    async def test_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_local_fonts_enabled(True)
        assert fake.last_call[0] == "CSS.setLocalFontsEnabled"

    async def test_params_true(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_local_fonts_enabled(True)
        assert fake.last_call[1] == {"enabled": True}

    async def test_params_false(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_local_fonts_enabled(False)
        assert fake.last_call[1]["enabled"] is False


# -- Convenience method tests --

@pytest.mark.unit
class TestGetInlineStylesAlias:
    async def test_delegates_to_get_inline_styles_for_node(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_inline_styles(1)
        assert fake.last_call[0] == "CSS.getInlineStylesForNode"
        assert fake.last_call[1] == {"nodeId": 1}


@pytest.mark.unit
class TestGetStylesheetTextAlias:
    async def test_delegates_to_get_style_sheet_text(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.get_stylesheet_text("ss1")
        assert fake.last_call[0] == "CSS.getStyleSheetText"
        assert fake.last_call[1] == {"styleSheetId": "ss1"}


@pytest.mark.unit
class TestSetStylesheetTextAlias:
    async def test_delegates_to_set_style_sheet_text(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_stylesheet_text("ss1", "body {}")
        assert fake.last_call[0] == "CSS.setStyleSheetText"
        params = fake.last_call[1]
        assert params["styleSheetId"] == "ss1"
        assert params["text"] == "body {}"


@pytest.mark.unit
class TestSetRuleStyle:
    async def test_calls_set_style_texts(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_rule_style("ss1", "color: green")
        assert fake.last_call[0] == "CSS.setStyleTexts"

    async def test_edit_without_range(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_rule_style("ss1", "color: green")
        edit = fake.last_call[1]["edits"][0]
        assert edit["styleSheetId"] == "ss1"
        assert edit["text"] == "color: green"
        assert "range" not in edit

    async def test_edit_with_range(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_rule_style("ss1", "color: green", range_=RANGE)
        edit = fake.last_call[1]["edits"][0]
        assert edit["range"] == RANGE


@pytest.mark.unit
class TestSetStyleText:
    async def test_calls_set_style_texts(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_text("ss1", RANGE, "color: red")
        assert fake.last_call[0] == "CSS.setStyleTexts"

    async def test_edit_params(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.set_style_text("ss1", RANGE, "color: red")
        edit = fake.last_call[1]["edits"][0]
        assert edit["styleSheetId"] == "ss1"
        assert edit["range"] == RANGE
        assert edit["text"] == "color: red"


@pytest.mark.unit
class TestCallSequence:
    async def test_multiple_calls(self) -> None:
        fake = FakeSender()
        domain = CSSDomain(fake.as_sender())
        await domain.enable()
        await domain.get_media_queries()
        await domain.disable()
        assert len(fake.calls) == 3
        assert fake.calls[0][0] == "CSS.enable"
        assert fake.calls[1][0] == "CSS.getMediaQueries"
        assert fake.calls[2][0] == "CSS.disable"
