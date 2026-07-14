"""Edge-case tests for the CSS domain — validation branches only.

Targets every TypeError/ValueError raise in CSSDomain to push
coverage from 73% to >=90%.
"""

import pytest

from cdpwave.domains.css import CSSDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestCSSEdgeValidation:
    async def test_add_rule_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.add_rule(123, "rule", {"startLine": 0})  # type: ignore[arg-type]

    async def test_add_rule_rule_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="rule_text must be a string"):
            await d.add_rule("sheet", 123, {"startLine": 0})  # type: ignore[arg-type]

    async def test_add_rule_location_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="location must be a dict"):
            await d.add_rule("sheet", "rule", "not-a-dict")  # type: ignore[arg-type]

    async def test_add_rule_node_validation_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(
            TypeError,
            match="node_for_property_syntax_validation must be an int",
        ):
            await d.add_rule(
                "sheet", "rule", {"startLine": 0},
                node_for_property_syntax_validation="x",  # type: ignore[arg-type]
            )

    async def test_add_rule_node_validation_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(
            TypeError,
            match="node_for_property_syntax_validation must be an int",
        ):
            await d.add_rule(
                "sheet", "rule", {"startLine": 0},
                node_for_property_syntax_validation=True,  # type: ignore[arg-type]
            )

    async def test_collect_class_names_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.collect_class_names(123)  # type: ignore[arg-type]

    async def test_create_style_sheet_frame_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="frame_id must be a string"):
            await d.create_style_sheet(123)  # type: ignore[arg-type]

    async def test_create_style_sheet_force_not_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="force must be a bool"):
            await d.create_style_sheet("frame", force="yes")  # type: ignore[arg-type]

    async def test_force_pseudo_state_node_id_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.force_pseudo_state("x", ["hover"])  # type: ignore[arg-type]

    async def test_force_pseudo_state_node_id_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.force_pseudo_state(True, ["hover"])  # type: ignore[arg-type]

    async def test_force_pseudo_state_classes_not_list(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="forced_pseudo_classes must be a list"):
            await d.force_pseudo_state(1, "hover")  # type: ignore[arg-type]

    async def test_force_starting_style_node_id_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.force_starting_style("x", True)  # type: ignore[arg-type]

    async def test_force_starting_style_node_id_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.force_starting_style(True, True)  # type: ignore[arg-type]

    async def test_force_starting_style_forced_not_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="forced must be a bool"):
            await d.force_starting_style(1, "yes")  # type: ignore[arg-type]

    async def test_get_background_colors_node_id_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_background_colors("x")  # type: ignore[arg-type]

    async def test_get_background_colors_node_id_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_background_colors(True)  # type: ignore[arg-type]

    async def test_get_computed_style_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_computed_style_for_node("x")  # type: ignore[arg-type]

    async def test_get_computed_style_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_computed_style_for_node(True)  # type: ignore[arg-type]

    async def test_resolve_values_values_not_list(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="values must be a list"):
            await d.resolve_values("not-a-list", 1)  # type: ignore[arg-type]

    async def test_resolve_values_node_id_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.resolve_values(["1em"], "x")  # type: ignore[arg-type]

    async def test_resolve_values_node_id_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.resolve_values(["1em"], True)  # type: ignore[arg-type]

    async def test_resolve_values_property_name_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="property_name must be a string"):
            await d.resolve_values(["1em"], 1, property_name=123)  # type: ignore[arg-type]

    async def test_resolve_values_pseudo_type_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="pseudo_type must be a string"):
            await d.resolve_values(["1em"], 1, pseudo_type=123)  # type: ignore[arg-type]

    async def test_resolve_values_pseudo_identifier_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="pseudo_identifier must be a string"):
            await d.resolve_values(["1em"], 1, pseudo_identifier=123)  # type: ignore[arg-type]

    async def test_get_longhand_properties_shorthand_name_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="shorthand_name must be a string"):
            await d.get_longhand_properties(123, "value")  # type: ignore[arg-type]

    async def test_get_longhand_properties_value_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="value must be a string"):
            await d.get_longhand_properties("margin", 123)  # type: ignore[arg-type]

    async def test_get_inline_styles_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_inline_styles_for_node("x")  # type: ignore[arg-type]

    async def test_get_inline_styles_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_inline_styles_for_node(True)  # type: ignore[arg-type]

    async def test_get_animated_styles_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_animated_styles_for_node("x")  # type: ignore[arg-type]

    async def test_get_animated_styles_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_animated_styles_for_node(True)  # type: ignore[arg-type]

    async def test_get_matched_styles_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_matched_styles_for_node("x")  # type: ignore[arg-type]

    async def test_get_matched_styles_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_matched_styles_for_node(True)  # type: ignore[arg-type]

    async def test_get_platform_fonts_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_platform_fonts_for_node("x")  # type: ignore[arg-type]

    async def test_get_platform_fonts_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_platform_fonts_for_node(True)  # type: ignore[arg-type]

    async def test_get_style_sheet_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.get_style_sheet_text(123)  # type: ignore[arg-type]

    async def test_get_layers_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_layers_for_node("x")  # type: ignore[arg-type]

    async def test_get_layers_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_layers_for_node(True)  # type: ignore[arg-type]

    async def test_get_location_for_selector_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.get_location_for_selector(123, "selector")  # type: ignore[arg-type]

    async def test_get_location_for_selector_selector_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="selector_text must be a string"):
            await d.get_location_for_selector("sheet", 123)  # type: ignore[arg-type]

    async def test_track_computed_style_updates_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int or None"):
            await d.track_computed_style_updates_for_node("x")  # type: ignore[arg-type]

    async def test_track_computed_style_updates_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int or None"):
            await d.track_computed_style_updates_for_node(True)  # type: ignore[arg-type]

    async def test_track_computed_style_updates_properties_not_list(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="properties_to_track must be a list"):
            await d.track_computed_style_updates("not-a-list")  # type: ignore[arg-type]

    async def test_set_effective_property_value_for_node_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.set_effective_property_value_for_node("x", "color", "red")  # type: ignore[arg-type]

    async def test_set_effective_property_value_for_node_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.set_effective_property_value_for_node(True, "color", "red")  # type: ignore[arg-type]

    async def test_set_effective_property_value_for_node_property_name_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="property_name must be a string"):
            await d.set_effective_property_value_for_node(1, 123, "red")  # type: ignore[arg-type]

    async def test_set_effective_property_value_for_node_value_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="value must be a string"):
            await d.set_effective_property_value_for_node(1, "color", 123)  # type: ignore[arg-type]

    async def test_set_property_rule_property_name_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_property_rule_property_name(123, {}, "color")  # type: ignore[arg-type]

    async def test_set_property_rule_property_name_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_property_rule_property_name("sheet", "not-a-dict", "color")  # type: ignore[arg-type]

    async def test_set_property_rule_property_name_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="property_name must be a string"):
            await d.set_property_rule_property_name("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_keyframe_key_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_keyframe_key(123, {}, "0%")  # type: ignore[arg-type]

    async def test_set_keyframe_key_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_keyframe_key("sheet", "not-a-dict", "0%")  # type: ignore[arg-type]

    async def test_set_keyframe_key_key_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key_text must be a string"):
            await d.set_keyframe_key("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_media_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_media_text(123, {}, "screen")  # type: ignore[arg-type]

    async def test_set_media_text_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_media_text("sheet", "not-a-dict", "screen")  # type: ignore[arg-type]

    async def test_set_media_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_media_text("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_container_query_condition_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_container_query_condition_text(123, {}, "min-width: 100px")  # type: ignore[arg-type]

    async def test_set_container_query_condition_text_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_container_query_condition_text("sheet", "not-a-dict", "min-width: 100px")  # type: ignore[arg-type]

    async def test_set_container_query_condition_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_container_query_condition_text("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_supports_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_supports_text(123, {}, "display: grid")  # type: ignore[arg-type]

    async def test_set_supports_text_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_supports_text("sheet", "not-a-dict", "display: grid")  # type: ignore[arg-type]

    async def test_set_supports_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_supports_text("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_navigation_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_navigation_text(123, {}, "auto")  # type: ignore[arg-type]

    async def test_set_navigation_text_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_navigation_text("sheet", "not-a-dict", "auto")  # type: ignore[arg-type]

    async def test_set_navigation_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_navigation_text("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_scope_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_scope_text(123, {}, "div")  # type: ignore[arg-type]

    async def test_set_scope_text_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_scope_text("sheet", "not-a-dict", "div")  # type: ignore[arg-type]

    async def test_set_scope_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_scope_text("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_rule_selector_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_rule_selector(123, {}, ".cls")  # type: ignore[arg-type]

    async def test_set_rule_selector_range_not_dict(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="range_ must be a dict"):
            await d.set_rule_selector("sheet", "not-a-dict", ".cls")  # type: ignore[arg-type]

    async def test_set_rule_selector_selector_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="selector must be a string"):
            await d.set_rule_selector("sheet", {}, 123)  # type: ignore[arg-type]

    async def test_set_style_sheet_text_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_style_sheet_text(123, "body { }")  # type: ignore[arg-type]

    async def test_set_style_sheet_text_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_style_sheet_text("sheet", 123)  # type: ignore[arg-type]

    async def test_set_style_texts_edits_not_list(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="edits must be a list"):
            await d.set_style_texts("not-a-list")  # type: ignore[arg-type]

    async def test_set_style_texts_node_validation_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(
            TypeError,
            match="node_for_property_syntax_validation must be an int or None",
        ):
            await d.set_style_texts(
                [], node_for_property_syntax_validation="x",  # type: ignore[arg-type]
            )

    async def test_set_style_texts_node_validation_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(
            TypeError,
            match="node_for_property_syntax_validation must be an int or None",
        ):
            await d.set_style_texts(
                [], node_for_property_syntax_validation=True,  # type: ignore[arg-type]
            )

    async def test_set_local_fonts_enabled_not_bool(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enabled must be a bool"):
            await d.set_local_fonts_enabled("yes")  # type: ignore[arg-type]

    async def test_get_inline_styles_alias_not_int(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="node_id must be an int"):
            await d.get_inline_styles("x")  # type: ignore[arg-type]

    async def test_get_stylesheet_text_alias_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.get_stylesheet_text(123)  # type: ignore[arg-type]

    async def test_set_stylesheet_text_alias_style_sheet_id_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="style_sheet_id must be a string"):
            await d.set_stylesheet_text(123, "body { }")  # type: ignore[arg-type]

    async def test_set_stylesheet_text_alias_text_not_str(self) -> None:
        d = CSSDomain(FakeSender({}))
        with pytest.raises(TypeError, match="text must be a string"):
            await d.set_stylesheet_text("sheet", 123)  # type: ignore[arg-type]
