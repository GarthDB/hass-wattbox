"""Entity classes for Wattbox integration."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEVICE_MANUFACTURER, DEVICE_MODEL, DOMAIN


class WattboxEntity(CoordinatorEntity):
    """Base entity for Wattbox devices."""

    def __init__(
        self,
        coordinator: Any,
        device_info: dict[str, Any],
        unique_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._attr_unique_id = unique_id

        # Initialize device info with defaults - will be updated when data is available
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "unknown")},
            name="Wattbox",
            manufacturer=DEVICE_MANUFACTURER,
            model=DEVICE_MODEL,
            sw_version=None,
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        # Update device info if coordinator data is available
        if self.coordinator.data:
            device_data = self.coordinator.data.get("device_info", {})
            if device_data:
                self._attr_device_info = DeviceInfo(
                    identifiers={(DOMAIN, device_data.get("serial_number", "unknown"))},
                    name=device_data.get("hostname", "Wattbox"),
                    manufacturer=DEVICE_MANUFACTURER,
                    model=device_data.get("model", DEVICE_MODEL),
                    sw_version=device_data.get("hardware_version"),
                )
        return self._attr_device_info

    @property
    def should_poll(self) -> bool:
        """Return if polling is needed."""
        return False


class WattboxDeviceEntity(WattboxEntity):
    """Base entity for Wattbox device-level entities."""

    def __init__(
        self,
        coordinator: Any,
        device_info: dict[str, Any],
        unique_id: str,
    ) -> None:
        """Initialize the device entity."""
        super().__init__(coordinator, device_info, unique_id)
        self._attr_should_poll = False


class WattboxOutletEntity(WattboxEntity):
    """Base entity for Wattbox outlet entities."""

    def __init__(
        self,
        coordinator: Any,
        device_info: dict[str, Any],
        unique_id: str,
        outlet_number: int,
    ) -> None:
        """Initialize the outlet entity."""
        super().__init__(coordinator, device_info, unique_id)
        self._outlet_number = outlet_number
        self._attr_should_poll = False
