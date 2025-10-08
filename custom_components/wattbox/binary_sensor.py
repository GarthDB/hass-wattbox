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

    # Create all status monitoring sensors
    sensors = [
        WattboxStatusBinarySensor(coordinator, config_entry.entry_id),
        WattboxPowerLostBinarySensor(coordinator, config_entry.entry_id),
        WattboxSafeVoltageBinarySensor(coordinator, config_entry.entry_id),
        WattboxUPSConnectedBinarySensor(coordinator, config_entry.entry_id),
        WattboxUPSPowerLostBinarySensor(coordinator, config_entry.entry_id),
    ]

    await async_add_entities(sensors)


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


class WattboxPowerLostBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox power lost binary sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the power lost binary sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_power_lost")
        self._attr_name = "Power Lost"
        self._attr_device_class = "power"

    @property
    def is_on(self) -> bool | None:
        """Return true if power has been lost."""
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        ups_status = status_info.get("ups_status", {})
        return ups_status.get("power_lost", False)


class WattboxSafeVoltageBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox safe voltage binary sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the safe voltage binary sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_safe_voltage")
        self._attr_name = "Safe Voltage"
        self._attr_device_class = "voltage"

    @property
    def is_on(self) -> bool | None:
        """Return true if voltage is safe."""
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        power_status = status_info.get("power_status", {})
        safe_voltage = power_status.get("safe_voltage")
        return safe_voltage == 1 if safe_voltage is not None else None


class WattboxUPSConnectedBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox UPS connected binary sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the UPS connected binary sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_ups_connected")
        self._attr_name = "UPS Connected"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self) -> bool | None:
        """Return true if UPS is connected."""
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        return status_info.get("ups_connected", False)


class WattboxUPSPowerLostBinarySensor(WattboxDeviceEntity, BinarySensorEntity):
    """Representation of a Wattbox UPS power lost binary sensor."""

    def __init__(
        self,
        coordinator: WattboxDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the UPS power lost binary sensor."""
        super().__init__(coordinator, {}, f"{entry_id}_ups_power_lost")
        self._attr_name = "UPS Power Lost"
        self._attr_device_class = "power"

    @property
    def is_on(self) -> bool | None:
        """Return true if UPS has lost power."""
        if not self.coordinator.data.get("connected", False):
            return None
        status_info = self.coordinator.data.get("status_info", {})
        ups_status = status_info.get("ups_status", {})
        return ups_status.get("power_lost", False)
