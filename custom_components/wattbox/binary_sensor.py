"""Binary sensor platform for Wattbox integration - v0.2.14 FORCE RELOAD."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WattboxDataUpdateCoordinator
from .entity import WattboxDeviceEntity

_LOGGER = logging.getLogger(__name__)

# v0.2.14: FORCE RELOAD - This comment forces Home Assistant to reload this file
# v0.2.14: COMPLETELY REWRITTEN to break Home Assistant caching


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattbox binary sensor entities."""
    # Check if async_add_entities is None or not callable
    if async_add_entities is None:
        _LOGGER.error(
            "async_add_entities is None! This is a Home Assistant platform issue."
        )
        return
    
    # Debug: Log the type of async_add_entities
    _LOGGER.debug(f"async_add_entities type: {type(async_add_entities)}")
    _LOGGER.debug(f"async_add_entities callable: {callable(async_add_entities)}")

    coordinator: WattboxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create all status monitoring sensors
    sensors = [
        WattboxStatusBinarySensor(coordinator, config_entry.entry_id),
        WattboxPowerLostBinarySensor(coordinator, config_entry.entry_id),
        WattboxSafeVoltageBinarySensor(coordinator, config_entry.entry_id),
        WattboxUPSConnectedBinarySensor(coordinator, config_entry.entry_id),
        WattboxUPSPowerLostBinarySensor(coordinator, config_entry.entry_id),
    ]

    # Filter out any None sensors and ensure we have a list
    valid_sensors = []
    for sensor in sensors:
        if sensor is not None:
            valid_sensors.append(sensor)

    _LOGGER.debug(
        f"Binary sensor setup: {len(sensors)} total, {len(valid_sensors)} valid"
    )

    if valid_sensors:
        # Try calling without await first, as it might not be async
        try:
            if asyncio.iscoroutinefunction(async_add_entities):
                await async_add_entities(valid_sensors)
            else:
                async_add_entities(valid_sensors)
        except Exception as e:
            _LOGGER.error(f"Error adding entities: {e}")
            _LOGGER.error(f"async_add_entities type: {type(async_add_entities)}")
    else:
        _LOGGER.warning("No valid binary sensors to add")


class WattboxStatusBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox device status binary sensor - v0.2.14."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the status binary sensor - v0.2.14."""
        super().__init__(coordinator, {}, f"{entry_id}_status")
        self._attr_name = "Device Status"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self) -> bool | None:
        """Return true if the device is online."""
        if not self.coordinator.data:
            return False
        return self.coordinator.data.get("connected", False)


class WattboxPowerLostBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox power lost binary sensor - v0.2.14."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the power lost binary sensor - v0.2.14."""
        super().__init__(coordinator, {}, f"{entry_id}_power_lost")
        self._attr_name = "Power Lost"
        self._attr_device_class = "power"

    @property
    def is_on(self) -> bool | None:
        """Return true if power has been lost."""
        if not self.coordinator.data:
            return False
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        ups_status = status_info.get("ups_status", {})
        return ups_status.get("power_lost", False)


class WattboxSafeVoltageBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox safe voltage binary sensor - v0.2.14."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the safe voltage binary sensor - v0.2.14."""
        super().__init__(coordinator, {}, f"{entry_id}_safe_voltage")
        self._attr_name = "Safe Voltage"
        self._attr_device_class = "voltage"

    @property
    def is_on(self) -> bool | None:
        """Return true if voltage is safe."""
        if not self.coordinator.data:
            return False
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        power_status = status_info.get("power_status", {})
        safe_voltage = power_status.get("safe_voltage")
        if safe_voltage is None:
            return None
        return bool(safe_voltage)


class WattboxUPSConnectedBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox UPS connected binary sensor - v0.2.14."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the UPS connected binary sensor - v0.2.14."""
        super().__init__(coordinator, {}, f"{entry_id}_ups_connected")
        self._attr_name = "UPS Connected"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self) -> bool | None:
        """Return true if UPS is connected."""
        if not self.coordinator.data:
            return False
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        return status_info.get("ups_connected", False)


class WattboxUPSPowerLostBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox UPS power lost binary sensor - v0.2.14."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the UPS power lost binary sensor - v0.2.14."""
        super().__init__(coordinator, {}, f"{entry_id}_ups_power_lost")
        self._attr_name = "UPS Power Lost"
        self._attr_device_class = "power"

    @property
    def is_on(self) -> bool | None:
        """Return true if UPS power has been lost."""
        if not self.coordinator.data:
            return False
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        ups_status = status_info.get("ups_status", {})
        return ups_status.get("power_lost", False)
