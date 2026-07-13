"""BluetoothEmulation domain: Bluetooth emulation for testing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class BluetoothEmulationDomain(BaseDomain):
    """Wrapper for the CDP BluetoothEmulation domain.

    Provides emulation of Bluetooth peripherals for testing
    Web Bluetooth API interactions.
    """

    async def enable(
        self,
        state: str,
        le_supported: bool,
    ) -> dict[str, Any]:
        """Enable the Bluetooth emulation domain.

        Args:
            state: Central state (``"absent"``, ``"powered-off"``,
                ``"powered-on"``).
            le_supported: Whether the simulated central supports low-energy.
        """
        return await self._call(
            "BluetoothEmulation.enable",
            {"state": state, "leSupported": le_supported},
        )

    async def disable(self) -> dict[str, Any]:
        """Disable the Bluetooth emulation domain."""
        return await self._call("BluetoothEmulation.disable")

    async def simulate_preconnected_peripheral(
        self,
        address: str,
        name: str,
        manufacturer_data: list[dict[str, Any]],
        known_service_uuids: list[str],
    ) -> dict[str, Any]:
        """Simulate a preconnected peripheral.

        Args:
            address: Peripheral address.
            name: Peripheral name.
            manufacturer_data: List of manufacturer data entries.
            known_service_uuids: List of known service UUIDs.
        """
        return await self._call(
            "BluetoothEmulation.simulatePreconnectedPeripheral",
            {
                "address": address,
                "name": name,
                "manufacturerData": manufacturer_data,
                "knownServiceUuids": known_service_uuids,
            },
        )

    async def simulate_advertisement(
        self,
        entry: dict[str, Any],
    ) -> dict[str, Any]:
        """Simulate a Bluetooth advertisement.

        Args:
            entry: ``ScanEntry`` dict describing the advertisement packet.
        """
        return await self._call(
            "BluetoothEmulation.simulateAdvertisement",
            {"entry": entry},
        )

    async def set_simulated_central_state(
        self,
        state: str,
    ) -> dict[str, Any]:
        """Set the simulated central state.

        Args:
            state: Central state (``"absent"``, ``"powered-off"``,
                ``"powered-on"``).
        """
        return await self._call(
            "BluetoothEmulation.setSimulatedCentralState",
            {"state": state},
        )

    async def add_service(
        self,
        address: str,
        service_uuid: str,
    ) -> dict[str, Any]:
        """Add a service to a peripheral.

        Args:
            address: Peripheral address.
            service_uuid: Service UUID to add.
        """
        return await self._call(
            "BluetoothEmulation.addService",
            {"address": address, "serviceUuid": service_uuid},
        )

    async def remove_service(
        self,
        service_id: str,
    ) -> dict[str, Any]:
        """Remove a service from the simulated central.

        Args:
            service_id: Service identifier to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeService",
            {"serviceId": service_id},
        )

    async def add_characteristic(
        self,
        service_id: str,
        characteristic_uuid: str,
        properties: dict[str, Any],
    ) -> dict[str, Any]:
        """Add a characteristic to a service.

        Args:
            service_id: Service identifier.
            characteristic_uuid: Characteristic UUID to add.
            properties: ``CharacteristicProperties`` dict.
        """
        return await self._call(
            "BluetoothEmulation.addCharacteristic",
            {
                "serviceId": service_id,
                "characteristicUuid": characteristic_uuid,
                "properties": properties,
            },
        )

    async def remove_characteristic(
        self,
        characteristic_id: str,
    ) -> dict[str, Any]:
        """Remove a characteristic from the simulated central.

        Args:
            characteristic_id: Characteristic identifier to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeCharacteristic",
            {"characteristicId": characteristic_id},
        )

    async def add_descriptor(
        self,
        characteristic_id: str,
        descriptor_uuid: str,
    ) -> dict[str, Any]:
        """Add a descriptor to a characteristic.

        Args:
            characteristic_id: Characteristic identifier.
            descriptor_uuid: Descriptor UUID to add.
        """
        return await self._call(
            "BluetoothEmulation.addDescriptor",
            {
                "characteristicId": characteristic_id,
                "descriptorUuid": descriptor_uuid,
            },
        )

    async def remove_descriptor(
        self,
        descriptor_id: str,
    ) -> dict[str, Any]:
        """Remove a descriptor from the simulated central.

        Args:
            descriptor_id: Descriptor identifier to remove.
        """
        return await self._call(
            "BluetoothEmulation.removeDescriptor",
            {"descriptorId": descriptor_id},
        )

    async def simulate_gatt_disconnection(
        self,
        address: str,
    ) -> dict[str, Any]:
        """Simulate a GATT disconnection.

        Args:
            address: Peripheral address.
        """
        return await self._call(
            "BluetoothEmulation.simulateGATTDisconnection",
            {"address": address},
        )

    async def simulate_gatt_operation_response(
        self,
        address: str,
        op_type: str,
        code: int,
    ) -> dict[str, Any]:
        """Simulate a GATT operation response.

        Args:
            address: Peripheral address.
            op_type: GATT operation type (``"connection"``, ``"discovery"``).
            code: HCI error code from Bluetooth Core Specification Vol 2
                Part D 1.3.
        """
        return await self._call(
            "BluetoothEmulation.simulateGATTOperationResponse",
            {"address": address, "type": op_type, "code": code},
        )

    async def simulate_characteristic_operation_response(
        self,
        characteristic_id: str,
        op_type: str,
        code: int,
        data: str | None = None,
    ) -> dict[str, Any]:
        """Simulate a characteristic operation response.

        Args:
            characteristic_id: Characteristic identifier.
            op_type: Characteristic operation type (``"read"``, ``"write"``,
                ``"subscribe-to-notifications"``,
                ``"unsubscribe-from-notifications"``).
            code: Error code from Bluetooth Core Specification Vol 3
                Part F 3.4.1.1.
            data: Response data (base64). Expected for successful read.
        """
        params: dict[str, Any] = {
            "characteristicId": characteristic_id,
            "type": op_type,
            "code": code,
        }
        if data is not None:
            params["data"] = data
        return await self._call(
            "BluetoothEmulation.simulateCharacteristicOperationResponse",
            params,
        )

    async def simulate_descriptor_operation_response(
        self,
        descriptor_id: str,
        op_type: str,
        code: int,
        data: str | None = None,
    ) -> dict[str, Any]:
        """Simulate a descriptor operation response.

        Args:
            descriptor_id: Descriptor identifier.
            op_type: Descriptor operation type (``"read"``, ``"write"``).
            code: Error code from Bluetooth Core Specification Vol 3
                Part F 3.4.1.1.
            data: Response data (base64). Expected for successful read.
        """
        params: dict[str, Any] = {
            "descriptorId": descriptor_id,
            "type": op_type,
            "code": code,
        }
        if data is not None:
            params["data"] = data
        return await self._call(
            "BluetoothEmulation.simulateDescriptorOperationResponse",
            params,
        )
