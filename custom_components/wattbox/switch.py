"""Switch platform for Wattbox integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WattboxDataUpdateCoordinator
from .entity import WattboxOutletEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox switch entities."""
    coordinator: WattboxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Get outlet info from coordinator data
    outlet_info = coordinator.data.get("outlet_info", [])

    # Create switches for each outlet
    switches = []
    for i, _outlet in enumerate(outlet_info):
        switch = WattboxSwitch(
            coordinator=coordinator,
            device_info=coordinator.data.get("device_info", {}),
            unique_id=f"{config_entry.entry_id}_outlet_{i + 1}",
            outlet_number=i + 1,
        )
        switches.append(switch)

    await async_add_entities(switches)


class WattboxSwitch(WattboxOutletEntity, SwitchEntity):
    """Representation of a Wattbox outlet switch."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        device_info: dict[str, Any],
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
        outlet_info = self.coordinator.data.get("outlet_info", [])
        if self._outlet_number <= len(outlet_info):
            outlet = outlet_info[self._outlet_number - 1]
            return bool(outlet.get("state", 0))
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.async_set_outlet_state(self._outlet_number, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.async_set_outlet_state(self._outlet_number, False)
