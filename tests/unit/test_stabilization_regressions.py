"""Regression tests for bugs found during the stabilization audit."""

import asyncio
import os
from typing import Any
from unittest.mock import MagicMock

import pytest

from cdpwave.browser.discovery import TargetDiscovery
from cdpwave.domains.background_service import BackgroundServiceDomain
from cdpwave.domains.dom import DOMDomain
from cdpwave.domains.network import NetworkDomain
from cdpwave.domains.sensor import SensorDomain
from cdpwave.domains.storage import StorageDomain
from cdpwave.exceptions import ConnectionClosedError, DiscoveryError
from cdpwave.transport.connection import Connection
from cdpwave.transport.correlation import Correlator
from cdpwave.transport.pipe_connection import PipeConnection
from cdpwave.transport.serializer import deserialize_message
from cdpwave.waiters import wait_for_network_idle
from tests.unit.fake_sender import FakeSender


class TestDeserializeNonDict:
    """Non-object JSON payloads must not crash the receive loop."""

    @pytest.mark.parametrize("raw", ['[1, 2, 3]', '"id"', '42', '"str"', 'null', 'true'])
    def test_non_dict_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError, match="not a JSON object"):
            deserialize_message(raw)

    def test_dict_still_works(self) -> None:
        assert deserialize_message('{"id": 1}') == {"id": 1}


class TestDoubleConnect:
    async def test_connection_connect_twice_raises(self) -> None:
        conn = Connection(url="ws://localhost:9222")
        conn._ws = AsyncMockWs()
        with pytest.raises(ConnectionClosedError, match="already connected"):
            await conn.connect()

    async def test_pipe_connect_twice_raises(self) -> None:
        if os.name != "posix":
            pytest.skip("pipe transport is POSIX-only")
        conn = PipeConnection(read_fd=0, write_fd=1)
        conn._read_transport = MagicMock()
        with pytest.raises(ConnectionClosedError, match="already connected"):
            await conn.connect()


class TestCorrelatorDiscard:
    async def test_discard_removes_pending(self) -> None:
        corr = Correlator()
        fut = corr.register(corr.next_id())
        cmd_id = next(iter(corr._pending))
        corr.discard(cmd_id)
        assert corr.pending_count == 0
        assert not fut.done()

    async def test_discard_unknown_id_is_noop(self) -> None:
        corr = Correlator()
        corr.discard(999)
        assert corr.pending_count == 0


class TestSendCommandCancellation:
    async def test_cancel_discards_pending_entry(self) -> None:
        conn = Connection(url="ws://localhost:9222")
        conn._closed = False
        conn._ws = AsyncMockWs()
        task = asyncio.create_task(conn.send_command("Page.enable"))
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert conn._correlator.pending_count == 0

    async def test_send_error_discards_pending_entry(self) -> None:
        conn = Connection(url="ws://localhost:9222")
        conn._closed = False
        ws = AsyncMockWs()
        ws.send_error = RuntimeError("boom")
        conn._ws = ws
        with pytest.raises(RuntimeError, match="boom"):
            await conn.send_command("Page.enable")
        assert conn._correlator.pending_count == 0

    async def test_pipe_cancel_discards_pending_entry(self) -> None:
        conn = PipeConnection(read_fd=0, write_fd=1)
        conn._closed = False
        conn._write_transport = MagicMock()
        task = asyncio.create_task(conn.send_command("Page.enable"))
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert conn._correlator.pending_count == 0


class AsyncMockWs:
    """Minimal async WebSocket double for send_command tests."""

    def __init__(self) -> None:
        self.send_error: Exception | None = None

    async def send(self, message: str) -> None:
        if self.send_error is not None:
            raise self.send_error


