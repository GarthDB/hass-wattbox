"""Entity classes for Wattbox integration."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class WattboxEntity(CoordinatorEntity):
    """Base entity for Wattbox devices."""

    def __init__(
        self,
        coordinator: Any,
        device_info: DeviceInfo,
        unique_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info


class WattboxDeviceEntity(WattboxEntity):
    """Base entity for Wattbox device-level entities."""

    def __init__(
        self,
        coordinator: Any,
        device_info: DeviceInfo,
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
        device_info: DeviceInfo,
        unique_id: str,
        outlet_number: int,
    ) -> None:
        """Initialize the outlet entity."""
        super().__init__(coordinator, device_info, unique_id)
        self._outlet_number = outlet_number
        self._attr_should_poll = False
