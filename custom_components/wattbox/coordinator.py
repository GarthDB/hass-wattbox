"""Data update coordinator for Wattbox integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL, DOMAIN
from .telnet_client import WattboxConnectionError, WattboxTelnetClient

_LOGGER = logging.getLogger(__name__)


class WattboxDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the Wattbox device."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        telnet_client: WattboxTelnetClient,
    ) -> None:
        """Initialize the coordinator."""
        self.telnet_client = telnet_client
        self.config_entry = config_entry

        # Get polling interval from config
        polling_interval = config_entry.data.get(
            CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=polling_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            # Ensure we're connected
            if not self.telnet_client.is_connected:
                await self.telnet_client.async_connect()

            # Get device info
            device_info = await self.telnet_client.async_get_device_info()

            # Get outlet status (assuming 18 outlets for 800 series)
            outlet_info = await self.telnet_client.async_get_outlet_status(18)

            # Get status monitoring data (includes power status via telnet)
            status_info = await self.telnet_client.async_get_status_info()

            # Extract power metrics from status_info for backward compatibility
            power_status = status_info.get("power_status", {})
            voltage = power_status.get("voltage")
            current = power_status.get("current")
            power = power_status.get("power")

            # Log the status info for debugging
            _LOGGER.debug("Status info: %s", status_info)
            _LOGGER.debug("Power status: %s", power_status)
            _LOGGER.debug(
                "Extracted metrics - voltage: %s, current: %s, power: %s",
                voltage,
                current,
                power,
            )

            return {
                "device_info": device_info,
                "outlet_info": outlet_info,
                "voltage": voltage,
                "current": current,
                "power": power,
                "status_info": status_info,
                "connected": True,
            }

        except WattboxConnectionError as err:
            _LOGGER.error("Connection error: %s", err)
            raise UpdateFailed(f"Connection error: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_set_outlet_state(self, outlet_number: int, state: bool) -> None:
        """Set outlet state."""
        try:
            await self.telnet_client.async_set_outlet_state(outlet_number, state)
            # Trigger a data refresh to get updated outlet states
            await self.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to set outlet %d state: %s", outlet_number, err)
            raise

    async def async_disconnect(self) -> None:
        """Disconnect from the device."""
        await self.telnet_client.async_disconnect()