class TestStorageTypeEnum:
    async def test_websql_accepted(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_data_for_origin("https://example.com", "websql")
        method, params = fake.last_call
        assert method == "Storage.clearDataForOrigin"
        assert params is not None
        assert params["storageTypes"] == "websql"

    async def test_web_sql_rejected(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        with pytest.raises(ValueError, match="invalid storage type"):
            await domain.clear_data_for_origin("https://example.com", "web_sql")

    @pytest.mark.parametrize(
        "storage_type", ["shader_cache", "storage_buckets", "other"]
    )
    async def test_missing_types_accepted(self, storage_type: str) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_data_for_storage_key("key", storage_type)
        _, params = fake.last_call
        assert params is not None
        assert params["storageTypes"] == storage_type

    async def test_storage_types_normalized(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        await domain.clear_data_for_origin(
            "https://example.com", " cookies, local_storage "
        )
        _, params = fake.last_call
        assert params is not None
        assert params["storageTypes"] == "cookies,local_storage"

    async def test_empty_part_rejected(self) -> None:
        fake = FakeSender({})
        domain = StorageDomain(fake)
        with pytest.raises(ValueError):
            await domain.clear_data_for_origin(
                "https://example.com", "cookies,,local_storage"
            )


class TestNetworkSourceScheme:
    async def test_unset_accepted(self) -> None:
        fake = FakeSender({})
        domain = NetworkDomain(fake)
        await domain.set_cookie("n", "v", source_scheme="Unset")
        _, params = fake.last_call
        assert params is not None
        assert params["sourceScheme"] == "Unset"


class TestDomRelationEnum:
    async def test_controlledby_rejected(self) -> None:
        fake = FakeSender({})
        domain = DOMDomain(fake)
        with pytest.raises(ValueError, match="relation must be"):
            await domain.get_element_by_relation(1, "controlledby")

    async def test_valid_relation_accepted(self) -> None:
        fake = FakeSender({"nodeId": 5})
        domain = DOMDomain(fake)
        await domain.get_element_by_relation(1, "CommandFor")
        _, params = fake.last_call
        assert params == {"nodeId": 1, "relation": "CommandFor"}


class TestSensorTypeEnum:
    async def test_proximity_rejected(self) -> None:
        fake = FakeSender({})
        domain = SensorDomain(fake)
        with pytest.raises(ValueError, match="sensor_type must be one of"):
            await domain.set_sensor_override("proximity")


class TestBackgroundServiceEnum:
    async def test_payment_installments_rejected(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        with pytest.raises(ValueError, match="service must be one of"):
            await domain.start_observing("paymentInstallments")

    async def test_valid_service_accepted(self) -> None:
        fake = FakeSender({})
        domain = BackgroundServiceDomain(fake)
        await domain.start_observing("paymentHandler")
        _, params = fake.last_call
        assert params == {"service": "paymentHandler"}


class TestDiscoveryValidation:
    async def test_get_version_non_dict(self) -> None:
        discovery = TargetDiscovery(port=1)

        import cdpwave.browser.discovery as disc_mod

        orig = disc_mod._http_get
        disc_mod._http_get = lambda url: ["not", "a", "dict"]
        try:
            with pytest.raises(DiscoveryError, match="Malformed /json/version"):
                await discovery.get_version()
        finally:
            disc_mod._http_get = orig

    async def test_list_targets_non_list(self) -> None:
        discovery = TargetDiscovery(port=1)

        import cdpwave.browser.discovery as disc_mod

        orig = disc_mod._http_get
        disc_mod._http_get = lambda url: {"error": "nope"}
        try:
            with pytest.raises(DiscoveryError, match="Malformed /json/list"):
                await discovery.list_targets()
        finally:
            disc_mod._http_get = orig

    async def test_target_id_is_quoted(self) -> None:
        discovery = TargetDiscovery(port=1)
        seen: list[str] = []

        def _record(url: str) -> Any:
            seen.append(url)
            return {}

        import cdpwave.browser.discovery as disc_mod

        orig = disc_mod._http_get
        disc_mod._http_get = _record
        try:
            await discovery.activate_tab("abc/../def?x=1")
        finally:
            disc_mod._http_get = orig
        assert "/json/activate/abc%2F..%2Fdef%3Fx%3D1" in seen[0]


class TestWaitForNetworkIdleOrdering:
    async def test_subscribes_before_enable(self) -> None:
        """Handlers must be registered before Network.enable() is sent."""
        from tests.unit.test_waiters import make_session

        session, dispatch = make_session()
        calls: list[str] = []

        orig_on = session.on

        def _on(event_name: str, handler: Any) -> Any:
            calls.append(f"on:{event_name}")
            return orig_on(event_name, handler)

        session.on = _on

        async def _enable() -> dict[str, Any]:
            calls.append("network.enable")
            return {}

        session.network.enable = _enable

        async def _finish() -> None:
            await asyncio.sleep(0.05)
            for handler in dispatch.get("Network.loadingFinished", []):
                await handler({"requestId": "r1"})

        task = asyncio.create_task(_finish())
        await asyncio.wait_for(wait_for_network_idle(session, idle_time=0.05), 5)
        await task

        first_on = next(i for i, c in enumerate(calls) if c.startswith("on:"))
        enable_idx = calls.index("network.enable")
        assert first_on < enable_idx
