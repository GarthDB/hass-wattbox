"""Binary sensor platform for Wattbox integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import WattboxDeviceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox binary sensor entities."""
    # TODO: Implement binary sensor setup
    # This will be implemented when we create the coordinator and telnet client
    pass


class WattboxStatusBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox device status binary sensor."""

    def __init__(
        self,
        coordinator: Any,
        device_info: Any,
        unique_id: str,
    ) -> None:
        """Initialize the status binary sensor."""
        super().__init__(coordinator, device_info, unique_id)
        self._attr_name = "Device Status"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self) -> bool | None:
        """Return true if the device is online."""
        # TODO: Implement status reading from coordinator
        return None
