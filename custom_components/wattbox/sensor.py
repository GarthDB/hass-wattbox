"""Sensor platform for Wattbox integration."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WattboxDataUpdateCoordinator
from .entity import WattboxDeviceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox sensor entities."""
    coordinator: WattboxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create device info sensors
    sensors = [
        WattboxFirmwareSensor(coordinator, config_entry.entry_id),
        WattboxModelSensor(coordinator, config_entry.entry_id),
        WattboxSerialSensor(coordinator, config_entry.entry_id),
        WattboxHostnameSensor(coordinator, config_entry.entry_id),
    ]

    async_add_entities(sensors)


class WattboxFirmwareSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox firmware sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the firmware sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_firmware")
        self._attr_name = "Firmware"
        self._attr_device_class = None

    @property
    def native_value(self) -> str | None:
        """Return the firmware value."""
        device_info = self.coordinator.data.get("device_info", {})
        return device_info.get("hardware_version")


class WattboxModelSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox model sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the model sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_model")
        self._attr_name = "Model"
        self._attr_device_class = None

    @property
    def native_value(self) -> str | None:
        """Return the model value."""
        device_info = self.coordinator.data.get("device_info", {})
        return device_info.get("model")


class WattboxSerialSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox serial sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the serial sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_serial")
        self._attr_name = "Serial Number"
        self._attr_device_class = None

    @property
    def native_value(self) -> str | None:
        """Return the serial value."""
        device_info = self.coordinator.data.get("device_info", {})
        return device_info.get("serial_number")


class WattboxHostnameSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox hostname sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the hostname sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_hostname")
        self._attr_name = "Hostname"
        self._attr_device_class = None

    @property
    def native_value(self) -> str | None:
        """Return the hostname value."""
        device_info = self.coordinator.data.get("device_info", {})
        return device_info.get("hostname")
