"""Binary sensor platform for Wattbox integration."""

from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    """Set up Wattbox binary sensor entities."""
    coordinator: WattboxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create connectivity sensor
    sensor = WattboxStatusBinarySensor(coordinator, config_entry.entry_id)
    async_add_entities([sensor])


class WattboxStatusBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox device status binary sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the status binary sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_status")
        self._attr_name = "Device Status"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self) -> bool | None:
        """Return true if the device is online."""
        return self.coordinator.data.get("connected", False)
