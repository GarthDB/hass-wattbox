"""Telnet client for Wattbox devices."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import telnetlib3

from .const import (
    TELNET_CMD_AUTO_REBOOT,
    TELNET_CMD_FIRMWARE,
    TELNET_CMD_HOSTNAME,
    TELNET_CMD_MODEL,
    TELNET_CMD_OUTLET_COUNT,
    TELNET_CMD_OUTLET_NAME,
    TELNET_CMD_OUTLET_SET,
    TELNET_CMD_OUTLET_STATUS,
    TELNET_CMD_POWER_STATUS,
    TELNET_CMD_SERVICE_TAG,
    TELNET_CMD_UPS_CONNECTION,
    TELNET_CMD_UPS_STATUS,
    TELNET_LOGIN_SUCCESS,
    TELNET_PASSWORD_PROMPT,
    TELNET_PORT,
    TELNET_TIMEOUT,
    TELNET_USERNAME_PROMPT,
)

_LOGGER = logging.getLogger(__name__)


class WattboxTelnetError(Exception):
    """Base exception for Wattbox Telnet errors."""


class WattboxConnectionError(WattboxTelnetError):
    """Exception raised when connection fails."""


class WattboxAuthenticationError(WattboxTelnetError):
    """Exception raised when authentication fails."""


class WattboxTelnetClient:
    """Telnet client for Wattbox devices."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = TELNET_PORT,
        timeout: int = TELNET_TIMEOUT,
    ) -> None:
        """Initialize the Telnet client."""
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._timeout = timeout
        self._reader: telnetlib3.TelnetReader | None = None
        self._writer: telnetlib3.TelnetWriter | None = None
        self._connected = False
        self._device_data: dict[str, Any] = {
            "device_info": {
                "hardware_version": None,
                "model": None,
                "serial_number": None,
                "hostname": None,
                "auto_reboot": None,
            },
            "outlet_info": [],
            "status_info": {
                "power_status": {
                    "current": None,
                    "power": None,
                    "voltage": None,
                    "safe_voltage": None,
                },
                "ups_status": {
                    "battery_charge": None,
                    "battery_load": None,
                    "battery_health": None,
                    "power_lost": None,
                    "battery_runtime": None,
                    "alarm_enabled": None,
                    "alarm_muted": None,
                },
                "ups_connected": None,
            },
        }

    async def async_connect(self) -> None:
        """Connect to the Wattbox device."""
        try:
            self._reader, self._writer = await asyncio.wait_for(
                telnetlib3.open_connection(self._host, self._port),
                timeout=self._timeout,
            )
            _LOGGER.debug("Connected to %s:%s", self._host, self._port)

            # Wait for username prompt
            await self._wait_for_prompt(TELNET_USERNAME_PROMPT)
            await self._send_command(self._username)

            # Wait for password prompt
            await self._wait_for_prompt(TELNET_PASSWORD_PROMPT)
            await self._send_command(self._password)

            # Wait for login success
            await self._wait_for_prompt(TELNET_LOGIN_SUCCESS)
            self._connected = True
            _LOGGER.debug("Successfully authenticated with %s", self._host)

        except asyncio.TimeoutError as err:
            raise WattboxConnectionError(
                f"Connection timeout to {self._host}:{self._port}"
            ) from err
        except Exception as err:
            raise WattboxConnectionError(
                f"Failed to connect to {self._host}:{self._port}: {err}"
            ) from err

    async def async_disconnect(self) -> None:
        """Disconnect from the Wattbox device."""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        self._connected = False
        _LOGGER.debug("Disconnected from %s", self._host)

    async def _wait_for_prompt(self, prompt: str) -> str:
        """Wait for a specific prompt and return the response."""
        if not self._reader:
            raise WattboxConnectionError("Not connected")

        try:
            response = await asyncio.wait_for(
                self._reader.readuntil(prompt.encode()),
                timeout=self._timeout,
            )
            return response.decode().strip()
        except asyncio.TimeoutError as err:
            raise WattboxConnectionError(
                f"Timeout waiting for prompt: {prompt}"
            ) from err

    async def _send_command(self, command: str) -> None:
        """Send a command to the device."""
        if not self._writer:
            raise WattboxConnectionError("Not connected")

        self._writer.write(command + "\r\n")
        await self._writer.drain()
        _LOGGER.debug("Sent command: %s", command)

    async def async_send_command(self, command: str) -> str:
        """Send a command and return the response."""
        if not self._connected:
            raise WattboxConnectionError("Not connected")

        await self._send_command(command)

        # Read the response
        if not self._reader:
            raise WattboxConnectionError("Not connected")

        try:
            response = await asyncio.wait_for(
                self._reader.readuntil(b"\n"),
                timeout=self._timeout,
            )
            return response.decode().strip()
        except asyncio.TimeoutError as err:
            raise WattboxConnectionError(
                f"Timeout waiting for response to command: {command}"
            ) from err

    async def async_get_device_info(self) -> dict[str, Any]:
        """Get device information."""
        if not self._connected:
            await self.async_connect()

        # Only get device info once per connection to avoid constant changes
        if not self._device_data["device_info"].get("hardware_version"):
            await self._get_firmware_info()
        if not self._device_data["device_info"].get("model"):
            await self._get_model_info()
        if not self._device_data["device_info"].get("serial_number"):
            await self._get_service_tag()
        if not self._device_data["device_info"].get("hostname"):
            await self._get_hostname()
        if not self._device_data["device_info"].get("auto_reboot"):
            await self._get_auto_reboot()

        # Fix field assignments if they appear to be swapped
        self._fix_field_assignments()

        return self._device_data["device_info"]

    def _fix_field_assignments(self) -> None:
        """Fix field assignments if they appear to be swapped."""
        device_info = self._device_data["device_info"]

        # Check if fields appear to be swapped based on their content patterns
        model = device_info.get("model", "")
        serial = device_info.get("serial_number", "")
        hostname = device_info.get("hostname", "")

        # If model looks like firmware version (e.g., "2.8.0.0") and we don't have
        # hardware_version
        if (
            model
            and "." in model
            and len(model.split(".")) == 4
            and not device_info.get("hardware_version")
        ):
            _LOGGER.info(
                "Model field contains firmware version, moving to hardware_version: %s",
                model,
            )
            device_info["hardware_version"] = model
            device_info["model"] = None

        # If serial looks like model number (e.g., "WB-800-IPVM-12") and we don't have model
        if serial and serial.startswith("WB-") and not device_info.get("model"):
            _LOGGER.info(
                "Serial field contains model number, moving to model: %s", serial
            )
            device_info["model"] = serial
            device_info["serial_number"] = None

        # If hostname looks like service tag (e.g., "ST201916431G842A") and we don't
        # have serial_number
        if (
            hostname
            and hostname.startswith("ST")
            and not device_info.get("serial_number")
        ):
            _LOGGER.info(
                "Hostname field contains service tag, moving to serial_number: %s",
                hostname,
            )
            device_info["serial_number"] = hostname
            device_info["hostname"] = None

    async def _get_firmware_info(self) -> None:
        """Get firmware information."""
        try:
            response = await self.async_send_command(TELNET_CMD_FIRMWARE)
            _LOGGER.debug("Firmware response: %s", response)

            if "=" in response:
                firmware_data = response.split("=")[1].strip()
                _LOGGER.debug("Firmware data: %s", firmware_data)
                self._parse_firmware_data(firmware_data)
            else:
                _LOGGER.warning("No firmware data in response: %s", response)
                self._device_data["device_info"]["hardware_version"] = None
        except Exception as e:
            _LOGGER.warning("Failed to get firmware info: %s", e)
            self._device_data["device_info"]["hardware_version"] = None

    def _parse_firmware_data(self, firmware_data: str) -> None:
        """Parse firmware data from device response."""
        if not firmware_data or firmware_data == "0,0,Good,False,0,False,False":
            self._device_data["device_info"]["hardware_version"] = "Unknown"
            return

        parts = firmware_data.split(",")

        if len(parts) == 1:
            self._parse_simple_firmware(parts[0].strip())
        elif len(parts) >= 2:
            self._parse_complex_firmware(parts[0].strip(), parts[1].strip())
        else:
            _LOGGER.warning("Invalid firmware data format: %s", firmware_data)
            self._device_data["device_info"]["hardware_version"] = "Unknown"

    def _parse_simple_firmware(self, firmware_version: str) -> None:
        """Parse simple firmware format (e.g., '1.0.0')."""
        if firmware_version and firmware_version != "0":
            self._update_firmware_if_different(firmware_version)
        else:
            self._device_data["device_info"]["hardware_version"] = "Unknown"

    def _parse_complex_firmware(self, version: str, revision: str) -> None:
        """Parse complex firmware format (version,revision,status,flags)."""
        if not self._validate_firmware_values(version, revision):
            return

        if version and revision and version != "0" and revision != "0":
            firmware_version = f"{version}.{revision}"
            self._update_firmware_if_different(firmware_version)
        else:
            self._device_data["device_info"]["hardware_version"] = "Unknown"

    def _validate_firmware_values(self, version: str, revision: str) -> bool:
        """Validate that values look like firmware, not power readings."""
        try:
            version_float = float(version)
            revision_float = float(revision)

            # If values are too large, this might be power data, not firmware
            if version_float > 10 or revision_float > 10:
                _LOGGER.warning(
                    "Firmware data looks like power readings: %s,%s. Skipping.",
                    version,
                    revision,
                )
                self._device_data["device_info"]["hardware_version"] = "Unknown"
                return False

        except ValueError:
            _LOGGER.warning("Invalid firmware data format: %s,%s", version, revision)
            self._device_data["device_info"]["hardware_version"] = "Unknown"
            return False

        return True

    def _update_firmware_if_different(self, firmware_version: str) -> None:
        """Update firmware version only if it's different."""
        current_firmware = self._device_data["device_info"].get("hardware_version")
        if current_firmware != firmware_version:
            _LOGGER.info("Firmware version: %s", firmware_version)
            self._device_data["device_info"]["hardware_version"] = firmware_version

    async def _get_model_info(self) -> None:
        """Get model information."""
        try:
            response = await self.async_send_command(TELNET_CMD_MODEL)
            _LOGGER.debug("Model response: %s", response)
            if "=" in response:
                model_data = response.split("=")[1].strip()
                _LOGGER.debug("Model data: %s", model_data)
                # The ?Model command should return the actual model number like
                # "WB-800-IPVM-6" But if we're getting firmware version, we need to
                # handle it differently
                if model_data and not model_data.startswith("WB-"):
                    # If it looks like firmware version (e.g., "2.8.0.0"), this might be
                    # wrong command
                    _LOGGER.warning(
                        "Model data looks like firmware version: %s", model_data
                    )
                    self._device_data["device_info"]["model"] = None
                else:
                    self._device_data["device_info"]["model"] = model_data
            else:
                self._device_data["device_info"]["model"] = None
        except Exception as e:
            _LOGGER.warning("Failed to get model info: %s", e)
            self._device_data["device_info"]["model"] = None

    async def _get_service_tag(self) -> None:
        """Get service tag information."""
        try:
            response = await self.async_send_command(TELNET_CMD_SERVICE_TAG)
            _LOGGER.debug("Service tag response: %s", response)
            if "=" in response:
                service_tag = response.split("=")[1].strip()
                _LOGGER.debug("Service tag data: %s", service_tag)
                # The ?ServiceTag command should return the service tag like
                # "ST191500681E8422" But if we're getting model number, we need to
                # handle it differently
                if service_tag and service_tag.startswith("WB-"):
                    # If it looks like model number (e.g., "WB-800-IPVM-12"), this might
                    # be wrong command
                    _LOGGER.warning(
                        "Service tag data looks like model number: %s", service_tag
                    )
                    self._device_data["device_info"]["serial_number"] = None
                else:
                    self._device_data["device_info"]["serial_number"] = service_tag
            else:
                self._device_data["device_info"]["serial_number"] = None
        except Exception as e:
            _LOGGER.warning("Failed to get service tag: %s", e)
            self._device_data["device_info"]["serial_number"] = None

    async def _get_hostname(self) -> None:
        """Get hostname information."""
        try:
            response = await self.async_send_command(TELNET_CMD_HOSTNAME)
            _LOGGER.debug("Hostname response: %s", response)
            if "=" in response:
                hostname = response.split("=")[1].strip()
                _LOGGER.debug("Hostname data: %s", hostname)
                # The ?Hostname command should return the hostname like "WattBox"
                # But if we're getting service tag, we need to handle it differently
                if hostname and hostname.startswith("ST") and len(hostname) > 10:
                    # If it looks like service tag (e.g., "ST201916431G842A"), this might
                    # be wrong command
                    _LOGGER.warning(
                        "Hostname data looks like service tag: %s", hostname
                    )
                    self._device_data["device_info"]["hostname"] = None
                else:
                    self._device_data["device_info"]["hostname"] = hostname
            else:
                self._device_data["device_info"]["hostname"] = None
        except Exception as e:
            _LOGGER.warning("Failed to get hostname: %s", e)
            self._device_data["device_info"]["hostname"] = None

    async def _get_auto_reboot(self) -> None:
        """Get auto reboot setting."""
        try:
            response = await self.async_send_command(TELNET_CMD_AUTO_REBOOT)
            self._device_data["device_info"]["auto_reboot"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get auto reboot setting: %s", e)

    async def _get_outlet_count(self) -> int:
        """Get the number of outlets on the device."""
        try:
            # First command returns empty, second command returns the first command's response
            await self.async_send_command(TELNET_CMD_OUTLET_COUNT)  # This returns empty
            response = await self.async_send_command(
                "?Firmware"
            )  # This returns the outlet count

            if "=" in response and "OutletCount" in response:
                count = int(response.split("=")[1])
                _LOGGER.debug("Device has %d outlets", count)
                return count
            else:
                _LOGGER.warning("Could not get outlet count, defaulting to 12")
                return 12
        except Exception as e:
            _LOGGER.warning("Failed to get outlet count: %s, defaulting to 12", e)
            return 12

    async def async_get_outlet_status(
        self, num_outlets: int = None
    ) -> list[dict[str, Any]]:
        """Get outlet status information."""
        if not self._connected:
            await self.async_connect()

        # Get the actual number of outlets from the device if not specified
        if num_outlets is None:
            num_outlets = await self._get_outlet_count()

        # Initialize outlet info if not already done
        if not self._device_data["outlet_info"]:
            self._device_data["outlet_info"] = [
                {"state": 0, "name": f"Outlet {i + 1}"} for i in range(num_outlets)
            ]

        await self._get_outlet_states()
        await self._get_outlet_names()

        return self._device_data["outlet_info"]

    async def _get_outlet_states(self) -> None:
        """Get outlet states."""
        try:
            # The device has a command delay - each command returns the response
            # from the previous command. We need to send a dummy command first
            # to get the outlet status response
            await self.async_send_command("?Firmware")  # This returns empty
            await self.async_send_command(
                TELNET_CMD_OUTLET_STATUS
            )  # This returns the outlet status
            response = await self.async_send_command(
                "?Firmware"
            )  # This returns the outlet status

            _LOGGER.debug("Outlet status response: %s", response)

            # The outlet status comes back as the response to the second dummy command
            if "=" in response and "OutletStatus" in response:
                outlet_states = response.split("=")[1].split(",")
                _LOGGER.debug("Parsed outlet states: %s", outlet_states)

                # Process only the number of outlets we have
                num_outlets = min(
                    len(outlet_states), len(self._device_data["outlet_info"])
                )
                for i in range(num_outlets):
                    self._device_data["outlet_info"][i]["state"] = int(outlet_states[i])
                    _LOGGER.debug(
                        "Set outlet %d state to %d", i + 1, int(outlet_states[i])
                    )
            else:
                _LOGGER.warning("No valid outlet status response found: %s", response)
        except Exception as e:
            _LOGGER.warning("Failed to get outlet status: %s", e)

    async def _get_outlet_names(self) -> None:
        """Get outlet names."""
        try:
            # The device has a command delay - each command returns the response
            # from the previous command. We need to send a dummy command first
            # to get the outlet names response
            await self.async_send_command("?Firmware")  # This returns empty
            await self.async_send_command(
                TELNET_CMD_OUTLET_NAME
            )  # This returns the outlet names
            response = await self.async_send_command(
                "?Firmware"
            )  # This returns the outlet names

            _LOGGER.debug("Outlet names response: %s", response)

            # The response should contain the outlet names
            if "=" in response and "OutletName" in response:
                outlet_names = response.split("=")[1].split(",")
                _LOGGER.debug("Parsed outlet names: %s", outlet_names)

                # Process only the number of outlets we have
                num_outlets = min(
                    len(outlet_names), len(self._device_data["outlet_info"])
                )
                for i in range(num_outlets):
                    # Clean up the name (remove braces)
                    clean_name = outlet_names[i].replace("{", "").replace("}", "")
                    self._device_data["outlet_info"][i]["name"] = clean_name
                    _LOGGER.debug("Set outlet %d name to %s", i + 1, clean_name)
            else:
                _LOGGER.warning("No valid outlet names response found: %s", response)
        except Exception as e:
            _LOGGER.warning("Failed to get outlet names: %s", e)

    async def async_set_outlet_state(self, outlet_number: int, state: bool) -> None:
        """Set outlet state (on/off)."""
        if not self._connected:
            await self.async_connect()

        command = f"{TELNET_CMD_OUTLET_SET}={outlet_number},{'ON' if state else 'OFF'}"
        try:
            await self.async_send_command(command)
            _LOGGER.debug(
                "Set outlet %d to %s", outlet_number, "ON" if state else "OFF"
            )

            # Update the internal state directly since we know what we set
            if 1 <= outlet_number <= len(self._device_data["outlet_info"]):
                self._device_data["outlet_info"][outlet_number - 1]["state"] = (
                    1 if state else 0
                )
                _LOGGER.debug(
                    "Updated internal state for outlet %d to %d",
                    outlet_number,
                    1 if state else 0,
                )

        except Exception as e:
            _LOGGER.error("Failed to set outlet %d state: %s", outlet_number, e)
            raise

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self._connected

    @property
    def device_data(self) -> dict[str, Any]:
        """Return current device data."""
        return self._device_data

    async def async_get_power_metrics(self) -> dict[str, Any]:
        """Get power metrics (voltage, current, power) via HTTP.

        Note: Currently returns placeholder values as HTTP authentication
        is not working with the device. This can be extended later when
        the correct authentication method is determined.
        """
        _LOGGER.debug("Power monitoring requested - returning placeholder values")
        _LOGGER.info(
            "Power monitoring not yet implemented - HTTP authentication failing"
        )

        # Return placeholder values for now
        # TODO: Implement proper HTTP power monitoring when authentication is resolved
        return {"voltage": None, "current": None, "power": None}

    async def async_get_status_info(self) -> dict[str, Any]:
        """Get device status information including power and UPS status."""
        if not self._connected:
            await self.async_connect()

        await self._get_power_status()
        await self._get_ups_connection()
        await self._get_ups_status()

        return self._device_data["status_info"]

    async def _get_power_status(self) -> None:
        """Get power status information."""
        try:
            response = await self.async_send_command(TELNET_CMD_POWER_STATUS)
            _LOGGER.debug("Power status response: %s", response)

            if "=" in response and "PowerStatus" in response:
                # Format: ?PowerStatus=60.00,600.00,110.00,1
                # Where: current, power, voltage, safe_voltage
                values = response.split("=")[1].split(",")
                if len(values) >= 4:
                    self._device_data["status_info"]["power_status"]["current"] = float(
                        values[0]
                    )
                    self._device_data["status_info"]["power_status"]["power"] = float(
                        values[1]
                    )
                    self._device_data["status_info"]["power_status"]["voltage"] = float(
                        values[2]
                    )
                    self._device_data["status_info"]["power_status"]["safe_voltage"] = (
                        int(values[3])
                    )
                    _LOGGER.debug(
                        "Parsed power status: current=%s, power=%s, voltage=%s, "
                        "safe_voltage=%s",
                        values[0],
                        values[1],
                        values[2],
                        values[3],
                    )
        except Exception as e:
            _LOGGER.warning("Failed to get power status: %s", e)

    async def _get_ups_connection(self) -> None:
        """Get UPS connection status."""
        try:
            response = await self.async_send_command(TELNET_CMD_UPS_CONNECTION)
            _LOGGER.debug("UPS connection response: %s", response)

            if "=" in response and "UPSConnection" in response:
                # Format: ?UPSConnection=0 or ?UPSConnection=1
                # 0 = Disconnected, 1 = Connected
                connected = int(response.split("=")[1])
                self._device_data["status_info"]["ups_connected"] = bool(connected)
                _LOGGER.debug("UPS connected: %s", bool(connected))
        except Exception as e:
            _LOGGER.warning("Failed to get UPS connection status: %s", e)

    async def _get_ups_status(self) -> None:
        """Get UPS status information."""
        try:
            response = await self.async_send_command(TELNET_CMD_UPS_STATUS)
            _LOGGER.debug("UPS status response: %s", response)

            if "=" in response and "UPSStatus" in response:
                # Format: ?UPSStatus=50,0,Good,False,25,True,False
                # Where: battery_charge, battery_load, battery_health, power_lost,
                #        battery_runtime, alarm_enabled, alarm_muted
                values = response.split("=")[1].split(",")
                if len(values) >= 7:
                    self._device_data["status_info"]["ups_status"]["battery_charge"] = (
                        int(values[0])
                    )
                    self._device_data["status_info"]["ups_status"]["battery_load"] = (
                        int(values[1])
                    )
                    self._device_data["status_info"]["ups_status"]["battery_health"] = (
                        values[2]
                    )
                    self._device_data["status_info"]["ups_status"]["power_lost"] = (
                        values[3] == "True"
                    )
                    self._device_data["status_info"]["ups_status"][
                        "battery_runtime"
                    ] = int(values[4])
                    self._device_data["status_info"]["ups_status"]["alarm_enabled"] = (
                        values[5] == "True"
                    )
                    self._device_data["status_info"]["ups_status"]["alarm_muted"] = (
                        values[6] == "True"
                    )
                    _LOGGER.debug(
                        "Parsed UPS status: charge=%s%%, load=%s%%, health=%s, "
                        "power_lost=%s, runtime=%smin, alarm_enabled=%s, "
                        "alarm_muted=%s",
                        values[0],
                        values[1],
                        values[2],
                        values[3],
                        values[4],
                        values[5],
                        values[6],
                    )
        except Exception as e:
            _LOGGER.warning("Failed to get UPS status: %s", e)
