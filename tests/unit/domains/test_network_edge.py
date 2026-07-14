"""Edge-case tests for the Network domain — validation branches only.

Targets every TypeError/ValueError raise in NetworkDomain to push
coverage from 75% to >=90%.
"""

import pytest

from cdpwave.domains.network import NetworkDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestNetworkEdgeValidation:
    async def test_enable_report_direct_socket_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="report_direct_socket_traffic must be a bool"):
            await d.enable(report_direct_socket_traffic="yes")  # type: ignore[arg-type]

    async def test_enable_enable_durable_messages_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enable_durable_messages must be a bool"):
            await d.enable(enable_durable_messages="yes")  # type: ignore[arg-type]

    async def test_enable_max_total_buffer_size_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_total_buffer_size must be an int or None"):
            await d.enable(max_total_buffer_size="x")  # type: ignore[arg-type]

    async def test_enable_max_total_buffer_size_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_total_buffer_size must be an int or None"):
            await d.enable(max_total_buffer_size=True)  # type: ignore[arg-type]

    async def test_enable_max_resource_buffer_size_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_resource_buffer_size must be an int or None"):
            await d.enable(max_resource_buffer_size="x")  # type: ignore[arg-type]

    async def test_enable_max_resource_buffer_size_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_resource_buffer_size must be an int or None"):
            await d.enable(max_resource_buffer_size=True)  # type: ignore[arg-type]

    async def test_enable_max_post_data_size_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_post_data_size must be an int or None"):
            await d.enable(max_post_data_size="x")  # type: ignore[arg-type]

    async def test_enable_max_post_data_size_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_post_data_size must be an int or None"):
            await d.enable(max_post_data_size=True)  # type: ignore[arg-type]

    async def test_set_user_agent_override_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="user_agent must be a str"):
            await d.set_user_agent_override(123)  # type: ignore[arg-type]

    async def test_set_user_agent_override_accept_language_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="accept_language must be a str or None"):
            await d.set_user_agent_override("UA", accept_language=123)  # type: ignore[arg-type]

    async def test_set_user_agent_override_platform_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="platform must be a str or None"):
            await d.set_user_agent_override("UA", platform=123)  # type: ignore[arg-type]

    async def test_set_user_agent_override_metadata_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="user_agent_metadata must be a dict or None"):
            await d.set_user_agent_override("UA", user_agent_metadata="not-a-dict")  # type: ignore[arg-type]

    async def test_set_extra_request_headers_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="headers must be a dict"):
            await d.set_extra_request_headers("not-a-dict")  # type: ignore[arg-type]

    async def test_get_cookies_urls_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="urls must be a list or None"):
            await d.get_cookies(urls="not-a-list")  # type: ignore[arg-type]

    async def test_get_cookies_url_element_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="urls\\[0\\] must be a str"):
            await d.get_cookies(urls=[123])  # type: ignore[list-item]

    async def test_set_cookie_name_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="name must be a str"):
            await d.set_cookie(123, "val")  # type: ignore[arg-type]

    async def test_set_cookie_value_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="value must be a str"):
            await d.set_cookie("name", 123)  # type: ignore[arg-type]

    async def test_set_cookie_secure_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="secure must be a bool"):
            await d.set_cookie("name", "val", secure="yes")  # type: ignore[arg-type]

    async def test_set_cookie_http_only_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="http_only must be a bool"):
            await d.set_cookie("name", "val", http_only="yes")  # type: ignore[arg-type]

    async def test_set_cookie_url_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url must be a str or None"):
            await d.set_cookie("name", "val", url=123)  # type: ignore[arg-type]

    async def test_set_cookie_domain_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="domain must be a str or None"):
            await d.set_cookie("name", "val", domain=123)  # type: ignore[arg-type]

    async def test_set_cookie_path_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="path must be a str or None"):
            await d.set_cookie("name", "val", path=123)  # type: ignore[arg-type]

    async def test_set_cookie_same_site_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="same_site must be a str or None"):
            await d.set_cookie("name", "val", same_site=123)  # type: ignore[arg-type]

    async def test_set_cookie_same_site_invalid(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(ValueError, match="same_site must be one of"):
            await d.set_cookie("name", "val", same_site="Invalid")

    async def test_set_cookie_expires_not_number(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="expires must be a number or None"):
            await d.set_cookie("name", "val", expires="x")  # type: ignore[arg-type]

    async def test_set_cookie_expires_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="expires must be a number or None"):
            await d.set_cookie("name", "val", expires=True)  # type: ignore[arg-type]

    async def test_set_cookie_priority_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="priority must be a str or None"):
            await d.set_cookie("name", "val", priority=123)  # type: ignore[arg-type]

    async def test_set_cookie_priority_invalid(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(ValueError, match="priority must be one of"):
            await d.set_cookie("name", "val", priority="Invalid")

    async def test_set_cookie_source_scheme_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="source_scheme must be a str or None"):
            await d.set_cookie("name", "val", source_scheme=123)  # type: ignore[arg-type]

    async def test_set_cookie_source_scheme_invalid(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(ValueError, match="source_scheme must be one of"):
            await d.set_cookie("name", "val", source_scheme="Invalid")

    async def test_set_cookie_source_port_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="source_port must be an int or None"):
            await d.set_cookie("name", "val", source_port="x")  # type: ignore[arg-type]

    async def test_set_cookie_source_port_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="source_port must be an int or None"):
            await d.set_cookie("name", "val", source_port=True)  # type: ignore[arg-type]

    async def test_set_cookie_partition_key_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="partition_key must be a dict or None"):
            await d.set_cookie("name", "val", partition_key="not-a-dict")  # type: ignore[arg-type]

    async def test_delete_cookies_name_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="name must be a str"):
            await d.delete_cookies(123)  # type: ignore[arg-type]

    async def test_delete_cookies_url_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url must be a str or None"):
            await d.delete_cookies("name", url=123)  # type: ignore[arg-type]

    async def test_delete_cookies_domain_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="domain must be a str or None"):
            await d.delete_cookies("name", domain=123)  # type: ignore[arg-type]

    async def test_delete_cookies_path_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="path must be a str or None"):
            await d.delete_cookies("name", path=123)  # type: ignore[arg-type]

    async def test_delete_cookies_partition_key_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="partition_key must be a dict or None"):
            await d.delete_cookies("name", partition_key="not-a-dict")  # type: ignore[arg-type]

    async def test_get_response_body_request_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a str"):
            await d.get_response_body(123)  # type: ignore[arg-type]

    async def test_set_cache_disabled_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cache_disabled must be a bool"):
            await d.set_cache_disabled("yes")  # type: ignore[arg-type]

    async def test_set_blocked_urls_url_patterns_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url_patterns must be a list or None"):
            await d.set_blocked_urls(url_patterns="not-a-list")  # type: ignore[arg-type]

    async def test_set_blocked_urls_urls_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="urls must be a list or None"):
            await d.set_blocked_urls(urls="not-a-list")  # type: ignore[arg-type]

    async def test_set_blocked_urls_url_element_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="urls\\[0\\] must be a str"):
            await d.set_blocked_urls(urls=[123])  # type: ignore[list-item]

    async def test_set_bypass_service_worker_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="bypass must be a bool"):
            await d.set_bypass_service_worker("yes")  # type: ignore[arg-type]

    async def test_load_network_resource_url_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="url must be a str"):
            await d.load_network_resource(123, {})  # type: ignore[arg-type]

    async def test_load_network_resource_options_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="options must be a dict"):
            await d.load_network_resource("http://x", "not-a-dict")  # type: ignore[arg-type]

    async def test_load_network_resource_frame_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="frame_id must be a str or None"):
            await d.load_network_resource("http://x", {}, frame_id=123)  # type: ignore[arg-type]

    async def test_get_request_post_data_request_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a str"):
            await d.get_request_post_data(123)  # type: ignore[arg-type]

    async def test_set_cookies_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="cookies must be a list"):
            await d.set_cookies("not-a-list")  # type: ignore[arg-type]

    async def test_emulate_network_conditions_by_rule_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="matched_network_conditions must be a list"):
            await d.emulate_network_conditions_by_rule("not-a-list")  # type: ignore[arg-type]

    async def test_emulate_network_conditions_by_rule_emulate_offline_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="emulate_offline_service_worker must be a bool"):
            await d.emulate_network_conditions_by_rule([], emulate_offline_service_worker="yes")  # type: ignore[arg-type]

    async def test_override_network_state_offline_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="offline must be a bool"):
            await d.override_network_state("yes", 0, 0, 0)  # type: ignore[arg-type]

    async def test_override_network_state_latency_not_number(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="latency must be a number"):
            await d.override_network_state(True, "x", 0, 0)  # type: ignore[arg-type]

    async def test_override_network_state_latency_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="latency must be a number"):
            await d.override_network_state(True, True, 0, 0)  # type: ignore[arg-type]

    async def test_override_network_state_download_not_number(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="download_throughput must be a number"):
            await d.override_network_state(True, 0, "x", 0)  # type: ignore[arg-type]

    async def test_override_network_state_download_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="download_throughput must be a number"):
            await d.override_network_state(True, 0, True, 0)  # type: ignore[arg-type]

    async def test_override_network_state_upload_not_number(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="upload_throughput must be a number"):
            await d.override_network_state(True, 0, 0, "x")  # type: ignore[arg-type]

    async def test_override_network_state_upload_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="upload_throughput must be a number"):
            await d.override_network_state(True, 0, 0, True)  # type: ignore[arg-type]

    async def test_override_network_state_connection_type_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="connection_type must be a str or None"):
            await d.override_network_state(True, 0, 0, 0, connection_type=123)  # type: ignore[arg-type]

    async def test_override_network_state_connection_type_invalid(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(ValueError, match="connection_type must be one of"):
            await d.override_network_state(True, 0, 0, 0, connection_type="invalid")

    async def test_set_accepted_encodings_not_list(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="encodings must be a list"):
            await d.set_accepted_encodings("not-a-list")  # type: ignore[arg-type]

    async def test_set_accepted_encodings_element_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="encodings\\[0\\] must be a str"):
            await d.set_accepted_encodings([123])  # type: ignore[list-item]

    async def test_get_certificate_origin_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="origin must be a str"):
            await d.get_certificate(123)  # type: ignore[arg-type]

    async def test_get_security_isolation_status_frame_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="frame_id must be a str or None"):
            await d.get_security_isolation_status(frame_id=123)  # type: ignore[arg-type]

    async def test_enable_reporting_api_enable_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enable must be a bool"):
            await d.enable_reporting_api("yes")  # type: ignore[arg-type]

    async def test_replay_xhr_request_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a str"):
            await d.replay_xhr(123)  # type: ignore[arg-type]

    async def test_search_in_response_body_request_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a str"):
            await d.search_in_response_body(123, "query")  # type: ignore[arg-type]

    async def test_search_in_response_body_query_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="query must be a str"):
            await d.search_in_response_body("req", 123)  # type: ignore[arg-type]

    async def test_search_in_response_body_case_sensitive_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="case_sensitive must be a bool"):
            await d.search_in_response_body("req", "query", case_sensitive="yes")  # type: ignore[arg-type]

    async def test_search_in_response_body_is_regex_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="is_regex must be a bool"):
            await d.search_in_response_body("req", "query", is_regex="yes")  # type: ignore[arg-type]

    async def test_set_attach_debug_stack_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enabled must be a bool"):
            await d.set_attach_debug_stack("yes")  # type: ignore[arg-type]

    async def test_get_response_body_for_interception_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="interception_id must be a str"):
            await d.get_response_body_for_interception(123)  # type: ignore[arg-type]

    async def test_take_response_body_for_interception_as_stream_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="interception_id must be a str"):
            await d.take_response_body_for_interception_as_stream(123)  # type: ignore[arg-type]

    async def test_stream_resource_content_request_id_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="request_id must be a str"):
            await d.stream_resource_content(123)  # type: ignore[arg-type]

    async def test_fetch_schemeful_site_origin_not_str(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="origin must be a str"):
            await d.fetch_schemeful_site(123)  # type: ignore[arg-type]

    async def test_set_cookie_controls_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enable_third_party_cookie_restriction must be a bool"):
            await d.set_cookie_controls(enable_third_party_cookie_restriction="yes")  # type: ignore[arg-type]

    async def test_enable_device_bound_sessions_not_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="enable must be a bool"):
            await d.enable_device_bound_sessions("yes")  # type: ignore[arg-type]

    async def test_delete_device_bound_session_key_not_dict(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key must be a dict"):
            await d.delete_device_bound_session("not-a-dict")  # type: ignore[arg-type]

    async def test_configure_durable_messages_max_total_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_total_buffer_size must be an int or None"):
            await d.configure_durable_messages(max_total_buffer_size="x")  # type: ignore[arg-type]

    async def test_configure_durable_messages_max_total_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_total_buffer_size must be an int or None"):
            await d.configure_durable_messages(max_total_buffer_size=True)  # type: ignore[arg-type]

    async def test_configure_durable_messages_max_resource_not_int(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_resource_buffer_size must be an int or None"):
            await d.configure_durable_messages(max_resource_buffer_size="x")  # type: ignore[arg-type]

    async def test_configure_durable_messages_max_resource_bool(self) -> None:
        d = NetworkDomain(FakeSender({}))
        with pytest.raises(TypeError, match="max_resource_buffer_size must be an int or None"):
            await d.configure_durable_messages(max_resource_buffer_size=True)  # type: ignore[arg-type]
