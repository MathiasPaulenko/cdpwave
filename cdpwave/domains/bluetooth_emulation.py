"""BluetoothEmulation domain: Bluetooth emulation for testing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class BluetoothEmulationDomain(BaseDomain):
    """Wrapper for the CDP BluetoothEmulation domain.

    Provides emulation of Bluetooth peripherals for testing
    Web Bluetooth API interactions.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Bluetooth emulation domain."""
        return await self._call("BluetoothEmulation.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Bluetooth emulation domain."""
        return await self._call("BluetoothEmulation.disable")

    async def simulate_preconnected_peripheral(
        self,
        address: str,
        name: str,
        known_service_uuids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Simulate a preconnected peripheral.

        Args:
            address: Peripheral address.
            name: Peripheral name.
            known_service_uuids: Optional list of known service UUIDs.
        """
        params: dict[str, Any] = {"address": address, "name": name}
        if known_service_uuids is not None:
            params["knownServiceUuids"] = known_service_uuids
        return await self._call(
            "BluetoothEmulation.simulatePreconnectedPeripheral",
            params,
        )

    async def simulate_advertisement(
        self,
        advertisement: dict[str, Any],
    ) -> dict[str, Any]:
        """Simulate a Bluetooth advertisement.

        Args:
            advertisement: Advertisement dict with ``gpAdvertisement``.
        """
        return await self._call(
            "BluetoothEmulation.simulateAdvertisement",
            {"advertisement": advertisement},
        )

    async def set_simulated_central_state(
        self,
        state: str,
    ) -> dict[str, Any]:
        """Set the simulated central state.

        Args:
            state: Central state (``"unknown"``, ``"resetting"``,
                ``"powered"``, ``"unauthorized"``, ``"poweredOff"``).
        """
        return await self._call(
            "BluetoothEmulation.setSimulatedCentralState",
            {"state": state},
        )

    async def add_service(
        self,
        peripheral_address: str,
        service: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a service to a peripheral.

        Args:
            peripheral_address: Peripheral address.
            service: Service dict with ``uuid`` and ``isPrimary``.
        """
        return await self._call(
            "BluetoothEmulation.addService",
            {
                "peripheralAddress": peripheral_address,
                "service": service,
            },
        )

    async def remove_service(
        self,
        peripheral_address: str,
        service_uuid: str,
    ) -> dict[str, Any]:
        """Remove a service from a peripheral.

        Args:
            peripheral_address: Peripheral address.
            service_uuid: Service UUID to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeService",
            {
                "peripheralAddress": peripheral_address,
                "serviceUuid": service_uuid,
            },
        )

    async def add_characteristic(
        self,
        peripheral_address: str,
        service_uuid: str,
        characteristic: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a characteristic to a service.

        Args:
            peripheral_address: Peripheral address.
            service_uuid: Service UUID.
            characteristic: Characteristic dict.
        """
        return await self._call(
            "BluetoothEmulation.addCharacteristic",
            {
                "peripheralAddress": peripheral_address,
                "serviceUuid": service_uuid,
                "characteristic": characteristic,
            },
        )

    async def remove_characteristic(
        self,
        peripheral_address: str,
        service_uuid: str,
        characteristic_uuid: str,
    ) -> dict[str, Any]:
        """Remove a characteristic from a service.

        Args:
            peripheral_address: Peripheral address.
            service_uuid: Service UUID.
            characteristic_uuid: Characteristic UUID to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeCharacteristic",
            {
                "peripheralAddress": peripheral_address,
                "serviceUuid": service_uuid,
                "characteristicUuid": characteristic_uuid,
            },
        )

    async def add_descriptor(
        self,
        peripheral_address: str,
        service_uuid: str,
        characteristic_uuid: str,
        descriptor: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a descriptor to a characteristic.

        Args:
            peripheral_address: Peripheral address.
            service_uuid: Service UUID.
            characteristic_uuid: Characteristic UUID.
            descriptor: Descriptor dict.
        """
        return await self._call(
            "BluetoothEmulation.addDescriptor",
            {
                "peripheralAddress": peripheral_address,
                "serviceUuid": service_uuid,
                "characteristicUuid": characteristic_uuid,
                "descriptor": descriptor,
            },
        )

    async def remove_descriptor(
        self,
        peripheral_address: str,
        service_uuid: str,
        characteristic_uuid: str,
        descriptor_uuid: str,
    ) -> dict[str, Any]:
        """Remove a descriptor from a characteristic.

        Args:
            peripheral_address: Peripheral address.
            service_uuid: Service UUID.
            characteristic_uuid: Characteristic UUID.
            descriptor_uuid: Descriptor UUID to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeDescriptor",
            {
                "peripheralAddress": peripheral_address,
                "serviceUuid": service_uuid,
                "characteristicUuid": characteristic_uuid,
                "descriptorUuid": descriptor_uuid,
            },
        )

    async def simulate_gatt_disconnection(
        self,
        peripheral_address: str,
    ) -> dict[str, Any]:
        """Simulate a GATT disconnection.

        Args:
            peripheral_address: Peripheral address.
        """
        return await self._call(
            "BluetoothEmulation.simulateGATTDisconnection",
            {"peripheralAddress": peripheral_address},
        )

    async def simulate_gatt_operation_response(
        self,
        peripheral_address: str,
        characteristic_uuid: str,
        status: int,
    ) -> dict[str, Any]:
        """Simulate a GATT operation response.

        Args:
            peripheral_address: Peripheral address.
            characteristic_uuid: Characteristic UUID.
            status: Response status code.
        """
        return await self._call(
            "BluetoothEmulation.simulateGATTOperationResponse",
            {
                "peripheralAddress": peripheral_address,
                "characteristicUuid": characteristic_uuid,
                "status": status,
            },
        )

    async def simulate_characteristic_operation_response(
        self,
        peripheral_address: str,
        characteristic_uuid: str,
        status: int,
    ) -> dict[str, Any]:
        """Simulate a characteristic operation response.

        Args:
            peripheral_address: Peripheral address.
            characteristic_uuid: Characteristic UUID.
            status: Response status code.
        """
        return await self._call(
            "BluetoothEmulation.simulateCharacteristicOperationResponse",
            {
                "peripheralAddress": peripheral_address,
                "characteristicUuid": characteristic_uuid,
                "status": status,
            },
        )

    async def simulate_descriptor_operation_response(
        self,
        peripheral_address: str,
        descriptor_uuid: str,
        status: int,
    ) -> dict[str, Any]:
        """Simulate a descriptor operation response.

        Args:
            peripheral_address: Peripheral address.
            descriptor_uuid: Descriptor UUID.
            status: Response status code.
        """
        return await self._call(
            "BluetoothEmulation.simulateDescriptorOperationResponse",
            {
                "peripheralAddress": peripheral_address,
                "descriptorUuid": descriptor_uuid,
                "status": status,
            },
        )
