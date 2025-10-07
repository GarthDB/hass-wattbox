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

# Telnet commands
TELNET_CMD_FIRMWARE: Final[str] = "?Firmware"
TELNET_CMD_MODEL: Final[str] = "?Model"
TELNET_CMD_SERVICE_TAG: Final[str] = "?ServiceTag"
TELNET_CMD_HOSTNAME: Final[str] = "?Hostname"
TELNET_CMD_OUTLET_STATUS: Final[str] = "?OutletStatus"
TELNET_CMD_OUTLET_NAME: Final[str] = "?OutletName"
TELNET_CMD_AUTO_REBOOT: Final[str] = "?AutoReboot"

# Telnet control commands
TELNET_CMD_OUTLET_SET: Final[str] = "!OutletSet"

# Telnet prompts
TELNET_USERNAME_PROMPT: Final[str] = "Username: "
TELNET_PASSWORD_PROMPT: Final[str] = "Password: "
TELNET_LOGIN_SUCCESS: Final[str] = "Successfully Logged In!"

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
