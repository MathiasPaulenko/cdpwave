"""Edge-case tests for the ServiceWorker domain — validation branches only.

Targets every TypeError raise in ServiceWorkerDomain to push
coverage from 75% to >=90%.
"""

import pytest

from cdpwave.domains.service_worker import ServiceWorkerDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestServiceWorkerEdgeValidation:
    async def test_deliver_push_message_origin_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="origin must be a string"):
            await d.deliver_push_message(123, "reg", "data")  # type: ignore[arg-type]

    async def test_deliver_push_message_registration_id_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="registration_id must be a string"):
            await d.deliver_push_message("origin", 123, "data")  # type: ignore[arg-type]

    async def test_deliver_push_message_data_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="data must be a string"):
            await d.deliver_push_message("origin", "reg", 123)  # type: ignore[arg-type]

    async def test_dispatch_sync_event_origin_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="origin must be a string"):
            await d.dispatch_sync_event(123, "reg")  # type: ignore[arg-type]

    async def test_dispatch_sync_event_registration_id_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="registration_id must be a string"):
            await d.dispatch_sync_event("origin", 123)  # type: ignore[arg-type]

    async def test_dispatch_sync_event_tag_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="tag must be a string"):
            await d.dispatch_sync_event("origin", "reg", tag=123)  # type: ignore[arg-type]

    async def test_dispatch_sync_event_last_chance_not_bool(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="last_chance must be a bool"):
            await d.dispatch_sync_event("origin", "reg", last_chance="yes")  # type: ignore[arg-type]

    async def test_start_worker_scope_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="scope must be a string"):
            await d.start_worker(123)  # type: ignore[arg-type]

    async def test_skip_waiting_scope_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="scope must be a string"):
            await d.skip_waiting(123)  # type: ignore[arg-type]

    async def test_stop_worker_version_id_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="version_id must be a string"):
            await d.stop_worker(123)  # type: ignore[arg-type]

    async def test_inspect_worker_version_id_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="version_id must be a string"):
            await d.inspect_worker(123)  # type: ignore[arg-type]

    async def test_update_scope_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="scope must be a string"):
            await d.update(123)  # type: ignore[arg-type]

    async def test_unregister_scope_not_str(self) -> None:
        d = ServiceWorkerDomain(FakeSender({}))
        with pytest.raises(TypeError, match="scope must be a string"):
            await d.unregister(123)  # type: ignore[arg-type]
