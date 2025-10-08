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
    TELNET_CMD_OUTLET_NAME,
    TELNET_CMD_OUTLET_SET,
    TELNET_CMD_OUTLET_STATUS,
    TELNET_CMD_SERVICE_TAG,
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

        await self._get_firmware_info()
        await self._get_model_info()
        await self._get_service_tag()
        await self._get_hostname()
        await self._get_auto_reboot()

        return self._device_data["device_info"]

    async def _get_firmware_info(self) -> None:
        """Get firmware information."""
        try:
            response = await self.async_send_command(TELNET_CMD_FIRMWARE)
            self._device_data["device_info"]["hardware_version"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get firmware info: %s", e)

    async def _get_model_info(self) -> None:
        """Get model information."""
        try:
            response = await self.async_send_command(TELNET_CMD_MODEL)
            self._device_data["device_info"]["model"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get model info: %s", e)

    async def _get_service_tag(self) -> None:
        """Get service tag information."""
        try:
            response = await self.async_send_command(TELNET_CMD_SERVICE_TAG)
            self._device_data["device_info"]["serial_number"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get service tag: %s", e)

    async def _get_hostname(self) -> None:
        """Get hostname information."""
        try:
            response = await self.async_send_command(TELNET_CMD_HOSTNAME)
            self._device_data["device_info"]["hostname"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get hostname: %s", e)

    async def _get_auto_reboot(self) -> None:
        """Get auto reboot setting."""
        try:
            response = await self.async_send_command(TELNET_CMD_AUTO_REBOOT)
            self._device_data["device_info"]["auto_reboot"] = (
                response.split("=")[1] if "=" in response else None
            )
        except Exception as e:
            _LOGGER.warning("Failed to get auto reboot setting: %s", e)

    async def async_get_outlet_status(
        self, num_outlets: int = 18
    ) -> list[dict[str, Any]]:
        """Get outlet status information."""
        if not self._connected:
            await self.async_connect()

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
            # Due to device's one-command delay, we need to send a dummy command first
            # to get the outlet status response
            await self.async_send_command("?Firmware")  # Dummy command
            response = await self.async_send_command(TELNET_CMD_OUTLET_STATUS)

            # The response should contain the outlet status
            # Look for both ?OutletStatus and ~OutletStatus (after control commands)
            if "=" in response and (
                "OutletStatus" in response or "~OutletStatus" in response
            ):
                outlet_states = response.split("=")[1].split(",")
                for i, state in enumerate(outlet_states):
                    if i < len(self._device_data["outlet_info"]):
                        self._device_data["outlet_info"][i]["state"] = int(state)
        except Exception as e:
            _LOGGER.warning("Failed to get outlet status: %s", e)

    async def _get_outlet_names(self) -> None:
        """Get outlet names."""
        try:
            # Due to device's one-command delay, we need to send a dummy command first
            # to get the outlet names response
            await self.async_send_command("?Firmware")  # Dummy command
            response = await self.async_send_command(TELNET_CMD_OUTLET_NAME)

            # The response should contain the outlet names
            if "=" in response and "OutletName" in response:
                outlet_names = response.split("=")[1].split(",")
                for i, name in enumerate(outlet_names):
                    if i < len(self._device_data["outlet_info"]):
                        # Clean up the name (remove braces)
                        clean_name = name.replace("{", "").replace("}", "")
                        self._device_data["outlet_info"][i]["name"] = clean_name
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
