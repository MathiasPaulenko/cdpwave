import asyncio

from cdpwave.transport.correlation import Correlator


class TestCorrelator:
    def test_next_id_starts_at_1(self) -> None:
        corr = Correlator()
        assert corr.next_id() == 1
        assert corr.next_id() == 2
        assert corr.next_id() == 3

    async def test_register_returns_future(self) -> None:
        corr = Correlator()
        fut = corr.register(1)
        assert isinstance(fut, asyncio.Future)
        assert not fut.done()

    async def test_resolve_sets_result(self) -> None:
        corr = Correlator()
        fut = corr.register(1)
        corr.resolve(1, {"value": 42})
        assert fut.done()
        assert fut.result() == {"value": 42}

    def test_resolve_unknown_id_is_noop(self) -> None:
        corr = Correlator()
        corr.resolve(999, {"value": 42})
        assert corr.pending_count == 0

    async def test_resolve_already_done_is_noop(self) -> None:
        corr = Correlator()
        fut = corr.register(1)
        fut.set_result({"old": True})
        corr.resolve(1, {"new": True})
        assert fut.result() == {"old": True}

    async def test_reject_sets_exception(self) -> None:
        corr = Correlator()
        fut = corr.register(1)
        error = RuntimeError("boom")
        corr.reject(1, error)
        assert fut.done()
        assert fut.exception() is error

    def test_reject_unknown_id_is_noop(self) -> None:
        corr = Correlator()
        corr.reject(999, RuntimeError("boom"))
        assert corr.pending_count == 0

    async def test_reject_already_done_is_noop(self) -> None:
        corr = Correlator()
        fut = corr.register(1)
        fut.set_result({"old": True})
        corr.reject(1, RuntimeError("boom"))
        assert fut.result() == {"old": True}

    async def test_reject_all_rejects_all_pending(self) -> None:
        corr = Correlator()
        fut1 = corr.register(1)
        fut2 = corr.register(2)
        fut3 = corr.register(3)
        error = ConnectionError("closed")
        corr.reject_all(error)
        assert fut1.exception() is error
        assert fut2.exception() is error
        assert fut3.exception() is error
        assert corr.pending_count == 0

    def test_reject_all_on_empty_is_noop(self) -> None:
        corr = Correlator()
        corr.reject_all(RuntimeError("boom"))
        assert corr.pending_count == 0

    async def test_pending_count(self) -> None:
        corr = Correlator()
        assert corr.pending_count == 0
        corr.register(1)
        assert corr.pending_count == 1
        corr.register(2)
        assert corr.pending_count == 2
        corr.resolve(1, {})
        assert corr.pending_count == 1

    async def test_resolve_pops_from_pending(self) -> None:
        corr = Correlator()
        corr.register(1)
        corr.resolve(1, {})
        assert corr.pending_count == 0

    async def test_reject_pops_from_pending(self) -> None:
        corr = Correlator()
        corr.register(1)
        corr.reject(1, RuntimeError("boom"))
        assert corr.pending_count == 0
