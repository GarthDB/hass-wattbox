"""Sensor platform for Wattbox integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricPotential, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import WattboxDeviceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox sensor entities."""
    # TODO: Implement sensor setup
    # This will be implemented when we create the coordinator and telnet client
    pass


class WattboxVoltageSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox voltage sensor."""

    def __init__(
        self,
        coordinator: Any,
        device_info: Any,
        unique_id: str,
    ) -> None:
        """Initialize the voltage sensor."""
        super().__init__(coordinator, device_info, unique_id)
        self._attr_name = "Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = "voltage"

    @property
    def native_value(self) -> float | None:
        """Return the voltage value."""
        # TODO: Implement value reading from coordinator
        return None


class WattboxCurrentSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox current sensor."""

    def __init__(
        self,
        coordinator: Any,
        device_info: Any,
        unique_id: str,
    ) -> None:
        """Initialize the current sensor."""
        super().__init__(coordinator, device_info, unique_id)
        self._attr_name = "Current"
        self._attr_native_unit_of_measurement = "A"
        self._attr_device_class = "current"

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        # TODO: Implement value reading from coordinator
        return None


class WattboxPowerSensor(WattboxDeviceEntity, SensorEntity):
    """Representation of a Wattbox power sensor."""

    def __init__(
        self,
        coordinator: Any,
        device_info: Any,
        unique_id: str,
    ) -> None:
        """Initialize the power sensor."""
        super().__init__(coordinator, device_info, unique_id)
        self._attr_name = "Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = "power"

    @property
    def native_value(self) -> float | None:
        """Return the power value."""
        # TODO: Implement value reading from coordinator
        return None
