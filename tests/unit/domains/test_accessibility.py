"""Unit tests for the Accessibility domain."""

import pytest

from cdpwave.domains.accessibility import AccessibilityDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDisable:
    async def test_disable_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.disable()
        assert fake.last_call[0] == "Accessibility.disable"

    async def test_disable_params_none(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.disable()
        assert fake.last_call[1] is None

    async def test_disable_returns_response(self) -> None:
        fake = FakeSender({"result": {}})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.disable()
        assert result == {"result": {}}


@pytest.mark.unit
class TestEnable:
    async def test_enable_calls_correct_method(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.enable()
        assert fake.last_call[0] == "Accessibility.enable"

    async def test_enable_params_none(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.enable()
        assert fake.last_call[1] is None

    async def test_enable_returns_response(self) -> None:
        fake = FakeSender({"result": {}})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.enable()
        assert result == {"result": {}}


@pytest.mark.unit
class TestGetAXNodeAndAncestors:
    async def test_no_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors()
        assert fake.last_call[0] == "Accessibility.getAXNodeAndAncestors"
        assert fake.last_call[1] == {}

    async def test_with_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(node_id=42)
        assert fake.last_call[1] == {"nodeId": 42}

    async def test_with_backend_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(backend_node_id=99)
        assert fake.last_call[1] == {"backendNodeId": 99}

    async def test_with_object_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(object_id="obj-123")
        assert fake.last_call[1] == {"objectId": "obj-123"}

    async def test_with_all_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(
            node_id=1, backend_node_id=2, object_id="obj-3"
        )
        assert fake.last_call[1] == {
            "nodeId": 1,
            "backendNodeId": 2,
            "objectId": "obj-3",
        }

    async def test_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(node_id=0)
        assert fake.last_call[1] == {}

    async def test_backend_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(backend_node_id=0)
        assert fake.last_call[1] == {}

    async def test_object_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_ax_node_and_ancestors(object_id="")
        assert fake.last_call[1] == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"nodes": [{"nodeId": "1"}]})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.get_ax_node_and_ancestors(node_id=1)
        assert "nodes" in result


@pytest.mark.unit
class TestGetChildAXNodes:
    async def test_required_id_sent(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_child_ax_nodes("ax-node-1")
        assert fake.last_call[0] == "Accessibility.getChildAXNodes"
        assert fake.last_call[1] == {"id": "ax-node-1"}

    async def test_with_frame_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_child_ax_nodes("ax-node-1", frame_id="frame-1")
        assert fake.last_call[1] == {"id": "ax-node-1", "frameId": "frame-1"}

    async def test_frame_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_child_ax_nodes("ax-node-1", frame_id="")
        assert fake.last_call[1] == {"id": "ax-node-1"}

    async def test_id_is_string_not_int(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_child_ax_nodes("3")
        params = fake.last_call[1]
        assert params is not None
        assert isinstance(params["id"], str)

    async def test_returns_response(self) -> None:
        fake = FakeSender({"nodes": [{"nodeId": "child-1"}]})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.get_child_ax_nodes("ax-node-1")
        assert "nodes" in result


@pytest.mark.unit
class TestGetFullAXTree:
    async def test_no_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree()
        assert fake.last_call[0] == "Accessibility.getFullAXTree"
        assert fake.last_call[1] == {}

    async def test_with_depth(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(depth=2)
        assert fake.last_call[1] == {"depth": 2}

    async def test_with_frame_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(frame_id="frame-1")
        assert fake.last_call[1] == {"frameId": "frame-1"}

    async def test_with_depth_and_frame_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(depth=3, frame_id="frame-1")
        assert fake.last_call[1] == {"depth": 3, "frameId": "frame-1"}

    async def test_depth_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(depth=0)
        assert fake.last_call[1] == {}

    async def test_frame_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(frame_id="")
        assert fake.last_call[1] == {}

    async def test_depth_zero_and_frame_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(depth=0, frame_id="")
        assert fake.last_call[1] == {}

    async def test_negative_depth_sent(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_full_ax_tree(depth=-1)
        assert fake.last_call[1] == {"depth": -1}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"nodes": [{"nodeId": "1"}]})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.get_full_ax_tree()
        assert "nodes" in result


@pytest.mark.unit
class TestGetPartialAXTree:
    async def test_fetch_relatives_always_sent_default_true(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree()
        assert fake.last_call[0] == "Accessibility.getPartialAXTree"
        assert fake.last_call[1] == {"fetchRelatives": True}

    async def test_fetch_relatives_false(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(fetch_relatives=False)
        assert fake.last_call[1] == {"fetchRelatives": False}

    async def test_with_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(node_id=42)
        assert fake.last_call[1] == {"fetchRelatives": True, "nodeId": 42}

    async def test_with_backend_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(backend_node_id=99)
        assert fake.last_call[1] == {
            "fetchRelatives": True,
            "backendNodeId": 99,
        }

    async def test_with_object_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(object_id="obj-1")
        assert fake.last_call[1] == {
            "fetchRelatives": True,
            "objectId": "obj-1",
        }

    async def test_with_all_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(
            node_id=1,
            backend_node_id=2,
            object_id="obj-3",
            fetch_relatives=False,
        )
        assert fake.last_call[1] == {
            "fetchRelatives": False,
            "nodeId": 1,
            "backendNodeId": 2,
            "objectId": "obj-3",
        }

    async def test_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(node_id=0)
        assert fake.last_call[1] == {"fetchRelatives": True}

    async def test_backend_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(backend_node_id=0)
        assert fake.last_call[1] == {"fetchRelatives": True}

    async def test_object_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(object_id="")
        assert fake.last_call[1] == {"fetchRelatives": True}

    async def test_all_zero_with_fetch_relatives_false(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree(
            node_id=0,
            backend_node_id=0,
            object_id="",
            fetch_relatives=False,
        )
        assert fake.last_call[1] == {"fetchRelatives": False}

    async def test_fetch_relatives_only_no_node(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_partial_ax_tree()
        params = fake.last_call[1]
        assert params is not None
        assert "nodeId" not in params
        assert "backendNodeId" not in params
        assert "objectId" not in params

    async def test_returns_response(self) -> None:
        fake = FakeSender({"nodes": [{"nodeId": "1"}]})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.get_partial_ax_tree(node_id=1)
        assert "nodes" in result


@pytest.mark.unit
class TestGetRootAXNode:
    async def test_no_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_root_ax_node()
        assert fake.last_call[0] == "Accessibility.getRootAXNode"
        assert fake.last_call[1] == {}

    async def test_with_frame_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_root_ax_node(frame_id="frame-1")
        assert fake.last_call[1] == {"frameId": "frame-1"}

    async def test_frame_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.get_root_ax_node(frame_id="")
        assert fake.last_call[1] == {}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"node": {"nodeId": "root"}})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.get_root_ax_node()
        assert "node" in result


@pytest.mark.unit
class TestQueryAXTree:
    async def test_no_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree()
        assert fake.last_call[0] == "Accessibility.queryAXTree"
        assert fake.last_call[1] == {}

    async def test_with_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(node_id=42)
        assert fake.last_call[1] == {"nodeId": 42}

    async def test_with_backend_node_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(backend_node_id=99)
        assert fake.last_call[1] == {"backendNodeId": 99}

    async def test_with_object_id(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(object_id="obj-1")
        assert fake.last_call[1] == {"objectId": "obj-1"}

    async def test_with_accessible_name(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(accessible_name="Submit")
        assert fake.last_call[1] == {"accessibleName": "Submit"}

    async def test_with_role(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(role="button")
        assert fake.last_call[1] == {"role": "button"}

    async def test_with_all_params(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(
            node_id=1,
            backend_node_id=2,
            object_id="obj-3",
            accessible_name="Click",
            role="link",
        )
        assert fake.last_call[1] == {
            "nodeId": 1,
            "backendNodeId": 2,
            "objectId": "obj-3",
            "accessibleName": "Click",
            "role": "link",
        }

    async def test_accessible_name_and_role_optional(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(node_id=1)
        params = fake.last_call[1]
        assert params is not None
        assert "accessibleName" not in params
        assert "role" not in params

    async def test_accessible_name_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(accessible_name="")
        assert fake.last_call[1] == {}

    async def test_role_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(role="")
        assert fake.last_call[1] == {}

    async def test_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(node_id=0)
        assert fake.last_call[1] == {}

    async def test_backend_node_id_zero_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(backend_node_id=0)
        assert fake.last_call[1] == {}

    async def test_object_id_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(object_id="")
        assert fake.last_call[1] == {}

    async def test_all_zero_and_empty_omitted(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(
            node_id=0,
            backend_node_id=0,
            object_id="",
            accessible_name="",
            role="",
        )
        assert fake.last_call[1] == {}

    async def test_negative_node_id_sent(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        await domain.query_ax_tree(node_id=-1)
        assert fake.last_call[1] == {"nodeId": -1}

    async def test_returns_response(self) -> None:
        fake = FakeSender({"nodes": [{"nodeId": "1", "role": {"value": "button"}}]})
        domain = AccessibilityDomain(fake.as_sender())
        result = await domain.query_ax_tree(node_id=1, role="button")
        assert "nodes" in result


@pytest.mark.unit
class TestMethodOrder:
    async def test_methods_exist(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        assert hasattr(domain, "disable")
        assert hasattr(domain, "enable")
        assert hasattr(domain, "get_ax_node_and_ancestors")
        assert hasattr(domain, "get_child_ax_nodes")
        assert hasattr(domain, "get_full_ax_tree")
        assert hasattr(domain, "get_partial_ax_tree")
        assert hasattr(domain, "get_root_ax_node")
        assert hasattr(domain, "query_ax_tree")

    async def test_all_methods_count(self) -> None:
        fake = FakeSender()
        domain = AccessibilityDomain(fake.as_sender())
        methods = [
            m for m in dir(domain)
            if not m.startswith("_") and callable(getattr(domain, m))
        ]
        assert len(methods) == 8


@pytest.mark.unit
class TestCallSequence:
    async def test_enable_then_full_tree_then_disable(self) -> None:
        fake = FakeSender({"nodes": []})
        domain = AccessibilityDomain(fake.as_sender())
        await domain.enable()
        await domain.get_full_ax_tree()
        await domain.disable()
        assert len(fake.calls) == 3
        assert fake.calls[0][0] == "Accessibility.enable"
        assert fake.calls[1][0] == "Accessibility.getFullAXTree"
        assert fake.calls[2][0] == "Accessibility.disable"
