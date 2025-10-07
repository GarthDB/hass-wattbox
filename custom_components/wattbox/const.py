"""Constants for the Wattbox integration."""

from __future__ import annotations

from typing import Final

# Base component constants
DOMAIN: Final[str] = "wattbox"
VERSION: Final[str] = "0.1.0"

# Configuration keys
CONF_HOST: Final[str] = "host"
CONF_USERNAME: Final[str] = "username"
CONF_PASSWORD: Final[str] = "password"
CONF_POLLING_INTERVAL: Final[str] = "polling_interval"

# Default values
DEFAULT_POLLING_INTERVAL: Final[int] = 30  # seconds
DEFAULT_USERNAME: Final[str] = "wattbox"
DEFAULT_PASSWORD: Final[str] = "wattbox"

# Telnet configuration
TELNET_PORT: Final[int] = 23
TELNET_TIMEOUT: Final[int] = 10

# Device information
DEVICE_MANUFACTURER: Final[str] = "SnapAV"
DEVICE_MODEL: Final[str] = "Wattbox 800 Series"

# Entity attributes
ATTR_OUTLET_NUMBER: Final[str] = "outlet_number"
ATTR_VOLTAGE: Final[str] = "voltage"
ATTR_CURRENT: Final[str] = "current"
ATTR_POWER: Final[str] = "power"
ATTR_FIRMWARE: Final[str] = "firmware"
ATTR_MODEL: Final[str] = "model"
ATTR_SERIAL: Final[str] = "serial"
ATTR_HOSTNAME: Final[str] = "hostname"
