"""Edge case unit tests for the Tethering domain."""

import pytest

from cdpwave.domains.tethering import TetheringDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestTetheringEdgeCases:
    async def test_bind_port_zero(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(0)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 0}

    async def test_unbind_port_zero(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(0)
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": 0}

    async def test_bind_negative_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(-1)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": -1}

    async def test_bind_large_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(65535)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 65535}

    async def test_bind_very_large_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(2147483647)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 2147483647}

    async def test_bind_complex_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind(complex(1, 2))  # type: ignore[arg-type]

    async def test_bind_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind((8080,))  # type: ignore[arg-type]

    async def test_bind_set_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind({8080})  # type: ignore[arg-type]

    async def test_bind_float_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind(3.14)  # type: ignore[arg-type]

    async def test_bind_string_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind("8080")  # type: ignore[arg-type]

    async def test_bind_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind(True)  # type: ignore[arg-type]

    async def test_bind_none_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind(None)  # type: ignore[arg-type]

    async def test_bind_list_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind([8080])  # type: ignore[arg-type]

    async def test_bind_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind({"port": 8080})  # type: ignore[arg-type]

    async def test_bind_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.bind(b"8080")  # type: ignore[arg-type]

    async def test_unbind_float_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind(3.14)  # type: ignore[arg-type]

    async def test_unbind_string_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind("8080")  # type: ignore[arg-type]

    async def test_unbind_bool_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind(True)  # type: ignore[arg-type]

    async def test_unbind_none_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind(None)  # type: ignore[arg-type]

    async def test_unbind_list_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind([8080])  # type: ignore[arg-type]

    async def test_unbind_dict_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind({"port": 8080})  # type: ignore[arg-type]

    async def test_unbind_tuple_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind((8080,))  # type: ignore[arg-type]

    async def test_unbind_set_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind({8080})  # type: ignore[arg-type]

    async def test_unbind_complex_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind(complex(1, 2))  # type: ignore[arg-type]

    async def test_unbind_bytes_raises(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError, match="port must be an integer"):
            await domain.unbind(b"8080")  # type: ignore[arg-type]

    async def test_unbind_negative_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(-1)
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": -1}

    async def test_unbind_large_port(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(65535)
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": 65535}

    async def test_unbind_int_subclass_accepted(self) -> None:
        class MyInt(int):
            pass

        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(MyInt(8080))
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": 8080}

    async def test_return_value_passthrough_bind(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = TetheringDomain(fake)
        result = await domain.bind(8080)
        assert result == {"result": "ok"}

    async def test_return_value_passthrough_unbind(self) -> None:
        fake = FakeSender({"result": "ok"})
        domain = TetheringDomain(fake)
        result = await domain.unbind(8080)
        assert result == {"result": "ok"}

    async def test_multiple_calls_tracked(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(8080)
        await domain.unbind(8080)
        await domain.bind(9090)
        await domain.unbind(9090)
        assert len(fake.calls) == 4
        assert fake.calls[0] == ("Tethering.bind", {"port": 8080})
        assert fake.calls[1] == ("Tethering.unbind", {"port": 8080})
        assert fake.calls[2] == ("Tethering.bind", {"port": 9090})
        assert fake.calls[3] == ("Tethering.unbind", {"port": 9090})

    async def test_bind_same_port_twice(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(8080)
        await domain.bind(8080)
        assert len(fake.calls) == 2
        assert fake.calls[0] == fake.calls[1]

    async def test_unbind_without_bind(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(8080)
        assert len(fake.calls) == 1
        assert fake.calls[0] == ("Tethering.unbind", {"port": 8080})

    async def test_full_lifecycle(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(8080)
        await domain.unbind(8080)
        assert len(fake.calls) == 2
        assert fake.calls[0] == ("Tethering.bind", {"port": 8080})
        assert fake.calls[1] == ("Tethering.unbind", {"port": 8080})

    async def test_no_extra_methods(self) -> None:
        public_methods = {
            name
            for name in dir(TetheringDomain)
            if not name.startswith("_") and callable(getattr(TetheringDomain, name))
        }
        assert public_methods == {"bind", "unbind"}

    async def test_order_matches_pdl(self) -> None:
        methods = [
            name for name in TetheringDomain.__dict__
            if not name.startswith("_") and callable(TetheringDomain.__dict__[name])
        ]
        assert methods.index("bind") < methods.index("unbind")

    async def test_bind_int_subclass_accepted(self) -> None:
        class MyInt(int):
            pass

        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(MyInt(8080))
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 8080}

    async def test_type_error_no_cdp_call_bind(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError):
            await domain.bind("8080")  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_type_error_no_cdp_call_unbind(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        with pytest.raises(TypeError):
            await domain.unbind("8080")  # type: ignore[arg-type]
        assert len(fake.calls) == 0

    async def test_no_enable_method_exists(self) -> None:
        assert not hasattr(TetheringDomain, "enable")

    async def test_no_disable_method_exists(self) -> None:
        assert not hasattr(TetheringDomain, "disable")

    async def test_concurrent_bind_unbind(self) -> None:
        import asyncio

        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await asyncio.gather(
            domain.bind(8080),
            domain.unbind(8080),
            domain.bind(9090),
            domain.unbind(9090),
        )
        assert len(fake.calls) == 4
        methods = [call[0] for call in fake.calls]
        assert methods.count("Tethering.bind") == 2
        assert methods.count("Tethering.unbind") == 2

    async def test_bind_unbind_cycle_repeated(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        for _ in range(5):
            await domain.bind(8080)
            await domain.unbind(8080)
        assert len(fake.calls) == 10
        for i in range(5):
            assert fake.calls[i * 2] == ("Tethering.bind", {"port": 8080})
            assert fake.calls[i * 2 + 1] == ("Tethering.unbind", {"port": 8080})

    async def test_bind_different_ports_each_call(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        for port in range(8000, 8010):
            await domain.bind(port)
        assert len(fake.calls) == 10
        for i, port in enumerate(range(8000, 8010)):
            assert fake.calls[i] == ("Tethering.bind", {"port": port})

    async def test_unbind_all_bound_ports(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        ports = [8000, 8001, 8002, 8003, 8004]
        for port in ports:
            await domain.bind(port)
        for port in ports:
            await domain.unbind(port)
        assert len(fake.calls) == 10
        for i, port in enumerate(ports):
            assert fake.calls[i] == ("Tethering.bind", {"port": port})
            assert fake.calls[i + 5] == ("Tethering.unbind", {"port": port})

    async def test_bind_port_one(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(1)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 1}

    async def test_unbind_port_one(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(1)
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": 1}

    async def test_bind_port_max_int32(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.bind(2147483647)
        method, params = fake.last_call
        assert method == "Tethering.bind"
        assert params == {"port": 2147483647}

    async def test_unbind_port_max_int32(self) -> None:
        fake = FakeSender({})
        domain = TetheringDomain(fake)
        await domain.unbind(2147483647)
        method, params = fake.last_call
        assert method == "Tethering.unbind"
        assert params == {"port": 2147483647}
