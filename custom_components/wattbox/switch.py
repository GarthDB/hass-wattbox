"""Switch platform for Wattbox integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import WattboxOutletEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox switch entities."""
    # TODO: Implement switch setup
    # This will be implemented when we create the coordinator and telnet client
    pass


class WattboxSwitch(WattboxOutletEntity, SwitchEntity):
    """Representation of a Wattbox outlet switch."""

    def __init__(
        self,
        coordinator: Any,
        device_info: Any,
        unique_id: str,
        outlet_number: int,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, device_info, unique_id, outlet_number)
        self._attr_name = f"Outlet {outlet_number}"
        self._attr_device_class = "outlet"

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        # TODO: Implement state reading from coordinator
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # TODO: Implement turn on command
        pass

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # TODO: Implement turn off command
        pass
